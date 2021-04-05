// This is just a script to add attributes to certain elements to make styling easier

$(document).ready(function() {
    var message_id = 1;

    //Replace form titles with nicer titles
    $("#name_username").html("Username:");
    $("#name_email").html("Email Address:");
    $("#name_password1").html("Create password:");
    $("#name_password2").html("Confirm password:");

    //Add id and class to list elements in password help text
    $("li").each(function() {
        $(this).attr("id", "message-" + message_id);
        $(this).attr("class", "form-message");
        message_id = message_id + 1;
    });

    //Hide all help text on page load
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

    //Show field helper text when it is focused on
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

    //Hide all help text when a field is unfocused
    $(".field_input").focusout(function() {
        $(".help_text").hide();
    });

    //Make all submit buttons orange
    $("button").each(function() {
        if ($(this).attr("type") == "submit") {
            $(this).addClass("orange_button");
        }
    });
    
})