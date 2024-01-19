document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("manage-side-button").addEventListener("click", getManageData);
});

function getManageData() {
    const fetchManageData = async () => {
        try {
            const response = await fetch('/data/manage');
            const data = await response.json();

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
                row.addEventListener("click", function() {comp_view(competition_type.id);});
            
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

                // Create edit button
                const edit_cell = row.insertCell();
                var btn = document.createElement("button");
                btn.innerHTML = "Edit";
                btn.classList.add("edit-btn", "btn", "btn-primary");
                btn.id = "manage-edit-btn-" + competition_type.id;
                edit_cell.appendChild(btn);


            });

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
    fetchManageData();
}