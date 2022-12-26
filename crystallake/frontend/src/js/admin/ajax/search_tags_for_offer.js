$(document).ready(function (){

    $('#open_tag_modal').on('click', function (){
        $('#find_tags_btn').trigger('click');
    })

    $('#find_tags_btn').on('click', function (){
        $('#search_tag').trigger('submit');
    })

    $('#tags_pagination').on('click', '[data-page]', function (){
        $('#search_tag').trigger('submit', $(this).attr('data-page'));
    })

    $('#clean_tags_btn').on('click', function (){
        const form = $('#search_tag')
        form.find('input').not('[name=csrfmiddlewaretoken]').val('')
        form.trigger('submit')
    })

    $('#add_tag_modal').on('click', '[data-sortby]', function (){
        var picked_sortby = $(this).attr('data-sortby');
        const icon = $(this).find('i');
        const active_sortby_elem = $('[data-sortby-active]');
        const active_sortby = active_sortby_elem.attr('data-sortby');


        if (picked_sortby === active_sortby){
            if (picked_sortby[0] === '-'){
                picked_sortby = picked_sortby.replace('-', '');
                icon.removeClass('fa-arrow-down-wide-short');
                icon.addClass('fa-arrow-down-short-wide');
            }
            else{
                picked_sortby = '-' + picked_sortby;
                icon.removeClass('fa-arrow-down-short-wide');
                icon.addClass('fa-arrow-down-wide-short');
            }
        }
        else{
            $(this).attr('data-sortby-active', '');
            active_sortby_elem.removeAttr('data-sortby-active');
            $(this).addClass('bg-c_yellow-700');
            active_sortby_elem.removeClass('bg-c_yellow-700');

        }

        $(this).attr('data-sortby', picked_sortby);
        $('#search_tag').trigger('submit');
    })

    $('#search_tag').on('submit', function (event, page='1'){
        event.preventDefault();

        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $('#add_tag_modal').find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)

        console.log(post_data)

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                build_rows(response['data']['tags'])
                build_pages(response['data']['pages'])
            },
        });

        function build_rows(data){
            var result = ''
            for(const item of data){
                const row = `
                    <tr>
                        <th scope="row">${item.id}</th>
                        <td>${item.name}</td>
                        <td class="p-0 position-relative w-10r">
                            <button data-id="${item.id}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" data-bs-dismiss="modal" type="button">
                                Выбрать
                            </button>
                        </td>
                    </tr>
                `
                result += row
            }
            $('#tags_add_body').html(result);
        }

        function build_pages(data){

            var result = ''

            if (data.current_page > 1){
                result += `
                    <li class="page-item">
                        <button class="page-link" type="button" data-page="${data.current_page - 1}" aria-label="Previous">
                            <span aria-hidden="true">&laquo;</span>
                        </button>
                    </li>
                `
            }

            if (data.current_page - 3 > 1){
                result += `
                    <li class="page-item">
                        <button class="page-link" type="button" data-page="1">1</button>
                    </li>
                    <li class="page-item">
                        <p class="page-link">&hellip;</p>
                    </li>
                `
            }

            for (var i = 1; i <= data.pages_count; i++){
                if (i == data.current_page){
                    result += `
                        <li class="page-item"><p class="page-link bg-c_yellow-700 text-black">${i}</p></li>
                    `
                }
                else if (i > data.current_page - 4 && i < data.current_page + 4){
                    result += `
                        <li class="page-item"><button class="page-link" type="button" data-page="${i}">${i}</button></li>
                    `
                }
            }

            if (data.current_page + 3 < data.pages_count){
                result += `
                    <li class="page-item">
                        <p class="page-link">&hellip;</p>
                    </li>
                    <li class="page-item">
                        <button class="page-link" type="button" data-page="${data.pages_count}">${data.pages_count}</button>
                    </li>
                `
            }

            if (data.current_page < data.pages_count){
                result += `
                    <li class="page-item">
                        <button class="page-link" type="button" data-page="${data.current_page + 1}" aria-label="Next">
                            <span aria-hidden="true">&raquo;</span>
                        </button>
                    </li>
                `
            }

            $('#tags_pagination').html(result);

        }
    });

})