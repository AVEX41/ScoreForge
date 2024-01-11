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
            console.log("Added event listener to new-button: " + data);
            console.log(data);

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    fetchCompData();

}