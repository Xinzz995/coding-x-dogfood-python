---
title: "Python API 规范化名称计数"
status: active
updated: 2026-08-05
scope: root
---

# Python API 规范化名称计数

## Context

Python Monorepo 的 API 包已经能够规范化单个或多个调用方名称，并能按首次出现顺序去重，
但调用方若要统计每个规范化名称的出现次数，仍需重复实现相同的规范化和计数逻辑。本任务用
公开 npm registry 独立安装的 `coding-x@0.34.0` 完成正式验证，同时保持两个 Python 包独立安装
和 GitHub 原生门禁不变。正式结果必须绑定 PR 最新提交、当前质量契约和公开稳定版本；旧候选、
旧提交或 Shadow 结果仅能作为历史记录，不能参与当前交付裁决。

## Goals

- 为 `dogfood_api` 新增统计规范化名称出现次数的公开函数。
- 复用现有名称规范化语义，并保留首次出现顺序。
- 保持调用方输入和所有既有公开函数行为不变。
- 使用公开 `coding-x@0.34.0` 对 PR 最新提交完成正式 Validator、本地三层 Review 和 Python 原生 CI。

## Non-Goals

- 不修改 Worker 包、质量契约、依赖或 GitHub 工作流。
- 不引入持久化、并发、网络、重试或发布行为。
- 不在 GitHub CI 安装 Node、npm 或 coding-x，也不在 GitHub 调用模型。
- 不复用 R6 PR #17 的分支、workspace、报告或本地 Review。
- 不把旧候选、旧提交或 Shadow 结果作为当前正式交付凭证。
- 不触发 npm staging 或 coding-x 发布流程。

## Golden Principles

| 原则 | 适用性与设计裁决 | 验证证据 |
|---|---|---|
| 可证伪完成合同 | 适用。验收测试先提交，并因公开函数尚不存在而失败。 | seed 提交、失败测试、功能实现提交。 |
| 生成方不得自签 | 适用。Developer 只实现，正式 Validator 和三层 Review 独立判断。 | 当前提交的 Validator receipt、三份 Review。 |
| 自治与可逆性对称 | 适用。实现只允许修改 API 实现文件，PR 保持开放。 | seed 到实现的文件差异。 |
| 复用原生执行面 | 适用。项目继续使用 Python、pytest、wheel 与 Ruff。 | 本地检查和 GitHub 三平台总闸。 |
| 失败与恢复优先 | 适用。公开版本、提交、契约或检查不一致时停止。 | 正式 doctor、当前提交绑定和远程检查。 |

## User Stories

### US-001: 统计规范化名称

作为 API 调用统计的使用者，我希望直接取得每个规范化名称的出现次数，从而无需在调用方重复
名称清理、匿名回退和计数逻辑。

#### Acceptance Criteria

- [ ] `dogfood_api` 公开新增 `normalized_name_counts(names: Sequence[str]) -> dict[str, int]`。
- [ ] 每个输入先沿用 `normalize_name` 的规则：去除首尾空白，空白名称归为 `anonymous`。
- [ ] 返回值按规范化名称首次出现顺序保存键，并记录每个名称的准确出现次数。
- [ ] 空序列返回空字典；函数接受可变列表与不可变序列，且不修改调用方输入。
- [ ] `normalize_name`、`normalize_names` 和 `normalize_unique_names` 的既有行为保持不变。
- [ ] 候选实现只修改 `packages/api/src/dogfood_api/__init__.py`；预置验收测试从 seed 到实现保持字节不变。
- [ ] API 与 Worker 两个包的 pytest、wheel 构建和 Ruff 检查全部通过。

## Verification

- 预置验收测试在 seed 提交上因缺少 `normalized_name_counts` 明确失败。
- 从 `https://registry.npmjs.org` 独立安装精确 `coding-x@0.34.0`，不使用本地压缩包、候选安装或 `npx`。
- 正式 doctor 确认运行版本和质量契约均为 `0.34.0`，workspace 安全健康且 GitHub 门禁就绪。
- 使用公开 `0.34.0` 针对 PR 最新提交重新派生 PRD，并顺序完成正式 Validator 与 Spec、工程标准、
  深度结构三层 Review；提交、PR 正文、Spec 或契约变化后不得复用旧结果。
- API 与 Worker 两个包分别完成 pytest、wheel 构建和 Ruff 检查。
- GitHub Linux、macOS、Windows 检查与 `quality-gate` 针对最终提交全部通过。

## 非规范历史记录

本功能曾使用 R7 固定候选在旧提交
`c5db8354b6144a2cd56e7d47b5484b8f2f0ba47c` 完成 Shadow 验证。该候选来自 coding-engine
`main` 提交 `61cf32673f1447f15dfd30e34bd611d0e6978c0e` 的 GitHub Actions 运行
`30961444465`，压缩包 SHA-256 为
`5d5a8ca03112ebc84d01ce6115a36cd4d45dcd15c3cb9bf6255fbb0bf4e0c20a`。

以上内容只用于追溯候选阶段，不是当前规格、运行入口、验收要求或交付凭证。公开 `0.34.0`、
PR 最新提交和本节之前的正式 Verification 才构成当前裁决边界。

## Rollback

若行为或证据不符合验收标准，通过新提交修复或回退 API 实现；不得修改预置测试、质量契约、
工作流或复用旧验证结果来取得绿色结果。任何修复提交都必须重新执行正式 Validator 和三层 Review。
