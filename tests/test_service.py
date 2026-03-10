import pytest
from app.service import response_adress
from app.service import request_api, formatted_adress
from unittest.mock import AsyncMock, patch
from app.model import Adress, Location, CEPResponse


@pytest.mark.asyncio
async def test_formatted_adress_response_api_client():

    mock_response = Adress(
        cep="06053020",
        state="SP",
        city="Osasco",
        neighborhood="Jaguaribe",
        street="Avenida José Lourenço",
        service="open-cep",
        location= Location(
            type="Point",
            coordinates={
                    "longitude": "-46.7861065",
                    "latitude": "-23.5558325"
                    }
        )
    )


    with patch('app.service.request_api', new_callable=AsyncMock) as mock_request:
        mock_request.return_value=mock_response

        result = await response_adress("06053020")

        assert isinstance(result, CEPResponse)
        assert result.endereco == "Avenida José Lourenço, Jaguaribe, Osasco/SP"
        mock_request.assert_called_once_with("06053020")
    

    
