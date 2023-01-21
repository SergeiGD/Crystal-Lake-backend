const form_date = require("./form_date");
const add_hours = require("./add_hours");

$(document).ready(function (){

    $('#edit_service_purchase_modal').on('popup_open', function (event, data){
        $('#edit_service_purchase').attr('action', data.edit_url)
        console.log(data)
        // $('#id_purchase_id').val(data.id)
        $('.service_name').html(data.offer.name).attr('href', data.offer.link)
        $('#id_edit-quantity').val(data.quantity)
        // $('#id_is_paid').prop('checked', data.is_paid);
        // $('#id_is_prepayment_paid').prop('checked', data.is_prepayment_paid);
        // $('#id_service_id').val(data.offer.id);

        $('#search_timetables').attr('service_id', data.offer.id)

        const start = new Date(data.start * 1000)
        const local_start = add_hours.add_hours(start, start.getTimezoneOffset() / 60 * -1)
        const end = new Date(data.end * 1000)
        const local_end = add_hours.add_hours(end, end.getTimezoneOffset() / 60 * -1)

        const day = local_start.toISOString().substring(0,10),
            start_time = local_start.toISOString().substring(11,16),
            end_time = local_end.toISOString().substring(11,16)

        $('#id_edit-day').val(day)
        $('#id_edit-time_start').val(start_time)
        $('#id_edit-time_end').val(end_time)

    })
})