$(document).ready(function () {

    // TODO: ДОБАВИТЬ АККОРДЕОН И ПРИ ЕГО ОТКРЫТИИ ВЫЗЫВАЕМ selectMonth


    $('.calendar__room').on('selectMonth', function(event, month_str, month_index, additional_info){

        if (!additional_info?.programmatically){
            $('.calendar__room').not(this).evoCalendar('selectMonth', month_index, {programmatically: true});
        }
        $(this).find('.day').first().trigger('click');

        $(this).siblings('form').children('button').first().trigger('click')
    });

    $("form[id$='_dates']").on('submit', function (event){
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
                calendar.evoCalendar.calendarEvents = []

                for (const day of response['data']){
                    calendar.evoCalendar('addCalendarEvent',
                        {
                            id: Date.now(),
                            name: "busy",
                            date: `${year}/${month}/${day}`,
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