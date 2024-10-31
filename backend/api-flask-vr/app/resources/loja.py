from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.loja import Loja
from app.schemas.loja import LojaSchema

loja_bp = Blueprint('loja_bp', __name__)
loja_schema = LojaSchema()
lojas_schema = LojaSchema(many=True)

@loja_bp.route('/lojas', methods=['GET'])
def get_lojas():
    lojas = Loja.query.all()
    return lojas_schema.jsonify(lojas)

@loja_bp.route('/loja', methods=['POST'])
def add_loja():
    data = request.get_json()
    nova_loja = Loja(
        descricao=data['descricao']
    )
    db.session.add(nova_loja)
    db.session.commit()
    return loja_schema.jsonify(nova_loja), 201