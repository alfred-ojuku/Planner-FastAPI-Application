from pydantic import BaseModel, EmailStr
from typing import Optional, List
from models.events import EventSchema

class BaseUser(BaseModel):
    email: EmailStr
    username: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@pack.com",
                "username": "Fast API"
            }
        }

class NewUser(BaseUser):
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@pack.com",
                "username": "Fast API",
                "password": "strong!!!"
            }
        }

class UserSignIn(NewUser):
	username: Optional[None] = None

	class Config:
		json_schema_extra = {
			"example": {
				"email": "fastapi@pack.com",
				"password": "strong!!!"
			}
		}

class User(BaseUser):
    events: Optional[List[str]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@pack.com",
                "username": "Fast API",
                "events": []
            }
        }

