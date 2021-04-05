$(document).ready(function() {
    console.log("top_scroll.js loaded successfully");
    windowResize();
    $(".back-to-top").hide();

    //Show back to top if not already at top of page
    $(window).scroll(function() {
        var max_scroll = 100;
        if($(this).scrollTop() > max_scroll) {
            $(".back-to-top").show();
        } else {
            $(".back-to-top").hide();
        }
    });


    $(window).resize(function() {
        windowResize();
    });

    $("#back-to-top-div").click(function() {
        $("html, body").animate({scrollTop: 0}, 10);
    });

})

function windowResize() {
    var width = window.innerWidth;
    if (width < 600) {
        $(".back-to-top").html("Top &#8593;");
    } else {
        $(".back-to-top").html("Back To Top &#8593;")
    }
}