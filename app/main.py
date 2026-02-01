from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import endpoints
from . import database  # Relative import to fix path issues

# --- LIFESPAN (Replaces the deprecated on_event) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the database
    database.init_db()
    print("✅ Database initialized for Dashboard.")
    yield
    # Shutdown: (Optional cleanup code goes here)

# Initialize the App with Lifespan
app = FastAPI(title="Honeypot Agent Backend", lifespan=lifespan)

# Allow connections from anywhere (useful for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect the Logic Routes
app.include_router(endpoints.router, prefix="/api/v1")

# Health Check
@app.get("/")
def health_check():
    return {"status": "running", "mode": "terminal-testing"}

# Run the server
if __name__ == "__main__":
    import uvicorn
    # Make sure this matches your folder structure (app.main:app)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)