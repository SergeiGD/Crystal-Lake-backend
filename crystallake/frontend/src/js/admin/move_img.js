$(document).ready(function(){
    function update_arrows(){
        $('.move_prev, .move_next').removeClass('opacity-50');

        const first_elem =$('#accordion_body_images').children('[data-active][data-order]:first');
        const last_elem = $('#accordion_body_images').children('[data-active][data-order]:last');

        first_elem.find('.move_prev').first().addClass('opacity-50');       // обновляем стрелки
        last_elem.find('.move_next').last().addClass('opacity-50');
    }

    update_arrows();

    $('#accordion_body_images').on('click', '.move_next', function(){
        const current_item = $(this).closest('[data-order]');
        const number = current_item.attr('data-order');

        if (number == $(current_item).siblings('[data-order]').length + 1) return;      // элемент является крайним, если число его братьев == его номеру + 1

        const next_item = current_item.next();

        current_item.insertAfter(next_item);
        current_item.attr('data-order', Number(number) + 1);
        next_item.attr('data-order', Number(number));                               // обновялем атрибуты, в которых содержится порядковый номер

        const current_order_input = current_item.find('input[id$=order]');
        current_order_input.attr('value', Number(number) + 1)                       // обновялем инпуты, в которых содержится порядковый номер
        const next_order_input = next_item.find('input[id$=order]');
        next_order_input.attr('value', Number(number))

        update_arrows();                                                            // обновляем стрелки
    });

    $('#accordion_body_images').on('click', '.move_prev', function(){
        const current_item = $(this).closest('[data-order]');
        const number = current_item.attr('data-order');

        if (number == 1) return;                                                    // элемент первый, если его номер равен 1 (нулевой - главная картинки объекта offer)

        const prev_item = current_item.prev();

        current_item.insertBefore(prev_item);

        current_item.attr('data-order', Number(number) - 1);
        prev_item.attr('data-order', Number(number));

        const current_order_input = current_item.find('input[id$=order]');
        current_order_input.attr('value', Number(number) - 1)
        const prev_order_input = prev_item.find('input[id$=order]');
        prev_order_input.attr('value', Number(number))

        update_arrows();
    });

    $('#accordion_body_images').on('refresh_required', function(){
        update_arrows();
    });


});