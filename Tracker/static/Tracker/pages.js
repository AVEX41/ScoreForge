// TODO: make the buttons work, to show the correct page
document.addEventListener("DOMContentLoaded", function () {
    // hide all pages except dashboard
    document.getElementById("dashboard").style.display = "block";
    document.getElementById("manage").style.display = "none";
    document.getElementById("profile").style.display = "none";
    document.getElementById("new").style.display = "none";


    // adding event listeners to buttons
    document.getElementById("dashboard-side-button").addEventListener("click", function () {showPage("dashboard");});
    document.getElementById("manage-side-button").addEventListener("click", function () {showPage("manage");});
    document.getElementById("profile-side-button").addEventListener("click", function () {showPage("profile");});
    document.getElementById("new-side-button").addEventListener("click", function () {showPage("new");});
    document.getElementById("manage-new-button").addEventListener("click", function () {showPage("new");});
});

function showPage(page) {
    console.log("showing " + page);
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

    // changing the active class
    try {
    document.getElementById(page + "-side-button").classList.add("active");
    } catch (error) {
        
    }
}