$(document).ready(function (){

    $('#temp_login_from_id').on('submit', function (event){
        event.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            success: function (response){
                console.log(response.data)
            },
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                console.log(response['message'])
            },
        }).statusCode({
           302: function (data){
                const response = jQuery.parseJSON(data.responseText)
                window.location.href = response['data']
            }
        });

    });
})