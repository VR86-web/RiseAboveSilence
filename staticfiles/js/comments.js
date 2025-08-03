document.addEventListener("DOMContentLoaded", function () {
    // Toggle Comments Section
    document.querySelectorAll(".show-comments-btn").forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            let postId = this.getAttribute("data-post-id");
            let commentSection = document.getElementById("comments-" + postId);
            let commentCount = commentSection.querySelectorAll(".comment-area-box").length;

            if (commentSection.style.display === "none" || commentSection.style.display === "") {
                commentSection.style.display = "block";
                this.textContent = "Hide Comments (" + (commentCount || "No") + ")";
            } else {
                commentSection.style.display = "none";
                this.textContent = "Show Comments (" + (commentCount || "No") + ")";
            }
        });
    });

    // Toggle "Leave a Comment" Form
    document.querySelectorAll(".leave-comment-btn").forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            let postId = this.getAttribute("data-post-id");
            let commentForm = document.getElementById("comment-form-" + postId);

            if (commentForm.style.display === "none" || commentForm.style.display === "") {
                commentForm.style.display = "block";
                this.textContent = "Cancel Comment";
            } else {
                commentForm.style.display = "none";
                this.textContent = "Leave a comment";
            }
        });
    });

    // Toggle Reply Form
    document.querySelectorAll(".reply-btn").forEach(function (button) {
        button.addEventListener("click", function () {
            let commentId = this.getAttribute("data-comment-id");
            let replyForm = document.getElementById("reply-form-" + commentId);

            if (replyForm.style.display === "none" || replyForm.style.display === "") {
                replyForm.style.display = "block";
                this.textContent = "Cancel Reply";
            } else {
                replyForm.style.display = "none";
                this.textContent = "Reply";
            }
        });
    });
});