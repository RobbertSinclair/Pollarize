$(document).ready(function() {
    var the_url = window.location.pathname;
    var poll_slug = the_url.split("/")[1];

    $(".answer-button").click(function(){
        var id = this.id;
        alert(id);
    })
})