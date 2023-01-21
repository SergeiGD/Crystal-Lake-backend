$(document).ready(function (){
    $(document).on('click', '[data-id]', function (){

        const form = $(this).closest('form');
        form.trigger('submit', {
            'phone': $(this).attr('data-phone'),
            'name': $(this).attr('data-name'),
            'id': $(this).attr('data-id'),
            'link': $(this).attr('data-link'),
            'time_str': $(this).attr('data-time-str'),
            'time_start': $(this).attr('data-time-start'),
            'time_end': $(this).attr('data-time-end'),
            'day': $(this).attr('data-day'),
            'url': $(this).attr('data-url'),
            }
        );
    });
})