$(document).ready(function (){
    $('#tags_list_body').on('click', '[data-id]', function (){
        $('#offer_tags').trigger('submit', $(this).attr('data-id'));
    });

    $('#offer_tags').on('submit', function (event, tag_id){
        event.preventDefault();

        //const csrf_token =  $('[name=csrfmiddlewaretoken]').attr('value')
        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')


        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'tag_id': tag_id, 'csrfmiddlewaretoken': csrf_token},
            success: function (data){
                const table = $('#tags_list_body');
                const row = table.find(`[data-id=${tag_id}]`).closest('tr')
                row.remove()
            }
        });

    });
});