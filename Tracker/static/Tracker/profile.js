document.addEventListener("DOMContentLoaded", () => {
    const hideEditForms = () => {
        document.querySelectorAll(".edit-form").forEach(element => {
            element.style.display = "none";
        });
        document.querySelectorAll(".profile-main").forEach(element => {
            element.style.display = "block";
        });
    };

    const showEditForms = () => {
        document.querySelectorAll(".edit-form").forEach(element => {
            element.style.display = "block";
        });
        document.querySelectorAll(".profile-main").forEach(element => {
            element.style.display = "none";
        });

        // add data to input
    };

    const showMainProfile = () => {
        hideEditForms();
    };

    const handleFormSubmission = (form, url, successCallback) => {
        form.addEventListener("submit", (event) => {
            event.preventDefault();

            const formData = new FormData(form);

            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken")
                    // Add any other headers if needed
                }
            })
            .then(response => {
                if (response.ok) {
                    successCallback(formData);
                } else {
                    console.error("Form submission failed with status: " + response.status);
                }
            })
            .catch(error => {
                console.error("Network error occurred while submitting the form:", error);
            });
        });
    };

    const handleNameFormSubmission = (formData) => {
        console.log("name form submitted successfully");

        document.getElementById("profile-first-name").innerHTML = formData.get("first_name");
        document.getElementById("profile-last-name").innerHTML = formData.get("last_name");

        showMainProfile();
    };

    const handleEmailFormSubmission = (formData) => {
        console.log("email form submitted successfully");

        document.getElementById("profile-email").innerHTML = formData.get("email");

        showMainProfile();
    };

    const handleUserNameFormSubmission = (formData) => {
        console.log("username form submitted successfully");

        document.getElementById("profile-user-name").innerHTML = formData.get("user_name");

        showMainProfile();
    };

    const handlePasswordFormSubmission = () => {
        console.log("pword form submitted successfully");

        showMainProfile();
    };

    // Initial setup
    hideEditForms();

    document.getElementById("profile-show-edit").addEventListener("click", () => {
        profile_show_form();
    });

    document.getElementById("profile-show-main").addEventListener("click", showMainProfile);

    // Handle forms
    handleFormSubmission(document.getElementById("profile-name-edit-form"), "form/edit/usr/name", handleNameFormSubmission);
    handleFormSubmission(document.getElementById("profile-email-edit-form"), "form/edit/usr/email", handleEmailFormSubmission);
    handleFormSubmission(document.getElementById("profile-user-name-edit-form"), "form/edit/usr/usrname", handleUserNameFormSubmission);
    handleFormSubmission(document.getElementById("profile-password-edit-form"), "form/edit/usr/pword", handlePasswordFormSubmission);

});

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