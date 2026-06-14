from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Produto, Venda, VendaItem
from app.schemas import ProdutoCreate, VendaCreate


def criar_produto(dados: ProdutoCreate, db: Session):
    produto_existente = db.query(Produto).filter(Produto.nome == dados.nome).first()

    if produto_existente:
        raise HTTPException(
            status_code=400,
            detail="Já existe um produto cadastrado com esse nome."
        )

    produto = Produto(
        nome=dados.nome,
        preco=dados.preco,
        quantidade=dados.quantidade
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto


def listar_produtos(estoque_baixo: bool, db: Session):
    query = db.query(Produto)

    if estoque_baixo:
        query = query.filter(Produto.quantidade <= 5)

    return query.all()


def criar_venda(dados: VendaCreate, db: Session):
    if not dados.itens:
        raise HTTPException(
            status_code=400,
            detail="A venda precisa ter pelo menos um item."
        )

    try:
        produtos_ids = sorted({item.produto_id for item in dados.itens})
        produtos_bloqueados = (
            db.query(Produto)
            .filter(Produto.id.in_(produtos_ids))
            .order_by(Produto.id)
            .with_for_update()
            .all()
        )
        produtos_por_id = {
            produto.id: produto for produto in produtos_bloqueados
        }

        venda = Venda(valor_total=Decimal("0.00"))

        db.add(venda)
        db.flush()

        valor_total = Decimal("0.00")
        itens_resposta = []

        for item in dados.itens:
            produto = produtos_por_id.get(item.produto_id)

            if not produto:
                raise HTTPException(
                    status_code=404,
                    detail=f"Produto com ID {item.produto_id} não encontrado."
                )

            if produto.quantidade < item.quantidade:
                raise HTTPException(
                    status_code=400,
                    detail=f"Estoque insuficiente para o produto {produto.nome}."
                )

            preco_unitario = Decimal(produto.preco)
            subtotal = preco_unitario * item.quantidade

            produto.quantidade = produto.quantidade - item.quantidade

            venda_item = VendaItem(
                venda_id=venda.id,
                produto_id=produto.id,
                quantidade=item.quantidade,
                preco_unitario=preco_unitario,
                subtotal=subtotal
            )

            db.add(venda_item)

            valor_total = valor_total + subtotal

            itens_resposta.append({
                "produto_id": produto.id,
                "quantidade": item.quantidade,
                "preco_unitario": preco_unitario,
                "subtotal": subtotal
            })

        venda.valor_total = valor_total

        db.commit()
        db.refresh(venda)

        return {
            "id": venda.id,
            "valor_total": venda.valor_total,
            "itens": itens_resposta
        }

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise
