// static/tracker/app.js

document.addEventListener("DOMContentLoaded", function () {
    // Sample data for the chart
    const data = {
      labels: ["Jan", "Feb", "Mar", "Apr", "May"],
      datasets: [
        {
          label: "Sample Data",
          data: [12, 19, 3, 5, 2],
          borderColor: "rgba(75, 192, 192, 1)",
          fill: false,
        },
      ],
    };
  
    const config = {
      type: "line",
      data: data,
      options: {
        scales: {
          x: {
            type: "category",
            labels: ["Jan", "Feb", "Mar", "Apr", "May"],
          },
          y: {
            beginAtZero: true,
          },
        },
      },
    };
  
    // Get the canvas element
    const ctx = document.getElementById("chartjs-dashboard-line").getContext("2d");
  
    // Create the chart
    const myChart = new Chart(ctx, config);
  });
  