
document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', () => {
        const postId = button.dataset.postId;

        fetch(`/api/posts/${postId}/like/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById(`like-count-${postId}`).textContent = data.like_count;
            // Optional: Change icon color on like/unlike
            if (data.liked) {
                button.querySelector('i').style.color = 'red';
            } else {
                button.querySelector('i').style.color = '';
            }
        });
    });
});

// CSRF helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

