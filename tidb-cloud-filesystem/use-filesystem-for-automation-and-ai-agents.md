---
title: Use TiDB Cloud Filesystem for Automation and AI Agents
summary: Learn how to use TiDB Cloud Filesystem to share workspaces, hand off CI artifacts, and support agent work with data, Git, journals, and secrets.
---

# Use TiDB Cloud Filesystem for Automation and AI Agents

TiDB Cloud Filesystem keeps files available when a machine, CI job, or agent sandbox is temporary. Choose a workflow below based on what you need to share or preserve. These examples use the TiDB Cloud CLI and open in the TiDB for AI documentation section.

If you are new to Filesystem, start with the [Quick Start](/tidb-cloud-filesystem/filesystem-quick-start.md) to create a Filesystem and work with your first file.

To share work across machines and CI jobs, see the following guides in the TiDB for AI documentation.

| Guide | What you can do |
| --- | --- |
| [Share a TiDB Cloud Filesystem Across Machines](/ai/ti/guides/ti-share-filesystem-across-machines-example.md) | Give users or automation on separate machines access to the same workspace without exchanging file copies. |
| [Hand Off CI Artifacts Between Isolated Jobs with TiDB Cloud Filesystem](/ai/ti/guides/ti-ci-artifact-handoff-example.md) | Keep build output in a Filesystem so a later CI job can retrieve it without copying a CLI profile. |

To support AI agent workflows, see the following guides in the TiDB for AI documentation.

| Guide | What you can do |
| --- | --- |
| [Use TiDB Cloud Filesystem in an Agent Sandbox](/ai/ti/guides/ti-agent-sandbox-example.md) | Give an ephemeral agent a shared workspace without exposing TiDB Cloud API keys to its sandbox. |
| [Persist Agent State Across Disposable Sandboxes with TiDB Cloud Filesystem](/ai/ti/guides/ti-persistent-agent-state-example.md) | Keep plans, results, and workflow history available after replacing a sandbox. |
| [Share a Read-Only Dataset Across Parallel Agents with TiDB Cloud Filesystem](/ai/ti/guides/ti-parallel-agent-dataset-example.md) | Let multiple agents use the same dataset without downloading a separate copy for each worker. |
| [Prepare a Git Workspace for Agents on TiDB Cloud Filesystem](/ai/ti/guides/ti-git-workspace-for-agents-example.md) | Make a large repository available to an agent while its clean Git data hydrates in the background. |
| [Record an Agent Workflow in a TiDB Cloud Filesystem Journal](/ai/ti/guides/ti-journal-agent-workflow-example.md) | Record and verify an ordered history of agent actions and handoffs. |
| [Delegate TiDB Cloud Filesystem Vault Secrets to an Agent](/ai/ti/guides/ti-vault-agent-secrets-example.md) | Give an agent limited access to a secret field without sharing the Filesystem owner token. |
