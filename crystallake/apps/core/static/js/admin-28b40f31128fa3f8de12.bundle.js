/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./src/scss/admin.scss":
/*!*****************************!*\
  !*** ./src/scss/admin.scss ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
// extracted by mini-css-extract-plugin


/***/ }),

/***/ "./src/js/admin/add_hours.js":
/*!***********************************!*\
  !*** ./src/js/admin/add_hours.js ***!
  \***********************************/
/***/ ((module) => {

 const add_hours = function(date, hours){
     date.setTime(date.getTime() + (hours * 60 * 60 * 1000))
     return date
}

module.exports.add_hours = add_hours;

/***/ }),

/***/ "./src/js/admin/add_worker_to_timetable.js":
/*!*************************************************!*\
  !*** ./src/js/admin/add_worker_to_timetable.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){

    $('#select_worker').on('submit', function (event, data){
        event.preventDefault();

        const same_elem = $('#timetable_workers_tbody').find(`[data-id="${data.id}"]`).length

        if(same_elem){
            return
        }

        const row = `
                <tr>
                    <th scope="row">${data.id}</th>
                    <td>
                        <a href="${data.link}" class="link-hover d-block">${data.name}</a>
                    </td>
                    <td>${data.phone}</td>
                    <td class="p-0 position-relative w-10r">
                        <button class="btn btn-danger w-100 rounded-0 h-100 position-absolute" type="button" data-temp-elem-id="${data.id}">Убрать</button>
                    </td>
                </tr>
            `
        $('#timetable_workers_tbody').append(row);

        $('#edit_timetable').trigger('worker_added', data.id)

    });

})

/***/ }),

/***/ "./src/js/admin/ajax/add_additional_elem.js":
/*!**************************************************!*\
  !*** ./src/js/admin/ajax/add_additional_elem.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* provided dependency */ var jQuery = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const errors = __webpack_require__(/*! ../errors */ "./src/js/admin/errors.js");
$(document).ready(function (){

    $('.add_additional_form').on('submit', function (event, data={}){
        event.preventDefault();

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': data.id, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
                window.location.reload();
            },
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                errors.handle_errors(response['message'], $('.errors_list'))
            },
        });

    });
})

/***/ }),

/***/ "./src/js/admin/ajax/create_same_room.js":
/*!***********************************************!*\
  !*** ./src/js/admin/ajax/create_same_room.js ***!
  \***********************************************/
/***/ (() => {

// $(document).ready(function (){
//
//     $('#add_same_room').on('submit', function (event){
//         event.preventDefault();
//
//         const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')
//
//         $.ajax({
//             url: $(this).attr('action'),
//             type: 'POST',
//             data: {'csrfmiddlewaretoken': csrf_token},
//             success: function (response){
//                 const new_room = {id: response['data'].id}
//                 append_row(new_room)
//             }
//         });
//
//         function append_row(room){
//             const row = `
//                 <tr>
//                     <th scope="row">${room.id}</th>
//                     <td class="p-0 position-relative w-10r">
//                         <button class="btn btn-danger w-100 rounded-0 h-100 position-absolute" type="button" data-id="${room.id}">Убрать</button>
//                     </td>
//                 </tr>
//             `
//             $('#same_rooms_list_body').append(row);
//
//         }
//
//     });
// })

/***/ }),

/***/ "./src/js/admin/ajax/default_set_main_info.js":
/*!****************************************************!*\
  !*** ./src/js/admin/ajax/default_set_main_info.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* provided dependency */ var jQuery = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const errors = __webpack_require__(/*! ../errors */ "./src/js/admin/errors.js");

$(document).ready(function (){
    $('.default_ajax_edit').on('submit', function (event){
        event.preventDefault();
        const current_form = $(this);

        $.ajax({
            url: current_form.attr('action'),
            type: 'POST',
            data: $(current_form).serialize(),
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                errors.handle_errors(response['message'], $('#main_info_errors'))
            },
        }).statusCode({
           302: function (data){
                const response = jQuery.parseJSON(data.responseText)
                window.location.href = response['data']
            }
        });
    })
})

/***/ }),

/***/ "./src/js/admin/ajax/delete_additional_elem.js":
/*!*****************************************************!*\
  !*** ./src/js/admin/ajax/delete_additional_elem.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* provided dependency */ var jQuery = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){

    $('.delete_additional_form').on('submit', function (event, data){
        const current_form = $(this);
        event.preventDefault();

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': data['id'], 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
                // window.location = window.location
                window.location.reload();
                // const table = current_form.closest('.additional_info_tbody');
                // const row = table.find(`[data-id=${elem_id}]`).closest('tr')
                // row.remove()
            }
        }).statusCode({
           302: function (data){
                const response = jQuery.parseJSON(data.responseText)
                window.location.href = response['data']
            }
        });

    });

    // $(document).ajaxStop(function(){
    //     window.location.reload();
    // });

});

/***/ }),

/***/ "./src/js/admin/ajax/edit_additional_elem.js":
/*!***************************************************!*\
  !*** ./src/js/admin/ajax/edit_additional_elem.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* provided dependency */ var jQuery = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){
    $('.edit_additional_form').on('submit', function (event, elem_id) {
        event.preventDefault();
        const popup = $(this).find('[data-popup]').attr('data-popup')
        //const  popup = $(this).attr('data-popup')

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': elem_id, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
                console.log(response.data)
                console.log(popup)
                $(popup).trigger('popup_open', response.data)
            }
        }).statusCode({
           302: function (data){
                const response = jQuery.parseJSON(data.responseText)
                window.location.href = response['data']
            }
        });

    })

})

/***/ }),

/***/ "./src/js/admin/ajax/get_dates_info.js":
/*!*********************************************!*\
  !*** ./src/js/admin/ajax/get_dates_info.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const add_hours = __webpack_require__(/*! ../add_hours */ "./src/js/admin/add_hours.js");

$(document).ready(function () {

    $('.calendar__room').on('selectMonth', function(event, month_str, month_index, additional_info){

        if (!additional_info?.programmatically){
            $('.calendar__room').not(this).evoCalendar('selectMonth', month_index, {programmatically: true});
        }
        $(this).find('.day').first().trigger('click');

        $(this).siblings('form').children('button').first().trigger('click')

    });

    $(".calendar__room_form").on('submit', function (event){
        event.preventDefault();

        const calendar = $(this).siblings('.evoCalendar')
        const date_str = calendar.evoCalendar('getActiveDate');
        const year = date_str.substring(0,4),
            month = date_str.substring(5,7)
        const start = new Date(
            year,
            parseInt(month) - 1,
            1,
        ).getTime()

        const end = new Date(
            year,
            month,
            0,
        ).getTime()

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'GET',
            data: {'start': start, 'end': end, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){

                 $('.day-busy').removeClass('day-busy')
                calendar.find(".event-indicator").removeClass('event-indicator')
                calendar.evoCalendar('removeCalendarEvent', []);

                for (const day of response['data']){

                    const date = new Date(day * 1000)
                    const local_date = add_hours.add_hours(date, date.getTimezoneOffset() / 60 * -1)
                    const date_str = local_date.toISOString().substring(0,10)

                    calendar.evoCalendar('addCalendarEvent',
                        {
                            id: Date.now(),
                            name: "busy",
                            date: date_str,
                            type: "busy",
                        }
                    );
                }

                $(".event-indicator").each(function(){              // если на день есть событие, то номер занят
                    $(this).parent().addClass('day-busy');
                });
            },
        });
    })

    $('.calendar__room').evoCalendar('selectMonth', new Date().getMonth(), {programmatically: true});   // при выбриаем текущей месяц, чтоб стригерить отправку запроса


    // $('.calendar__room').on('selectMonth', function(){
    //     console.log($(`.calendar[data-id="68"]`).evoCalendar.calendarEvents)
    //     console.log($(this).attr('data-id'))
    //
    //     $(".event-indicator").each(function(){              // если на день есть событие, то номер занят
    //         $(this).parent().addClass('day-busy');
    //     });
    // });
})

/***/ }),

/***/ "./src/js/admin/ajax/get_service_dates_info.js":
/*!*****************************************************!*\
  !*** ./src/js/admin/ajax/get_service_dates_info.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const add_hours = __webpack_require__(/*! ../add_hours */ "./src/js/admin/add_hours.js");

$(document).ready(function () {

    // TODO: ДОБАВИТЬ АККОРДЕОН И ПРИ ЕГО ОТКРЫТИИ ВЫЗЫВАЕМ selectMonth


    $('.calendar__service').on('selectMonth', function(event, month_str, month_index){

        // if (!additional_info?.programmatically){
        //     $('.calendar__service').not(this).evoCalendar('selectMonth', month_index, {programmatically: true});
        // }
        $(this).find('.day').first().trigger('click');

        $(this).siblings('form').children('button').first().trigger('click')

        console.log('asd')
    });

    $(".calendar__service_form").on('submit', function (event){
        event.preventDefault();

        const calendar = $(this).siblings('.evoCalendar')
        const date_str = calendar.evoCalendar('getActiveDate');
        const year = date_str.substring(0,4),
            month = date_str.substring(5,7)
        const start = new Date(
            year,
            parseInt(month) - 1,
            1,
        ).getTime()

        const end = new Date(
            year,
            month,
            0,
        ).getTime()

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'GET',
            data: {'start': start, 'end': end, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){

                $('.day-busy').removeClass('day-busy')
                calendar.find(".event-indicator").removeClass('event-indicator')
                calendar.evoCalendar('removeCalendarEvent', []);

                for (const day of response['data']){
                    const start = new Date(day.start * 1000)
                    const local_start = add_hours.add_hours(start, start.getTimezoneOffset() / 60 * -1)
                    const end = new Date(day.end * 1000)
                    const local_end = add_hours.add_hours(end, end.getTimezoneOffset() / 60 * -1)

                    const date = local_start.toISOString().substring(0,10)
                    const start_time = local_start.toISOString().substring(11,16)
                    const end_time = local_end.toISOString().substring(11,16)
                    calendar.evoCalendar('addCalendarEvent',
                        {
                            id: new Date(),
                            date: date,
                            name: `${start_time} - ${end_time}`,
                            type: "enable",
                            description: (day.left !== undefined) ? `${day.left} мест(а)` : ''
                        }
                    );

                }

                $(".event-indicator").each(function(){              // если на день есть событие, то номер занят
                    $(this).parent().addClass('day-enable');
                });
            },
        });
    })

    $('.calendar__service').evoCalendar('selectMonth', new Date().getMonth(), {programmatically: true});   // при выбриаем текущей месяц, чтоб стригерить отправку запроса

})

/***/ }),

/***/ "./src/js/admin/ajax/manage_purchase.js":
/*!**********************************************!*\
  !*** ./src/js/admin/ajax/manage_purchase.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* provided dependency */ var jQuery = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const errors = __webpack_require__(/*! ../errors */ "./src/js/admin/errors.js");
$(document).ready(function (){

    $('.manage_purchase').on('submit', function (event){
        event.preventDefault();

        const form = $(this)

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            success: function (){
                window.location.reload();
            },
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                errors.handle_errors(response['message'], form.find('.errors_list'))
            },
        });

    });
})

/***/ }),

/***/ "./src/js/admin/ajax/manage_timetable.js":
/*!***********************************************!*\
  !*** ./src/js/admin/ajax/manage_timetable.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* provided dependency */ var jQuery = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const errors = __webpack_require__(/*! ../errors */ "./src/js/admin/errors.js");
$(document).ready(function (){
    //var workers = []
    var workers = {}
    //var deleted_workers = []

    const form = $('#edit_timetable, #create_timetable');

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

    form.on('submit', function (event){
        event.preventDefault();

        var raw_data = $(this).serializeArray();
        var form_data = new FormData();

        $.map(raw_data, function(n, i){
            form_data.append(n['name'], n['value'])
        });

        form_data.append('workers', JSON.stringify(workers))
        console.log(form_data)

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

/***/ }),

/***/ "./src/js/admin/ajax/offer_ajax.js":
/*!*****************************************!*\
  !*** ./src/js/admin/ajax/offer_ajax.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* provided dependency */ var jQuery = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const errors = __webpack_require__(/*! ../errors */ "./src/js/admin/errors.js");
$(document).ready(function (){



    var files_uploaded = []

    var files_deleted = []

    $('#edit_main_info_form').on('file_uploaded', function (event, file_params){
        files_uploaded = [...files_uploaded, file_params]
    })

    $('#edit_main_info_form').on('file_deleted', function (event, file_id){
        files_deleted = [...files_deleted, file_id]
    })

    $('#save_main_btn').on('click', function (){
        $('#edit_main_info_form').trigger('submit')
    });

    $('#edit_main_info_form').on('submit', function (event){
        event.preventDefault();

        var raw_data = $("#edit_main_info_form").serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value'])
        });

        $.map(files_deleted, function(n, i){
            for (var file in n){
                post_data.append(file, n[file])
            }
        });

        $.map(files_uploaded, function(n, i){
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
            error: function (jqXHR){
                const response = jQuery.parseJSON(jqXHR.responseText)
                errors.handle_errors(response['message'], $("#main_info_errors"))
            },
        }).statusCode({
           302: function (data){
                const response = jQuery.parseJSON(data.responseText)
                window.location.href = response['data']
            }
        });
    })





});

/***/ }),

/***/ "./src/js/admin/ajax/search_clients_for_order.js":
/*!*******************************************************!*\
  !*** ./src/js/admin/ajax/search_clients_for_order.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const find_items = __webpack_require__(/*! ../find_items */ "./src/js/admin/find_items.js");
$(document).ready(function (){

    $('#search_clients').on('submit', function (event, page='1'){
        event.preventDefault();

        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $('#pick_client_modal').find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                build_rows(response['data']['items'])
                find_items.build_pages(response['data']['pages'], $('#clients_pagination'))
            },
        });

        function build_rows(data){
            var result = ''
            for(const item of data){
                const row = `
                    <tr>
                        <th scope="row">${item.id}</th>
                        <td>
                            <a class="link-hover" href="${item.link}">${item.name}</a>   
                        </td>
                        <td>
                            ${item.phone}
                        </td>
                        <td class="p-0 position-relative w-10r">
                            <button data-id="${item.id}" data-name="${item.name}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" data-bs-dismiss="modal" type="button">
                                Выбрать
                            </button>
                        </td>
                    </tr>
                `
                result += row
            }
            $('#clients_tbody').html(result);
        }

    });

})

/***/ }),

/***/ "./src/js/admin/ajax/search_groups_for_worker.js":
/*!*******************************************************!*\
  !*** ./src/js/admin/ajax/search_groups_for_worker.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const find_items = __webpack_require__(/*! ../find_items */ "./src/js/admin/find_items.js");
$(document).ready(function (){

    $('#search_groups').on('submit', function (event, page='1'){
        event.preventDefault();

        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $('#pick_group_modal').find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                build_rows(response['data']['items'])
                find_items.build_pages(response['data']['pages'], $('#groups_pagination'))
            },
        });

        function build_rows(data){
            var result = ''
            for(const item of data){
                const row = `
                    <tr>
                        <th scope="row">${item.id}</th>
                        <td>
                            <a class="link-hover" href="${item.link}">${item.name}</a>   
                        </td>
                        <td class="p-0 position-relative w-10r">
                            <button data-id="${item.id}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" data-bs-dismiss="modal" type="button">
                                Выбрать
                            </button>
                        </td>
                    </tr>
                `
                result += row
            }
            $('#groups_tbody').html(result);
        }

    });

})

/***/ }),

/***/ "./src/js/admin/ajax/search_permissions_for_group.js":
/*!***********************************************************!*\
  !*** ./src/js/admin/ajax/search_permissions_for_group.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const find_items = __webpack_require__(/*! ../find_items */ "./src/js/admin/find_items.js");
$(document).ready(function (){

    $('#search_permissions').on('submit', function (event, page='1'){
        event.preventDefault();

        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $('#pick_permission_modal').find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                build_rows(response['data']['items'])
                find_items.build_pages(response['data']['pages'], $('#permissions_pagination'))
            },
        });

        function build_rows(data){
            var result = ''
            for(const item of data){
                const row = `
                    <tr>
                        <th scope="row">${item.id}</th>
                        <td>${item.name}</td>
                        <td class="p-0 position-relative w-10r">
                            <button data-id="${item.id}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" data-bs-dismiss="modal" type="button">
                                Выбрать
                            </button>
                        </td>
                    </tr>
                `
                result += row
            }
            $('#permissions_tbody').html(result);
        }

    });

})

/***/ }),

/***/ "./src/js/admin/ajax/search_rooms.js":
/*!*******************************************!*\
  !*** ./src/js/admin/ajax/search_rooms.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const find_items = __webpack_require__(/*! ../find_items */ "./src/js/admin/find_items.js");
$(document).ready(function (){

    $('#search_rooms').on('submit', function (event, page='1'){
        event.preventDefault();

        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $('#rooms_sorting').find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                build_rows(response['data']['items'])
                find_items.build_pages(response['data']['pages'], $('#rooms_pagination'))
            },
        });

        function build_rows(data){
            var result = ''
            for(const item of data){
                const row = `
                    <tr>
                        <th scope="row">${item.id}</th>
                        <td>
                            <a class="link-hover" href="${item.link}">${item.name}</a>   
                        </td>
                        <td>
                            ${item.beds}
                        </td>
                        <td>
                            ${item.rooms}
                        </td>
                        <td>
                            ${item.default_price}
                        </td><td>
                            ${item.weekend_price}
                        </td>
                        <td class="p-0 position-relative w-10r">
                            <button data-id="${item.id}" data-name="${item.name}" data-link="${item.link}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" data-bs-toggle="modal" data-bs-target="#create_room_purchase_modal" type="button">

<!--                            <button data-id="${item.id}" data-name="${item.name}" data-link="${item.link}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" data-bs-toggle="modal" data-bs-target="#room_purchase_modal" type="button">-->
                                Выбрать
                            </button>
                        </td>
                    </tr>
                `
                result += row
            }
            $('#rooms_tbody').html(result);
        }

    });

})

/***/ }),

/***/ "./src/js/admin/ajax/search_services.js":
/*!**********************************************!*\
  !*** ./src/js/admin/ajax/search_services.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const find_items = __webpack_require__(/*! ../find_items */ "./src/js/admin/find_items.js");
$(document).ready(function (){

    $('#search_services').on('submit', function (event, page='1'){
        event.preventDefault();

        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $('#services_sorting').find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)


        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                build_rows(response['data']['items'])
                find_items.build_pages(response['data']['pages'], $('#services_pagination'))
            },
        });

        function build_rows(data){
            var result = ''
            for(const item of data){
                const row = `
                    <tr>
                        <th scope="row">${item.id}</th>
                        <td>
                            <a class="link-hover" href="${item.link}">${item.name}</a>   
                        </td>
                        <td>
                            ${item.dynamic_timetable}
                        </td>
                        <td>
                            ${item.default_price}
                        </td><td>
                            ${item.weekend_price}
                        </td>
                        <td class="p-0 position-relative w-10r">
                            <button data-id="${item.id}" data-dynamic="${item.dynamic_timetable}" data-name="${item.name}" data-link="${item.link}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" data-bs-toggle="modal"  data-bs-target="#service_purchase_modal" type="button">
                                Выбрать
                            </button>
                        </td>
                    </tr>
                `
                result += row
            }
            $('#services_tbody').html(result);
        }

    });

})

/***/ }),

/***/ "./src/js/admin/ajax/search_services_for_worker.js":
/*!*********************************************************!*\
  !*** ./src/js/admin/ajax/search_services_for_worker.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const find_items = __webpack_require__(/*! ../find_items */ "./src/js/admin/find_items.js");
$(document).ready(function (){

    $('#search_service').on('submit', function (event, page='1'){
        event.preventDefault();

        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $('#pick_service_modal').find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                build_rows(response['data']['items'])
                find_items.build_pages(response['data']['pages'], $('#services_pagination'))
            },
        });

        function build_rows(data){
            var result = ''
            for(const item of data){
                const row = `
                    <tr>
                        <th scope="row">${item.id}</th>
                        <td>
                            <a class="link-hover" href="${item.link}">${item.name}</a>   
                        </td>
                        <td class="p-0 position-relative w-10r">
                            <button data-id="${item.id}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" data-bs-dismiss="modal" type="button">
                                Выбрать
                            </button>
                        </td>
                    </tr>
                `
                result += row
            }
            $('#services_tbody').html(result);
        }

    });

})

/***/ }),

/***/ "./src/js/admin/ajax/search_tags_for_offer.js":
/*!****************************************************!*\
  !*** ./src/js/admin/ajax/search_tags_for_offer.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const find_items = __webpack_require__(/*! ../find_items */ "./src/js/admin/find_items.js");
$(document).ready(function (){

    $('#search_tag').on('submit', function (event, page='1'){
        event.preventDefault();

        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $('#add_tag_modal').find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                build_rows(response['data']['items'])
                find_items.build_pages(response['data']['pages'], $('#tags_pagination'))
            },
        });

        function build_rows(data){
            var result = ''
            for(const item of data){
                const row = `
                    <tr>
                        <th scope="row">${item.id}</th>
                        <td>
                            <a class="link-hover" href="${item.link}">${item.name}</a>   
                        </td>
                        <td class="p-0 position-relative w-10r">
                            <button data-id="${item.id}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" data-bs-dismiss="modal" type="button">
                                Выбрать
                            </button>
                        </td>
                    </tr>
                `
                result += row
            }
            $('#tags_add_body').html(result);
        }

    });

})

/***/ }),

/***/ "./src/js/admin/ajax/search_timetables_for_service.js":
/*!************************************************************!*\
  !*** ./src/js/admin/ajax/search_timetables_for_service.js ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const find_items = __webpack_require__(/*! ../find_items */ "./src/js/admin/find_items.js");
const form_date = __webpack_require__(/*! ../form_date */ "./src/js/admin/form_date.js");

$(document).ready(function (){

    $('#search_timetables').on('submit', function (event, page='1'){
        event.preventDefault();


        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $('#pick_timetable_modal').find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)
        post_data.append('service_id', $('#id_service_id').attr('value'))

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                build_rows(response['data']['items'])
                find_items.build_pages(response['data']['pages'], $('#timetables_pagination'))
            },
        });

        function build_rows(data){
            var result = ''
            for(const item of data){
                const start = new Date(item.start * 1000)   // на 1000, т.к. получаем в секундах, а джесу нужно в мс
                const end = new Date(item.end * 1000)
                const formated_start = form_date.form_date(start)
                const formated_end = form_date.form_date(start)
                const day = start.toISOString().substring(0,10)
                const start_time = start.toISOString().substring(11,16)
                const end_time = end.toISOString().substring(11,16)
                const row = `
                    <tr>
                        <td scope="row">${formated_start}</td>
                        <td scope="row">${formated_end}</td>
                        <td class="p-0 position-relative w-10r">
                            <button data-day="${day}" data-time-start="${start_time}" data-time-end="${end_time}" data-time-str="${formated_start} - ${formated_end}" data-id="${item.id}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" data-bs-toggle="modal"  data-bs-target="#service_purchase_modal" type="button">
                                Выбрать
                            </button>
                        </td>
                    </tr>
                `
                result += row
            }
            $('#timetables_tbody').html(result);
        }

    });

})

/***/ }),

/***/ "./src/js/admin/ajax/search_workers_for_timetable.js":
/*!***********************************************************!*\
  !*** ./src/js/admin/ajax/search_workers_for_timetable.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const find_items = __webpack_require__(/*! ../find_items */ "./src/js/admin/find_items.js");
$(document).ready(function (){

    $('#search_worker').on('submit', function (event, page='1', called_by){
        event.preventDefault();

        var raw_data = $(this).serializeArray();
        var post_data = new FormData();

        $.map(raw_data, function(n, i){
            post_data.append(n['name'], n['value']);
        });

        const sort_by = $('#pick_worker_modal').find('[data-sortby-active]').attr('data-sortby')
        post_data.append('sort_by', sort_by)
        post_data.append('page_number', page)

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: post_data,
            processData: false,
            contentType: false,
            success: function (response){
                build_rows(response['data']['items'])
                find_items.build_pages(response['data']['pages'], $('#workers_pagination'))
            },
        });

        function build_rows(data){
            var result = ''
            for(const item of data){
                const row = `
                    <tr>
                        <th scope="row">${item.id}</th>
                        <td>
                            <a class="link-hover" href="${item.link}">${item.name}</a>   
                        </td>
                        <td>
                            ${item.phone}
                        </td>
                        <td class="p-0 position-relative w-10r">
                            <button data-id="${item.id}" data-name="${item.name}" data-link="${item.link}" data-phone="${item.phone}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" type="button" data-bs-toggle="modal" data-bs-target="#manage_timetable_modal">
                                Выбрать
                            </button>
                        </td>
                    </tr>
                `
                result += row
            }
            $('#workers_tbody').html(result);
        }

    });

})

/***/ }),

/***/ "./src/js/admin/clean_popup.js":
/*!*************************************!*\
  !*** ./src/js/admin/clean_popup.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){
    $('[data-popup-to-clean]').on('click', function (){
        const popup = $(this).attr('data-popup-to-clean')
        $(popup).find('input').not('[name="csrfmiddlewaretoken"]').val('').prop('checked', false)
        $(popup).find('tbody').html('')
    })
})

/***/ }),

/***/ "./src/js/admin/delete_img.js":
/*!************************************!*\
  !*** ./src/js/admin/delete_img.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function() {
    $('#edit_main_info_form').on('click', '.delete_img', function () {
        const container = $(this).closest('[data-order]');

        container.nextAll('[data-order]').each(function () {
            const new_order = $(this).find('input[id$=order]').attr('value') - 1;   // изменяем порядоковые номера последующих картинок
            $(this).find('input[id$=order]').attr('value', new_order);
            $(this).attr('data-order', new_order)
        });


        const id = container.find('input[id$=id]').attr('value')
        const form_name = container.find('input[id$=id]').attr('name').slice(0, -2)

        $('#edit_main_info_form').trigger('file_deleted', {[form_name + 'id']: id, [form_name + 'DELETE ']: 'on'}); // отправляем форму на удаление и id картинки

        container.addClass('d-none')            // скрываем картинку и помечаем как не активную
        container.removeAttr('data-active')

        $('#accordion_body_images').trigger('refresh_required');    // обновляем стелки


    });
});


/***/ }),

/***/ "./src/js/admin/errors.js":
/*!********************************!*\
  !*** ./src/js/admin/errors.js ***!
  \********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
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

/***/ }),

/***/ "./src/js/admin/find_items.js":
/*!************************************!*\
  !*** ./src/js/admin/find_items.js ***!
  \************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
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

/***/ }),

/***/ "./src/js/admin/form_date.js":
/*!***********************************!*\
  !*** ./src/js/admin/form_date.js ***!
  \***********************************/
/***/ ((module) => {

const form_date = function(date) {
        const year = date.toISOString().substring(0,4),
            month = date.toISOString().substring(5,7),
            day = date.toISOString().substring(8,10),
            hours = date.toISOString().substring(11,13),
            minutes = date.toISOString().substring(14,16);

        return `${day}/${month}/${year} ${hours}:${minutes}`;
    }


module.exports.form_date = form_date;

/***/ }),

/***/ "./src/js/admin/item_select.js":
/*!*************************************!*\
  !*** ./src/js/admin/item_select.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){
    $(document).on('click', '[data-id]', function (){

        const form = $(this).closest('form');
        form.trigger('submit', {
            'is_dynamic': $(this).attr('data-dynamic'),
            'phone': $(this).attr('data-phone'),
            'name': $(this).attr('data-name'),
            'id': $(this).attr('data-id'),
            'link': $(this).attr('data-link'),
            'time_str': $(this).attr('data-time-str'),
            'time_start': $(this).attr('data-time-start'),
            'time_end': $(this).attr('data-time-end'),
            'day': $(this).attr('data-day')
            }
        );
        // form.trigger('submit', [
        //     $(this).attr('data-id'),
        //     $(this).attr('data-name'),
        //     $(this).attr('data-link'),
        //     {
        //         'is_dynamic': $(this).attr('data-dynamic'),
        //         'phone': $(this).attr('data-phone'),
        //     }
        // ]);
    });
})

/***/ }),

/***/ "./src/js/admin/move_img.js":
/*!**********************************!*\
  !*** ./src/js/admin/move_img.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function(){
    function update_arrows(){
        $('.move_prev, .move_next').removeClass('opacity-50');

        const first_elem =$('#accordion_body_images').children('[data-active][data-order]:first');
        const last_elem = $('#accordion_body_images').children('[data-active][data-order]:last');

        first_elem.find('.move_prev').first().addClass('opacity-50');       // обновляем стрелки
        last_elem.find('.move_next').last().addClass('opacity-50');
    }

    update_arrows();

    $('#accordion_body_images').on('click', '.move_next', function(){
        const current_item = $(this).closest('[data-order]');
        const number = current_item.attr('data-order');

        if (number == $(current_item).siblings('[data-order][data-active]').length + 1) return;      // элемент является крайним, если число его братьев == его номеру + 1

        const next_item = current_item.nextAll('[data-active]').first();

        current_item.insertAfter(next_item);
        current_item.attr('data-order', Number(number) + 1);
        next_item.attr('data-order', Number(number));                               // обновялем атрибуты, в которых содержится порядковый номер

        const current_order_input = current_item.find('input[id$=order]');
        current_order_input.attr('value', Number(number) + 1)                       // обновялем инпуты, в которых содержится порядковый номер
        const next_order_input = next_item.find('input[id$=order]');
        next_order_input.attr('value', Number(number))

        update_arrows();                                                            // обновляем стрелки
    });

    $('#accordion_body_images').on('click', '.move_prev', function(){
        const current_item = $(this).closest('[data-order]');
        const number = current_item.attr('data-order');

        if (number == 1) return;                                                    // элемент первый, если его номер равен 1 (нулевой - главная картинки объекта offer)

        const prev_item = current_item.prevAll('[data-active]').first();

        current_item.insertBefore(prev_item);

        console.log(number)

        current_item.attr('data-order', Number(number) - 1);
        prev_item.attr('data-order', Number(number));

        const current_order_input = current_item.find('input[id$=order]');
        current_order_input.attr('value', Number(number) - 1)
        const prev_order_input = prev_item.find('input[id$=order]');
        prev_order_input.attr('value', Number(number))

        update_arrows();
    });

    $('#accordion_body_images').on('refresh_required', function(){
        update_arrows();
    });


});

/***/ }),

/***/ "./src/js/admin/new_offer_main_img.js":
/*!********************************************!*\
  !*** ./src/js/admin/new_offer_main_img.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){
    // при загрузке фотографии к новому предложению, скрываем изначальную кнопку и отображаем картику
    $('#img_wrapper__temp > .upload_img_input').on('change', function (){
        $(this).siblings('.img').removeClass('d-none')                      // отображаем картинки
        $('#upload_button__temp').addClass('d-none')                        // скрываем кнопку
        $('#img_wrapper__temp').addClass('img_wrapper').removeAttr('id')    // удаляем id
    });
});

/***/ }),

/***/ "./src/js/admin/remove_worker_from_timetable.js":
/*!******************************************************!*\
  !*** ./src/js/admin/remove_worker_from_timetable.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){
    $('#timetable_workers_tbody').on('click', '[data-temp-elem-id]', function (){
        event.preventDefault()
        const worker_id = $(this).attr('data-temp-elem-id')
        // const table = $('#timetable_workers_tbody');
        // const row = table.find(`[data-id=${worker_id}]`).closest('tr')
        // row.remove()
        $(this).closest('tr').remove()
        $('#edit_timetable').trigger('worker_deleted', worker_id)
    })
})

/***/ }),

/***/ "./src/js/admin/room_purchase_popup_open.js":
/*!**************************************************!*\
  !*** ./src/js/admin/room_purchase_popup_open.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const add_hours = __webpack_require__(/*! ./add_hours */ "./src/js/admin/add_hours.js");
$(document).ready(function (){

    $('#room_purchase_modal').on('popup_open', function (event, data){

        $('#id_purchase_id').val(data.id)
        $('.purchase_name').html(data.offer.name).attr('href', data.offer.link)
        $('.room_timetable_link').attr('href', data.offer.link + '#dates')
        const start = new Date(data.start * 1000)
        const local_start = add_hours.add_hours(start, start.getTimezoneOffset() / 60 * -1)
        $('#id_start').val(local_start.toISOString().split('T')[0])
        const end = new Date(data.end * 1000)
        const local_end = add_hours.add_hours(end, end.getTimezoneOffset() / 60 * -1)
        $('#id_end').val(local_end.toISOString().split('T')[0])
        $('#id_is_paid').prop('checked', data.is_paid);
        $('#id_is_prepayment_paid').prop('checked', data.is_prepayment_paid);
    })
})

/***/ }),

/***/ "./src/js/admin/select_client.js":
/*!***************************************!*\
  !*** ./src/js/admin/select_client.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){

    $('#select_client').on('submit', function (event, data){
        event.preventDefault();

        $('#id_client_name').val(data.name);
        $('#id_client_id').val(data.id);

    });

})

/***/ }),

/***/ "./src/js/admin/select_room_purchase.js":
/*!**********************************************!*\
  !*** ./src/js/admin/select_room_purchase.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){

    $('#select_room_purchase').on('submit', function (event, data){
        event.preventDefault();

        $('.purchase_name').html(data.name).attr('href', data.link);
        $('#id_create-room_id').val(data.id);
        $('.room_timetable_link').attr('href', data.link + '#dates')

    });

})

/***/ }),

/***/ "./src/js/admin/select_service_purchase.js":
/*!*************************************************!*\
  !*** ./src/js/admin/select_service_purchase.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){

    $('#select_service_purchase').on('submit', function (event, data){
        event.preventDefault();

        $('#service_purchase').html(data.name).attr('href', data.link);
        $('#id_service_id').val(data.id);

        const is_dynamic = (data.is_dynamic === 'true');

        if (is_dynamic){
            $('.static_time_field').addClass('d-block')
            $('.dynamic_time_field').addClass('d-none')
        }
        else{
            $('.dynamic_time_field').addClass('d-block')
            $('.static_time_field').addClass('d-none')
        }

    });

})

/***/ }),

/***/ "./src/js/admin/select_timetable.js":
/*!******************************************!*\
  !*** ./src/js/admin/select_timetable.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){

    $('#select_timetable').on('submit', function (event, data){
        event.preventDefault();

        $('#id_time_select_text').val(data.time_str);

        $('#id_day').val(data.day);
        $('#id_time_start').val(data.time_start);
        $('#id_time_end').val(data.time_end);

    });

})

/***/ }),

/***/ "./src/js/admin/service_purchase_popup_open.js":
/*!*****************************************************!*\
  !*** ./src/js/admin/service_purchase_popup_open.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const form_date = __webpack_require__(/*! ./form_date */ "./src/js/admin/form_date.js");
const add_hours = __webpack_require__(/*! ./add_hours */ "./src/js/admin/add_hours.js");

$(document).ready(function (){

    $('#service_purchase_modal').on('popup_open', function (event, data){

        $('#id_purchase_id').val(data.id)
        $('#service_purchase').html(data.offer.name).attr('href', data.offer.link)
        $('#id_quantity').val(data.quantity)
        $('#id_is_paid').prop('checked', data.is_paid);
        $('#id_is_prepayment_paid').prop('checked', data.is_prepayment_paid);
        $('#id_service_id').val(data.offer.id);

        const start = new Date(data.start * 1000)
        const local_start = add_hours.add_hours(start, start.getTimezoneOffset() / 60 * -1)
        const end = new Date(data.end * 1000)
        const local_end = add_hours.add_hours(end, end.getTimezoneOffset() / 60 * -1)

        const day = local_start.toISOString().substring(0,10),
            start_time = local_start.toISOString().substring(11,16),
            end_time = local_end.toISOString().substring(11,16)

        $('#id_day').val(day)
        $('#id_time_start').val(start_time)
        $('#id_time_end').val(end_time)
        if (data.offer.dynamic_timetable){
            $('.static_time_field').removeClass('d-none')
            $('.static_time_field').addClass('d-block')

            $('.dynamic_time_field').removeClass('d-block')
            $('.dynamic_time_field').addClass('d-none')
        }
        else{
            $('#id_time_select_text').val(`${form_date.form_date(start)} - ${form_date.form_date(end)}`)

            $('.dynamic_time_field').removeClass('d-none')
            $('.dynamic_time_field').addClass('d-block')

            $('.static_time_field').removeClass('d-block')
            $('.static_time_field').addClass('d-none')
        }

        // const start = new Date(data.start * 1000)
        // $('#id_start').val(start.toISOString().split('T')[0])
        // const end = new Date(data.end * 1000)
        // $('#id_end').val(end.toISOString().split('T')[0])
        // $('#id_is_paid').prop('checked', data.is_paid);
        // $('#id_is_prepayment_paid').prop('checked', data.is_prepayment_paid);
    })
})

/***/ }),

/***/ "./src/js/admin/show_img.js":
/*!**********************************!*\
  !*** ./src/js/admin/show_img.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function(){

    $('.main_info_container').on('click', '.open_img', function(){
        const modal_id = $(this).attr("data-bs-target");                // берем id попапа
        const img_src = $(this).siblings('img').first().attr('src');    // получаем src каритнки
        $(modal_id + " img").attr('src', img_src);                      // устанавливаем src картинке в попапе
    });

});

/***/ }),

/***/ "./src/js/admin/timetable_popup_open.js":
/*!**********************************************!*\
  !*** ./src/js/admin/timetable_popup_open.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
const add_hours = __webpack_require__(/*! ./add_hours */ "./src/js/admin/add_hours.js");
$(document).ready(function (){

    $('#manage_timetable_modal').on('popup_open', function (event, data){
        console.log(data)

        $('#id_timetable_id').val(data.id)
        const start = new Date(data.start * 1000)
        const local_start = add_hours.add_hours(start, start.getTimezoneOffset() / 60 * -1)
        const end = new Date(data.end * 1000)
        const local_end = add_hours.add_hours(end, end.getTimezoneOffset() / 60 * -1)
        $('#id_date').val(local_start.toISOString().substring(0,10))
        $('#id_start').val(local_start.toISOString().substring(11,16))
        $('#id_end').val(local_end.toISOString().substring(11,16))
        $('#timetable_workers_tbody').html('')

        for (const worker of data.workers){
            const row = `
                <tr>
                    <th scope="row">${worker.id}</th>
                    <td>
                        <a href="${worker.link}" class="link-hover d-block">${worker.name}</a>
                    </td>
                    <td>${worker.phone}</td>
                    <td class="p-0 position-relative w-10r">
                        <button class="btn btn-danger w-100 rounded-0 h-100 position-absolute" type="button" data-temp-elem-id="${worker.id}">Убрать</button>
                    </td>
                </tr>
            `
            $('#timetable_workers_tbody').append(row);
        }

    })
})

/***/ }),

/***/ "./src/js/admin/upload_img.js":
/*!************************************!*\
  !*** ./src/js/admin/upload_img.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function(){
    $('#edit_main_info_form').on('click', '.upload_img_button', function(){
        $(this).siblings('.upload_img_input').trigger('click');     // при клике вызываем скрытый загрузчик файлов
    });

    $('#accordion_body_images').on('click', '.upload_new_img_button', function(){
        $('#id_form-__prefix__-path').trigger('click');             // при клике вызываем скрытый загрузчик файлов
    });

    $('#edit_main_info_form').on('change', '.upload_img_input', function(){
        const file = $(this).get(0).files[0];                          // получаем загруженный файй
        const input = $(this);

        var is_new_img = false;                                         // флаг, загружаем мы новую картинки или редактируем существующую

        if ($(this).closest('[data-empty-container]').length) is_new_img = true;    // если для пустого 'контейнера', то новая

        if(file){
            const img_elem = $(this).siblings('img');
            const reader = new FileReader();


            reader.onloadend = function(){
                const img_src_temp = reader.result;                            // получаем base64 картинки

                const file_ext = img_src_temp.substring("data:image/".length, img_src_temp.indexOf(";base64"))


                var img_to_resize = new Image();
                img_to_resize.src = img_src_temp;

                img_to_resize.onload = function (){
                    const resized_src = resize_image(img_to_resize, file_ext); // !!

                    img_elem.attr('src', resized_src);                          // устанавливаем img новый src

                    if (is_new_img) register_new_img();                     // если новая, то также обновляем все необходимые инпуты

                    const input_name = input.attr('name');

                    const resized_file =  base64_to_file(resized_src, file_ext); // !!
                    //$('#edit_main_info_form').trigger('file_uploaded', {[input_name]: file});   // выгружаем имя и картинку, для POST ajax запроса
                    $('#edit_main_info_form').trigger('file_uploaded', {[input_name]: resized_file});
                }


            }

            reader.readAsDataURL(file);
        }
    });

    function resize_image(image, file_ext){
        const canvas = document.createElement("canvas");
        canvas.height = 500;
        canvas.width = 500;
        const canvas_context = canvas.getContext('2d');
        canvas_context.drawImage(image, 0, 0, 500, 500);
        return canvas.toDataURL(`image/${file_ext}`);

        // var image = new Image();
        // image.src = base64;
        //
        // image.onload = function (){
        //     var canvas = document.createElement("canvas");
        //
        //     //var octx = canvas.getContext('2d')
        //
        //     canvas.getContext('2d').drawImage(image, 0, 0, 500, 500);
        //     console.log(canvas.toDataURL('image/png'))
        //     return canvas.toDataURL('image/png');
        // }
        //var canvas = document.createElement('canvas')

        // var canvas = document.createElement('canvas'),
        //             //max_size = 544,
        //             width = 500,
        //             height = 500;
        // //max_size = 544;
        // //const width = 500;
        // //const height = 500;
        //
        // canvas.width = width;
        // canvas.height = height;
        // canvas.getContext('2d').drawImage(image, 0, 0, width, height);
        // //console.log(canvas.toDataURL('image/png'))
        // return canvas.toDataURL('image/png');

        //return dataUrl;
    }

    function base64_to_file(base64, file_ext){
        var BASE64_MARKER = ';base64,';

        var parts = base64.split(BASE64_MARKER);
        var contentType = parts[0].split(':')[1];
        var raw = window.atob(parts[1]);
        var rawLength = raw.length;

        var uInt8Array = new Uint8Array(rawLength);

        for (var i = 0; i < rawLength; ++i) {
            uInt8Array[i] = raw.charCodeAt(i);
        }

        return new File([uInt8Array], `uploaded_img.${file_ext}`, {type: contentType});
    }

    function register_new_img(){
        const container = $('[data-empty-container]')
        const order = $('[data-active][data-order]').length + 1;                 // получаем порядковый номер, который будет у картинки

        container.find('input[id$=order]').attr('value', order)     // устанавливаем порядковый номер
        container.attr('data-order', order)
        container.removeAttr('data-empty-container')                //  убираем признак 'пустого конрейнера (заготовки)'
        container.attr('data-active', '')

        //$('#id_form-TOTAL_FORMS').attr('value', order)              // обновляем общее кол-во форм у формсета

        const old_total_forms = $('#id_form-TOTAL_FORMS').attr('value')
        $('#id_form-TOTAL_FORMS').attr('value', parseInt(old_total_forms) + 1)

        container.removeClass('d-none')                             // отображаем елемент

        const regex = RegExp('__prefix__', 'g')

        const new_img_number = $('[data-order]').length - 1;

        container.find('input').each(function (index, element){
            const new_id = $(this).attr('id').replace(regex, new_img_number)             // заменяем id и имя пустой формы на нужный
            const new_name = $(this).attr('name').replace(regex, new_img_number)
            $(this).attr('id', new_id)
            $(this).attr('name', new_name)
        });

        const new_container = create_container()                        // создаем новый пустой конейтер
        container.after(new_container);

        $('#accordion_body_images').trigger('refresh_required');
    }

    function create_container(){
        return  `
            <div class="col-lg-4 col-sm-6 col-12 mb-4 d-none" data-empty-container>
                <div class="w-100">
                    <div class="img_wrapper">

                        <img src="" alt="Доп. фото" class="img-fluid w-100 img rounded">

                        <button class="btn open_img btn-dark" type="button" data-bs-toggle="modal" data-bs-target="#show_img_modal">
                            <i class="fa-solid fa-up-right-and-down-left-from-center"></i>
                        </button>

                        <button class="btn btn-primary update_img w-10r upload_img_button" type="button">
                            <i class="fa-solid fa-arrow-up-from-bracket"></i>
                            Обновить
                        </button>

                        <button class="btn btn-danger delete_img w-10r" type="button">
                            <i class="fa-solid fa-xmark"></i>
                            Удалить
                        </button>

                        <input type="number" name="form-__prefix__-order" class="d-none" id="id_form-__prefix__-order">
                        <input type="file" name="form-__prefix__-path" class="upload_img_input d-none" accept="image/png, image/jpeg, image/jpg" id="id_form-__prefix__-path">
                        <input type="hidden" name="form-__prefix__-id" id="id_form-__prefix__-id">

                    </div>
                </div>

                <div class="mt-2 text-center">
                    <i class="fa-solid fa-arrow-left fs-2 move_prev" role="button"></i>
                    <i class="fa-solid fa-arrow-right fs-2 ms-5 move_next" role="button"></i>
                </div>

            </div>
        `
    }

})

/***/ }),

/***/ "./src/js/common/evo-calendar/evo-calendar.js":
/*!****************************************************!*\
  !*** ./src/js/common/evo-calendar/evo-calendar.js ***!
  \****************************************************/
/***/ ((module, exports, __webpack_require__) => {

var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;/*!
 * Evo Calendar - Simple and Modern-looking Event Calendar Plugin
 *
 * Licensed under the MIT License
 * 
 * Version: 1.1.3
 * Author: Edlyn Villegas
 * Docs: https://edlynvillegas.github.com/evo-calendar
 * Repo: https://github.com/edlynvillegas/evo-calendar
 * Issues: https://github.com/edlynvillegas/evo-calendar/issues
 * 
 */

;(function(factory) {
    'use strict';
    if (true) {
        !(__WEBPACK_AMD_DEFINE_ARRAY__ = [__webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js")], __WEBPACK_AMD_DEFINE_FACTORY__ = (factory),
		__WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ?
		(__WEBPACK_AMD_DEFINE_FACTORY__.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__)) : __WEBPACK_AMD_DEFINE_FACTORY__),
		__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
    } else {}

}(function($) {
    'use strict';
    var EvoCalendar = window.EvoCalendar || {};
    
    EvoCalendar = (function() {
        var instanceUid = 0;
        function EvoCalendar(element, settings) {
            var _ = this;
            _.defaults = {
                theme: null,
                format: 'mm/dd/yyyy',
                titleFormat: 'MM yyyy',
                eventHeaderFormat: 'MM d, yyyy',
                firstDayOfWeek: 0,
                language: 'en',
                todayHighlight: false,
                sidebarDisplayDefault: true,
                sidebarToggler: true,
                eventDisplayDefault: true,
                eventListToggler: true,
                calendarEvents: null
            };
            _.options = $.extend({}, _.defaults, settings);

            _.initials = {
                default_class: $(element)[0].classList.value,
                validParts: /dd?|DD?|mm?|MM?|yy(?:yy)?/g,
                dates: {
                    en: {
                        days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                        daysShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
                        daysMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
                        months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                        monthsShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                        noEventForToday: "No event for today.. so take a rest! :)",
                        noEventForThisDay: "No event for this day.. so take a rest! :)",
                        previousYearText: "Previous year",
                        nextYearText: "Next year",
                        closeSidebarText: "Close sidebar",
                        closeEventListText: "Close event list"
                    },
                    ru: {
                        days: ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четвернг", "Пятница", "Суббота"],
                        daysShort: ["ВС", "ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ"],
                        daysMin: ["ВС", "ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ"],
                        months: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрт", "Ноябрь", "Декабрь"],
                        monthsShort: ["Янв", "Фев", "Март", "Апр", "Май", "Июнь", "Июль", "Авг", "Сент", "Окт", "Нояб", "Дек"],
                        noEventForToday: "На эту дату ничего нет",
                        noEventForThisDay: "На эту дату ничего нет",
                        previousYearText: "Предыдущий год",
                        nextYearText: "Следующий год",
                        closeSidebarText: "Закрыть месяца",
                        closeEventListText: "Закрть время"
                    },
                    es: {
                        days: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
                        daysShort: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"],
                        daysMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sa"],
                        months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
                        monthsShort: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
                        noEventForToday: "No hay evento para hoy.. ¡así que descanse! :)",
                        noEventForThisDay: "Ningún evento para este día.. ¡así que descanse! :)",
                        previousYearText: "Año anterior",
                        nextYearText: "El próximo año",
                        closeSidebarText: "Cerrar la barra lateral",
                        closeEventListText: "Cerrar la lista de eventos"
                    },
                    de: {
                        days: ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"],
                        daysShort: ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"],
                        daysMin: ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"],
                        months: ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
                        monthsShort: ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"],
                        noEventForToday: "Keine Veranstaltung für heute.. also ruhen Sie sich aus! :)",
                        noEventForThisDay: "Keine Veranstaltung für diesen Tag.. also ruhen Sie sich aus! :)",
                        previousYearText: "Vorheriges Jahr",
                        nextYearText: "Nächstes Jahr",
                        closeSidebarText: "Schließen Sie die Seitenleiste",
                        closeEventListText: "Schließen Sie die Ereignisliste"
                    },
                    pt: {
                        days: ["Domingo", "Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado"],
                        daysShort: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"],
                        daysMin: ["Do", "2a", "3a", "4a", "5a", "6a", "Sa"],
                        months: ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
                        monthsShort: ["Jan", "Feb", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"],
                        noEventForToday: "Nenhum evento para hoje.. então descanse! :)",
                        noEventForThisDay: "Nenhum evento para este dia.. então descanse! :)",
                        previousYearText: "Ano anterior",
                        nextYearText: "Próximo ano",
                        closeSidebarText: "Feche a barra lateral",
                        closeEventListText: "Feche a lista de eventos"
                    },
                    fr: {
                        days: ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"],
                        daysShort: ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"],
                        daysMin: ["Di", "Lu", "Ma", "Me", "Je", "Ve", "Sa"],
                        months: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
                        monthsShort: ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"],
                        noEventForToday: "Rien pour aujourd'hui... Belle journée :)",
                        noEventForThisDay: "Rien pour ce jour-ci... Profite de te réposer :)",
                        previousYearText: "Année précédente",
                        nextYearText: "L'année prochaine",
                        closeSidebarText: "Fermez la barre latérale",
                        closeEventListText: "Fermer la liste des événements"
                    },
                    nl: {
                        days: ["Zondag", "Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag"],
                        daysShort: ["Zon", "Maan", "Din", "Woe", "Don", "Vrij", "Zat"],
                        daysMin: ["Zo", "Ma", "Di", "Wo", "Do", "Vr", "Za"],
                        months: ["Januari", "Februari", "Maart", "April", "Mei", "Juni", "Juli", "Augustus", "September", "Oktober", "November", "December"],
                        monthsShort: ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"],
                        noEventForToday: "Geen event voor vandaag.. dus rust even uit! :)",
                        noEventForThisDay: "Geen event voor deze dag.. dus rust even uit! :)",
                        previousYearText: "Vorig jaar",
                        nextYearText: "Volgend jaar",
                        closeSidebarText: "Sluit de zijbalk",
                        closeEventListText: "Sluit de event lijst"
                    }
                }
            }
            _.initials.weekends = {
                sun: _.initials.dates[_.options.language].daysShort[0],
                sat: _.initials.dates[_.options.language].daysShort[6]
            }


            // Format Calendar Events into selected format
            if(_.options.calendarEvents != null) {
                for(var i=0; i < _.options.calendarEvents.length; i++) {
                    // If event doesn't have an id, throw an error message
                    if(!_.options.calendarEvents[i].id) {
                        console.log("%c Event named: \""+_.options.calendarEvents[i].name+"\" doesn't have a unique ID ", "color:white;font-weight:bold;background-color:#e21d1d;");
                    }
                    if(_.isValidDate(_.options.calendarEvents[i].date)) {
                        _.options.calendarEvents[i].date = _.formatDate(_.options.calendarEvents[i].date, _.options.format)
                    }
                }
            }

            // Global variables
            _.startingDay = null;
            _.monthLength = null;
            _.windowW = $(window).width();
            
            // CURRENT
            _.$current = {
                month: (isNaN(this.month) || this.month == null) ? new Date().getMonth() : this.month,
                year: (isNaN(this.year) || this.year == null) ? new Date().getFullYear() : this.year,
                date: _.formatDate(_.initials.dates[_.defaults.language].months[new Date().getMonth()]+' '+new Date().getDate()+' '+ new Date().getFullYear(), _.options.format)
            }

            // ACTIVE
            _.$active = {
                month: _.$current.month,
                year: _.$current.year,
                date: _.$current.date,
                event_date: _.$current.date,
                events: []
            }

            // LABELS
            _.$label = {
                days: [],
                months: _.initials.dates[_.defaults.language].months,
                days_in_month: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            }

            // HTML Markups (template)
            _.$markups = {
                calendarHTML: '',
                mainHTML: '',
                sidebarHTML: '',
                eventHTML: ''
            }
            // HTML DOM elements
            _.$elements = {
                calendarEl: $(element),
                innerEl: null,
                sidebarEl: null,
                eventEl: null,

                sidebarToggler: null,
                eventListToggler: null,

                activeDayEl: null,
                activeMonthEl: null,
                activeYearEl: null
            }
            _.$breakpoints = {
                tablet: 768,
                mobile: 425
            }
            _.$UI = {
                hasSidebar: true,
                hasEvent: true
            }

            _.formatDate = $.proxy(_.formatDate, _);
            _.selectDate = $.proxy(_.selectDate, _);
            _.selectMonth = $.proxy(_.selectMonth, _);
            _.selectYear = $.proxy(_.selectYear, _);
            _.selectEvent = $.proxy(_.selectEvent, _);
            _.toggleSidebar = $.proxy(_.toggleSidebar, _);
            _.toggleEventList = $.proxy(_.toggleEventList, _);
            
            _.instanceUid = instanceUid++;

            _.init(true);
        }

        return EvoCalendar;

    }());

    // v1.0.0 - Initialize plugin
    EvoCalendar.prototype.init = function(init) {
        var _ = this;
        
        if (!$(_.$elements.calendarEl).hasClass('calendar-initialized')) {
            $(_.$elements.calendarEl).addClass('evo-calendar calendar-initialized');
            if (_.windowW <= _.$breakpoints.tablet) { // tablet/mobile
                _.toggleSidebar(false);
                _.toggleEventList(false);
            } else {
                if (!_.options.sidebarDisplayDefault) _.toggleSidebar(false);
                else _.toggleSidebar(true);

                if (!_.options.eventDisplayDefault) _.toggleEventList(false);
                else _.toggleEventList(true);
            }
            if (_.options.theme) _.setTheme(_.options.theme); // set calendar theme
            _.buildTheBones(); // start building the calendar components
        }
    };
    // v1.0.0 - Destroy plugin
    EvoCalendar.prototype.destroy = function() {
        var _ = this;
        // code here
        _.destroyEventListener();
        if (_.$elements.calendarEl) {
            _.$elements.calendarEl.removeClass('calendar-initialized');
            _.$elements.calendarEl.removeClass('evo-calendar');
            _.$elements.calendarEl.removeClass('sidebar-hide');
            _.$elements.calendarEl.removeClass('event-hide');
        }
        _.$elements.calendarEl.empty();
        _.$elements.calendarEl.attr('class', _.initials.default_class);
        $(_.$elements.calendarEl).trigger("destroy", [_])
    }

    // v1.0.0 - Limit title (...)
    EvoCalendar.prototype.limitTitle = function(title, limit) {
        var newTitle = [];
        limit = limit === undefined ? 18 : limit;
        if ((title).split(' ').join('').length > limit) {
            var t = title.split(' ');
            for (var i=0; i<t.length; i++) {
                if (t[i].length + newTitle.join('').length <= limit) {
                    newTitle.push(t[i])
                }
            }
            return newTitle.join(' ') + '...'
        }
        return title;
    }

    // v1.1.2 - Check and filter strings
    EvoCalendar.prototype.stringCheck = function(d) {
        return d.replace(/[^\w]/g, '\\$&');
    }
            
    // v1.0.0 - Parse format (date)
    EvoCalendar.prototype.parseFormat = function(format) {
        var _ = this;
        if (typeof format.toValue === 'function' && typeof format.toDisplay === 'function')
            return format;
        // IE treats \0 as a string end in inputs (truncating the value),
        // so it's a bad format delimiter, anyway
        var separators = format.replace(_.initials.validParts, '\0').split('\0'),
            parts = format.match(_.initials.validParts);
        if (!separators || !separators.length || !parts || parts.length === 0){
            console.log("%c Invalid date format ", "color:white;font-weight:bold;background-color:#e21d1d;");
        }
        return {separators: separators, parts: parts};
    };
    
    // v1.0.0 - Format date
    EvoCalendar.prototype.formatDate = function(date, format, language) {
        var _ = this;
        if (!date)
            return '';
        language = language ? language : _.defaults.language
        if (typeof format === 'string')
            format = _.parseFormat(format);
        if (format.toDisplay)
            return format.toDisplay(date, format, language);

        var ndate = new Date(date);
        // if (!_.isValidDate(ndate)) { // test
        //     ndate = new Date(date.replace(/-/g, '/'))
        // }
        
        var val = {
            d: ndate.getDate(),
            D: _.initials.dates[language].daysShort[ndate.getDay()],
            DD: _.initials.dates[language].days[ndate.getDay()],
            m: ndate.getMonth() + 1,
            M: _.initials.dates[language].monthsShort[ndate.getMonth()],
            MM: _.initials.dates[language].months[ndate.getMonth()],
            yy: ndate.getFullYear().toString().substring(2),
            yyyy: ndate.getFullYear()
        };
        
        val.dd = (val.d < 10 ? '0' : '') + val.d;
        val.mm = (val.m < 10 ? '0' : '') + val.m;
        date = [];
        var seps = $.extend([], format.separators);
        for (var i=0, cnt = format.parts.length; i <= cnt; i++){
            if (seps.length)
                date.push(seps.shift());
            date.push(val[format.parts[i]]);
        }
        return date.join('');
    };

    // v1.0.0 - Get dates between two dates
    EvoCalendar.prototype.getBetweenDates = function(dates) {
        var _ = this, betweenDates = [];
        for (var x = 0; x < _.monthLength; x++) {
            var active_date = _.formatDate(_.$label.months[_.$active.month] +' '+ (x + 1) +' '+ _.$active.year, _.options.format);
            if (_.isBetweenDates(active_date, dates)) {
                betweenDates.push(active_date);
            }
        }
        return betweenDates;
    };

    // v1.0.0 - Check if date is between the passed calendar date 
    EvoCalendar.prototype.isBetweenDates = function(active_date, dates) {
        var sd, ed;
        if (dates instanceof Array) {
            sd = new Date(dates[0]);
            ed = new Date(dates[1]);
        } else {
            sd = new Date(dates);
            ed = new Date(dates);
        }
        if (sd <= new Date(active_date) && ed >= new Date(active_date)) {
            return true;
        }
        return false;
    }
    
    // v1.0.0 - Check if event has the same event type in the same date
    EvoCalendar.prototype.hasSameDayEventType = function(date, type) {
        var _ = this, eventLength = 0;

        for (var i = 0; i < _.options.calendarEvents.length; i++) {
            if (_.options.calendarEvents[i].date instanceof Array) {
                var arr = _.getBetweenDates(_.options.calendarEvents[i].date);
                for (var x = 0; x < arr.length; x++) {
                    if(date === arr[x] && type === _.options.calendarEvents[i].type) {
                        eventLength++;
                    }
                }
            } else {
                if(date === _.options.calendarEvents[i].date && type === _.options.calendarEvents[i].type) {
                    eventLength++;
                }
            }
        }

        if (eventLength > 0) {
            return true;
        }
        return false;
    }
    
    // v1.0.0 - Set calendar theme
    EvoCalendar.prototype.setTheme = function(themeName) {
        var _ = this;
        var prevTheme = _.options.theme;
        _.options.theme = themeName.toLowerCase().split(' ').join('-');

        if (_.options.theme) $(_.$elements.calendarEl).removeClass(prevTheme);
        if (_.options.theme !== 'default') $(_.$elements.calendarEl).addClass(_.options.theme);
    }

    // v1.0.0 - Called in every resize
    EvoCalendar.prototype.resize = function() {
        var _ = this;
        _.windowW = $(window).width();

        if (_.windowW <= _.$breakpoints.tablet) { // tablet
            _.toggleSidebar(false);
            _.toggleEventList(false);

            if (_.windowW <= _.$breakpoints.mobile) { // mobile
                $(window)
                    .off('click.evocalendar.evo-' + _.instanceUid)
            } else {
                $(window)
                    .on('click.evocalendar.evo-' + _.instanceUid, $.proxy(_.toggleOutside, _));
            }
        } else {
            if (!_.options.sidebarDisplayDefault) _.toggleSidebar(false);
            else _.toggleSidebar(true);

            if (!_.options.eventDisplayDefault) _.toggleEventList(false);
            else _.toggleEventList(true);
            
            $(window)
                .off('click.evocalendar.evo-' + _.instanceUid);
        }
    }

    // v1.0.0 - Initialize event listeners
    EvoCalendar.prototype.initEventListener = function() {
        var _ = this;

        // resize
        $(window)
            .off('resize.evocalendar.evo-' + _.instanceUid)
            .on('resize.evocalendar.evo-' + _.instanceUid, $.proxy(_.resize, _));

        // IF sidebarToggler: set event listener: toggleSidebar
        if(_.options.sidebarToggler) {
            _.$elements.sidebarToggler
            .off('click.evocalendar')
            .on('click.evocalendar', _.toggleSidebar);
        }
        
        // IF eventListToggler: set event listener: toggleEventList
        if(_.options.eventListToggler) {
            _.$elements.eventListToggler
            .off('click.evocalendar')
            .on('click.evocalendar', _.toggleEventList);
        }

        // set event listener for each month
        _.$elements.sidebarEl.find('[data-month-val]')
        .off('click.evocalendar')
        .on('click.evocalendar', _.selectMonth);

        // set event listener for year
        _.$elements.sidebarEl.find('[data-year-val]')
        .off('click.evocalendar')
        .on('click.evocalendar', _.selectYear);

        // set event listener for every event listed
        _.$elements.eventEl.find('[data-event-index]')
        .off('click.evocalendar')
        .on('click.evocalendar', _.selectEvent);
    };
    
    // v1.0.0 - Destroy event listeners
    EvoCalendar.prototype.destroyEventListener = function() {
        var _ = this;
        
        $(window).off('resize.evocalendar.evo-' + _.instanceUid);
        $(window).off('click.evocalendar.evo-' + _.instanceUid);
        
        // IF sidebarToggler: remove event listener: toggleSidebar
        if(_.options.sidebarToggler) {
            _.$elements.sidebarToggler
            .off('click.evocalendar');
        }
        
        // IF eventListToggler: remove event listener: toggleEventList
        if(_.options.eventListToggler) {
            _.$elements.eventListToggler
            .off('click.evocalendar');
        }

        // remove event listener for each day
        _.$elements.innerEl.find('.calendar-day').children()
        .off('click.evocalendar')

        // remove event listener for each month
        _.$elements.sidebarEl.find('[data-month-val]')
        .off('click.evocalendar');

        // remove event listener for year
        _.$elements.sidebarEl.find('[data-year-val]')
        .off('click.evocalendar');

        // remove event listener for every event listed
        _.$elements.eventEl.find('[data-event-index]')
        .off('click.evocalendar');
    };
    
    // v1.0.0 - Calculate days (incl. monthLength, startingDays based on :firstDayOfWeekName)
    EvoCalendar.prototype.calculateDays = function() {
        var _ = this, nameDays, weekStart, firstDay;
        _.monthLength = _.$label.days_in_month[_.$active.month]; // find number of days in month
        if (_.$active.month == 1) { // compensate for leap year - february only!
            if((_.$active.year % 4 == 0 && _.$active.year % 100 != 0) || _.$active.year % 400 == 0){
                _.monthLength = 29;
            }
        }
        nameDays = _.initials.dates[_.options.language].daysShort;
        weekStart = _.options.firstDayOfWeek;
        
        while (_.$label.days.length < nameDays.length) {
            if (weekStart == nameDays.length) {
                weekStart=0;
            }
            _.$label.days.push(nameDays[weekStart]);
            weekStart++;
        }
        firstDay = new Date(_.$active.year, _.$active.month).getDay() - weekStart;
        _.startingDay = firstDay < 0 ? (_.$label.days.length + firstDay) : firstDay;
    }

    // v1.0.0 - Build the bones! (incl. sidebar, inner, events), called once in every initialization
    EvoCalendar.prototype.buildTheBones = function() {
        var _ = this;
        _.calculateDays();
        
        if (!_.$elements.calendarEl.html()) {
            var markup;

            // --- BUILDING MARKUP BEGINS --- //

            // sidebar
            markup = '<div class="calendar-sidebar">'+
                        '<div class="calendar-year">'+
                        '<button class="icon-button" role="button" data-year-val="prev" title="'+_.initials.dates[_.options.language].previousYearText+'">'+
                                '<span class="chevron-arrow-left"></span>'+
                            '</button>'+
                            '&nbsp;<p></p>&nbsp;'+
                            '<button class="icon-button" role="button" data-year-val="next" title="'+_.initials.dates[_.options.language].nextYearText+'">'+
                                '<span class="chevron-arrow-right"></span>'+
                            '</button>'+
                        '</div><div class="month-list">'+
                        '<ul class="calendar-months">';
                            for(var i = 0; i < _.$label.months.length; i++) {
                                markup += '<li class="month" role="button" data-month-val="'+i+'">'+_.initials.dates[_.options.language].months[i]+'</li>';
                            }
                        markup += '</ul>';
            markup += '</div></div>';
        
            // inner
            markup += '<div class="calendar-inner">'+
                            '<table class="calendar-table">'+
                                '<tr><th colspan="7"></th></tr>'+
                                '<tr class="calendar-header">';
                                for(var i = 0; i < _.$label.days.length; i++ ){
                                    var headerClass = "calendar-header-day";
                                    if (_.$label.days[i] === _.initials.weekends.sat || _.$label.days[i] === _.initials.weekends.sun) {
                                        headerClass += ' --weekend';
                                    }
                                    markup += '<td class="'+headerClass+'">'+_.$label.days[i]+'</td>';
                                }
                                markup += '</tr></table>'+
                        '</div>';

            // events
            markup += '<div class="calendar-events">'+
                            '<div class="event-header"><p></p></div>'+
                            '<div class="event-list"></div>'+
                        '</div>';

            // --- Finally, build it now! --- //
            _.$elements.calendarEl.html(markup);

            if (!_.$elements.sidebarEl) _.$elements.sidebarEl = $(_.$elements.calendarEl).find('.calendar-sidebar');
            if (!_.$elements.innerEl) _.$elements.innerEl = $(_.$elements.calendarEl).find('.calendar-inner');
            if (!_.$elements.eventEl) _.$elements.eventEl = $(_.$elements.calendarEl).find('.calendar-events');

            // if: _.options.sidebarToggler
            if(_.options.sidebarToggler) {
                $(_.$elements.sidebarEl).append('<span id="sidebarToggler" role="button" aria-pressed title="'+_.initials.dates[_.options.language].closeSidebarText+'"><button class="icon-button"><span class="bars"></span></button></span>');
                if(!_.$elements.sidebarToggler) _.$elements.sidebarToggler = $(_.$elements.sidebarEl).find('span#sidebarToggler');
            }
            if(_.options.eventListToggler) {
                $(_.$elements.calendarEl).append('<span id="eventListToggler" role="button" aria-pressed title="'+_.initials.dates[_.options.language].closeEventListText+'"><button class="icon-button"><span class="chevron-arrow-right"></span></button></span>');
                if(!_.$elements.eventListToggler) _.$elements.eventListToggler = $(_.$elements.calendarEl).find('span#eventListToggler');
            }
        }

        _.buildSidebarYear();
        _.buildSidebarMonths();
        _.buildCalendar();
        _.buildEventList();
        _.initEventListener(); // test

        _.resize();
    }

    // v1.0.0 - Build Event: Event list
    EvoCalendar.prototype.buildEventList = function() {
        var _ = this, markup, hasEventToday = false;
        
        _.$active.events = [];
        // Event date
        var title = _.formatDate(_.$active.date, _.options.eventHeaderFormat, _.options.language);
        _.$elements.eventEl.find('.event-header > p').text(title);
        // Event list
        var eventListEl = _.$elements.eventEl.find('.event-list');
        // Clear event list item(s)
        if (eventListEl.children().length > 0) eventListEl.empty();
        if (_.options.calendarEvents) {
            for (var i = 0; i < _.options.calendarEvents.length; i++) {
                if(_.isBetweenDates(_.$active.date, _.options.calendarEvents[i].date)) {
                    eventAdder(_.options.calendarEvents[i])
                }
                else if (_.options.calendarEvents[i].everyYear) {
                    var d = new Date(_.$active.date).getMonth() + 1 + ' ' + new Date(_.$active.date).getDate();
                    var dd = new Date(_.options.calendarEvents[i].date).getMonth() + 1 + ' ' + new Date(_.options.calendarEvents[i].date).getDate();
                    // var dates = [_.formatDate(_.options.calendarEvents[i].date[0], 'mm/dd'), _.formatDate(_.options.calendarEvents[i].date[1], 'mm/dd')];

                    if(d==dd) {
                        eventAdder(_.options.calendarEvents[i])
                    }
                }
            };
        }
        function eventAdder(event) {
            hasEventToday = true;
            _.addEventList(event)
        }
        // IF: no event for the selected date
        if(!hasEventToday) {
            markup = '<div class="event-empty">';
            if (_.$active.date === _.$current.date) {
                markup += '<p>'+_.initials.dates[_.options.language].noEventForToday+'</p>';
            } else {
                markup += '<p>'+_.initials.dates[_.options.language].noEventForThisDay+'</p>';
            }
            markup += '</div>';
        }
        eventListEl.append(markup)
    }

    // v1.0.0 - Add single event to event list
    EvoCalendar.prototype.addEventList = function(event_data) {
        var _ = this, markup;
        var eventListEl = _.$elements.eventEl.find('.event-list');
        if (eventListEl.find('[data-event-index]').length === 0) eventListEl.empty();
        _.$active.events.push(event_data);
        markup = '<div class="event-container" role="button" data-event-index="'+(event_data.id)+'">';
        markup += '<div class="event-icon"><div class="event-bullet-'+event_data.type+'"';
        if (event_data.color) {
            markup += 'style="background-color:'+event_data.color+'"'
        }
        markup += '></div></div><div class="event-info"><p class="event-title">'+_.limitTitle(event_data.name);
        if (event_data.badge) markup += '<span>'+event_data.badge+'</span>';
        markup += '</p>'
        if (event_data.description) markup += '<p class="event-desc">'+event_data.description+'</p>';
        markup += '</div>';
        markup += '</div>';
        eventListEl.append(markup);

        _.$elements.eventEl.find('[data-event-index="'+(event_data.id)+'"]')
        .off('click.evocalendar')
        .on('click.evocalendar', _.selectEvent);
    }
    // v1.0.0 - Remove single event to event list
    EvoCalendar.prototype.removeEventList = function(event_data) {
        var _ = this, markup;
        var eventListEl = _.$elements.eventEl.find('.event-list');
        if (eventListEl.find('[data-event-index="'+event_data+'"]').length === 0) return; // event not in active events
        eventListEl.find('[data-event-index="'+event_data+'"]').remove();
        if (eventListEl.find('[data-event-index]').length === 0) {
            eventListEl.empty();
            if (_.$active.date === _.$current.date) {
                markup += '<p>'+_.initials.dates[_.options.language].noEventForToday+'</p>';
            } else {
                markup += '<p>'+_.initials.dates[_.options.language].noEventForThisDay+'</p>';
            }
            eventListEl.append(markup)
        }
    }
    
    // v1.0.0 - Build Sidebar: Year text
    EvoCalendar.prototype.buildSidebarYear = function() {
        var _ = this;
        
        _.$elements.sidebarEl.find('.calendar-year > p').text(_.$active.year);
    }

    // v1.0.0 - Build Sidebar: Months list text
    EvoCalendar.prototype.buildSidebarMonths = function() {
        var _ = this;
        
        _.$elements.sidebarEl.find('.calendar-months > [data-month-val]').removeClass('active-month');
        _.$elements.sidebarEl.find('.calendar-months > [data-month-val="'+_.$active.month+'"]').addClass('active-month');
    }

    // v1.0.0 - Build Calendar: Title, Days
    EvoCalendar.prototype.buildCalendar = function() {
        var _ = this, markup, title;
        
        _.calculateDays();

        title = _.formatDate(new Date(_.$label.months[_.$active.month] +' 1 '+ _.$active.year), _.options.titleFormat, _.options.language);
        _.$elements.innerEl.find('.calendar-table th').text(title);

        _.$elements.innerEl.find('.calendar-body').remove(); // Clear days
        
        markup += '<tr class="calendar-body">';
                    var day = 1;
                    for (var i = 0; i < 9; i++) { // this loop is for is weeks (rows)
                        for (var j = 0; j < _.$label.days.length; j++) { // this loop is for weekdays (cells)
                            if (day <= _.monthLength && (i > 0 || j >= _.startingDay)) {
                                var dayClass = "calendar-day";
                                if (_.$label.days[j] === _.initials.weekends.sat || _.$label.days[j] === _.initials.weekends.sun) {
                                    dayClass += ' --weekend'; // add '--weekend' to sat sun
                                }
                                markup += '<td class="'+dayClass+'">';

                                var thisDay = _.formatDate(_.$label.months[_.$active.month]+' '+day+' '+_.$active.year, _.options.format);
                                markup += '<div class="day" role="button" data-date-val="'+thisDay+'">'+day+'</div>';
                                day++;
                            } else {
                                markup += '<td>';
                            }
                            markup += '</td>';
                        }
                        if (day > _.monthLength) {
                            break; // stop making rows if we've run out of days
                        } else {
                            markup += '</tr><tr class="calendar-body">'; // add if not
                        }
                    }
                    markup += '</tr>';
        _.$elements.innerEl.find('.calendar-table').append(markup);

        if(_.options.todayHighlight) {
            _.$elements.innerEl.find("[data-date-val='" + _.$current.date + "']").addClass('calendar-today');
        }
        
        // set event listener for each day
        _.$elements.innerEl.find('.calendar-day').children()
        .off('click.evocalendar')
        .on('click.evocalendar', _.selectDate)

        var selectedDate = _.$elements.innerEl.find("[data-date-val='" + _.$active.date + "']");
        
        if (selectedDate) {
            // Remove active class to all
            _.$elements.innerEl.children().removeClass('calendar-active');
            // Add active class to selected date
            selectedDate.addClass('calendar-active');
        }
        if(_.options.calendarEvents != null) { // For event indicator (dots)
            _.buildEventIndicator();
        }
    };

    // v1.0.0 - Add event indicator/s (dots)
    EvoCalendar.prototype.addEventIndicator = function(event) {
        var _ = this, htmlToAppend, thisDate;
        var event_date = event.date;
        var type = _.stringCheck(event.type);
        
        if (event_date instanceof Array) {
            if (event.everyYear) {
                for (var x=0; x<event_date.length; x++) {
                    event_date[x] = _.formatDate(new Date(event_date[x]).setFullYear(_.$active.year), _.options.format);
                }
            }
            var active_date = _.getBetweenDates(event_date);
            
            for (var i=0; i<active_date.length; i++) {
                appendDot(active_date[i]);
            }
        } else {
            if (event.everyYear) {
                event_date = _.formatDate(new Date(event_date).setFullYear(_.$active.year), _.options.format);
            }
            appendDot(event_date);
        }

        function appendDot(date) {
            thisDate = _.$elements.innerEl.find('[data-date-val="'+date+'"]');

            if (thisDate.find('span.event-indicator').length === 0) {
                thisDate.append('<span class="event-indicator"></span>');
            }
            
            if (thisDate.find('span.event-indicator > .type-bullet > .type-'+type).length === 0) {
                htmlToAppend = '<div class="type-bullet"><div ';
                
                htmlToAppend += 'class="type-'+event.type+'"'
                if (event.color) { htmlToAppend += 'style="background-color:'+event.color+'"' }
                htmlToAppend += '></div></div>';
                thisDate.find('.event-indicator').append(htmlToAppend);
            }
        }      
    };
    
    // v1.0.0 - Remove event indicator/s (dots)
    EvoCalendar.prototype.removeEventIndicator = function(event) {
        var _ = this;
        var event_date = event.date;
        var type = _.stringCheck(event.type);

        if (event_date instanceof Array) {
            var active_date = _.getBetweenDates(event_date);
            
            for (var i=0; i<active_date.length; i++) {
                removeDot(active_date[i]);
            }
        } else {
            removeDot(event_date);
        }

        function removeDot(date) {
            // Check if no '.event-indicator', 'cause nothing to remove
            if (_.$elements.innerEl.find('[data-date-val="'+date+'"] span.event-indicator').length === 0) {
                return;
            }

            // // If has no type of event, then delete 
            if (!_.hasSameDayEventType(date, type)) {
                _.$elements.innerEl.find('[data-date-val="'+date+'"] span.event-indicator > .type-bullet > .type-'+type).parent().remove();
            }
        }
    };
    
    /****************
    *    METHODS    *
    ****************/

    // v1.0.0 - Build event indicator on each date
    EvoCalendar.prototype.buildEventIndicator = function() {
        var _ = this;
        
        // prevent duplication
        _.$elements.innerEl.find('.calendar-day > day > .event-indicator').empty();
        
        for (var i = 0; i < _.options.calendarEvents.length; i++) {
            _.addEventIndicator(_.options.calendarEvents[i]);
        }
    };

    // v1.0.0 - Select event
    EvoCalendar.prototype.selectEvent = function(event) {
        var _ = this;
        var el = $(event.target).closest('.event-container');
        var id = $(el).data('eventIndex').toString();
        var index = _.options.calendarEvents.map(function (event) { return (event.id).toString() }).indexOf(id);
        var modified_event = _.options.calendarEvents[index];
        if (modified_event.date instanceof Array) {
            modified_event.dates_range = _.getBetweenDates(modified_event.date);
        }
        $(_.$elements.calendarEl).trigger("selectEvent", [_.options.calendarEvents[index]])
    }

    // v1.0.0 - Select year
    EvoCalendar.prototype.selectYear = function(event) {
        var _ = this;
        var el, yearVal;

        if (typeof event === 'string' || typeof event === 'number') {
            if ((parseInt(event)).toString().length === 4) {
                yearVal = parseInt(event);
            }
        } else {
            el = $(event.target).closest('[data-year-val]');
            yearVal = $(el).data('yearVal');
        }

        if(yearVal == "prev") {
            --_.$active.year;
        } else if (yearVal == "next") {
            ++_.$active.year;
        } else if (typeof yearVal === 'number') {
            _.$active.year = yearVal;
        }
        
        if (_.windowW <= _.$breakpoints.mobile) {
            if(_.$UI.hasSidebar) _.toggleSidebar(false);
        }
        
        $(_.$elements.calendarEl).trigger("selectYear", [_.$active.year])

        _.buildSidebarYear();
        _.buildCalendar();
    };

    // v1.0.0 - Select month
    EvoCalendar.prototype.selectMonth = function(event, additional_info = {}) {
        var _ = this;

        if (typeof event === 'string' || typeof event === 'number') {
            if (event >= 0 && event <=_.$label.months.length) {
                // if: 0-11
                _.$active.month = (event).toString();
            }
        } else {
            // if month is manually selected
            _.$active.month = $(event.currentTarget).data('monthVal');
        }
        
        _.buildSidebarMonths();
        _.buildCalendar();
        
        if (_.windowW <= _.$breakpoints.tablet) {
            if(_.$UI.hasSidebar) _.toggleSidebar(false);
        }

        // EVENT FIRED: selectMonth
        $(_.$elements.calendarEl).trigger("selectMonth", [_.initials.dates[_.options.language].months[_.$active.month], _.$active.month, additional_info])
    };

    // v1.0.0 - Select specific date
    EvoCalendar.prototype.selectDate = function(event) {
        var _ = this;
        var oldDate = _.$active.date;
        var date, year, month, activeDayEl, isSameDate;

        if (typeof event === 'string' || typeof event === 'number' || event instanceof Date) {
            date = _.formatDate(new Date(event), _.options.format)
            year = new Date(date).getFullYear();
            month = new Date(date).getMonth();
            
            if (_.$active.year !== year) _.selectYear(year);
            if (_.$active.month !== month) _.selectMonth(month);
            activeDayEl = _.$elements.innerEl.find("[data-date-val='" + date + "']");
        } else {
            activeDayEl = $(event.currentTarget);
            date = activeDayEl.data('dateVal')
        }
        isSameDate = _.$active.date === date;
        // Set new active date
        _.$active.date = date;
        _.$active.event_date = date;
        // Remove active class to all
        _.$elements.innerEl.find('[data-date-val]').removeClass('calendar-active');
        // Add active class to selected date
        activeDayEl.addClass('calendar-active');
        // Build event list if not the same date events built
        if (!isSameDate) _.buildEventList();

        // EVENT FIRED: selectDate
        $(_.$elements.calendarEl).trigger("selectDate", [_.$active.date, oldDate])
    };
    
    // v1.0.0 - Return active date
    EvoCalendar.prototype.getActiveDate = function() {
        var _ = this;
        return _.$active.date;
    }
    
    // v1.0.0 - Return active events
    EvoCalendar.prototype.getActiveEvents = function() {
        var _ = this;
        return _.$active.events;
    }

    // v1.0.0 - Hide Sidebar/Event List if clicked outside
    EvoCalendar.prototype.toggleOutside = function(event) {
        var _ = this, isInnerClicked;
        
        isInnerClicked = event.target === _.$elements.innerEl[0];

        if (_.$UI.hasSidebar && isInnerClicked) _.toggleSidebar(false);
        if (_.$UI.hasEvent && isInnerClicked) _.toggleEventList(false);
    }

    // v1.0.0 - Toggle Sidebar
    EvoCalendar.prototype.toggleSidebar = function(event) {
        var _ = this;

        if (event === undefined || event.originalEvent) {
            $(_.$elements.calendarEl).toggleClass('sidebar-hide');
            _.$UI.hasSidebar = !_.$UI.hasSidebar;
        } else {
            if(event) {
                $(_.$elements.calendarEl).removeClass('sidebar-hide');
                _.$UI.hasSidebar = true;
            } else {
                $(_.$elements.calendarEl).addClass('sidebar-hide');
                _.$UI.hasSidebar = false;
            }
        }

        if (_.windowW <= _.$breakpoints.tablet) {
            if (_.$UI.hasSidebar && _.$UI.hasEvent) _.toggleEventList();
        }
    };

    // v1.0.0 - Toggle Event list
    EvoCalendar.prototype.toggleEventList = function(event) {
        var _ = this;

        if (event === undefined || event.originalEvent) {
            $(_.$elements.calendarEl).toggleClass('event-hide');
            _.$UI.hasEvent = !_.$UI.hasEvent;
        } else {
            if(event) {
                $(_.$elements.calendarEl).removeClass('event-hide');
                _.$UI.hasEvent = true;
            } else {
                $(_.$elements.calendarEl).addClass('event-hide');
                _.$UI.hasEvent = false;
            }
        }

        if (_.windowW <= _.$breakpoints.tablet) {
            if (_.$UI.hasEvent && _.$UI.hasSidebar) _.toggleSidebar();
        }
    };

    // v1.0.0 - Add Calendar Event(s)
    EvoCalendar.prototype.addCalendarEvent = function(arr) {
        var _ = this;

        function addEvent(data) {
            if(!data.id) {
                console.log("%c Event named: \""+data.name+"\" doesn't have a unique ID ", "color:white;font-weight:bold;background-color:#e21d1d;");
            }

            if (data.date instanceof Array) {
                for (var j=0; j < data.date.length; j++) {
                    if(isDateValid(data.date[j])) {
                        data.date[j] = _.formatDate(new Date(data.date[j]), _.options.format);
                    }
                }
            } else {
                if(isDateValid(data.date)) {
                    data.date = _.formatDate(new Date(data.date), _.options.format);
                }
            }
            
            if (!_.options.calendarEvents) _.options.calendarEvents = [];
            _.options.calendarEvents.push(data);
            // add to date's indicator
            _.addEventIndicator(data);
            // add to event list IF active.event_date === data.date
            if (_.$active.event_date === data.date) _.addEventList(data);
            // _.$elements.innerEl.find("[data-date-val='" + data.date + "']")

            function isDateValid(date) {
                if(_.isValidDate(date)) {
                    return true;
                } else {
                    console.log("%c Event named: \""+data.name+"\" has invalid date ", "color:white;font-weight:bold;background-color:#e21d1d;");
                }
                return false;
            }
        }
        if (arr instanceof Array) { // Arrays of events
            for(var i=0; i < arr.length; i++) {
                addEvent(arr[i])
            }
        } else if (typeof arr === 'object') { // Single event
            addEvent(arr)
        }
    };

    // v1.0.0 - Remove Calendar Event(s)
    EvoCalendar.prototype.removeCalendarEvent = function(arr) {
        var _ = this;

        function deleteEvent(data) {


            // Array index
            var index = _.options.calendarEvents.map(function (event) { return event.id }).indexOf(data);
            
            if (index >= 0) {
                var event = _.options.calendarEvents[index];
                // Remove event from calendar events
                _.options.calendarEvents.splice(index, 1);
                // remove to event list
                _.removeEventList(data);
                // remove event indicator
                _.removeEventIndicator(event);
            } else {
                console.log("%c "+data+": ID not found ", "color:white;font-weight:bold;background-color:#e21d1d;");
            }
        }

        if (arr instanceof Array) { // Arrays of index
            if (arr.length === 0){
                for(const event of _.options.calendarEvents) {
                    deleteEvent(event.id)
                }
            }

            for(var i=0; i < arr.length; i++) {
                deleteEvent(arr[i])
            }
        } else { // Single index
            deleteEvent(arr)
        }
    };

    // v1.0.0 - Check if date is valid
    EvoCalendar.prototype.isValidDate = function(d){
        return new Date(d) && !isNaN(new Date(d).getTime());
    }

    $.fn.evoCalendar = function() {
        var _ = this,
            opt = arguments[0],
            args = Array.prototype.slice.call(arguments, 1),
            l = _.length,
            i,
            ret;
        for (i = 0; i < l; i++) {
            if (typeof opt == 'object' || typeof opt == 'undefined')
                _[i].evoCalendar = new EvoCalendar(_[i], opt);
            else
                ret = _[i].evoCalendar[opt].apply(_[i].evoCalendar, args);
            if (typeof ret != 'undefined') return ret;
        }
        return _;
    };

}));


/***/ }),

/***/ "./src/js/common/evo-calendar/evo-starter.js":
/*!***************************************************!*\
  !*** ./src/js/common/evo-calendar/evo-starter.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
// import './evo-calendar'

$(document).ready(function(){

    // const serviceEvents = [
    //     {
    //         id: "required-id-1",
    //         name: "busy",
    //         date: "2022/11/11",
    //         type: "enable",
    //         name:"15:00 - 17:00",
    //         description:"3 мест(а)"
    //     },
    // ];
    //
    // const roomEvents = [
    //     {
    //         id: "required-id-1",
    //         name: "busy",
    //         date: "2022/11/11",
    //         type: "busy",
    //     },
    //     {
    //         id: "required-id-2",
    //         name: "busy",
    //         date: "2022/11/12",
    //         type: "busy",
    //     },
    //     {
    //         id: "required-id-3",
    //         name: "busy",
    //         date: "2022/11/13",
    //         type: "busy",
    //     },
    //
    // ];


    // $('.calendar__service').evoCalendar({
    //     calendarEvents: serviceEvents,
    //
    //     format: 'yyyy/mm/dd',
    //
    //     sidebarDisplayDefault: false,
    //     sidebarToggler: true,
    //
    //     eventListToggler: false,
    //
    //     eventDisplayDefault: false,
    //
    //     language:'ru',
    //
    //     firstDayOfWeek: 1
    // });

    $('.evoCalendar').evoCalendar({
        calendarEvents: [],

        format: 'yyyy/mm/dd',

        sidebarDisplayDefault: false,
        sidebarToggler: true,

        eventDisplayDefault: false,
        eventListToggler: false,

        todayHighlight: true,

        language:'ru',

        firstDayOfWeek: 1
    });



    $('.calendar__service .calendar-events').addClass('calendar-events__required');
   
    // $('.calendar__service').on('selectMonth', function(){
    //     $(".event-indicator").each(function(){              // если на день есть событие, оказываем услугу в этот день
    //         $(this).parent().addClass('day-enable');
    //     });
    // });
    //
    // $('.calendar__room').on('selectMonth', function(){
    //     $(".event-indicator").each(function(){              // если на день есть событие, то номер занят
    //         $(this).parent().addClass('day-busy');
    //     });
    // });

    //$('.evoCalendar').evoCalendar('selectMonth', new Date().getMonth());    // выбираем текущий месяц

    // $('.calendar__room').on('selectMonth', function(){
    //     $(this).siblings('form').children('button').trigger('click')
    // });
    
});

/***/ }),

/***/ "./src/js/common/redirect.js":
/*!***********************************!*\
  !*** ./src/js/common/redirect.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
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

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/chunk loaded */
/******/ 	(() => {
/******/ 		var deferred = [];
/******/ 		__webpack_require__.O = (result, chunkIds, fn, priority) => {
/******/ 			if(chunkIds) {
/******/ 				priority = priority || 0;
/******/ 				for(var i = deferred.length; i > 0 && deferred[i - 1][2] > priority; i--) deferred[i] = deferred[i - 1];
/******/ 				deferred[i] = [chunkIds, fn, priority];
/******/ 				return;
/******/ 			}
/******/ 			var notFulfilled = Infinity;
/******/ 			for (var i = 0; i < deferred.length; i++) {
/******/ 				var [chunkIds, fn, priority] = deferred[i];
/******/ 				var fulfilled = true;
/******/ 				for (var j = 0; j < chunkIds.length; j++) {
/******/ 					if ((priority & 1 === 0 || notFulfilled >= priority) && Object.keys(__webpack_require__.O).every((key) => (__webpack_require__.O[key](chunkIds[j])))) {
/******/ 						chunkIds.splice(j--, 1);
/******/ 					} else {
/******/ 						fulfilled = false;
/******/ 						if(priority < notFulfilled) notFulfilled = priority;
/******/ 					}
/******/ 				}
/******/ 				if(fulfilled) {
/******/ 					deferred.splice(i--, 1)
/******/ 					var r = fn();
/******/ 					if (r !== undefined) result = r;
/******/ 				}
/******/ 			}
/******/ 			return result;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		// no baseURI
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"admin": 0
/******/ 		};
/******/ 		
/******/ 		// no chunk on demand loading
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		__webpack_require__.O.j = (chunkId) => (installedChunks[chunkId] === 0);
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some((id) => (installedChunks[id] !== 0))) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 			return __webpack_require__.O(result);
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunkcrystal_lake_frontend"] = self["webpackChunkcrystal_lake_frontend"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module depends on other loaded chunks and execution need to be delayed
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/scss/admin.scss")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/common/redirect.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/common/evo-calendar/evo-starter.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/common/evo-calendar/evo-calendar.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./node_modules/bootstrap/dist/js/bootstrap.bundle.min.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/show_img.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/move_img.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/upload_img.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/delete_img.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/new_offer_main_img.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/select_client.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/select_room_purchase.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/select_service_purchase.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/select_timetable.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/find_items.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/item_select.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/clean_popup.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/room_purchase_popup_open.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/service_purchase_popup_open.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/timetable_popup_open.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/add_worker_to_timetable.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/remove_worker_from_timetable.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/search_rooms.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/search_services.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/offer_ajax.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/search_tags_for_offer.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/search_services_for_worker.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/search_groups_for_worker.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/search_permissions_for_group.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/search_clients_for_order.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/search_workers_for_timetable.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/search_timetables_for_service.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/delete_additional_elem.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/edit_additional_elem.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/add_additional_elem.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/manage_purchase.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/create_same_room.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/default_set_main_info.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/manage_timetable.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/get_dates_info.js")))
/******/ 	var __webpack_exports__ = __webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js"], () => (__webpack_require__("./src/js/admin/ajax/get_service_dates_info.js")))
/******/ 	__webpack_exports__ = __webpack_require__.O(__webpack_exports__);
/******/ 	
/******/ })()
;
//# sourceMappingURL=admin-28b40f31128fa3f8de12.bundle.js.map