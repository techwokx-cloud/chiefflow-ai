from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import WorkflowItem, User, ApprovalRequest, ActivityLog
from app.schemas import WorkflowItemCreate, WorkflowItemOut, ApprovalDecision
from app.security import get_current_user
from app.agents.manager import process_item, execute_approved

router = APIRouter(prefix="/api/inbox", tags=["inbox"])


@router.get("", response_model=list[WorkflowItemOut])
def list_items(status: str | None = None, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    query = select(WorkflowItem).where(WorkflowItem.org_id == user.org_id)
    if status:
        query = query.where(WorkflowItem.status == status)
    query = query.order_by(WorkflowItem.created_at.desc())
    return session.exec(query).all()


@router.get("/{item_id}", response_model=WorkflowItemOut)
def get_item(item_id: str, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    item = session.get(WorkflowItem, item_id)
    if not item or item.org_id != user.org_id:
        raise HTTPException(status_code=404, detail="Not found")
    return item


@router.post("", response_model=WorkflowItemOut)
async def create_item(payload: WorkflowItemCreate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    item = WorkflowItem(org_id=user.org_id, **payload.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    item = await process_item(session, item)
    return item


@router.post("/{item_id}/reprocess", response_model=WorkflowItemOut)
async def reprocess_item(item_id: str, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    item = session.get(WorkflowItem, item_id)
    if not item or item.org_id != user.org_id:
        raise HTTPException(status_code=404, detail="Not found")
    item = await process_item(session, item)
    return item


@router.post("/{item_id}/approve", response_model=WorkflowItemOut)
async def approve_item(item_id: str, decision: ApprovalDecision, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    item = session.get(WorkflowItem, item_id)
    if not item or item.org_id != user.org_id:
        raise HTTPException(status_code=404, detail="Not found")

    approval = session.exec(
        select(ApprovalRequest).where(ApprovalRequest.workflow_item_id == item_id, ApprovalRequest.status == "pending")
    ).first()
    if approval:
        approval.status = "approved" if decision.approve else "rejected"
        approval.resolved_by = user.id
        from datetime import datetime
        approval.resolved_at = datetime.utcnow()
        session.add(approval)

    if decision.approve:
        item = await execute_approved(session, item)
        session.add(ActivityLog(
            org_id=user.org_id, workflow_item_id=item_id, actor=f"user:{user.full_name}",
            action="approved_action", detail=decision.note or "Approved by human reviewer",
        ))
    else:
        item.status = "rejected"
        session.add(item)
        session.add(ActivityLog(
            org_id=user.org_id, workflow_item_id=item_id, actor=f"user:{user.full_name}",
            action="rejected_action", detail=decision.note or "Rejected by human reviewer",
        ))
        session.commit()
        session.refresh(item)

    return item


@router.post("/{item_id}/archive", response_model=WorkflowItemOut)
def archive_item(item_id: str, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    item = session.get(WorkflowItem, item_id)
    if not item or item.org_id != user.org_id:
        raise HTTPException(status_code=404, detail="Not found")
    item.status = "archived"
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
