from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..model import Pedido
from ..database import SessionLocal
import numpy as np

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/recomendacao/{usuario_id}")
def recomendar_produtos(usuario_id: int, db: Session = Depends(get_db)):
    pedidos = db.query(Pedido).filter(Pedido.usuario_id == usuario_id).all()
    historico_usuario = [pedido.item for pedido in pedidos]

    sabores_pizza = ["Margherita", "Pepperoni", "Quatro Queijos", "Frango com Catupiry", "Calabresa", "Vegetariana"]
    bebidas = ["Cerveja Budweiser", "Coca-Cola Zero", "Coca-Cola", "Fanta Laranja", "Guaraná Antarctica"]

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
        recommendations = [
            all_items[i] for i in range(len(all_items))
            if recommendations_encoded[i] > 0.5 and all_items[i] not in user_purchase_history
        ]
        return recommendations

    recomendacoes = recommend_products(historico_usuario, cardapio)

    pizzas_recomendadas_nomes = [r for r in recomendacoes if r in sabores_pizza][:2]

    if len(pizzas_recomendadas_nomes) == 0:
        pizzas_recomendadas_nomes = sabores_pizza[:2]

    pizzas_recomendadas = [
        {"nome": pizza, "preco": precos_pizza.get(pizza, "Preço não encontrado")}
        for pizza in pizzas_recomendadas_nomes
    ]

    return {
        "pizzas_recomendadas": pizzas_recomendadas,
        "bebidas_recomendadas": bebidas
    }
