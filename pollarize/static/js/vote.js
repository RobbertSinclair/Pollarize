$(document).ready(function() {
    var the_url = window.location.pathname;
    var poll_slug = the_url.split("/")[1];

    $(".answer-button").click(function(){
        var id = this.id;
        var postUrl = "/json/" + poll_slug + "/add-vote";
        var data = {
            poll_slug: poll_slug,
            answerid: id,
        }
        $.ajax({
            type: "POST",
            url: postUrl,
            data: data,
            success: function(data) {
                alert("Success you voted for " + $(this.id).val());
                window.location.href = poll_slug + "/result/";
            },
            failure: function(data) {
                alert("Failed");
            }


        });
    })
})