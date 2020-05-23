$(function () {

     var $myChart = $("#user_hour_analysis_chart");
     $.ajax({
        url: $myChart.data("url"),
        success: function (data) {

            //console.log(data)

            hour_data = {
                labels: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],
                datasets: [{
                    label: '# of Tweets and Retweets',
                    data: data.data,
                    backgroundColor: 'rgba(0,0,255,0.1)',
                    borderColor: 'rgba(0,0,255,0.5)',
                    borderWidth: 1
                }]
            }

            var ctx = $myChart[0];
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: hour_data,
                options: {
                    title: {
                        display: true,
                        text: data.title_text
                    },
                    scales: {
                        yAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: "Number of Tweet plus Retweet",
                                fontFamily: 'sans-serif'
                            },
                            ticks: { beginAtZero: true }
                        }],
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: "Hour of day",
                                fontFamily: 'sans-serif'
                            }
                        }]
                    }
                }
            })
        }
    })
})
