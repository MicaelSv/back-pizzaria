from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/endereco/{usuario_id}")
def listar_endereco(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return {
        "status": "sucesso",
        "endereco": {
            "cep": usuario.cep,
            "endereco": usuario.endereco,
            "numero": usuario.numero,
            "complemento": usuario.complemento,
            "bairro": usuario.bairro,
            "cidade": usuario.cidade,
            "estado": usuario.estado
        }
    }
