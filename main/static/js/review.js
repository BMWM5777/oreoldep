document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".star-rating label");
    const ratingInput = document.getElementById("id_rating");

    stars.forEach((star, index) => {
        star.addEventListener("click", function () {
            const value = 5 - index;  // Исправляем порядок (1 слева, 5 справа)
            ratingInput.value = value;
            highlightStars(value);
        });

        star.addEventListener("mouseover", function () {
            highlightStars(5 - index);
        });

        star.parentNode.addEventListener("mouseleave", function () {
            highlightStars(parseInt(ratingInput.value));
        });
    });

    function highlightStars(count) {
        stars.forEach((star, i) => {
            star.style.color = i >= 5 - count ? "gold" : "#ddd";
        });
    }
});
