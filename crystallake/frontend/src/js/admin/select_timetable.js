$(document).ready(function (){

    $('#select_timetable').on('submit', function (event, data){
        event.preventDefault();

        $('#id_time_select_text').val(data.time_str);

        $('#id_day').val(data.day);
        $('#id_time_start').val(data.time_start);
        $('#id_time_end').val(data.time_end);

    });

})