const errors = require("../../common/errors");

$(document).ready(function (){
    $('.default_ajax_edit').on('submit', function (event){
        event.preventDefault();
        const current_form = $(this);

        $.ajax({
            url: current_form.attr('action'),
            type: 'POST',
            data: $(current_form).serialize(),
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                errors.handle_errors(response['message'], $('#main_info_errors'))
            },
        }).statusCode({
           302: function (data){
                const response = jQuery.parseJSON(data.responseText)
                window.location.href = response['data']
            }
        });
    })
})