$(function(){
    $(document).on("click",'#responder',function(){
        var resp = prompt("Digite a senha:");
        user_email = sessionStorage.getItem('email');
        meuip = sessionStorage.getItem('meuip');
        jwt = sessionStorage.getItem('jwt')

        var log = JSON.stringify({ email: user_email, resposta: resp });

        $.ajax({
            url: `http://${meuip}:5000/nivel2`,
            type: 'PUT',
            dataType: 'json',
            contentType: 'application/json',
            headers: { Authorization: 'Bearer ' + jwt },
            data: log, 
            success: sucesso,
            error: erroAoResponder
    });
    function sucesso (retorno){
        alert(`${retorno.Resultado}`)
        if (retorno.Resultado === 'certa'){
            alert('Resposta correta');
            window.location.assign('/desafio3');
        }else{
            alert('Resposta errada!');
        }
    };
    function erroAoResponder(retorno){
            window.alert('Ocorreu um erro no backend',retorno.erro)
    }
});
});