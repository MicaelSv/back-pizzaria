from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# rodar isso aqui no terminal pra adicionar as novas tabelas no banco de dados
#from database import engine
#from model import Base
#Base.metadata.create_all(bind=engine)


Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    cep = Column(String)
    endereco = Column(String)
    numero = Column(String)
    complemento = Column(String)
    bairro = Column(String)
    cidade = Column(String)
    estado = Column(String)

    pedidos = relationship("Pedido", back_populates="usuario")

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    item = Column(String, nullable=False)

    usuario = relationship("Usuario", back_populates="pedidos")