const main_info_errors = require("./main_info_errors");

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
                main_info_errors.handle_errors(response['message'])
                $([document.documentElement, document.body]).animate({
                    scrollTop: $("#main_info_errors").offset().top
                }, 200);
            },
        }).statusCode({
           302: function (data){
                const response = jQuery.parseJSON(data.responseText)
                window.location.href = response['data']
            }
        });
    })
})