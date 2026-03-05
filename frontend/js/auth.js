import { CONFIG } from "./config.js";

const { createClient } = supabase; // loaded from CDN
export const sb = createClient(CONFIG.SUPABASE_URL, CONFIG.SUPABASE_ANON_KEY);

// ── Token helper (used by api.js) ────────────────────────────────────────────
export async function getToken() {
  const { data } = await sb.auth.getSession();
  return data?.session?.access_token ?? null;
}

// ── Render nav auth section ──────────────────────────────────────────────────
async function renderNav() {
  const navAuth = document.getElementById("nav-auth");
  if (!navAuth) return;

  const { data: { session } } = await sb.auth.getSession();

  if (session) {
    const user = session.user;
    const name = user.user_metadata?.full_name?.split(" ")[0] ?? "Me";
    navAuth.innerHTML = `
      <a href="/checkin.html" class="btn btn-primary" style="padding:6px 14px">+ Check In</a>
      <a href="/profile.html">${name}</a>
      <a href="#" id="btn-logout">Logout</a>
    `;
    document.getElementById("btn-logout")?.addEventListener("click", async (e) => {
      e.preventDefault();
      await sb.auth.signOut();
      window.location.href = "/";
    });

    // Show check-in hero if on home page
    document.getElementById("hero")?.classList.remove("hidden");

    // Upsert user row on backend (fire and forget)
    try {
      const { default: { api } } = await import("./api.js");
      await api.users.upsertMe({
        supabase_id: user.id,
        display_name: user.user_metadata?.full_name,
        avatar_url: user.user_metadata?.avatar_url,
      });
    } catch (_) {}

  } else {
    navAuth.innerHTML = `<button id="btn-login" class="btn btn-secondary" style="padding:6px 14px">Login with Google</button>`;
    document.getElementById("btn-login")?.addEventListener("click", async () => {
      await sb.auth.signInWithOAuth({
        provider: "google",
        options: { redirectTo: window.location.origin },
      });
    });
  }
}

renderNav();
