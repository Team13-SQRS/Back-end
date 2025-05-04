from fastapi import FastAPI
from app.routes import notes, auth
from app.database.database import Base, engine
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Create DB tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI()

# Include routers
app.include_router(notes.router, prefix="/api", tags=["notes"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
