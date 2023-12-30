document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("manage-side-button").addEventListener("click", getManageData);
});

function getManageData() {
    const fetchManageData = async () => {
        try {
            const response = await fetch('/data/manage');
            const data = await response.json();

            // Create table
            let table = document.getElementById("manage-table-content");

            if (table.rows.length > 0) {
                // remove event listeners
                for (let i = 0; i < table.rows.length; i++) {
                    document.querySelectorAll(".manage-table-row").forEach(function(element) {
                        element.removeEventListener("click", function() {
                            comp_view(i);
                        });
                    });
                }
            }

            table.innerHTML = "";

            // add data to table
            data.competition_types.forEach((competition_type, index) => {
                const row = table.insertRow(index);
                row.id = "manage-table-row-" + competition_type.id;
                row.classList.add("manage-table-row");
                row.addEventListener("click", function() {comp_view(competition_type.id);});
                console.log(competition_type);
            
                // add cells
                for (const key in competition_type) {
                    if (key == "id") {
                        continue;
                    }
                    if (competition_type.hasOwnProperty(key)) {
                        const cell = row.insertCell();
                        cell.innerHTML = competition_type[key];
                        if (key == "shots_count") {
                            cell.classList.add("d-none", "d-md-table-cell");
                        }
                    }
                }


            });

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
    fetchManageData();
}