from extensions import db
from flask_login import UserMixin


user_roles = db.Table('user_roles',
                      db.Column('client_id', db.Integer, db.ForeignKey(
                          'clients.id', ondelete='CASCADE')),
                      db.Column('role_id', db.Integer, db.ForeignKey(
                          'roles.id', ondelete='CASCADE'))
                      )


class Client(db.Model, UserMixin):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref='clients')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    roles = db.Column(db.String(20), unique=True)
