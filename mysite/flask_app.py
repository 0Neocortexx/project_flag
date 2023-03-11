from model import app, Usuario, filtro,db,criptografar_sen,verifica_senha,get_usuario,verifica_injecao,Desafio
from flask import render_template, request,jsonify

@app.route('/')
def home():
    '''Rota inicial do site

    Returns:
        index(html): retorna a página inicial
    '''
    return render_template('index.html')

@app.route('/update')
def update():
    '''Renderiza a página de update

    Returns:
        updates(html): retorna a página de update
    '''
    return render_template('updates.html')

@app.route('/render_menu', methods=['GET'])
def niveis():
    '''Renderiza a página de niveis

    Returns:
        niveis(html): Página de niveis
    '''
    return render_template('menu.html')

@app.route('/cadastro', methods= ['GET'])
def cadastro():
    '''Renderiza a página de cadastro

    Returns:
        cadastro(html): página de cadastro
    '''
    return render_template('cadastro.html')

@app.route('/login', methods= ['GET'])
def login():
    '''Renderiza a página de login.

    Returns:
        login(html): página de login
    '''
    return render_template('login.html')

@app.route('/perfil', methods=['GET'])
def profile():
    return render_template('perfil.html')

@app.route('/ranking', methods=['GET'])
def ranking():
    return render_template('ranking_global.html')

@app.route('/desafio1',methods=['GET'])
def render_desafio1():
    return render_template('desafio1.html')

@app.route('/desafio2',methods=['GET'])
def render_desafio2():
    return render_template('desafio2.html')

@app.route('/desafio3',methods=['GET'])
def render_desafio3():
    return render_template('desafio3.html')

@app.route('/desafio4',methods=['GET'])
def render_desafio4():
    return render_template('desafio4.html')

@app.route('/desafio5',methods=['GET'])
def render_desafio5():
    return render_template('desafio5.html')

@app.route('/desafio6',methods=['GET'])
def render_desafio6():
    return render_template('desafio6.html')


@app.route('/cadastro', methods=['POST'])
def realizar_cadastro():
    try:
        dados = request.get_json(force=True)
        user = Usuario(id_email =  dados['email'],nome = dados['nome'],senha = dados['senha'])
        for f in filtro:
            if f in user.nome or f in user.id_email or f in user.senha:
                user.nome = user.nome.replace(f,'')
                user.id_email = user.id_email.replace(f,'')
                user.senha = user.senha.replace(f,'')
        if user.id_email == '' or user.nome == '' or user.senha == '':
            resposta = jsonify({'Resultado': 'nulo'})
            resposta.headers.add('Access-Control-Allow-Origin', '*')
            return resposta
        if '@' not in user.id_email and len(user.id_email)<=6:
            resposta = jsonify({'Resultado':'email inv'})
            resposta.headers.add('Access-Control-Allow-Origin', '*')
            return resposta
        a = db.session.query(Usuario.id_email).filter_by(id_email = user.id_email).first()
        if a is not None:
            resposta = jsonify({'Resultado':'Usuário já cadastrado'})
            resposta.headers.add('Access-Control-Allow-Origin', '*')
            return resposta
        user.senha = criptografar_sen(user.senha)
        db.session.add(user) # Adiciona o usuário na tabela.
        db.session.commit()
        resposta = jsonify({'Resultado': 'sucesso', 'Detalhes': 'ok'})
    except Exception as e:
        # Retorna um erro de cadastro caso ocorra.
        resposta = jsonify({'Resultado': 'Erro', 'Detalhes': str(e)})
    resposta.headers.add('Access-Control-Allow-Origin', '*')
    return resposta

@app.route('/login', methods= ['POST'])
def realizar_login():
    try:
        dados = request.get_json(force=True) #Pega os dados do formulario.
        email = str(dados['email'])
        senha = str(dados['senha'])
        for f in filtro: # laço de repetição que verifica se não há um texto suspeto de possuir injeção XSS ou SQL.
            if f in email or f in senha:
                email = email.replace(f,'')
                senha = senha.replace(f,'')
        senha = senha.encode('utf-8') # Deixa a senha no padrão utf-8.
        login = verifica_senha(senha,email) # Função que verifica a existencia do usuário.
        user = get_usuario(email) # Select que pega o email e nome do usuário.
        email = user.id_email
        nome = user.nome
        resposta = jsonify({'Resultado': 'sucesso', 'nome':nome,'email':email})
        resposta.headers.add('Access-Control-Allow-Origin', '*')
        if login == False:
            resposta = jsonify({'Resultado': 'senha inv'})
    except Exception as e:
        # Retorna um erro de cadastro caso ocorra.
        resposta = jsonify({'Resultado': 'Erro', 'Detalhes': str(e)})
    return resposta

@app.route('/carregar_desafio',methods=['POST'])
def render_nivel():
    try:
        dados = request.get_json(force=True)
        print(dados)
        email = dados['email']
        user = get_usuario(email)
        resposta = jsonify({'Resposta':'sucesso','desafio':user.desafio_atual})
    except Exception as e:
        resposta=jsonify({'Resposta':'erro','Detalhes':str(e)})
    resposta.headers.add('Access-Control-Allow-Origin', '*')
    return resposta


@app.route('/update_nome', methods=['PUT'])
def update_nome():
    try:
        dados = request.get_json(force=True) # Pega os dados do formulario
        user = str(dados['novo_nome'])
        for f in filtro: # laço de repetição que verifica se não há um texto suspeito de possuir injeção XSS ou SQL.
            if f in user:
                user = user.replace(f,'')
        if dados['novo_nome'] == '':
            resposta = jsonify({'Resultado':'nulo'})
            return resposta
        email_user = dados['email']
        db.session.query(Usuario).filter_by(id_email=email_user).update(dict(nome=user)) # Realiza o update do nome
        db.session.commit()
        user = db.session.query(Usuario.nome).filter_by(id_email=email_user).first() # Retorna uma lista com o novo nome.
        nome = user[0] # Retira o nome de uma lista
        resposta = jsonify({'Resultado': 'sucesso','nome':nome})
        resposta.headers.add('Access-Control-Allow-Origin', '*')
    except Exception as e:
        # Retorna um erro de cadastro caso ocorra.
        resposta = jsonify({'Resultado': 'Erro', 'Detalhes': str(e)})
        return resposta
    return resposta

@app.route('/update_email', methods=['PUT'])
def update_email():
    try:
        dados = request.get_json(force=True) # Pega os dados do formulario
        email_user = dados['email']
        email_novo = str(dados['novo_email'])
        for f in filtro: # laço de repetição que verifica se não há um texto suspeto de possuir injeção XSS ou SQL.
            if f in email_novo:
                email_novo = email_novo.replace(f,'')
        if email_novo == '' and len(email_novo)<=4 or '@' not in email_novo:
            resposta = jsonify({'Resultado':'nulo'})
            return resposta
        db.session.query(Usuario).filter_by(id_email=email_user).update(dict(id_email=email_novo)) # Atualiza o email do usuário.
        db.session.commit()
        user = db.session.query(Usuario.id_email).filter_by(id_email=email_novo).first() # Retorna uma lista com o novo email.
        email = user[0] # Tira o email da lista
        resposta = jsonify({'Resultado': 'sucesso','email':email})
    except Exception as e:
        # Retorna um erro de cadastro caso ocorrá.
        resposta = jsonify({'Resultado': 'Erro', 'Detalhes': str(e)})
        return resposta
    resposta.headers.add('Access-Control-Allow-Origin', '*')
    return resposta


@app.route('/update_senha', methods=['PUT'])
def update_senha():
    try:
        print('entrou')
        dados = request.get_json(force=True) # Pega os dados do formulario.
        email_user = dados['email']
        senha_new = str(dados['nova_senha'])
        senha_ver = verifica_injecao(senha_new) # função que verifica se não há um texto suspeito de possuir injeção XSS ou SQL.
        print(senha_ver)
        if senha_ver is None:
            print('deu nulo')
            resposta = jsonify({'Resultado':'nulo'})
        elif senha_ver == 'inv':
            resposta = jsonify({'Resultado':'Invalido'})
        else:
            print('deu certo')
            senha_new = criptografar_sen(senha_ver)  # função que criptografa a senha
            print(senha_ver)
            db.session.query(Usuario).filter_by(id_email=email_user).update(dict(senha=senha_new)) # Atualiza a senha.
            db.session.commit()
            resposta = jsonify({'Resultado':'sucesso'})
    except Exception as e:
        # Retorna um erro de cadastro caso ocorra.
        resposta = jsonify({'Resultado': 'Erro', 'Detalhes': str(e)})
    resposta.headers.add('Access-Control-Allow-Origin', '*')
    return resposta


@app.route('/nivel1', methods=['PUT'])
def nivel1():
    resposta = jsonify({'Resposta':'errada'})
    dados = request.get_json()
    try:
        answer= str(dados['resposta'])
        for f in filtro:
            if f in answer:
                answer = resposta.replace(f,'')
        user = Usuario.query.get(dados['email'])
        if answer == 'senha' or answer == 'Senha' or answer == 'SENHA' :
            desafio = Desafio.query.get(1)
            if user.desafio_atual == desafio.id:
                user.pont_ger += desafio.pont_ger
                user.pont_cript += desafio.pont_cript
                user.pont_char += desafio.pont_char
                user.pont_estgn += desafio.pont_estgn
                user.desafio_atual += 1
                resposta = jsonify({"Resultado":"certa"})
                db.session.commit()
                return resposta
            else:
                resposta = jsonify({'Resposta':'erro','Detalhes':'Usuário já passou ou não esta no desafio certo'})
                return resposta
    except Exception as e:
        resposta = jsonify({'Resposta':'erro','Detalhes':str(e)})
        return resposta
    resposta.headers.add('Access-Control-Allow-Origin','*')
    return resposta

@app.route("/nivel2",methods=['PUT'])
def nivel2():
    resposta = jsonify({'Resposta':'errada'})
    dados = request.get_json()
    try:
        answer= str(dados['resposta'])
        for f in filtro:
            if f in answer:
                answer = resposta.replace(f,'')
        user = Usuario.query.get(dados['email'])
        if answer == 'culpado' or answer == 'Culpado' or answer == 'CULPADO': #A resposta do desafio não foi definida ainda.
            desafio = Desafio.query.get(2)
            if user.desafio_atual == desafio.id:
                user.pont_ger += desafio.pont_ger
                user.pont_cript += desafio.pont_cript
                user.pont_char += desafio.pont_char
                user.pont_estgn += desafio.pont_estgn
                user.desafio_atual += 1
                resposta = jsonify({"Resultado":"certa"})
                db.session.commit()
                return resposta
            else:
                resposta = jsonify({'Resposta':'erro','Detalhes':'Usuário já passou ou não esta no desafio certo'})
                return resposta
    except Exception as e:
        resposta = jsonify({'Resposta':'erro','Detalhes':str(e)})
        return resposta
    resposta.headers.add('Access-Control-Allow-Origin','*')
    return resposta

@app.route("/nivel3",methods=['PUT'])
def nivel3():
    resposta = jsonify({'Resposta':'errada'})
    dados = request.get_json()
    try:
        answer= str(dados['resposta'])
        for f in filtro:
            if f in answer:
                answer = resposta.replace(f,'')
        user = Usuario.query.get(dados['email'])
        if answer == 'sinfonia': #A resposta do desafio não foi definida ainda.
            desafio = Desafio.query.get(3)
            if user.desafio_atual == desafio.id:
                user.pont_ger += desafio.pont_ger
                user.pont_cript += desafio.pont_cript
                user.pont_char += desafio.pont_char
                user.pont_estgn += desafio.pont_estgn
                user.desafio_atual += 1
                resposta = jsonify({"Resultado":"certa"})
                db.session.commit()
                return resposta
            else:
                resposta = jsonify({'Resposta':'erro','Detalhes':'Usuário já passou ou não esta no desafio certo'})
                return resposta
    except Exception as e:
        resposta = jsonify({'Resposta':'erro','Detalhes':str(e)})
        return resposta
    resposta.headers.add('Access-Control-Allow-Origin','*')
    return resposta

@app.route('/gera_ranking', methods=['GET'])
def gera_ranking():
    resposta = jsonify({'resultado':'ok'})
    resposta.headers.add('Access-Control-Allow-Origin', '*')
    try:
        user = db.session.query(Usuario).order_by(Usuario.pont_ger.desc()).slice(0,20)
        user_json =[ x.return_pont() for x in user]
        resposta = jsonify(user_json)
    except Exception as e:
        resposta = jsonify({'Resultado': 'Erro', 'Detalhes': str(e)})
        return resposta
    return resposta

@app.route('/get_user', methods=['POST'])
def get_user():
    resposta = jsonify({'Resultado':'ok'})
    dados= request.get_json(force=True)
    try:
        email = dados['email']
        user = get_usuario(email)
    except Exception as e:
        resposta = jsonify({'Resultado': 'Erro', 'Detalhes': str(e)})
        return resposta
    resposta = jsonify({'Resultado':'sucesso','estn':str(user.pont_estgn),'cript':str(user.pont_cript),'ger':str(user.pont_ger),'char':str(user.pont_char)})
    resposta.headers.add('Access-Control-Allow-Origin', '*')
    return resposta


