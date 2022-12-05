from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, BooleanField, IntegerField, SelectField, StringField, FieldList, TimeField
from wtforms.validators import DataRequired, Length, NumberRange

class AdminLoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Login')

class CompraForm(FlaskForm):
    meias = IntegerField('Selecione a quantidade de meia-entradas', validators=[NumberRange(min=0)], default=0)
    maneira = SelectField('Selecione a maneira de pagamento', choices=[('Dinheiro', 'Dinheiro'), ('Débito', 'Débito'), ('Crédito', 'Crédito')])
    submit = SubmitField('Comprar') 

class EditarSessaoForm(FlaskForm):
    titulo = StringField('Alterar o título: ', validators=[DataRequired()])
    classificacao = SelectField('Alterar a classificação: ', choices=[('Livre', 'Livre'), ('+10', '+10'), ('+12', '+12'), ('+14', '+14'), ('+16', '+16'), ('+18', '+18')])
    legenda = BooleanField('Legendado:')
    DDD = BooleanField('3D:')
    horarios = FieldList(unbound_field = TimeField(validators=[DataRequired()], default=datetime.strptime('00:00', '%H:%M')), min_entries=2, max_entries=4, render_kw={"style":"font-size:30px"})
    confirmar = SubmitField('Confirmar', id='confirmar')
    aplicar = SubmitField('Aplicar', id='aplicar')
    cancelar = SubmitField('Cancelar', id='cancelar')
