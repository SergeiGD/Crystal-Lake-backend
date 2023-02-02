"use strict";

import '../jquery-mobile/jquery.mobile.custom.min.js';

$(document).ready(function(){

    function spawn_dots(){
        $('.slider').each(function(){
            const count = $(this).siblings('.slider_content').length;
            var dot = '<div class="slider_item"></div>';
            for(let i = 0; i < count; i++){
                $(this).append(dot);
            }
            $(this).children('.slider_item').first().addClass('slider_item__active');
        });
    }

    spawn_dots();

    var auto_play_timer;    // таймер для автоматического переключения слайдов

    $('.slider_item').on('click', function(){

        var new_dot = $(this).first();

        if (new_dot.hasClass('slider_item__active')){
            return;
        }

        var old_dot = new_dot.siblings('.slider_item__active');

        swipe_slider(old_dot, new_dot);

    });

    

    $('.slider_content').on("swipeleft", function(){

        if ($(this).siblings('.slider_content').length < 2) return;


        var current_card = $(this).first();

        var slider = current_card.siblings('.slider');


        var current_dot = slider.children('.slider_item__active');
        var current_dot_index = current_dot.index();


        var last_index = slider.children().length - 1;    // получаем крайний индекс слайдера


        if (current_dot_index == last_index){
            var new_dot = slider.children().eq(0);
        }
        else{
            var new_dot = slider.children().eq(++current_dot_index);
        }

        swipe_slider(current_dot, new_dot);
        
    });

    $('.slider_content').on("swiperight", function(){

        if ($(this).siblings('.slider_content').length < 2) return;

        var current_card = $(this).first();

        var slider = current_card.siblings('.slider');


        var current_dot = slider.children('.slider_item__active');
        var current_dot_index = current_dot.index();


        var last_index = slider.children().length - 1;    // получаем крайний индекс слайдера


        if (current_dot_index == 0){
            var new_dot = slider.children().eq(last_index);
        }
        else{
            var new_dot = slider.children().eq(--current_dot_index);
        }

        swipe_slider(current_dot, new_dot);
    });

    function swipe_slider(old_dot, new_dot){


        if (!isSliderRequired($(old_dot).parent())){    // проверяем, не скрыт ли слайдер
            return;
        }

        var all_cards = old_dot.parent().siblings('.slider_content');

        var old_card = all_cards.eq(old_dot.index());
        var new_card = all_cards.eq(new_dot.index());

        old_dot.removeClass("slider_item__active");
        new_dot.addClass('slider_item__active');

        old_card.removeClass('slider_content__active');
        new_card.addClass('slider_content__active');
        new_card.fadeOut(0);                // анимация переключения слайдов
        new_card.fadeIn(300);

        clearTimeout(auto_play_timer);      // сбрасываем таймер на случай, если свайпнули вручную
        swipe_auto();                       // (чтоб не переключался мгновенно)
    }

    function isSliderRequired(slider) {
        if (slider.siblings('.tablet-slider-required').is(':visible') || slider.siblings('.always-slider-required').length > 0){
            return true;    // слайдер нужно листать, если у нас планшет / слайдер всегда показывается на всех экранах
        }

        return false;
    }

    function swipe_auto(){
        auto_play_timer = setInterval(function(){

            $('.slider_content__active').trigger('swipeleft');  // тригерим событие переключения следующего слайда

        }, 5000);
    }

    swipe_auto();

    $('.slider_content').on("dragstart", function(event) { event.preventDefault(); });

});
