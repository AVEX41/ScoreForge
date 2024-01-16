document.addEventListener('DOMContentLoaded', function () {
    // add event listener to the button
    document.getElementById("comp-view-new-btn").addEventListener("click", () => {
        //handle click
        showPage("comp-new");
    });
});

function comp_view(row) {
    // show page
    showPage("comp-view");

    // fetch data
    const fetchCompData = async () => {
        try {
            const response = await fetch('/data/manage/' + row);
            const data = await response.json();

            // add data to page
            document.getElementById("comp-view-title").innerHTML = data.performance_indicator_name;
            document.getElementById("comp-view-description").innerHTML = data.performance_indicator_description;

            // ------------------- Add data to table -------------------
            // Create table
            let table = document.getElementById("comp-view-table-content");
            let headers = ["score", "timestamp"];

            // clear table
            table.innerHTML = "";

            // add data to table
            data.data_points.forEach((competition, index) => {
                // use headers to add data to table
                const row = table.insertRow(index);
                headers.forEach((header, index) => {
                    // add cells
                    const cell1 = row.insertCell();
                    cell1.innerHTML = competition.fields[header];
                });
            });

            // ------------------- Add event listener to new-button -------------------
            // remove old event listener if it exists
            document.getElementById("comp-view-new-btn").removeEventListener("click", () => {
                //handle click
                comp_new(data)
            });

            // Add event listener to new-button with parameter
            document.getElementById("comp-view-new-btn").addEventListener("click", () => {
                //handle click
                comp_new(data)
            });

            // ------------------- Add event listener to edit-button -------------------
            // TODO

            // ------------------- Add event listener to delete-button -------------------
            // TODO

            // ------------------- Add data to graph -------------------
    
            const data_points = data.data_points.map((data_point, index) => ({
            x: index + 1, // Number each starting from one
            y: data_point.fields.score, // Vertical value as int_score
            }));
    
            const chartData = {
            labels: data_points.map(scoreSet => scoreSet.x),
            datasets: [
                {
                label: "Sample Data",
                data: data_points,
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
            const ctx = document.getElementById("chartjs-comp-view").getContext("2d");
    
            // Create the chart
            const myChart = new Chart(ctx, config);

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    fetchCompData();

}