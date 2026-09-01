---
layout: default
title: "Horizon Summary: 2026-09-01 (ZH)"
date: 2026-09-01
lang: zh
---

> From 59 items, 3 important content pieces were selected

---

1. [Slotstream 使低内存 Mac 能够以良好速度运行超大语言模型](#item-1) ⭐️ 9.0/10
2. [I trained a small transformer in 1.5hrs and it beats many LLMs](#item-2) ⭐️ 9.0/10
3. [Movie Scene Map – 13,312 films, series, games, anime and manga](#item-3) ⭐️ 8.0/10

---

<a id="item-1"></a>
## [Slotstream 使低内存 Mac 能够以良好速度运行超大语言模型](https://github.com/carloslfu/slotstream) ⭐️ 9.0/10

slotstream 项目推出了一种方法，通过利用专家卸载和 SSD 流式传输，在低内存 Mac（16GB-48GB）上以大约每秒 12 个 token 的速度运行 100GB+ 的大型语言模型，特别是 Qwen3.8-Flash-Next 4-bit，该项目使用 MLX 和 Swift 原生构建。 这一创新显著降低了在消费级 Mac 上本地运行强大大型语言模型的门槛，使内存有限的用户也能使用先进的 AI 功能。 该项目专门针对通常需要超过 100GB RAM 的 125B 参数 Qwen3.8-Flash-Next 4-bit 模型，通过采用专家卸载和 SSD 流式传输，在内存低至 16GB 的 Mac 上实现了运行，并计划未来通过 MTP 模块实现推测解码。

hackernews · carloslfu · Sep 1, 16:42 · [社区讨论](https://news.ycombinator.com/item?id=49524447)

**背景**: 大型语言模型（LLM）是经过海量数据集训练的 AI 模型，能够生成类人文本，而在设备上本地运行它们（称为本地推理）通常需要大量内存。专家卸载和 SSD 流式传输是内存优化技术，允许模型的某些部分仅在需要时才从较慢的存储（如 SSD）加载，从而有效扩展可用 RAM。MLX 是 Apple 针对 Apple 芯片优化的机器学习框架，Swift 是 Apple 的编程语言，两者都用于原生开发。

**社区讨论**: 社区表现出高度参与，用户讨论了在不同 Mac 配置上的性能预期，寻求扩大上下文窗口，并质疑大型模型在实际应用中的优势。同时，也有关于项目文档的建设性反馈，以及对低端硬件上在没有散热问题的情况下实现性能的某些怀疑。

**标签**: `#Large Language Models`, `#Local Inference`, `#Memory Optimization`, `#Mac Development`, `#AI/ML Engineering`

---

<a id="item-2"></a>
## [I trained a small transformer in 1.5hrs and it beats many LLMs](https://mvakde.github.io/blog/44-on-arc-1/) ⭐️ 9.0/10

A researcher trained a small transformer in 1.5 hours that achieved top performance on the Abstraction and Reasoning Corpus (ARC) benchmark, outperforming many large language models and demonstrating an efficient approach to complex AI problems.

hackernews · porridgeraisin · Sep 1, 09:52 · [社区讨论](https://news.ycombinator.com/item?id=49519939)

**标签**: `#AI/ML`, `#Transformers`, `#Efficient AI`, `#Benchmarking`, `#Abstraction and Reasoning Corpus (ARC)`

---

<a id="item-3"></a>
## [Movie Scene Map – 13,312 films, series, games, anime and manga](https://moviescenemap.com/) ⭐️ 8.0/10

Movie Scene Map is a web service that geographically maps over 13,000 film, series, game, anime, and manga scenes, offering a novel way to explore media locations.

hackernews · Flightmussy · Sep 1, 16:34 · [社区讨论](https://news.ycombinator.com/item?id=49524320)

**标签**: `#Data Visualization`, `#Web Application`, `#Media Curation`, `#Geographic Data`

---