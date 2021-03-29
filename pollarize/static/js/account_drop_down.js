$(document).ready(function() {
    console.log("account_drop_down.js loaded successfully");
    $("#account_drop_down").hide();

    $("#navbar_account").click(function() {
        $("#account_drop_down").toggle();
    });
})