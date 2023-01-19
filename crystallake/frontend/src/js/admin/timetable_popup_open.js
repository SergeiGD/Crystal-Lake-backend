const add_hours = require('./add_hours');
$(document).ready(function (){

    $('#manage_timetable_modal').on('popup_open', function (event, data){
        console.log(data)

        $('#id_timetable_id').val(data.id)
        const start = new Date(data.start * 1000)
        const local_start = add_hours.add_hours(start, start.getTimezoneOffset() / 60 * -1)
        const end = new Date(data.end * 1000)
        const local_end = add_hours.add_hours(end, end.getTimezoneOffset() / 60 * -1)
        $('#id_date').val(local_start.toISOString().substring(0,10))
        $('#id_start').val(local_start.toISOString().substring(11,16))
        $('#id_end').val(local_end.toISOString().substring(11,16))
        $('#timetable_workers_tbody').html('')

        for (const worker of data.workers){
            const row = `
                <tr>
                    <th scope="row">${worker.id}</th>
                    <td>
                        <a href="${worker.link}" class="link-hover d-block">${worker.name}</a>
                    </td>
                    <td>${worker.phone}</td>
                    <td class="p-0 position-relative w-10r">
                        <button class="btn btn-danger w-100 rounded-0 h-100 position-absolute" type="button" data-temp-elem-id="${worker.id}">Убрать</button>
                    </td>
                </tr>
            `
            $('#timetable_workers_tbody').append(row);
        }

    })
})