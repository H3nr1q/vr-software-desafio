from app.extensions import db

class Produto(db.Model):
    __tablename__ = "produto"
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(60), nullable=False)
    custo = db.Column(db.Numeric(13, 3))
    imagem = db.Column(db.LargeBinary(length=(2**32) - 1), nullable=True)  # Define explicitamente como LONGBLOB