from fastapi import FastAPI, Request, Depends,  HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, engine  
from .model import Base, Usuario, Pedido  # importa o modelo
import numpy as np
from datetime import datetime

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

@app.post("/pedido/{usuario_id}")
async def criar_pedido(usuario_id: int, request: Request, db: Session = Depends(get_db)):
    dados = await request.json()
    itens_pedidos = dados.get("itens", [])  # Exemplo de payload esperado: {"itens": ["Calabresa", "Guaraná Antarctica"]}

    for item in itens_pedidos:
        novo_pedido = Pedido(
            usuario_id=usuario_id,
            item=item
        )
        db.add(novo_pedido)

    db.commit()
    return {"status": "sucesso", "mensagem": "Pedido salvo com sucesso!"}


@app.get("/recomendacao/{usuario_id}")
def recomendar_produtos(usuario_id: int, db: Session = Depends(get_db)):
    # Busca histórico de pedidos do usuário
    pedidos = db.query(Pedido).filter(Pedido.usuario_id == usuario_id).all()
    historico_usuario = [pedido.item for pedido in pedidos]

    # Definindo sabores e bebidas
    sabores_pizza = ["Margherita", "Pepperoni", "Quatro Queijos", "Frango com Catupiry", "Calabresa", "Vegetariana"]
    bebidas = ["Cerveja Budweiser", "Coca-Cola Zero", "Coca-Cola", "Fanta Laranja", "Guaraná Antarctica"]

    # Preços das pizzas
    precos_pizza = {
        "Margherita": 45,
        "Quatro Queijos": 60,
        "Calabresa": 50,
        "Pepperoni": 55,
        "Frango com Catupiry": 55,
        "Vegetariana": 55
    }

    cardapio = {
        "Pizzas": sabores_pizza,
        "Bebidas": bebidas
    }

    # Funções auxiliares
    def encode_purchase_history(user_purchase_history, cardapio):
        all_items = [item for items in cardapio.values() for item in items]
        encoded_history = np.zeros(len(all_items))
        for item in user_purchase_history:
            if item in all_items:
                encoded_history[all_items.index(item)] = 1
        return encoded_history

    def create_neural_network(input_size, hidden_size, output_size):
        np.random.seed(0)
        W1 = np.random.randn(input_size, hidden_size)
        b1 = np.zeros(hidden_size)
        W2 = np.random.randn(hidden_size, output_size)
        b2 = np.zeros(output_size)
        return W1, b1, W2, b2

    def relu(x):
        return np.maximum(0, x)

    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    def forward_propagation(X, W1, b1, W2, b2):
        Z1 = np.dot(X, W1) + b1
        A1 = relu(Z1)
        Z2 = np.dot(A1, W2) + b2
        A2 = sigmoid(Z2)
        return A2

    def recommend_products(user_purchase_history, cardapio):
        encoded_history = encode_purchase_history(user_purchase_history, cardapio)

        input_size = len(encoded_history)
        hidden_size = 10
        output_size = len(encoded_history)

        W1, b1, W2, b2 = create_neural_network(input_size, hidden_size, output_size)
        recommendations_encoded = forward_propagation(encoded_history, W1, b1, W2, b2)

        all_items = [item for items in cardapio.values() for item in items]
        recommendations = [all_items[i] for i in range(len(all_items)) if recommendations_encoded[i] > 0.5 and all_items[i] not in user_purchase_history]
        return recommendations

    # Fazendo a recomendação
    recomendacoes = recommend_products(historico_usuario, cardapio)

    # Filtrar: 2 pizzas + 2 bebidas
    pizzas_recomendadas_nomes = [r for r in recomendacoes if r in sabores_pizza][:2]
    bebidas_recomendadas = [r for r in recomendacoes if r in bebidas][:2]

    # Montar pizzas recomendadas com nome + preço
    pizzas_recomendadas = [
        {
            "nome": pizza,
            "preco": precos_pizza.get(pizza, "Preço não encontrado")
        }
        for pizza in pizzas_recomendadas_nomes
    ]

    return {
        "pizzas_recomendadas": pizzas_recomendadas,
        "bebidas_recomendadas": bebidas_recomendadas
    }


@app.get("/historico/{usuario_id}")
def listar_historico(usuario_id: int, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.usuario_id == usuario_id).all()

    sabores_pizza = ["Margherita", "Pepperoni", "Quatro Queijos", "Frango com Catupiry", "Calabresa", "Vegetariana"]
    bebidas = ["Cerveja Budweiser", "Coca-Cola Zero", "Coca-Cola", "Fanta Laranja", "Guaraná Antarctica"]

    historico = []
    for pedido in pedidos:
        if pedido.item in sabores_pizza:
            descricao = f"Pizza {pedido.item}"
        elif pedido.item in bebidas:
            descricao = f"Bebida {pedido.item}"
        else:
            descricao = pedido.item  # Caso futuro de outro tipo de item

        data_formatada = pedido.data_pedido.strftime("%d/%m/%Y") if pedido.data_pedido else "Data desconhecida"

        historico.append({
            "descricao": descricao,
            "data_pedido": data_formatada
        })

    return {"status": "sucesso", "historico": historico}


@app.get("/endereco/{usuario_id}")
def listar_endereco(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    endereco = {
        "cep": usuario.cep,
        "endereco": usuario.endereco,
        "numero": usuario.numero,
        "complemento": usuario.complemento,
        "bairro": usuario.bairro,
        "cidade": usuario.cidade,
        "estado": usuario.estado
    }

    return {"status": "sucesso", "endereco": endereco}