from app.database import Base, engine
from app.models import Produto, Venda, VendaItem

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")