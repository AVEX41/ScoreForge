// TODO: make the buttons work, to show the correct page
document.addEventListener("DOMContentLoaded", function () {
    // adding event listeners to buttons
    document.getElementById("dashboard-side-button").addEventListener("click", function () {showPage("dashboard");});
    document.getElementById("manage-side-button").addEventListener("click", function () {showManage()});
    document.getElementById("profile-side-button").addEventListener("click", function () {showPage("profile"); hideEditForms()});

    showPage("dashboard");
});

function showPage(page) {
    // removing active class from all buttons
    document.querySelectorAll(".sidebar-item").forEach(function (button) {
        if (button.classList.contains("active")) {
            button.classList.remove("active");
        }
    });

    // making all pages invisible
    document.querySelectorAll(".main-page").forEach(function (page) {
        page.style.display = "none";
    });

    // showing the correct page
    document.getElementById(page).style.display = "block";

    // changing the active class, if it is not a side button, then manage is active
    try {
        document.getElementById(page + "-side-button").classList.add("active");
    } catch (error) {
        document.getElementById("manage-side-button").classList.add("active");
    }
}