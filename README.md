# API de Gestao de Vendas e Estoque

API REST desenvolvida com FastAPI para cadastro de produtos, consulta de
estoque e realizacao de vendas com baixa de estoque.

## Funcionalidades

- Cadastro de produtos com validacao de nome, preco e quantidade.
- Bloqueio de cadastro de produtos com nomes duplicados.
- Listagem completa de produtos.
- Filtro para produtos com estoque baixo ou zerado.
- Registro de vendas com um ou mais produtos.
- Validacao de estoque antes de concluir uma venda.
- Calculo e retorno do valor total da venda.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

## Requisitos

- Python instalado
- PostgreSQL instalado e em execucao
- Banco de dados PostgreSQL chamado `vendas_estoque`

## Configuracao

Clone o repositorio e acesse a pasta do projeto:

```powershell
git clone https://github.com/RennaN-C/teste-vendas-estoque.git
cd teste-vendas-estoque
```

Crie e ative um ambiente virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

Crie o banco de dados no PostgreSQL:

```sql
CREATE DATABASE vendas_estoque;
```

Crie o arquivo `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

Edite o `.env` com os dados do seu PostgreSQL:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/vendas_estoque
```

Crie as tabelas:

```powershell
python create_tables.py
```

## Executando a aplicacao

Inicie a API:

```powershell
uvicorn app.main:app --reload
```

A API estara disponivel em:

- API: http://127.0.0.1:8000
- Frontend simples: http://127.0.0.1:8000/front
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Exemplos de uso

### Cadastrar um produto

```powershell
curl.exe -X POST "http://127.0.0.1:8000/produtos" -H "Content-Type: application/json" -d '{"nome":"Teclado","preco":150.00,"quantidade":10}'
```

Resposta esperada:

```json
{
  "id": 1,
  "nome": "Teclado",
  "preco": "150.00",
  "quantidade": 10
}
```

### Listar produtos

```powershell
curl.exe "http://127.0.0.1:8000/produtos"
```

### Listar produtos com estoque baixo ou zerado

Produtos com quantidade menor ou igual a 5:

```powershell
curl.exe "http://127.0.0.1:8000/produtos?estoque_baixo=true"
```

### Registrar uma venda

```powershell
curl.exe -X POST "http://127.0.0.1:8000/vendas" -H "Content-Type: application/json" -d '{"itens":[{"produto_id":1,"quantidade":2}]}'
```

Resposta esperada:

```json
{
  "id": 1,
  "valor_total": "300.00",
  "itens": [
    {
      "produto_id": 1,
      "quantidade": 2,
      "preco_unitario": "150.00",
      "subtotal": "300.00"
    }
  ]
}
```

## Estrutura do projeto

```text
app/
  database.py
  main.py
  models.py
  routes.py
  schemas.py
  services.py
create_tables.py
requirements.txt
test_connection.py
```

## Regras de negocio

- O nome do produto e obrigatorio.
- O preco do produto deve ser maior que zero.
- A quantidade inicial nao pode ser negativa.
- Nao e permitido cadastrar produtos com o mesmo nome.
- Uma venda deve possuir pelo menos um item.
- Nao e permitido vender uma quantidade maior que o estoque disponivel.
- Se algum item da venda for invalido, a operacao e cancelada.
