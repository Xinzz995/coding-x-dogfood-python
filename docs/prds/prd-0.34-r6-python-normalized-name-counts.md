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
coding-x 0.34.0 的 R6 固定候选新增这一公开行为，同时保持两个 Python 包独立安装和 GitHub
原生门禁不变。

候选必须来自 coding-engine `main` 提交
`2f099f0bf0675c39c63dc781495aa61f2a472ba3` 的 GitHub Actions 运行 `30941731201`，压缩包
SHA-256 为 `214784c4a62958a34644ccf2daa75c4133925ee23e54df1ce50d7e10833e87cd`。本轮固定绝对 CLI 为
`/private/tmp/coding-x-python-r6.8Hq2OY/candidate-install/node_modules/coding-x/dist/cli.js`；正式模式
拒绝、Shadow doctor、Shadow apply-prd、Developer、Validator 和最终 Review 都不得切换入口。

## Goals

- 为 `dogfood_api` 新增统计规范化名称出现次数的公开函数。
- 复用现有名称规范化语义，并保留首次出现顺序。
- 保持调用方输入和所有既有公开函数行为不变。
- 让候选完整经过 Developer、Validator、本地三层 Review 和 Python 原生 CI。

## Non-Goals

- 不修改 Worker 包、质量契约、依赖或 GitHub 工作流。
- 不引入持久化、并发、网络、重试或发布行为。
- 不在 GitHub CI 安装 Node、npm、coding-x，也不在 GitHub 调用模型。
- 不复用 R5 PR #16 的分支、workspace、报告或本地 Review。
- Shadow 结果不作为正式交付凭证；本 PR 不合并，也不触发 npm staging。

## Golden Principles

| 原则 | 适用性与设计裁决 | 验证证据 |
|---|---|---|
| 可证伪完成合同 | 适用。验收测试先提交，并因公开函数尚不存在而失败。 | seed 提交、失败测试、候选实现提交。 |
| 生成方不得自签 | 适用。Developer 只实现，Validator 和三层 Review 独立判断。 | Validator receipt、三份 Review。 |
| 自治与可逆性对称 | 适用。实现只允许修改 API 实现文件，PR 保持开放。 | seed 到实现的文件差异。 |
| 复用原生执行面 | 适用。项目继续使用 Python、pytest、wheel 与 Ruff。 | 本地检查和 GitHub 三平台总闸。 |
| 失败与恢复优先 | 适用。候选、版本、提交或检查不一致时停止。 | 正式拒绝、Shadow 退出状态和远端检查。 |

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
- 同一候选绝对 CLI 完成 workspace 初始化、正式模式拒绝、Shadow doctor、Shadow apply-prd、
  Developer、Validator 和最终三层 Review；三个 Shadow 命令均退出 7。
- 核对 `progress.md` 只在既有前缀后追加，并确认所有候选身份均为 R6、没有回落到 R5。
- GitHub Linux、macOS、Windows 检查与 `quality-gate` 针对最终提交全部通过。

## Rollback

若行为或证据不符合验收标准，回退候选生成的 API 实现提交；不得修改预置测试、质量契约、
工作流或候选身份来取得绿色结果。
