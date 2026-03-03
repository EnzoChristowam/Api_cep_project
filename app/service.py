from fastapi import HTTPException 
from fastapi.responses import JSONResponse
from app.client import request_api
from app.model import Adress


#método para retornar o endereço
def formatted_adress(adress:Adress) -> dict:
    return {"Endereço":adress.street+", "+adress.neighborhood+", "+adress.city+"/"+adress.state}


async def response_adress(cep:str):

    #Mandando o cep para o método de request_adress e recebendo a resposta.
    resp_api = await request_api(cep)

    #Recebendo a informação e validando a questão de algum erro
    #tratando o erro
    if resp_api.status_code != 200:
        if resp_api.status_code == 400:
            return JSONResponse(
                status_code=400,
                content={
                    "name": "BadRequestError",
                    "message": "O CEP deve conter exatamente 8 dígitos numéricos",
                    "type": "validation_error"
                })
        elif resp_api.status_code == 404:
            return JSONResponse(
                status_code=404,
                content={
                    "name": "NotFoundError",
                    "message": "CEP NAO ENCONTRADO",
                    "type": "service_error"
                })
        elif resp_api.status_code == 500:
            return JSONResponse(
                status_code=500,
                content={
                    "name": "InternalError",
                    "message": "Erro interno no serviço de CEP",
                    "type": "internal_error"
                })
        else:
            raise HTTPException(status_code=503, detail="Serviço indisponível no momento")   

    #Habilitar a resposta para a classe Adress
    data = resp_api.json()
    adress = Adress(**data)

    return formatted_adress(adress)

