$(document).ready(function (){

    $(document).on('click', '[data-id]', function (){
        const form = $(this).closest('form');
        form.trigger('submit', $(this).attr('data-id'));
    });

    $('[data-additional-form]').on('submit', function (event, elem_id){
        const current_form = $(this);
        event.preventDefault();

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': elem_id, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
                const table = current_form.find('.additional_info_tbody');
                const row = table.find(`[data-id=${elem_id}]`).closest('tr')
                row.remove()
            }
        }).statusCode({
           302: function (data){
                const response = jQuery.parseJSON(data.responseText)
                window.location.href = response['data']
            }
        });

    });

});