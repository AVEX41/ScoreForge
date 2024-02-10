function comp_view(row) {
    // show page
    showPage("comp-view");

    // fetch data
    const fetchCompData = async () => {
        try {
            const response = await fetch('/data/manage/' + row);
            const data = await response.json();

            // CSRF token
            csrf_token = new FormData(document.getElementById("comp-new-form")).get("csrfmiddlewaretoken");

            // add data to page
            document.getElementById("comp-view-title").innerHTML = data.performance_indicator_name;
            document.getElementById("comp-view-description").innerHTML = data.performance_indicator_description;

            // ------------------- Add data to table -------------------
            // Create table, and removing event listeners
            let old_table = document.getElementById("comp-view-table-content"); 
            table = old_table.cloneNode(true);
            old_table.parentNode.replaceChild(table, old_table);

            // Headers of table
            let headers = ["score", "edit", "delete"];

            // clear table
            table.innerHTML = "";

            // add data to table
            data.data_points.forEach((competition, index) => {
                // use headers to add data to table
                const row = table.insertRow(index);
                headers.forEach((header, index) => {
                    // add cells
                    const cell = row.insertCell();
                    if (header !== "edit" && header !== "delete") {
                        cell.innerHTML = competition.fields[header];
                    } else {
                        if (header === "edit") {
                            var btn = document.createElement("button");
                            btn.innerHTML = "Edit";
                            btn.classList.add("edit-btn", "btn", "btn-primary");
                            btn.id = "edit-btn-" + competition.pk;
                            cell.appendChild(btn);
                        } else if (header === "delete") {
                            // create form
                            var delete_form = document.createElement("form");
                            delete_form.id = "delete-form-" + index;
                            delete_form.classList.add("delete-form");
                            delete_form.method = "post"

                            // btn
                            var btn= document.createElement("button");
                            btn.innerHTML = "Delete";
                            btn.classList.add("delete-btn", "btn", "btn-danger");
                            btn.id = "delete-btn-" + competition.pk;
                            btn.type = "submit";
                            delete_form.appendChild(btn);

                            // Hidden ID
                            var h_val = document.createElement("input");
                            h_val.type = "hidden";
                            h_val.name = "item";
                            h_val.value = competition.pk;
                            delete_form.appendChild(h_val);

                            // CSRF token
                            var inpt_token = document.createElement("input");
                            inpt_token.type = "hidden";
                            inpt_token.name = "csrfmiddlewaretoken";
                            inpt_token.value = csrf_token;
                            delete_form.appendChild(inpt_token);

                            // add to cell
                            cell.appendChild(delete_form);
                        }
                    }
                });
            });

            // ------------------- Add event listener to new-button -------------------
            // remove event listener
            let old_btn = document.getElementById("comp-view-new-btn"); 
            btn = old_btn.cloneNode(true);
            old_btn.parentNode.replaceChild(btn, old_btn);

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
            document.querySelectorAll(".delete-form").forEach((element, index) => {

                element.onsubmit = function (event) {
                    event.preventDefault();

                    var formData = new FormData(element);

                    fetch("/form/comp-delete", {
                        method: "POST",
                        body: formData,
                        headers: {
                            "X-CSRFToken": formData.get("csrfmiddlewaretoken")
                            // Add any other headers if needed
                        }
                    })
                    .then(response => {
                        // Check if the request was successful (status 2xx)
                        if (response.ok) {
                            // Handle the successful response here
                            console.log("delete successfull");
                        } else {
                            // Handle the error response here
                            console.error("Deletion returned with status: " + response.status);
                        }
                    })
                    .catch(error => {
                        // Handle network errors here
                        console.error("Network error occurred while submitting the form:", error);
                    });
                }
            });

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