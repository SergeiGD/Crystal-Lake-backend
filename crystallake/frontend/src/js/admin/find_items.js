$(document).ready(function (){

    $('.open_search_btn').on('click', function (){
        const find_form_id = $(this).attr('data-form');
        $(find_form_id).trigger('submit');
    })

    $('.find_btn').on('click', function (){
        $(this).closest('.find_form').trigger('submit')
    })


    $('.pagination').on('click', '[data-page]', function (){
        const page = $(this).attr('data-page')
        const form = $(this).closest('.pagination').parent().siblings('.find_form');
        $('.page_input').val(page)
        form.trigger('submit', page)
    })

    $('.clean_btn').on('click', function (){
        const form = $(this).closest('.find_form')
        form.find('input').not('[name=csrfmiddlewaretoken]').val('')
        form.trigger('submit')
    })

    $('[data-sortby]').on('click', function (){
        var picked_sortby = $(this).attr('data-sortby');
        const icon = $(this).find('i');
        const active_sortby_elem = $(this).parent().children('[data-sortby-active]');
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
        const form_selector = $(this).closest('[data-find-form]').attr('data-find-form')
        const form = $(form_selector);
        // form.find('.sorting_input').val(picked_sortby).change();
        form.find('.sorting_input').val(picked_sortby).change();
        form.trigger('submit');
    })

    // $('.sorting_input').on('change', function (){
    //     console.log('change')
    // })

    function refresh_icons(){

        const sorting_input = $('.sorting_input');
        if(sorting_input.length == 0) return
        // if(sorting_input.length > 0){
        //     const old_sorty = $('[data-sortby-active]')
        //     old_sorty.removeClass('bg-c_yellow-700')
        //     old_sorty.removeAttr('data-sortby-active')
        // }
        const old_sorty = $('[data-sortby-active]')
        old_sorty.removeClass('bg-c_yellow-700')
        old_sorty.removeAttr('data-sortby-active')
        const active_sorting = sorting_input.val();
        const sort_elem = $(`[data-sortby$=${active_sorting.replace('-', '')}]`);
        const icon = sort_elem.find('i')
        sort_elem.attr('data-sortby-active', '')
        sort_elem.attr('data-sortby', active_sorting)
        const is_desc = active_sorting.includes('-')
        if (is_desc){
            icon.removeClass('fa-arrow-down-short-wide');
            icon.addClass('fa-arrow-down-wide-short');
        }
        else{
            icon.removeClass('fa-arrow-down-wide-short');
            icon.addClass('fa-arrow-down-short-wide');
        }
        sort_elem.addClass('bg-c_yellow-700');

    }
    //
    refresh_icons();

});

const build_pages = function (data, pages_elem){

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

    pages_elem.html(result);
}

module.exports.build_pages = build_pages;