from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    nome= Column(String(100), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    quantidade= Column(Integer, nullable=False)

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True)
    data_hora = Column(DateTime, server_default=func.now())
    valor_total = Column(Numeric(10, 2), nullable=False, default=0)

class VendaItem(Base):
    __tablename__ = "vendas_itens"

    id = Column(Integer, primary_key=True)
    venda_id= Column(ForeignKey("vendas.id"), nullable=False)
    produto_id = Column(ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)