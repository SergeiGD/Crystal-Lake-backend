$(document).ready(function(){
    $('.profile_burger').on('click', function(){
        $('.profile_menu').css('opacity', '0');

        $('.profile_burger, .profile_menu').toggleClass('profile_burger__active');
        
        $('.profile_menu').animate({
            opacity: 1
        }, 300);
    });
});