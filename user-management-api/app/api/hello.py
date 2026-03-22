"""Hello API endpoint."""
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class HelloResponse(BaseModel):
    """Response model for hello endpoint."""
    message: str
    timestamp: datetime


@router.get("/hello", response_model=HelloResponse)
async def hello():
    """Hello endpoint."""
    return HelloResponse(
        message="Hello from FastAPI!",
        timestamp=datetime.now(),
    )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
