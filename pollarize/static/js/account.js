//Set size of account overlay dynamically on account page
$(document).ready(function() {
    setOverlaySize();

    $(window).resize(function() {
        setOverlaySize();
    });

    
});

function setOverlaySize() {
    $(".overlay").css("height", $("#profile_img").height());
    $(".overlay").css("width", $("#profile_img").width());
}