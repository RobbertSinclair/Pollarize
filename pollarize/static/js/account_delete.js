$(document).ready(function(){
    console.log("account_delete.js loaded successfully");

    //Hide delete form on page load
    $("#account_delete_block").hide();

    //If delete account button is clicked, show form
    $('#delete_button').click(function() {
        $("#account_delete_block").slideDown("slow");
    });
})
