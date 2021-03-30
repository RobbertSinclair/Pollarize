var balloons_on = false;
var balloons_on_load = 20;
var min_time = 125; var dev_time = 300;

$(document).ready(function(){
    console.log("balloons.js loaded successfully");

    function make_balloon() {

        var padding = 100;
        var min_ms = 650; var dev_ms = 1250;



        var choice = Math.floor(Math.random() * balloon_images.length);
        var balloonHTML = '<img src="' + balloon_images[choice] +
        '" class="balloon"></img>';
        var left_val = (padding + Math.floor(Math.random() * (window.innerWidth - 2*padding)))
        var animation_time = min_ms + Math.floor(Math.random() * dev_ms);

        $(balloonHTML).appendTo(".main")
        .css({"left": left_val, "top": $(window).height()})
        .animate({top: "-160px"}, animation_time, function () {
        if($(this).length){
            $(this).remove();
        }

        });

        var delay = min_time + Math.floor(Math.random() * dev_time);
        if (balloons_on){
           setTimeout(make_balloon, delay);
           }


    }

    $('#trophy').click(function() {
        balloons_on = !balloons_on;
        if(balloons_on){
            make_balloon();
            console.log("Turned on balloons!");
        }
        else{
            console.log("Turned off balloons!");
        }
    });

    for (i = 0; i < balloons_on_load; i++) {
        var delay = min_time + Math.floor(Math.random() * dev_time);
        setTimeout(make_balloon, delay);
    }

})
