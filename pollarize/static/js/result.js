
function displayChart(poll_question, answer1, votes1, answer2, votes2) {
    var theCanvas = document.getElementById("poll-chart");
    var theData = {
            labels: [answer1, answer2],
            datasets: [{
                label: "",
                backgroundColor: ["#ff9c00", "#505050"],
                data: [votes1, votes2]
            }]
    };

    Chart.defaults.scale.ticks.beginAtZero = true;
    var theOptions = {
        scales: {
            xAxes: [{
                gridLines: {
                    offsetGridLines: true
                }
            }]
        }
    };

    var theChart = new Chart(theCanvas, {
        type: 'horizontalBar',
        data: theData,
        options: theOptions,
        responsive: true,
        maintainAspectRation: false,

    })
}