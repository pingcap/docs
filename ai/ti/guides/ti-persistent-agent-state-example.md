---
title: TiDB Cloud Filesystem を使用して使い捨てサンドボックス間でエージェントの状態を永続化する
summary: エージェントのサンドボックスを置き換える際に、TiDB Cloud Filesystem 内でプラン、チェックポイント、出力、ワークフロー履歴を保持します。
---

# TiDB Cloud Filesystem を使用して使い捨てサンドボックス間でエージェントの状態を永続化する

このワークフローでは、エージェントの計算環境を使い捨てのままにしつつ、プラン、中間結果、診断ファイル、ワークフロー履歴を TiDB Cloud Filesystem に保持します。置き換え用のサンドボックスは、ローカルディスクを保持するためだけに以前のサンドボックスを稼働させ続けることなく、タスクを再開できます。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 仕組み {#how-it-works}

信頼できるマシンが 1 つの Filesystem をプロビジョニングします。各サンドボックスには、Filesystem トークンとリージョンコードのみが渡されます。トークンは Filesystem を識別するため、エージェントは TiDB Cloud のコントロールプレーンキーを受け取ることなく、リモート名前空間に永続的なタスク状態を書き込み、ジャーナルにワークフロー遷移を記録できます。

## 前提条件 {#prerequisites}

- 信頼できるマシンに TiDB Cloud CLI をインストールして設定します。
- 各サンドボックスに TiDB Cloud CLI をインストールします。
- 信頼できるマシンに `jq` をインストールします。
- トークン転送には、安全なシークレットマネージャーまたは暗号化されたサンドボックス入力を使用します。

## ステップ 1. 状態保存用 Filesystem をプロビジョニングする {#step-1-provision-the-state-filesystem}

信頼できるマシンで、次を実行します。

```bash
umask 077
ti fs create-file-system --wait > ./filesystem.json
export FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"
```

`TI_FS_TOKEN` はシークレットマネージャーに保存し、クリーンアップ用に `FILE_SYSTEM_ID` を記録し、設定されたリージョンコードも記録します。これらの値を安全に保存した後、`filesystem.json` を削除します。

## ステップ 2. 最初のサンドボックスを起動する {#step-2-start-the-first-sandbox}

次の環境変数を注入します。

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

プランを書き込み、ワークフロージャーナルを作成します。

```bash
printf '%s\n' '# Plan' '1. inspect' '2. change' '3. verify' \
  | ti fs copy-file --from-stdin --to-remote /tasks/task-42/plan.md

ti fs-journal create-journal \
  --journal-id task-42 \
  --journal-kind agent \
  --title "task 42" \
  --actor agent:worker-1

ti fs-journal append-journal-entries \
  --journal-id task-42 \
  --entry-json '{"type":"task.checkpoint","step":"inspection-complete"}'
```

`agent` ジャーナル種別は、このジャーナルをエージェントワークフローとして分類します。また、`--journal-kind` を省略した場合のデフォルト値でもあります。別のワークフロー分類が必要な場合、このオプションにはカスタム文字列を指定できます。

## ステップ 3. 置き換え用サンドボックスで再開する {#step-3-resume-in-a-replacement-sandbox}

同じ 2 つの FS 変数を新しいサンドボックスに注入し、永続状態を復元します。

```bash
ti fs read-file --path /tasks/task-42/plan.md
ti fs-journal read-journal-entries --journal-id task-42 --after-seq 0
```

同じタスクパス配下に結果を書き続けます。並列エージェント同士が互いのファイルを上書きしないよう、一意のタスク ID を使用してください。

## クリーンアップ {#cleanup}

サンドボックスが Filesystem の使用を停止したら、信頼できるマシンからそれを削除します。

```bash
rm -f ./filesystem.json
ti fs delete-file-system --file-system-id "$FILE_SYSTEM_ID"
```

Filesystem を削除すると、そのタスクファイルとジャーナルも削除されます。

## セキュリティおよび運用上の注意 {#security-and-operational-notes}

- FS トークンは所有者資格情報です。実行時のシークレットストアに保持し、イメージやタスクプロンプトには含めないでください。
- 完了した直接データプレーン書き込みは、リモートから参照可能になります。マウントされた FUSE 書き込みについては、サンドボックスを削除する前に正常にアンマウントしてください。
- ジャーナルは順序付けられたワークフローの証跡を保持し、タスクファイルは変更可能な作業状態を保持します。状態と履歴の両方が必要な場合は、両方を使用してください。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud Filesystem Journal CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-journal.md)
- [TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md)