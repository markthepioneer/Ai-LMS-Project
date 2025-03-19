# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Database
from .database import engine, Base, get_db
from . import models

# Import all modules
from .finance_module import router as finance_router
from .health_module import router as health_router
from .task_module import router as task_router
from .portfolio_module import router as portfolio_router
from .memory_module import router as memory_router
from .email_module import router as email_router
from .life_balancer_module import router as life_balancer_router

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="AI Life Management System",
    description="A comprehensive AI-powered system for managing all aspects of life",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all module routers
app.include_router(finance_router)
app.include_router(health_router)
app.include_router(task_router)
app.include_router(portfolio_router)
app.include_router(memory_router)
app.include_router(email_router)
app.include_router(life_balancer_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI Life Management System API",
        "documentation": "/docs",
        "modules": [
            "Finance",
            "Health",
            "Task Management",
            "Portfolio Manager",
            "Memory Assistant",
            "Email and Call Handler",
            "Life Balancer"
        ]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# User profile endpoint
@app.get("/profile")
async def get_user_profile(db: Session = Depends(get_db)):
    # In a real implementation, this would get the current user's profile
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "modules_enabled": [
            "finance",
            "health",
            "tasks",
            "portfolio",
            "memory",
            "email",
            "balance"
        ]
    }

# Error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    # Log the error here
    return {"detail": str(exc), "status_code": 500}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)