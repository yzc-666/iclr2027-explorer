"""Compute the statistics behind docs/trends.html and write docs/data/trends.json.

    python3 scripts/build_trends.py     # also run by build_site.py

All numbers (and the findings text) are derived from data/raw/papers.json and
data/tags.json, so the page stays in sync after re-classification.
"""

import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "data" / "trends.json"

MODELS = {
    "Qwen": r"\bqwen", "Llama": r"\bllama", "GPT（OpenAI）": r"\bgpt-?(?:3|4|5|o|-oss)|\bchatgpt|\bo[134](?:-mini)?\b",
    "Claude": r"\bclaude\b", "DeepSeek": r"deepseek", "Gemma": r"\bgemma", "Gemini": r"\bgemini\b",
    "Mistral": r"\bmi[sx]tral", "OLMo": r"\bolmo", "GLM": r"\bglm-?\d", "Kimi": r"\bkimi\b", "Phi": r"\bphi-\d",
}
BENCHMARKS = {
    "ImageNet": r"imagenet", "LIBERO": r"\blibero", "GSM8K": r"gsm8k", "SWE-bench": r"swe-?bench", "AIME": r"\baime",
    "VBench": r"vbench", "MATH(-500)": r"\bmath-?500\b|\bmath benchmark|\bmath dataset", "MMLU": r"\bmmlu",
    "HumanEval / MBPP": r"humaneval|\bmbpp", "GPQA": r"\bgpqa", "LiveCodeBench": r"livecodebench", "BrowseComp": r"browsecomp",
    "OSWorld": r"osworld", "WebArena": r"webarena", "ARC-AGI": r"arc-agi", "τ-bench": r"τ\^?2?[- ]?bench|\btau\^?2?-bench",
}
KEYWORD_SYNONYMS = {
    "LLM": ["large language models", "large language model", "llm", "llms", "language models", "language model"],
    "agents / LLM agents": ["llm agents", "llm agent", "agents", "agent", "ai agents", "large language model agents",
                            "language agents", "agentic ai", "llm-based agents"],
    "reinforcement learning": ["reinforcement learning", "rl", "deep reinforcement learning"],
    "VLM": ["vision-language models", "vision language models", "vision-language model", "vlm", "vlms",
            "vision language model", "large vision-language models"],
    "MLLM": ["multimodal large language models", "multimodal large language model", "mllm", "mllms"],
    "diffusion models": ["diffusion models", "diffusion model", "diffusion"],
    "world models": ["world models", "world model"],
    "benchmark": ["benchmark", "benchmarks", "benchmarking"],
    "MoE": ["mixture-of-experts", "mixture of experts", "moe"],
    "on-policy distillation": ["on-policy distillation", "on policy distillation", "on-policy self-distillation"],
    "VLA": ["vision-language-action models", "vision-language-action model", "vla"],
    "recursive self-improvement": ["recursive self-improvement", "recursive self improvement", "rsi"],
    "test-time scaling": ["test-time scaling", "test-time compute", "inference-time scaling"],
    "self-evolving agents": ["self-evolving agents", "self-evolving agent", "self-evolving", "self-evolution"],
    "sparse autoencoders": ["sparse autoencoders", "sparse autoencoder", "sae", "saes"],
    "interpretability": ["interpretability", "explainable ai", "explainability"],
    "memory / agent memory": ["agent memory", "memory", "long-term memory"],
    "RAG": ["retrieval-augmented generation", "rag"],
    "time series forecasting": ["time series forecasting", "time-series forecasting"],
    "GNN": ["graph neural networks", "graph neural network", "gnn", "gnns"],
    "robot manipulation": ["robotic manipulation", "robot manipulation"],
    "LoRA / PEFT": ["lora", "low-rank adaptation", "parameter-efficient fine-tuning"],
}
KEYWORD_LIMIT = 20
HOT_TAGS = ["world_models", "vla", "opd", "dllm", "efficient_reasoning", "jepa", "wam", "ai_scientist", "latent_reasoning",
            "sae", "rsi", "looped", "reward_hacking", "algo_discovery", "cot_faith"]
RL_LLM = ["rl4llm", "agentic_rl"]
RL_CLASSIC = ["bandits", "value_based", "il", "offline_rl", "marl", "goal_hrl", "exploration", "rl_theory", "mbrl", "safe_rl"]
AGENT_SUBTAGS = ["harness", "agent_eval", "tool_use", "agentic_rl", "agent_memory", "mas", "self_evolving", "coding_agents",
                 "deep_research", "gui_agents"]


def pct(a, b):
    return round(100 * a / b, 1) if b else 0.0


def main():
    papers = [p for p in json.loads((ROOT / "data" / "raw" / "papers.json").read_text()) if p["status"] == "active"]
    assigned = json.loads((ROOT / "data" / "tags.json").read_text())
    taxonomy = json.loads((ROOT / "data" / "taxonomy.json").read_text())
    n = len(papers)
    tags = {p["id"]: set(assigned[p["id"]]) for p in papers}
    tag_meta = {t["id"]: dict(t, group=g["zh"]) for g in taxonomy for t in g["tags"]}
    umbrella = {t for t, m in tag_meta.items() if m.get("includes") or "（全部" in m["zh"]}
    count = Counter(t for s in tags.values() for t in s)
    both = lambda a, b: sum(1 for s in tags.values() if a in s and b in s)
    text = {p["id"]: f"{p['title']} {' '.join(p.get('keywords') or [])} {p.get('abstract') or ''}" for p in papers}
    mentions = lambda rx, pool=papers: sum(1 for p in pool if re.search(rx, text[p["id"]], re.I))

    def co_tags(focus, k=3):
        sub = [s for s in tags.values() if focus in s]
        c = Counter(t for s in sub for t in s if t != focus and t not in umbrella)
        return [(t, m) for t, m in c.most_common() if m / len(sub) < 0.85][:k]

    def co_text(focus, k=3):
        return "、".join(f"{tag_meta[t]['zh'].split('（')[0]}（{m}）" for t, m in co_tags(focus, k))

    kw = Counter()
    lookup = {alias: canon for canon, aliases in KEYWORD_SYNONYMS.items() for alias in aliases}
    for p in papers:
        seen = set()
        for k in p.get("keywords") or []:
            for x in re.split(r"[;,；]", k):
                x = x.strip().lower()
                if x:
                    seen.add(lookup.get(x, x))
        kw.update(seen)

    llm_papers = [p for p in papers if "llm_all" in tags[p["id"]]]
    model_counts = {k: mentions(rx) for k, rx in MODELS.items()}
    qwen_llm = mentions(MODELS["Qwen"], llm_papers)
    bench_counts = {k: mentions(rx) for k, rx in BENCHMARKS.items()}
    bench_title = sum(1 for p in papers if re.search(r"bench", p["title"], re.I))

    cdates = sorted(p["cdate"] for p in papers)
    last = cdates[-1]
    within = lambda h: pct(sum(1 for c in cdates if c >= last - h * 3600e3), n)
    day = lambda ms: datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%m-%d")
    per_day = Counter(day(c) for c in cdates)
    last_utc = datetime.fromtimestamp(last / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")

    rl_llm = sum(1 for s in tags.values() if "rl_all" in s and s & set(RL_LLM))
    titles_colon = sum(1 for p in papers if ":" in p["title"])
    titles_q = sum(1 for p in papers if "?" in p["title"])
    ar_group = next(g for g in taxonomy if g["id"] == "autoresearch")["count"]
    c = count

    findings = [
        ("LLM 是绝对中心",
         f"{pct(c['llm_all'], n)}% 的投稿（{c['llm_all']:,} 篇）与 LLM 相关；作者关键词第一名是 LLM（{kw['LLM']:,} 篇），"
         f"第二名是 agents（{kw['agents / LLM agents']:,} 篇）。"),
        ("强化学习已经“LLM 化”",
         f"{c['rl_all']:,} 篇 RL 相关论文里，{pct(rl_llm, c['rl_all']):.0f}% 是 LLM 后训练或智能体 RL（RLVR / GRPO {c['rl4llm']:,}，"
         f"Agentic RL {c['agentic_rl']:,}）；离线 RL {c['offline_rl']}、基于模型的 RL {c['mbrl']}、多智能体 RL {c['marl']} 篇。"),
        ("智能体从“做 agent”转向“agent 工程”",
         f"{c['llm_agents']:,} 篇 LLM 智能体论文中，harness / skills / 上下文工程（{c['harness']:,}）、评测（{c['agent_eval']:,}）、"
         f"工具调用（{c['tool_use']:,}）、记忆（{c['agent_memory']:,}）都多于 GUI agent（{c['gui_agents']}）和深度研究（{c['deep_research']}）。"),
        ("蒸馏的主角变成 OPD",
         f"{c['kd']:,} 篇蒸馏论文里 {pct(both('opd', 'kd'), c['kd']):.0f}% 是 on-policy distillation（OPD 共 {c['opd']} 篇），"
         f"最常与 {co_text('opd')}同现，已成为与 RLVR 并列的后训练手段。"),
        ("自我改进与自动化科研成形",
         f"该大类共 {ar_group:,} 篇：RSI {c['rsi']}、AutoResearch / AI Scientist {c['ai_scientist']}、AlphaEvolve 类算法发现 "
         f"{c['algo_discovery']}。RSI 最常与 {co_text('rsi', 2)}同现，从标签看多围绕改进 agent 的脚手架和代码。"),
        ("具身与世界模型升温",
         f"世界模型 {c['world_models']:,}、VLA {c['vla']:,}、world-action model {c['wam']}；VLA 基准 LIBERO 被 "
         f"{bench_counts['LIBERO']} 篇提及，在统计的 benchmark 中仅次于 ImageNet（{bench_counts['ImageNet']}）。"),
        ("生成模型向 flow 与离散扩散迁移",
         f"扩散相关 {c['diffusion']:,} 篇；flow matching {c['flow_matching']:,}、扩散语言模型 {c['dllm']}"
         f"（其中 {both('dllm', 'spec_decode')} 篇涉及并行 / 投机解码）；视频生成 {c['video_gen']:,}，与世界模型交叉 "
         f"{both('video_gen', 'world_models')} 篇。"),
        ("可解释性转向机制可解释",
         f"可解释性 {c['interp_all']:,} 篇里 {pct(both('interp_all', 'llm_all'), c['interp_all']):.0f}% 研究 LLM；机制可解释 / 电路分析 "
         f"{c['mech_interp']:,} 篇，是特征归因（{c['attribution']}）的 {c['mech_interp'] / max(1, c['attribution']):.1f} 倍；"
         f"steering {c['steering']}、SAE {c['sae']}。"),
        ("Qwen 成为默认开源基座",
         f"{model_counts['Qwen']:,} 篇提到 Qwen，是 Llama（{model_counts['Llama']:,}）的 "
         f"{model_counts['Qwen'] / max(1, model_counts['Llama']):.1f} 倍，在 LLM 相关论文中占 {pct(qwen_llm, len(llm_papers))}%；"
         f"闭源模型里 GPT {model_counts['GPT（OpenAI）']}、Claude {model_counts['Claude']}、Gemini {model_counts['Gemini']}。"),
        ("Benchmark 很多，截止前冲刺明显",
         f"{pct(c['benchmark'], n)}% 的投稿声称提出新 benchmark / 数据集，{pct(bench_title, n)}% 的标题带 “Bench”；"
         f"{within(24)}% 的投稿条目创建于最后 24 小时，{within(48)}% 创建于最后 48 小时。"),
    ]

    def bars(ids):
        return [dict(label=tag_meta[t]["zh"], value=c[t], tag=t) for t in ids]

    data = dict(
        n=n,
        stats=[
            dict(value=f"{n:,}", label="有效投稿"),
            dict(value=f"{pct(c['llm_all'], n)}%", label="与 LLM 相关"),
            dict(value=f"{pct(rl_llm, c['rl_all']):.0f}%", label="RL 论文是 LLM / 智能体 RL"),
            dict(value=f"{within(24)}%", label="在截止前 24 小时内创建"),
        ],
        findings=[dict(title=t, body=b) for t, b in findings],
        groups=sorted(
            [dict(label=g["zh"], value=pct(g["count"], n), tag=next((t["id"] for t in g["tags"] if t["id"] in umbrella), None))
             for g in taxonomy], key=lambda x: -x["value"]),
        keywords=[dict(label=k, value=v) for k, v in kw.most_common(KEYWORD_LIMIT)],
        rl=dict(llm=bars(RL_LLM), classic=sorted(bars(RL_CLASSIC), key=lambda x: -x["value"]), total=c["rl_all"], llm_total=rl_llm),
        agents=sorted(bars(AGENT_SUBTAGS), key=lambda x: -x["value"]),
        models=sorted([dict(label=k, value=v) for k, v in model_counts.items()], key=lambda x: -x["value"]),
        benchmarks=sorted([dict(label=k, value=v) for k, v in bench_counts.items()], key=lambda x: -x["value"])[:12],
        timeline=dict(days=sorted(per_day), counts=[per_day[d] for d in sorted(per_day)], last=last_utc,
                      share24=within(24), share48=within(48), share168=within(168)),
        titles=dict(colon=pct(titles_colon, n), question=pct(titles_q, n)),
        hot=sorted([dict(label=tag_meta[t]["zh"], value=c[t], tag=t, note=f"常与 {co_text(t)}同现") for t in HOT_TAGS],
                   key=lambda x: -x["value"]),
    )
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    print(f"trends: {len(findings)} findings, {len(data['hot'])} hot directions -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
