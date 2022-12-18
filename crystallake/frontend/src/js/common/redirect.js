$(document).ready(function(){
    $("[data-goto]").on('click', function(e){
        e.stopPropagation();
        window.location.href = e.currentTarget.getAttribute('data-goto');
    });

    $(".offers").on('click', function(e){
        const elem = e.target.closest('[data-goto]');                                       // в списке офферов (скидки) есть элементы, добавляющиеся диначимески.
        if(!elem) return;                                                                   // поэтому будет искать в его дочерних элементах
        if (elem.dataset.goto) window.location.href = elem.dataset.goto;
    });
});