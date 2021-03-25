$(document).ready(function(){
    console.log("homepage.js loaded successfully");

    $(".poll_box").each(function() {
    populateBox(this)
    });

})

function populateBox(box) {
    var poll_slug = $(box).attr('id').substring(5)
    console.log(poll_slug);

    $.get("/json/" + poll_slug + "/results", function( data ) {
           var total = data.votes1 + data.votes2;
           var percent1 = Math.round((data.votes1 / total) * 100);
           var percent2 = 100 - percent1;
           $(box).find('.orange_percent').html(percent1 + '%');
           $(box).find('.grey_percent').html(percent2 + '%');
           $(box).find('.box_votes').html(total + ' votes');

           var totalString;
           if(total < 1000){
            totalString = total + " votes";
           }
           else if(total < 1000000){
             totalString = (Math.round((total / 100)) / 10) + "K votes";
           } else{
             totalString = (Math.round((total / 100000)) / 10) + "M votes";
           }
           $(box).find('.box_votes').html(totalString);

           var orange_bar_start = Math.min(Math.max(percent1, 1), 99)
           console.log(orange_bar_start);
           $(box).find('.vote_bar').css("background",
           "linear-gradient(90deg, #ff9c00 " + orange_bar_start + "%, #505050 " + (orange_bar_start + 0.1) + "%)");
        });
}