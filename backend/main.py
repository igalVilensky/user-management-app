from fastapi import FastAPI
import uvicorn
from routers import user_routes
from fastapi.middleware.cors import CORSMiddleware
from models import Base
from database import engine

app = FastAPI()
app.include_router(user_routes.router)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Backend is running"}

# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)