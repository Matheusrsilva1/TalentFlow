from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configurações do aplicativo podem ser adicionadas aqui
    # app.config.from_object('config.Config')

    # Importar e registrar o Blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

    # Adicionar uma rota principal para o dashboard (a ser implementada)
    @app.route('/')
    def index():
        return "Dashboard do Gestor (em breve)"