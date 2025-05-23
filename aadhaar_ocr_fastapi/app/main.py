from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import ocr

app = FastAPI(
    title="Aadhaar OCR Microservice",
    description="Microservice for extracting information from Aadhaar cards using OCR",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ocr.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Aadhaar OCR Microservice"}
