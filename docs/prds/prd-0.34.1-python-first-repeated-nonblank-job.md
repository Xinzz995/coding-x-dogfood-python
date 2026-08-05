---
title: "Python Worker 首个重复非空任务"
status: active
updated: 2026-08-06
scope: root
---

# Python Worker 首个重复非空任务

## Context

Python Monorepo 的 Worker 包已经能够清理任务名称、过滤空任务并按首次出现顺序去重，
但调用方若要找出遍历过程中最先第二次出现的有效任务，仍需重复实现相同的空白清理和
过滤逻辑。本任务为 `coding-x@0.34.1` 候选验证提供一个独立、可证伪的真实改动，同时
保持 API 与 Worker 两个包独立安装，以及 GitHub 原生质量门禁不变。

## Goals

- 为 `dogfood_worker` 新增查找首个重复非空任务的公开函数。
- 复用现有任务去除首尾空白、过滤空任务和保持遍历顺序的语义。
- 保持调用方输入以及所有既有公开函数行为不变。
- 以先失败的验收测试证明新行为在实现前并不存在。

## Non-Goals

- 不修改 API 包、质量契约、依赖或 GitHub 工作流。
- 不引入持久化、并发、网络、重试或发布行为。
- 不在 GitHub CI 安装 Node、npm 或 coding-x，也不在 GitHub 调用模型。
- 不把候选版本的 Shadow 结果解释为正式交付通过。

## Golden Principles

| 原则 | 适用性与设计裁决 | 验证证据 |
|---|---|---|
| 可证伪完成合同 | 适用。验收测试先提交，并因公开函数尚不存在而失败。 | seed 提交、失败测试、后续实现提交。 |
| 生成方不得自签 | 适用。实现与后续 Validator、Review 分开执行。 | 后续针对最终提交产生的独立结果。 |
| 自治与可逆性对称 | 适用。后续实现只允许修改 Worker 实现文件，且可由单一提交回退。 | seed 到实现的精确文件差异。 |
| 复用原生执行面 | 适用。项目继续使用 Python、pytest、wheel 与 Ruff。 | 本地检查和 GitHub 原生检查。 |
| 失败与恢复优先 | 适用。候选、提交或检查不一致时停止，不复用旧结果。 | 当前提交绑定和可重复执行的检查。 |

## User Stories

### US-001: 查找首个重复非空任务

作为任务队列的使用者，我希望直接取得遍历过程中最先第二次出现的有效任务，从而无需在
调用方重复实现任务清理、空值过滤和重复判断。

#### Acceptance Criteria

- [ ] `dogfood_worker` 公开新增
      `first_repeated_nonblank_job(jobs: Sequence[str]) -> str | None`。
- [ ] 每个任务沿用现有规则：去除首尾空白，并忽略清理后为空的任务。
- [ ] 按输入顺序遍历，返回第一个第二次出现的非空任务；
      `build, deploy, deploy, build` 返回 `deploy`。
- [ ] 空序列、全空白序列或没有重复有效任务时返回 `None`。
- [ ] 函数接受可变列表和不可变序列，且不修改调用方输入。
- [ ] `next_job`、`next_nonblank_job`、`nonblank_jobs` 和 `unique_nonblank_jobs`
      的既有行为保持不变。
- [ ] 候选实现只修改 `packages/worker/src/dogfood_worker/__init__.py`；预置验收测试
      从 seed 到实现保持字节不变。
- [ ] API 与 Worker 两个包的 pytest、wheel 构建和 Ruff 检查全部通过。

## Verification

- 预置验收测试在 seed 提交上仅因缺少 `first_repeated_nonblank_job` 明确失败。
- Worker 既有测试与 API 全部测试在 seed 提交上继续通过。
- 后续实现提交必须保持本规格与预置验收测试不变，并分别运行两个包的 pytest、wheel 构建
  和 Ruff 检查。
- 候选验证必须绑定精确的 coding-x 候选包、当前分支提交和对应检查结果；旧提交或旧结果
  不得复用。

## Rollback

若后续实现不符合验收标准，通过新提交修复或回退 Worker 实现；不得修改预置测试、质量
契约、工作流或复用旧验证结果来取得绿色结果。
