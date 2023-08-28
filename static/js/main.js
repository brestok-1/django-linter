$(document).ready(function () {
    $(".delete-button").click(function () {
        if (confirm("Вы уверены, что хотите удалить файл?")) {
            $(this).closest("form").submit();
        } else {
            return false
        }
    });
    $('.wrap-drag').height($('.wrap-drag').width() * 0.75);
    $(window).resize(function () {
        $('.wrap-drag').height($('.wrap-drag').width() * 0.75);
    });
    $('.wrap-loading').height($('.wrap-loading').width() * 0.6);
    $(window).resize(function () {
        $('.wrap-loading').height($('.wrap-loading').width() * 0.6);
    });
});
