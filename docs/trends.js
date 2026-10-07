"use strict";

const $ = (s) => document.querySelector(s);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
const fmt = (n) => n.toLocaleString("en-US");

function bars(el, items, { suffix = "", accent = () => false } = {}) {
  const max = Math.max(...items.map((x) => x.value), 1);
  $(el).innerHTML = `<div class="bars">${items.map((x) => {
    const label = x.tag
      ? `<a href="index.html#t=${encodeURIComponent(x.tag)}" title="查看该标签的论文">${esc(x.label)}</a>`
      : `<span>${esc(x.label)}</span>`;
    return `<div class="blabel" title="${esc(x.label)}">${label}</div>
      <div class="btrack"><div class="bfill${accent(x) ? " accent" : ""}" style="width:${(100 * x.value) / max}%"></div></div>
      <div class="bval">${fmt(x.value)}${suffix}</div>`;
  }).join("")}</div>`;
}

function timeline(el, days, counts) {
  const W = 760, H = 260, L = 52, R = 20, T = 26, B = 46;
  const max = Math.ceil(Math.max(...counts) / 2000) * 2000;
  const x = (i) => L + (i * (W - L - R)) / (days.length - 1);
  const y = (v) => T + (H - T - B) * (1 - v / max);
  const pts = counts.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(" ");
  const ticks = [];
  for (let v = 0; v <= max; v += max / 4) ticks.push(v);
  const xLabels = days.map((d, i) => (i % 4 === 0 || i === days.length - 1 ? i : -1)).filter((i) => i >= 0);
  $(el).innerHTML = `<svg viewBox="0 0 ${W} ${H}" class="tl" role="img" aria-label="每日新建投稿条目数折线图">
    ${ticks.map((v) => `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" class="grid"/>
      <text x="${L - 6}" y="${y(v) + 4}" text-anchor="end">${fmt(v)}</text>`).join("")}
    <polygon points="${x(0)},${y(0)} ${pts} ${x(days.length - 1)},${y(0)}" class="area"/>
    <polyline points="${pts}" class="line"/>
    ${counts.map((v, i) => `<circle cx="${x(i)}" cy="${y(v)}" r="2.5" class="dot"><title>${days[i]}：${fmt(v)} 篇</title></circle>`).join("")}
    ${xLabels.map((i) => `<text x="${x(i)}" y="${H - B + 16}" text-anchor="${i === days.length - 1 ? "end" : "middle"}">${days[i]}</text>`).join("")}
    <text x="${(L + W - R) / 2}" y="${H - 6}" text-anchor="middle" class="axis">投稿条目创建日期（UTC）</text>
    <text x="${L}" y="12" text-anchor="end" class="axis">篇 / 天</text>
  </svg>`;
}

async function init() {
  const meta = await fetch("data/meta.json", { cache: "no-cache" }).then((r) => r.json());
  const d = await fetch(`data/trends.json?v=${meta.version}`).then((r) => r.json());

  $("#lede").textContent =
    `基于 ${fmt(d.n)} 篇有效投稿的标题、作者关键词、摘要和自动标签。只有本届数据，下文的“热度”指本届占比，不代表增长。`;
  $("#built").textContent = `页面数据生成于 ${meta.built}`;
  $("#stats").innerHTML = d.stats.map((s) => `<div class="stat"><div class="sv">${esc(s.value)}</div><div class="sl">${esc(s.label)}</div></div>`).join("");
  $("#findings").innerHTML = d.findings.map((f) => `<li><strong>${esc(f.title)}</strong><p>${esc(f.body)}</p></li>`).join("");

  bars("#c-groups", d.groups, { suffix: "%" });
  bars("#c-keywords", d.keywords);
  const rlItems = [...d.rl.llm.map((x) => ({ ...x, llm: true })), ...d.rl.classic];
  bars("#c-rl", rlItems, { accent: (x) => x.llm });
  $("#cap-rl").textContent =
    `横轴：论文数（规则标签）。“强化学习（全部）”共 ${fmt(d.rl.total)} 篇，其中 ${fmt(d.rl.llm_total)} 篇带 LLM RL 或 Agentic RL 标签。`;
  bars("#c-agents", d.agents);
  bars("#c-models", d.models, { accent: (x) => x.label === "Qwen" });
  bars("#c-bench", d.benchmarks);
  timeline("#c-timeline", d.timeline.days, d.timeline.counts);
  $("#cap-timeline").textContent =
    `横轴：投稿条目首次创建日期（UTC，最后一天截至 ${d.timeline.last.slice(11)}）；纵轴：当日新建篇数。` +
    `最后 24 小时 ${d.timeline.share24}%，最后 48 小时 ${d.timeline.share48}%，最后一周 ${d.timeline.share168}%。`;

  $("#hot").innerHTML = d.hot.map((h) => `<tr>
    <td><a href="index.html#t=${encodeURIComponent(h.tag)}">${esc(h.label)}</a></td>
    <td class="num">${fmt(h.value)}</td><td class="muted">${esc(h.note)}</td></tr>`).join("");
}

init().catch((err) => {
  $("#lede").textContent = "数据加载失败：" + err.message;
  console.error(err);
});
