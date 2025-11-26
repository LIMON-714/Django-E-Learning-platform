// Example: highlight active sidebar item dynamically
document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll(".dashboard-nav ul li a");
    links.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add("active");
        }
    });
});
