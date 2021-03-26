$(document).ready(function() {
    var the_url = window.location.pathname;
    var poll_slug = the_url.split("/")[1];

    $(".answer-button").click(function(){
        var id = this.id;
        var postUrl = "/json/add-vote/";
        var data = {
            poll_slug: poll_slug,
            answer_id: id,
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        }
        $.ajax({
            type: "POST",
            url: postUrl,
            data: data,
            success: function(data) {
                alert("Success you voted for " + $(this.id).val());
                var newUrl = poll_slug + "/result/"
                window.location.href = newUrl;
            },
            failure: function(data) {
                alert("Failed");
            }


        });
    })
})