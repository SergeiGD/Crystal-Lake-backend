const errors = require("../errors");
$(document).ready(function (){

    $('.manage_purchase').on('submit', function (event){
        event.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            success: function (){
                window.location.reload();
            },
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                errors.handle_errors(response['message'], $('.errors_list'))
            },
        });

    });
})