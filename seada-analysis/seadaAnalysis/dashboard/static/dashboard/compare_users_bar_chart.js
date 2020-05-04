$(function () {

    var $myChart = $("#myChart");
      $.ajax({
        url: $myChart.data("url"),
        success: function (data) {

            console.log(data)

            var barChartData = {
                //labels: ['I1', 'I2', 'I3', 'I4', 'I5', 'I6'],
                labels: data.labels,
                datasets: [
                    {
                        label: data.user1_label,
                        data: data.user1_data,
                        //data: [12, 10, 3, 5, 2, 3],
                        //data: [{x:'2016-12-25', y:20}, {x:'2016-12-26', y:10}, {x:'2016-12-27', y:5}, {x:'2016-12-28', y:1}],
                        //data: [[5,6], [-3,-6]],
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1,
                    },
                    {
                        label: data.user2_label,
                        data: data.user2_data,
                        //data: [12, 10, 3, 5, 2, 3],
                        //data: [{x:'2016-12-25', y:20}, {x:'2016-12-26', y:10}, {x:'2016-12-27', y:5}, {x:'2016-12-28', y:1}],
                        //data: [[5,6], [-3,-6]],
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
                    barChartData.labels.push('I7');
                    for (var index = 0; index < barChartData.datasets.length; ++index) {
                        barChartData.datasets[index].data.push(7);
                    }

                    window.myBar.update();
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



