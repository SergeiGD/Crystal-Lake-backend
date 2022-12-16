$(document).ready(function (){
    // при загрузке фотографии к новому предложению, скрываем изначальную кнопку и отображаем картику
    $('#img_wrapper__temp > .upload_img_input').on('change', function (){
        $(this).siblings('.img').removeClass('d-none')                      // отображаем картинки
        $('#upload_button__temp').addClass('d-none')                        // скрываем кнопку
        $('#img_wrapper__temp').addClass('img_wrapper').removeAttr('id')    // удаляем id
    });
});