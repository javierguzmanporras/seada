$(function () {

    var $myChart = $("#myChart");
      $.ajax({
        url: $myChart.data("url"),
        success: function (data) {

            var barChartData = {
                labels: data.labels,
                datasets: [
                    {
                        label: data.user1_label,
                        data: data.user1_data,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                    },
                    {
                        label: data.user2_label,
                        data: data.user2_data,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                }]
            };

            var ctx = $myChart[0];
            ctx.width = 900;
            ctx.height = 500;
            window.myBar = new Chart(ctx, {
                type: 'bar',
                data: barChartData,
                options: {
                    responsive: false,
                    maintainAspectRatio: true,
                    scales: {
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Day',
                                fontFamily: 'sans-serif',
                            },
                        }],
                        yAxes: [{
                            ticks: {beginAtZero: true},
                            scaleLabel: {
                                display: true,
                                labelString: 'Number of Tweets and Re-tweets',
                                fontFamily: 'sans-serif',
                            }
                        }]
                    },
                    title: {
                        display: true,
                        text: 'Tweets and Retweets compare'
                    }
                }
            });

            document.getElementById('addData').addEventListener('click', function() {
                if (barChartData.datasets.length > 0) {
                    $.ajax({
                        type: 'GET',
                        url: "http://127.0.0.1:8000/dashboard/compareusers/barchart/" + data.user1_label + "/" + data.user2_label + "/" + barChartData.labels[0],
                        complete: function() {},
                        success: function (data) {
                            barChartData.labels.unshift(data.label);
                            barChartData.datasets[0].data.unshift(data.user1_data);
                            barChartData.datasets[1].data.unshift(data.user2_data);
                            window.myBar.update();
                        }
                    })
//                    for (var index = 0; index < barChartData.datasets.length; ++index) {
//                        barChartData.datasets[index].data.unshift();
//                    }
                }
            });

            document.getElementById('removeLastData').addEventListener('click', function() {
                barChartData.labels.splice(-1, 1); // remove the label first

                barChartData.datasets.forEach(function(dataset) {
                    dataset.data.pop();
                });

                window.myBar.update();
            });

            document.getElementById('removeFirstData').addEventListener('click', function() {
                barChartData.labels.splice(1, -1); // remove the label first

                barChartData.datasets.forEach(function(dataset) {
                    dataset.data.shift();
                });

                window.myBar.update();
            });
        }
    });
});



