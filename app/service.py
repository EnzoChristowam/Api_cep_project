from fastapi import HTTPException 
from fastapi.responses import JSONResponse
from app.client import request_api
from app.model import Adress, CEPResponse, ErrorResponse


#método para retornar o endereço
def formatted_adress(adress:Adress) -> CEPResponse:
    return CEPResponse(endereco=f"{adress.street}, {adress.neighborhood}, {adress.city}/{adress.state}")


async def response_adress(cep:str) -> CEPResponse:

    #Mandando o cep para o método de request_adress e recebendo a resposta.
    adress = await request_api(cep)

    return formatted_adress(adress)