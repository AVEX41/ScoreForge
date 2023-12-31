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
            console.log("/data/manage/" + row);
            const response = await fetch('/data/manage/' + row);
            const data = await response.json();

            console.log(data);
            // add data to page
            
            document.getElementById("comp-view-title").innerHTML = data.competition_type_name;
            document.getElementById("comp-view-description").innerHTML = data.competition_type_description;
            document.getElementById("comp-view-shots-count").innerHTML = data.competition_type_shots_count;

            // Create table
            let table = document.getElementById("comp-view-table-content");
            let headers = ["int_score", "decimal_score", "total_inners", "timestamp"];

            // add data to table
            data.competitions.forEach((competition, index) => {
                // use headers to add data to table
                const row = table.insertRow(index);
                console.log(competition)
                headers.forEach((header, index) => {
                    // add cells
                    const cell1 = row.insertCell();
                    cell1.innerHTML = competition.fields[header];
                    console.log("Header:" + competition.fields[header]);
                });
            });

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    fetchCompData();

}