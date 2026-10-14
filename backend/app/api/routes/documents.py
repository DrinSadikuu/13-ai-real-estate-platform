
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.document_service import DocumentService


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
):
    file_content = await file.read()

    service = DocumentService(session)

    return await service.process_document(
        filename=file.filename,
        file_content=file_content,
    )
