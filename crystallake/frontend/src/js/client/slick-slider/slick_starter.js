require('./slick');

$(document).ready(function(){
    $('.slick_slider').slick({
        arrows: false,
        dots: true,
        slidesToShow: 1,
        infinite: false,
        autoplay: false,
        variableWidth: true,
    });

    $('.photos_img').on("click", function(){
        const slider_number = $(this).attr("data-number");
        console.log(slider_number);
        $("#images_modal").addClass("modal_wrapper__active");
        $('.slick_slider').slick('slickGoTo', slider_number, true);        // открываем именну ту картинку, на которую нажали
    });

    $('#images_modal, #images_close').on("click", function(){
        $("#images_modal").removeClass("modal_wrapper__active");
    });

    $(document).on("keyup", function(e) {
        if (e.key === "Escape") { 
            $('#images_modal').trigger('click');
        }
    });

    $(".slick_slider").on("click", function(e) {
        e.stopPropagation();
    });
});