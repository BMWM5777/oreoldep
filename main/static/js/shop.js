document.addEventListener("DOMContentLoaded", function () {
    const sortButton = document.getElementById("sort-button");
    const sortOptions = document.getElementById("sort-options");

    const translations = {
        "ru": {
            "price_desc": "По убыванию цены",
            "price_asc": "По возрастанию цены",
            "newest": "По свежести (новые)",
            "oldest": "По свежести (старые)",
            "default": "Сортировать ▼"
        },
        "kk": {
            "price_desc": "Баға бойынша кему",
            "price_asc": "Баға бойынша өсу",
            "newest": "Жаңасы бірінші",
            "oldest": "Ескісі бірінші",
            "default": "Сұрыптау ▼"
        }
    };

    const currentLang = document.documentElement.lang || "ru";

    sortButton.addEventListener("click", function (event) {
        event.stopPropagation();
        sortOptions.style.display = (sortOptions.style.display === "block") ? "none" : "block";
    });

    document.addEventListener("click", function (event) {
        if (!sortButton.contains(event.target) && !sortOptions.contains(event.target)) {
            sortOptions.style.display = "none";
        }
    });

    const urlParams = new URLSearchParams(window.location.search);
    const currentSort = urlParams.get("sort") || "default";

    sortButton.innerText = translations[currentLang][currentSort] || translations["ru"]["default"];

    document.querySelectorAll("#sort-options li").forEach(function (option) {
        option.addEventListener("click", function () {
            const sortValue = this.getAttribute("data-sort");
            urlParams.set("sort", sortValue);
            urlParams.set("page", 1);
            window.location.search = urlParams.toString();
        });
    });
});





// shop.js
document.addEventListener('DOMContentLoaded', function() {
    // Бургер меню категорий
    const categoryBurger = document.querySelector('.category-burger');
    const sidebar = document.querySelector('.sidebar');
    const sidebarOverlay = document.createElement('div');
    sidebarOverlay.className = 'sidebar-overlay';
    document.body.appendChild(sidebarOverlay);

    categoryBurger.addEventListener('click', () => {
        sidebar.classList.toggle('active');
        sidebarOverlay.style.display = 'block';
    });

    sidebarOverlay.addEventListener('click', () => {
        sidebar.classList.remove('active');
        sidebarOverlay.style.display = 'none';
    });

    // Закрытие меню при клике вне области
    document.addEventListener('click', (e) => {
        if (!sidebar.contains(e.target) && !categoryBurger.contains(e.target)) {
            sidebar.classList.remove('active');
            sidebarOverlay.style.display = 'none';
        }
    });

    // Обработчик сортировки
    const sortButton = document.getElementById('sort-button');
    const sortOptions = document.getElementById('sort-options');

    sortButton.addEventListener('click', (e) => {
        e.stopPropagation();
        sortOptions.classList.toggle('hidden');
    });

    document.addEventListener('click', () => {
        sortOptions.classList.add('hidden');
    });
});