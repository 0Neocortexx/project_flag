$(function(){
    $(document).on("click",'#carregar',function(){
        user_email = sessionStorage.getItem('email')
        meuip = sessionStorage.getItem('meuip');
        jwt = sessionStorage.getItem('jwt')

        var log = JSON.stringify({ email: user_email});

        $.ajax({
            url: `http://${meuip}:5000/carregar_desafio`,
            type: 'POST',
            dataType: 'json',
            contentType: 'application/json',
            headers: { Authorization: 'Bearer ' + jwt },
            data: log, 
            success: sucesso,
            error: erroAoCarregar
    });
    function sucesso (retorno){
        if (retorno.Resposta === 'sucesso'){
            if(retorno.desafio === 1){
                window.location.assign('/desafio1');
            }else if(retorno.desafio === 2){
                window.location.assign('/desafio2');
            }else if(retorno.desafio === 3){
                window.location.assign('/desafio3');
        } else{
            alert('Você já realizou todos os desafios')
        }
    }};  function erroAoCarregar(retorno){
            window.alert('Ocorreu um erro no backend',retorno.erro)
}});
});