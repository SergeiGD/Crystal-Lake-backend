$(document).ready(function (){

    $('#select_worker').on('submit', function (event, worker_id, worker_name, worker_link, additional_data){
        event.preventDefault();

        const same_elem = $('#timetable_workers_tbody').find(`[data-id="${worker_id}"]`).length

        if(same_elem){
            return
        }

        const row = `
                <tr>
                    <th scope="row">${worker_id}</th>
                    <td>
                        <a href="${worker_link}" class="link-hover d-block">${worker_name}</a>
                    </td>
                    <td>${additional_data.phone}</td>
                    <td class="p-0 position-relative w-10r">
                        <button class="btn btn-danger w-100 rounded-0 h-100 position-absolute" type="button" data-temp-elem-id="${worker_id}">Убрать</button>
                    </td>
                </tr>
            `
        $('#timetable_workers_tbody').append(row);

        $('#edit_timetable').trigger('worker_added', worker_id)

    });

})