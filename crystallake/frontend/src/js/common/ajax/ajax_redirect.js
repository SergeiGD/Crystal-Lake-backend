const errors = require("../../common/errors");

$(document).ready(function (){
    $('.ajax_redirect').on('submit', function (){
        event.preventDefault();

        const errors_list = $(this).find('.errors_wrapper')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                errors.handle_errors(response['message'], errors_list)
            },
        }).statusCode({
           302: function (data){
                const response = jQuery.parseJSON(data.responseText)
                window.location.href = response['data']
            }
        });
    })
})