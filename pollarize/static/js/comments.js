$(document).ready(function(){
    $(".loading").hide();
    $(".replies").hide();
    $(".hide-replies").hide();
    $(".reply-form").hide();
    $(".hide-reply-form").hide();
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
        $("#replies-" + comment_id).slideDown("slow");
    } else {
        $("#replies-" + comment_id).slideDown("slow");
    }
    $("#load-replies-"+ comment_id).hide();
    $("#hide-replies-" + comment_id).show();
    
    $('#loading-' + comment_id).hide();
}

function hideReplies(comment_id) {
    $("#replies-" + comment_id).slideUp("slow");
    $("#load-replies-" + comment_id).show();
    $("#hide-replies-" + comment_id).hide();
}


function showReplyForm(comment_id) {
    $("#reply-form-" + comment_id).slideDown("slow");
    $("#hide-reply-form-" + comment_id).show();
    $("#add-reply-" + comment_id).hide();
    
}

function hideReplyForm(comment_id) {
    $("#reply-form-" + comment_id).slideUp("slow");
    $("#hide-reply-form-" + comment_id).hide();
    $("#add-reply-" + comment_id).show();
}



function postComment(poll_slug, submitter, children, parent) {
    console.log(parent);
    if (parent == null) {
        var the_comment = $("#add-comment").val();
    } else {
        var the_comment = $("#add-reply-text-" + parent).val();
    }
    var post_data = {
        comment: the_comment,
        poll: poll_slug,
        submitter: submitter,
        parent: parent,
        children: children,
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
    }
    console.log(post_data);
    var the_url = '/json/add-comment/'; 
    $.ajax({
        type: 'POST',
        url: the_url,
        data: post_data,
        success:function(data)
        {
            var profile_pic = data.profile_image;
            var html_string = "<div class='comment' id='comment-" + data.comment_id + "' />" 
            + "<img class='mr-3 rounded-circle profile-img' alt='Profile image' src='" + profile_pic + "' />" 
            + "<h3>" + submitter + "</h3>" 
            + "<p>" + the_comment + "</p>"; 
            
            
            if(parent == null) {
                
                $("#comments").prepend(html_string);

                $("#add-comment").val("");
            } else {
                $("#replies-" + parent).prepend(html_string);
                $("#load-replies-" + parent).html("Load Replies (" + data.children + ") &#8595;");
                $("#add-reply-text-" + parent).val("");
                $("#reply-form-" + parent).slideUp();
                $("#add-reply-" + parent).show();
                $("#hide-reply-form-" + parent).hide();

            }

        },
        failure:function(data)
        {
            console.log("Failure")
        }
    })
}

function addVote(vote_amount, comment_id, votes) {
    var post_data = {
        id: comment_id,
        votes: votes,
        vote_amount: vote_amount,
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
    }
    var the_url = "/json/add-vote/";
    $.ajax({
        type: "POST",
        url: the_url,
        data: post_data,
        success: function(data) {
            $("#votes-" + comment_id).html(data.votes);

        },
        failure: function(data) {
            console.log("Failure");
        }
    })
}