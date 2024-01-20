document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("new-form");

    form.onsubmit = function (event) {
        event.preventDefault();

        var formData = new FormData(form);
        value = document.getElementById("new-submit-type").value

        // Variable to check if is edit or new
        if (value === "false") {
            is_new = true;

        } else {
            is_new = false;
        }
        

        // fetch url
        fetch_url = (is_new) ? "/form/new" : "/form/edit";



        // Use fetch to send the form data
        fetch(fetch_url, {
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
                showManage();
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

        document.getElementById("new-submit-type").value = entity.id;
    } else {

        document.getElementById("new-form").reset();
        document.getElementById("new-submit-type").value = false;
    }
}
