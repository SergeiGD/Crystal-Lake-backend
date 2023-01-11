$(document).ready(function (){

    $('#select_service_purchase').on('submit', function (event, data){
        event.preventDefault();

        $('#service_purchase').html(data.name).attr('href', data.link);
        $('#id_service_id').val(data.id);

        const is_dynamic = (data.is_dynamic === 'true');

        if (is_dynamic){
            $('.static_time_field').addClass('d-block')
            $('.dynamic_time_field').addClass('d-none')
        }
        else{
            $('.dynamic_time_field').addClass('d-block')
            $('.static_time_field').addClass('d-none')
        }

    });

})