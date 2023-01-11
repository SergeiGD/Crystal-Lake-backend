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

/***/ "./src/js/admin/add_worker_to_timetable.js":
/*!*************************************************!*\
  !*** ./src/js/admin/add_worker_to_timetable.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){

    $('#select_worker').on('submit', function (event, worker_id, worker_name, worker_link, additional_data){
        event.preventDefault();

        const same_elem = $('#timetable_workers_tbody').find(`[data-id="${worker_id}"]`).length

        if(same_elem){
            return
        }

        const row = `
                <tr>
                    <th scope="row">${worker_id}</th>
                    <td>
                        <a href="${worker_link}" class="link-hover d-block">${worker_name}</a>
                    </td>
                    <td>${additional_data.phone}</td>
                    <td class="p-0 position-relative w-10r">
                        <button class="btn btn-danger w-100 rounded-0 h-100 position-absolute" type="button" data-temp-elem-id="${worker_id}">Убрать</button>
                    </td>
                </tr>
            `
        $('#timetable_workers_tbody').append(row);

        $('#edit_timetable').trigger('worker_added', worker_id)

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

    $('.add_additional_form').on('submit', function (event, data){
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
/***/ ((__unused_webpack_module, __unused_webpack_exports, __webpack_require__) => {

/* provided dependency */ var $ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
$(document).ready(function (){

    $('#add_same_room').on('submit', function (event, room_id){
        event.preventDefault();

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': room_id, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
                const new_room = {id: response['data'].id}
                append_row(new_room)
            }
        });

        function append_row(room){
            const row = `
                <tr>
                    <th scope="row">${room.id}</th>
                    <td class="p-0 position-relative w-10r">
                        <button class="btn btn-danger w-100 rounded-0 h-100 position-absolute" type="button" data-id="${room.id}">Убрать</button>
                    </td>
                </tr>
            `
            $('#same_rooms_list_body').append(row);

        }

    });
})

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

    $('.delete_additional_form').on('submit', function (event, elem_id){
        const current_form = $(this);
        event.preventDefault();

        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': elem_id, 'csrfmiddlewaretoken': csrf_token},
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


        const csrf_token = $(this).find('[name=csrfmiddlewaretoken]').attr('value')

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: {'elem_id': elem_id, 'csrfmiddlewaretoken': csrf_token},
            success: function (response){
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

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            success: function (){
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
                            <button data-id="${item.id}" data-name="${item.name}" data-link="${item.link}" class="btn btn-primary w-100 rounded-0 h-100 position-absolute" data-bs-toggle="modal" data-bs-target="#room_purchase_modal" type="button">
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
$(document).ready(function (){

    $('#room_purchase_modal').on('popup_open', function (event, data){

        $('#id_purchase_id').val(data.id)
        $('#room_purchase').html(data.name).attr('href', data.link)
        const start = new Date(data.start * 1000)
        $('#id_start').val(start.toISOString().split('T')[0])
        const end = new Date(data.end * 1000)
        $('#id_end').val(end.toISOString().split('T')[0])
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

        $('#room_purchase').html(data.name).attr('href', data.link);
        $('#id_room_id').val(data.id);

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

$(document).ready(function (){

    $('#service_purchase_modal').on('popup_open', function (event, data){

        $('#id_purchase_id').val(data.id)
        $('#service_purchase').html(data.name).attr('href', data.link)
        $('#id_quantity').val(data.quantity)
        $('#id_is_paid').prop('checked', data.is_paid);
        $('#id_is_prepayment_paid').prop('checked', data.is_prepayment_paid);
        $('#id_service_id').val(data.offer_id);

        const start = new Date(data.start * 1000)
        const end = new Date(data.end * 1000)

        const day = start.toISOString().substring(0,10),
            start_time = start.toISOString().substring(11,16),
            end_time = end.toISOString().substring(11,16)

        $('#id_day').val(day)
        $('#id_time_start').val(start_time)
        $('#id_time_end').val(end_time)
        if (data.is_dynamic){
            $('.static_time_field').addClass('d-block')
            $('.dynamic_time_field').addClass('d-none')
        }
        else{
            $('#id_time_select_text').val(`${form_date.form_date(start)} - ${form_date.form_date(end)}`)

            $('.dynamic_time_field').addClass('d-block')
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
$(document).ready(function (){

    $('#manage_timetable_modal').on('popup_open', function (event, data){

        $('#id_timetable_id').val(data.id)
        const start = new Date(data.start * 1000)
        const end = new Date(data.end * 1000)
        $('#id_date').val(start.toISOString().substring(0,10))
        $('#id_start').val(start.toISOString().substring(11,16))
        $('#id_end').val(end.toISOString().substring(11,16))
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
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
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
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/scss/admin.scss")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/common/redirect.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/common/evo-calendar/evo-starter.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./node_modules/bootstrap/dist/js/bootstrap.bundle.min.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/show_img.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/move_img.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/upload_img.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/delete_img.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/new_offer_main_img.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/select_client.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/select_room_purchase.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/select_service_purchase.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/select_timetable.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/find_items.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/item_select.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/clean_popup.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/room_purchase_popup_open.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/service_purchase_popup_open.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/timetable_popup_open.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/add_worker_to_timetable.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/remove_worker_from_timetable.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/search_rooms.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/search_services.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/offer_ajax.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/search_tags_for_offer.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/search_services_for_worker.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/search_groups_for_worker.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/search_permissions_for_group.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/search_clients_for_order.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/search_workers_for_timetable.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/search_timetables_for_service.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/delete_additional_elem.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/edit_additional_elem.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/add_additional_elem.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/manage_purchase.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/create_same_room.js")))
/******/ 	__webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/default_set_main_info.js")))
/******/ 	var __webpack_exports__ = __webpack_require__.O(undefined, ["vendors-node_modules_jquery_dist_jquery_js","vendors-node_modules_bootstrap_dist_js_bootstrap_bundle_min_js","src_js_common_evo-calendar_evo-starter_js-src_js_common_redirect_js"], () => (__webpack_require__("./src/js/admin/ajax/manage_timetable.js")))
/******/ 	__webpack_exports__ = __webpack_require__.O(__webpack_exports__);
/******/ 	
/******/ })()
;
//# sourceMappingURL=admin-3cbe38b46019b87adc9f.bundle.js.map