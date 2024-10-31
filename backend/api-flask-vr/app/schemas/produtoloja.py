from app.extensions import ma
from app.models.produtoloja import ProdutoLoja

class ProdutoLojaSchema(ma.SQLAlchemyAutoSchema):
    produto = ma.Nested('ProdutoSchema', only=('id', 'descricao', 'custo', 'imagem'))  # Substitua pelos campos desejados
    loja = ma.Nested('LojaSchema', only=('id', 'descricao'))  # Substitua pelos campos desejados

    class Meta:
        model = ProdutoLoja
        load_instance = True
