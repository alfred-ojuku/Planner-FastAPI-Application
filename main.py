from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse
from routes.users import user_router
from routes.events import event_router
from database.connections import get_db
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
	get_db()
	
	yield

app = FastAPI(lifespan=lifespan)

# Register routes
app.include_router(user_router, prefix="/users")
app.include_router(event_router, prefix="/events")

@app.get("/")
async def home():
	return RedirectResponse(url="/event/")

if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
