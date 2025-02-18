from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String, JSON

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, pool_size=10, max_overflow=20, pool_timeout=30)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Event(Base):
	__tablename__ = "events"

	id = Column(Integer, primary_key=True, autoincrement=True, index=True)
	title = Column(String, index=True)
	image = Column(String)
	description = Column(String)
	tags = Column(JSON)
	location = Column(String)
	owner_id = Column(Integer)

	@staticmethod
	def example():
		return {
			"title":"FastAPI Book Launch",
			"image": "https://linktomyimage.com/image.png",
			"description":"We will be discussing the contents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
			"tags": ["python", "fastapi", "book", "launch"],
            		"location": "Google Meet",
			"event_owner": "fastapi@pack.com"
		}

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, autoincrement=True, index=True)
	username = Column(String, index=True)
	email = Column(String)
	password_hash = Column(String)

def initialize_db():
	Base.metadata.create_all(bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
