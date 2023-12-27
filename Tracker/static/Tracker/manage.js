document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM loaded!, from manage.js");

    document.getElementById("manage-side-button").addEventListener("click", getManageData);
    //getManageData();

});

function getManageData() {
    const fetchManageData = async () => {
        try {
            const response = await fetch('/data/manage');
            const data = await response.json();
            console.log(data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
    fetchManageData();
}