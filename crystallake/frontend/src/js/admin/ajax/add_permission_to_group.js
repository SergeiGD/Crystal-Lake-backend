$(document).ready(function (){

    $('#select_permission').on('submit', function (event, service_id){
        event.preventDefault();

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': service_id, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
                const new_permissions = {name: response['data'].name, id: response['data'].id}
                append_row(new_permissions)
            }
        });

        function append_row(permission){
            const row = `
                <tr>
                    <th scope="row">${permission.id}</th>
                    <td>${permission.name}</td>
                    <td class="p-0 position-relative w-10r">
                        <button class="btn btn-danger w-100 rounded-0 h-100 position-absolute" type="button" data-id="${permission.id}">Убрать</button>
                    </td>
                </tr>
            `
            $('#permissions_list_body').append(row);

        }

    });
})