from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from ..model import Usuario
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/cadastro")
async def receber_cadastro(request: Request, db: Session = Depends(get_db)):
    dados = await request.json()
    if db.query(Usuario).filter(Usuario.email == dados["email"]).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    novo_usuario = Usuario(**dados)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"status": "sucesso", "mensagem": "Usuário salvo com sucesso!"}

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    dados = await request.json()
    usuario = db.query(Usuario).filter(
        Usuario.email == dados.get("email"),
        Usuario.senha == dados.get("senha")
    ).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos.")
    return {"status": "sucesso", "mensagem": "Login realizado com sucesso!", "usuario_id": usuario.id}
