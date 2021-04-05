var getUrl = "/json/search/";

$(document).ready(function() {

    //Populate search result boxes with new information after every input to search bar
    $("#searchbar").on('input', function() {
        populate_box("#searchbar");
    })
    //Main search bar on search page
    $("#page_searchbar").on('input', function() {
        populate_box("#page_searchbar");
    })
})

function populate_box(search_bar){
            var data = {
            search_term: $(search_bar).val(),
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
        }
        //Get results from views
        $.ajax({
            type: 'POST',
            url: getUrl,
            data: data,
            success: function(data) {
                var htmlString = "";
                //Add all possible search options to results list
                for (var i = 0; i < data.polls.length; i++) {
                    htmlString += "<option value='" + data.polls[i].question + "'><a href='" + data.polls[i].question_link + "'/></option>";
                }
                htmlString += "</ul>";
                console.log(htmlString);
                //Display results list
                $("#search-results").html(htmlString);
                console.log(data);
            },
            failure: function() {
                console.log("Failure");
            }

        })
}
