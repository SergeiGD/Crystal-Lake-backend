const errors = require("../../common/errors");

$(document).ready(function (){
    $('#client_reset_phone_form').on('submit', function (e){
        e.preventDefault();

        const errors_list = $(this).find('.errors_wrapper')

        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            type: 'POST',
            success: function (){
                $('#client_reset_phone_form').addClass('hidden_auth_form')
                $('#client_reset_form').removeClass('hidden_auth_form')
            },
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                errors.handle_errors(response['message'], errors_list)
            },
        })
    })
})