const errors = require("../errors");
$(document).ready(function (){
    //var workers = []
    var workers = {}
    //var deleted_workers = []

    //const form = $('#edit_timetable, #create_timetable');
    const form = $('.workers_form')

    form.on('worker_added', function (event, worker_id){
        //added_workers.push(worker_id)
        //workers.push({[worker_id]: true})
        workers[worker_id] = true
    })

    form.on('worker_deleted', function (event, worker_id){
        //deleted_workers.push(worker_id)
        //workers.push({worker_id: false})
        workers[worker_id] = false
    })

    $('[data-popup-to-clean]').on('click', function (){
        workers = {}
    })

    form.on('submit', function (event){
        event.preventDefault();

        var raw_data = $(this).serializeArray();
        var form_data = new FormData();

        $.map(raw_data, function(n, i){
            form_data.append(n['name'], n['value'])
        });

        form_data.append('workers', JSON.stringify(workers))

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            processData: false,
            contentType: false,
            data: form_data,
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                errors.handle_errors(response['message'], $("#timetable_errors"))
            },
            success: function (){
                document.location.reload()
            }

        });

    })
})