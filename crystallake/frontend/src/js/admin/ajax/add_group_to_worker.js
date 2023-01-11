$(document).ready(function (){

    $('#select_group').on('submit', function (event, group_id){
        event.preventDefault();

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': group_id, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
                window.location.reload();
                // const new_group = {name: response['data'].name, id: response['data'].id, link: response['data'].link}
                // append_row(new_group)
            }
        });

        function append_row(group){
            const row = `
                <tr>
                    <th scope="row">${group.id}</th>
                    <td>
                        <a href="${group.link}" class="link-hover d-block">${group.name}</a>
                    </td>
                    
                    <td class="p-0 position-relative w-10r">
                        <button class="btn btn-danger w-100 rounded-0 h-100 position-absolute" type="button" data-id="${group.id}">Убрать</button>
                    </td>
                </tr>
            `
            $('#groups_list_body').append(row);

        }

    });
})