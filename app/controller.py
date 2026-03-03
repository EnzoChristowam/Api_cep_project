
from fastapi import APIRouter
from app.service import response_adress

router = APIRouter()

@router.get("/cep/v1/{cep}")
async def get_cep_and_response(cep:str):
    return await response_adress(cep)