$(document).ready(function (){

    $('#select_timetable').on('submit', function (event, data){
        event.preventDefault();

        $('#id_create-time_select_text').val(data.time_str);
        $('#id_edit-time_select_text').val(data.time_str);
        $('#id_create-timetable_id').val(data.id);
        $('#id_edit-timetable_id').val(data.id);

        $('#id_create-day').val(data.day);
        $('#id_edit-day').val(data.day);
        $('#id_create-time_start').val(data.time_start);
        $('#id_edit-time_start').val(data.time_start);
        $('#id_create-time_end').val(data.time_end);
        $('#id_edit-time_end').val(data.time_end);

    });

})