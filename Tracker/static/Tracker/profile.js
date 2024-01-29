document.addEventListener("DOMContentLoaded", () => {
    Array.from(document.getElementsByClassName("edit-form")).forEach(element => {
        element.style.display = "none";
    });
});

function profile_show_main(field) {
    console.log(field);
}

function profile_show_form(field) {
    console.log(field);
}