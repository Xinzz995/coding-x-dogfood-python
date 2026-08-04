---
title: "Python Worker 最后一个非空任务"
status: active
updated: 2026-08-04
scope: root
---

# Python Worker 最后一个非空任务

## Context

Python Monorepo 的 Worker 包已经能够取得第一个非空任务、列出全部非空任务并稳定去重，但还
不能直接取得队列中最后一个可执行任务。本任务用 coding-x 0.34.0 的全新固定候选验证这一
公开行为，同时保持两个 Python 包独立安装和 GitHub 原生门禁不变。

候选必须来自 coding-engine `main` 提交
`08d9539d1cca986a9ed2ff2b4f1498ac849988b3` 的 GitHub Actions 运行 `30914071363`，压缩包
SHA-256 为 `4a0a616e33a48a54f574c44a31d3d510fb380a247d90d2cfd1e459f02dcd8c54`。本轮固定绝对 CLI 为
`/private/tmp/coding-x-dogfood-0.34-r5.eDvI6T/python-install/node_modules/coding-x/dist/cli.js`，正式与 shadow
反例、Developer、Validator 和最终 Review 都不得换用其他入口。

## Goals

- 为 `dogfood_worker` 新增取得最后一个非空任务的公开函数。
- 复用现有非空任务清理语义，返回去除首尾空白后的任务文本。
- 保持输入序列和所有既有函数行为不变。
- 让候选完成 Developer、Validator 与最终三层 Review，并由 Python 原生 CI 复核。

## Non-Goals

- 不修改 API 包、质量契约、依赖或 GitHub 工作流。
- 不引入 Node、npm 或 coding-x 到 GitHub CI。
- 不引入持久化、并发、网络、重试或发布行为。
- Shadow 结果不作为正式交付凭证，不合并本 PR，也不触发 npm staging。

## Golden Principles

| 原则 | 适用性与设计裁决 | 验证证据 |
|---|---|---|
| 可证伪完成合同 | 适用。验收测试先提交并因缺少公开函数失败。 | seed 提交、候选实现提交、pytest。 |
| 生成方不得自签 | 适用。Developer 只实现，Validator 与三层 Review 独立判断。 | Validator receipt、三份 Review。 |
| 自治与可逆性对称 | 适用。只允许修改 Worker 实现，PR 保持开放。 | seed 到实现的文件差异。 |
| 复用原生执行面 | 适用。项目继续使用 Python、pytest、wheel 与 Ruff。 | 本地检查和 GitHub 三平台总闸。 |
| 失败与恢复优先 | 适用。候选、版本、提交或检查不一致时停止。 | Shadow 退出状态和远端检查。 |

## User Stories

### US-001: 取得最后一个非空任务

作为队列消费者，我希望取得清理后的最后一个非空任务，从而无需在调用方重复过滤和索引逻辑。

#### Acceptance Criteria

- [ ] `dogfood_worker` 公开新增 `last_nonblank_job(jobs: Sequence[str]) -> str | None`。
- [ ] 函数返回输入序列中最后一个非空任务，并去除该任务首尾空白。
- [ ] 空序列和全部为空白的序列返回 `None`。
- [ ] 函数接受可变列表与不可变序列，且不修改调用方输入。
- [ ] `next_job`、`next_nonblank_job`、`nonblank_jobs` 和 `unique_nonblank_jobs` 的现有行为保持不变。
- [ ] 候选实现只修改 `packages/worker/src/dogfood_worker/__init__.py`；预置验收测试从 seed 到实现保持不变。
- [ ] API 与 Worker 两个包的 pytest、wheel 构建和 Ruff 检查全部通过。

## Verification

- 预置验收测试在 seed 提交上因缺少 `last_nonblank_job` 明确失败。
- 同一候选 CLI 完成 workspace init、正式模式拒绝、Shadow doctor、Shadow apply-prd 和最终 run。
- GitHub Linux、macOS、Windows 检查与 `quality-gate` 针对最新提交全部通过。

## Rollback

若行为或证据不符合验收标准，回退候选生成的 Worker 实现提交；不得修改预置测试、质量契约、
工作流或候选身份来取得绿色结果。
