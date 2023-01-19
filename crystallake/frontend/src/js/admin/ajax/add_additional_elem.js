const errors = require("../errors");
$(document).ready(function (){

    $('.add_additional_form').on('submit', function (event, data={}){
        event.preventDefault();

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': data.id, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
                window.location.reload();
            },
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                errors.handle_errors(response['message'], $('.errors_list'))
            },
        });

    });
})