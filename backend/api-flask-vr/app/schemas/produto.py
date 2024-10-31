import base64
from app.extensions import ma
from app.models.produto import Produto

class ProdutoSchema(ma.SQLAlchemyAutoSchema):
    imagem = ma.Method("get_imagem", "set_imagem")

    class Meta:
        model = Produto
        load_instance = True

    def get_imagem(self, obj):
        """Converte a imagem binária para Base64 para a serialização."""
        if obj.imagem:
            return base64.b64encode(obj.imagem).decode('utf-8')  # Converte para string Base64
        return None

    def set_imagem(self, value):
        """Decodifica a imagem Base64 para binário antes de armazená-la no banco de dados."""
        if value:
            return base64.b64decode(value)  # Converte de volta para binário
        return None
