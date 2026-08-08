---
title: "Python Worker 重复非空任务列表"
status: active
updated: 2026-08-08
scope: root
---

# Python Worker 重复非空任务列表

## Context

Worker 包已经能取得首个重复非空任务，但调用方若要得到全部发生过重复的任务，仍需重复实现
空白清理、过滤和去重逻辑。本任务提供一个范围很小、可证伪的新能力，并用于验证同一
coding-x 0.35.0 候选包在 Python 多包项目中的完整 Shadow 流程。

## Goals

- 按每个任务第二次出现的顺序返回全部重复非空任务。
- 复用现有任务清理和过滤语义。
- 每个重复任务只返回一次，不修改调用方输入。
- 保持所有既有公开函数行为不变。

## Non-Goals

- 不修改 API 包、质量契约、依赖或 GitHub 工作流。
- 不返回次数，不排序结果，不引入持久化、并发、网络或发布行为。
- 不把候选 Shadow 结果解释为正式交付通过。

## Golden Principles

| 原则 | 适用性与设计裁决 | 验证证据 |
|---|---|---|
| 可证伪完成合同 | 适用。验收测试先提交，并因公开函数尚不存在而失败。 | seed 提交与失败测试。 |
| 生成方不得自签 | 适用。Builder、Validator 与最终 Review 分开执行。 | 最终 workspace 证据。 |
| 自治与可逆性对称 | 适用。实现只允许修改一个 Worker 源文件。 | seed 到实现的精确差异。 |
| 复用原生执行面 | 适用。继续使用 Python、pytest、wheel 和 Ruff。 | 本地与 GitHub 原生检查。 |
| 失败与恢复优先 | 适用。候选或提交不一致时停止，不复用旧结果。 | 候选身份与提交绑定。 |

## User Stories

### US-001: 取得全部重复非空任务

作为任务队列的使用者，我希望取得所有发生过重复的有效任务，从而无需在调用方重复实现清理和判断。

#### Acceptance Criteria

- [ ] `dogfood_worker` 公开新增
      `repeated_nonblank_jobs(jobs: Sequence[str]) -> list[str]`。
- [ ] 每个任务沿用现有规则：去除首尾空白，并忽略清理后为空的任务。
- [ ] 结果按每个任务第二次出现的顺序排列；
      `build, deploy, build, deploy, build, test` 返回 `build, deploy`，且 `build` 只出现一次。
- [ ] 空序列、全空白序列或没有重复有效任务时返回空列表。
- [ ] 函数接受可变列表和不可变序列，且不修改调用方输入。
- [ ] 现有 `next_job`、`next_nonblank_job`、`nonblank_jobs`、`unique_nonblank_jobs` 和
      `first_repeated_nonblank_job` 行为保持不变。
- [ ] 实现只修改 `packages/worker/src/dogfood_worker/__init__.py`；本规格和预置验收测试保持不变。
- [ ] API 与 Worker 两个包的 pytest、wheel 构建和 Ruff 检查全部通过。

## Verification

- 预置验收测试在 seed 提交上仅因缺少 `repeated_nonblank_jobs` 明确失败。
- 后续实现提交保持本规格和预置测试不变，并通过两个包的全部原生检查。
- 候选验证绑定精确候选包、当前提交和远端总闸；旧提交或旧结果不得复用。

## Rollback

若实现不符合验收标准，通过新提交修复或回退 Worker 实现；不得修改预置测试、质量契约或工作流来取得绿色结果。
