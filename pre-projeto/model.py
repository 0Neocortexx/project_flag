from config import *

class Usuario(db.Model):
    email = db.Column(db.String(254), primary_key=True, nullable=False)
    nome = db.Column(db.String(254), nullable=False)
    senha = db.Column(db.String(254), nullable=False)
    objetivo = db.Column(db.String(254), nullable=False)

    def __str__(self):
        return f'Nome: {self.nome}, Email: {self.email}, Senha: {self.senha}, Objetivo: {self.objetivo}'

    def json(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "objetivo": self.objetivo
        }
    
if __name__=="__main__":
    db.create_all()