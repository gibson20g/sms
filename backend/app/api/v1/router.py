from fastapi import APIRouter
from app.api.v1.endpoints import auth, profiles, conversations, messages, statuses

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["Profiles"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["Conversations"])
api_router.include_router(messages.router, prefix="/messages", tags=["Messages"])
api_router.include_router(statuses.router, prefix="/statuses", tags=["Statuses"])
