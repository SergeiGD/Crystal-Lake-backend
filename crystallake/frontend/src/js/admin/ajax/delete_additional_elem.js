const errors = require("../errors");

$(document).ready(function (){

    $('.delete_additional_form').on('submit', function (event, data){
        const current_form = $(this);
        event.preventDefault();

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': data['id'], 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
                window.location.reload();
            },
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                const errors_list = current_form.closest('table').siblings('.additional_errors');
                errors.handle_errors(response['message'], errors_list)
            },
        }).statusCode({
           302: function (data){
                const response = jQuery.parseJSON(data.responseText)
                window.location.href = response['data']
            }
        });

    });

    // $(document).ajaxStop(function(){
    //     window.location.reload();
    // });

});