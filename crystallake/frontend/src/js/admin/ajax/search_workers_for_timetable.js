const find_items = require("../find_items");
$(document).ready(function (){

    $('#search_worker').on('submit', function (event, page='1', called_by){
        event.preventDefault();

        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $('#pick_worker_modal').find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                build_rows(response['data']['items'])
                find_items.build_pages(response['data']['pages'], $('#workers_pagination'))
            },
        });

        function build_rows(data){
            var result = ''
            for(const item of data){
                const row = `
                    <tr>
                        <th scope="row">${item.id}</th>
                        <td>
                            <a class="link-hover" href="${item.link}">${item.name}</a>   
                        </td>
                        <td>
                            ${item.phone}
                        </td>
                        <td class="p-0 position-relative w-10r">
                            <button data-id="${item.id}" data-name="${item.name}" data-link="${item.link}" data-phone="${item.phone}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" type="button" data-bs-toggle="modal" data-bs-target="#manage_timetable_modal">
                                Выбрать
                            </button>
                        </td>
                    </tr>
                `
                result += row
            }
            $('#workers_tbody').html(result);
        }

    });

})