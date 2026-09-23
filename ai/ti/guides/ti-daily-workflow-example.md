---
title: 日次の TiDB Cloud CLI ワークフローを実行する
summary: リソースを確認し、TiDB Cloud Starter インスタンスと file system を管理し、TiDB Cloud CLI の更新を確認して、リソースをクリーンアップします。
---

# 日次の TiDB Cloud CLI ワークフローを実行する

この例では、TiDB Cloud Starter と TiDB Cloud Filesystem にまたがる、一般的なオペレーターのワークフローを示します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 前提条件 {#prerequisites}

- `ti` をインストールし、`ti configure` を実行します。
- 組織に、1 つの TiDB Cloud Starter インスタンスと 1 つの file system を作成できる容量があることを確認します。

## ステップ 1. 現在のリソースを確認する {#step-1-inspect-current-resources}

```bash
ti db list-db-clusters --db-cluster-type starter --output text
ti fs list-file-systems --output text
```

## ステップ 2. TiDB Cloud Starter インスタンスを作成する {#step-2-create-a-tidb-cloud-starter-instance}

```bash
ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name daily-demo \
  --dry-run

export DB_CLUSTER_ID="$(ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name daily-demo \
  --wait \
  --query id \
  --output text)"
```

このコマンドは、返されたクラスター ID を `DB_CLUSTER_ID` に保存します。`--wait` が設定されているため、作成コマンドはクラスターがアクティブになった後に戻ります。後で再度確認することもできます。

```bash
ti db describe-db-cluster \
  --db-cluster-id "$DB_CLUSTER_ID" \
  --output text
```

## ステップ 3. SQL アクセスを確認する {#step-3-verify-sql-access}

```bash
ti db create-db-sql-users --db-cluster-id "$DB_CLUSTER_ID"
ti db execute-sql-statement \
  --db-cluster-id "$DB_CLUSTER_ID" \
  --read-only \
  --sql "SELECT CURRENT_TIMESTAMP AS checked_at" \
  --output text
```

## ステップ 4. file system を作成して使用する {#step-4-create-and-use-a-filesystem}

```bash
export TI_FS_FILE_SYSTEM_ID="$(ti fs create-file-system \
  --wait \
  --query file_system_id \
  --output text)"

printf 'daily workflow\n' | ti fs copy-file \
  --from-stdin \
  --to-remote /notes/today.txt

ti fs list-files \
  --path /notes \
  --output text
```

`/notes/today.txt` 内のファイルにより、明示的に選択したリソースが使用可能であることを確認できます。

## ステップ 5. 更新を確認する {#step-5-check-for-updates}

インストール済みバージョンを変更せずに、新しいバージョンが利用可能かどうかを確認します。

```bash
ti update --check
```

更新をプレビューします。

```bash
ti update --dry-run
```

別のワークフローでアクティブな file system または Vault マウントがある場合は、更新を適用する前にライターを停止してアンマウントしてください。これにより、`ti` と file system ランタイムが一緒に更新されます。手順については、[TiDB Cloud CLI を更新する](/ai/ti/reference/ti-install-configure-update.md#update-tidb-cloud-cli) を参照してください。

適切なタイミングで更新を適用します。

```bash
ti update
```

## クリーンアップ {#cleanup}

```bash
ti fs delete-file-system \
  --file-system-id "$TI_FS_FILE_SYSTEM_ID"

ti db delete-db-cluster \
  --db-cluster-id "$DB_CLUSTER_ID"
```

> **Note:**
>
> ローカルの TiDB Cloud CLI 設定を削除しても、リモートリソースは削除されません。

## セキュリティに関する注意 {#security-notes}

- file system トークンや整形済みのデータベース接続文字列を出力しないでください。
- 一意の自動化プレフィックスを使用し、その実行で作成されたリソースのみを削除してください。
- 破壊的な操作は `--dry-run` で事前確認してください。

## 次のステップ {#what-s-next}

- [TiDB Cloud Starter CLI コマンドリファレンス](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)