"use strict";

$(document).ready(function(){
    $('.time').on("click", function(){

        if ($(this).hasClass("time__active")){
            return;
        }

        $(".time__active").removeClass("time__active");
        $(this).addClass("time__active");
    });
});