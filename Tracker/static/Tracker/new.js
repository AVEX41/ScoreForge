document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("new-form");

    form.onsubmit = function (event) {
        event.preventDefault();

        var formData = new FormData(form);



        // Use fetch to send the form data
        fetch("/form/new", {
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
                showPage("manage");
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
    }

});
function showNew(data, edit) {
    showPage("new");

    document.getElementById("new-header").innerHTML = (edit) ? "Edit" : "Add new";

    if (edit !== false) {
        entity = data.competition_types[edit]

        document.getElementById("new-name-input").value = entity.name;
        document.getElementById("new-desc-input").value = entity.description;

        console.log(data);
        console.log(edit);
        console.log(entity.id);

        document.getElementById("new-submit-type").value = entity.id;
        document.get
    }
}