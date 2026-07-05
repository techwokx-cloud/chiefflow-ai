from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import User, Organization
from app.schemas import SignupRequest, LoginRequest, TokenResponse
from app.security import hash_password, verify_password, create_access_token
from app.seed import seed_agents_for_org, seed_demo_workflow_items

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(payload: SignupRequest, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    org = Organization(name=payload.org_name)
    session.add(org)
    session.commit()
    session.refresh(org)

    user = User(
        org_id=org.id, email=payload.email, full_name=payload.full_name,
        hashed_password=hash_password(payload.password), role="owner",
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    seed_agents_for_org(session, org.id)

    token = create_access_token(user.id, org.id)
    return TokenResponse(access_token=token, user_id=user.id, org_id=org.id, full_name=user.full_name)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user.id, user.org_id)
    return TokenResponse(access_token=token, user_id=user.id, org_id=user.org_id, full_name=user.full_name)


@router.post("/demo-login", response_model=TokenResponse)
async def demo_login(session: Session = Depends(get_session)):
    """One-click demo access - no signup/login required. Uses (or creates) a seeded demo org
    that's pre-populated with realistic, already-processed workflow items."""
    user = session.exec(select(User).where(User.email == "demo@chiefflow.ai")).first()
    if not user:
        org = Organization(name="ChiefFlow Demo Co.")
        session.add(org)
        session.commit()
        session.refresh(org)
        user = User(
            org_id=org.id, email="demo@chiefflow.ai", full_name="George Jabley",
            hashed_password=hash_password("demo-password"), role="owner",
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        seed_agents_for_org(session, org.id)

    await seed_demo_workflow_items(session, user.org_id)
    token = create_access_token(user.id, user.org_id)
    return TokenResponse(access_token=token, user_id=user.id, org_id=user.org_id, full_name=user.full_name)
