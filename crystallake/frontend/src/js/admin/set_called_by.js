$(document).ready(function (){
    $(document).on('click', '[data-set-called-by]', function (){
        $('.changeable_popup').attr('data-popup-to-open', $(this).attr('data-set-called-by'))
    })
})