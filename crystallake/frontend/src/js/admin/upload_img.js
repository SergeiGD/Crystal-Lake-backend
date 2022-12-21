$(document).ready(function(){
    $('#edit_main_info_form').on('click', '.upload_img_button', function(){
        $(this).siblings('.upload_img_input').trigger('click');     // при клике вызываем скрытый загрузчик файлов
    });

    $('#accordion_body_images').on('click', '.upload_new_img_button', function(){
        $('#id_form-__prefix__-path').trigger('click');             // при клике вызываем скрытый загрузчик файлов
    });

    $('#edit_main_info_form').on('change', '.upload_img_input', function(){
        const file = $(this).get(0).files[0];                          // получаем загруженный файй
        const input = $(this);

        var is_new_img = false;                                         // флаг, загружаем мы новую картинки или редактируем существующую

        if ($(this).closest('[data-empty-container]').length) is_new_img = true;    // если для пустого 'контейнера', то новая

        if(file){
            const img_elem = $(this).siblings('img');
            const reader = new FileReader();

            reader.onloadend = function(){
                const img_src = reader.result;                            // получаем base64 картинки

                // ВОТ ТУТ ЗАПРОС НА ПОЛУЧЕНИЕК

                img_elem.attr('src', img_src);                          // устанавливаем img новый src

                if (is_new_img) register_new_img();                     // если новая, то также обновляем все необходимые инпуты

                const input_name = input.attr('name');

                $('#edit_main_info_form').trigger('file_uploaded', {[input_name]: file});   // выгружаем имя и картинку, для POST ajax запроса
            }

            reader.readAsDataURL(file);
        }
    });

    function register_new_img(){
        const container = $('[data-empty-container]')
        const order = $('[data-active][data-order]').length + 1;                 // получаем порядковый номер, который будет у картинки

        container.find('input[id$=order]').attr('value', order)     // устанавливаем порядковый номер
        container.attr('data-order', order)
        container.removeAttr('data-empty-container')                //  убираем признак 'пустого конрейнера (заготовки)'
        container.attr('data-active', '')

        //$('#id_form-TOTAL_FORMS').attr('value', order)              // обновляем общее кол-во форм у формсета

        const old_total_forms = $('#id_form-TOTAL_FORMS').attr('value')
        $('#id_form-TOTAL_FORMS').attr('value', parseInt(old_total_forms) + 1)

        container.removeClass('d-none')                             // отображаем елемент

        const regex = RegExp('__prefix__', 'g')

        container.find('input').each(function (index, element){
            const new_id = $(this).attr('id').replace(regex, order - 1)             // заменяем id и имя пустой формы на нужный
            const new_name = $(this).attr('name').replace(regex, order - 1)
            $(this).attr('id', new_id)
            $(this).attr('name', new_name)
        });

        const new_container = create_container()                        // создаем новый пустой конейтер
        container.after(new_container);

        $('#accordion_body_images').trigger('refresh_required');
    }

    function create_container(){
        return  `
            <div class="col-lg-4 col-sm-6 col-12 mb-4 d-none" data-empty-container>
                <div class="w-100">
                    <div class="img_wrapper">

                        <img src="" alt="Доп. фото" class="img-fluid w-100 img rounded">

                        <button class="btn open_img btn-dark" type="button" data-bs-toggle="modal" data-bs-target="#show_img_modal">
                            <i class="fa-solid fa-up-right-and-down-left-from-center"></i>
                        </button>

                        <button class="btn btn-primary update_img w-10r upload_img_button" type="button">
                            <i class="fa-solid fa-arrow-up-from-bracket"></i>
                            Обновить
                        </button>

                        <button class="btn btn-danger delete_img w-10r" type="button">
                            <i class="fa-solid fa-xmark"></i>
                            Удалить
                        </button>

                        <input type="number" name="form-__prefix__-order" class="d-none" id="id_form-__prefix__-order">
                        <input type="file" name="form-__prefix__-path" class="upload_img_input d-none" accept="image/png, image/jpeg" id="id_form-__prefix__-path">
                        <input type="hidden" name="form-__prefix__-id" id="id_form-__prefix__-id">

                    </div>
                </div>

                <div class="mt-2 text-center">
                    <i class="fa-solid fa-arrow-left fs-2 move_prev" role="button"></i>
                    <i class="fa-solid fa-arrow-right fs-2 ms-5 move_next" role="button"></i>
                </div>

            </div>
        `
    }

})