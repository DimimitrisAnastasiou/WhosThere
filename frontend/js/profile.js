import { api } from "./api.js";
import { sb } from "./auth.js";

async function loadProfile() {
  const params = new URLSearchParams(window.location.search);
  const username = params.get("u");

  try {
    let user;
    if (username) {
      user = await api.users.getByUsername(username);
    } else {
      const { data: { session } } = await sb.auth.getSession();
      if (!session) { window.location.href = "/"; return; }
      user = await api.users.me();
    }

    document.getElementById("profile-name").textContent = user.display_name ?? user.username ?? "User";
    document.getElementById("profile-username").textContent = user.username ? `@${user.username}` : "";
    const avatarEl = document.getElementById("profile-avatar");
    if (user.avatar_url) { avatarEl.src = user.avatar_url; }
    else { avatarEl.style.display = "none"; }

    const checkins = await api.checkins.list({ limit: 50 });
    const userCheckins = checkins.filter(c => c.user.id === user.id && !c.is_anonymous);
    const feed = document.getElementById("profile-feed");

    if (!userCheckins.length) { feed.innerHTML = `<p class="muted">No public check-ins yet.</p>`; return; }

    feed.innerHTML = userCheckins.map(c => `
      <div class="checkin-card">
        <div class="checkin-body">
          <div class="checkin-place"><a href="/places.html?id=${c.place.id}">${c.place.name}</a></div>
          ${c.note ? `<div class="checkin-note">${c.note}</div>` : ""}
          <div class="checkin-meta">${new Date(c.created_at).toLocaleDateString()}</div>
        </div>
      </div>
    `).join("");
  } catch (err) {
    document.getElementById("profile-feed").innerHTML = `<p class="error">${err.message}</p>`;
  }
}

loadProfile();
