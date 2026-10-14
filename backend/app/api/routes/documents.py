from app.services.pdf_service import InvalidPDFError, EmptyPDFError
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.db.database import get_db
from app.services.document_service import DocumentService
from pydantic import BaseModel, Field


router = APIRouter(prefix="/documents", tags=["Documents"])

class DocumentSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    limit: int = Field(default=5, ge=1, le=20)
    document_id: UUID | None = None


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_db),
):
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    # 1. Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="Only PDF files are supported",
        )

    # 2. Read file with size limit
    file_content = await file.read(MAX_FILE_SIZE + 1)

    # 3. Validate file size
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size exceeds the 10 MB limit",
        )

    # 4. Validate PDF signature
    if not file_content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file",
        )

    # 5. Process validated document
    service = DocumentService(session)

    try:
        result = await service.process_document(
            filename=file.filename,
            file_content=file_content,
        )

    except InvalidPDFError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except EmptyPDFError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return result

@router.post("/search")
async def search_documents(
    request: DocumentSearchRequest,
    session: AsyncSession = Depends(get_db),
):
    service = DocumentService(session)

    results = await service.search_documents(
        query=request.query,
        limit=request.limit,
        document_id=request.document_id,
    )

    return {
        "query": request.query,
        "total_results": len(results),
        "results": results,
    }

@router.get("/")
async def get_all_documents(session: AsyncSession = Depends(get_db)):
    service = DocumentService(session)

    return await service.get_all_documents()

@router.get("/{document_id}")
async def get_document_by_id(
        document_id:UUID,
        session: AsyncSession = Depends(get_db),
):
    service = DocumentService(session)
    document = await service.get_document_by_id(document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return document

@router.get("/{document_id}/download")
async def get_document_download_url(
        document_id: UUID,
        session: AsyncSession = Depends(get_db),
):
    service = DocumentService(session)

    result = await service.get_document_download_url(document_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return result

@router.delete("/{document_id}")
async def delete_document(
    document_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    service = DocumentService(session)

    deleted = await service.delete_document(document_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return {
        "message": "Document deleted successfully",
        "document_id": str(document_id),
    }
