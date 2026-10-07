"""Fine-grained topic taxonomy for ICLR 2027 submissions.

Each tag has one or more rules; a tag is assigned if any rule fires.

A rule fires when
  * its pattern matches the title or author keywords, or matches the
    abstract (+TLDR) at least `min_abs` times, and
  * its optional `ctx` pattern matches the title/keywords, or matches the
    abstract at least `ctx_min` times, and
  * the paper's primary area is in `areas` (if given).

`pat` is case-insensitive; `acr` is case-sensitive (for acronyms such as
OPD, SAE, VLA). A rule with neither only checks `areas` / `ctx`.
`min_abs=99` effectively restricts a rule to title/keywords.
`include=[tag ids]` makes a rule fire whenever any of those tags fired, so
umbrella tags ("RL (all)") cover their sub-tags; included tags must not
themselves use `include`.
"""


def R(pat=None, acr=None, min_abs=2, ctx=None, ctx_min=2, areas=None, include=None):
    return dict(pat=pat, acr=acr, min_abs=min_abs, ctx=ctx, ctx_min=ctx_min, areas=areas, include=include)


LLM = (
    r"\bllms?\b|large language models?|language models?|\blms\b|reasoning models?|\blrms?\b"
    r"|\bmllms?\b|\bvlms?\b|\bgpt|chatgpt|\bqwen|\bllama|deepseek|\bgemini\b|\bclaude\b"
)
AGENT = LLM + r"|\bagents?\b|agentic"
RL = (
    r"reinforcement learning|\brl\b|\bmdps?\b|markov decision|q-learning|actor-critic"
    r"|policy gradient|polic(?:y|ies) optimi[sz]ation"
)
ROBOT = r"\brobot|embodied|gripper|manipulator|end-effector"


TAXONOMY = [
    {
        "id": "llm",
        "zh": "LLM 训练与推理",
        "en": "LLM Training & Reasoning",
        "tags": [
            ("llm_all", "LLM 相关（全部）", "LLM-related (all)", [R(LLM, min_abs=2)]),
            ("rl4llm", "LLM 强化学习（RLVR / GRPO）", "RL for LLMs (RLVR/GRPO)", [
                R(r"\brlvr\b|verifiable rewards?|\bgrpo\b|group relative policy|\bdapo\b|\bgspo\b"
                  r"|reinforcement fine-?tuning|\brl post-?training|rl-based post-?training|zero-?rl\b"
                  r"|r1-(?:style|like|zero)|rl with verifi|reinforcement learning (?:with|from) verifi", min_abs=1),
                R(r"reinforcement learning|\brl\b|\bppo\b|policy optimi[sz]ation|policy gradient", ctx=LLM),
            ]),
            ("rlhf", "RLHF 与偏好优化（DPO 等）", "RLHF & Preference Optimization", [
                R(r"\brlhf\b|\brlaif\b|human feedback|preference optimi[sz]ation|\bdpo\b|\bsimpo\b|\bkto\b"
                  r"|preference alignment|bradley-?terry|preference (?:data|pairs|dataset)", min_abs=2),
            ]),
            ("reward_model", "奖励模型（ORM / PRM / Verifier）", "Reward Models & Verifiers", [
                R(r"reward models?|reward modell?ing|process reward|\bprms?\b|outcome reward|generative reward"
                  r"|\bgenrm\b|verifier models?|generative verifiers?|rubric", min_abs=2),
            ]),
            ("reward_hacking", "奖励欺骗（Reward Hacking）", "Reward Hacking", [
                R(r"reward hacking|reward over-?optimi[sz]ation|specification gaming|reward tampering|reward exploitation", min_abs=1),
            ]),
            ("opd", "在线策略蒸馏（OPD）", "On-Policy Distillation (OPD)", [
                R(r"on[- ]?policy (?:self[- ]?)?distill|\bgkd\b|generalized knowledge distillation"
                  r"|student[- ]generated (?:outputs|sequences|samples|rollouts|trajectories)", min_abs=1),
                R(acr=r"\bOPS?D\b", min_abs=1),
            ]),
            ("kd", "知识蒸馏（通用）", "Knowledge Distillation", [
                R(r"knowledge distillation|\bdistill(?:ation|ing|ed)?\b|teacher[- ]student|student models?", min_abs=2),
            ]),
            ("cot", "LLM 推理 / 思维链 / 推理模型", "LLM Reasoning / CoT / Reasoning Models", [
                R(r"chain[- ]of[- ]thoughts?|\bcot\b|reasoning traces?|long reasoning|reasoning models?|\blrms?\b"
                  r"|large reasoning|slow thinking|o1-like|deepseek-r1|thinking models?", min_abs=2),
                R(r"\breasoning\b", ctx=LLM, min_abs=3),
            ]),
            ("latent_reasoning", "隐式 / 连续空间推理", "Latent / Continuous Reasoning", [
                R(r"latent reasoning|continuous (?:thoughts?|reasoning|chain|latent)|implicit (?:chain[- ]of[- ]thought|reasoning)"
                  r"|reasoning in (?:the )?(?:latent|continuous)|latent (?:chain|thoughts?|space reasoning|tokens? reasoning)"
                  r"|\bcoconut\b|soft thinking|soft (?:reasoning )?tokens|thinking in latent", min_abs=1),
            ]),
            ("tts", "测试时扩展（Test-time Scaling）", "Test-time Scaling & Search", [
                R(r"test[- ]time (?:scaling|compute)|inference[- ]time (?:scaling|compute)|best[- ]of[- ]n|self[- ]consistency"
                  r"|majority vot|parallel (?:thinking|reasoning|sampling)|sequential scaling|budget forcing", min_abs=1),
                R(r"tree search|\bmcts\b|monte carlo tree|beam search|verifier-guided|search over reasoning", ctx=LLM),
            ]),
            ("efficient_reasoning", "高效推理（Overthinking / 推理长度）", "Efficient Reasoning (overthinking, length)", [
                R(r"overthink|underthink|efficient reasoning|reasoning efficiency|reasoning length|concise (?:reasoning|thinking)"
                  r"|adaptive (?:thinking|reasoning)|thinking budget|token budget|length penalt|redundant (?:reasoning|thinking)"
                  r"|compress(?:ing|ed|ion of)? (?:the )?(?:reasoning|chain[- ]of[- ]thought|cot)|early exit(?:ing)? (?:of|in|from|during) (?:reasoning|thinking)"
                  r"|when to stop thinking|hybrid thinking", min_abs=1),
            ]),
            ("math", "数学推理与定理证明", "Math Reasoning & Theorem Proving", [
                R(r"mathematical reasoning|math reasoning|theorem prov|formal proofs?|autoformali[sz]|olympiad|\baime\b"
                  r"|math500|gsm8k|competition(?:-level)? math|mathematical problem|math word problems?|\bminif2f\b", min_abs=2),
                R(acr=r"\bLean ?4\b|\bLean\b(?= (?:prover|theorem|proof|code|formal|environment))", min_abs=1),
            ]),
            ("code", "代码生成", "Code Generation", [
                R(r"code generation|code llms?|code (?:language )?models?|program synthesis|\bcoding\b|code reasoning|code completion"
                  r"|text-to-sql|\bsql\b|competitive programming|code repair|program repair|unit tests?|verilog|cuda kernels?", min_abs=2),
            ]),
            ("self_improve", "自我改进 / 自进化 / Self-Play", "Self-Improvement / Self-Evolution / Self-Play", [
                R(r"self[- ]improv|self[- ]evol|self[- ]play|self[- ]rewarding|self[- ]refine|recursive self|self[- ]correct"
                  r"|self[- ]reflect|self[- ]train(?:ing)?\b|self[- ]generated (?:data|curricul)|self[- ]verif", min_abs=2),
            ]),
            ("icl", "上下文学习（ICL）", "In-Context Learning", [
                R(r"in[- ]context learn|\bicl\b|many[- ]shot|in[- ]context examples|demonstration selection", min_abs=2),
            ]),
            ("long_context", "长上下文", "Long Context", [
                R(r"long[- ]context|context (?:length|window)s?|length (?:generali[sz]ation|extrapolation)|long[- ]sequence"
                  r"|needle[- ]in[- ]a[- ]haystack|context extension|million[- ]token", min_abs=2),
            ]),
            ("rag", "检索增强 / 检索 / Embedding", "RAG, Retrieval & Embeddings", [
                R(r"retrieval[- ]augmented|\brag\b|retrievers?\b|dense retrieval|information retrieval|re-?ranking|rerankers?"
                  r"|text embeddings?|embedding models?|search engines?|graphrag|knowledge retrieval|generative retrieval", min_abs=2),
            ]),
            ("hallucination", "幻觉与事实性", "Hallucination & Factuality", [
                R(r"hallucinat|factuality|factual (?:errors|consistency|accuracy|knowledge)|confabulat", min_abs=2),
            ]),
            ("judge", "LLM-as-a-Judge / 自动评测", "LLM-as-a-Judge", [
                R(r"llm[- ]as[- ]an?[- ]judges?|llm judges?|judge models?|as a judge|judging|automatic evaluat|llm-based evaluat"
                  r"|evaluator models?|auto-?evaluat", min_abs=2),
            ]),
            ("pretrain", "预训练与 Scaling Law", "Pretraining & Scaling Laws", [
                R(r"scaling laws?|compute[- ]optimal|pre-?training (?:data|corpus|corpora|recipes?|mixtures?)|data mix(?:ture|ing)"
                  r"|mid-?training|continued pre-?training|learning rate schedul|\bwsd\b|language model pre-?training"
                  r"|pre-?training (?:of |large )?(?:llms?|language models)", min_abs=2),
            ]),
            ("tokenization", "Tokenizer / 分词", "Tokenization", [
                R(r"tokeni[sz](?:er|ers|ation)\b|byte[- ]level|\bbpe\b|vocabulary (?:size|expansion|scaling|adaptation|transfer)|large vocabular|subword|tokenizer-free", min_abs=2),
            ]),
            ("peft", "参数高效微调（LoRA / PEFT）", "PEFT / LoRA", [
                R(r"\blora\b|low[- ]rank adapt|parameter[- ]efficient|\badapters?\b|prompt tuning|prefix tuning|\bpeft\b", min_abs=2),
            ]),
            ("merging", "模型合并 / 任务向量", "Model Merging & Task Vectors", [
                R(r"model merging|merg(?:e|ing) (?:of )?(?:models|llms|experts|checkpoints)|task arithmetic|task vectors?"
                  r"|weight averaging|model soups?|model fusion|merged models?", min_abs=1),
            ]),
            ("editing", "知识编辑", "Knowledge / Model Editing", [
                R(r"knowledge editing|model editing|editing (?:knowledge|facts)|fact(?:ual)? editing|\brome\b|\bmemit\b|knowledge updat", min_abs=1),
            ]),
            ("sft", "指令微调 / SFT", "Instruction Tuning & SFT", [
                R(r"instruction[- ]follow|instruction[- ]tun|supervised fine-?tun|\bsft\b|instruction data", min_abs=2),
            ]),
            ("multilingual", "多语言 / 翻译", "Multilingual & Translation", [
                R(r"multilingual|cross-?lingual|low-resource languages?|machine translation|\btranslation\b|non-english", min_abs=2),
            ]),
            ("persona", "个性化 / 角色扮演 / 用户模拟", "Personalization, Persona & User Simulation", [
                R(r"personali[sz](?:ation|ed) (?:llms?|alignment|generation|response|assistant)|\bpersonas?\b|role[- ]?play"
                  r"|user simulat|simulated users?|user modell?ing|human simulat|social simulat", min_abs=1),
            ]),
        ],
    },
    {
        "id": "agents",
        "zh": "智能体",
        "en": "Agents",
        "tags": [
            ("llm_agents", "LLM 智能体（全部）", "LLM Agents (all)", [
                R(r"llm[- ]agents?|language agents?|ai agents?|autonomous agents?|llm-based agents?|foundation model agents?|(?:language )?model agents?"
                  r"|multimodal agents?|agentic (?:ai|systems?|llms?|models?|tasks?|workflows?|search|coding|reasoning|rl|reinforcement|frameworks?|environments?)", min_abs=1),
                R(r"agentic|\bagents?\b", ctx=LLM, min_abs=3),
                R(include=["coding_agents", "gui_agents", "deep_research", "agentic_rl", "mas", "science_agents"]),
            ]),
            ("tool_use", "工具调用 / Function Calling / MCP", "Tool Use / Function Calling / MCP", [
                R(r"tool[- ]use|tool[- ]using|tool[- ]calling|function[- ]calling|tool[- ]augmented|tool[- ]integrated|tool learning"
                  r"|\bmcp\b|model context protocol|\bapi calls?\b|external tools", min_abs=1),
            ]),
            ("agent_memory", "智能体记忆", "Agent Memory", [
                R(r"agent(?:ic)? memory|memory (?:systems?|mechanisms?|management|architectures?|modules?|banks?|retrieval|consolidation)"
                  r"|long[- ]term memory|episodic memory|memory[- ]augmented|conversational memory|memory for (?:llms?|agents?)",
                  ctx=AGENT, ctx_min=1, min_abs=1),
            ]),
            ("coding_agents", "代码智能体 / SWE Agent", "Coding / SWE Agents", [
                R(r"coding agents?|software engineering agents?|swe[- ]?agents?|swe-bench|code agents?|issue resolution"
                  r"|terminal[- ]bench|agentic coding|repository-level (?:code|software|issue)|software engineering tasks", min_abs=1),
            ]),
            ("gui_agents", "GUI / Web / Computer-use 智能体", "GUI / Web / Computer-use Agents", [
                R(r"gui agents?|web agents?|computer[- ]use|web navigation|browser agents?|mobile agents?|\bos agents?|webarena"
                  r"|osworld|android|gui grounding|web browsing|graphical user interface|screen understanding|ui automation", min_abs=1),
            ]),
            ("deep_research", "深度研究 / 搜索智能体", "Deep Research / Search Agents", [
                R(r"deep research|search agents?|agentic search|web search|search[- ]augmented|research agents?|information[- ]seeking"
                  r"|browsecomp|agentic retrieval|search-r1", min_abs=1),
            ]),
            ("mas", "多智能体系统（LLM）", "LLM Multi-Agent Systems", [
                R(r"multi[- ]agent (?:systems?|collaboration|debate|frameworks?|llms?|communication|coordination|orchestration|workflows?)"
                  r"|multiple (?:llm )?agents|agent (?:collaboration|orchestration|teams?|societ)|multi[- ]llm|llm debate|agent swarms?",
                  ctx=LLM, ctx_min=1, min_abs=1),
            ]),
            ("harness", "Harness / Skills / 上下文工程 / Prompt 优化", "Harness, Skills, Context Eng. & Prompt Optimization", [
                R(r"(?:\| |; )(?:agent |agentic )?harness(?:es)?(?= ;|$)", min_abs=99),
                R(r"agent harness|harness (?:design|engineering|optimi[sz]ation)|(?:a|an|the|our|its|their|this|agentic|coding|evaluation|execution) harness\b"
                  r"|agent skills?|skill (?:librar(?:y|ies)|evolution|discovery|acquisition|reuse)"
                  r"|context engineering|context management|prompt optimi[sz]|automatic prompt|prompt engineering"
                  r"|workflow (?:optimi[sz]|generation|automation|search)|agent design|scaffold(?:ing)?\b|agentic workflows?",
                  ctx=AGENT, ctx_min=1, min_abs=1),
            ]),
            ("agentic_rl", "智能体强化学习（Agentic RL）", "Agentic RL", [
                R(r"agentic (?:reinforcement learning|rl)|multi-turn (?:rl|reinforcement)|long-horizon (?:rl|reinforcement)"
                  r"|rl for (?:llm )?agents|agent(?:s)? rl\b|tool-integrated (?:rl|reinforcement)", min_abs=1),
                R(r"reinforcement learning|\brl\b|\bgrpo\b|policy optimi[sz]ation",
                  ctx=r"llm[- ]agents?|language agents?|agentic|tool[- ]use|tool[- ]calling|multi-turn|search agents?", min_abs=1),
            ]),
            ("agent_eval", "智能体评测 / Benchmark", "Agent Benchmarks & Evaluation", [
                R(r"agent(?:ic)? (?:benchmarks?|evaluation|evals?)|benchmark(?:ing)? (?:for )?(?:llm |ai )?agents|evaluat(?:e|ing) (?:llm |ai )?agents", min_abs=1),
                R(r"\bbench(?:mark)?s?\b|\barena\b", ctx=r"\bagents?\b|agentic", ctx_min=3, min_abs=99),
            ]),
            ("science_agents", "AI 科学家 / 自动化研究", "AI Scientist & Automated Research", [
                R(r"ai scientists?|automated (?:scientific )?(?:research|discovery)|scientific agents?|autonomous research"
                  r"|hypothesis generation|ml engineering agents?|mle-bench|paper writing|research automation|idea generation", min_abs=1),
            ]),
        ],
    },
    {
        "id": "arch",
        "zh": "模型架构",
        "en": "Architectures",
        "tags": [
            ("looped", "循环 / 递归深度 Transformer（Loop Transformer）", "Looped / Recurrent-depth Transformers", [
                R(r"looped (?:transformers?|models?|language models?|llms?|architectures?|networks?)|loop(?:ed|ing) transformers?"
                  r"|recurrent[- ]depth|universal transformers?|depth[- ]recurren|recursive transformers?|weight[- ]tied (?:layers|depth|blocks|transformers?)"
                  r"|layer (?:looping|recurrence)|parameter[- ]shar(?:ed|ing) (?:across )?(?:layers|depth|blocks)|tiny recursive|\btrm\b"
                  r"|hierarchical reasoning models?|\bhrm\b|\bouro\b|recursive reasoning models?|latent (?:recurrence|iteration)"
                  r"|looping (?:layers|blocks|the model)|iterat(?:ed|ive) (?:layers|depth|blocks)|deep equilibrium|\bdeqs?\b", min_abs=1),
            ]),
            ("adaptive_compute", "自适应计算 / Early Exit / 动态深度", "Adaptive Computation / Early Exit", [
                R(r"adaptive computation|early[- ]exit|dynamic depth|layer skipping|skip(?:ping)? layers|mixture[- ]of[- ]depths"
                  r"|conditional computation|halting|ponder|adaptive depth|compute allocation", min_abs=1),
            ]),
            ("moe", "混合专家（MoE）", "Mixture-of-Experts", [
                R(r"mixture[- ]of[- ]experts?|\bmoes?\b|sparse(?:ly)?[- ]gated|expert (?:routing|specialization|load|parallel)"
                  r"|load[- ]balancing loss|routed experts|fine-grained experts", min_abs=1),
            ]),
            ("ssm", "线性注意力 / SSM / RNN", "Linear Attention / SSM / RNN", [
                R(r"state[- ]space models?|\bssms?\b|\bmamba\d?\b|linear attention|linear rnns?|recurrent neural networks?|\brnns?\b"
                  r"|\blstms?\b|\brwkv\b|gated delta|deltanet|sub-?quadratic|linear[- ]time (?:sequence|attention)|xlstm|linear recurren"
                  r"|hybrid (?:attention|linear)", min_abs=2),
            ]),
            ("attention", "注意力机制 / 稀疏注意力", "Attention Mechanisms / Sparse Attention", [
                R(r"attention (?:mechanisms?|heads?|sinks?|patterns?|variants?|kernels?|layers?)|softmax attention|sparse attention"
                  r"|multi-head attention|flash ?attention|\bgqa\b|multi-head latent|native sparse|attention sparsity|attention entropy", min_abs=2),
            ]),
            ("posenc", "位置编码 / 长度泛化", "Positional Encoding & Length Generalization", [
                R(r"positional (?:encodings?|embeddings?)|position(?:al)? (?:bias|interpolation)|\brope\b|rotary|length generali[sz]"
                  r"|length extrapolat|\balibi\b|\bnope\b", min_abs=1),
            ]),
            ("ttt", "测试时训练 / 记忆层 / 联想记忆", "Test-time Training / Memory Layers / Associative Memory", [
                R(r"test[- ]time training|\bttt\b|fast weights|memory layers?|associative memor|hopfield|\btitans\b"
                  r"|test[- ]time (?:learning|memori[sz]ation)|online (?:memory|learning) layers?", min_abs=1),
            ]),
            ("snn", "脉冲 / 类脑网络", "Spiking & Neuromorphic", [
                R(r"spiking|neuromorphic|\bsnns?\b", min_abs=1),
            ]),
            ("kan", "KAN / 归一化 / 超网络等网络组件", "KANs, Normalization, Hypernetworks & Other Blocks", [
                R(r"kolmogorov[- ]arnold|hypernetworks?|neural cellular automata|liquid neural|\bnormali[sz]ation layers?|layer ?norm|\brmsnorm\b", min_abs=1),
                R(acr=r"\bKANs?\b", min_abs=1),
            ]),
        ],
    },
    {
        "id": "gen",
        "zh": "生成模型",
        "en": "Generative Models",
        "tags": [
            ("diffusion", "扩散模型（全部）", "Diffusion Models (all)", [
                R(r"diffusion|denoising diffusion|score[- ]based|score matching|\bddpm\b|\bddim\b|latent diffusion|stable diffusion", min_abs=2),
                R(include=["dllm", "diff_align"]),
            ]),
            ("flow_matching", "Flow Matching / 归一化流", "Flow Matching & Normalizing Flows", [
                R(r"flow matching|rectified flows?|stochastic interpolants?|normali[sz]ing flows?|continuous normali[sz]ing"
                  r"|flow[- ]based (?:generative|models?|policy|policies)|mean ?flows?|flow maps?", min_abs=1),
            ]),
            ("dllm", "扩散语言模型 / 离散扩散", "Diffusion Language Models / Discrete Diffusion", [
                R(r"diffusion language models?|discrete diffusion|masked diffusion|diffusion llms?|\bdllms?\b|\bdlms?\b|text diffusion"
                  r"|\bllada\b|non-?autoregressive (?:language|text) (?:models?|generation)|any-order|block diffusion"
                  r"|diffusion-based (?:language|text|llms?)|\bmdms?\b|\bmdlms?\b|masked generative models?", min_abs=1),
            ]),
            ("fewstep", "少步生成 / 一致性模型 / 扩散加速", "Few-step / Consistency / Diffusion Acceleration", [
                R(r"few[- ]step|one[- ]step (?:generat|diffusion|sampl|image)|single[- ]step generat|consistency (?:models?|distillation|training|trajectory)"
                  r"|distribution matching distillation|\bdmd\d?\b|diffusion distillation|step distillation|progressive distillation"
                  r"|shortcut models?|accelerat(?:e|ing|ed) (?:diffusion )?sampling|fast sampling|sampling acceleration|ode solvers?"
                  r"|(?:feature|cache|token) caching|diffusion (?:acceleration|efficiency)|efficient diffusion|inference acceleration for diffusion", min_abs=1),
            ]),
            ("guidance", "引导与可控生成（CFG 等）", "Guidance & Controllable Generation", [
                R(r"classifier[- ]free guidance|\bcfg\b|guidance (?:scale|methods?|strength|schedul)|controllable (?:generation|synthesis)"
                  r"|conditional generation|controlnet|guided (?:sampling|generation|diffusion)|training-free guidance|reward[- ]guided", min_abs=1),
            ]),
            ("diff_align", "扩散模型对齐 / 奖励微调", "Diffusion Alignment & Reward Fine-tuning", [
                R(r"(?:preference|reward|rl|reinforcement) (?:fine-?tuning|optimi[sz]ation|learning|alignment)|\bdpo\b|\bgrpo\b|reward models?|human preference",
                  ctx=r"diffusion|flow matching|text-to-image|image generation|video generation|flow models?", ctx_min=2, min_abs=1),
            ]),
            ("t2i", "图像生成 / 文生图", "Image Generation / Text-to-Image", [
                R(r"text[- ]to[- ]image|image generation|image synthesis|\bt2i\b|visual generation|image generative|generated images", min_abs=1),
            ]),
            ("ar_visual", "自回归视觉生成 / 视觉 Tokenizer", "Autoregressive Visual Generation & Visual Tokenizers", [
                R(r"autoregressive (?:image|visual|video) (?:generation|models?|generative)|visual autoregressive|visual tokeni[sz]|image tokeni[sz]"
                  r"|video tokeni[sz]|vector[- ]quanti[sz]|\bvq-?vae\b|\bvqgan\b|next[- ]scale prediction|masked autoregressive"
                  r"|1d tokeni[sz]|continuous tokens", min_abs=1),
                R(acr=r"\bVAR\b", min_abs=1),
            ]),
            ("video_gen", "视频生成", "Video Generation", [
                R(r"video generation|video diffusion|text[- ]to[- ]video|\bt2v\b|image[- ]to[- ]video|\bi2v\b|video synthesis|video generative"
                  r"|autoregressive video|long video generation|talking (?:head|face)|video (?:generation )?models?(?= generat)|video generators?", min_abs=1),
            ]),
            ("img_edit", "图像 / 视频编辑与个性化生成", "Image/Video Editing & Personalization", [
                R(r"image editing|video editing|instruction[- ]based editing|inpainting|style transfer|personali[sz]ed (?:generation|image|text-to-image)"
                  r"|subject[- ]driven|customi[sz]ed generation|text[- ]guided editing|editing models?", min_abs=1),
            ]),
            ("gen3d", "3D / 4D 生成", "3D / 4D Generation", [
                R(r"3d generation|text[- ]to[- ]3d|image[- ]to[- ]3d|4d generation|3d (?:asset|shape|scene|object|content) generation"
                  r"|mesh generation|3d generative|generat(?:e|ing|ion of) 3d|3d diffusion", min_abs=1),
            ]),
            ("unified_mm", "统一理解与生成模型", "Unified Understanding & Generation", [
                R(r"unified (?:multimodal|models?|understanding and generation|autoregressive|generation and understanding)"
                  r"|understanding and generation|generation and understanding|any-to-any|omni[- ]?modal|\bomni\b", min_abs=1),
            ]),
            ("inverse", "逆问题 / 图像复原 / 底层视觉", "Inverse Problems, Restoration & Low-level Vision", [
                R(r"inverse problems?|posterior sampling|image restoration|super[- ]resolution|deblurr|image denoising|compressed sensing"
                  r"|plug-and-play (?:priors?|diffusion|denois)|low[- ]light (?:image|enhancement)|image enhancement|dehaz|derain|image harmoni[sz]ation|low[- ]level vision|image fusion", min_abs=1),
            ]),
            ("other_gen", "VAE / GAN / EBM / 其他生成模型", "VAEs / GANs / EBMs", [
                R(r"\bgans?\b|generative adversarial|variational auto-?encoders?|\bvaes?\b|energy[- ]based models?|\bebms?\b", min_abs=1),
            ]),
            ("gen_theory", "扩散 / 生成模型理论", "Diffusion & Generative Model Theory", [
                R(r"theor(?:y|etical)|provabl|convergence (?:rate|guarantee|analysis)|sample complexity|generali[sz]ation (?:bound|error|of)|memori[sz]ation",
                  ctx=r"diffusion|flow matching|score[- ]based|generative models?", min_abs=2),
            ]),
        ],
    },
    {
        "id": "mm",
        "zh": "多模态与视觉",
        "en": "Multimodal & Vision",
        "tags": [
            ("vlm", "视觉语言模型（VLM / MLLM）", "Vision-Language Models (VLM/MLLM)", [
                R(r"vision[- ]language models?|\bvlms?\b|\blvlms?\b|multimodal large language|\bmllms?\b|multimodal llms?|large multimodal models?"
                  r"|\blmms?\b|vision[- ]language|visual instruction|\bllava\b|qwen\d?(?:\.\d)?-?vl|visual question answering|\bvqa\b", min_abs=2),
            ]),
            ("mm_reasoning", "多模态推理", "Multimodal Reasoning", [
                R(r"multimodal reasoning|visual reasoning|thinking with images|visual chain[- ]of[- ]thought|multimodal (?:chain|cot)"
                  r"|visual math|geometry problems?|chart (?:understanding|reasoning|qa)|visual (?:thinking|reflection)", min_abs=1),
            ]),
            ("video_und", "视频理解", "Video Understanding", [
                R(r"video understanding|video question answering|video[- ]?qa|long[- ]video|video llms?|video-language|video large language"
                  r"|temporal grounding|streaming video|video reasoning|action recognition|video (?:comprehension|analysis|captioning)", min_abs=1),
            ]),
            ("token_compress", "Token 剪枝 / 压缩", "Token Pruning / Compression", [
                R(r"visual tokens? (?:pruning|compression|reduction|merging|selection|dropping)|token (?:pruning|merging|reduction|compression|dropping|eviction)"
                  r"|\btome\b|redundant (?:visual )?tokens", min_abs=1),
            ]),
            ("spatial", "空间推理 / 空间智能", "Spatial Reasoning / Spatial Intelligence", [
                R(r"spatial (?:reasoning|intelligence|understanding|cognition|relation|awareness)|3d (?:spatial|scene) (?:reasoning|understanding)"
                  r"|mental rotation|perspective[- ]taking|cognitive maps?", min_abs=1),
            ]),
            ("vision3d", "3D 视觉（3DGS / NeRF / 重建）", "3D Vision (3DGS / NeRF / Reconstruction)", [
                R(r"gaussian splatting|\b3dgs\b|neural radiance|\bnerfs?\b|novel view synthesis|3d reconstruction|multi-view (?:stereo|reconstruction|geometry)"
                  r"|depth estimation|point clouds?|\bslam\b|structure[- ]from[- ]motion|camera pose|4d reconstruction|scene reconstruction"
                  r"|feed-forward 3d|\bmeshes\b|\bvggt\b|\bdust3r\b|implicit neural representations?|neural fields?|signed distance", min_abs=1),
            ]),
            ("detseg", "检测 / 分割 / 跟踪 / 定位", "Detection, Segmentation, Tracking & Grounding", [
                R(r"object detection|semantic segmentation|instance segmentation|panoptic|segmentation|\bsam\d?\b|segment anything"
                  r"|open[- ]vocabulary (?:detection|segmentation)|referring (?:expression|segmentation)|visual grounding|object tracking|\btracking\b"
                  r"|re-?identification|\bre-?id\b", min_abs=2),
            ]),
            ("vision_backbone", "视觉骨干 / ViT / 图像分类", "Vision Backbones / ViT / Classification", [
                R(r"vision transformers?|\bvits?\b|convolutional (?:neural )?networks?|\bcnns?\b|image classification|visual backbones?|vision foundation models?", min_abs=2),
            ]),
            ("clip", "CLIP / 图文对比学习 / 跨模态检索", "CLIP, Image-Text Contrastive & Cross-modal Retrieval", [
                R(r"\bclip\b|contrastive language[- ]image|image[- ]text (?:retrieval|alignment|matching|pairs)|\bsiglip\b|cross[- ]modal retrieval"
                  r"|vision[- ]language pre-?training|multimodal (?:embeddings?|retrieval)|composed image retrieval", min_abs=1),
            ]),
            ("audio", "音频 / 语音 / 音乐", "Audio, Speech & Music", [
                R(r"\baudio\b|\bspeech\b|\bmusic\b|\basr\b|text[- ]to[- ]speech|spoken|\bvoice\b|\bsound\b|acoustic|speaker", min_abs=2),
            ]),
            ("doc_ocr", "文档 / OCR / 图表理解", "Documents, OCR & Charts", [
                R(r"\bocr\b|document (?:understanding|parsing|images?|ai|question)|\bcharts?\b|table understanding|text-rich|scene text|infographics?", min_abs=2),
            ]),
        ],
    },
    {
        "id": "rl",
        "zh": "强化学习",
        "en": "Reinforcement Learning",
        "tags": [
            ("rl_all", "强化学习（全部，含 LLM RL）", "Reinforcement Learning (all, incl. RL for LLMs)", [
                R(RL, min_abs=2),
                R(areas={"reinforcement learning"}),
                R(include=["rl4llm", "agentic_rl", "offline_rl", "mbrl", "marl", "safe_rl", "goal_hrl", "rl_theory"]),
            ]),
            ("offline_rl", "离线强化学习", "Offline RL", [
                R(r"offline (?:reinforcement learning|rl|policy|multi-agent|goal|imitation|data)|batch rl|offline-to-online|\bd4rl\b"
                  r"|conservative q|behavio(?:u)?r regulari[sz]", min_abs=1, ctx=RL + r"|offline", ctx_min=1),
            ]),
            ("mbrl", "基于模型的强化学习", "Model-based RL", [
                R(r"model[- ]based (?:reinforcement learning|rl|planning|policy|value)|\bdreamer(?:v\d)?\b|\bmuzero\b|\btd-mpc\d?\b|learned dynamics models?", min_abs=1),
            ]),
            ("marl", "多智能体强化学习（MARL）", "Multi-Agent RL", [
                R(r"multi[- ]agent reinforcement|\bmarl\b|cooperative multi[- ]agent|decentrali[sz]ed (?:multi-agent|policies|execution)"
                  r"|centrali[sz]ed training|multi[- ]agent (?:rl|policy|coordination|games?)", min_abs=1),
            ]),
            ("exploration", "探索 / 内在激励", "Exploration & Intrinsic Motivation", [
                R(r"\bexploration\b|intrinsic (?:motivation|rewards?)|curiosity|novelty[- ]seeking|count-based|exploration[- ]exploitation", ctx=RL, min_abs=2),
            ]),
            ("il", "模仿学习 / 行为克隆 / 逆强化学习", "Imitation Learning / BC / IRL", [
                R(r"imitation learning|behavio(?:u)?r(?:al)? cloning|inverse reinforcement|learning from demonstrations?|\birl\b|apprenticeship", min_abs=1),
            ]),
            ("safe_rl", "安全 / 约束强化学习", "Safe & Constrained RL", [
                R(r"safe (?:reinforcement learning|rl|exploration|polic(?:y|ies))|constrained (?:mdps?|reinforcement learning|rl|polic(?:y|ies))|\bcmdps?\b", min_abs=1),
            ]),
            ("bandits", "Bandit / 在线学习", "Bandits & Online Learning", [
                R(r"\bbandits?\b|thompson sampling|upper confidence bound|\bucb\b|best[- ]arm|online learning|online convex|regret (?:bounds?|minimi[sz]ation|guarantees?)"
                  r"|no-regret|\bexperts? advice|dueling", min_abs=1),
            ]),
            ("goal_hrl", "目标条件 / 分层 / 无监督 RL", "Goal-conditioned / Hierarchical / Unsupervised RL", [
                R(r"goal[- ]conditioned|hierarchical (?:reinforcement learning|rl|polic(?:y|ies))|skill discovery|unsupervised (?:reinforcement learning|rl)"
                  r"|options framework|temporal abstraction|zero-shot (?:rl|reinforcement)|successor (?:features|representations|measures)"
                  r"|forward-backward representation|behavior foundation models?", min_abs=1),
            ]),
            ("rl_theory", "强化学习理论", "RL Theory", [
                R(r"provabl|sample complexity|regret bound|finite[- ]sample|minimax optimal|convergence (?:guarantee|rate|analysis)|polynomial[- ]time|\btheor(?:y|etical)\b",
                  ctx=r"reinforcement learning|\bmdps?\b|markov decision|\brl\b|q-learning|temporal[- ]difference", min_abs=2),
            ]),
            ("value_based", "值函数 / TD 学习 / Actor-Critic", "Value-based, TD & Actor-Critic", [
                R(r"q-learning|value functions?|temporal[- ]difference|\btd\(|\btd learning|actor-critic|\bcritics?\b|bellman|distributional rl|\bdqn\b|\bsac\b"
                  r"|value estimation|off-policy (?:evaluation|learning|rl)", min_abs=2),
            ]),
        ],
    },
    {
        "id": "embodied",
        "zh": "具身智能 / 机器人 / 世界模型",
        "en": "Embodied AI, Robotics & World Models",
        "tags": [
            ("vla", "视觉-语言-动作模型（VLA）", "Vision-Language-Action Models", [
                R(r"vision[- ]language[- ]action|\bvlas?\b|\bpi[_-]?0(?:\.5)?\b|\bπ0|openvla|robot foundation models?|generalist robot polic"
                  r"|robot(?:ic)? (?:foundation )?polic(?:y|ies) .{0,30}(?:language|vlm)", min_abs=1),
            ]),
            ("manipulation", "机器人操作 / 灵巧手", "Robot Manipulation & Dexterity", [
                R(r"manipulation|grasp(?:ing)?\b|dexterous|bimanual|pick[- ]and[- ]place|robot(?:ic)? arms?", ctx=ROBOT, ctx_min=1, min_abs=1),
            ]),
            ("robot_all", "机器人学习（全部）", "Robot Learning (all)", [
                R(r"\brobot(?:s|ic|ics)?\b|embodied", min_abs=2),
                R(areas={"applications to robotics, autonomy, planning"}),
                R(include=["vla", "manipulation", "locomotion", "navigation"]),
            ]),
            ("world_models", "世界模型", "World Models", [
                R(r"world models?|world simulators?|world modell?ing|interactive (?:video )?(?:generation|world)|game engines?"
                  r"|neural simulators?|learned simulators?|generative (?:simulators?|environments?)", min_abs=2),
            ]),
            ("wam", "世界-动作模型 / 视频策略", "World Action Models / Video Policies", [
                R(r"world[- ]action models?|action[- ]conditioned (?:video|world)|video (?:policy|policies)|video[- ]action|unified (?:world model|video[- ]action)"
                  r"|\bwams?\b|video prediction policy|video (?:generation|diffusion) (?:models? )?(?:as|for) (?:robot )?polic", min_abs=1),
            ]),
            ("driving", "自动驾驶", "Autonomous Driving", [
                R(r"autonomous driving|self[- ]driving|end-to-end driving|driving (?:scenes?|policy|policies|simulation|world)|\bnuscenes\b|\bnavsim\b"
                  r"|autonomous vehicles?|motion forecasting|trajectory prediction", min_abs=1),
            ]),
            ("navigation", "具身导航", "Embodied Navigation", [
                R(r"(?:vision[- ]language|visual|embodied|object[- ]goal|robot(?:ic)?|image[- ]goal) navigation|\bvln\b|navigation (?:agents?|polic(?:y|ies)|tasks?)|\bhabitat\b", min_abs=1),
            ]),
            ("locomotion", "运动控制 / 人形机器人 / Sim2Real", "Locomotion, Humanoids & Sim2Real", [
                R(r"locomotion|humanoids?|legged|quadruped|whole[- ]body control|sim[- ]to[- ]real|sim2real|motion tracking", min_abs=1),
            ]),
            ("motion", "人体动作生成 / 数字人", "Human Motion Generation & Avatars", [
                R(r"human motion|motion generation|motion synthesis|text[- ]to[- ]motion|avatars?|human[- ]object interaction|hand[- ]object|human pose|human video"
                  r"|human mesh|hand (?:motion|pose|mesh)|body (?:pose|mesh)", min_abs=1),
            ]),
            ("planning", "规划（LLM / 经典）", "Planning", [
                R(r"\bplanning\b|\bplanners?\b|task planning|\bpddl\b|motion planning|long-horizon planning", min_abs=2),
            ]),
        ],
    },
    {
        "id": "interp",
        "zh": "可解释性",
        "en": "Interpretability",
        "tags": [
            ("interp_all", "可解释性（全部）", "Interpretability (all)", [
                R(r"interpretab|explainab|\bxai\b|mechanistic", min_abs=99),
                R(areas={"interpretability and explainable AI"}),
                R(include=["mech_interp", "sae", "steering", "attribution", "concept", "cot_faith"]),
            ]),
            ("mech_interp", "机制可解释性 / 电路分析", "Mechanistic Interpretability & Circuits", [
                R(r"mechanistic interpretab|circuit (?:discovery|analysis|tracing)|attribution graphs?|activation patching|causal (?:tracing|mediation|abstraction)"
                  r"|path patching|induction heads?|logit lens|tuned lens|superposition|polysemantic|monosemantic|reverse[- ]engineer", min_abs=1),
                R(r"\bmechanistic(?:ally)?\b|\bcircuits?\b",
                  ctx=r"interpretab|transformers?|language models?|\bllms?\b|neural networks?|attention heads?", ctx_min=1, min_abs=2),
            ]),
            ("sae", "稀疏自编码器 / 字典学习（SAE）", "Sparse Autoencoders & Dictionary Learning", [
                R(r"sparse auto-?encoders?|transcoders?|crosscoders?|dictionary learning|sparse dictionar|monosemantic features", min_abs=1),
                R(acr=r"\bSAEs?\b", min_abs=1),
            ]),
            ("probing", "探针 / 表征分析与几何", "Probing & Representation Analysis/Geometry", [
                R(r"linear probes?|probing (?:classifiers?|experiments?|analys[ie]s|tasks?|studies)|representation(?:al)? (?:analysis|geometry|similarity analysis)"
                  r"|linear representation hypothesis|\bcka\b|truth directions?|world representations?|probe accuracy|(?:trained|train|training) (?:linear )?probes"
                  r"|(?:internal|hidden|latent) representations? (?:encode|of (?:llms?|language models|transformers))", min_abs=1),
                R(r"\bprob(?:e|es|ing)\b", ctx=r"representations?|hidden states?|activations?|residual stream|internal states?", min_abs=2),
            ]),
            ("steering", "激活引导 / 表征工程（Steering）", "Activation Steering & Representation Engineering", [
                R(r"activation steering|steering vectors?|representation engineering|\brepe\b|activation (?:addition|editing|intervention)"
                  r"|inference[- ]time intervention|steer(?:ing|ability)? (?:llms?|language models?|models?|behaviou?rs?|generation)"
                  r"|concept (?:vectors?|directions?)|contrastive activation", min_abs=1),
                R(r"\bsteer(?:ing|s|ed)?\b", ctx=LLM, min_abs=2),
            ]),
            ("attribution", "特征归因 / 数据归因 / XAI", "Feature & Data Attribution / XAI", [
                R(r"feature attribution|saliency|shapley|\bshap\b|integrated gradients|attribution methods?|explainab|\bxai\b|post[- ]hoc explanations?"
                  r"|counterfactual explanations?|local explanations?|\blime\b|grad-?cam|data attribution|influence functions?|training data attribution", min_abs=2),
            ]),
            ("concept", "概念模型 / 可解释模型设计", "Concept-based & Inherently Interpretable Models", [
                R(r"concept bottleneck|concept[- ]based (?:models?|explanations?|interpretab)|inherently interpretable|interpretable[- ]by[- ]design"
                  r"|interpretable (?:models?|machine learning|neural)|prototype(?:-based)? (?:networks|learning|models?)|self-explaining|glass-box"
                  r"|generalized additive|symbolic regression", min_abs=1),
            ]),
            ("cot_faith", "CoT 忠实性与监控", "CoT Faithfulness & Monitoring", [
                R(r"(?:cot|chain[- ]of[- ]thought|reasoning) (?:faithfulness|monitor(?:ing|ability|s)?)|faithful(?:ness)? (?:of )?(?:the )?(?:reasoning|chain|explanations?|cot)"
                  r"|unfaithful|monitorability|cot monitor|reasoning (?:transparency|legibility)", min_abs=1),
            ]),
            ("memorization", "记忆 / 数据污染", "Memorization & Contamination", [
                R(r"memori[sz](?:ation|e|es|ed|ing)|verbatim|training data extraction|extraction attacks?|data contamination|benchmark contamination|contaminat", min_abs=2),
            ]),
        ],
    },
    {
        "id": "safety",
        "zh": "安全、对齐与可信",
        "en": "Safety, Alignment & Trust",
        "tags": [
            ("jailbreak", "越狱 / 红队测试", "Jailbreaks & Red-teaming", [
                R(r"jailbreak|red[- ]team|adversarial prompts?|harmful (?:requests?|prompts?|queries|instructions)", min_abs=1),
            ]),
            ("safety_align", "安全对齐 / 拒答 / 护栏", "Safety Alignment, Refusal & Guardrails", [
                R(r"safety alignment|safety fine-?tun|safety training|\brefusals?\b|over-?refusal|guardrails?|harmless|content moderation"
                  r"|safety classifiers?|llm safety|ai safety|catastrophic risks?|dangerous capabilit|\bmisuse\b|safety cases?|safety-critical behaviou?r", min_abs=1),
            ]),
            ("prompt_injection", "Prompt 注入 / 智能体安全", "Prompt Injection & Agent Security", [
                R(r"prompt injection|indirect injection|agent(?:ic)? (?:security|safety|risks?)|tool poisoning|memory poisoning|agent hijack"
                  r"|secur(?:e|ity) of (?:llm )?agents|sandbox escape|unsafe actions", min_abs=1),
            ]),
            ("backdoor", "后门 / 数据投毒", "Backdoors & Data Poisoning", [
                R(r"backdoors?|trojan|data poisoning|poisoning attacks?|poisoned", min_abs=1),
            ]),
            ("adv", "对抗鲁棒性", "Adversarial Robustness", [
                R(r"adversarial (?:robustness|attacks?|examples?|training|perturbations?|defen[cs]es?)|certified robust|randomi[sz]ed smoothing"
                  r"|robust(?:ness)? (?:to|against) adversarial|evasion attacks?", min_abs=1),
            ]),
            ("deception", "欺骗 / 谄媚 / 谋划 / 涌现失准", "Deception, Sycophancy, Scheming & Misalignment", [
                R(r"sycophan|decepti(?:on|ve)|scheming|sandbagging|alignment faking|situational awareness|evaluation awareness|hidden objectives?"
                  r"|strategic (?:deception|underperformance)|emergent misalignment|misaligned (?:models?|ai|behaviou?rs?|llms?|agents?)"
                  r"|agentic misalignment|power[- ]seeking|\bhonesty\b|\blying\b|persuasion", min_abs=1),
            ]),
            ("alignment", "AI 对齐 / 价值对齐 / 可扩展监督", "AI Alignment, Values & Scalable Oversight", [
                R(r"ai alignment|value alignment|human values|pluralistic alignment|aligning (?:llms?|language models|ai)|alignment of (?:llms?|language models)"
                  r"|\bllm alignment|constitutional|superalignment|scalable oversight|weak[- ]to[- ]strong|ai control|moral|ethic", min_abs=1),
            ]),
            ("unlearning", "机器遗忘 / 概念擦除", "Machine Unlearning & Concept Erasure", [
                R(r"unlearn|right to be forgotten|concept erasure|eras(?:e|ing) concepts?|forget sets?", min_abs=1),
            ]),
            ("privacy", "隐私 / 差分隐私 / 成员推断", "Privacy, DP & Membership Inference", [
                R(r"differential(?:ly)? privacy|differentially private|\bdp-sgd\b|membership inference|privacy[- ]preserv|privacy (?:attacks?|leakage|risks?|guarantees?)"
                  r"|data reconstruction attacks?|private (?:learning|training|inference|data)", min_abs=1),
            ]),
            ("federated", "联邦学习", "Federated Learning", [
                R(r"federated", min_abs=1),
            ]),
            ("watermark", "水印 / AIGC 检测 / 深度伪造", "Watermarking, AIGC Detection & Deepfakes", [
                R(r"watermark|ai[- ]generated (?:text|images?|content|videos?)|machine[- ]generated text|detect(?:ing|ion of)? (?:ai|machine|llm)[- ]generated"
                  r"|deepfake|forgery detection|fake (?:images?|news|videos?)|copyright|content provenance", min_abs=1),
            ]),
            ("fairness", "公平性与偏见", "Fairness & Bias", [
                R(r"fairness|\bfair\b|social bias|gender bias|racial bias|stereotyp|demographic|discriminat(?:ion|ory)|\bequit(?:y|able)\b|bias(?:es)? (?:in|of|against) (?:llms?|models?|language)", min_abs=2),
            ]),
        ],
    },
    {
        "id": "reliable",
        "zh": "可靠性与泛化",
        "en": "Reliability & Generalization",
        "tags": [
            ("uq", "不确定性 / 校准 / 共形预测", "Uncertainty, Calibration & Conformal Prediction", [
                R(r"uncertainty (?:quantification|estimation|estimates?|calibration|aware)|conformal|selective prediction|abstention|abstain"
                  r"|epistemic uncertainty|aleatoric|confidence estimation|predictive uncertainty|prediction (?:sets|intervals)", min_abs=1),
                R(r"confidence calibration|calibration error|\bece\b|well[- ]calibrated|miscalibrat|overconfiden|calibrated (?:confidence|uncertaint|probabilit|predictions?)"
                  r"|model calibration|calibration of (?:llms?|language models|neural|classifiers?|models?|confidence)", min_abs=1),
            ]),
            ("ood", "OOD 检测 / 分布偏移 / 虚假相关", "OOD, Distribution Shift & Spurious Correlations", [
                R(r"out[- ]of[- ]distribution|\bood\b|distribution(?:al)? shifts?|covariate shift|domain shift|spurious (?:correlations?|features)"
                  r"|shortcut learning|subpopulation shift|anomaly detection|novelty detection", min_abs=2),
            ]),
            ("adaptation", "领域适应 / 领域泛化 / 测试时适应", "Domain Adaptation / Generalization / TTA", [
                R(r"domain adaptation|domain generali[sz]ation|test[- ]time adaptation|\btta\b|unsupervised domain|source[- ]free|transfer learning", min_abs=1),
            ]),
            ("continual", "持续学习 / 灾难性遗忘", "Continual Learning & Forgetting", [
                R(r"continual(?:ly)? learn|lifelong learning|catastrophic(?:ally)? forget|class[- ]incremental|incremental learning|loss of plasticity|plasticity loss"
                  r"|stability[- ]plasticity|continual (?:pre-?training|fine-?tuning|adaptation)", min_abs=1),
            ]),
        ],
    },
    {
        "id": "efficiency",
        "zh": "高效机器学习",
        "en": "Efficient ML",
        "tags": [
            ("quant", "量化", "Quantization", [
                R(r"(?<!vector )(?<!vector-)quanti[sz](?:ation|ed|ing|e)\b|low[- ]bit|\bint[248]\b|\bfp[48]\b|\bmxfp\d|\bnvfp4\b|binari[sz]|\bw\da\d|[1-4]-bit|ternary", min_abs=1),
            ]),
            ("pruning", "剪枝与稀疏化", "Pruning & Sparsity", [
                R(r"\bprun(?:e|ed|ing)\b|sparsit|sparsif|\bn:m\b|2:4 sparsity|structured sparse|weight sparse|lottery ticket", min_abs=2),
            ]),
            ("kv_cache", "KV Cache 优化", "KV Cache", [
                R(r"kv[- ]?cache|key[- ]value cache|\bkv (?:compression|eviction|quantization|states?)|cache (?:eviction|compression)|prefix caching", min_abs=1),
            ]),
            ("spec_decode", "投机解码 / 并行解码 / 多 Token 预测", "Speculative & Parallel Decoding / MTP", [
                R(r"speculative (?:decoding|sampling|generation|inference)|draft models?|parallel decoding|multi[- ]token prediction|\bmtp\b"
                  r"|lookahead decoding|\bmedusa\b|\beagle-?\d?\b|jacobi decoding|self-speculative", min_abs=1),
            ]),
            ("systems", "推理服务 / 系统 / 硬件", "Serving, Systems & Hardware", [
                R(r"\bserving\b|inference (?:systems?|engines?|serving|throughput|latency)|throughput|\bgpu (?:kernels?|memory|utili[sz]ation)"
                  r"|distributed training|(?:pipeline|tensor|data|expert|sequence|context) parallel(?:ism)?|\bvllm\b|\bsglang\b|disaggregat"
                  r"|on-device|edge devices?|mobile devices?|\bfpgas?\b|compilers?\b|hardware[- ]aware|memory bandwidth", min_abs=2),
            ]),
            ("efficient_train", "高效训练 / 低精度训练", "Efficient & Low-precision Training", [
                R(r"efficient (?:training|pre-?training|fine-?tuning)|training efficiency|low[- ]precision training|mixed[- ]precision|fp8 training"
                  r"|memory[- ]efficient (?:training|fine-?tuning|optimi[sz])|gradient checkpointing|compute[- ]efficient training|communication[- ]efficient", min_abs=1),
            ]),
            ("routing", "模型路由 / 级联", "Model Routing & Cascades", [
                R(r"model routing|llm routing|(?:llm|model|query) routers?|model cascades?|cascad(?:e|ing) (?:of )?(?:models|llms)"
                  r"|routing (?:queries|requests|among|between|across) (?:llms|models)|route (?:queries|requests)", min_abs=1),
            ]),
            ("efficient_all", "高效推理（全部）", "Efficient Inference (all)", [
                R(r"efficient inference|inference (?:efficiency|acceleration|cost|speed-?up)|accelerat(?:e|ing) inference|speed-?ups?|latency|wall-clock", min_abs=2),
                R(include=["quant", "kv_cache", "spec_decode", "routing", "efficient_reasoning", "token_compress", "adaptive_compute"]),
            ]),
        ],
    },
    {
        "id": "theory",
        "zh": "优化与理论",
        "en": "Optimization & Theory",
        "tags": [
            ("optimizers", "优化器（Muon / Adam / 二阶等）", "Optimizers (Muon, Adam, second-order...)", [
                R(r"\bmuon\b|\badamw?\b|shampoo|\bsoap\b|\boptimizers?\b|second[- ]order (?:optimi[sz]|methods?)|precondition|learning rates?"
                  r"|sharpness[- ]aware|weight decay|\bmomentum\b|natural gradient|sign(?:sgd| descent)|orthogonali[sz]ed (?:updates?|gradients?)"
                  r"|spectral (?:norm )?(?:descent|updates?)|steepest descent", min_abs=2),
            ]),
            ("opt_theory", "优化理论", "Optimization Theory", [
                R(r"convergence (?:rates?|analysis|guarantees?)|(?:non-?)?convex|stochastic gradient|\bsgd\b|gradient descent|minimax optimi|saddle[- ]point"
                  r"|variational inequalit|bilevel|zeroth[- ]order|derivative[- ]free|distributed optimi|oracle complexity|first-order methods?", min_abs=2),
                R(areas={"optimization"}),
            ]),
            ("learning_theory", "学习理论（泛化 / 样本复杂度）", "Learning Theory (generalization, sample complexity)", [
                R(r"generali[sz]ation bounds?|sample complexity|pac[- ]bayes|\bpac\b|vc[- ]dimension|rademacher|statistical rates?|minimax (?:rates?|optimal|lower)"
                  r"|excess risk|uniform convergence|learnability|benign overfitting|information[- ]theoretic (?:bounds?|limits?|lower)", min_abs=1),
                R(areas={"learning theory"}),
            ]),
            ("dl_theory", "深度学习理论（NTK / 平均场 / 特征学习）", "Deep Learning Theory (NTK, mean-field, feature learning)", [
                R(r"neural tangent|\bntk\b|mean[- ]field|infinite[- ]width|feature learning|lazy (?:training|regime)|overparameteri[sz]|implicit (?:bias|regulari[sz]ation)"
                  r"|two-layer (?:neural )?networks?|shallow networks?|single[- ]index|multi[- ]index|teacher[- ]student setting|scaling limits?"
                  r"|\bmup\b|μp|maximal update|deep linear networks?", min_abs=1),
            ]),
            ("transformer_theory", "Transformer 理论 / 表达能力", "Transformer Theory & Expressivity", [
                R(r"expressiv(?:e power|ity)|circuit complexity|\btc\^?0\b|turing[- ]complete|formal languages?|state tracking|\bautomata\b"
                  r"|provabl[ey].{0,60}(?:transformers?|attention|in-context)|theoretical (?:analysis|understanding|framework) (?:of|for) (?:transformers?|attention|in-context|chain)"
                  r"|transformers? (?:can|provably|learn to)", min_abs=1),
            ]),
            ("dynamics", "训练动力学 / 深度学习科学（Grokking 等）", "Training Dynamics & Science of DL", [
                R(r"training dynamics|learning dynamics|grokking|loss landscapes?|neural collapse|edge of stability|emergen(?:ce|t) (?:abilities|capabilit)"
                  r"|phase transitions? (?:in|during) (?:training|learning)|double descent|simplicity bias|lottery ticket|mode connectivity|loss spikes?", min_abs=1),
            ]),
            ("ot", "最优传输 / 薛定谔桥", "Optimal Transport & Schrödinger Bridges", [
                R(r"optimal transport|wasserstein|sinkhorn|schr[oö]dinger bridges?|gromov", min_abs=1),
                R(acr=r"\bOT\b", min_abs=2),
            ]),
            ("game", "博弈论 / 机制设计 / 经济学", "Game Theory, Mechanism Design & Economics", [
                R(r"game[- ]theor|\bnash\b|stackelberg|correlated equilibri|equilibri(?:um|a) (?:computation|selection|learning|finding)|mechanism design"
                  r"|auctions?|social choice|\bvoting\b|strategic (?:agents|behaviou?r|classification)|regret matching|extensive[- ]form|normal[- ]form"
                  r"|zero[- ]sum|general[- ]sum|potential games?|matrix games?|imperfect[- ]information|economics?\b|\bmarkets?\b|\bpricing\b", min_abs=2),
            ]),
        ],
    },
    {
        "id": "rep",
        "zh": "表征学习",
        "en": "Representation Learning",
        "tags": [
            ("ssl", "自监督 / 对比学习", "Self-supervised & Contrastive Learning", [
                R(r"self[- ]supervised|contrastive (?:learning|loss|objectives?|pre-?training|representation)|\bsimclr\b|\bbyol\b|\bdino(?:v\d)?\b"
                  r"|masked (?:image modell?ing|autoencoders?)|\bmae\b|pretext tasks?|\binfonce\b", min_abs=1),
            ]),
            ("jepa", "JEPA / 隐空间预测", "JEPA & Latent Prediction", [
                R(r"\bjepa\b|joint[- ]embedding predictive|\b[ivl]-jepa|latent[- ]space prediction|predictive (?:representations?|coding)", min_abs=1),
            ]),
            ("rep_align", "表征对齐 / 柏拉图表征", "Representation Alignment / Platonic Representations", [
                R(r"representation(?:al)? (?:alignment|convergence|similarity)|platonic|\brepa\b|universal representations?|cross-model alignment", min_abs=1),
            ]),
            ("meta", "元学习 / 小样本", "Meta-learning & Few-shot", [
                R(r"meta[- ]learn|few[- ]shot learning|learning to learn|\bmaml\b", min_abs=1),
            ]),
            ("clustering", "聚类", "Clustering", [
                R(r"clustering|cluster assignments?", min_abs=2),
            ]),
            ("multimodal_rep", "多模态表征 / 融合", "Multimodal Representation & Fusion", [
                R(r"multimodal (?:representation|fusion|learning|alignment|pre-?training)|cross[- ]modal (?:alignment|learning|fusion)|modality (?:gap|alignment|fusion)", min_abs=1),
            ]),
        ],
    },
    {
        "id": "science",
        "zh": "AI for Science 与应用",
        "en": "AI for Science & Applications",
        "tags": [
            ("pde", "PDE / 神经算子 / 物理信息", "PDEs, Neural Operators & Physics-informed ML", [
                R(r"neural operators?|partial differential|\bpdes?\b|physics[- ]informed|\bpinns?\b|fourier neural operator|\bfno\b|fluid dynamics"
                  r"|navier[- ]stokes|computational fluid|turbulen|surrogate models?", min_abs=2),
            ]),
            ("molecule", "分子 / 化学 / 材料", "Molecules, Chemistry & Materials", [
                R(r"molecul|chemi(?:cal|stry)|\bdrugs?\b|drug discovery|ligand|docking|materials? (?:discovery|design|science|property)|crystal|retrosynthes"
                  r"|catalys|force fields?|interatomic|quantum chemistry|\bdft\b|conformer", min_abs=2),
            ]),
            ("bio", "蛋白质 / 生物 / 基因组 / 单细胞", "Proteins, Biology, Genomics & Single-cell", [
                R(r"protein|antibod|peptide|enzyme|\brna\b|\bdna\b|genom|gene expression|single[- ]cell|transcriptom|virtual cell"
                  r"|perturbation (?:prediction|response|effects?)|bioinformatic|biological sequences?", min_abs=2),
            ]),
            ("medical", "医疗健康", "Medicine & Healthcare", [
                R(r"medical|clinical|health ?care|patients?|disease|(?:medical|clinical|disease|cancer) diagnos|radiolog|patholog|\behrs?\b|electronic health"
                  r"|hospital|\bmri\b|x-?rays?|histopatholog|surgical|biomedical|\becg\b", min_abs=2),
            ]),
            ("neuro", "神经科学 / 脑解码 / 认知科学", "Neuroscience, Brain Decoding & Cognitive Science", [
                R(r"neuroscien|\bbrains?\b|neural (?:recordings?|activity|data|population|decoding)|\beeg\b|\bfmri\b|\bmeg\b|spike trains?|cortex|cortical"
                  r"|brain[- ]computer|\bbci\b|cognitive science|human cognition|psycholog", min_abs=2),
                R(areas={"applications to neuroscience & cognitive science"}),
            ]),
            ("earth", "气象 / 气候 / 遥感", "Weather, Climate & Remote Sensing", [
                R(r"weather|climate|precipitation|atmospher|\bocean|earth (?:system|observation)|remote sensing|satellite|geospatial|hyperspectral", min_abs=2),
            ]),
            ("quantum", "量子机器学习", "Quantum ML", [
                R(r"quantum (?:machine learning|comput|circuits?|neural|states?|many-body|systems?|algorithms?|error|hardware)|qubits?|variational quantum", min_abs=1),
            ]),
            ("physics", "物理 / 科学机器学习（其他）", "Physics & Scientific ML (other)", [
                R(r"scientific machine learning|ai for science|scientific discovery|physical systems?|\bphysics\b|astronom|cosmolog|particle physics|high-energy", min_abs=2),
            ]),
            ("timeseries", "时间序列", "Time Series", [
                R(r"time[- ]series|forecasting|spatio[- ]?temporal|temporal point process", min_abs=2),
                R(areas={"learning on time series and dynamical systems"}),
            ]),
            ("graph", "图学习 / GNN", "Graph Learning / GNNs", [
                R(r"graph neural|\bgnns?\b|graph (?:learning|representation|transformers?|generation|data|structured|classification|foundation|signal)"
                  r"|message[- ]passing|node classification|link prediction|knowledge graphs?|hypergraph|molecular graphs?", min_abs=2),
            ]),
            ("geometric", "几何深度学习 / 等变性", "Geometric DL & Equivariance", [
                R(r"equivarian|symmetr(?:y|ies)|geometric deep learning|\bmanifolds?\b|hyperbolic|lie groups?|\bse\(3\)|\be\(3\)|riemannian"
                  r"|topological (?:data|deep)|persistent homology|sheaf", min_abs=2),
            ]),
            ("tabular", "表格数据", "Tabular Data", [
                R(r"tabular|\btabpfn\b|spreadsheets?", min_abs=1),
            ]),
            ("recsys", "推荐系统", "Recommender Systems", [
                R(r"recommend(?:er|ation)s?\b|collaborative filtering|click[- ]through|\bctr\b|user[- ]item", min_abs=2),
            ]),
            ("combopt", "组合优化 / 运筹", "Combinatorial Optimization & OR", [
                R(r"combinatorial optimi|neural combinatorial|vehicle routing|\btsp\b|traveling salesman|mixed[- ]integer|\bmilp\b|operations research"
                  r"|integer (?:linear )?programming|\bsat solv|linear programming|job[- ]shop|scheduling problems?", min_abs=1),
            ]),
            ("neurosymbolic", "神经符号 / 形式化验证 / 逻辑推理", "Neurosymbolic, Formal Verification & Logic", [
                R(r"neuro[- ]?symbolic|formal verification|program verification|logical reasoning|symbolic reasoning|first[- ]order logic"
                  r"|theorem provers?|\bsmt\b|formal methods|verified code|logic programming", min_abs=1),
            ]),
        ],
    },
    {
        "id": "prob",
        "zh": "概率与因果",
        "en": "Probabilistic & Causal",
        "tags": [
            ("causal", "因果推断 / 因果发现", "Causal Inference & Discovery", [
                R(r"causal (?:inference|discovery|effects?|graphs?|structure|representation|models?|identification|estimation|bandits?)|causality"
                  r"|treatment effects?|instrumental variables?|do-calculus|structural causal|potential outcomes|unmeasured confound", min_abs=1),
                R(r"counterfactual|confound|identifiab", ctx=r"\bcausal", ctx_min=1, min_abs=2),
            ]),
            ("bayes", "贝叶斯 / 变分推断 / 采样", "Bayesian, Variational Inference & Sampling", [
                R(r"bayesian|variational inference|\bmcmc\b|markov chain monte carlo|langevin|sequential monte carlo|posterior (?:inference|approximation)"
                  r"|gaussian process|importance sampling|sampling from (?:unnormali[sz]ed|boltzmann)|boltzmann|amortized inference|probabilistic (?:models?|inference|programming)", min_abs=2),
            ]),
            ("bo_automl", "贝叶斯优化 / 黑盒优化 / AutoML / 进化搜索", "Bayesian Opt., Black-box, AutoML & Evolutionary Search", [
                R(r"bayesian optimi[sz]ation|black[- ]box optimi[sz]ation|experimental design|active learning|hyperparameter optimi|neural architecture search"
                  r"|\bnas\b|automl|evolutionary (?:algorithms?|search|strategies|computation)|genetic (?:algorithms?|programming)|alphaevolve|program search", min_abs=1),
            ]),
            ("stats", "统计推断 / 假设检验", "Statistical Inference & Testing", [
                R(r"hypothesis test|two[- ]sample test|statistical (?:inference|tests?|testing)|p-values?|confidence intervals?|e-values?|sequential testing"
                  r"|false discovery|prediction-powered|semiparametric|doubly robust", min_abs=1),
            ]),
        ],
    },
    {
        "id": "data",
        "zh": "数据与评测",
        "en": "Data & Evaluation",
        "tags": [
            ("benchmark", "新 Benchmark / 数据集", "New Benchmarks & Datasets", [
                R(areas={"datasets and benchmarks"}),
                R(r"bench(?:mark)?s?\b|\bdatasets?\b|\bcorpus\b|\barena\b", min_abs=99),
                R(r"we (?:introduce|present|propose|release|construct|build|curate|develop) (?:\w+[ -]){0,8}?(?:benchmark|dataset|suite|testbed)", min_abs=1),
            ]),
            ("eval_method", "评测方法论", "Evaluation Methodology", [
                R(r"evaluation (?:methodology|protocols?|practices|validity|science|pitfalls)|benchmark (?:validity|saturation|reliability|quality|design)"
                  r"|psychometric|item response|construct validity|meta-?evaluation|leaderboards?|measurement (?:error|validity)|reproducibility crisis", min_abs=1),
                R(r"evaluation metrics?|reproducib|statistical significance", min_abs=99),
            ]),
            ("synthetic", "合成数据 / 模型坍塌", "Synthetic Data & Model Collapse", [
                R(r"synthetic data|data synthesis|synthesi[sz]ed (?:data|datasets?|examples|instructions)|model collapse|generated (?:training )?data|data generation pipelines?", min_abs=1),
            ]),
            ("data_select", "数据选择 / 数据配比 / 数据集蒸馏", "Data Selection, Mixing & Dataset Distillation", [
                R(r"data (?:selection|curation|filtering|pruning|mixture|mixing|quality|valuation|efficien)|coresets?|dataset (?:distillation|condensation|pruning)"
                  r"|curriculum", min_abs=1),
            ]),
        ],
    },
]
