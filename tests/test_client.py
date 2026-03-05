import pytest
from app.client import request_api
import httpx
import respx


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


    adress_api = await request_api("06053020")

    assert adress_api.cep == "06053020"
    assert adress_api.state == "SP"
    assert adress_api.city == "Osasco"
    assert adress_api.neighborhood == "Jaguaribe"
    assert adress_api.street == "Avenida José Lourenço"
    assert adress_api.location.type == "Point"
    assert adress_api.location.coordinates['longitude'] == "-46.7861065"
    assert adress_api.location.coordinates['latitude'] == "-23.5558325"
    

