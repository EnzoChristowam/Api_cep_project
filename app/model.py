from pydantic import BaseModel, field_validator
from fastapi.responses import JSONResponse

class Location(BaseModel):
    type:str
    coordinates:dict

class Adress(BaseModel):
    cep:str
    state:str
    city:str
    neighborhood:str
    street:str
    service:str
    location:Location


class CEPResponse(BaseModel):
    endereco:str



class ErrorResponse(BaseModel):
    name:str
    message:str
    type:str