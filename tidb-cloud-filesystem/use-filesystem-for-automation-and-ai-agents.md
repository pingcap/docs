---
title: 自動化と AI エージェントのワークフローを探る
summary: ファイルシステムのワークスペース共有、CI アーティファクトの受け渡し、データ、Git、ジャーナル、シークレットによるエージェント支援のための TiDB for AI の例を紹介します。
---

# 自動化と AI エージェントのワークフローを探る

TiDB Cloud Filesystem は、マシン、CI ジョブ、またはエージェントのサンドボックスが一時的な環境であっても、ファイルを利用可能な状態に保ちます。共有または保持したい内容に応じて、以下のワークフローを選択してください。

TiDB Cloud Filesystem を初めて使用する場合は、まず [クイックスタート](/tidb-cloud-filesystem/filesystem-quick-start.md) を参照して、ファイルシステムを作成し、最初のファイルを操作してください。

マシン間および CI ジョブ間で作業を共有するには、[TiDB for AI](https://docs.pingcap.com/ai/) ドキュメントの以下のガイドを参照してください。

| 実行したいこと | ガイド |
| --- | --- |
| 分離された CI ジョブ間でビルドアーティファクトを受け渡す | [TiDB Cloud Filesystem を使用して分離されたジョブ間で CI アーティファクトを受け渡す](/ai/ti/guides/ti-ci-artifact-handoff-example.md) |

AI エージェントのワークフローを支援するには、[TiDB for AI](https://docs.pingcap.com/ai/) ドキュメントの以下のガイドを参照してください。エージェント向けに TiDB Cloud Filesystem を評価している場合は、より長時間実行されるワークフローや並列ワークフローに進む前に、まずサンドボックスの例から始めてください。

| 実行したいこと | ガイド |
| --- | --- |
| エージェントのサンドボックスに共有ワークスペースへのアクセスを提供する | [エージェントサンドボックスで TiDB Cloud Filesystem を使う](/ai/ti/guides/ti-agent-sandbox-example.md) |
| 使い捨てサンドボックス間でエージェントの状態を保持する | [TiDB Cloud Filesystem を使用して使い捨てサンドボックス間でエージェントの状態を永続化する](/ai/ti/guides/ti-persistent-agent-state-example.md) |
| 並列エージェント間で読み取り専用データセットを共有する | [TiDB Cloud Filesystem を使用して並列エージェント間で読み取り専用データセットを共有する](/ai/ti/guides/ti-parallel-agent-dataset-example.md) |
| エージェント用の大規模な Git ワークスペースを準備する | [TiDB Cloud Filesystem 上でエージェント向けの Git ワークスペースを準備する](/ai/ti/guides/ti-git-workspace-for-agents-example.md) |
| エージェントのワークフローを記録して検証する | [ファイルシステムジャーナルにエージェントワークフローを記録する](/ai/ti/guides/ti-journal-agent-workflow-example.md) |
| エージェントに Vault シークレットへの限定的なアクセスを提供する | [エージェントにファイルシステム Vault シークレットを委任する](/ai/ti/guides/ti-vault-agent-secrets-example.md) |