
from fastapi import FastAPI
from app.controller import router

    
#inicializando a rota
app = FastAPI()

app.include_router(router)

     