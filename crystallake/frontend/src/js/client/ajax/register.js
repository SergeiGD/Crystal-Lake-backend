const errors = require("../../common/errors");

$(document).ready(function (){
    $('#client_register_from').on('submit', function (){
        event.preventDefault();

        const errors_list = $(this).find('.auth_errors')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            success: function (){
                $('#client_register_from').addClass('hidden_auth_form')
                $('#client_register_code_from').removeClass('hidden_auth_form')
            },
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                errors.handle_errors(response['message'], errors_list)
            },
        })
    })
})