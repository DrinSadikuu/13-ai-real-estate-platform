
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.document_service import DocumentService
from pydantic import BaseModel, Field


router = APIRouter(prefix="/documents", tags=["Documents"])

class DocumentSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=20)


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

@router.post("/search")
async def search_documents(
    request: DocumentSearchRequest,
    session: AsyncSession = Depends(get_db),
):
    service = DocumentService(session)

    results = await service.search_documents(
        query=request.query,
        limit=request.limit,
    )

    return {
        "query": request.query,
        "total_results": len(results),
        "results": results,
    }
