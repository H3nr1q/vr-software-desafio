from app.extensions import db

class Loja(db.Model):
    __tablename__ = "loja"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(60), nullable=False)
