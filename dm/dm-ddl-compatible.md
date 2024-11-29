---
title: Special Handling of DM DDLs
summary: DM がステートメント タイプに応じて DDL ステートメントを解析および処理する方法を学習します。
---

# DM DDL の特別な処理 {#special-handling-of-dm-ddls}

TiDB データ移行 (DM) はデータを移行するときに、DDL ステートメントを解析し、ステートメントの種類と現在の移行段階に応じて処理します。

## DDL文をスキップする {#skip-ddl-statements}

次のステートメントは DM ではサポートされていないため、DM は解析後すぐにスキップします。

<table><tr><th>説明</th><th>構文</th></tr><tr><td>取引</td><td><code>^SAVEPOINT</code></td></tr><tr><td>すべてのフラッシュSQLをスキップする</td><td><code>^FLUSH</code></td></tr><tr><td rowspan="3">テーブルメンテナンス</td><td><code>^OPTIMIZE\\s+TABLE</code></td></tr><tr><td> <code>^ANALYZE\\s+TABLE</code></td></tr><tr><td> <code>^REPAIR\\s+TABLE</code></td></tr><tr><td>一時テーブル</td><td><code>^DROP\\s+(\\/\\*\\!40005\\s+)?TEMPORARY\\s+(\\*\\/\\s+)?TABLE</code></td></tr><tr><td rowspan="2">トリガー</td><td><code>^CREATE\\s+(DEFINER\\s?=.+?)?TRIGGER</code></td></tr><tr><td> <code>^DROP\\s+TRIGGER</code></td></tr><tr><td rowspan="3">手順</td><td><code>^DROP\\s+PROCEDURE</code></td></tr><tr><td> <code>^CREATE\\s+(DEFINER\\s?=.+?)?PROCEDURE</code></td></tr><tr><td> <code>^ALTER\\s+PROCEDURE</code></td></tr><tr><td rowspan="3">ビュー</td><td><code>^CREATE\\s*(OR REPLACE)?\\s+(ALGORITHM\\s?=.+?)?(DEFINER\\s?=.+?)?\\s+(SQL SECURITY DEFINER)?VIEW</code></td></tr><tr><td> <code>^DROP\\s+VIEW</code></td></tr><tr><td> <code>^ALTER\\s+(ALGORITHM\\s?=.+?)?(DEFINER\\s?=.+?)?(SQL SECURITY DEFINER)?VIEW</code></td></tr><tr><td rowspan="4">関数</td><td><code>^CREATE\\s+(AGGREGATE)?\\s*?FUNCTION</code></td></tr><tr><td> <code>^CREATE\\s+(DEFINER\\s?=.+?)?FUNCTION</code></td></tr><tr><td> <code>^ALTER\\s+FUNCTION</code></td></tr><tr><td> <code>^DROP\\s+FUNCTION</code></td></tr><tr><td rowspan="3">テーブルスペース</td><td><code>^CREATE\\s+TABLESPACE</code></td></tr><tr><td> <code>^ALTER\\s+TABLESPACE</code></td></tr><tr><td> <code>^DROP\\s+TABLESPACE</code></td></tr><tr><td rowspan="3">イベント</td><td><code>^CREATE\\s+(DEFINER\\s?=.+?)?EVENT</code></td></tr><tr><td> <code>^ALTER\\s+(DEFINER\\s?=.+?)?EVENT</code></td></tr><tr><td> <code>^DROP\\s+EVENT</code></td></tr><tr><td rowspan="7">アカウント管理</td><td><code>^GRANT</code></td></tr><tr><td> <code>^REVOKE</code></td></tr><tr><td> <code>^CREATE\\s+USER</code></td></tr><tr><td> <code>^ALTER\\s+USER</code></td></tr><tr><td> <code>^RENAME\\s+USER</code></td></tr><tr><td> <code>^DROP\\s+USER</code></td></tr><tr><td> <code>^DROP\\s+USER</code></td></tr></table>

## DDL文を書き換える {#rewrite-ddl-statements}

次のステートメントは、ダウンストリームに複製される前に書き換えられます。

| 元の声明                  | 書き直された声明                           |
| --------------------- | ---------------------------------- |
| `^CREATE DATABASE...` | `^CREATE DATABASE...IF NOT EXISTS` |
| `^CREATE TABLE...`    | `^CREATE TABLE..IF NOT EXISTS`     |
| `^DROP DATABASE...`   | `^DROP DATABASE...IF EXISTS`       |
| `^DROP TABLE...`      | `^DROP TABLE...IF EXISTS`          |
| `^DROP INDEX...`      | `^DROP INDEX...IF EXISTS`          |

## シャードマージ移行タスク {#shard-merge-migration-tasks}

DM が悲観的モードまたは楽観的モードでテーブルをマージおよび移行する場合、DDL レプリケーションの動作は他のシナリオとは異なります。詳細については、 [悲観モード](/dm/feature-shard-merge-pessimistic.md)および[楽観モード](/dm/feature-shard-merge-optimistic.md)を参照してください。

## オンラインDDL {#online-ddl}

オンライン DDL 機能では、DDL イベントも特別な方法で処理されます。詳細については、 [GH-ost/PT-osc を使用するデータベースからの移行](/dm/feature-online-ddl.md)を参照してください。
