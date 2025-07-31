from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi import Depends
from modules.beach_profile.services.create_beach_profile_service import CreateBeachProfileService
from src.dependencies.injections import get_create_beach_profile_service
from typing import Optional

router = APIRouter()

class BeachProfileRequest(BaseModel):
    profile_file_name: str
    wave_data_file_name: Optional[str] = None

@router.post("/beach-profile", status_code=201)
async def create_profiles(
    request: BeachProfileRequest,
    service: CreateBeachProfileService = Depends(get_create_beach_profile_service)
):
    try:
        result = service.create_profiles_from_csv(request.profile_file_name, request.wave_data_file_name)
        return {
            "message": "Success",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))