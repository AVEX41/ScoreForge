function showManage() {
    showPage("manage");
    getManageData();
}


function getManageData() {
    const fetchManageData = async () => {
        try {
            const response = await fetch('/data/manage');
            const data = await response.json();

            // CSRF token
            csrf_token = new FormData(document.getElementById("comp-new-form")).get("csrfmiddlewaretoken");

            // add event listener to new button
            document.getElementById("manage-new-button").addEventListener("click", function () {
                showNew(data, false);
            });

            // Create table, and removing event listeners
            let old_table = document.getElementById("manage-table-content"); 
            table = old_table.cloneNode(true);
            old_table.parentNode.replaceChild(table, old_table);
            //let table = document.getElementById("manage-table-content");

            table.innerHTML = "";

            // add data to table
            data.competition_types.forEach((competition_type, index) => {
                const row = table.insertRow(index);
                row.id = "manage-table-row-" + competition_type.id;
                row.classList.add("manage-table-row");
                //row.addEventListener("click", () => {comp_view(competition_type.id);});
            
                // add cells
                const show_cell = row.insertCell();
                // create show button
                var show_btn = document.createElement("button");
                show_btn.innerHTML = "Show";
                show_btn.classList.add("new-edit-btn", "btn", "btn-info");
                show_btn.id = "manage-show-btn-" + competition_type.id;
                show_cell.appendChild(show_btn);

                // add Event Listener to show button
                document.getElementById("manage-show-btn-" + competition_type.id).addEventListener("click", () => {comp_view(competition_type.id);});

                for (const key in competition_type) {
                    if (key == "id" || key == "timestamp" || key == "user_favourite") {
                        continue;
                    }
                    if (competition_type.hasOwnProperty(key)) {
                        const cell = row.insertCell();
                        cell.innerHTML = competition_type[key];
                    } 
                }

                // create cell for both buttons
                const edit_cell = row.insertCell();
                
                // Create edit button
                var edit_btn = document.createElement("button");
                edit_btn.innerHTML = "Edit";
                edit_btn.classList.add("new-edit-btn", "btn", "btn-primary");
                edit_btn.id = "manage-edit-btn-" + competition_type.id;
                edit_cell.appendChild(edit_btn);
                
                // add Event Listener to edit button
                document.getElementById("manage-edit-btn-" + competition_type.id).addEventListener("click", () => {
                    showNew(data, index);
                });

                // Add favourite button or form
                const fav_cell = row.insertCell();

                if (competition_type.user_favourite == true) {
                    var fav_btn = document.createElement("button");
                    fav_btn.innerHTML = "Favourite";
                    fav_btn.classList.add("new-fav-btn", "btn", "btn-warning");
                    fav_btn.id = "manage-fav-btn-" + competition_type.id;
                    fav_btn.disabled = true;
                    fav_cell.appendChild(fav_btn);
                } else {
                    var fav_form = document.createElement("form");
                    fav_form.id = "manage-fav-btn-" + competition_type.id;
                    fav_form.classList.add("new-fav-form")

                    var fav_data = document.createElement("input");
                    fav_data.type = "hidden";
                    fav_data.value = competition_type.id;
                    fav_data.name = "perf_id";

                    var fav_input = document.createElement("input");
                    fav_input.type = "submit";
                    fav_input.value = "Favourite";
                    fav_input.classList.add("btn", "btn-warning");

                    fav_form.appendChild(fav_input);
                    fav_form.appendChild(fav_data);
                    fav_cell.appendChild(fav_form);
                }

                // Add event listener to form submit button
                document.querySelectorAll(".new-fav-form").forEach((element) => {
                    element.onsubmit = (event) => {
                        event.preventDefault();

                        var formData = new FormData(element);
                        
                        // Use fetch to send the form data
                        fetch("form/fav", {
                            method: "POST",
                            body: formData,
                            headers: {
                                "X-CSRFToken": csrf_token
                                // Add any other headers if needed
                            }
                        })
                        .then(response => {
                            // Check if the request was successful (status 2xx)
                            if (response.ok) {
                                // Handle the successful response here
                                getManageData();
                            } else {
                                // Handle the error response here
                                console.error("Form submission failed with status: " + response.status);
                            }
                        })
                        .catch(error => {
                            // Handle network errors here
                            console.error("Network error occurred while submitting the form:", error);
                        });
                    };
                });
            });

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
    fetchManageData();
}