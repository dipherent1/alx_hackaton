from app.routers.endpoints.chatRouter import chat_router
from app.routers.endpoints.base import base_router
from fastapi import APIRouter, HTTPException

routerList = [
    chat_router,
    base_router
]

routers = APIRouter()

for router in routerList:
    routers.include_router(router)

def getRouters():
    """
    Returns the list of routers.
    """
    return routers