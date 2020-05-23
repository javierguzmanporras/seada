    var timeFormat = 'MM/DD/YYYY HH:mm';

		function newDateString(days) {
			return moment().add(days, 'd').format(timeFormat);
		}

		var color = Chart.helpers.color;
		console.info(newDateString(0))
		var config = {
			type: 'bar',
			data: {
				labels: [
					newDateString(0),
					newDateString(1),
					newDateString(2),
					newDateString(3),
					newDateString(4),
					newDateString(5),
					newDateString(6),
					newDateString(7),
					newDateString(8),
					newDateString(9),
					newDateString(10),
					newDateString(11),
					newDateString(12),
					newDateString(13),
					newDateString(14),
					newDateString(15),
					newDateString(16),
					newDateString(17),
					newDateString(18),
					newDateString(19),
					newDateString(0),
					newDateString(1),
					newDateString(2),
					newDateString(3),
					newDateString(4),
					newDateString(5),
					newDateString(6),
					newDateString(7),
					newDateString(8),
					newDateString(9),
					newDateString(10),
					newDateString(11),
					newDateString(12),
					newDateString(13),
					newDateString(14),
					newDateString(15),
					newDateString(16),
					newDateString(17),
					newDateString(18),
					newDateString(19),
					newDateString(0),
					newDateString(1),
					newDateString(2),
					newDateString(3),
					newDateString(4),
					newDateString(5),
					newDateString(6),
					newDateString(7),
					newDateString(8),
					newDateString(9),
					newDateString(10),
					newDateString(11),
					newDateString(12),
					newDateString(13),
					newDateString(14),
					newDateString(15),
					newDateString(16),
					newDateString(17),
					newDateString(18),
					newDateString(19),
					newDateString(0),
					newDateString(1),
					newDateString(2),
					newDateString(3),
					newDateString(4),
					newDateString(5),
					newDateString(6),
					newDateString(7),
					newDateString(8),
					newDateString(9),
					newDateString(10),
					newDateString(11),
					newDateString(12),
					newDateString(13),
					newDateString(14),
					newDateString(15),
					newDateString(16),
					newDateString(17),
					newDateString(18),
					newDateString(19),
				],
				datasets: [{
					type: 'bar',
					label: 'Dataset 1',
					backgroundColor: 'red',
					borderColor: 'red',
					data: [79, -71, 3, 54, -88, 72, 25, 66, 77, 88, 79, -71, 3, 54, -88, 72, 25, 66, 77, 88, 79, -71, 3, 54, -88, 72, 25, 66, 77, 88, 79, -71, 3, 54, -88, 72, 25, 66, 77, 88,79, -71, 3, 54, -88, 72, 25, 66, 77, 88, 79, -71, 3, 54, -88, 72, 25, 66, 77, 88, 79, -71, 3, 54, -88, 72, 25, 66, 77, 88, 79, -71, 3, 54, -88, 72, 25, 66, 77, 88],
				}, {
					type: 'bar',
					label: 'Dataset 2',
					backgroundColor: 'blue',
					borderColor: 'blue',
					data: [96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77, 96, 11, -2, -12, -77, 60, -55, 44, -33, -77],
				}]
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
							// round: 'day'
						}
					}],
				},
			}
		};

		window.onload = function() {
			var ctx = document.getElementById('time_line_chart').getContext('2d');
			window.myLine = new Chart(ctx, config);

		};

//		var colorNames = Object.keys(window.chartColors);





