
$(document).ready(function(){
    console.log("result.js loaded successfully");
    var the_url = window.location.pathname;
    var theCanvas = document.getElementById("poll-chart");
    var theChart;
    var poll_slug = the_url.split("/")[1];
    var request_url = "/json/" + poll_slug + "/results/"
    $.get(request_url, function(data) {
        chartData = displayChart(data.answer1, data.votes1, data.answer2, data.votes2);
        theChart = new Chart(theCanvas, chartData)
    });
});


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