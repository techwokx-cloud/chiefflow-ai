from fastapi import APIRouter, Depends, UploadFile, File, Form

from sqlmodel import Session

from app.database import get_session
from app.models import WorkflowItem, User
from app.schemas import WorkflowItemOut
from app.security import get_current_user
from app.services.document_processor import extract_text_from_upload
from app.agents.manager import process_item

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload", response_model=WorkflowItemOut)
async def upload_document(
    file: UploadFile = File(...),
    title: str | None = Form(None),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    file_bytes = await file.read()
    text = extract_text_from_upload(file.filename, file_bytes)
    source = "pdf" if file.filename.lower().endswith(".pdf") else "docx"

    item = WorkflowItem(
        org_id=user.org_id,
        source=source,
        title=title or file.filename,
        raw_text=text or "(No extractable text found in document)",
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    item = await process_item(session, item)
    return item
