from fastapi import APIRouter
from . import user_router, admin_router, campaign_router, comment_router


api_router = APIRouter()


api_router.include_router(user_router.router, tags=['User'], prefix='/user')
api_router.include_router(admin_router.router, tags=['Admin'], prefix='/admin')
api_router.include_router(campaign_router.router, tags=['Campaign'], prefix='/campaign')
api_router.include_router(comment_router.router, tags=['Comment'], prefix='/comment')

