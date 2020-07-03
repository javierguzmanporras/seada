$.ajax({
    url: $("#time-line-chart").attr("data-url"),
    dataType: 'json',
    success: function (data) {
        //Highcharts.chart("time_line_container", data);
        Highcharts.chart('time_line_container', {
            chart: {
                zoomType: 'x',
                type: 'timeline'
            },
            plotOptions: {
                series: {
                    dataLabels: {
                        enabled: true
                    }
                }
            },
            xAxis: {
                type: 'datetime',
                visible: true
            },
            yAxis: {
                gridLineWidth: 1,
                title: null,
                labels: {
                    enabled: false
                }
            },
            legend: {
                enabled: false
            },
            title: {
                text: 'Timeline of user'
            },
            tooltip: {
                style: {
                    width: 300
                }
            },
            series: [{
                dataLabels: {
                    allowOverlap: false,
                    format: '<span style="color:{point.color}">● </span><span style="font-weight: bold;" > ' +
                        '{point.x:%d %b %Y}</span><br/>{point.label}'
                },
                marker: {
                    symbol: 'circle'
                },
                data: data
            }]
        });
    }
});