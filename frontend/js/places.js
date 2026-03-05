import { api } from "./api.js";

let debounce = null;

async function loadPlaces(q = "") {
  const grid = document.getElementById("places-grid");
  try {
    const places = await api.places.list(q);
    if (!places.length) { grid.innerHTML = `<p class="muted">No places found.</p>`; return; }
    grid.innerHTML = places.map(p => `
      <div class="place-card" onclick="window.location='/checkin.html?place=${p.id}'">
        <h3>${p.name}</h3>
        <p>${p.address ?? (p.is_custom ? "Custom place" : "")}</p>
      </div>
    `).join("");
  } catch (err) {
    grid.innerHTML = `<p class="error">${err.message}</p>`;
  }
}

document.getElementById("search-places")?.addEventListener("input", (e) => {
  clearTimeout(debounce);
  debounce = setTimeout(() => loadPlaces(e.target.value.trim()), 300);
});

loadPlaces();
