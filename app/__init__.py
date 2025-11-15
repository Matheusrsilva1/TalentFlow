from flask import Flask
from dotenv import load_dotenv
import os

try:
    from pymongo import MongoClient
except Exception:
    MongoClient = None

def create_app():
    app = Flask(__name__)
    load_dotenv()
    uri = os.getenv('MONGODB_URI')
    db_name = os.getenv('MONGODB_DB', 'talentflow')
    if uri and MongoClient:
        try:
            kwargs = {'serverSelectionTimeoutMS': 5000}
            try:
                import certifi
                kwargs['tlsCAFile'] = certifi.where()
                kwargs['tls'] = True
            except Exception:
                pass
            client = MongoClient(uri, **kwargs)
            client.admin.command('ping')
            app.config['DB'] = client[db_name]
            app.config['DB_ERROR'] = None
        except Exception as e:
            app.config['DB'] = None
            app.config['DB_ERROR'] = str(e)
    else:
        app.config['DB'] = None
        app.config['DB_ERROR'] = 'MONGODB_URI ausente no .env.'

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
