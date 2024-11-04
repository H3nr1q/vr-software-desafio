from app.extensions import ma
from app.models.produtoloja import ProdutoLoja

class ProdutoLojaSchema(ma.SQLAlchemyAutoSchema):
    produto = ma.Nested('ProdutoSchema', only=('id', 'descricao', 'custo', 'imagem'))
    loja = ma.Nested('LojaSchema', only=('id', 'descricao'))

    class Meta:
        model = ProdutoLoja
        load_instance = True
