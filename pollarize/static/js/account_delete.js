var balloons_on = false;
//Number of balloons to generate on page load
var balloons_on_load = 20;
//Variables to alter boundaries of randomness
var min_time = 175; var dev_time = 300;
var min_ms = 650; var dev_ms = 2000;
//Size of padding on left and right side where balloons can't generate
var padding = 100;

$(document).ready(function(){
    console.log("account_delete.js loaded successfully");

    //Hide delete form on page load
    $("#account_delete_block").hide();

    $('#delete_button').click(function() {
        $("#account_delete_block").slideDown("slow");
    });
})
