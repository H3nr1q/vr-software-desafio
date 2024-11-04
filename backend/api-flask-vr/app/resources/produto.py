import base64
from flask import Blueprint, json, request, jsonify
from app.extensions import db
from app.models.produto import Produto
from app.models.produtoloja import ProdutoLoja
from app.schemas.produto import ProdutoSchema
from app.schemas.produtoloja import ProdutoLojaSchema
from sqlalchemy import func

produto_bp = Blueprint('produto_bp', __name__)
produto_schema = ProdutoSchema()
produtos_schema = ProdutoSchema(many=True)

@produto_bp.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return produtos_schema.jsonify(produtos)

@produto_bp.route('/produto', methods=['POST'])
def add_produto():
    # Carrega os dados do formulário
    data = request.form.to_dict(flat=False)
    imagem = request.files.get('imagem')
    
    # Processa a imagem se ela existir
    if imagem:
        imagem_binario = imagem.read()
        data['imagem'] = base64.b64encode(imagem_binario).decode('utf-8')
    else:
        data['imagem'] = None

    # Verifica se o campo 'descricao' está presente
    if not data.get('descricao'):
        return jsonify({"error": "O campo 'descricao' é obrigatório"}), 400

    # Cria o objeto do produto
    novo_produto = produto_schema.load({
        'descricao': data['descricao'][0],
        'custo': data['custo'][0],
        'imagem': data['imagem']
    }, session=db.session)

    # Adiciona o produto ao banco para obter o ID, mas não comita ainda
    db.session.add(novo_produto)
    db.session.flush()  # Isso gera o ID do produto sem comitar

    # Processa e valida a lista de preços
    precos_data = data.get('precos[]', [])
    
    for preco_json in precos_data:
        try:
            print("Preço JSON:", preco_json)
            preco_obj = json.loads(preco_json)  # Deserializa o JSON
            # Adiciona diretamente ao banco sem usar o schema
            novo_preco = ProdutoLoja(
                produto_id=novo_produto.id,
                loja_id=preco_obj['lojaId'],
                preco_venda=preco_obj['precoVenda']
            )
            db.session.add(novo_preco)
        except Exception as e:
            return jsonify({"error": f"Erro ao processar preço: {str(e)}"}), 400

    # Adiciona os preços no banco
    db.session.commit()  # Agora salva o produto e os preços

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
    produto_atualizado = produto_schema.load({
        'descricao': data['descricao'],
        'custo': data['custo'],
        'imagem': data['imagem']
    }, instance=produto, session=db.session)

    ProdutoLoja.query.filter_by(produto_id=produto.id).delete()

    # Processa e valida a lista de preços
    precos_data = data.get('precos[]', [])
    if isinstance(precos_data, str):
        precos_data = [precos_data]
    
    for preco_json in precos_data:
        
        try:
            print("Preço JSON:", preco_json)
            preco_obj = json.loads(preco_json)  # Deserializa o JSON
            # Adiciona diretamente ao banco
            novo_preco = ProdutoLoja(
                produto_id=produto_atualizado.id,
                loja_id=preco_obj['lojaId'],
                preco_venda=preco_obj['precoVenda']
            )
            db.session.add(novo_preco)
        except Exception as e:
            return jsonify({"error": f"Erro ao processar preço: {str(e)}"}), 400

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


@produto_bp.route('/produto/maxId', methods=['GET'])
def max_id():
    max_id_produto = db.session.query(func.max(Produto.id)).scalar()
    return jsonify(max_id=max_id_produto)