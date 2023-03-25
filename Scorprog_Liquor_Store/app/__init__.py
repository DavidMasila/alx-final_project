from flask import Flask, redirect, url_for, flash
from config import Config
from extensions import db, migrate,login_manager, principal, admin_permission, admin_role
from flask_principal import Identity, identity_loaded, PermissionDenied, RoleNeed, Permission
from flask_login import current_user

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
        
        #initialize flask_principal
        principal.init_app(app)

        #user information providers
        @identity_loaded.connect_via(app)
        def on_identity_loaded(sender, identity):
            identity.user = current_user

            if hasattr(current_user, 'is_admin'):
                if current_user.is_admin:
                    identity.provides.add(admin_role)
                    identity.provides.add(admin_permission)
                else:
                    identity.provides.add(Permission(RoleNeed('user')))
                    identity.provides.add(RoleNeed('user'))

        @app.errorhandler(PermissionDenied)
        def handle_permission_denied(e):
            flash(f"You lack the permission to access this page. Log in with the right account")
            return(redirect(url_for('auth.login')))
        
        ######Blueprints Registration
        #main blueprint
        from .blueprints.main_blueprint import main
        app.register_blueprint(main)

        #auth blurprint
        from .blueprints.auth_blueprint import auth
        app.register_blueprint(auth)

        db.create_all()
        return app