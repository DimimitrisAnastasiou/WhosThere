import { api } from "./api.js";

let selectedPlace = null;
let searchTimeout = null;

const searchInput = document.getElementById("place-search");
const suggestions = document.getElementById("place-suggestions");
const selectedEl = document.getElementById("selected-place");
const selectedName = document.getElementById("selected-place-name");
const clearBtn = document.getElementById("clear-place");
const submitBtn = document.getElementById("btn-submit");
const noteInput = document.getElementById("checkin-note");
const anonCheck = document.getElementById("checkin-anonymous");
const errorEl = document.getElementById("checkin-error");

// ── Place search ─────────────────────────────────────────────────────────────
searchInput?.addEventListener("input", () => {
  clearTimeout(searchTimeout);
  const q = searchInput.value.trim();
  if (q.length < 2) { suggestions.classList.add("hidden"); return; }

  searchTimeout = setTimeout(async () => {
    try {
      const results = await api.places.search(q);
      renderSuggestions(results);
    } catch {
      // silently fail on search
    }
  }, 300);
});

function renderSuggestions(results) {
  if (!results.length) { suggestions.classList.add("hidden"); return; }
  suggestions.innerHTML = results.map(r => `
    <li data-id='${JSON.stringify(r)}'>
      <div>${r.name}</div>
      <div class="suggestion-address">${r.address ?? ""}</div>
    </li>
  `).join("");
  suggestions.classList.remove("hidden");
}

suggestions?.addEventListener("click", async (e) => {
  const li = e.target.closest("li");
  if (!li) return;
  const place = JSON.parse(li.dataset.id);

  // Persist place to DB then select it
  try {
    const saved = await api.places.create({
      name: place.name,
      google_place_id: place.google_place_id,
      address: place.address,
      lat: place.lat,
      lng: place.lng,
    });
    selectPlace(saved);
  } catch (err) {
    showError(err.message);
  }
});

function selectPlace(place) {
  selectedPlace = place;
  searchInput.value = "";
  suggestions.classList.add("hidden");
  selectedName.textContent = place.name;
  selectedEl.classList.remove("hidden");
  searchInput.parentElement.querySelector("input").classList.add("hidden");
  submitBtn.disabled = false;
}

clearBtn?.addEventListener("click", () => {
  selectedPlace = null;
  selectedEl.classList.add("hidden");
  searchInput.classList.remove("hidden");
  submitBtn.disabled = true;
});

// ── Custom place ──────────────────────────────────────────────────────────────
document.getElementById("create-custom")?.addEventListener("click", (e) => {
  e.preventDefault();
  document.getElementById("custom-place-form").classList.toggle("hidden");
});

document.getElementById("btn-add-custom")?.addEventListener("click", async () => {
  const name = document.getElementById("custom-name").value.trim();
  const address = document.getElementById("custom-address").value.trim();
  if (!name) return;

  try {
    const saved = await api.places.create({ name, address, is_custom: true });
    selectPlace(saved);
    document.getElementById("custom-place-form").classList.add("hidden");
  } catch (err) {
    showError(err.message);
  }
});

// ── Submit check-in ───────────────────────────────────────────────────────────
submitBtn?.addEventListener("click", async () => {
  if (!selectedPlace) return;
  submitBtn.disabled = true;
  hideError();

  try {
    await api.checkins.create({
      place_id: selectedPlace.id,
      note: noteInput.value.trim() || null,
      is_anonymous: anonCheck.checked,
    });
    window.location.href = "/";
  } catch (err) {
    showError(err.message);
    submitBtn.disabled = false;
  }
});

function showError(msg) { errorEl.textContent = msg; errorEl.classList.remove("hidden"); }
function hideError() { errorEl.classList.add("hidden"); }
