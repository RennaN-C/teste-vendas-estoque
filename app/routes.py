from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ProdutoCreate, ProdutoResponse, VendaCreate, VendaResponse
from app.services import criar_produto, criar_venda, listar_produtos


router = APIRouter()


@router.get("/")
def home():
    return {
        "mensagem": "API de Gestão de Vendas e Estoque está funcionando"
    }


@router.post("/produtos", response_model=ProdutoResponse, status_code=201)
def cadastrar_produto(dados: ProdutoCreate, db: Session = Depends(get_db)):
    return criar_produto(dados, db)


@router.get("/produtos", response_model=list[ProdutoResponse])
def consultar_produtos(
    estoque_baixo: bool = False,
    db: Session = Depends(get_db)
):
    return listar_produtos(estoque_baixo, db)


@router.post("/vendas", response_model=VendaResponse, status_code=201)
def registrar_venda(dados: VendaCreate, db: Session = Depends(get_db)):
    return criar_venda(dados, db)
