$(document).ready(function (){
    $('[data-set-called-by]').on('click', function (){
        $('.changeable_popup').attr('data-popup-to-open', $(this).attr('data-set-called-by'))
    })
})