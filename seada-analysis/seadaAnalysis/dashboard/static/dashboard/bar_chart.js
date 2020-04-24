    $(function () {

      var $populationChart = $("#population-chart");
      $.ajax({
        url: $populationChart.data("url"),
        success: function (data) {

          var ctx = $populationChart[0].getContext("2d");

          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Population',
                backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe'],
                data: data.data
              }]
            },
            options: {
              responsive: true,
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Population Bar Chart'
              }
            }
          });

        }
      });

    });