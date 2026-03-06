import pytest
from app.client import request_api
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


    adress_api = await request_api("06053020")

    assert adress_api.cep == "06053020"
    assert adress_api.state == "SP"
    assert adress_api.city == "Osasco"
    assert adress_api.neighborhood == "Jaguaribe"
    assert adress_api.street == "Avenida José Lourenço"
    assert adress_api.service == "open-cep"
    assert adress_api.location.type == "Point"
    assert adress_api.location.coordinates['longitude'] == "-46.7861065"
    assert adress_api.location.coordinates['latitude'] == "-23.5558325"


@respx.mock
@pytest.mark.asyncio
async def test_formatted_adress_error_400():
    #criando u mock de retorno da rota acionada
    respx.get("https://brasilapi.com.br/api/cep/v2/0000000").mock(
        return_value=httpx.Response(
            400, 
            json={
                "message":"O CEP deve conter exatamente 8 dígitos numéricos",
                "type":"validation_error"
            }
        )
    )

    with pytest.raises(HTTPException) as exc_info:
        await request_api("0000000")

    assert exc_info.value.status_code == 400

    assert exc_info.value.detail["message"] == "O CEP deve conter exatamente 8 dígitos numéricos"
    assert exc_info.value.detail["type"] == "validation_error"
    assert exc_info.value.detail["name"] == "BadRequestError"



@respx.mock
@pytest.mark.asyncio
async def test_formatted_adress_error_404():
    #criando u mock de retorno da rota acionada
    respx.get("https://brasilapi.com.br/api/cep/v2/00000000").mock(
        return_value=httpx.Response(
            404, 
            json={
                "message":"O CEP deve conter exatamente 8 dígitos numéricos",
                "type":"validation_error"
            }
        )
    )

    with pytest.raises(HTTPException) as exc_info:
        await request_api("00000000")

    assert exc_info.value.status_code == 404

    assert exc_info.value.detail["message"] == "CEP NAO ENCONTRADO"
    assert exc_info.value.detail["type"] == "service_error"
    assert exc_info.value.detail["name"] == "NotFoundError"




@respx.mock
@pytest.mark.asyncio
async def test_formatted_adress_error_500():
    #criando u mock de retorno da rota acionada
    respx.get("https://brasilapi.com.br/api/cep/v2/99999999").mock(
        return_value=httpx.Response(
            500, 
            json={
                "message":"O CEP deve conter exatamente 8 dígitos numéricos",
                "type":"validation_error"
            }
        )
    )

    with pytest.raises(HTTPException) as exc_info:
        await request_api("99999999")

    assert exc_info.value.status_code == 500

    assert exc_info.value.detail["message"] == "Erro interno no serviço de CEP"
    assert exc_info.value.detail["type"] == "internal_error"
    assert exc_info.value.detail["name"] == "InternalError"




@respx.mock
@pytest.mark.asyncio
async def test_formatted_adress_error_503():
    #criando u mock de retorno da rota acionada
    respx.get("https://brasilapi.com.br/api/cep/v2/99999998").mock(
        return_value=httpx.Response(
            503, 
            json={
                "detail":"Serviço indisponível no momento"
            }
        )
    )

    with pytest.raises(HTTPException) as exc_info:
        await request_api("99999998")

    assert exc_info.value.status_code == 503

    assert exc_info.value.detail == "Serviço indisponível no momento"





@respx.mock
@pytest.mark.asyncio
async def test_formatted_adress_error_Timeout():
    #criando u mock de retorno da rota acionada
    respx.get("https://brasilapi.com.br/api/cep/v2/01010101").mock(
        side_effect=httpx.TimeoutException("Erro interno")
    )

    with pytest.raises(HTTPException) as exc_info:
        await request_api("01010101")

    assert exc_info.value.status_code == 500

    assert "Erro interno" in exc_info.value.detail



@respx.mock
@pytest.mark.asyncio
async def test_formatted_adress_error_Timeout():
    #criando u mock de retorno da rota acionada
    respx.get("https://brasilapi.com.br/api/cep/v2/01010102").mock(
        side_effect=httpx.RequestError("Erro interno")
    )

    with pytest.raises(HTTPException) as exc_info:
        await request_api("01010102")

    assert exc_info.value.status_code == 500

    assert "Erro interno" in exc_info.value.detail


@respx.mock
@pytest.mark.asyncio
async def test_formatted_adress_error_Timeout():
    #criando u mock de retorno da rota acionada
    respx.get("https://brasilapi.com.br/api/cep/v2/01010103").mock(
        side_effect=httpx.ConnectError("Erro interno")
    )

    with pytest.raises(HTTPException) as exc_info:
        await request_api("01010103")

    assert exc_info.value.status_code == 500

    assert "Erro interno" in exc_info.value.detail
