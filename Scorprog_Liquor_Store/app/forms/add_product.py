from flask_wtf import FlaskForm
from wtforms.validators import input_required, Length
from wtforms import StringField, BooleanField, SubmitField, SelectField, IntegerField, TextAreaField


class Liquor(FlaskForm):
    name = StringField('Liqour Name: ',validators=[input_required(), Length(max=50)])
    choice = [('gin', 'Gin'),('whiskey','Whiskey'),('wine','Wine'),('beer', 'Beer')]
    type = SelectField('Alcohol Type: ', choices=choice, validators=[input_required()])
    price = IntegerField('Price', validators=[input_required()])
    description = TextAreaField('Description', validators=[input_required(), Length(min=10, max=200)])
    available = BooleanField('Available: ')
    submit = SubmitField('Add Product')