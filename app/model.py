from pydantic import BaseModel, field_validator
from fastapi.responses import JSONResponse

class Adress(BaseModel):
    cep:str
    state:str
    city:str
    neighborhood:str
    street:str
    service:str
    location:dict
