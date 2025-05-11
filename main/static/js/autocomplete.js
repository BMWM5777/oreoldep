document.addEventListener('DOMContentLoaded', function() {
    const debounce = (func, wait) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    };

    const initAutocomplete = (inputElement) => {
        const container = inputElement.closest('.autocomplete');
        const itemsDiv = container.querySelector('.autocomplete-items');

        const fetchSuggestions = async (value) => {
            try {
                const response = await fetch(`/cities/autocomplete/?term=${encodeURIComponent(value)}`);
                return await response.json();
            } catch (error) {
                console.error('Ошибка запроса:', error);
                return [];
            }
        };

        const showSuggestions = (items) => {
            itemsDiv.innerHTML = '';
            items.forEach(item => {
                const div = document.createElement('div');
                div.className = 'autocomplete-item';
                div.innerHTML = `
                    <div class="city-name">${item.name}</div>
                    <div class="postal-code">${item.postal}</div>
                `;
                div.onclick = () => {
                    inputElement.value = item.name;
                    document.getElementById('id_postal_code').value = item.postal;
                    itemsDiv.style.display = 'none';
                };
                itemsDiv.appendChild(div);
            });
            itemsDiv.style.display = items.length ? 'block' : 'none';
        };

        inputElement.addEventListener('input', debounce(async (e) => {
            const value = e.target.value.trim();
            if (value.length < 2) {
                itemsDiv.style.display = 'none';
                return;
            }
            
            const suggestions = await fetchSuggestions(value);
            showSuggestions(suggestions);
        }, 300));

        document.addEventListener('click', (e) => {
            if (!container.contains(e.target)) {
                itemsDiv.style.display = 'none';
            }
        });
    };

    // Инициализация для обоих полей
    const cityInput = document.getElementById('id_city');
    const postalInput = document.getElementById('id_postal_code');

    if (cityInput) initAutocomplete(cityInput);
    if (postalInput) initAutocomplete(postalInput);
});