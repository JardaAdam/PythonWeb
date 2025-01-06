$(document).ready(function() {
    $('select.select2').each(function() {
        // Pokud má `multiple` atribut, je to multi-select
        if ($(this).attr('multiple')) {
            $(this).select2({
                closeOnSelect: false
            });
        } else {
            // Pro jednotlivé selecty tedy zavření při výběru
            $(this).select2({
                closeOnSelect: true
            });
        }
    });
});