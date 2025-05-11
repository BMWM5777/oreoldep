document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const searchResults = document.getElementById("search-results");
    const searchResultsContainer = document.getElementById("search-results-container");

    // 1) При вводе текста в поле
    searchInput.addEventListener("input", function () {
        const query = searchInput.value.trim();

        // Если поле пустое, скрываем оба контейнера и выходим
        if (!query) {
            searchResults.innerHTML = "";
            searchResults.classList.add("hidden");
            searchResultsContainer.innerHTML = "";
            searchResultsContainer.classList.add("hidden");
            return;
        }

        // Иначе делаем fetch и показываем быстрые результаты
        fetch(`/search/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                // Очищаем быстрые результаты
                searchResults.innerHTML = "";

                if (data.results.length > 0) {
                    data.results.forEach(item => {
                        const li = document.createElement("li");
                        li.innerHTML = `<i class="fas fa-search"></i> ${item.name}`;
                        li.dataset.url = item.url;
                        li.classList.add("search-item");
                        li.addEventListener("click", function () {
                            window.location.href = this.dataset.url;
                        });
                        searchResults.appendChild(li);
                    });
                    searchResults.classList.remove("hidden");
                } else {
                    const li = document.createElement("li");
                    li.textContent = "❌ Нет результатов";
                    li.classList.add("no-results");
                    searchResults.appendChild(li);
                    searchResults.classList.remove("hidden");
                }
            });
    });

    searchInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && searchInput.value.trim() !== "") {
            fetch(`/search/?q=${searchInput.value.trim()}`)
                .then(response => response.json())
                .then(data => {
                    searchResults.classList.add("hidden");
                    searchResults.innerHTML = "";
                    searchResultsContainer.innerHTML = "";
                    searchResultsContainer.classList.remove("hidden");

                    if (data.results.length > 0) {
                        let html = "<h3>Результаты поиска:</h3><div class='search-results-grid'>";
                        data.results.forEach(item => {
                            html += `
                                <div class="search-item-card">
                                    <a href="${item.url}">
                                        <img src="${item.image}" alt="${item.name}">
                                        <p>${item.name}</p>
                                    </a>
                                </div>
                            `;
                        });
                        html += "</div>";
                        searchResultsContainer.innerHTML = html;
                    } else {
                        searchResultsContainer.innerHTML = "<p class='no-results'>❌ Нет результатов</p>";
                    }
                });
        }
    });

    document.addEventListener("click", function (event) {
        if (
            !searchInput.contains(event.target) &&
            !searchResults.contains(event.target) &&
            !searchResultsContainer.contains(event.target)
        ) {
            searchResults.classList.add("hidden");
            searchResultsContainer.classList.add("hidden");
        }
    });
});
