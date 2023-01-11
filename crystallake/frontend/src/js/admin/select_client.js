$(document).ready(function (){

    $('#select_client').on('submit', function (event, data){
        event.preventDefault();

        $('#id_client_name').val(data.name);
        $('#id_client_id').val(data.id);

    });

})