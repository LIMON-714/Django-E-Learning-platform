document.addEventListener("DOMContentLoaded", function () {

    /* ===============================
       ENROLLMENT MODAL
    =============================== */
    const enrollModal = document.getElementById("enrollModal");
    const btnEnroll = document.getElementById("btn-request-course");
    const closeModal = document.querySelector(".close-modal");
    const enrollForm = document.getElementById("enrollForm");

    // Open modal
    btnEnroll?.addEventListener("click", () => {
        enrollModal.classList.add("show");
    });

    // Close modal with (X)
    closeModal?.addEventListener("click", () => {
        enrollModal.classList.remove("show");
    });

    // Close modal if clicking outside
    enrollModal?.addEventListener("click", function (e) {
        if (e.target === enrollModal) {
            enrollModal.classList.remove("show");
        }
    });

    /* ===============================
       FORM SUBMISSION
       (Django will handle POST → redirect)
    =============================== */
    enrollForm?.addEventListener("submit", function () {
        console.log("Form submitted → Django will redirect to payment page.");
        // DO NOT preventDefault!
    });

    /* ===============================
       REVIEW SLIDER
    =============================== */
    const scrollLeftBtn = document.getElementById("scroll-left");
    const scrollRightBtn = document.getElementById("scroll-right");
    const reviewWrapper = document.querySelector(".reviews-wrapper");

    if (reviewWrapper) {
        const cards = Array.from(reviewWrapper.children);
        let index = 0;

        function showReview(i) {
            if (i < 0) index = cards.length - 1;
            else if (i >= cards.length) index = 0;
            else index = i;

            const card = cards[0];
            const style = window.getComputedStyle(card);
            const marginRight = parseFloat(style.marginRight);
            const totalWidth = card.offsetWidth + marginRight;

            reviewWrapper.style.transform = `translateX(-${index * totalWidth}px)`;
        }

        scrollLeftBtn?.addEventListener("click", () => showReview(index - 1));
        scrollRightBtn?.addEventListener("click", () => showReview(index + 1));

        showReview(0);
        window.addEventListener("resize", () => showReview(index));
    }

});
