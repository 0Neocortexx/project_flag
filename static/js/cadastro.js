$(function() {

    $(document).on('click', '#btnCadastro', function(){
        user_nome = $('#nome-cadastro').val();
        user_email = $('#email-cadastro').val();
        user_senha = $('#senha-cadastro').val();
        meuip = sessionStorage.getItem('meuip');
        var dados = JSON.stringify({nome: user_nome, email: user_email, senha: user_senha});

        $.ajax({
            url: meuip,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: dados,
            success: usuarioCadastrado,
            error: anyError
        });


        function usuarioCadastrado (retorno) {
            if (retorno.Resultado === 'sucesso') {
                alert('Usuário cadastrado com sucesso!');
                $('#mensagem').text('Usuário cadastrado com sucesso!');

                $('#nome-cadastro').val('');
                $('#email-cadastro').val('');
                $('#senha-cadastro').val('');
                window.location.assign('/login');

                sessionStorage.setItem('email',retorno.email);
                sessionStorage.setItem('nome',retorno.nome);
                window.location.assign('/login')

            }else if(retorno.Resultado === 'nulo'){
                alert('Não pode ter campos nulos.');
                window.location.assign("/cadastro");
            }else if(retorno.Resultado === 'email inv'){
                alert('Email Invalido');
                window.location.assign("/cadastro");
            } else if(retorno.Resultado === 'Usuário cadastrado'){
                alert('O email utilizado já está cadastrado!');
                window.location.assign("/cadastro");
            }
        }

        function anyError (retorno) {
            alert('Erro ao contatar back-end: ' + retorno.Resultado + ': ' + retorno.Detalhes);
        }

    });


});
