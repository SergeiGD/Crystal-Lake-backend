 const handle_errors = function(errors, elem){
    var result = ''
    for (var field in errors){
        const message = errors[field][0]
        result += `<li>${message}</li>`
    }
    elem.html(result);

    $([document.documentElement, document.body]).animate({
        scrollTop: elem.offset().top
    }, 200);
}

module.exports.handle_errors = handle_errors;