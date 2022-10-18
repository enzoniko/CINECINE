from app import db

#class Room(db.Model):

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    # Generos vai ter que ser uma string grande com cada genero separado por virgula
    generos = db.Column(db.String(120), nullable=False)
    legendado = db.Column(db.Boolean, nullable=False)
    # Horarios vai ter que ser uma string grande com cada horario separado por virgula
    horarios = db.Column(db.String(120), nullable=False)
    threeDimensions = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"User('{self.nome}', '{self.generos}', '{self.legendado}', '{self.horarios}', '{self.threeDimensions}')"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    forma = db.Column(db.String(20), nullable=False)
    ingressos = db.Column(db.Integer, nullable=False)
    meias = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User('{self.valor}', '{self.forma}', '{self.ingressos}', '{self.meias}')"