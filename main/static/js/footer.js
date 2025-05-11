document.getElementById('year').textContent = new Date().getFullYear();

const scrollTopBtn = document.getElementById('scrollTop');
window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
        scrollTopBtn.style.display = 'block';
    } else {
        scrollTopBtn.style.display = 'none';
    }
});
scrollTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

document.addEventListener("DOMContentLoaded", function () {
    const aboutLink = document.getElementById("about-link");

    if (aboutLink) {
        aboutLink.addEventListener("click", function (event) {
            event.preventDefault();

            if (window.location.pathname === "/") {
                scrollToAbout();
            } else {
                sessionStorage.setItem("scrollToAbout", "true");
                window.location.href = "/";
            }
        });
    }

    if (sessionStorage.getItem("scrollToAbout") === "true") {
        sessionStorage.removeItem("scrollToAbout");
        setTimeout(scrollToAbout, 500);
    }

    function scrollToAbout() {
        const aboutSection = document.getElementById("about");
        if (aboutSection) {
            const offset = 150;
            const elementPosition = aboutSection.getBoundingClientRect().top + window.scrollY;
            const offsetPosition = elementPosition - offset;

            window.scrollTo({
                top: offsetPosition,
                behavior: "smooth"
            });
        }
    }
});
