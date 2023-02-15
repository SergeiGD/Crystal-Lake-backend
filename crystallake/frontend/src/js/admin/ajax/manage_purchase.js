const errors = require("../../common/errors");
$(document).ready(function (){

    $('.manage_purchase').on('submit', function (event){
        event.preventDefault();

        const form = $(this)
        $('#id_create-multiple_rooms_acceptable').val('True')


        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            success: function (){
                window.location.reload();
            },
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                errors.handle_errors(response['message'], form.find('.errors_list'))
            },
        });

    });
})