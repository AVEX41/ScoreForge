function comp_view(row) {
    console.log("clicked " + row);

    // show page
    showPage("comp-view");

    // fetch data
    const fetchCompData = async () => {
        try {
            const response = await fetch('/data/manage/' + row);
            const data = await response.json();

            console.log(data);
            // add data to page
            /*
            document.getElementById("comp-view-title").innerHTML = data.competition_type.name;
            document.getElementById("comp-view-description").innerHTML = data.competition_type.description;
            document.getElementById("comp-view-shots-count").innerHTML = data.competition_type.shots_count;

            document.getElementById("comp-view-shots").innerHTML = "";
            data.shots.forEach((shot, index) => {
                document.getElementById("comp-view-shots").innerHTML += "<li>" + shot.name + "</li>";
            });
            */

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

}