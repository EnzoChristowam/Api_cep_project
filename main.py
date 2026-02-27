from pydantic import BaseModel, validator
from fastapi import FastAPI, HTTPException 
import certifi
import json
import asyncio
import httpx

app = FastAPI()
    

class Adress(BaseModel):
    cep:str
    state:str
    city:str
    neighborhood:str
    street:str
    service:str
    location:dict

    #Nesta etapa eu estou validando se o cep pego e armazenado na classe tem 8 numeros
    @validator("cep")
    def cep_must_have_eight_nums(cls, cep:str)->str:
        if len(cep)!=8 or not cep.isdigit():
            raise ValueError("cep must have eight numbers")
        return cep
    
    def __init__(self, cep, state, city, neighborhood, street, service, location):
           self.cep = cep
           self.state = state
           self.city = city
           self.neighborhood = neighborhood
           self.street = street
           self.service = service
           self.location = location


#método para retornar o endereço
def return_adress(adress:Adress) -> dict:
    return {"Rua":adress.street,
            "Bairro":adress.neighborhood,
            "Cidade/Sigla do estado":adress.city+"/"+adress.state}
    



#método para conseguir realizar a requisição e devolvendo a mensagem correspondente conforme o erro que pode ser gerado
async def request_adress(cep:str):
     
    url = f'https://brasilapi.com.br/api/cep/v2/89220333'

    try:
        async with httpx.AsyncClient as client:
            resp = await client.get(url, timeout=10.0)

            return resp
                 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno {e}")
    






@app.get("/cep/v2/{cep}")
async def get_cep_and_response(cep:str):

    #validação
    if len(cep)!=8 or not cep.isdigit():
            raise HTTPException(status_code=400, detail="O cep deve ter 8 NÚMEROS")

    #Mandando o cep para o método de request_adress e recebendo a resposta.
    resp_api = await request_adress(cep)

    #Recebendo a informação e validando a questão de algum erro
    #tratando o erro
    if resp_api != 200:

        if resp_api == 400:
                        return { 
                            "name": "BadRequestError",
                            "message": "CEP deve conter exatamente 8 dígitos",
                            "type": "validation_error"
                }
        elif resp_api == 404:
                        return {                  
                            "name": "NotFoundError",
                            "message": "CEP NAO ENCONTRADO",
                            "type": "service_error"
                      }
        elif resp_api == 500:
                        return {           
                            "name": "InternalError",
                            "message": "Erro interno no serviço de CEP",
                            "type": "internal_error"
                      }
        else:
                      raise HTTPException(status_code=503, detail="Serviço indisponível no momento")   

    #Habilitar a resposta para a classe Adress
    adress = Adress(**resp_api)

    #No caso da resposta da apí estar correta, retornar as informações pedidas
    return_adress(adress)

     