$(document).ready(function(){
    $('.move_next').on('click', function(){
        const current_item = $(this).closest('[data-order]');
        const number = current_item.attr('data-order');

        if (number == $(current_item).siblings('[data-order]').length + 1) return;

        const next_item = current_item.next();

        current_item.insertAfter(next_item);
        current_item.attr('data-order', Number(number) + 1);
        next_item.attr('data-order', Number(number));

        $('.move_prev, .move_next').removeClass('opacity-50');

        const first_elem = current_item.parent(':first-child');
        const last_elem = current_item.parent(':last-child');

        first_elem.find('.move_prev').first().addClass('opacity-50');
        last_elem.find('.move_next').last().addClass('opacity-50');
    });

    $('.move_prev').on('click', function(){
        const current_item = $(this).closest('[data-order]');
        const number = current_item.attr('data-order');

        if (number == 1) return;

        const prev_item = current_item.prev();

        current_item.insertBefore(prev_item);
        current_item.attr('data-order', Number(number) - 1);
        prev_item.attr('data-order', Number(number));

        $('.move_prev, .move_next').removeClass('opacity-50');

        const first_elem = current_item.parent(':first-child');
        const last_elem = current_item.parent(':last-child');

        first_elem.find('.move_prev').first().addClass('opacity-50');
        last_elem.find('.move_next').last().addClass('opacity-50');
    });
});