// TODO: make the buttons work, to show the correct page
document.addEventListener("DOMContentLoaded", function () {
    // hide all pages except index
    document.getElementById("index").style.display = "block";
    document.getElementById("manage").style.display = "none";
    document.getElementById("add").style.display = "none";


    // adding event listeners to buttons
    document.getElementById("dashboard-side-button").addEventListener("click", showIndex);
    document.getElementById("manage-side-button").addEventListener("click", showManage);
    document.getElementById("profile-side-button").addEventListener("click", showAdd);



    // function to show index page
    function showIndex() {
        // removing active class from all buttons
        document.querySelectorAll(".sidebar-item").forEach(function (button) {
            if (button.classList.contains("active")) {
                button.classList.remove("active");
            }
        });

        // changing the active class
        document.getElementById("dashboard-side-button").classList.add("active");

        // shows index page
        document.getElementById("index").style.display = "block";
        document.getElementById("manage").style.display = "none";
        document.getElementById("add").style.display = "none";
    }

    // function to show manage page
    function showManage() {
        // removing active class from all buttons
        document.querySelectorAll(".sidebar-item").forEach(function (button) {
            if (button.classList.contains("active")) {
                button.classList.remove("active");
            }
        });

        // changing the active class
        document.getElementById("manage-side-button").classList.add("active");

        document.getElementById("index").style.display = "none";
        document.getElementById("manage").style.display = "block";
        document.getElementById("add").style.display = "none";
    }

    // function to show add page
    function showAdd() {
        // removing active class from all buttons
        document.querySelectorAll(".sidebar-item").forEach(function (button) {
            if (button.classList.contains("active")) {
                button.classList.remove("active");
            }
        });
    
        // changing the active class
        document.getElementById("profile-side-button").classList.add("active");

        document.getElementById("index").style.display = "none";
        document.getElementById("manage").style.display = "none";
        document.getElementById("add").style.display = "block";
    }

});