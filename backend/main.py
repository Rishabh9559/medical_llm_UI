from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router as chat_router
from services.db_service import db_service
import uvicorn

app = FastAPI(title="Medical LLM Assistant API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and CRA default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)

@app.on_event("startup")
async def startup_event():
    """Connect to database on startup"""
    await db_service.connect()
    print("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await db_service.close()
    print("Closed MongoDB connection")

@app.get("/")
async def root():
    return {"message": "Medical LLM Assistant API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
