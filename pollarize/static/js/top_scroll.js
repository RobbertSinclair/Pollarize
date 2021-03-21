$(document).ready(function() {
    windowResize();
    
    $(window).scroll(function() {
        var max_scroll = 100;

        if($(this).scrollTop() > max_scroll) {
            $("#back-to-top-button").show();
        } else {
            $("#back-to-top-button").hide();
        }
    });


    $(window).resize(function() {
        windowResize();
    });

    $("#back-to-top-button").click(function() {
        $("html, body").animate({scrollTop: 0}, 10);
    });

})

function windowResize() {
    var width = window.innerWidth;
    if (width < 600) {
        $("#back-to-top-button").html("Top &#8593;");
    } else {
        $("#back-to-top-button").html("Back To Top &#8593;")
    }
}