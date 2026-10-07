# ICLR 2027 投稿分类统计

有效投稿 42,378 篇（另有撤稿 216、desk reject 419，不计入下表）。每篇平均 4.0 个标签，未命中任何标签 466 篇（1.1%）。标签可重叠，所以各标签数量之和大于论文总数。

## 一级：OpenReview primary area（作者自选）

| Primary area | 篇数 |
|---|---:|
| foundation or frontier models, including LLMs | 6,679 |
| applications to computer vision, audio, language, and other modalities | 5,461 |
| alignment, fairness, safety, privacy, and societal considerations | 3,231 |
| datasets and benchmarks | 3,133 |
| generative models | 2,877 |
| reinforcement learning | 2,369 |
| applications to robotics, autonomy, planning | 2,237 |
| unsupervised, self-supervised, semi-supervised, and supervised representation learning | 2,130 |
| applications to physical sciences (physics, chemistry, biology, etc.) | 1,958 |
| interpretability and explainable AI | 1,777 |
| optimization | 1,592 |
| learning theory | 1,370 |
| transfer learning, meta learning, and lifelong learning | 1,165 |
| other topics in machine learning (i.e., none of the above) | 1,139 |
| learning on time series and dynamical systems | 1,138 |
| learning on graphs and other geometries & topologies | 945 |
| probabilistic methods (Bayesian methods, variational inference, sampling, UQ, etc.) | 875 |
| applications to neuroscience & cognitive science | 708 |
| infrastructure, software libraries, hardware, systems, etc. | 690 |
| neurosymbolic & hybrid AI systems (physics-informed, logic & formal reasoning, etc.) | 558 |
| causal reasoning | 346 |

## 二级：细分标签（规则匹配，见 `scripts/taxonomy.py`）

### LLM 训练与推理（LLM Training & Reasoning）— 22,421 篇

| 标签 | English | 篇数 |
|---|---|---:|
| LLM 相关（全部） | LLM-related (all) | 17,084 |
| LLM 推理 / 思维链 / 推理模型 | LLM Reasoning / CoT / Reasoning Models | 3,504 |
| LLM 强化学习（RLVR / GRPO） | RL for LLMs (RLVR/GRPO) | 3,098 |
| 知识蒸馏（通用） | Knowledge Distillation | 2,129 |
| 参数高效微调（LoRA / PEFT） | PEFT / LoRA | 1,230 |
| 自我改进 / 自进化 / Self-Play | Self-Improvement / Self-Evolution / Self-Play | 1,191 |
| 代码生成 | Code Generation | 1,125 |
| 检索增强 / 检索 / Embedding | RAG, Retrieval & Embeddings | 993 |
| 测试时扩展（Test-time Scaling） | Test-time Scaling & Search | 951 |
| 在线策略蒸馏（OPD） | On-Policy Distillation (OPD) | 912 |
| 指令微调 / SFT | Instruction Tuning & SFT | 875 |
| 长上下文 | Long Context | 726 |
| 奖励模型（ORM / PRM / Verifier） | Reward Models & Verifiers | 653 |
| 高效推理（Overthinking / 推理长度） | Efficient Reasoning (overthinking, length) | 631 |
| 数学推理与定理证明 | Math Reasoning & Theorem Proving | 545 |
| 幻觉与事实性 | Hallucination & Factuality | 491 |
| RLHF 与偏好优化（DPO 等） | RLHF & Preference Optimization | 480 |
| 个性化 / 角色扮演 / 用户模拟 | Personalization, Persona & User Simulation | 428 |
| 预训练与 Scaling Law | Pretraining & Scaling Laws | 416 |
| 上下文学习（ICL） | In-Context Learning | 389 |
| 隐式 / 连续空间推理 | Latent / Continuous Reasoning | 345 |
| LLM-as-a-Judge / 自动评测 | LLM-as-a-Judge | 338 |
| Tokenizer / 分词 | Tokenization | 331 |
| 多语言 / 翻译 | Multilingual & Translation | 331 |
| 模型合并 / 任务向量 | Model Merging & Task Vectors | 253 |
| 奖励欺骗（Reward Hacking） | Reward Hacking | 198 |
| 知识编辑 | Knowledge / Model Editing | 172 |

### 智能体（Agents）— 7,825 篇

| 标签 | English | 篇数 |
|---|---|---:|
| LLM 智能体（全部） | LLM Agents (all) | 6,775 |
| Harness / Skills / 上下文工程 / Prompt 优化 | Harness, Skills, Context Eng. & Prompt Optimization | 1,559 |
| 智能体评测 / Benchmark | Agent Benchmarks & Evaluation | 1,524 |
| 工具调用 / Function Calling / MCP | Tool Use / Function Calling / MCP | 1,301 |
| 智能体强化学习（Agentic RL） | Agentic RL | 986 |
| 智能体记忆 | Agent Memory | 984 |
| 多智能体系统（LLM） | LLM Multi-Agent Systems | 911 |
| 代码智能体 / SWE Agent | Coding / SWE Agents | 836 |
| 深度研究 / 搜索智能体 | Deep Research / Search Agents | 529 |
| GUI / Web / Computer-use 智能体 | GUI / Web / Computer-use Agents | 464 |
| AI 科学家 / 自动化研究 | AI Scientist & Automated Research | 261 |

### 模型架构（Architectures）— 3,433 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 混合专家（MoE） | Mixture-of-Experts | 818 |
| 注意力机制 / 稀疏注意力 | Attention Mechanisms / Sparse Attention | 652 |
| 线性注意力 / SSM / RNN | Linear Attention / SSM / RNN | 571 |
| 位置编码 / 长度泛化 | Positional Encoding & Length Generalization | 458 |
| 自适应计算 / Early Exit / 动态深度 | Adaptive Computation / Early Exit | 352 |
| 测试时训练 / 记忆层 / 联想记忆 | Test-time Training / Memory Layers / Associative Memory | 297 |
| 循环 / 递归深度 Transformer（Loop Transformer） | Looped / Recurrent-depth Transformers | 253 |
| KAN / 归一化 / 超网络等网络组件 | KANs, Normalization, Hypernetworks & Other Blocks | 231 |
| 脉冲 / 类脑网络 | Spiking & Neuromorphic | 219 |

### 生成模型（Generative Models）— 7,239 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 扩散模型（全部） | Diffusion Models (all) | 3,474 |
| Flow Matching / 归一化流 | Flow Matching & Normalizing Flows | 1,295 |
| 图像生成 / 文生图 | Image Generation / Text-to-Image | 1,266 |
| 视频生成 | Video Generation | 1,223 |
| 引导与可控生成（CFG 等） | Guidance & Controllable Generation | 759 |
| 少步生成 / 一致性模型 / 扩散加速 | Few-step / Consistency / Diffusion Acceleration | 696 |
| 逆问题 / 图像复原 / 底层视觉 | Inverse Problems, Restoration & Low-level Vision | 650 |
| 扩散语言模型 / 离散扩散 | Diffusion Language Models / Discrete Diffusion | 637 |
| 统一理解与生成模型 | Unified Understanding & Generation | 557 |
| 扩散模型对齐 / 奖励微调 | Diffusion Alignment & Reward Fine-tuning | 546 |
| 图像 / 视频编辑与个性化生成 | Image/Video Editing & Personalization | 521 |
| VAE / GAN / EBM / 其他生成模型 | VAEs / GANs / EBMs | 499 |
| 自回归视觉生成 / 视觉 Tokenizer | Autoregressive Visual Generation & Visual Tokenizers | 356 |
| 3D / 4D 生成 | 3D / 4D Generation | 269 |
| 扩散 / 生成模型理论 | Diffusion & Generative Model Theory | 212 |

### 多模态与视觉（Multimodal & Vision）— 9,486 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 视觉语言模型（VLM / MLLM） | Vision-Language Models (VLM/MLLM) | 4,294 |
| 检测 / 分割 / 跟踪 / 定位 | Detection, Segmentation, Tracking & Grounding | 1,486 |
| 3D 视觉（3DGS / NeRF / 重建） | 3D Vision (3DGS / NeRF / Reconstruction) | 1,460 |
| 音频 / 语音 / 音乐 | Audio, Speech & Music | 1,108 |
| 视频理解 | Video Understanding | 986 |
| CLIP / 图文对比学习 / 跨模态检索 | CLIP, Image-Text Contrastive & Cross-modal Retrieval | 937 |
| 空间推理 / 空间智能 | Spatial Reasoning / Spatial Intelligence | 648 |
| 多模态推理 | Multimodal Reasoning | 634 |
| 视觉骨干 / ViT / 图像分类 | Vision Backbones / ViT / Classification | 545 |
| Token 剪枝 / 压缩 | Token Pruning / Compression | 385 |
| 文档 / OCR / 图表理解 | Documents, OCR & Charts | 197 |

### 强化学习（Reinforcement Learning）— 6,771 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 强化学习（全部，含 LLM RL） | Reinforcement Learning (all, incl. RL for LLMs) | 5,928 |
| Bandit / 在线学习 | Bandits & Online Learning | 725 |
| 值函数 / TD 学习 / Actor-Critic | Value-based, TD & Actor-Critic | 653 |
| 模仿学习 / 行为克隆 / 逆强化学习 | Imitation Learning / BC / IRL | 392 |
| 离线强化学习 | Offline RL | 340 |
| 多智能体强化学习（MARL） | Multi-Agent RL | 334 |
| 目标条件 / 分层 / 无监督 RL | Goal-conditioned / Hierarchical / Unsupervised RL | 314 |
| 探索 / 内在激励 | Exploration & Intrinsic Motivation | 297 |
| 强化学习理论 | RL Theory | 255 |
| 基于模型的强化学习 | Model-based RL | 252 |
| 安全 / 约束强化学习 | Safe & Constrained RL | 151 |

### 具身智能 / 机器人 / 世界模型（Embodied AI, Robotics & World Models）— 5,279 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 机器人学习（全部） | Robot Learning (all) | 3,334 |
| 世界模型 | World Models | 1,387 |
| 机器人操作 / 灵巧手 | Robot Manipulation & Dexterity | 1,313 |
| 规划（LLM / 经典） | Planning | 1,209 |
| 视觉-语言-动作模型（VLA） | Vision-Language-Action Models | 1,012 |
| 自动驾驶 | Autonomous Driving | 596 |
| 人体动作生成 / 数字人 | Human Motion Generation & Avatars | 512 |
| 世界-动作模型 / 视频策略 | World Action Models / Video Policies | 494 |
| 运动控制 / 人形机器人 / Sim2Real | Locomotion, Humanoids & Sim2Real | 430 |
| 具身导航 | Embodied Navigation | 258 |

### 可解释性（Interpretability）— 4,468 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 可解释性（全部） | Interpretability (all) | 3,598 |
| 机制可解释性 / 电路分析 | Mechanistic Interpretability & Circuits | 1,260 |
| 探针 / 表征分析与几何 | Probing & Representation Analysis/Geometry | 1,052 |
| 激活引导 / 表征工程（Steering） | Activation Steering & Representation Engineering | 742 |
| 特征归因 / 数据归因 / XAI | Feature & Data Attribution / XAI | 513 |
| 稀疏自编码器 / 字典学习（SAE） | Sparse Autoencoders & Dictionary Learning | 344 |
| 记忆 / 数据污染 | Memorization & Contamination | 334 |
| 概念模型 / 可解释模型设计 | Concept-based & Inherently Interpretable Models | 302 |
| CoT 忠实性与监控 | CoT Faithfulness & Monitoring | 131 |

### 安全、对齐与可信（Safety, Alignment & Trust）— 4,663 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 安全对齐 / 拒答 / 护栏 | Safety Alignment, Refusal & Guardrails | 1,182 |
| 对抗鲁棒性 | Adversarial Robustness | 593 |
| 水印 / AIGC 检测 / 深度伪造 | Watermarking, AIGC Detection & Deepfakes | 568 |
| 隐私 / 差分隐私 / 成员推断 | Privacy, DP & Membership Inference | 544 |
| 联邦学习 | Federated Learning | 518 |
| 越狱 / 红队测试 | Jailbreaks & Red-teaming | 509 |
| Prompt 注入 / 智能体安全 | Prompt Injection & Agent Security | 458 |
| 机器遗忘 / 概念擦除 | Machine Unlearning & Concept Erasure | 434 |
| AI 对齐 / 价值对齐 / 可扩展监督 | AI Alignment, Values & Scalable Oversight | 373 |
| 欺骗 / 谄媚 / 谋划 / 涌现失准 | Deception, Sycophancy, Scheming & Misalignment | 359 |
| 公平性与偏见 | Fairness & Bias | 348 |
| 后门 / 数据投毒 | Backdoors & Data Poisoning | 336 |

### 可靠性与泛化（Reliability & Generalization）— 4,520 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 不确定性 / 校准 / 共形预测 | Uncertainty, Calibration & Conformal Prediction | 1,726 |
| OOD 检测 / 分布偏移 / 虚假相关 | OOD, Distribution Shift & Spurious Correlations | 1,381 |
| 领域适应 / 领域泛化 / 测试时适应 | Domain Adaptation / Generalization / TTA | 988 |
| 持续学习 / 灾难性遗忘 | Continual Learning & Forgetting | 922 |

### 高效机器学习（Efficient ML）— 5,864 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 高效推理（全部） | Efficient Inference (all) | 4,349 |
| 量化 | Quantization | 1,120 |
| 高效训练 / 低精度训练 | Efficient & Low-precision Training | 963 |
| 推理服务 / 系统 / 硬件 | Serving, Systems & Hardware | 936 |
| 剪枝与稀疏化 | Pruning & Sparsity | 844 |
| KV Cache 优化 | KV Cache | 843 |
| 投机解码 / 并行解码 / 多 Token 预测 | Speculative & Parallel Decoding / MTP | 402 |
| 模型路由 / 级联 | Model Routing & Cascades | 173 |

### 优化与理论（Optimization & Theory）— 5,913 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 优化理论 | Optimization Theory | 2,051 |
| 学习理论（泛化 / 样本复杂度） | Learning Theory (generalization, sample complexity) | 1,772 |
| 优化器（Muon / Adam / 二阶等） | Optimizers (Muon, Adam, second-order...) | 942 |
| 训练动力学 / 深度学习科学（Grokking 等） | Training Dynamics & Science of DL | 722 |
| 最优传输 / 薛定谔桥 | Optimal Transport & Schrödinger Bridges | 620 |
| 博弈论 / 机制设计 / 经济学 | Game Theory, Mechanism Design & Economics | 605 |
| Transformer 理论 / 表达能力 | Transformer Theory & Expressivity | 507 |
| 深度学习理论（NTK / 平均场 / 特征学习） | Deep Learning Theory (NTK, mean-field, feature learning) | 476 |

### 表征学习（Representation Learning）— 3,701 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 自监督 / 对比学习 | Self-supervised & Contrastive Learning | 1,848 |
| 多模态表征 / 融合 | Multimodal Representation & Fusion | 921 |
| JEPA / 隐空间预测 | JEPA & Latent Prediction | 489 |
| 聚类 | Clustering | 343 |
| 表征对齐 / 柏拉图表征 | Representation Alignment / Platonic Representations | 316 |
| 元学习 / 小样本 | Meta-learning & Few-shot | 267 |

### AI for Science 与应用（AI for Science & Applications）— 10,331 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 时间序列 | Time Series | 2,079 |
| 医疗健康 | Medicine & Healthcare | 1,422 |
| 图学习 / GNN | Graph Learning / GNNs | 1,315 |
| 物理 / 科学机器学习（其他） | Physics & Scientific ML (other) | 1,220 |
| 几何深度学习 / 等变性 | Geometric DL & Equivariance | 1,105 |
| 神经科学 / 脑解码 / 认知科学 | Neuroscience, Brain Decoding & Cognitive Science | 982 |
| 蛋白质 / 生物 / 基因组 / 单细胞 | Proteins, Biology, Genomics & Single-cell | 948 |
| 分子 / 化学 / 材料 | Molecules, Chemistry & Materials | 895 |
| PDE / 神经算子 / 物理信息 | PDEs, Neural Operators & Physics-informed ML | 681 |
| 表格数据 | Tabular Data | 557 |
| 神经符号 / 形式化验证 / 逻辑推理 | Neurosymbolic, Formal Verification & Logic | 489 |
| 气象 / 气候 / 遥感 | Weather, Climate & Remote Sensing | 475 |
| 组合优化 / 运筹 | Combinatorial Optimization & OR | 422 |
| 推荐系统 | Recommender Systems | 357 |
| 量子机器学习 | Quantum ML | 192 |

### 概率与因果（Probabilistic & Causal）— 2,701 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 贝叶斯 / 变分推断 / 采样 | Bayesian, Variational Inference & Sampling | 873 |
| 因果推断 / 因果发现 | Causal Inference & Discovery | 818 |
| 贝叶斯优化 / 黑盒优化 / AutoML / 进化搜索 | Bayesian Opt., Black-box, AutoML & Evolutionary Search | 768 |
| 统计推断 / 假设检验 | Statistical Inference & Testing | 546 |

### 数据与评测（Data & Evaluation）— 6,800 篇

| 标签 | English | 篇数 |
|---|---|---:|
| 新 Benchmark / 数据集 | New Benchmarks & Datasets | 4,570 |
| 评测方法论 | Evaluation Methodology | 1,451 |
| 数据选择 / 数据配比 / 数据集蒸馏 | Data Selection, Mixing & Dataset Distillation | 1,088 |
| 合成数据 / 模型坍塌 | Synthetic Data & Model Collapse | 804 |
