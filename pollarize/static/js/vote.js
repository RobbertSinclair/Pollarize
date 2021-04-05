$(document).ready(function() {
    var the_url = window.location.pathname;
    var poll_slug = the_url.split("/")[1];
    var origin = window.location.origin;

    //When vote button is clicked
    $(".answer-button").click(function(){
        var id = this.id;
        var postUrl = "/json/add-vote/";
        //Send vote information to views
        var data = {
            poll_slug: poll_slug,
            answer_id: id,
            the_answer: $("." + this.id).text(),
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
        }
        $.ajax({
            type: "POST",
            url: postUrl,
            data: data,
            success: function(data) {
                //Redirect to results page for the poll
                var newUrl = origin + "/" + poll_slug + "/results/";
                window.location.href = newUrl;
            },
            failure: function(data) {
                alert("Failed");
            }


        });
    })
})