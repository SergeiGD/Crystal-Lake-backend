const form_date = function(date) {
        const year = date.toISOString().substring(0,4),
            month = date.toISOString().substring(5,7),
            day = date.toISOString().substring(8,10),
            hours = date.toISOString().substring(11,13),
            minutes = date.toISOString().substring(14,16);

        return `${day}/${month}/${year} ${hours}:${minutes}`;
    }


module.exports.form_date = form_date;