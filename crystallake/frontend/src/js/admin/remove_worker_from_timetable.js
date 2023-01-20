$(document).ready(function (){
    $('.timetable_workers_tbody').on('click', '[data-temp-elem-id]', function (){
        event.preventDefault()
        const worker_id = $(this).attr('data-temp-elem-id')
        // const table = $('#timetable_workers_tbody');
        // const row = table.find(`[data-id=${worker_id}]`).closest('tr')
        // row.remove()
        $(this).closest('tr').remove()
        $('#edit_timetable').trigger('worker_deleted', worker_id)
    })
})