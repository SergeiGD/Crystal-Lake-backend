const find_items = require("../find_items");
$(document).ready(function (){

    $('.ajax_search').on('submit', function (event, page='1'){
        event.preventDefault();

        const form = $(this);

        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $(`[data-find-form="#${form.attr('id')}"]`).find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)
        post_data.append('popup_to_open', $(this).attr('data-popup-to-open'))

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                console.log($(`tbody[data-find-form="#${form.attr('id')}"]`))
                $(`tbody[data-find-form="#${form.attr('id')}"]`).html(response['data']['items'])
                find_items.build_pages(response['data']['pages'], $(`.pagination[data-find-form="#${form.attr('id')}"]`))
            },
        });

    });

})