from fastapi import Depends
from modules.storage.storage_service import StorageService
from modules.beach_profile.services.create_beach_profile_service import CreateBeachProfileService
from modules.wave.services.calculate_wave_break_service import CalculateWaveBreakService

def get_storage_service():
    return StorageService()

def get_calculate_wave_break_service():
    return CalculateWaveBreakService()

def get_create_beach_profile_service(
    storage_service: StorageService = Depends(get_storage_service),
    calculate_wave_break_service: CalculateWaveBreakService = Depends(get_calculate_wave_break_service),
):
    return CreateBeachProfileService(storage_service, calculate_wave_break_service)
