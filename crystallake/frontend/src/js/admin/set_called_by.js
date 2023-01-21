$(document).ready(function (){
    $('[data-set-called-by]').on('click', function (){
        console.log($(this).attr('data-set-called-by'))
        console.log($('[data-called-by]'))
        $('[data-called-by]').attr('data-called-by', $(this).attr('data-set-called-by'))
    })
})