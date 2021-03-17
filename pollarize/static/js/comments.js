$(document).ready(function(){
    $(".loading").hide();
    $(".replies").hide();
    $(".hide-replies").hide();
})


function loadReplies(comment_id) {
    var reply_children_count = $("#replies-" + comment_id).children().length;
    
    $("#loading-" + comment_id).show();
    if (reply_children_count == 1) {
        $.get("/json/" + comment_id + "/child-comments", function( data ) {
            for (var i = 0; i < data.comments.length; i++) {
                var the_comment = data.comments[i];
                $("#replies-" + comment_id).append("<div class='comment' id='comment-" + the_comment.id + 
                "'><img class='mr-3 rounded-circle profile-img' alt='Profile image' src='" + the_comment.profile_image + "'/><h3>" + the_comment.submitter + "</h3><p>" + the_comment.comment + "</p></div>");
                
            } 
        });
    }
    $("#load-replies-"+ comment_id).hide();
    $("#hide-replies-" + comment_id).show();
    $("#replies-" + comment_id).slideDown("slow");
    $('#loading-' + comment_id).hide();
}

function hideReplies(comment_id) {
    $("#replies-" + comment_id).slideUp("slow");
    $("#load-replies-" + comment_id).show();
    $("#hide-replies-" + comment_id).hide();
}



function postComment(poll_slug, submitter) {
    var the_comment = $("#add-comment").val();
    var post_data = {
        comment: the_comment,
        poll: poll_slug,
        submitter: submitter,
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
    }
    var the_url = '/json/add-comment/'; 
    $.ajax({
        type: 'POST',
        url: the_url,
        data: post_data,
        success:function(data)
        {
            //console.log("Success")
            var profile_pic = data.profile_image;
            $("#comments").prepend("<div class='comment' id='comment-" + data.comment_id + "' />" 
            + "<img class='mr-3 rounded-circle profile-img' alt='Profile image' src='" + profile_pic + "' />" 
            + "<h3>" + submitter + "</h3>" 
            + "<p>" + the_comment + "</p>");

            $("#add-comment").val("");

        },
        failure:function(data)
        {
            console.log("Failure")
        }
    })
}