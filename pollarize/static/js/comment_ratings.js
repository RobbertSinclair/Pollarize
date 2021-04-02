$(document).ready(function(){
    console.log("comment_ratings.js loaded successfully");
    //get all comment votes
    $(".comment").each(function() {
        getRating(this)
    });

})
//Update data for poll box
function getRating(comment) {
    //get poll slug from box
    var comment_id = $(comment).attr('id').substring(8)

    //get comment rating as JSON
    $.get("/json/" + comment_id + "/rating/", function( data ) {
        if(data.vote == null){
            return;
        }
           //get total votes and percentage split
           var rating = data.vote;

           if(rating > 0){
              $("#upvote-" + comment_id).addClass("upvote-selected");
              console.log("Added upvote to comment " + comment_id);
           }
           else if(rating < 0){
              $("#downvote-" + comment_id).addClass("downvote-selected");
              console.log("Added downvote to comment " + comment_id);
           }
        });
}