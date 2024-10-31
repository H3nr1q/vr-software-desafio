from app.extensions import ma
from app.models.loja import Loja

class LojaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Loja
        load_instance = True