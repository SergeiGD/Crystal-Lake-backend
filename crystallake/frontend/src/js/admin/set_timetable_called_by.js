$(document).ready(function (){
    $('.manage_timetable_btn').on('click', function (){
        console.log($('#select_worker').attr('data-called-by', $(this).attr('data-bs-target')))
        $('#select_worker').attr('data-called-by', $(this).attr('data-bs-target'))
    })
})