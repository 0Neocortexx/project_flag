$(function(){
    $(document).on("click",'#update_email',function(){
        email = sessionStorage.getItem('email');
        novo_email = $('#novo_email').val();
        meuip = sessionStorage.getItem('meuip');
        jwt = sessionStorage.getItem('jwt')

        var log = JSON.stringify({ email: email, novo_email: novo_email  });

        $.ajax({
            url: `http://${meuip}:5000/update_email`,
            type: 'PUT',
            dataType: 'json',
            contentType: 'application/json',
            headers: { Authorization: 'Bearer ' + jwt },
            data: log, 
            success: updateConcluido,
    });
    function updateConcluido(retorno){
        if (retorno.Resultado == 'sucesso'){
            sessionStorage.removeItem('email');
            sessionStorage.setItem('email',retorno.email);
            window.alert('Alteração feita com sucesso');
            window.location.assign('/perfil');
        } else if (retorno.Resultado == 'nulo'){
            alert('Email invalido!');
        }else if (retorno.Resultado == 'Usuário cadastrado'){
            alert('Email já esta sendo utilizado por outra conta!');
        }else {
        window.alert('Ocorreu um erro, verifique se o email foi preenchido corretamente!');
        }};

});
});