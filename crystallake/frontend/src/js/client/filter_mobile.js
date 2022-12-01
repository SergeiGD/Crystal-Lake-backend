$(document).ready(function(){
    $('.mobile_filter').on('click', function(){
        $('.filter').css('opacity', '0');

        $('.filter').toggleClass('filter__active');

        $('.filter').animate({
            opacity: 1
        }, 300);
    });
    
});