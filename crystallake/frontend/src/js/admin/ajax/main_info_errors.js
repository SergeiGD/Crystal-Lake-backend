 const handle_errors = function(errors){
    var result = ''
    for (var field in errors){
        const message = errors[field][0]
        result += `<li>${message}</li>`
    }
    $('#main_info_errors').html(result);

    $([document.documentElement, document.body]).animate({
        scrollTop: $("#main_info_errors").offset().top
    }, 200);
}

module.exports.handle_errors = handle_errors;