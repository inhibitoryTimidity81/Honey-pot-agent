from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import endpoints

# Initialize the App
app = FastAPI(title="Honeypot Agent Backend")

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
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)