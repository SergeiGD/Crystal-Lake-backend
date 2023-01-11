const form_date = require("./form_date");

$(document).ready(function (){

    $('#service_purchase_modal').on('popup_open', function (event, data){

        $('#id_purchase_id').val(data.id)
        $('#service_purchase').html(data.name).attr('href', data.link)
        $('#id_quantity').val(data.quantity)
        $('#id_is_paid').prop('checked', data.is_paid);
        $('#id_is_prepayment_paid').prop('checked', data.is_prepayment_paid);
        $('#id_service_id').val(data.offer_id);

        const start = new Date(data.start * 1000)
        const end = new Date(data.end * 1000)

        const day = start.toISOString().substring(0,10),
            start_time = start.toISOString().substring(11,16),
            end_time = end.toISOString().substring(11,16)

        $('#id_day').val(day)
        $('#id_time_start').val(start_time)
        $('#id_time_end').val(end_time)
        if (data.is_dynamic){
            $('.static_time_field').addClass('d-block')
            $('.dynamic_time_field').addClass('d-none')
        }
        else{
            $('#id_time_select_text').val(`${form_date.form_date(start)} - ${form_date.form_date(end)}`)

            $('.dynamic_time_field').addClass('d-block')
            $('.static_time_field').addClass('d-none')
        }

        // const start = new Date(data.start * 1000)
        // $('#id_start').val(start.toISOString().split('T')[0])
        // const end = new Date(data.end * 1000)
        // $('#id_end').val(end.toISOString().split('T')[0])
        // $('#id_is_paid').prop('checked', data.is_paid);
        // $('#id_is_prepayment_paid').prop('checked', data.is_prepayment_paid);
    })
})