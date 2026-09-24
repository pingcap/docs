---
title: エージェントサンドボックスで TiDB Cloud Filesystem を使う
summary: 信頼できるマシン上で file system をプロビジョニングし、TiDB Cloud API キーを使わずに、クリーンなエージェントサンドボックスへ設定不要でアクセスを提供します。
---

# エージェントサンドボックスで TiDB Cloud Filesystem を使う

このワークフローでは、ユーザーの TiDB Cloud CLI 設定全体をサンドボックスにコピーすることなく、一時的なコーディングエージェントに対して永続的で共有可能なワークスペースを提供できます。サンドボックスのローカルディスクが使い捨てであっても、エージェントが成果物、リポジトリの状態、または以前のセッションや他のワーカーからのファイルを必要とし、サンドボックスごとにその状態を毎回再構築したくない場合に使用します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは予告なく変更される場合があります。

> **Note:**
>
> このワークフローを実際に試せる版として、[TiDB Cloud Filesystem for Agent Sandbox Lab](https://labs.tidb.io/labs/demo_901) を開いてください。このインタラクティブな演習では、エージェントサンドボックスで永続的な file system を使用する方法を案内します。

## 仕組み {#how-it-works}

信頼できるマシンが一度だけ file system をプロビジョニングします。サンドボックスには file system のオーナートークンとリージョンコードだけが渡されるため、`ti configure`、コピーした `~/.ti/` ディレクトリ、または TiDB Cloud API キーなしで、通常のファイル操作やデータプレーン、マウント、Git、ジャーナル、vault のワークフローを利用できます。これにより、汎用オブジェクトストレージ API で必要となるアプリケーション固有のアップロードおよびダウンロードロジックも不要になります。このトークンは file system を識別します。エージェントが一部のシークレットだけを必要とする場合は、オーナートークンの代わりに委任された vault トークンを使用してください。

## 前提条件 {#prerequisites}

- 信頼できるマシンに TiDB Cloud CLI をインストールして設定します。
- リリースインストーラーを使用して、サンドボックスに TiDB Cloud CLI をインストールします。
- 信頼できるマシンに `jq` をインストールします。
- トークンの受け渡しには、安全なシークレットマネージャーまたは暗号化されたサンドボックス入力を使用します。

## ステップ 1. 信頼できるマシンでプロビジョニングする {#step-1-provision-on-the-trusted-machine}

```bash
umask 077
ti fs create-file-system --wait > ./filesystem.json
export FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"
```

トークンをシークレットマネージャーに保存し、コントロールプレーンのクリーンアップ用に `FILE_SYSTEM_ID` を記録し、file system の作成に使用したリージョンコードも記録します。トークンを安全に保存した後、`filesystem.json` を削除してください。

## ステップ 2. サンドボックスに最小限の環境を注入する {#step-2-inject-the-minimum-sandbox-environment}

次の内容で、サンドボックスのシークレットまたは環境変数の仕組みを設定します。

```bash
TI_FS_TOKEN=<owner-token>
TI_REGION_CODE=<filesystem-region-code>
```

サンドボックスには `TIDB_CLOUD_PUBLIC_KEY`、`TIDB_CLOUD_PRIVATE_KEY`、`ti configure`、または `~/.ti/` からコピーしたファイルは不要です。

## ステップ 3. 直接アクセスを確認する {#step-3-verify-direct-access}

サンドボックス内で次を実行します。

```bash
printf 'sandbox ready\n' | ti fs copy-file \
  --from-stdin \
  --to-remote /sandbox/status.txt

ti fs read-file --path /sandbox/status.txt
```

期待される出力:

```text
sandbox ready
```

## ステップ 4. 必要に応じて Filesystem をマウントする {#step-4-optionally-mount-the-file-system}

Linux で FUSE を使用する場合:

```bash
mkdir -p "$HOME/workspace"
ti fs mount-file-system \
  --mount-path "$HOME/workspace" \
  --driver fuse

cat "$HOME/workspace/sandbox/status.txt"
```

macOS では、FUSE のインストールが不要な WebDAV を使用するため、`--driver fuse` を省略します。Git ワークスペース、レイヤー、online drain などの FUSE 固有の機能が必要な場合は、macFUSE をインストールして FUSE を選択してください。プラットフォーム要件とマウントパスの制限については、[File System をマウントする](/tidb-cloud-filesystem/filesystem-mount.md) を参照してください。

マウント後は、同じ FS 環境で `ti fs-git`、`ti fs-journal`、およびオーナーに認可された `ti fs-vault` コマンドを使用できます。エージェントが一部のシークレットフィールドだけを必要とする場合は、オーナートークンの代わりに委任された `TI_VAULT_TOKEN` を渡してください。

## クリーンアップ {#cleanup}

ライターを停止してアンマウントします。正常な FUSE アンマウントでは、保留中の作業が自動的にフラッシュおよび drain されます。

```bash
ti fs unmount-file-system --mount-path "$HOME/workspace"
```

FUSE マウントでは、マウントを維持したままリモートへの永続化を確認したい場合、`ti fs drain-file-system --mount-path "$HOME/workspace"` を別途使用します。`drain-file-system` は WebDAV ではサポートされていません。詳細は [安全に終了する](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely) を参照してください。信頼できるマシンに戻って、次を実行します。

```bash
ti fs delete-file-system \
  --file-system-id "$FILE_SYSTEM_ID"
```

## セキュリティと運用上の注意 {#security-and-operational-notes}

- `TI_FS_TOKEN` はオーナー認証情報として扱ってください。
- イメージ、リポジトリ、コマンドフラグ、または操作ログに配置しないでください。
- サンドボックスを削除しても、リモートの file system は削除されません。
- 正常なアンマウントでは保留中の FUSE 書き込みが drain されますが、アンマウントせずにサンドボックスを削除しても drain されません。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md)
