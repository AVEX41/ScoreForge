document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("comp-new-form");

    form.onsubmit = function (event) {
        event.preventDefault();

        var formData = new FormData(form);
        value = document.getElementById("comp-new-edit-id").value

        // Variable to check if is edit or new
        if (value === "false") {
            is_new = true;

        } else {
            is_new = false;
        }
        

        // fetch url
        fetch_url = (is_new) ? "/form/comp-new" : "/form/comp-edit";

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

function comp_new(data, edit) {
    showPage("comp-new");

    // remove old data from form
    document.getElementById("comp-new-form").reset();

    // add title to page
    document.getElementById("comp-new-title").innerHTML = data.performance_indicator_name;

    // add hidden data to form
    document.getElementById("comp-new-hidden-field").value = data.performance_indicator_id;
    
    if (edit === false) {
        document.getElementById("comp-new-edit-id").value = edit;
    } else {
        // add hidden value
        document.getElementById("comp-new-edit-id").value = data.data_points[edit].pk;

        // prefill value
        document.getElementById("data_point_score_field").value = data.data_points[edit].fields.score;
    }
}