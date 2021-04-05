var theChart;

$(document).ready(function(){
    console.log("result.js loaded successfully");
    var the_url = window.location.pathname;
    var theCanvas = document.getElementById("poll-chart");
    var poll_slug = the_url.split("/")[1];
    var request_url = "/json/" + poll_slug + "/results/"
    //Get chart
    $.get(request_url, function(data) {
        chartData = displayChart(data.answer1, data.votes1, data.answer2, data.votes2);
        theChart = new Chart(theCanvas, chartData)
    });
    UpdateChart();
});

//Display chart data
function displayChart(answer1, votes1, answer2, votes2) {
    var theData = {
            labels: [answer1, answer2],
            datasets: [{
                label: "",
                backgroundColor: ["#ff9c00", "#505050"],
                data: [votes1, votes2]
            }]
    };

    Chart.defaults.scale.ticks.beginAtZero = true;

    chartData = {
        type: 'horizontalBar',
        data: theData,
        responsive: true,
        maintainAspectRatio: true,

    };

    return chartData;
}

// This function checks every 2 seconds to get the most up to date chart.
function UpdateChart() {
    var poll_slug = window.location.pathname.split("/")[1];
    var request_url = "/json/" + poll_slug + "/results/";
    $.get(request_url, function(data) {
        votes1 = data.votes1;
        votes2 = data.votes2;
        var chartData = theChart.data.datasets[0].data;
        theChart.data.datasets[0].data[0] = votes1;
        theChart.data.datasets[0].data[1] = votes2;
        theChart.update();
        //Display latest vote if it exists
        if(data.latest_user != null){
            $("#latest").html("LATEST: " + data.latest_user + " voted for " + data.latest_option);
        }

    })
    //Recursively call function after 2 seconds
    setTimeout(UpdateChart, 2000);
}