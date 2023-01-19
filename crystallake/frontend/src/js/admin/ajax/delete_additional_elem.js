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
                // window.location = window.location
                window.location.reload();
                // const table = current_form.closest('.additional_info_tbody');
                // const row = table.find(`[data-id=${elem_id}]`).closest('tr')
                // row.remove()
            }
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