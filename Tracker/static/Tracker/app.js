document.addEventListener("DOMContentLoaded", function () {
  // Sample data for the chart
  const fetchData = async () => {
    try {
      const response = await fetch('/data/index');
      const data = await response.json();

      const scoreSets = data.score_sets.map(scoreSet => ({
        x: scoreSet.fields.nbr, // Use "nbr" as horizontal value
        y: scoreSet.fields.int_score, // Vertical value as int_score
      }));

      const chartData = {
        labels: scoreSets.map(scoreSet => scoreSet.x),
        datasets: [
          {
            label: "Sample Data",
            data: scoreSets,
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
                text: 'int_score',
              },
            },
          },
        },
      };

      // Get the canvas element
      const ctx = document.getElementById("chartjs-dashboard-line").getContext("2d");

      // Create the chart
      const myChart = new Chart(ctx, config);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  // Call the fetchData function
  fetchData();
});
