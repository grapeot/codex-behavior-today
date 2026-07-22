# RFC

## Measurement Contract

一个 measurement identity 由模型名、transport、probe battery 版本和 request protocol 版本组成。首版固定为 `gpt-5.6-sol`、ChatGPT/Codex subscription compatibility transport、`v1` battery 与 `v1` protocol。

统计对象是 endpoint 的条件输出分布，不是模型权重。请求参数无法由 subscription compatibility transport 可靠控制时，页面必须将结果表述为该 transport 下的观察。

## Data Flow

本机 sampler 逐个请求目标 cell，记录原始回答到 ignored SQLite。随后生成公开 aggregate JSON：计数、无效回答数、latency summary 与 distribution metrics。静态页面只读取公开 aggregate JSON。

## Metrics

每个 cell 比较 canonical answer count distribution 的 Jensen-Shannon divergence。日环比用于展示；总体 drift 以今日对前 14 个有效日聚合分布的 JSD 衡量。只有至少 14 个历史日且总体 drift 超过历史相邻日 JSD 的 99th percentile，页面才显示 `notable shift`。

## Deployment

`master` 是唯一主分支，受 branch protection 保护。GitHub Actions 从 `master` 上传 committed `site/` 目录并部署 GitHub Pages。Actions 不拥有 OAuth credential，也不发起 API 请求。

日更在本机生成 data/site 后，创建一个 date-scoped branch、push、开 PR 并 merge。这样公开 Git 历史保留每日数据变更的 PR 审计轨迹，同时 scheduler 不需要也不能直接写入保护分支。
