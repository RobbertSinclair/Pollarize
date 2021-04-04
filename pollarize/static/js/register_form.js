// This is just a script to add attributes to certain elements to make styling easier

$(document).ready(function() {
    var message_id = 1;
    $("li").each(function() {
        $(this).attr("id", "message-" + message_id);
        $(this).attr("class", "form-message");
        message_id = message_id + 1;
    });

    $("ul").attr("class", "form-messages");

    $("ul").closest("div").attr("id", "password1-div");
    $("#password1-div").append("<div id='pass-form-div'></div>");
    $("#pass-form-div").append($("#password1-div>.centre"))
    $("#password1-div").append("<div id='messages-div'></div>");
    $("#messages-div").append($("#password1-div>ul"));

    $("button").each(function() {
        if ($(this).attr("type") == "submit") {
            $(this).addClass("orange_button");
        }
    })
    
})