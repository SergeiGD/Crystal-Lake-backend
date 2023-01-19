const add_hours = require('../add_hours');

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