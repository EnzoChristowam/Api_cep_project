import pytest
from app.service import response_adress
import httpx
import respx
from fastapi import HTTPException


@respx.mock
@pytest.mark.asyncio
async def test_formatted_adress_response_api_client():

    #criando u mock de retorno da rota acionada
    respx.get("https://brasilapi.com.br/api/cep/v2/06053020").mock(
        return_value=httpx.Response(
            200, 
            json={
                "cep": "06053020",
                "state": "SP",
                "city": "Osasco",
                "neighborhood": "Jaguaribe",
                "street": "Avenida José Lourenço",
                "service": "open-cep",
                "location": {
                    "type": "Point",
                    "coordinates": {
                    "longitude": "-46.7861065",
                    "latitude": "-23.5558325"
                    }
                }
            }
        )
    )


    resp_formatted_adress = await response_adress("06053020")

    assert resp_formatted_adress.endereco == "Avenida José Lourenço, Jaguaribe, Osasco/SP"
    

    
