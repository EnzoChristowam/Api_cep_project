from fastapi import HTTPException 
import httpx
import certifi
import ssl
from app.model import Adress

async def request_api(cep:str):
     
    url = f'https://brasilapi.com.br/api/cep/v2/{cep}'

    try:
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.get(url, timeout=10.0)

            return resp
                 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno {e}")