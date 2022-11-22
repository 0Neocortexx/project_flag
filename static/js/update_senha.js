$(function(){
    $(document).on("click",'#update_senha',function(){
        email = sessionStorage.getItem('email');
        senha = $('#nova_senha').val();
        meuip = sessionStorage.getItem('meuip');
        jwt = sessionStorage.getItem('jwt')

        var log = JSON.stringify({ email: email, nova_senha: senha  });

        $.ajax({
            url: `http://${meuip}:5000/update_senha`,
            type: 'PUT',
            dataType: 'json',
            contentType: 'application/json',
            headers: { Authorization: 'Bearer ' + jwt },
            data: log, 
            success: updateConcluido
    });
    function updateConcluido(retorno){
        if (retorno.Resultado == 'sucesso'){
            window.alert('Alteração feita com sucesso');
            window.location.assign('/perfil');
    } else if (retorno.Resultado == 'nulo'){
        alert('Não pode inserir um texto vazio');
    }else {
        alert('Ocorreu um erro, verifique a senha foi preenchido corretamente!');
    }}
});
});