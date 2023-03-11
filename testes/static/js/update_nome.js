$(function(){
    $(document).on("click",'#update_nome',function(){
        email = sessionStorage.getItem('email');
        nome = $('#novo_nome').val();
        meuip = sessionStorage.getItem('meuip');
        jwt = sessionStorage.getItem('jwt')

        var log = JSON.stringify({ email: email, novo_nome: nome  });

        $.ajax({
            url: `http://${meuip}:5000/update_nome`,
            type: 'PUT',
            dataType: 'json',
            contentType: 'application/json',
            headers: { Authorization: 'Bearer ' + jwt },
            data: log, 
            success: updateConcluido,
    });
    function updateConcluido(retorno){
        if (retorno.Resultado == 'sucesso'){
            sessionStorage.getItem('nome');
            sessionStorage.removeItem('nome');
            sessionStorage.setItem('nome',retorno.nome);
            window.alert('Nome alterado!')
            window.location.assign('/perfil');
        } else if (retorno.Resultado == 'nulo'){
            alert('Não pode inserir um texto vazio');
        }else{
            window.alert('Ocorreu um erro durante o update')
    }};
});
});