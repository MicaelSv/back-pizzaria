from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal
from model import Usuario  # importa o modelo

app = FastAPI()

# Configurando o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou substitua com a URL do frontend em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/msg")
def read_root():
    return JSONResponse(content={"message": "Hello from FastAPI on Vercel!"})

@app.post("/cadastro")
async def receber_cadastro(request: Request, db: Session = Depends(get_db)):
    dados = await request.json()
    
    novo_usuario = Usuario(
        nome=dados["nome"],
        senha=dados["senha"],
        email=dados["email"],
        cep=dados["cep"],
        endereco=dados["endereco"],
        numero=dados["numero"],
        complemento=dados["complemento"],
        bairro=dados["bairro"],
        cidade=dados["cidade"],
        estado=dados["estado"],
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return JSONResponse(content={"status": "sucesso", "mensagem": "Usuário salvo com sucesso!"})