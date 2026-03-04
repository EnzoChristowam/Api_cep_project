from fastapi.responses import JSONResponse
from app.model import CEPResponse, ErrorResponse
from fastapi import APIRouter
from app.service import response_adress

router = APIRouter()

@router.get("/cep/v1/{cep}",
            response_class=JSONResponse,
            responses={
                400: {"model": ErrorResponse, "description": "CEP inválido"},
                404: {"model": ErrorResponse, "description": "CEP não encontrado"},
                500: {"model": ErrorResponse, "description": "Erro interno"},
            })
async def get_cep_and_response(cep:str):
    return await response_adress(cep)