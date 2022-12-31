$(document).ready(function (){
    $('.find_btn').on('click', function (){
        $(this).closest('.find_form').trigger('submit')
    })

    // $('#tags_pagination').on('click', '[data-page]', function (){
    //     $('#search_tag').trigger('submit', $(this).attr('data-page'));
    // })

    $('.pagination').on('click', '[data-page]', function (){
        const page = $(this).attr('data-page')
        const form = $(this).closest('.pagination').parent().siblings('.find_form');
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
        const form = $(this).closest('form').siblings('.find_form')
        form.trigger('submit');
    })
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