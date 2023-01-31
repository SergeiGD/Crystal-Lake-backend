$( function() {
    $("#login_open, #login_open__footer").on("click", function(){
        $("#login_modal").toggleClass("modal_wrapper__active");
        $('.header_burger, .header_menu').removeClass('burger__active');    // скрываем бургер, чтоб не загораживал
    });

    $("#login_close, #signup_close, #login_modal").on("click", function(){
        const login_popup = $('#login_popup');
        const modal = login_popup.parent();
        modal.removeClass("modal_wrapper__active");         // скрываем модальную область
    });

    $("#login_popup, #signup_popup").on("click", function(e) {
        e.stopPropagation();         // останавливаем, чтоб не зыкрывалось окно, как при клике за областью попапа  
    });

    $("#reset_password_btn").on("click", function (){
        $("#client_login_form").addClass("hidden_auth_form")
        $('#client_reset_phone_form').removeClass('hidden_auth_form')
    })

    $("#back_to_login_btn").on('click', function (){
        $('#client_reset_phone_form').addClass('hidden_auth_form')
        $('#client_login_form').removeClass('hidden_auth_form')
    })

    $("#back_to_reset_phone_btn").on('click', function (){
        $('#client_reset_form').addClass('hidden_auth_form')
        $('#client_reset_phone_form').removeClass('hidden_auth_form')
    })

    $("#back_to_register_btn").on('click', function (){
        $('#client_register_code_from').addClass('hidden_auth_form')
        $('#client_register_from').removeClass('hidden_auth_form')
    })

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