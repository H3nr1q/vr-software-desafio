from app.extensions import ma
from app.models.produtoloja import ProdutoLoja

class ProdutoLojaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProdutoLoja
        load_instance = True
