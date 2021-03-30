var balloons_on = false;
//Number of balloons to generate on page load
var balloons_on_load = 20;
//Variables to alter boundaries of randomness
var min_time = 125; var dev_time = 300;
var min_ms = 650; var dev_ms = 1250
//Size of padding on left and right side where balloons can't generate
var padding = 100;

$(document).ready(function(){
    console.log("balloons.js loaded successfully");

    function make_balloon() {
        //Choose random colour and create balloon of that colour
        var choice = Math.floor(Math.random() * balloon_images.length);
        var balloonHTML = '<img src="' + balloon_images[choice] +
        '" class="balloon"></img>';

        //Choose random balloon speed and horizontal position
        var left_val = (padding + Math.floor(Math.random() * (window.innerWidth - 2*padding)))
        var animation_time = min_ms + Math.floor(Math.random() * dev_ms);

        //Create balloon and animate to top of screen
        $(balloonHTML).appendTo(".main")
        .css({"left": left_val, "top": ($(window).scrollTop() + $(window).height())})
        .animate({top: "-160px"}, animation_time, function () {
        //Delete balloon when it reaches the top of screen
        if($(this).length){
            $(this).remove();
        }

        });


        //Recursively call with delay if repeating option is on
        if (balloons_on){
           //Generate random delay until next balloon (when infinitely generating)
           var delay = min_time + Math.floor(Math.random() * dev_time);
           setTimeout(make_balloon, delay);
           }


    }

    //Clicking trophy on rankings page toggles infinite balloons
    $('#trophy').click(function() {
        balloons_on = !balloons_on;
        //If balloons turned on, start generating them again
        if(balloons_on){
            make_balloon();
            console.log("Turned on balloons!");
        }
        else{
            console.log("Turned off balloons!");
        }
    });

    //Generate a number of balloons on page load with random delay between
    for (i = 0; i < balloons_on_load; i++) {
        var delay = min_time + Math.floor(Math.random() * dev_time);
        setTimeout(make_balloon, delay);
    }

})
