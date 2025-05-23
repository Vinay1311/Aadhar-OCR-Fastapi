# Aadhaar OCR Microservice

FastAPI-based service for extracting information from Aadhaar cards using OCR.

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
brew install tesseract
```

2. Run the service:
```bash
uvicorn app.main:app --reload
```

## API Usage

### Extract Aadhaar Info

POST `/api/ocr/aadhaar`

Upload an Aadhaar card image (PNG/JPEG) to extract:
- Name
- Aadhaar Number
- DOB
- Gender
- Address

Example Response:
```json
{
    "status": "success",
    "data": {
        "name": "Suresh Kumar",
        "aadhaar_number": "XXXX XXXX XXXX",
        "dob": "1992-06-15",
        "gender": "Male",
        "address": "Full extracted address"
    }
}
```

## Technology Stack

- FastAPI
- PyTesseract
- Pillow
- Python-Multipart
- uvicorn
