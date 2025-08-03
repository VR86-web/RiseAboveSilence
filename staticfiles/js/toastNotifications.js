let displayedNotificationIds = JSON.parse(localStorage.getItem("shownToastIds")) || [];

async function checkNewComments() {
    const since = localStorage.getItem("lastCheck") || new Date(Date.now() - 5 * 60000).toISOString();

    try {
        const response = await fetch("/api/new-comments/?since=" + since);
        if (!response.ok) throw new Error("Failed to fetch");

        const data = await response.json();

        data.notifications.forEach(n => {
            if (!displayedNotificationIds.includes(n.id)) {
                showToast(n);
                displayedNotificationIds.push(n.id);
            }
        });

        localStorage.setItem("shownToastIds", JSON.stringify(displayedNotificationIds));
        localStorage.setItem("lastCheck", new Date().toISOString());
    } catch (err) {
        console.error("Notification fetch failed", err);
    }
}

function showToast(notification) {
    const toast = document.createElement("div");
    toast.className = "toast-notification";

    const link = document.createElement("a");
    link.href = `/post/${notification.post_id}/details/#comment-${notification.id}`;
    link.innerHTML = notification.type === "reply"
        ? `<strong>${notification.author}</strong> replied to your comment:<br><small>${notification.content}</small>`
        : `<strong>${notification.author}</strong> commented on your post:<br><small>${notification.content}</small>`;
    link.style.color = "#fff";

    const closeBtn = document.createElement("span");
    closeBtn.className = "close-btn";
    closeBtn.innerHTML = "&times;";
    closeBtn.onclick = () => toast.remove();

    toast.appendChild(closeBtn);
    toast.appendChild(link);
    document.body.appendChild(toast);
}

document.addEventListener("DOMContentLoaded", () => {
    checkNewComments();
    setInterval(checkNewComments, 15000);
});

