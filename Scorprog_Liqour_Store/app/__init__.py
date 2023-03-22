from flask import Flask
from config import Config
from extensions import db, migrate,login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    with app.app_context():
        #model importing to run with context manager
        from .models.users import Client
        from .models.drinks import Products

        ######config
        app.config.from_object(config_class)
        db.init_app(app)
        migrate.init_app(app, db)

        ######Login Manager
        #initialize login_manager
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'
        
        #user_loader
        @login_manager.user_loader
        def load_user(user_id):
            return Client.query.get(int(user_id))
        
        ######Blueprints Registration
        #main blueprint
        from .blueprints.main_blueprint import main
        app.register_blueprint(main)

        #auth blurprint
        from .blueprints.auth_blueprint import auth
        app.register_blueprint(auth)

        db.create_all()
        return app