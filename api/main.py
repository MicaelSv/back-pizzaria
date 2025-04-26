from fastapi import FastAPI, Request, Depends,  HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine  
from .model import Base, Usuario, Pedido  # importa o modelo

# uvicorn main:app --reload

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

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

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

    return {"status": "sucesso", "mensagem": "Usuário salvo com sucesso!"}

@app.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    dados = await request.json()
    email = dados.get("email")
    senha = dados.get("senha")

    usuario = db.query(Usuario).filter(Usuario.email == email, Usuario.senha == senha).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos.")

    return {"status": "sucesso", "mensagem": "Login realizado com sucesso!", "usuario_id": usuario.id}


from .model import Usuario, Pedido

@app.post("/pedido")
async def criar_pedido(request: Request, db: Session = Depends(get_db)):
    dados = await request.json()
    usuario_id = dados.get("usuario_id")
    descricao = dados.get("descricao")  # o que o usuário pediu

    if not usuario_id or not descricao:
        raise HTTPException(status_code=400, detail="Dados insuficientes.")

    novo_pedido = Pedido(usuario_id=usuario_id, descricao=descricao)
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return {"status": "sucesso", "mensagem": "Pedido registrado com sucesso!"}
