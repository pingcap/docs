---
title: 探索自动化与 AI Agent 工作流
summary: 查找 TiDB for AI 示例，了解如何共享文件系统工作区、交接 CI 制品，以及使用数据、Git、日志（Journal）和 Secret 为 agent 提供支持。
---

# 探索自动化与 AI Agent 工作流

当机器、CI 作业或 agent 沙箱是临时性的时，TiDB Cloud Filesystem 可以让文件保持可用。根据你需要共享或保留的内容，选择下面的工作流。

如果你刚开始使用 TiDB Cloud Filesystem，请先阅读[快速开始](/tidb-cloud-filesystem/filesystem-quick-start.md)，创建一个文件系统并操作你的第一个文件。

如需在多台机器和 CI 作业之间共享工作，请参阅 [TiDB for AI](https://docs.pingcap.com/ai/) 文档中的以下指南。

| 你想要做什么 | 指南 |
| --- | --- |
| 在隔离的 CI 作业之间传递构建制品 | [使用 TiDB Cloud Filesystem 在隔离作业之间交接 CI 制品](/ai/ti/guides/ti-ci-artifact-handoff-example.md) |

如需支持 AI agent 工作流，请参阅 [TiDB for AI](https://docs.pingcap.com/ai/) 文档中的以下指南。如果你正在评估 TiDB Cloud Filesystem 是否适用于 agent，建议先从沙箱示例开始，再过渡到运行时间更长或并行的工作流。

| 你想要做什么 | 指南 |
| --- | --- |
| 让 agent 沙箱能够访问共享工作区 | [在 Agent 沙箱中使用 TiDB Cloud Filesystem](/ai/ti/guides/ti-agent-sandbox-example.md) |
| 在一次性沙箱之间保留 agent 状态 | [使用 TiDB Cloud Filesystem 在一次性沙箱之间持久化 Agent 状态](/ai/ti/guides/ti-persistent-agent-state-example.md) |
| 在并行 agent 之间共享只读数据集 | [使用 TiDB Cloud Filesystem 在并行 Agent 之间共享只读数据集](/ai/ti/guides/ti-parallel-agent-dataset-example.md) |
| 为 agent 准备大型 Git 工作区 | [在 TiDB Cloud Filesystem 上为 Agent 准备 Git 工作区](/ai/ti/guides/ti-git-workspace-for-agents-example.md) |
| 记录并验证 agent 工作流 | [在文件系统日志（Journal）中记录 Agent 工作流](/ai/ti/guides/ti-journal-agent-workflow-example.md) |
| 为 agent 提供对 Vault Secret 的受限访问 | [将文件系统 Vault Secret 委派给 Agent](/ai/ti/guides/ti-vault-agent-secrets-example.md) |