$(document).ready(function() {
    $(window).scroll(function() {
        var max_scroll = 100;

        if($(this).scrollTop() > max_scroll) {
            $("#back-to-top-button").show();
        } else {
            $("#back-to-top-button").hide();
        }

        
    });

    $("#back-to-top-button").click(function() {
        $("html, body").animate({scrollTop: 0}, 10);
    });

})