// Paste into the DevTools console of an openreview.net tab (after the page
// has loaded, so the browser challenge is already passed) while
// `python3 scripts/receive.py` is running.
(async () => {
  const API = "https://api2.openreview.net/notes";
  const RECEIVER = "http://127.0.0.1:8765";
  const VENUES = {
    active: "ICLR.cc/2027/Conference/Submission",
    withdrawn: "ICLR.cc/2027/Conference/Withdrawn_Submission",
    desk_rejected: "ICLR.cc/2027/Conference/Desk_Rejected_Submission",
  };
  const PAGE = 1000;
  const FIELDS = ["title", "keywords", "abstract", "primary_area", "TLDR"];

  const slim = (n, status) => {
    const c = n.content || {};
    const o = { id: n.id, number: n.number, cdate: n.cdate, status };
    for (const f of FIELDS) if (c[f] && c[f].value != null) o[f] = c[f].value;
    return o;
  };

  const getPage = async (venueid, offset) => {
    const url = `${API}?content.venueid=${encodeURIComponent(venueid)}&limit=${PAGE}&offset=${offset}&sort=number:asc&count=true`;
    for (let attempt = 0; attempt < 5; attempt++) {
      const r = await fetch(url, { credentials: "include" });
      if (r.ok) return r.json();
      await new Promise((res) => setTimeout(res, 2000 * (attempt + 1)));
    }
    throw new Error(`failed: ${url}`);
  };

  const log = [];
  for (const [status, venueid] of Object.entries(VENUES)) {
    let offset = 0;
    let total = Infinity;
    while (offset < total) {
      const j = await getPage(venueid, offset);
      total = j.count ?? (j.notes.length < PAGE ? offset + j.notes.length : Infinity);
      if (!j.notes.length) break;
      const name = `${status}_${String(offset / PAGE).padStart(3, "0")}`;
      await fetch(`${RECEIVER}/${name}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(j.notes.map((n) => slim(n, status))),
      });
      offset += j.notes.length;
      log.push(`${name}: ${offset}/${total}`);
    }
  }
  console.log(log.join("\n"));
  return log;
})();
