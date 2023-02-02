// import './evo-calendar'
require('./evo-calendar');
$(document).ready(function(){

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

});