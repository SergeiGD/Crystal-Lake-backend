$(document).ready(function (){

    $('#select_worker').on('submit', function (event, data){
        event.preventDefault();

        const same_elem = $('#timetable_workers_tbody').find(`[data-id="${data.id}"]`).length

        if(same_elem){
            return
        }

        const row = `
                <tr>
                    <th scope="row">${data.id}</th>
                    <td>
                        <a href="${data.link}" class="link-hover d-block">${data.name}</a>
                    </td>
                    <td>${data.phone}</td>
                    <td class="p-0 position-relative w-10r">
                        <button class="btn btn-danger w-100 rounded-0 h-100 position-absolute" type="button" data-temp-elem-id="${data.id}">Убрать</button>
                    </td>
                </tr>
            `
        $('#timetable_workers_tbody').append(row);

        $('#edit_timetable').trigger('worker_added', data.id)

    });

})