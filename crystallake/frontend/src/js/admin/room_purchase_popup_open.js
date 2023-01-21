const add_hours = require('./add_hours');
$(document).ready(function (){

    $('#edit_room_purchase_modal').on('popup_open', function (event, data){

        $('#edit_room_purchase').attr('action', data.edit_url)
        $('.room_name').html(data.offer.name).attr('href', data.offer.link)
        $('.room_timetable_link').attr('href', data.offer.link + '#dates')
        const start = new Date(data.start * 1000)
        const local_start = add_hours.add_hours(start, start.getTimezoneOffset() / 60 * -1)
        $('#id_edit-start').val(local_start.toISOString().split('T')[0])
        const end = new Date(data.end * 1000)
        const local_end = add_hours.add_hours(end, end.getTimezoneOffset() / 60 * -1)
        $('#id_edit-end').val(local_end.toISOString().split('T')[0])
        // $('#id_is_paid').prop('checked', data.is_paid);
        // $('#id_is_prepayment_paid').prop('checked', data.is_prepayment_paid);
    })
})