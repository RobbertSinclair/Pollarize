// This is just a script to add attributes to certain elements to make styling easier

$(document).ready(function() {
    var message_id = 1;

    $("#name_username").html("Username:");
    $("#name_email").html("Email Address:");
    $("#name_password1").html("Create password:");
    $("#name_password2").html("Confirm password:");

    $("li").each(function() {
        $(this).attr("id", "message-" + message_id);
        $(this).attr("class", "form-message");
        message_id = message_id + 1;
    });

    $(".help_text").each(function() {
            if($(this).attr("id") != "help_username"){
                $(this).hide();
            }

    });

    $("ul").attr("class", "form-messages");

    $("ul").closest("div").attr("id", "password1-div");
    $("#password1-div").append("<div id='pass-form-div'></div>");
    $("#pass-form-div").append($("#password1-div>.centre"))
    $("#password1-div").append("<div id='messages-div'></div>");
    $("#messages-div").append($("#password1-div>ul"));

    $(".field_input").focusin(function() {
        var field_id = $(this).attr("id").substring(6);
        console.log(field_id);

        if(field_id == "password1"){
            $(".help_text").show();
            $("#help_username").hide();
            $("#help_password2").hide();
        }
        else if($("#help_" + field_id).is(":hidden")){
            $("#help_" + field_id).show();
        }
    });

    $(".field_input").focusout(function() {
        $(".help_text").hide();
    });

    $("button").each(function() {
        if ($(this).attr("type") == "submit") {
            $(this).addClass("orange_button");
        }
    });
    
})