import base64
from app.extensions import ma
from app.models.produto import Produto

class ProdutoSchema(ma.SQLAlchemyAutoSchema):
    imagem = ma.Method("get_imagem", "set_imagem")

    class Meta:
        model = Produto
        load_instance = True

    def get_imagem(self, obj):
        if obj.imagem:
            return base64.b64encode(obj.imagem).decode('utf-8')
        return None

    def set_imagem(self, value):
        if value:
            return base64.b64decode(value)
        return None
