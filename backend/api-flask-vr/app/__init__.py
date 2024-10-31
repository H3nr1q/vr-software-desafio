from flask import Flask
from .config import Config
from .extensions import db, ma, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    #Models para aplicação da Migration
    from .models import loja
    from .models import produto
    from .models import produtoloja

    #Blueprint

    from .resources.produto import produto_bp
    from .resources.loja import loja_bp
    # from .resources.produtoloja import produtoloja_bp

    app.register_blueprint(produto_bp)
    app.register_blueprint(loja_bp)
    # app.register_blueprint(produtoloja_bp)

    return app

