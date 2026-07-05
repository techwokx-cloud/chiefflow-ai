from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import ActivityLog, User
from app.schemas import ActivityOut
from app.security import get_current_user

router = APIRouter(prefix="/api/activity", tags=["activity"])


@router.get("", response_model=list[ActivityOut])
def list_activity(limit: int = 50, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    query = (
        select(ActivityLog)
        .where(ActivityLog.org_id == user.org_id)
        .order_by(ActivityLog.created_at.desc())
        .limit(limit)
    )
    return session.exec(query).all()
