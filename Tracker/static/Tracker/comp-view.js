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
            // Create table, and removing event listeners
            let old_table = document.getElementById("comp-view-table-content"); 
            table = old_table.cloneNode(true);
            old_table.parentNode.replaceChild(table, old_table);

            // Headers of table
            let headers = ["score", "timestamp", "edit"];

            // clear table
            table.innerHTML = "";

            // add data to table
            data.data_points.forEach((competition, index) => {
                // use headers to add data to table
                const row = table.insertRow(index);
                headers.forEach((header, index) => {
                    // add cells
                    const cell1 = row.insertCell();
                    if(header !== "edit") {
                        
                        cell1.innerHTML = competition.fields[header];
                    } else {
                        var btn = document.createElement("button");
                        btn.innerHTML = "Edit";
                        btn.classList.add("edit-btn", "btn", "btn-primary");
                        btn.id = "edit-btn-" + competition.pk;
                        cell1.appendChild(btn);
                    }
                });
            });

            // ------------------- Add event listener to new-button -------------------
            // remove old event listener if it exists
            document.getElementById("comp-view-new-btn").removeEventListener("click", () => {
                //handle click
                comp_new(data, false)
            });

            // Add event listener to new-button with parameter
            document.getElementById("comp-view-new-btn").addEventListener("click", () => {
                //handle click
                comp_new(data, false)
            });

            // ------------------- Add event listener to edit-button -------------------
            // Add event listener to new-button with parameter

            document.querySelectorAll(".edit-btn").forEach((element, index) => {
                element.addEventListener("click", () => {
                    comp_new(data, index); // index is numbering of the btn
                });
            });

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
                label: data.performance_indicator_name,
                data: data_points,
                borderColor: "rgba(59, 126, 221, 1)",
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
    
            // Replace the comp view
            let old_chart = document.getElementById("chartjs-comp-view"); 
            chart = old_chart.cloneNode(true);
            old_chart.parentNode.replaceChild(chart, old_chart);

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