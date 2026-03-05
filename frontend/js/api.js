import { CONFIG } from "./config.js";
import { getToken } from "./auth.js";

const BASE = CONFIG.API_URL;

async function request(method, path, body = null) {
  const token = await getToken();
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  if (res.status === 204) return null;
  return res.json();
}

// ── CheckIns ────────────────────────────────────────────────────────────────
export const api = {
  checkins: {
    list: (params = {}) => {
      const qs = new URLSearchParams(params).toString();
      return request("GET", `/api/checkins${qs ? "?" + qs : ""}`);
    },
    create: (data) => request("POST", "/api/checkins", data),
    delete: (id) => request("DELETE", `/api/checkins/${id}`),
  },

  // ── Places ─────────────────────────────────────────────────────────────────
  places: {
    list: (q = "") => request("GET", `/api/places${q ? `?q=${encodeURIComponent(q)}` : ""}`),
    get: (id) => request("GET", `/api/places/${id}`),
    search: (q) => request("GET", `/api/places/search?q=${encodeURIComponent(q)}`),
    create: (data) => request("POST", "/api/places", data),
  },

  // ── Users ──────────────────────────────────────────────────────────────────
  users: {
    me: () => request("GET", "/api/users/me"),
    upsertMe: (data) => request("POST", "/api/users/me", data),
    updateMe: (data) => request("PATCH", "/api/users/me", data),
    getByUsername: (username) => request("GET", `/api/users/${username}`),
  },
};
