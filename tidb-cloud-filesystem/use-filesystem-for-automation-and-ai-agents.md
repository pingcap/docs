---
title: Explore Automation and AI Agent Workflows
summary: Find TiDB for AI examples for sharing file system workspaces, handing off CI artifacts, and supporting agents with data, Git, journals, and secrets.
---

# Explore Automation and AI Agent Workflows

TiDB Cloud Filesystem keeps files available when a machine, CI job, or agent sandbox is temporary. Choose a workflow below based on what you need to share or preserve.

If you are new to TiDB Cloud Filesystem, start with the [Quick Start](/tidb-cloud-filesystem/filesystem-quick-start.md) to create a file system and work with your first file.

To share work across machines and CI jobs, see the following guides in the [TiDB for AI](https://docs.pingcap.com/ai/) documentation.

| What you want to do | Guide |
| --- | --- |
| Pass build artifacts between isolated CI jobs | [Hand Off CI Artifacts Between Isolated Jobs with TiDB Cloud Filesystem](/ai/ti/guides/ti-ci-artifact-handoff-example.md) |

To support AI agent workflows, see the following guides in the [TiDB for AI](https://docs.pingcap.com/ai/) documentation. If you are evaluating TiDB Cloud Filesystem for agents, start with the sandbox example before moving to longer-running or parallel workflows.

| What you want to do | Guide |
| --- | --- |
| Give an agent sandbox access to a shared workspace | [Use TiDB Cloud Filesystem in an Agent Sandbox](/ai/ti/guides/ti-agent-sandbox-example.md) |
| Keep agent state across disposable sandboxes | [Persist Agent State Across Disposable Sandboxes with TiDB Cloud Filesystem](/ai/ti/guides/ti-persistent-agent-state-example.md) |
| Share a read-only dataset with parallel agents | [Share a Read-Only Dataset Across Parallel Agents with TiDB Cloud Filesystem](/ai/ti/guides/ti-parallel-agent-dataset-example.md) |
| Prepare a large Git workspace for an agent | [Prepare a Git Workspace for Agents on TiDB Cloud Filesystem](/ai/ti/guides/ti-git-workspace-for-agents-example.md) |
| Record and verify an agent workflow | [Record an Agent Workflow in a File System Journal](/ai/ti/guides/ti-journal-agent-workflow-example.md) |
| Give an agent limited access to a Vault secret | [Delegate File System Vault Secrets to an Agent](/ai/ti/guides/ti-vault-agent-secrets-example.md) |
