"use strict";

$(document).ready(function(){
    $(window).on("scroll", function () { 

        // считаем дошли ли до конца каталога, не долистывая одного элемента
        if($(document).height() <= $(window).scrollTop() + $(window).height() + $('.footer').height() + $('.card_short').height()){
            // всятавляем три элемента
            for (let i = 0; i < 8; i++){
                // тут будет ajax запрос
                $('.catalog_medium').append($('.card_short').first().clone());
            }
        }
    
    });
});
