from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token
from models.users import User, NewUser, TokenResponse
from database.connections import get_db, User
from auth.hash_password import HashPassword

hash_password = HashPassword()

user_router = APIRouter(tags=["User"])

@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def sign_new_user(data: NewUser, session = Depends(get_db)) -> dict:
	db_user = session.query(User).filter(User.email == data.email).first()

	if db_user:
		raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="The user with the email provided already exists")
	
	new_user = User(username=data.username,
			            email=data.email,
			            password_hash=hash_password.create_hash(data.password)	
		             )

	session.add(new_user)
	session.commit()
	session.refresh(new_user)
	
	return {"message": "User successfully registered"}

@user_router.post("/token", response_model=TokenResponse)
async def get_token(data: OAuth2PasswordRequestForm = Depends(), session = Depends(get_db)) -> dict:
	db_user = session.query(User).filter(User.email == data.username).first()

	if not db_user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

	if hash_password.verify_hash(data.password, db_user.password_hash):
		access_token = create_access_token(db_user.email)
		return {"access_token":access_token, "token_type": "Bearer"}
	else:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong credentials passed")
