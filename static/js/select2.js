// Inicializace Select2 s podporou multiple-select
$(document).ready(function() {
   $('.select2').select2({
       closeOnSelect: false  // Důležité pro multi-select
   });
});
