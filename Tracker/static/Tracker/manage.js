document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM loaded!, from manage.js");

    document.getElementById("manage-side-button").addEventListener("click", getManageData);
    //getManageData();

});

function getManageData() {
    const fetchManageData = async () => {
        try {
            const response = await fetch('/data/manage');
            const data = await response.json();
            //console.log(data);

            // Create table
            let table = document.getElementById("manage-table-content");
            table.innerHTML = "";
            /*
            let row = table.insertRow(0);
            let cell = row.insertCell(0);
            cell.innerHTML = "<b>Username</b>";
            cell = row.insertCell(1);
            cell.innerHTML = "<b>First Name</b>";
            */

            // add data to table
            data.competition_types.forEach((competition_type, index) => {
                console.log(competition_type);
                row = table.insertRow(index); // remove + 1 afterwards
            
                // add cells
                for (const key in competition_type) {
                    if (key == "id") {
                        continue;
                    }
                    if (competition_type.hasOwnProperty(key)) {
                        cell = row.insertCell();
                        cell.innerHTML = competition_type[key];
                    }
                }
            });

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
    fetchManageData();
}