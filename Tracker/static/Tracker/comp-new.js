document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("comp-new-form");

    form.onsubmit = function (event) {
        event.preventDefault();

        var formData = new FormData(form);

        // Variable to check if is edit or new
        is_new = true;

        // fetch url
        fetch_url = (is_new) ? "/form/comp-new" : "/form/comp-edit";

        // Use fetch to send the form data
        fetch("/form/comp-new", {
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
                console.log("Form submission successful");
                console.log(response.message);
                comp_view(formData.get("competition_type"));
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

function comp_new(data_point, edit) {
    console.log("comp_new called with param: " + data_point);

    showPage("comp-new");

    // add title to page
    document.getElementById("comp-new-title").innerHTML = data_point.performance_indicator_name;

    // add hidden data to form
    document.getElementById("comp-new-hidden-field").value = data_point.performance_indicator_id;
    document.getElementById("comp-new-edit-id").value = edit;
    console.log("edit value:" + edit);

    // remove old data from form
    document.getElementById("comp-new-form").reset();

}