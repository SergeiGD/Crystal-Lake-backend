$( function() {
    $("#login_open, #login_open__footer").on("click", function(){
        $("#login_modal").toggleClass("modal_wrapper__active");
        $("#login_popup").toggleClass("login_popup__active");
        $('.header_burger, .header_menu').removeClass('burger__active');    // скрываем бургер, чтоб не загораживал
    });

    $("#login_close, #signup_close, #login_modal").on("click", function(){
        const login_popup = $('#login_popup');
        const modal = login_popup.parent();
        login_popup.removeClass("login_popup__active");     // скрываем само окно авторизации / регистарции
        modal.removeClass("modal_wrapper__active");         // скрываем модальную область
    });

    $("#login_popup, #signup_popup").on("click", function(e) {
        e.stopPropagation();         // останавливаем, чтоб не зыкрывалось окно, как при клике за областью попапа  
    });

    $(document).on("keyup", function(e) {
        if (e.key === "Escape") { 
            $('#login_close').trigger('click');     // закрытие на эскейп
        }
    });

    $("#end_login_button").on("click", function(){
        window.location.href = "profile_active.html";
    });
    
    $("#goto_singup, #goto_login").on("click", function(){
        $("#login_popup, #signup_popup").toggleClass("login_popup__active");
    });

  });