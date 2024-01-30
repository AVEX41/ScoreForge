document.addEventListener("DOMContentLoaded", () => {
    Array.from(document.getElementsByClassName("edit-form")).forEach(element => {
        element.style.display = "none";
    });

    document.getElementById("profile-show-edit").addEventListener("click", () => {
        profile_show_form()
    });
    document.getElementById("profile-show-main").addEventListener("click", () => {
        profile_show_main()
    });


    // ---- Handle forms ----
    name_form = document.getElementById("profile-name-edit-form");
    email_form = document.getElementById("profile-email-edit-form");
    user_name_form = document.getElementById("profile-user-name-edit-form");
    pword_form = document.getElementById("profile-password-edit-form");

    // Handle name
    name_form.onsubmit = (event) => {
        event.preventDefault();

        var formData = new FormData(name_form);
        
        // Use fetch to send the form data
        fetch("form/edit/usr/name", {
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
                console.log("name form submitted successfully");

                document.getElementById("profile-first-name").innerHTML = formData.get("first_name");
                document.getElementById("profile-last-name").innerHTML = formData.get("last_name");
                
                profile_show_main();
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

    // Handle email
    email_form.onsubmit = (event) => {
        event.preventDefault();

        var formData = new FormData(email_form);
        
        // Use fetch to send the form data
        fetch("form/edit/usr/email", {
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
                console.log("email form submitted successfully");

                document.getElementById("profile-email").innerHTML = formData.get("email");
                
                profile_show_main();
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

    // Handle user name
    user_name_form.onsubmit = (event) => {
        event.preventDefault();

        var formData = new FormData(user_name_form);
        
        // Use fetch to send the form data
        fetch("form/edit/usr/usrname", {
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
                console.log("username form submitted successfully");
                
                document.getElementById("profile-user-name").innerHTML = formData.get("user_name");
                
                profile_show_main();
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

    // Handle pword
    pword_form.onsubmit = (event) => {
        event.preventDefault();

        var formData = new FormData(pword_form);
        
        // Use fetch to send the form data
        fetch("form/edit/usr/pword", {
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
                console.log("pword form submitted successfully");

                profile_show_main();
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

function profile_show_main() {
    // show correct bunch
    Array.from(document.getElementsByClassName("edit-form")).forEach(element => {
        element.style.display = "none";
    });
    Array.from(document.getElementsByClassName("profile-main")).forEach(element => {
        element.style.display = "block";
    });
}

function profile_show_form() {
    // show correct bunch
    Array.from(document.getElementsByClassName("edit-form")).forEach(element => {
        element.style.display = "block";
    });
    Array.from(document.getElementsByClassName("profile-main")).forEach(element => {
        element.style.display = "none";
    });

    // --- Add data to fields ---
    var usr_first_name = document.getElementById("profile-first-name").innerHTML;
    var usr_last_name = document.getElementById("profile-last-name").innerHTML;
    var usr_name = document.getElementById("profile-user-name").innerHTML;
    var usr_email =  document.getElementById("profile-email").innerHTML;

    // Perfill forms
    document.getElementById("profile-inp-first-name").value = usr_first_name;
    document.getElementById("profile-inp-last-name").value = usr_last_name;
    document.getElementById("profile-inp-user-name").value = usr_name;
    document.getElementById("profile-inp-email").value = usr_email;

}