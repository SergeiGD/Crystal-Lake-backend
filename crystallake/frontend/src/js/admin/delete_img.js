$(document).ready(function() {
    $('#edit_main_info_form').on('click', '.delete_img', function () {
        const container = $(this).closest('[data-order]');

        container.nextAll('[data-order]').each(function () {
            const new_order = $(this).find('input[id$=order]').attr('value') - 1;   // изменяем порядоковые номера последующих картинок
            $(this).find('input[id$=order]').attr('value', new_order);
            $(this).attr('data-order', new_order)
        });


        const id = container.find('input[id$=id]').attr('value')
        const form_name = container.find('input[id$=id]').attr('name').slice(0, -2)

        $('#edit_main_info_form').trigger('file_deleted', {[form_name + 'id']: id, [form_name + 'DELETE ']: 'on'}); // отправляем форму на удаление и id картинки

        container.addClass('d-none')            // скрываем картинку и помечаем как не активную
        container.removeAttr('data-active')

        $('#accordion_body_images').trigger('refresh_required');    // обновляем стелки


    });
});
