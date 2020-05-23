    $(function () {

    var $timelineChart = $("#time_line_chart");
      $.ajax({
        url: $timelineChart.data("url"),
        success: function (data) {



            //var timeFormat = 'MM/DD/YYYY HH:mm';
            var timeFormat = 'YYYY-MM-DD HH:mm:ss';
            function newDateString(days) {
			    return moment().add(days, 'd').format(timeFormat);
		    }
		    var color = Chart.helpers.color;
		    console.info(data.labels)
		    console.info(data.data)
		    var config = {
			type: 'bar',
			data: {
				labels: data.labels,
				datasets: [{
					type: 'bar',
					label: 'Dataset 1',
					backgroundColor: 'red',
					borderColor: 'red',
					data: data.data
				},
//				{
//					type: 'bar',
//					label: 'Dataset 2',
//					backgroundColor: 'blue',
//					borderColor: 'blue',
//					data: [96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77],
//				}
				]
			    },
                options: {
                    responsive: true,
                    title: {
                        text: 'Chart.js Combo Time Scale'
                    },
                    scales: {
                        xAxes: [{
                            type: 'time',
                            display: true,
                            time: {
                                format: timeFormat,
                                unit: 'hour',
                                // round: 'day'
                            }
                        }],
                    },
                }
            };

            var ctx = document.getElementById('time_line_chart').getContext('2d');
            window.myLine = new Chart(ctx, config);

//            window.onload = function() {
//                var ctx = document.getElementById('time_line_chart').getContext('2d');
//                window.myLine = new Chart(ctx, config2);
//            };
        }
    });
});






