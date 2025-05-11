document.addEventListener("DOMContentLoaded", function () {
    const mainImage = document.querySelectorAll('.product-image');
    const thumbnails = document.querySelectorAll('.thumbnail');

    thumbnails.forEach((thumb, index) => {
        thumb.addEventListener("click", function () {
            mainImage.forEach(img => img.classList.remove("active"));
            thumbnails.forEach(thumb => thumb.classList.remove("selected"));
            mainImage[index].classList.add("active");
            this.classList.add("selected");
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const contentEl = document.getElementById('desc-content');
    const btn = document.getElementById('toggle-desc-btn');
    if (!contentEl || !btn) return;
  
    const fullText = contentEl.innerText.trim();
    const words = fullText.split(/\s+/);
  
    if (words.length > 50) {
      const shortText = words.slice(0, 50).join(' ') + '...';
      contentEl.innerText = shortText;
      btn.style.display = 'inline-block';
  
      let isExpanded = false;
      btn.addEventListener('click', function() {
        if (isExpanded) {
          contentEl.innerText = shortText;
          btn.innerText = 'Показать полностью';
        } else {
          contentEl.innerText = fullText;
          btn.innerText = 'Скрыть';
        }
        isExpanded = !isExpanded;
      });
    }
  });
  