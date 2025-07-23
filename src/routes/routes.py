from fastapi import APIRouter
from modules.beach_profile.controllers.beach_profile_controller import router as beach_profile_router

router = APIRouter()

def include_routes():
    mapped_routes = [
        beach_profile_router
    ]
    
    for route in mapped_routes:
        router.include_router(route)

include_routes()