$(document).ready(function (){

    $('#room_purchase_modal').on('popup_open', function (event, data){

        $('#id_purchase_id').val(data.id)
        $('#room_purchase').html(data.name).attr('href', data.link)
        const start = new Date(data.start * 1000)
        $('#id_start').val(start.toISOString().split('T')[0])
        const end = new Date(data.end * 1000)
        $('#id_end').val(end.toISOString().split('T')[0])
        $('#id_is_paid').prop('checked', data.is_paid);
        $('#id_is_prepayment_paid').prop('checked', data.is_prepayment_paid);
    })
})