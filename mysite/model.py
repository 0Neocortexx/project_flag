from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from datetime import timedelta
import bcrypt

# configurações
app = Flask(__name__)
app.app_context().push()
# caminho do banco de dados
path = os.path.dirname(os.path.abspath(__file__))
arquivobd = os.path.join(path, 'project_flag.db')
# sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+arquivobd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# segurança - JWT
app.config['JWT_SECRET_KEY'] = 'theAndrewislying'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes= 30)

class Desafio(db.Model):
    """Representa um desafio.
    Herda de db.Model que é a classe base para todos os modelos no SQLAlchemy.
    """
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(254))
    password = db.Column(db.String(254))
    pont_ger = db.Column(db.Integer,default = 0) # Pontuação Geral do desafio.
    pont_cript = db.Column(db.Integer,default = 0) # Pontuação Criptografia do desafio.
    pont_estgn = db.Column(db.Integer,default = 0) # Pontuação Estegnografia do desafio.
    pont_char = db.Column(db.Integer,default = 0) # Pontuação de Charadas do desasfio.

    def __str__(self):
        return f'{self.id},{self.nome},{self.password}'

class Usuario(db.Model):
    """Representa um usuário.
    Herda de db.Model que é a classe base para todos os modelos no SQLAlchemy.
    """
    id_email = db.Column(db.String(254), primary_key=True)
    nome = db.Column(db.String(254))
    senha = db.Column(db.String(254))
    pont_ger = db.Column(db.Integer,nullable = True,default = 0) # Pontuação Geral.
    pont_cript = db.Column(db.Integer,nullable = True,default = 0) # Pontuação Criptografia.
    pont_estgn = db.Column(db.Integer,nullable = True,default = 0) # Pontuação Estegnografia.
    pont_char = db.Column(db.Integer,nullable = True,default = 0) # Pontuação de Charadas.
    desafio_atual = db.Column(db.Integer,db.ForeignKey(Desafio.id), nullable = False,default = 1)


    def __str__(self):
        """Retorna o objeto em string."""
        return f"{self.id_email},{self.nome},{self.senha},{self.pont_ger},{self.pont_cript},{self.pont_estgn},{self.pont_char}"

    def json(self):
        """Retorna o objeto no formato json."""
        return {
            'email':self.id_email,
            'nome':self.nome
        }

    def ret_pont(self):
        """Retorna as pontuações em formato json."""
        return{
            'pont_ger':self.pont_ger,
            'pont_cript':self.pont_cript,
            'pont_estgn':self.pont_estgn,
            'pont_char':self.pont_char
        }

def criptografar_sen(senha: str):
        """Criptografa a senha usando o bcrypt."""
        senha = senha.encode('utf-8') # Deixa a senha no padrão utf-8.
        nova_senha = bcrypt.hashpw(senha,bcrypt.gensalt()) # Gera a senha criptografada
        senha = nova_senha
        return senha


def verifica_senha(senha_dig:str,email_dig:str):
    """Verifica se a senha digitada corresponde a que está no banco de dados
    usando o email de referência.

    Args:
        senha_dig (str): senha digitada.
        email_dig (str): email digitado.

    Returns:
        bool: False caso aconteça algum erro ou caso a senha não esteja no banco;
        True caso esteja e corresponda.
    """
    for q in db.session.query(Usuario.senha).filter(Usuario.id_email==email_dig).all():
        try:
            resultado = bcrypt.checkpw(senha_dig,q[0])
        except:
            return False
        if q == None:
            return False
        return resultado

filtro = ('alert.','<script>','<','>','javascript',';','--',",","=","+",'/',"'",'"',"src=","admin'--","js"
            ,"or 1=1", "delete from usuario", "document.write","sessionStorage.","Window.","document.",'href=',"]>")

def get_usuario(email: str):
    return Usuario.query.get(email)

def verifica_injecao(dado: str):
    resposta = dado
    for f in filtro: # laço de repetição que verifica se não há um texto suspeito de possuir injeção XSS ou SQL.

        if f in dado:
            resposta = 'inv'
        elif dado == '':
            resposta = None
    return resposta

def verifica_injecao_email(email: str):
    for f in filtro: # laço de repetição que verifica se não há um texto suspeito de possuir injeção XSS ou SQL.
        if f in email:
            resposta = email.replace(f,'')
    if resposta == '' and len(resposta)<=4 or '@' not in resposta:
        resposta = None
    return resposta

def atualizar_user(dados):
    try:
        user = get_usuario(dados['email'])
        if user is not None:
            if 'novo_nome' in dados:
                user.nome = verifica_injecao(dados['novo_nome'])
            if 'senha' in dados:
                senha = verifica_injecao(dados['senha'])
                user.senha = criptografar_sen(senha)
            if 'email' in dados:
                user.email = verifica_injecao_email(dados['novo_email'])
            if dados is None:
                return False
            db.session.commit()
            return True
        return False
    except:
        return False


if __name__ == '__main__':

    db.create_all()
    #desafio1 = Desafio(nome="Desafio4",password='')
    #db.session.query(Desafio).filter_by(id = 3).update(dict(password = 'sinfonia'))
    #db.session.add(desafio1)
    #db.session.query(Usuario).filter_by(desafio_atual = 3).update(dict(pont_ger= 0, pont_cript = 20, pont_estgn=0,pont_char =0))
    #db.session.query(Desafio).filter_by(id = 3).update(dict(pont_ger= 20, pont_cript = 20, pont_estgn=0,pont_char =0))
    #db.session.commit()
    db.session.query(Desafio).filter_by(id = 3).update(dict(pont_ger= 20, pont_cript = 20, pont_estgn=0,pont_char =0))
    desafio1 = Desafio(nome="Desafio1",password='senha', pont_ger=10, pont_char=10)
    desafio2 = Desafio(nome="Desafio2",password='culpado',pont_ger=30,pont_cript=10,pont_char=20)
    desafio3 = Desafio(nome="Desafio3",password='sinfonia',pont_ger=20, pont_cript=20)
    db.session.add(desafio1)
    db.session.add(desafio2)
    db.session.add(desafio3)
    db.session.commit()
    print("inserido!")


    #for a in db.session.query(Usuario.nome).filter().order_by(Usuario.pont_ger.desc()).slice(0,21):
        #print(a)