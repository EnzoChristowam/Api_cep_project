from fastapi import HTTPException 
import httpx
from app.model import Adress, ErrorResponse

async def request_api(cep:str):

    cep_cleaned = cep.replace("-","") if "-" in cep else cep
     
    url = f'https://brasilapi.com.br/api/cep/v2/{cep_cleaned}'

    try:
        async with httpx.AsyncClient(verify=False) as client:
            resp_api = await client.get(url, timeout=10.0)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno {e}")


    #Recebendo a informação e validando a questão de algum erro
    #tratando o erro
    if resp_api.status_code != 200:
                if resp_api.status_code == 400:
                    raise HTTPException(
                        status_code=resp_api.status_code,
                        detail= ErrorResponse(
                            name="BadRequestError",
                            message="O CEP deve conter exatamente 8 dígitos numéricos",
                            type="validation_error"
                        ).model_dump())
                

                elif resp_api.status_code == 404:
                    raise HTTPException(
                        status_code=resp_api.status_code,
                        detail= ErrorResponse(
                            name="NotFoundError",
                            message="CEP NAO ENCONTRADO",
                            type="service_error"
                        ).model_dump())
                

                elif resp_api.status_code == 500:
                    raise HTTPException(
                        status_code=resp_api.status_code,
                        detail= ErrorResponse(
                            name="InternalError",
                            message="Erro interno no serviço de CEP",
                            type="internal_error"
                        ).model_dump())
                        
                else:
                    raise HTTPException(status_code=503, detail="Serviço indisponível no momento")   

    #Habilitar a resposta para a classe Adress
    data = resp_api.json()
    adress = Adress(**data)

    return adress

            
    