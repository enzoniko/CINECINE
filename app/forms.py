
from email.policy import default
from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange


class AdminLoginForm(FlaskForm):
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=20)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CompraForm(FlaskForm):
    meias = IntegerField('Selecione a quantidade de meia-entradas', validators=[NumberRange(min=0)], default=0)
    maneira = SelectField('Selecione a maneira de pagamento', choices=[('Dinheiro', 'Dinheiro'), ('Débito', 'Débito'), ('Crédito', 'Crédito')])
    submit = SubmitField('Comprar') 
