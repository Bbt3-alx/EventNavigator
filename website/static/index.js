$(document).ready( function() {
    $(".search-input").on('keyUp', function() {
        var value = $(this).val().toLowerCase();
        $('.card-body').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});