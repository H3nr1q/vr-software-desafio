import base64
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.produto import Produto
from app.models.produtoloja import ProdutoLoja
from app.schemas.produto import ProdutoSchema

produto_bp = Blueprint('produto_bp', __name__)
produto_schema = ProdutoSchema()
produtos_schema = ProdutoSchema(many=True)

@produto_bp.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return produtos_schema.jsonify(produtos)

@produto_bp.route('/produto', methods=['POST'])
def add_produto():
    # Carrega os dados do formulário diretamente usando o schema
    data = request.form.to_dict()
    imagem = request.files.get('imagem')

    if imagem:
        # Lê a imagem como binário e converte para Base64
        imagem_binario = imagem.read()
        data['imagem'] = base64.b64encode(imagem_binario).decode('utf-8')
    else:
        data['imagem'] = None

    # Valida o campo 'descricao'
    if not data.get('descricao'):
        return jsonify({"error": "O campo 'descricao' é obrigatório"}), 400

    # Usa o ProdutoSchema para carregar os dados
    novo_produto = produto_schema.load(data, session=db.session)

    # Adiciona o novo produto ao banco de dados
    db.session.add(novo_produto)
    db.session.commit()

    return produto_schema.jsonify(novo_produto), 201

@produto_bp.route('/produto/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404

    # Carrega os dados do formulário
    data = request.form.to_dict()
    imagem = request.files.get('imagem')

    if imagem:
        # Lê a imagem como binário e converte para Base64
        imagem_binario = imagem.read()
        data['imagem'] = base64.b64encode(imagem_binario).decode('utf-8')
    else:
        data['imagem'] = base64.b64encode(produto.imagem).decode('utf-8')

    # Valida o campo 'descricao'
    if not data.get('descricao'):
        return jsonify({"error": "O campo 'descricao' é obrigatório"}), 400

    # Usa o ProdutoSchema para atualizar os dados
    produto_atualizado = produto_schema.load(data, instance=produto, session=db.session)

    # Comita as alterações no banco de dados
    db.session.commit()

    return produto_schema.jsonify(produto_atualizado), 200


@produto_bp.route('/produto/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    # Busca o produto pelo ID
    produto = Produto.query.get(produto_id)
    if not produto:
        return jsonify({"error": "Produto não encontrado"}), 404

    # Remove os preços associados a esse produto
    precos = ProdutoLoja.query.filter_by(produto_id=produto_id).all()
    for preco in precos:
        db.session.delete(preco)

    # Remove o produto do banco de dados
    db.session.delete(produto)
    db.session.commit()

    return jsonify({"message": "Produto e preços excluídos com sucesso"}), 204
