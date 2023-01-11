$(document).ready(function (){

    $('#select_room_purchase').on('submit', function (event, data){
        event.preventDefault();

        $('#room_purchase').html(data.name).attr('href', data.link);
        $('#id_room_id').val(data.id);

    });

})