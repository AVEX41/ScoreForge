document.addEventListener("DOMContentLoaded", function () {
    // on new/edit submit
    var edit_form = document.getElementById("new-form");

    edit_form.onsubmit = function (event) {
        event.preventDefault();

        var formData = new FormData(edit_form);
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
                message = (is_new) ? "Performance indicator created successfully." : "Performance indicator created successfully.";
                showMessage("success", message);

            } else {
                console.error("Form submission failed with status: " + response.status);
                // Handle the error response here
                return response.json();
            }
        })
        .then(data => {
            showMessage("danger", data.message);
        })
        .catch(error => {
            // Handle network errors here
            console.error("Network error occurred while submitting the form:", error);
        });
    }

    // delete form
    var delete_form = document.getElementById("new-delete-form");

    delete_form.onsubmit = function (event) {
        event.preventDefault();

        var formData = new FormData(delete_form);
        
        // Use fetch to send the form data
        fetch("form/delete", {
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
                showMessage("success", "Perfomance indicator deleted successfully.");
            } else {
                console.error("Form submission failed with status: " + response.status);
                // Handle the error response here
                return response.json();
            }
        })
        .then(data => {
            showMessage("danger", data.message);
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

        // create delete button
        document.getElementById("new-delete-form").style.display = "flex";

        // add hidden data to form
        document.getElementById("new-delete-id").value = entity.id;
    } else {
        
        document.getElementById("new-form").reset();
        document.getElementById("new-submit-type").value = false;

        // hide delete button
        document.getElementById("new-delete-form").style.display = "none";
    }
}
