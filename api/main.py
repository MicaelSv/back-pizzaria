from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurando o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou substitua com a URL do frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/msg")
def read_root():
    return JSONResponse(content={"message": "Hello from FastAPI on Vercel!"})


# Nova rota para receber os dados do formulário
@app.post("/cadastro")
async def receber_cadastro(request: Request):
    dados = await request.json()
    print("📥 Dados recebidos do frontend:")
    for chave, valor in dados.items():
        print(f"{chave}: {valor}")
    
    return JSONResponse(content={"status": "sucesso", "mensagem": "Dados recebidos com sucesso!"})