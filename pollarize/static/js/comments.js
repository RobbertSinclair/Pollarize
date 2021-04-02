$(document).ready(function(){
    console.log("comments.js loaded successfully");
    $(".loading").hide();
    $(".replies").hide();
    $(".hide-replies").hide();
    $(".reply-form").hide();
    $(".hide-reply-form").hide();
    repliesResize();

    $(".load-replies").each(function() {
        var id = $(this).attr("id");
        var the_string = $(this).html();
        var reply_length = parseInt(the_string.replaceAll(/\D/g, ""), 10);
        if (reply_length == 0) {
            $("#" + id).hide();
        }
    });
    
    if(window.innerWidth <= 500) {
        $("#add-comment").attr('rows', 2);
    }

    $(window).resize(function() {
        if(window.innerWidth <= 500) {
            $("#add-comment").attr('rows', 2);
        } else {
            $("#add-comment").attr('rows', 5);
        }
        repliesResize();
    })
    
})

function repliesResize() {
    if(window.innerWidth <= 1000) {
        $(".replies").css("marginLeft", "10vw");
    } else {
        $(".replies").css("marginLeft", "4vw");
    }
}


function loadReplies(comment_id) {
    var reply_children_count = $("#replies-" + comment_id).children().length;
    $("#replies-" + comment_id).slideDown("slow");
    $("#loading-" + comment_id).show();
    if (reply_children_count == 1) {
        $.get("/json/" + comment_id + "/child-comments", function( data ) {
            console.log(data);
            for (var i = 0; i < data.comments.length; i++) {
                var the_comment = data.comments[i];
                if (the_comment.vote_option != null) {
                    var votes_for = "Voted for " + the_comment.vote_option;
                } else {
                    var votes_for = "Has not voted yet";
                }
                $("#replies-" + comment_id).append("<div class='comment row replies' id='comment-" + the_comment.id +
                "'><div class='col'><img class='mr-3 rounded-circle profile-img' alt='Profile image' src='" + the_comment.profile_image + "'/><h3>" + the_comment.submitter + " - " + votes_for + "</h3><p>" + the_comment.comment + "</p></div>" + 
                "<div class='col'><button id='upvote-" + the_comment.id + "'class='upvote vote-button'" +
                "onClick='addVote(1, " + the_comment.id + ", " + the_comment.votes + ")'><ion-icon name='chevron-up-outline'></ion-icon></button>" +
                "<label id='votes-" + the_comment.id + "'>" + the_comment.votes + "</label>" + 
                "<button id='downvote-" + the_comment.id + "' class='downvote vote-button' onClick='addVote(-1, " + the_comment.id + ", " + the_comment.votes + ")'><ion-icon name='chevron-down-outline'></ion-icon></button></div></div>");

                if (the_comment.user_vote > 0){
                    $("#upvote-" + the_comment.id).addClass("upvote-selected");
                }
                else if (the_comment.user_vote < 0){
                    $("#downvote-" + the_comment.id).addClass("downvote-selected");
                }

            }
        });
        
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
    if (the_comment != "") {
        var the_url = '/json/add-comment/'; 
        $.ajax({
            type: 'POST',
            url: the_url,
            data: post_data,
            success:function(data)
            {
                console.log(data);
                if (data.vote_option != null) {
                    var vote_string = "Voted for " + data.vote_option;
                } else {
                    var vote_string = "Has not Voted";
                }
                var profile_pic = data.profile_image;
                var html_string = "<div class='comment' id='comment-" + data.comment_id + ">"
                + "<div class='row'>"
                + "<div class='col-md'>"
                + "<div id='comment_title'>"
                + "<img class='mr-3 rounded-circle profile-img' alt='Profile image' src='" + profile_pic + "' />" 
                + "<h3>" + submitter + " - " + vote_string + "</h3>"
                + "</div>"
                + "<p>" + the_comment + "</p>"
                + "</div>"
                + "</div>"
                + "</div>"; 
                
                if(parent == null) {
                    
                    $("#comments").prepend(html_string);

                    $("#add-comment").val("");
                } else {
                    $("#replies-" + parent).prepend(html_string);
                    $("#load-replies-" + parent).html("Load Replies (" + data.children + ") &#8595;");
                    if($("#load-replies-" + parent).is(":hidden") && $("hide-replies-" + parent).is(":hidden")) {
                        $("#load-replies-" + parent).show();
                    }
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
}

function addVote(vote_amount, comment_id, votes) {
    var page_url = window.location.pathname;
    var poll_slug = page_url.split("/")[1];
    var post_data = {
        id: comment_id,
        votes: votes,
        vote_amount: vote_amount,
        poll_slug: poll_slug,
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
    }
    console.log(post_data);
    var the_url = "/json/add-comment-vote/";
    $.ajax({
        type: "POST",
        url: the_url,
        data: post_data,
        success: function(data) {
            $("#votes-" + comment_id).html(data.votes);
            console.log(data);
            if(vote_amount == 1 && !data.voted_before) {
                console.log("Upvote");
                $("#upvote-" + comment_id).addClass("upvote-selected");
            } else if (vote_amount == -1 && !data.voted_before) {
                console.log("Downvote");
                $("#downvote-" + comment_id).addClass("downvote-selected");
            } else {
                $("#upvote-" + comment_id).removeClass("upvote-selected");
                $("#downvote-" + comment_id).removeClass("downvote-selected");
            }

        },
        failure: function(data) {
            console.log("Failure");
        }
    })
}