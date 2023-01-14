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