$(document).ready(function (){
    $(document).on('click', '[data-id]', function (){

        const form = $(this).closest('form');
        form.trigger('submit', {
            'is_dynamic': $(this).attr('data-dynamic'),
            'phone': $(this).attr('data-phone'),
            'name': $(this).attr('data-name'),
            'id': $(this).attr('data-id'),
            'link': $(this).attr('data-link'),
            'time_str': $(this).attr('data-time-str'),
            'time_start': $(this).attr('data-time-start'),
            'time_end': $(this).attr('data-time-end'),
            'day': $(this).attr('data-day')
            }
        );
        // form.trigger('submit', [
        //     $(this).attr('data-id'),
        //     $(this).attr('data-name'),
        //     $(this).attr('data-link'),
        //     {
        //         'is_dynamic': $(this).attr('data-dynamic'),
        //         'phone': $(this).attr('data-phone'),
        //     }
        // ]);
    });
})