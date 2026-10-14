
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile

from app.services.s3_service import S3Service


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_content = await file.read()

    file_key = f"ai-real-estate/property-documents/{uuid4()}.pdf"

    s3_service = S3Service()
    s3_service.upload_file(file_content, file_key)

    return {
        "filename": file.filename,
        "s3_key": file_key,
        "message": "Document uploaded successfully",
    }
