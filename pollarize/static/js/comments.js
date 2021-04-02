$(document).ready(function(){
    console.log("comments.js loaded successfully");
    $(".loading").hide();
    $(".replies").hide();
    $(".hide-replies").hide();
    $(".reply-form").hide();
    $(".hide-reply-form").hide();
    repliesResize();
    var auth;
    var username;
    $.get("/json/user/", function(data) {
        auth = data.authenticated;
        username = data.username;
        console.log(data);
    });

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
    });

    $(".submit-reply").click(function() {
        console.log($(this).attr("id") + " add reply clicked");
        var poll_slug = window.location.pathname.split("/")[1];
        var parent = $(this).attr("id").replaceAll(/\D/g, "");
        var children = parseInt($(this).attr("val"));
        postComment(poll_slug, username, children, parent); 
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
                $("#replies-" + comment_id).append("<div class='comment row' id='comment-" + the_comment.id + 
                "'><div class='col'><img class='mr-3 rounded-circle profile-img' alt='Profile image' src='" + the_comment.profile_image + "'/><h3>" + the_comment.submitter + " - " + votes_for + "</h3><p>" + the_comment.comment + "</p></div>" + 
                "<div class='col'><button id='upvote-" + the_comment.id + "'class='upvote vote-button'" +
                "onClick='addVote(1, " + the_comment.id + ", " + the_comment.votes + ")'><ion-icon name='chevron-up-outline'></ion-icon></button>" +
                "<label id='votes-" + the_comment.id + "'>" + the_comment.votes + "</label>" + 
                "<button id='downvote-" + the_comment.id + "' class='downvote vote-button' onClick='addVote(-1, " + the_comment.id + ", " + the_comment.votes + ")'><ion-icon name='chevron-down-outline'></ion-icon></button></div></div>");
                
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
                var html_string = "<div class='comment' id='comment-" + data.comment_id + "'>"
                + "<div class='row'>"
                + "<div class='col-md'>"
                + "<div id='comment_title'>"
                + "<img class='mr-3 rounded-circle profile-img' alt='Profile image' src='" + profile_pic + "' />" 
                + "<h3>" + submitter + " - " + vote_string + "</h3>"
                + "</div>"
                + "<p>" + the_comment + "</p>"; 
                
                if(parent == null) {
                    var post_comment_string = "postComment('" + poll_slug + "', \'" + submitter + "\', " + data.comment_id + ")";
                    console.log(post_comment_string);
                    
                    html_string = html_string + "<button id='load-replies-" + data.comment_id + "' class='btn btn-link orange_button load-replies' value='0' onClick='loadReplies(" + data.comment_id + ")'>Load Replies (0) &#8595;</button>"
                    + "<button id='hide-replies-" + data.comment_id + "' class='hide-replies btn btn-link orange_button' onClick='hideReplies(" + data.comment_id + ")'>Hide Replies &#8593;</button>"
                    + "<button id='add-reply-" + data.comment_id + "' class='add-reply btn btn-link grey_button' onClick='showReplyForm(" + data.comment_id + ")'>Reply</button>"
                    + "<button id='hide-reply-form-" + data.comment_id + "' class='hide-reply-form btn btn-link grey_button' onClick='hideReplyForm(" + data.comment_id + ")'>Cancel</button>"
                    + "</div>"
                    + "<div class='col-sm'>"
                    + "<button id='upvote-" + data.comment_id + "' class='upvote vote-button' onClick='addVote(1, " + data.comment_id + ", 0)'><ion-icon name='chevron-up-outline'></ion-icon></button>"
                    + "<label id='votes-" + data.comment_id + "'>0</label>"
                    + "<button id='downvote-" + data.comment_id + "' class='downvote vote-button' onClick='addVote(-1, " + data.comment_id + ", 0)'><ion-icon name='chevron-down-outline'></ion-icon></button>"
                    + "</div>"
                    + "<div class='ml-5'>"
                    + "<form id='reply-form-" + data.comment_id + "' class='ml-5 reply-form' onSubmit='return false;'>"
                    + "<div class='form-group'>"
                    + "<label for='reply-text'>Enter Reply:</label><br>"
                    + "<textarea name='reply-text' class='form-control' cols='30' rows='2' id='add-reply-text-" + data.comment_id + "'></textarea><br>"
                    + "</div>"
                    + "<button class='btn btn-link grey_button submit-reply' id='submit-reply-" + data.comment_id + "'>Submit</button>"
                    + "</form>"
                    + "</div>"
                    + "<div id='replies-" + data.comment_id + "' class='row-ml-5 replies'>"
                    + "</div>"
                    + "</div>";
                    
                    $("#submit-reply-" + parent).attr("val", children + 1);
                    $("#comments").prepend(html_string);
                    $("#replies-" + data.comment_id).hide();
                    $("#hide-replies-" + data.comment_id).hide();
                    $("#load-replies-" + data.comment_id).hide();
                    $("#reply-form-" + data.comment_id).hide();
                    $("#hide-reply-form-" + data.comment_id).hide();

                    $("#add-comment").val("");
                } else {
                    html_string = html_string + "</div></div></div>";
                    $("#replies-" + parent).prepend(html_string);
                    $("#load-replies-" + parent).html("Load Replies (" + data.children + ") &#8595;");
                    if($("#load-replies-" + parent).is(":hidden") && post_data.children == 0) {
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