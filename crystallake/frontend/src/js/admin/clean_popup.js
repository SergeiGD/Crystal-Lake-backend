$(document).ready(function (){
    $('[data-popup-to-clean]').on('click', function (){
        const popup = $(this).attr('data-popup-to-clean')
        $(popup).find('input').not('[name="csrfmiddlewaretoken"]').val('').prop('checked', false)
        $(popup).find('tbody').html('')
    })
})