---
title: Worker
summary: cloud control が有効なデプロイ向けの Worker 関連 SQL コマンド。
---

# Worker

cloud control が有効なデプロイ向けの Worker 関連 SQL コマンドです。

> **Note:**
>
> Worker 管理コマンドには cloud control が必要です。`cloud_control_grpc_server_address` が設定されていない場合、これらのコマンドを実行すると {{{ .lake }}} は `CloudControlNotEnabled` エラーを返します。

## サポートされるステートメント {#supported-statements}

| 文 | 目的 |
|-----------|---------|
| `CREATE WORKER` | オプションのキーと値のオプションリストを指定して worker を作成します |
| `ALTER WORKER` | worker のタグまたはオプションを更新するか、worker の状態を変更します |
| `DROP WORKER` | worker を削除します |
| `SHOW WORKERS` | 現在のテナント内の worker を一覧表示します |

## コマンドリファレンス {#command-reference}

| コマンド | 説明 |
|---------|-------------|
| [CREATE WORKER](/tidb-cloud-lake/sql/create-worker.md) | worker 定義を作成します |
| [ALTER WORKER](/tidb-cloud-lake/sql/alter-worker.md) | worker のタグ、オプション、または状態を変更します |
| [DROP WORKER](/tidb-cloud-lake/sql/drop-worker.md) | worker 定義を削除します |
| [SHOW WORKERS](/tidb-cloud-lake/sql/show-workers.md) | worker とそのメタデータを一覧表示します |
| [Examples](/tidb-cloud-lake/sql/worker-examples.md) | 検証済みの worker SQL の例を示します |

## 注意事項 {#notes}

- オプション名では大文字と小文字は区別されません。{{{ .lake }}} はプランニング時にそれらを小文字に正規化します。
- `SHOW WORKERS` は `name`、`tags`、`options`、`created_at`、`updated_at` の各カラムを返します。
- `ALTER WORKER` は `SET TAG`、`UNSET TAG`、`SET`、`UNSET`、`SUSPEND`、`RESUME` をサポートします。
- `CREATE WORKER` は `TAG` 句をサポートしません。