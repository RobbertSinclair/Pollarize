var getUrl = "/json/search/";

$(document).ready(function() {
    $("#searchbar").on('input', function() {
        console.log("main")
        populate_box("#searchbar");
    })

    $("#page_searchbar").on('input', function() {
        console.log("Page");
        populate_box("#page_searchbar");
    })
})

function populate_box(search_bar){
            var data = {
            search_term: $(search_bar).val(),
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
        }

        $.ajax({
            type: 'POST',
            url: getUrl,
            data: data,
            success: function(data) {
                var htmlString = "";
                for (var i = 0; i < data.polls.length; i++) {
                    htmlString += "<option value='" + data.polls[i].question + "'><a href='" + data.polls[i].question_link + "'/></option>";
                }
                htmlString += "</ul>";
                console.log(htmlString);
                $("#search-results").html(htmlString);
                console.log(data);
            },
            failure: function() {
                console.log("Failure");
            }

        })
}
