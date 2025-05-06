from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import auth, pedido, recomendacao, endereco

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
app.include_router(auth.router)
app.include_router(pedido.router)
app.include_router(recomendacao.router)
app.include_router(endereco.router)
