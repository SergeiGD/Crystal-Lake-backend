$(document).ready(function(){
    $("[data-goto]").on('mousedown', function(e){
        e.stopPropagation();
        const url = e.currentTarget.getAttribute('data-goto');
        if (e.which == 1) {
          window.location.href = url
       }
        if (e.which == 2) {
          window.open(url, '_blank').focus();
       }
    });

    $(".offers").on('mousedown', function(e){
        const elem = e.target.closest('[data-goto]');                                       // в списке офферов (скидки) есть элементы, добавляющиеся диначимески.
        if(!elem) return;                                                                   // поэтому будет искать в его дочерних элементах
        if (!elem.dataset.goto) return;
        //if (elem.dataset.goto) window.location.href = elem.dataset.goto;
        if (e.which == 1) {
            window.location.href = elem.dataset.goto;

       }
        if (e.which == 2) {
            window.open(elem.dataset.goto, '_blank').focus();
       }
    });
});