const find_items = require("../find_items");
const form_date = require("../form_date");

$(document).ready(function (){

    $('#search_timetables').on('submit', function (event, page='1'){
        event.preventDefault();


        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $('#pick_timetable_modal').find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)
        post_data.append('service_id', $(this).attr('service_id'))

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                build_rows(response['data']['items'])
                find_items.build_pages(response['data']['pages'], $('#timetables_pagination'))
            },
        });

        function build_rows(data){
            const called_by = $('#search_timetables').attr('data-called-by')
            console.log(called_by)
            var result = ''
            for(const item of data){
                const start = new Date(item.start * 1000)   // на 1000, т.к. получаем в секундах, а джесу нужно в мс
                const end = new Date(item.end * 1000)
                const formated_start = form_date.form_date(start)
                const formated_end = form_date.form_date(end)
                const day = start.toISOString().substring(0,10)
                const start_time = start.toISOString().substring(11,16)
                const end_time = end.toISOString().substring(11,16)
                const row = `
                    <tr>
                        <td scope="row">${formated_start}</td>
                        <td scope="row">${formated_end}</td>
                        <td class="p-0 position-relative w-10r">
                            <button data-day="${day}" data-time-start="${start_time}" data-time-end="${end_time}" data-time-str="${formated_start} - ${formated_end}" data-id="${item.id}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" data-bs-toggle="modal"  data-bs-target="${called_by}" type="button">
                                Выбрать
                            </button>
                        </td>
                    </tr>
                `
                result += row
            }
            $('#timetables_tbody').html(result);
        }

    });

})