$(document).ready(function () {
    $(".delete-button").click(function () {
        if (confirm("Вы уверены, что хотите удалить файл?")) {
            $(this).closest("form").submit();
        }
        else {
            return false
        }
    });
});
