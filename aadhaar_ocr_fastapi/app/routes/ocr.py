from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict
from ..services.ocr_service import OCRService
import io

router = APIRouter()
ocr_service = OCRService()

@router.post("/api/ocr/aadhaar")
async def process_aadhaar_image(file: UploadFile = File(...)):
    """
    Process an uploaded Aadhaar card image and extract information using OCR.
    
    Args:
        file: Uploaded image file (PNG, JPG, JPEG)
    
    Returns:
        JSON response containing extracted information
    """
    # Check file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read image content
        image_bytes = await file.read()
        
        # Extract text using OCR
        text = ocr_service.extract_text_from_image(image_bytes)
        print("Extracted Text:>>>>>>", text)
        
        # Parse the extracted text
        result = ocr_service.parse_aadhaar_text(text)
        
        return {
            "status_code": 200,
            "data": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
