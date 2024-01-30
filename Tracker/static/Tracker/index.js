document.addEventListener("DOMContentLoaded", function () {
    // Sample data for the chart
    const fetchIndexData = async () => {
      try {
        const response = await fetch('/data/index/fav');
        const data = await response.json();
  
        const perf_indicator = data.perf_indicator.map((perf_indicator, index) => ({
          x: index + 1, // Number each starting from one
          y: perf_indicator.fields.score, // Vertical value as int_score
        }));
  
        const chartData = {
          labels: perf_indicator.map(scoreSet => scoreSet.x),
          datasets: [
            {
              label: data.perf_indicator_id,
              data: perf_indicator,
              borderColor: "rgba(75, 192, 192, 1)",
              fill: false,
            },
          ],
        };
  
        const config = {
          type: "line",
          data: chartData,
          options: {
            scales: {
              x: {
                type: "linear", // Use linear scale for numeric x-axis
                position: 'bottom',
                title: {
                  display: true,
                  text: 'NBR',
                },
              },
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: 'score',
                },
              },
            },
          },
        };
  
        // Get the canvas element
        const ctx = document.getElementById("chartjs-dashboard-line").getContext("2d");
  
        // Create the chart
        const myChart = new Chart(ctx, config);

        // Add title to graph
        document.getElementById("index-chart-title").innerHTML = "Favourited Perfomance indicator: " + data.perf_indicator_id;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };


  document.getElementById("dashboard-side-button").addEventListener("click", fetchIndexData);



  // Call the fetchData function
  fetchIndexData();
});