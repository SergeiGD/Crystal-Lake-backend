$(document).ready(function (){

    $('#select_service_purchase').on('submit', function (event, data){
        event.preventDefault();

        $('.service_name').html(data.name).attr('href', data.link);
        $('#id_create-service_id').val(data.id);
        $('.service_timetable_link').attr('href', data.link + '#dates')

        $('#search_timetables').attr('service_id', data.id)

    });

})