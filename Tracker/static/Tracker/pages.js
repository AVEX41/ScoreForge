// TODO: make the buttons work, to show the correct page
document.addEventListener("DOMContentLoaded", function () {
    // hide all pages except index
    document.getElementById("index").style.display = "block";
    document.getElementById("manage").style.display = "none";
    document.getElementById("add").style.display = "none";
});

// function to show index page
function showIndex() {
    document.getElementById("index").style.display = "block";
    document.getElementById("manage").style.display = "none";
    document.getElementById("add").style.display = "none";
    console.log("index shown");
}

// function to show manage page
function showManage() {
    document.getElementById("index").style.display = "none";
    document.getElementById("manage").style.display = "block";
    document.getElementById("add").style.display = "none";
}

// function to show add page
function showAdd() {
    document.getElementById("index").style.display = "none";
    document.getElementById("manage").style.display = "none";
    document.getElementById("add").style.display = "block";
}

