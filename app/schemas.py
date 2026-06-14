from decimal import Decimal
from pydantic import BaseModel, Field

class ProdutoCreate(BaseModel):
    nome: str = Field(..., min_length=1)
    preco: Decimal = Field(..., gt=0)
    quantidade: int = Field(..., ge=0)

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    preco: Decimal
    quantidade: int

    class Config:
        from_attributes = True

class VendaItemCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)


class VendaCreate(BaseModel):
    itens: list[VendaItemCreate]


class VendaItemResponse(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal


class VendaResponse(BaseModel):
    id: int
    valor_total: Decimal
    itens: list[VendaItemResponse]