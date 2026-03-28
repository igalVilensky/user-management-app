from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user_routes
from database import engine, Base

app = FastAPI(
    title="User Administration API",
    version="1.0.0",
    description="API for managing users"
)

# Include routers
app.include_router(user_routes.router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Vue dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "User Administration API is running"}

# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)