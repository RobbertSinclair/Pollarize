$(document).ready(function(){
    console.log("populate_boxes.js loaded successfully");
    //populate all poll boxes
    $(".poll_box, .centre_poll_box").each(function() {
    populateBox(this)
    });

})
//Update data for poll box
function populateBox(box) {
    //get poll slug from box
    var poll_slug = $(box).attr('id').substring(5)

    //get results of poll from AJAX
    $.get("/json/" + poll_slug + "/results", function( data ) {
           //get total votes and percentage split
           var total = data.votes1 + data.votes2;
           var totalString;

           if(total == 0){
               var percent1 = "--";
               var percent2 = "--";
               totalString = "No votes"
           }
           else{
               var percent1 = Math.round((data.votes1 / total) * 100);
               var percent2 = 100 - percent1;

               //calculate vote string
               if(total == 1){
                totalString = "1 vote";
               }
               else if(total < 1000){
                totalString = total + " votes";
               }
               else if(total < 1000000){
                 //display in terms of thousands with one decimal
                 totalString = (Math.round((total / 100)) / 10) + "K votes";
               } else{
                 //display in terms of millions with one decimal
                 totalString = (Math.round((total / 100000)) / 10) + "M votes";
               }
           }

           //update percentages
           $(box).find('.orange_percent').html(percent1 + '%');
           $(box).find('.grey_percent').html(percent2 + '%');

           //set vote string
           $(box).find('.box_votes').html(totalString);

           //set orange percentage to between 1 and 99 percent to guarantee 2 colours
           var orange_bar_start = Math.min(Math.max(percent1, 1), 99)
           //change vote bar to match percentages
           $(box).find('.vote_bar').css("background",
           "linear-gradient(90deg, #ff9c00 " + orange_bar_start + "%, #505050 " + (orange_bar_start + 0.1) + "%)");

           //log progress
           console.log("Updated data for question " + poll_slug)
        });
}