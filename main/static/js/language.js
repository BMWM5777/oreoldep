document.addEventListener("DOMContentLoaded", function() {
    const selects = document.querySelectorAll(".language-select");
    
    selects.forEach(select => {
        function updateFlag() {
            const selectedOption = select.options[select.selectedIndex];
            const flagUrl = selectedOption.getAttribute("data-flag");
            select.style.backgroundImage = `url('${flagUrl}')`;
        }
        
        select.addEventListener("change", updateFlag);
        updateFlag();
    });
});
