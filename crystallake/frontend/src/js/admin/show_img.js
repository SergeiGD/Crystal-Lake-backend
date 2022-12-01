$(document).ready(function(){

    $('.open_img').on('click', function(){
        const modal_id = $(this).attr("data-bs-target");
        const img_src = $(this).siblings('img').first().attr('src');
        $(modal_id + " img").attr('src', img_src);
        console.log($('#asdqwe').attr('data-asd'))
    });


});