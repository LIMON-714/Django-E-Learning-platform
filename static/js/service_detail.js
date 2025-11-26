// =====================
// Modal Functionality
// =====================

// Get modal elements
const requestBtn = document.getElementById('requestServiceBtn');
const serviceModal = document.getElementById('serviceModal');
const closeModal = document.getElementById('closeModal');
const backdrop = document.querySelector('.service-modal-backdrop');
const form = document.querySelector('.service-form');

// Open modal
if (requestBtn) {
    requestBtn.addEventListener('click', () => {
        serviceModal.classList.add('show');
    });
}

// Close modal button
if (closeModal) {
    closeModal.addEventListener('click', () => {
        serviceModal.classList.remove('show');
    });
}

// Close modal when clicking backdrop
if (backdrop) {
    backdrop.addEventListener('click', () => {
        serviceModal.classList.remove('show');
    });
}

// =====================
// AJAX Form Submission
// =====================

if (form) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Remove old feedback
        const oldFeedback = form.querySelector('.form-feedback');
        if (oldFeedback) oldFeedback.remove();

        // Create feedback message
        let feedback = document.createElement('div');
        feedback.className = 'form-feedback';
        feedback.textContent = 'Sending...';
        form.appendChild(feedback);

        // Submit form
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => {
            if(response.ok){
                form.reset();
                feedback.textContent = 'Sent!';

                // Auto close modal after 1.5s
                setTimeout(() => {
                    serviceModal.classList.remove('show');
                    feedback.remove();
                }, 1500);

            } else {
                feedback.textContent = 'Error! Please try again.';
            }
        })
        .catch(error => {
            console.error(error);
            feedback.textContent = 'Error! Please try again.';
        });
    });
}



// =====================
// Review Slider
// =====================

document.addEventListener("DOMContentLoaded", function () {
    let reviews = document.querySelectorAll(".single-review");
    let currentIndex = 0;

    if (reviews.length > 0) {
        reviews[0].classList.add("active");
    }

    function showReview(i) {
        reviews.forEach(r => r.classList.remove("active"));
        reviews[i].classList.add("active");
    }

    const btnPrev = document.getElementById("review-prev");
    const btnNext = document.getElementById("review-next");

    if (btnPrev && btnNext) {
        btnPrev.addEventListener("click", () => {
            currentIndex = (currentIndex - 1 + reviews.length) % reviews.length;
            showReview(currentIndex);
        });

        btnNext.addEventListener("click", () => {
            currentIndex = (currentIndex + 1) % reviews.length;
            showReview(currentIndex);
        });
    }
});
