from app.models.produto import Produto
from app.extensions import db

def get_all_produtos():
    return Produto.query.all()

def add_produto(data):
    novo_produto = Produto(
        descricao=data['descricao'],
        custo=data.get('custo'),
        imagem=data.get('imagem')
    )
    db.session.add(novo_produto)
    db.session.commit()
    return novo_produto
