$(document).ready(function (){

    $('#select_worker').on('submit', function (event, data){
        event.preventDefault();

        // берем data-called-by и там ищем по классу

        const called_by = $(this).attr('data-called-by')
        const workers_tbody = $(called_by).find('.timetable_workers_tbody')

        const same_elem = workers_tbody.find(`[data-temp-elem-id="${data.id}"]`).length

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
        workers_tbody.append(row);

        $(called_by).find('.workers_form').trigger('worker_added', data.id)

    });

})