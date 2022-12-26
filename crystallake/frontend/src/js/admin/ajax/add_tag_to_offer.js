$(document).ready(function (){
    $('#tags_add_body').on('click', '[data-id]', function (){
        $('#select_tag').trigger('submit', $(this).attr('data-id'));
    });

    $('#select_tag').on('submit', function (event, tag_id){
        event.preventDefault();

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'tag_id': tag_id, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
                const new_tag = {name: response['data'].name, id: response['data'].id, link: response['data'].link}
                append_row(new_tag)
            }
        });

        function append_row(tag){
            const row = `
                <tr>
                    <th scope="row">${tag.id}</th>
                    <td>
                        <a href="${tag.link}" class="link-hover d-block">${tag.name}</a>
                    </td>
                    <td class="p-0 position-relative w-10r">
                        <button class="btn btn-danger w-100 rounded-0 h-100 position-absolute" type="button" data-id="${tag.id}">Убрать</button>
                    </td>
                </tr>
            `
            $('#tags_list_body').append(row);

        }

    });
})