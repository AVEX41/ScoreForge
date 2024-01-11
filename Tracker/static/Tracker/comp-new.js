document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("comp-new-form");

    form.onsubmit = function (event) {
        event.preventDefault();

        var formData = new FormData(form);



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

function comp_new(data_point) {
    console.log("comp_new called with param: " + data_point);

    showPage("comp-new");
    document.getElementById("comp-new-title").innerHTML = data_point.performance_indicator_name;

    // add hidden data to form
    document.getElementById("comp-new-hidden-field").value = data_point.performance_indicator_id;

}