from fastapi import FastAPI
from app.api.routes import notes
from app.database.database import Base, engine
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Create DB tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI()

# Include routers
app.include_router(notes.router, prefix="/api", tags=["notes"])
