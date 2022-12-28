$(document).ready(function (){

    $('#add_same_room').on('submit', function (event, room_id){
        event.preventDefault();

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': room_id, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
                const new_room = {id: response['data'].id}
                append_row(new_room)
            }
        });

        function append_row(room){
            const row = `
                <tr>
                    <th scope="row">${room.id}</th>
                    <td class="p-0 position-relative w-10r">
                        <button class="btn btn-danger w-100 rounded-0 h-100 position-absolute" type="button" data-id="${room.id}">Убрать</button>
                    </td>
                </tr>
            `
            $('#same_rooms_list_body').append(row);

        }

    });
})