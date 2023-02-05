$(document).ready(function (){
    $('.delete_cart_item_icon').on('click', function (){
        $(this).find('.delete_cart_item_btn').trigger('click');
    })
    $('.delete_cart_item_btn').on('click', function (e){
        e.stopPropagation();
    });
})