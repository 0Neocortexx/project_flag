$(function(){
    $(document).on("click",'#update_senha',function(){
        email = sessionStorage.getItem('email');
        senha = $('#nova_senha').val();
        var log = JSON.stringify({ email: email, nova_senha: senha  });

        $.ajax({
            url: `https://projectflag.pythonanywhere.com/update_senha`,
            type: 'PUT',
            dataType: 'json',
            contentType: 'application/json',
            data: log,
            success: updateConcluido
    });
    function updateConcluido(retorno){
        if (retorno.Resultado == 'sucesso'){
            window.alert('Alteração feita com sucesso');
            window.location.assign('/perfil');
    } else if (retorno.Resultado == 'nulo'){
        alert('Não pode inserir um texto vazio');
    }else if(retorno.Resultado == 'Invalido'){
        alert('A Senha possui caracteres inválidos.')
    }

    else {
        alert('Ocorreu um erro, verifique a senha foi preenchido corretamente!'+retorno.Detalhes);
    }}
});
});