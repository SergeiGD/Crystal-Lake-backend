$(document).ready(function(){
    $('.header_burger').on('click', function(){
        $('.header_burger, .header_menu').toggleClass('burger__active');
    });
});