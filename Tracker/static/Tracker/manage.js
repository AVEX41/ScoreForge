document.addEventListener("DOMContentLoaded", function () {
    // eventlistener to get data
    document.getElementById("manage-side-button").addEventListener("click", getManageData);


    function getManageData() {
        const fetchManageData = async () => {
            try {
                const response = await fetch('/data/manage');
                const data = await response.json();


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
                    for (const key in competition_type) {
                        if (key == "id") {
                            continue;
                        }
                        if (competition_type.hasOwnProperty(key)) {
                            const cell = row.insertCell();
                            cell.innerHTML = competition_type[key];
                        }
                    }

                    // create cell for both buttons
                    const edit_show_cell = row.insertCell();
                    
                    // Create edit button
                    var edit_btn = document.createElement("button");
                    edit_btn.innerHTML = "Edit";
                    edit_btn.classList.add("new-edit-btn", "btn", "btn-primary");
                    edit_btn.id = "manage-edit-btn-" + competition_type.id;
                    edit_show_cell.appendChild(edit_btn);
                    
                    // add Event Listener to edit button
                    document.getElementById("manage-edit-btn-" + competition_type.id).addEventListener("click", () => {
                        showNew(data, index);
                    });
                    
                    // create show button
                    var show_btn = document.createElement("button");
                    show_btn.innerHTML = "Show";
                    show_btn.classList.add("new-edit-btn", "btn", "btn-info");
                    show_btn.id = "manage-show-btn-" + competition_type.id;
                    edit_show_cell.appendChild(show_btn);

                    // add Event Listener to show button
                    document.getElementById("manage-show-btn-" + competition_type.id).addEventListener("click", () => {comp_view(competition_type.id);});
                });

            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
        fetchManageData();
    }
});