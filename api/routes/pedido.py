from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from ..model import Pedido
from ..database import SessionLocal
import pytz

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pedido/{usuario_id}")
async def criar_pedido(usuario_id: int, request: Request, db: Session = Depends(get_db)):
    dados = await request.json()
    for item in dados.get("itens", []):
        db.add(Pedido(usuario_id=usuario_id, item=item))
    db.commit()
    return {"status": "sucesso", "mensagem": "Pedido salvo com sucesso!"}

@router.get("/historico/{usuario_id}")
def listar_historico(usuario_id: int, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.usuario_id == usuario_id).all()
    sabores = ["Margherita", "Pepperoni", "Quatro Queijos", "Frango com Catupiry", "Calabresa", "Vegetariana"]
    br_tz = pytz.timezone('America/Sao_Paulo')
    historico = []
    for pedido in pedidos:
        descricao = f"{'Pizza' if pedido.item in sabores else 'Bebida'} {pedido.item}"
        data = pedido.data_pedido.astimezone(br_tz).strftime("%d/%m/%Y") if pedido.data_pedido else "Data desconhecida"
        historico.append({"descricao": descricao, "data_pedido": data})
    return {"status": "sucesso", "historico": historico}
