from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_principal import Principal, RoleNeed, Permission

db=SQLAlchemy()
migrate=Migrate()
login_manager = LoginManager()
principal = Principal()

admin_role = RoleNeed('admin')
admin_permission = Permission(RoleNeed('admin'))