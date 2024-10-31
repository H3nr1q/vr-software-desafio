from app.extensions import db

class ProdutoLoja(db.Model):
    __tablename__ = "produtoloja"
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    loja_id = db.Column(db.Integer, db.ForeignKey("loja.id"), nullable=False)
    preco_venda = db.Column(db.Numeric(13, 3), nullable=False)
    produto = db.relationship("Produto", backref="precos")
    loja = db.relationship("Loja")
