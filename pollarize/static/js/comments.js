
function loadReplies(comment_id) {
    console.log("loadReplies has been run");
    $.get("/json/" + comment_id + "/child-comments", function( data ) {
        for (var i = 0; i < data.comments.length; i++) {
            var the_comment = data.comments[i];
            $("#replies-" + comment_id).append("<div class='comment' id='comment-" + the_comment.id + 
            "'><img class='mr-3 rounded-circle profile-img' alt='Profile image' src='" + the_comment.profile_image + "'/><h3>" + the_comment.submitter + "</h3><p>" + the_comment.comment + "</p></div>");
            $("#load-replies-"+ comment_id).remove();
        }
    });
}



function postComment(poll_slug, submitter) {
    var the_comment = $("#add-comment").val();
    var post_data = {
        comment: the_comment,
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
    }
    console.log(post_data.csrfmiddlewaretoken);
    $ajax({
        type: 'POST',
        url: '/json/' + poll_slug + '/comment/',
        data: post_data,
        success:function(response)
        {
            alert(response);
        },
        failure:function(response)
        {
            alert(response);
        }
    })
}