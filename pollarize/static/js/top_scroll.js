$(document).ready(function() {
    console.log("top_scroll.js loaded successfully");
    windowResize();
    $(".back-to-top").hide();
    
    $(window).scroll(function() {
        console.log($(this).scrollTop());
        var max_scroll = 100;

        if($(this).scrollTop() > max_scroll) {
            console.log("Back To Top shows")
            $(".back-to-top").show();
        } else {
            console.log("Back to top does not show");
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