# Aadhaar OCR Microservice

A FastAPI-based microservice for extracting information from Aadhaar cards using Optical Character Recognition (OCR).

## Project Structure

```
aadhaar_ocr_fastapi/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application entry point
│   ├── routes/              # API route definitions
│   │   └── ocr.py          # OCR API endpoints
│   └── services/            # Business logic services
│       └── ocr_service.py  # OCR processing service
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation
```

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
brew install tesseract       # Install Tesseract OCR engine
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

## Project Flow

1. **Image Upload**
   - User uploads an Aadhaar card image through the API endpoint
   - The image is received as a multipart form data

2. **OCR Processing**
   - The image is processed using PyTesseract OCR engine
   - Text is extracted from the image

3. **Information Extraction**
   - The extracted text is parsed to find specific patterns:
     - Name: Extracted from text above DOB or between DOB and Gender
     - Aadhaar Number: Using regex pattern (4 digits space 4 digits space 4 digits)
     - DOB: Using regex pattern (DD/MM/YYYY)
     - Gender: Looking for keywords like 'Male', 'Female', 'M', 'F'
     - Address: Extracted by identifying address keywords and parsing the text block

4. **Data Cleaning**
   - Text is cleaned to remove special characters
   - Address formatting is standardized
   - Personal information is validated against regex patterns

## Technology Stack

- FastAPI: Modern, fast web framework for building APIs
- PyTesseract: Python wrapper for Google's Tesseract-OCR
- Pillow: Python Imaging Library for image processing
- Python-Multipart: For handling file uploads
- uvicorn: ASGI server implementation for running the application

## Key Features

- Efficient OCR processing using Tesseract
- Robust text pattern matching for accurate information extraction
- Clean and maintainable code structure
- FastAPI's built-in request validation and error handling
- Easy to extend with additional OCR capabilities

## Error Handling

The API includes comprehensive error handling for:
- Invalid image formats
- Missing image uploads
- OCR processing failures
- Pattern matching failures
- Invalid data formats

## Security Considerations

- All Aadhaar numbers are masked in the response (XXXX XXXX XXXX)
- The service doesn't store any Aadhaar images or extracted data
- Input validation is performed at all levels
- Rate limiting can be added for production use

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
