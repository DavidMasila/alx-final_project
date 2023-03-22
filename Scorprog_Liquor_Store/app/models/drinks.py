from extensions import  db

class Products(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(50), nullable = False)
    type = db.Column(db.String(50), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    description = db.Column(db.Text, nullable = False)
    available = db.Column(db.Boolean)

