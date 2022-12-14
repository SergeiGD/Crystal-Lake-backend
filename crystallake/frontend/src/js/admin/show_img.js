$(document).ready(function(){

    $('.main_info_container').on('click', '.open_img', function(){
        const modal_id = $(this).attr("data-bs-target");                // берем id попапа
        const img_src = $(this).siblings('img').first().attr('src');    // получаем src каритнки
        $(modal_id + " img").attr('src', img_src);                      // устанавливаем src картинке в попапе
    });

});