$(document).ready(function() {
    console.log("account_drop_down.js loaded successfully");
    //Hide drop down on page load
    $("#account_drop_down").hide();
    //Clicking account button toggles drop down visibility
    $("#navbar_account").click(function() {
        $("#account_drop_down").toggle();
    });
})