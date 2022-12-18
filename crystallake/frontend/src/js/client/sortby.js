$(document).ready(function (){

    function refresh_icons(){
        $('.sorting .sorting_icon_active').removeClass('sorting_icon_active');

        const sort_by_input = $('#id_sort_by');
        const picked_value = sort_by_input.val();
        const is_desc = sort_by_input.val().includes('-')


        const new_sort_elem = $(`[data-sortby$=${picked_value.replace('-', '')}]`);
        new_sort_elem.attr('data-sortby', picked_value)
        const new_sort_icon = new_sort_elem.find('i');
        new_sort_icon.addClass('sorting_icon_active');
        if (is_desc){
            new_sort_icon.removeClass('fa-arrow-down-short-wide');
            new_sort_icon.addClass('fa-arrow-up-wide-short');
        }
        else{
            new_sort_icon.removeClass('fa-arrow-up-wide-short');
            new_sort_icon.addClass('fa-arrow-down-short-wide');
        }
    }

    refresh_icons();


    $('#clean_btn').on('click', function (){
       window.location.href = window.location.href.split('?')[0];
    });


    $('.sorting_item').on('click', function (){

        var picked_value = $(this).attr('data-sortby');
        const current_value = $('#id_sort_by').val();

        if (picked_value === current_value){
            if (picked_value[0] === '-'){
                picked_value = picked_value.replace('-', '')
            }
            else{
                picked_value = '-' + picked_value;
            }

            $(this).attr('data-sortby', picked_value);

        }

        $('#id_sort_by').val(picked_value).change();


    });

    $('#id_sort_by').on('change', function() {

        refresh_icons();

        $('#offers').trigger('submit');
    });


});