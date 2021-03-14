
function loadReplies(comment_id) {
    console.log("loadReplies has been run");
    $.get("/json/" + comment_id + "/child-comments", function( data ) {
        for (var i = 0; i < data.comments.length; i++) {
            var the_comment = data.comments[i];
            $("#replies-" + comment_id).append("<div class='comment' id='comment-" + the_comment.id + 
            "'><h3>" + the_comment.submitter + "</h3><p>" + the_comment.comment + "</p></div>");
            $("#load-replies-"+ comment_id).remove();
        }
    });
}