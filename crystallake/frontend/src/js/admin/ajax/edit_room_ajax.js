$(document).ready(function (){

    var files_uploaded = []

    var files_deleted = []

    //const csrf_token = $('input[name=csrfmiddlewaretoken]').attr('value')

    $('#edit_main_info_form').on('file_uploaded', function (event, file_params){
        files_uploaded = [...files_uploaded, file_params]
    })

    $('#edit_main_info_form').on('file_deleted', function (event, file_id){
        files_deleted = [...files_deleted, file_id]
    })

    $('#edit_main_info_form').on('submit', function (event){
        event.preventDefault();

        var raw_data = $("#edit_main_info_form").serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value'])
        });

        $.map(files_uploaded, function(n, i){
            for (var file in n){
                post_data.append(file, n[file])
            }
        });

        $.map(files_deleted, function(n, i){
            for (var file in n){
                post_data.append(file, n[file])
            }
        });

        $.ajax({
            url: $('#edit_main_info_form').attr('action'),
            type: 'POST',
            mimeType: 'multipart/form-data',
            processData: false,
            contentType: false,
            data: post_data,
            // success: function (data, textStatus, jqXHR){
            //     const response_json = jQuery.parseJSON(jqXHR.responseText)
            //     window.location.href = response_json['url']
            // },
            error: function (jqXHR){
                const errors_json = jQuery.parseJSON(jqXHR.responseText)
                $('#errors').html(build_erros_list(errors_json));
                $([document.documentElement, document.body]).animate({
                    scrollTop: $("#errors").offset().top
                }, 200);
            }
        }).statusCode({
           302: function (response){
               console.log(typeof(response))
                const response_json = jQuery.parseJSON(response.responseText)
                window.location.href = response_json['url']
            }
        });
    })

    function build_erros_list(errors){
        var result = ''
        for (var field in errors){
            const message = errors[field][0].message
            result += `<li>${message}</li>`
        }
        return result
    }


});