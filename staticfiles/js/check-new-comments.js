
    let unreadNotifications = [];

    async function checkNewComments() {
    const since = localStorage.getItem('lastCheck') || new Date(Date.now() - 5 * 60000).toISOString();

    try {
    const response = await fetch("/api/new-comments/?since=" + since);
    if (!response.ok) throw new Error("Failed to fetch");

    const data = await response.json();
    console.log("Fetched notifications:", data);

    data.notifications.forEach(n => {
    if (!unreadNotifications.some(item => item.id === n.id)) {
    unreadNotifications.push(n);
}
});

    // Update badge
    const badge = document.getElementById("notif-badge");
    if (unreadNotifications.length > 0) {
    badge.innerText = unreadNotifications.length;
    badge.style.display = "inline-block";
} else {
    badge.style.display = "none";
}

    localStorage.setItem("unreadNotifications", JSON.stringify(unreadNotifications));
    localStorage.setItem("lastCheck", new Date().toISOString());
} catch (err) {
    console.error("Notification fetch failed", err);
}
}

    function renderNotificationMenu() {
    const menu = document.getElementById("notif-menu");
    menu.innerHTML = "";

    if (unreadNotifications.length === 0) {
    const empty = document.createElement("span");
    empty.className = "dropdown-item text-muted";
    empty.textContent = "No new notifications";
    menu.appendChild(empty);
    return;
}

    unreadNotifications.forEach(n => {
    const link = document.createElement("a");
    link.className = "dropdown-item";
    link.href = `/post/${n.post_id}/details/#comment-${n.id}`;
    const msg = n.type === "reply"
    ? `<strong>${n.author}</strong> replied to your comment:`
    : `<strong>${n.author}</strong> commented on your post:`;
    link.innerHTML = `${msg}<br><small>${n.content}</small>`;
    menu.appendChild(link);
});
}

    // Attach events
    document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("notifDropdown").addEventListener("click", renderNotificationMenu);
    checkNewComments();
    setInterval(checkNewComments, 15000);
});


