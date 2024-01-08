$(function(){
    $(document).on("click",'#responder',function(){
        var resp = prompt("Digite a senha:");
        user_email = sessionStorage.getItem('email');
        var log = JSON.stringify({ email: user_email, resposta: resp });

        $.ajax({
            url: `https://projectflag.pythonanywhere.com/nivel3`,
            type: 'PUT',
            dataType: 'json',
            contentType: 'application/json',
            data: log,
            success: sucesso,
            error: erroAoResponder
    });
    function sucesso (retorno){
        if (retorno.Resultado === 'certa'){
            alert('Resposta correta');
            window.location.assign('/desafio4');
        }else{
            alert('Resposta errada!');
        }
    };
    function erroAoResponder(retorno){
            window.alert('Ocorreu um erro no backend',retorno.erro)
    }
});
});