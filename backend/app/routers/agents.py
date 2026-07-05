from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Agent, User
from app.schemas import AgentOut
from app.security import get_current_user

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("", response_model=list[AgentOut])
def list_agents(user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return session.exec(select(Agent).where(Agent.org_id == user.org_id)).all()
