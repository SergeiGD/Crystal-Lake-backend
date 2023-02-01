 const add_hours = function(date, hours){
     date.setTime(date.getTime() + (hours * 60 * 60 * 1000))
     return date
}

module.exports.add_hours = add_hours;