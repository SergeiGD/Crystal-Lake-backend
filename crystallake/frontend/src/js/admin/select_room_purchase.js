$(document).ready(function (){

    $('#select_room_purchase').on('submit', function (event, data){
        event.preventDefault();

        $('.purchase_name').html(data.name).attr('href', data.link);
        $('#id_create-room_id').val(data.id);
        $('.room_timetable_link').attr('href', data.link + '#dates')

    });

})