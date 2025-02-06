from pydantic import BaseModel
from typing import List, Optional

class EventSchema(BaseModel):
	title: str
	image: str
	description: str
	tags: List[str]
	location: str

	class Config:
		from_attributes = True
		json_schema_extra = {
			"example": {
				"title": "FastAPI Book Launch",
				"image":"https://linktomyimage.com/image.png",
				"description":"We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
				"tags": ["python", "fastapi", "book", "launch"],
				"location": "Google Meet"
			}
		}

class EventResponse(EventSchema):
	id: int

	class Config:
		from_attributes = True
		json_schema_extra = {
			"example": {
				"id": 1,
				"title": "FastAPI Book Launch",
				"image":"https://linktomyimage.com/image.png",
				"description":"We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
				"tags": ["python", "fastapi", "book", "launch"],
				"location": "Google Meet"
			}
		}

class EventUpdate(BaseModel):
	title: Optional[str] = None
	image: Optional[str] = None
	description: Optional[str] = None
	tags: Optional[List[str]] = None
	location: Optional[str] = None

	class Config:
		from_attributes = True
		json_schema_extra = {
			"example": {
				"title": "FastAPI Book Launch",
				"image": "https://linktomyimage.com/image.png",
                                "description": "We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
				"tags": ["python", "fastapi", "book", "launch"],
				"location": "Google Meet"
			}
		}


