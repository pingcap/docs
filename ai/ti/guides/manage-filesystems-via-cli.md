---
title: TiDB Cloud Filesystem を管理する
summary: "`ti fs` を使用してファイルシステムを作成し、ファイルの書き込みと読み取りを行う方法、およびその他のファイルシステムタスク向けガイドについて説明します。"
---

# TiDB Cloud Filesystem を管理する

TiDB Cloud CLI (`ti`) を使用すると、TiDB Cloud Filesystem 内のファイルシステムリソースを作成および管理し、ターミナルや自動化ワークフローからそのファイルを操作できます。

## ファイルシステムを作成して使用する {#create-and-use-a-file-system}

開始する前に、組織内でファイルシステムを作成できる API キーを使用して、[TiDB Cloud CLI をインストールして設定](/ai/ti/reference/ti-install-configure-update.md)してください。`ti configure` を実行するときは、サポートされているファイルシステムのリージョンを選択します。

ファイルシステムを作成し、準備完了になるまで待機します。

```shell
ti fs create-file-system --display-name my-workspace --wait
```

返された `file_system_id` をコピーし、以降のコマンド内の `<file-system-id>` を置き換えてください。CLI はファイルシステムトークンをローカルに保存します。返された `fs_token`（ファイルシステムトークン）はシークレットとして扱い、コマンド出力を公開しないでください。

```shell
echo "Hello from my workspace" | ti fs copy-file --file-system-id "<file-system-id>" --from-stdin --to-remote /hello.txt
ti fs read-file --file-system-id "<file-system-id>" --path /hello.txt
```

読み取り結果として `Hello from my workspace` が返されます。サポートされているリージョン、詳細なセットアップ手順、およびクリーンアップ手順については、[TiDB Cloud Filesystem を使い始める](/tidb-cloud-filesystem/filesystem-quick-start.md)を参照してください。

## その他のファイルシステムタスク {#more-file-system-tasks}

ファイルシステムを作成した後は、以下のガイドを参照して各種ファイルシステムタスクを実行してください。

| 実行したいこと | ガイド |
| --- | --- |
| 別のマシン、CI ジョブ、またはエージェント環境から既存のファイルシステムにアクセスする | [既存のファイルシステムにアクセスする](/tidb-cloud-filesystem/access-filesystem.md) |
| ファイルやディレクトリのアップロード、ダウンロード、読み取り、整理、確認、検索を行う | [ファイルとディレクトリを操作する](/tidb-cloud-filesystem/work-with-filesystem-data.md) |
| アクセストークンの生成、インポート、スコープ設定、確認、無効化、更新、取り消しを行う | [ファイルシステムトークンを管理する](/tidb-cloud-filesystem/manage-filesystem-tokens.md) |
| ファイルシステム内のファイルを別のユーザー、マシン、CI ジョブ、またはエージェントと共有する | [ファイルシステムを共有する](/tidb-cloud-filesystem/filesystem-sharing.md) |
| ローカルファイルパスを通じてファイルシステム内のファイルにアクセスする | [ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md) |
| レイヤーとチェックポイントを使用して変更を分離する | [ファイルシステムのレイヤーとチェックポイントを管理する](/tidb-cloud-filesystem/manage-filesystem-layers.md) |
| マウントされたファイルシステム上で Git リポジトリを操作する | [Git ワークスペースを管理する](/tidb-cloud-filesystem/manage-git-workspaces.md) |
| 順序付けられたワークフローイベントを記録および検証する | [ファイルシステムでジャーナルを使用する](/tidb-cloud-filesystem/use-filesystem-journals.md) |
| シークレットの保存、委任、注入、監査、取り消しを行う | [ファイルシステムの Vault シークレットを管理する](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md) |
| メディア抽出またはセマンティック検索のために AI プロバイダーを設定する | [ファイルシステムの AI プロバイダーを設定する](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md) |

構文、フラグ、および出力フィールドについては、[`ti fs` コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)を参照してください。
