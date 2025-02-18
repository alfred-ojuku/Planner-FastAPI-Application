from fastapi import APIRouter, HTTPException, Depends, Request, status
from database.connections import get_db, Event, User
from models.events import EventSchema, EventUpdate, EventResponse
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from auth.authenticate import authenticate

event_router = APIRouter(tags=["Events"])

@event_router.post("/new", status_code=status.HTTP_201_CREATED)
async def create_event(new_event: EventSchema, user:str = Depends(authenticate), session = Depends(get_db)) -> dict:
	db_user = session.query(User).filter(User.email == user).first()

	if not db_user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {new_event.event_owner} does not exists")

	event = Event(
		title = new_event.title,
		image = new_event.image,
		description = new_event.description,
		tags = new_event.tags,
		location = new_event.location,
		owner_id = db_user.id
		)

	session.add(event)
	session.commit()
	session.refresh(event)

	return {"message": "Event created successfully"}

@event_router.get("/", response_model=List[EventResponse])
async def retrieve_all_events(user: str = Depends(authenticate), session = Depends(get_db)) -> List[EventSchema]:
	return session.query(Event).all()

@event_router.get("/{id}", response_model=EventResponse)
async def retrieve_event(id:int, user: str = Depends(authenticate), session = Depends(get_db)) -> EventSchema:

	event = session.query(Event).filter(Event.id == id).first()
	
	if not event:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id {id} does not exist")
	
	return event

@event_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(id: int, user: str = Depends(authenticate), session = Depends(get_db)) -> None:
	event = session.query(Event).filter(Event.id == id).first()
	owner = session.query(User).filter(User.email == user).first()

	if not event:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id {id} does not exist")
	
	if owner.id != event.owner_id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not allowed")

	try:
		session.delete(event)
		session.commit()
	except SQLAlchemyError as e:
		session.rollback()
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

@event_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_events(confirm: bool = False, user:str = Depends(authenticate), session=Depends(get_db)) -> None:
	if not confirm:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Confirm required. Set confirm=true to delete all events")

	try:
		session.query(Event).delete()
		session.commit()
	except SQLAlchemyError as e:
		session.rollback()
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")

@event_router.put("/{id}", response_model=EventUpdate)
async def update_event(id:int, new_data:EventUpdate, user: str = Depends(authenticate), session = Depends(get_db)) -> EventSchema:
	event = session.query(Event).filter(Event.id == id).first()
	owner = session.query(User).filter(User.email == user).first()

	if not event:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Event with id {id} does not exist")
	
	if owner.id != event.owner_id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not allowed")
	
	event_data = new_data.model_dump(exclude_unset=True)

	for key, value in event_data.items():
		setattr(event, key, value)

	session.commit()
	session.refresh(event)


	return event
