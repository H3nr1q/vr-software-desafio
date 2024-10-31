import base64
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.produto import Produto
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
