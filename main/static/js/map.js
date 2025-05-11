document.addEventListener("DOMContentLoaded", function () {
    let map;
    DG.then(function () {
        map = DG.map('map', {
            center: [50.278597, 57.158513],
            zoom: 16
        });

        DG.marker([50.278597, 57.158513]).addTo(map).bindPopup("Наш автосервис");
    });
});
