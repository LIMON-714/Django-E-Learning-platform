document.addEventListener("DOMContentLoaded", function () {

    // Buttons
    const likeBtn = document.querySelector(".blog-actions .action-item:first-child");
    const shareBtn = document.querySelector(".blog-actions .action-item:nth-child(2)");

    // Blog ID from URL
    const blogId = window.location.pathname.split("/").filter(Boolean).pop();

    // CSRF token helper
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Like button click
    if (likeBtn) {
        likeBtn.addEventListener("click", async function () {
            try {
                const response = await fetch(`/blogs/${blogId}/toggle-like/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "Content-Type": "application/json",
                    },
                    credentials: "same-origin"
                });

                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const data = await response.json();

                // Update icon and color
                if (data.liked) {
                    likeBtn.querySelector("i").classList.remove("fa-regular");
                    likeBtn.querySelector("i").classList.add("fa-solid");
                    likeBtn.querySelector("i").style.color = "#0DCAF0";
                } else {
                    likeBtn.querySelector("i").classList.remove("fa-solid");
                    likeBtn.querySelector("i").classList.add("fa-regular");
                    likeBtn.querySelector("i").style.color = "";
                }

                // Update like count
                likeBtn.querySelector("span").textContent = `Like (${data.total_likes})`;
            } catch (error) {
                console.error("Like button error:", error);
                alert("Something went wrong while liking the blog. Check console for details.");
            }
        });
    }

    // Share button click
    if (shareBtn) {
        shareBtn.addEventListener("click", async function () {
            try {
                const blogUrl = window.location.href;
                const shareText = encodeURIComponent(document.title);

                // Open Facebook popup
                const facebook = `https://www.facebook.com/sharer/sharer.php?u=${blogUrl}`;
                window.open(facebook, "_blank", "width=600,height=400");
/*
                // Increment share count in backend
                const response = await fetch(`/blogs/${blogId}/add-share/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "Content-Type": "application/json",
                    },
                    credentials: "same-origin"
                });
*/
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const data = await response.json();

                shareBtn.querySelector("span").style.color = "#0dcaf0"; // info color
                shareBtn.querySelector("span").textContent = `Share (${data.total_shares})`;
            } catch (error) {
                console.error("Share button error:", error);
                alert("Something went wrong while sharing the blog. Check console for details.");
            }
        });
    }

});
