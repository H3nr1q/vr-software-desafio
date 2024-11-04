from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.produto import Produto
from app.models.loja import Loja
from app.models.produtoloja import ProdutoLoja
from app.schemas.produtoloja import ProdutoLojaSchema

produtoloja_bp = Blueprint('produtoloja_bp', __name__)
produtoloja_schema = ProdutoLojaSchema()
produtolojas_schema = ProdutoLojaSchema(many=True)

@produtoloja_bp.route('/produtolojas/<int:produto_id>', methods=['GET'])
def get_produto_lojas(produto_id):
    produto_lojas = ProdutoLoja.query.filter_by(produto_id=produto_id).all()
    return produtolojas_schema.jsonify(produto_lojas)

@produtoloja_bp.route('/produtoloja', methods=['POST'])
def add_produto_loja():
    data = request.get_json()
    
    if 'produto_id' not in data or 'loja_id' not in data or 'preco_venda' not in data:
        return jsonify({"error": "Os campos 'produto_id', 'loja_id' e 'preco_venda' são obrigatórios."}), 400
    
    nova_produto_loja = ProdutoLoja(
        produto_id=data['produto_id'],
        loja_id=data['loja_id'],
        preco_venda=data['preco_venda']
    )
    
    db.session.add(nova_produto_loja)
    db.session.commit()
    
    return produtoloja_schema.jsonify(nova_produto_loja), 201
