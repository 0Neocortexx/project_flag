$(function(){
    $(document).on("click",'#submit-login',function(){
        email = $('#email-login').val();
        senha = $('#senha-login').val();
        meuip = sessionStorage.getItem('meuip');

        var log = JSON.stringify({ email: email, senha: senha  });

        $.ajax({
            url: `http://${meuip}:5000/realizar_login`,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            data: log, 
            success: loginConcluido,
            error: erroAoLogar
    });
    function loginConcluido (retorno){
        if (retorno.Resultado === 'sucesso'){
            sessionStorage.setItem('email',retorno.email);
            sessionStorage.setItem('nome',retorno.nome);
            sessionStorage.setItem('jwt',retorno.Detalhes);
            window.alert('Login relizado com sucesso!');
            window.location.assign('/render_menu');
        }else if (retorno.Resultado === 'senha inv'){
            alert('Senha invalida');
        }else{
            alert(`Verifique se os dados estão corretos.`);
        }
    };
    function erroAoLogar(retorno){
            window.alert(`Login Incorreto. Verifique a senha,${retorno.Detalhes}`)
    }
});
});