"""Main entry point for user-management-api FastAPI application."""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import routers
from app.api import hello

# Lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up user-management-api...")
    yield
    # Shutdown
    print("Shutting down user-management-api...")

# Create FastAPI app
app = FastAPI(
    title="user-management-api",
    description="FastAPI microservice",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hello.router, prefix="/api", tags=["health"])

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to user-management-api!"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
