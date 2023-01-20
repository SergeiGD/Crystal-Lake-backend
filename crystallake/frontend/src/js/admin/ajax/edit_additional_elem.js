$(document).ready(function (){
    $('.edit_additional_form').on('submit', function (event, elem_id) {
        event.preventDefault();
        const popup = $(this).find('[data-popup]').attr('data-popup')
        //const  popup = $(this).attr('data-popup')

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': elem_id, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
                $(popup).trigger('popup_open', response.data)
            }
        }).statusCode({
           302: function (data){
                const response = jQuery.parseJSON(data.responseText)
                window.location.href = response['data']
            }
        });

    })

})