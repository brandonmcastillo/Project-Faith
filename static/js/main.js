$(document).ready(function () {
    $(document).scroll(function () {
        var y = $(this).scrollTop();
        if (y > 0) {
            $('#about').slideDown('slow');
        } else {
            $('#about').fadeOut();
        }
    });

    $(document).scroll(function () {
        var a = $(this).scrollTop();
        if (a > 1000) {
            $('#slide-container2').slideDown('fast');
        } else {
            $('#slide-container2').fadeOut('fast');
        }
    });

    $(document).scroll(function () {
        var b = $(this).scrollTop();
        if (b > 1500) {
            $('#slide-container3').slideDown('slow');
        } else {
            $('#slide-container3').fadeOut('fast');
        }
    });
    $(document).scroll(function () {
        var b = $(this).scrollTop();
        if (b > 2100) {
            $('#slide-container4').slideDown('fast');
        } else {
            $('#slide-container4').fadeOut('fast');
        }
    });
});