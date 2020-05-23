$(function () {

    var $myChart = $("#user_sentiment_analysis_chart");
    $.ajax({
        url: $myChart.data("url"),
        success: function (data) {

            //console.log(data)

            sentiment_data = {
                labels: ["Negative","Positive","Neutral"],
                datasets: [{
                    label: "Sentiments Analysis",
                    data: data.data,
                    backgroundColor:[
                        "rgb(255, 99, 132)",
                        "rgb(54, 162, 235)",
                        "rgb(255, 205, 86)"
                    ]
                }]
            }

            var ctx = $myChart[0];
            var myPieChart = new Chart(ctx, {
                type: 'pie',
                data: sentiment_data,
                options: {
                    responsive: true,
                     title: {
                        display: true,
                        text: data.title_text
                    },
                }
            })
        }
    })
})