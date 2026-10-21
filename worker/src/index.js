// Stores the Saturday-test logger's sessions so they can be read back later, from anywhere.
// PUT  /sessions/<gateway>/<session>   the logger's whole session as JSON (replaces the last copy)
// GET  /sessions                       every stored session, newest first, with counts
// GET  /sessions/latest                the newest session in full
// GET  /sessions/<gateway>/<session>   one session in full
// Test data only: reads and writes are open, so nothing sensitive belongs here.

const ID = /^[\w-]{1,40}$/;
const MAX_BYTES = 5 * 1024 * 1024;
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, PUT, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

function json(body, status = 200) {
  return new Response(typeof body === "string" ? body : JSON.stringify(body, null, 1), {
    status, headers: { "Content-Type": "application/json", "Cache-Control": "no-store", ...CORS },
  });
}

async function list(env) {
  const out = [];
  let cursor;
  do {
    const page = await env.SESSIONS.list({ cursor });
    for (const k of page.keys) out.push({ key: k.name, ...(k.metadata || {}) });
    cursor = page.list_complete ? null : page.cursor;
  } while (cursor);
  return out.sort((a, b) => (b.updated || "").localeCompare(a.updated || ""));
}

export default {
  async fetch(req, env) {
    if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
    const parts = new URL(req.url).pathname.split("/").filter(Boolean);
    if (parts[0] !== "sessions") return json({ error: "not found" }, 404);

    if (req.method === "GET" && parts.length === 1) return json(await list(env));
    if (req.method === "GET" && parts[1] === "latest" && parts.length === 2) {
      const [top] = await list(env);
      const v = top && await env.SESSIONS.get(top.key);
      return v ? json(v) : json({ error: "no sessions yet" }, 404);
    }
    if (parts.length !== 3 || !ID.test(parts[1]) || !ID.test(parts[2])) return json({ error: "bad path" }, 400);
    const key = `${parts[1]}/${parts[2]}`;

    if (req.method === "GET") {
      const v = await env.SESSIONS.get(key);
      return v ? json(v) : json({ error: "not found" }, 404);
    }
    if (req.method === "PUT") {
      const text = await req.text();
      if (text.length > MAX_BYTES) return json({ error: "too large" }, 413);
      let s;
      try { s = JSON.parse(text); } catch (e) { return json({ error: "not JSON" }, 400); }
      if (!s || !Array.isArray(s.runs) || !Array.isArray(s.events)) return json({ error: "needs runs and events" }, 400);
      const updated = new Date().toISOString();
      await env.SESSIONS.put(key, text, { metadata: { updated, runs: s.runs.length, events: s.events.length } });
      return json({ ok: true, key, updated });
    }
    return json({ error: "method not allowed" }, 405);
  },
};
