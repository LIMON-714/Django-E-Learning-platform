// Profile Image Live Preview
document.getElementById("imageInput").addEventListener("change", function(e) {
    const reader = new FileReader();
    reader.onload = function() {
        document.getElementById("previewImage").src = reader.result;
    };
    reader.readAsDataURL(e.target.files[0]);
});
