import pytest
from app.service import response_adress
import asyncio
import json
from app.main import app
from fastapi.testclient import TestClient
import httpx



#Basicamente, agora temos que definir 3 coisas: O que vamos pegar, o que vamos fazer e o que vamos comoparar.

#TESTE DE FORMATO DA SAÍDA DO MÉTODO DO SERVICE
@pytest.mark.asyncio
async def test_format_response():
    cep = "06053020"
    expected_response = {
        "Endereço":"Avenida José Lourenço, Jaguaribe, Osasco/SP"
    }

    response = await response_adress(cep)
    assert response == expected_response


#TESTE DE ERRO 400
client = TestClient(app)

def test_error_400_response_adress():

    invalid_cep = "0605302"
    json_response_test = {
                    "name": "BadRequestError",
                    "message": "O CEP deve conter exatamente 8 dígitos numéricos",
                    "type": "validation_error"
                }


    response = client.get(f"http://127.0.0.1:8000/cep/v1/{invalid_cep}")

    assert response.status_code == 400

    assert response.json() == json_response_test



#VALIDANDO O ERRO 404
def test_error_404_response_adress():
    inexistent_cep = "00000000"

    json_response_test = {
                    "name": "NotFoundError",
                    "message": "CEP NAO ENCONTRADO",
                    "type": "service_error"
    }

    response = client.get(f"http://127.0.0.1:8000/cep/v1/{inexistent_cep}")

    assert response.status_code == 404
    assert response.json() == json_response_test


