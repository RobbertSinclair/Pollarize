$(document).ready(function() {
    var getUrl = "/json/search/";
    $("#searchbar").on('input', function() {

        var data = {
            search_term: $("#searchbar").val(),
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
        
    })
})
