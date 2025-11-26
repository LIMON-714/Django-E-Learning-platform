document.addEventListener("DOMContentLoaded", function () {
    const paymentMethod = document.getElementById("paymentMethod");

    const mobileDiv = document.getElementById("mobileInputDiv");
    const cardDiv = document.getElementById("cardInputDiv");
    const paypalDiv = document.getElementById("paypalInputDiv");

    // Hide all fields initially
    mobileDiv.classList.add("d-none");
    cardDiv.classList.add("d-none");
    paypalDiv.classList.add("d-none");

    paymentMethod.addEventListener("change", function () {
        const value = this.value.toLowerCase();

        // Hide all fields first
        mobileDiv.classList.add("d-none");
        cardDiv.classList.add("d-none");
        paypalDiv.classList.add("d-none");

        // Show relevant field based on selected payment method
        if (value === "bkash" || value === "nagad" || value === "rocket") {
            mobileDiv.classList.remove("d-none");
        } else if (value === "card") {
            cardDiv.classList.remove("d-none");
        } else if (value === "paypal") {
            paypalDiv.classList.remove("d-none");
        }
    });
});
