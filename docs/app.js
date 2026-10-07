"use strict";

const PAGE = 50;
const STATUS_LABEL = { active: "有效投稿", withdrawn: "已撤稿", desk_rejected: "Desk Reject" };

const state = {
  tags: new Set(),
  q: "",
  area: "",
  status: new Set(["active"]),
  mode: "and",
  sort: "num",
  tagFilter: "",
};

let META = null;
let P = [];
let results = [];
let rendered = 0;
let lastCounts = null;
let lastGroupCounts = null;
const collapsed = new Set();
const absCache = new Map();

const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const fmt = (n) => n.toLocaleString("en-US");
const hue = (gi) => Math.round((gi * 360) / META.groups.length);
const isPinned = (i) => META.tags[i].zh.includes("（全部");

async function init() {
  const meta = await fetch("data/meta.json", { cache: "no-cache" }).then((r) => r.json());
  const rows = await fetch(`data/papers.json?v=${meta.version}`).then((r) => r.json());
  META = meta;
  META.tagIndex = new Map(META.tags.map((t, i) => [t.id, i]));
  P = rows.map((r, i) => ({
    i, id: r[0], num: r[1], title: r[2], kw: r[3], area: r[4], status: r[5], tags: r[6],
    // Only the Chinese part of tag names is searchable: Latin words in names such as "（全部：RSI / Self-Play）"
    // would otherwise make English queries match every paper under an umbrella tag.
    hay: (r[2] + " \u0001 " + r[3] + " \u0001 " +
      r[6].map((t) => meta.tags[t].zh.replace(/[A-Za-z0-9]+/g, " ")).join(" \u0001 ")).toLowerCase(),
  }));

  const sc = META.statusCounts;
  $("#stats").textContent =
    `共 ${fmt(META.total)} 篇：有效 ${fmt(sc.active)} · 撤稿 ${fmt(sc.withdrawn)} · desk reject ${fmt(sc.desk_rejected)}` +
    ` ｜ ${META.groups.length} 个大类 · ${META.tags.length} 个细分标签`;
  $("#built").textContent = `页面数据生成于 ${META.built}`;
  $("#area").insertAdjacentHTML("beforeend",
    META.areas.map((a, i) => `<option value="${i}">${esc(a)}（${fmt(META.areaCounts[i])}）</option>`).join(""));

  setupControls();
  readHash();
  update(false);
  window.addEventListener("hashchange", () => { readHash(); update(false); });
}

function tokenize(q) {
  const toks = [];
  for (const m of q.toLowerCase().matchAll(/"([^"]+)"|(\S+)/g)) toks.push((m[1] || m[2]).trim());
  return toks.filter(Boolean);
}

const CJK = /[\u3400-\u9fff\uf900-\ufaff]/;
// Latin tokens must start at a word boundary ("rl" must not match "world", "rsi" not "adversarial");
// CJK text has no word boundaries, so CJK tokens match anywhere.
const tokenSource = (t) => (CJK.test(t[0]) ? "" : "(?<![a-z0-9])") + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const matchers = (q) => tokenize(q).map((t) => new RegExp(tokenSource(t), "i"));

function baseFilter() {
  const ms = matchers(state.q);
  const area = state.area === "" ? -1 : Number(state.area);
  const st = new Set([...state.status].map((s) => META.statuses.indexOf(s)));
  return P.filter((p) => st.has(p.status) && (area < 0 || p.area === area) && ms.every((m) => m.test(p.hay)));
}

function tagMatch(p) {
  if (!state.tags.size) return true;
  if (state.mode === "and") {
    for (const t of state.tags) if (!p.tags.includes(t)) return false;
    return true;
  }
  for (const t of state.tags) if (p.tags.includes(t)) return true;
  return false;
}

function sortResults() {
  const ms = matchers(state.q);
  const byNum = (a, b) => a.status - b.status || a.num - b.num;
  if (state.sort === "rel" && ms.length) {
    const score = (p) => ms.reduce((s, m) => s + (m.test(p.title) ? 2 : 1), 0);
    for (const p of results) p._s = score(p);
    results.sort((a, b) => b._s - a._s || byNum(a, b));
  } else if (state.sort === "num_desc") {
    results.sort((a, b) => a.status - b.status || b.num - a.num);
  } else if (state.sort === "title") {
    results.sort((a, b) => a.title.localeCompare(b.title, "en"));
  } else {
    results.sort(byNum);
  }
}

function update(push = true) {
  const base = baseFilter();
  results = base.filter(tagMatch);
  sortResults();

  const src = state.mode === "and" ? results : base;
  const counts = new Int32Array(META.tags.length);
  const groupCounts = new Int32Array(META.groups.length);
  const seen = new Int32Array(META.groups.length).fill(-1);
  for (const p of src) {
    for (const t of p.tags) {
      counts[t]++;
      const g = META.tags[t].g;
      if (seen[g] !== p.i) { seen[g] = p.i; groupCounts[g]++; }
    }
  }
  lastCounts = counts;
  lastGroupCounts = groupCounts;

  renderSidebar();
  renderActiveFilters();
  renderOverview();
  $("#count").textContent = `${fmt(results.length)} 篇`;
  $("#list").innerHTML = "";
  rendered = 0;
  renderMore();
  if (push) writeHash();
}

function renderSidebar() {
  const f = state.tagFilter.trim().toLowerCase();
  $("#groups").innerHTML = META.groups.map((g, gi) => {
    let idx = g.tags.slice().sort((a, b) => isPinned(b) - isPinned(a) || lastCounts[b] - lastCounts[a] || META.tags[b].count - META.tags[a].count);
    if (f) idx = idx.filter((i) => `${META.tags[i].zh} ${META.tags[i].en} ${META.tags[i].id}`.toLowerCase().includes(f));
    if (!idx.length) return "";
    const open = f || !collapsed.has(g.id);
    return `<div class="group${open ? " open" : ""}" style="--hue:${hue(gi)}">
      <button class="ghead" data-group="${g.id}"><span class="caret"></span>${esc(g.zh)}<span class="muted en">${esc(g.en)}</span><span class="n">${fmt(lastGroupCounts[gi])}</span></button>
      <ul>${idx.map((i) => {
        const t = META.tags[i], n = lastCounts[i];
        const cls = ["tag", state.tags.has(i) && "on", !n && "zero", isPinned(i) && "pinned"].filter(Boolean).join(" ");
        return `<li><button class="${cls}" data-tag="${i}" title="${esc(t.en)}"><span class="name">${esc(t.zh)}</span><span class="n">${fmt(n)}</span></button></li>`;
      }).join("")}</ul></div>`;
  }).join("") || `<p class="muted" style="padding:12px">没有匹配的标签</p>`;
}

function renderActiveFilters() {
  const items = [];
  for (const i of state.tags) {
    items.push(`<button class="afilter" data-rm-tag="${i}" style="--hue:${hue(META.tags[i].g)}">${esc(META.tags[i].zh)}</button>`);
  }
  if (state.q) items.push(`<button class="afilter" data-rm="q">搜索：${esc(state.q)}</button>`);
  if (state.area !== "") items.push(`<button class="afilter" data-rm="area">${esc(META.areas[Number(state.area)])}</button>`);
  if (items.length > 1) items.push(`<button class="afilter clear" data-rm="all">清除全部</button>`);
  $("#active-filters").innerHTML = items.join("");

  const ms = matchers(state.q);
  const matches = ms.length
    ? META.tags.map((t, i) => i).filter((i) => !state.tags.has(i) &&
        ms.every((m) => m.test(`${META.tags[i].zh} ${META.tags[i].en} ${META.tags[i].id}`)))
    : [];
  $("#tag-suggest").innerHTML = matches.length
    ? `<span class="muted">匹配的标签（点击改为按标签筛选）：</span>` + matches.slice(0, 10).map((i) =>
        `<button class="chip" data-suggest="${i}" style="--hue:${hue(META.tags[i].g)}" title="${esc(META.tags[i].en)}">${esc(META.tags[i].zh)} · ${fmt(META.tags[i].count)}</button>`
      ).join("")
    : "";
}

function renderOverview() {
  if (state.tags.size || state.q) { $("#overview").innerHTML = ""; return; }
  $("#overview").innerHTML = META.groups.map((g, gi) => {
    const idx = g.tags.slice().sort((a, b) => isPinned(b) - isPinned(a) || lastCounts[b] - lastCounts[a]);
    const max = Math.max(1, ...idx.filter((i) => !isPinned(i)).map((i) => lastCounts[i]));
    return `<div class="ocard" style="--hue:${hue(gi)}">
      <h3>${esc(g.zh)}<span class="n">${fmt(lastGroupCounts[gi])} 篇</span></h3>
      ${idx.map((i) => `<button class="obar" data-tag="${i}" title="${esc(META.tags[i].en)}">
        <span class="fill" style="width:${Math.min(100, (100 * lastCounts[i]) / max)}%"></span>
        <span>${esc(META.tags[i].zh)}</span><span class="n">${fmt(lastCounts[i])}</span></button>`).join("")}
    </div>`;
  }).join("");
}

function highlight(text, toks) {
  if (!toks.length) return esc(text);
  const re = new RegExp("(" + toks.map(tokenSource).join("|") + ")", "gi");
  return text.split(re).map((s, k) => (k % 2 ? `<mark>${esc(s)}</mark>` : esc(s))).join("");
}

function card(p, toks) {
  const st = META.statuses[p.status];
  const chips = p.tags.map((t) =>
    `<button class="chip${state.tags.has(t) ? " on" : ""}" data-tag="${t}" style="--hue:${hue(META.tags[t].g)}" title="${esc(META.tags[t].en)}">${highlight(META.tags[t].zh, toks)}</button>`
  ).join("");
  return `<li class="paper" data-i="${p.i}">
    <div class="ptitle"><a href="https://openreview.net/forum?id=${encodeURIComponent(p.id)}" target="_blank" rel="noopener">${highlight(p.title, toks)}</a>${
      st !== "active" ? `<span class="badge ${st}">${STATUS_LABEL[st]}</span>` : ""}</div>
    <div class="pmeta"><span>#${p.num}</span><span>${esc(META.areas[p.area])}</span><a href="https://openreview.net/pdf?id=${encodeURIComponent(p.id)}" target="_blank" rel="noopener">PDF</a></div>
    ${p.kw ? `<div class="kw">${highlight(p.kw, toks)}</div>` : ""}
    <div class="chips">${chips || '<span class="muted">（无细分标签）</span>'}</div>
    <details><summary>摘要</summary><div class="abs">加载中…</div></details>
  </li>`;
}

function renderMore() {
  const toks = tokenize(state.q);
  const next = results.slice(rendered, rendered + PAGE);
  $("#list").insertAdjacentHTML("beforeend", next.map((p) => card(p, toks)).join(""));
  rendered += next.length;
  $("#sentinel").textContent = rendered < results.length ? "加载中…" : results.length ? `已显示全部 ${fmt(results.length)} 篇` : "没有匹配的论文";
}

async function loadAbstract(i) {
  const shard = Math.floor(i / META.shardSize);
  if (!absCache.has(shard)) absCache.set(shard, fetch(`data/abs/${shard}.json?v=${META.version}`).then((r) => r.json()));
  return (await absCache.get(shard))[i % META.shardSize];
}

function toggleTag(i) {
  if (state.tags.has(i)) state.tags.delete(i); else state.tags.add(i);
  update();
  window.scrollTo({ top: 0 });
}

function writeHash() {
  const h = new URLSearchParams();
  if (state.tags.size) h.set("t", [...state.tags].map((i) => META.tags[i].id).join(","));
  if (state.q) h.set("q", state.q);
  if (state.area !== "") h.set("a", state.area);
  const st = META.statuses.filter((s) => state.status.has(s)).join(",");
  if (st !== "active") h.set("s", st);
  if (state.mode !== "and") h.set("m", state.mode);
  if (state.sort !== "num") h.set("o", state.sort);
  const s = h.toString();
  if (location.hash.slice(1) !== s) history.replaceState(null, "", s ? "#" + s : location.pathname + location.search);
}

function readHash() {
  const h = new URLSearchParams(location.hash.slice(1));
  state.tags = new Set((h.get("t") || "").split(",").map((id) => META.tagIndex.get(id)).filter((i) => i !== undefined));
  state.q = h.get("q") || "";
  state.area = h.get("a") || "";
  state.status = new Set((h.get("s") || "active").split(",").filter((s) => META.statuses.includes(s)));
  state.mode = h.get("m") === "or" ? "or" : "and";
  state.sort = h.get("o") || "num";
  $("#q").value = state.q;
  $("#area").value = state.area;
  $("#mode").value = state.mode;
  $("#sort").value = state.sort;
  $$('input[name="status"]').forEach((el) => { el.checked = state.status.has(el.value); });
}

function exportCSV() {
  const rows = [["number", "title", "status", "primary_area", "tags", "keywords", "url"]];
  for (const p of results) {
    rows.push([p.num, p.title, META.statuses[p.status], META.areas[p.area],
      p.tags.map((t) => META.tags[t].zh).join("; "), p.kw, `https://openreview.net/forum?id=${p.id}`]);
  }
  const csv = "\ufeff" + rows.map((r) => r.map((v) => `"${String(v).replace(/"/g, '""')}"`).join(",")).join("\n");
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
  a.download = `iclr2027_${results.length}.csv`;
  a.click();
  URL.revokeObjectURL(a.href);
}

function setupControls() {
  let timer;
  $("#q").addEventListener("input", (e) => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      state.q = e.target.value.trim();
      if (state.q && state.sort === "num") { state.sort = "rel"; $("#sort").value = "rel"; }
      update();
    }, 200);
  });
  $("#area").addEventListener("change", (e) => { state.area = e.target.value; update(); });
  $("#mode").addEventListener("change", (e) => { state.mode = e.target.value; update(); });
  $("#sort").addEventListener("change", (e) => { state.sort = e.target.value; update(); });
  $$('input[name="status"]').forEach((el) => el.addEventListener("change", () => {
    state.status = new Set($$('input[name="status"]:checked').map((x) => x.value));
    update();
  }));
  $("#tagfilter").addEventListener("input", (e) => { state.tagFilter = e.target.value; renderSidebar(); });
  $("#expand-all").addEventListener("click", () => { collapsed.clear(); renderSidebar(); });
  $("#collapse-all").addEventListener("click", () => { META.groups.forEach((g) => collapsed.add(g.id)); renderSidebar(); });
  $("#export").addEventListener("click", exportCSV);

  $("#groups").addEventListener("click", (e) => {
    const g = e.target.closest("[data-group]");
    if (g) {
      const id = g.dataset.group;
      if (collapsed.has(id)) collapsed.delete(id); else collapsed.add(id);
      renderSidebar();
      return;
    }
    const t = e.target.closest("[data-tag]");
    if (t) toggleTag(Number(t.dataset.tag));
  });
  for (const sel of ["#list", "#overview"]) {
    $(sel).addEventListener("click", (e) => {
      const t = e.target.closest("[data-tag]");
      if (t) toggleTag(Number(t.dataset.tag));
    });
  }
  $("#tag-suggest").addEventListener("click", (e) => {
    const b = e.target.closest("[data-suggest]");
    if (!b) return;
    state.tags.add(Number(b.dataset.suggest));
    state.q = "";
    $("#q").value = "";
    if (state.sort === "rel") { state.sort = "num"; $("#sort").value = "num"; }
    update();
  });
  $("#active-filters").addEventListener("click", (e) => {
    const b = e.target.closest("button");
    if (!b) return;
    if (b.dataset.rmTag !== undefined) state.tags.delete(Number(b.dataset.rmTag));
    else if (b.dataset.rm === "q") { state.q = ""; $("#q").value = ""; }
    else if (b.dataset.rm === "area") { state.area = ""; $("#area").value = ""; }
    else if (b.dataset.rm === "all") { state.tags.clear(); state.q = ""; state.area = ""; $("#q").value = ""; $("#area").value = ""; }
    update();
  });
  $("#list").addEventListener("toggle", async (e) => {
    const d = e.target;
    if (d.tagName !== "DETAILS" || !d.open || d.dataset.loaded) return;
    d.dataset.loaded = "1";
    const i = Number(d.closest(".paper").dataset.i);
    const box = d.querySelector(".abs");
    try {
      box.innerHTML = highlight(await loadAbstract(i), tokenize(state.q));
    } catch {
      box.textContent = "摘要加载失败，请刷新重试。";
      delete d.dataset.loaded;
    }
  }, true);

  new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && rendered < results.length) renderMore();
  }, { rootMargin: "800px" }).observe($("#sentinel"));
}

init().catch((err) => {
  $("#stats").textContent = "数据加载失败：" + err.message;
  console.error(err);
});
