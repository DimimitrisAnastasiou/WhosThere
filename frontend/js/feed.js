import { api } from "./api.js";

function timeAgo(dateStr) {
  const diff = (Date.now() - new Date(dateStr)) / 1000;
  if (diff < 60) return "just now";
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

function renderCheckin(c) {
  const isAnon = c.is_anonymous || c.user.is_anonymous;
  const name = isAnon ? "Anonymous" : (c.user.display_name ?? "Someone");
  const avatar = isAnon ? "👤" : (c.user.avatar_url
    ? `<img class="avatar" src="${c.user.avatar_url}" alt="${name}" />`
    : `<div class="avatar">${name[0]}</div>`);

  return `
    <div class="checkin-card">
      ${typeof avatar === "string" && avatar.startsWith("<img") ? avatar : `<div class="avatar">${avatar}</div>`}
      <div class="checkin-body">
        <div class="checkin-place">
          ${name} checked into <a href="/places.html?id=${c.place.id}">${c.place.name}</a>
        </div>
        ${c.note ? `<div class="checkin-note">${c.note}</div>` : ""}
        <div class="checkin-meta">${timeAgo(c.created_at)}${c.place.address ? ` · ${c.place.address}` : ""}</div>
      </div>
    </div>
  `;
}

async function loadFeed() {
  const feed = document.getElementById("feed");
  if (!feed) return;

  try {
    const checkins = await api.checkins.list({ limit: 30 });
    if (!checkins.length) {
      feed.innerHTML = `<p class="muted">No check-ins yet. Be the first!</p>`;
      return;
    }
    feed.innerHTML = checkins.map(renderCheckin).join("");
  } catch (err) {
    feed.innerHTML = `<p class="error">Could not load feed: ${err.message}</p>`;
  }
}

loadFeed();
