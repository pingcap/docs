---
title: DM-worker Introduction
summary: Learn the features of DM-worker.
---

# DMワーカーの紹介 {#dm-worker-introduction}

DM-worker は、MySQL/MariaDB から TiDB にデータを移行するために使用されるツールです。

次の機能があります。

-   MySQL または MariaDB インスタンスのセカンダリ データベースとして機能
-   MySQL/MariaDB からbinlogイベントを読み取り、ローカルstorageに永続化します。
-   単一の DM-worker は、1 つの MySQL/MariaDB インスタンスのデータを複数の TiDB インスタンスに移行することをサポートします
-   複数の DM-worker は、複数の MySQL/MariaDB インスタンスのデータを 1 つの TiDB インスタンスに移行することをサポートします

## DMワーカー処理ユニット {#dm-worker-processing-unit}

DM ワーカー タスクには、リレー ログ、ダンプ処理ユニット、ロード処理ユニット、 binlogレプリケーションなど、複数の論理ユニットが含まれています。

### 中継ログ {#relay-log}

リレー ログは、アップストリームの MySQL/MariaDB からのbinlogデータを永続的に保存し、 binlogレプリケーションのためにbinlogイベントにアクセスする機能を提供します。

その理論的根拠と機能は、MySQL のリレー ログに似ています。詳細については、 [MySQL リレー ログ](https://dev.mysql.com/doc/refman/5.7/en/replica-logs-relaylog.html)を参照してください。

### ダンプ処理単位 {#dump-processing-unit}

ダンプ処理ユニットは、上流の MySQL/MariaDB からローカル ディスクに完全なデータをダンプします。

### 負荷処理ユニット {#load-processing-unit}

ロード処理ユニットは、ダンプ処理ユニットのダンプされたファイルを読み取り、これらのファイルを下流の TiDB にロードします。

### Binlogレプリケーション/同期処理ユニット {#binlog-replication-sync-processing-unit}

Binlogレプリケーション/同期処理ユニットは、上流の MySQL/MariaDB のbinlogイベントまたはリレー ログのbinlogイベントを読み取り、これらのイベントを SQL ステートメントに変換してから、これらのステートメントを下流の TiDB に適用します。

## DM-worker に必要な権限 {#privileges-required-by-dm-worker}

このセクションでは、DM-worker が必要とするアップストリームおよびダウンストリーム データベース ユーザーの権限と、それぞれの処理ユニットが必要とするユーザー権限について説明します。

### アップストリーム データベース ユーザー権限 {#upstream-database-user-privileges}

アップストリーム データベース (MySQL/MariaDB) ユーザーには、次の権限が必要です。

| 特権                   | 範囲    |
| :------------------- | :---- |
| `SELECT`             | テーブル  |
| `RELOAD`             | グローバル |
| `REPLICATION SLAVE`  | グローバル |
| `REPLICATION CLIENT` | グローバル |

データを`db1`から TiDB に移行する必要がある場合は、次の`GRANT`ステートメントを実行します。

```sql
GRANT RELOAD,REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'your_user'@'your_wildcard_of_host'
GRANT SELECT ON db1.* TO 'your_user'@'your_wildcard_of_host';
```

他のデータベースから TiDB にデータを移行する必要がある場合は、それぞれのデータベースのユーザーに同じ権限が付与されていることを確認してください。

### ダウンストリーム データベース ユーザー権限 {#downstream-database-user-privileges}

ダウンストリーム データベース (TiDB) ユーザーには、次の権限が必要です。

| 特権       | 範囲          |
| :------- | :---------- |
| `SELECT` | テーブル        |
| `INSERT` | テーブル        |
| `UPDATE` | テーブル        |
| `DELETE` | テーブル        |
| `CREATE` | データベース、テーブル |
| `DROP`   | データベース、テーブル |
| `ALTER`  | テーブル        |
| `INDEX`  | テーブル        |

移行する必要があるデータベースまたはテーブルに対して、次の`GRANT`ステートメントを実行します。

```sql
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX ON db.table TO 'your_user'@'your_wildcard_of_host';
```

### 各処理ユニットに必要な最小限の特権 {#minimal-privilege-required-by-each-processing-unit}

| 処理ユニット          | 最小限のアップストリーム (MySQL/MariaDB) 特権                                                                          | 最小限のダウンストリーム (TiDB) 特権                                                                                                                                                                            | 最小限のシステム権限          |
| :-------------- | :------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------ |
| 中継ログ            | `REPLICATION SLAVE` (binlogを読む)<br/> `REPLICATION CLIENT` ( `show master status` , `show slave status` ) | ヌル                                                                                                                                                                                                | ローカル ファイルの読み取り/書き込み |
| ごみ              | `SELECT`<br/> `RELOAD` (読み取りロックでテーブルをフラッシュし、テーブルのロックを解除します）                                              | ヌル                                                                                                                                                                                                | ローカル ファイルの書き込み      |
| ロード             | ヌル                                                                                                       | `SELECT` (チェックポイント履歴を照会)<br/> `CREATE` (データベース/テーブルを作成する)<br/> `DELETE` (チェックポイントを削除)<br/> `INSERT` (ダンプ データの挿入)                                                                                  | ローカル ファイルの読み取り/書き込み |
| Binlogのレプリケーション | `REPLICATION SLAVE` (binlogを読む)<br/> `REPLICATION CLIENT` ( `show master status` , `show slave status` ) | `SELECT` (インデックスと列を表示)<br/> `INSERT` (DML)<br/> `UPDATE` (DML)<br/> `DELETE` (DML)<br/> `CREATE` (データベース/テーブルを作成)<br/> `DROP` (データベース/テーブルを削除)<br/> `ALTER` (テーブルを変更)<br/> `INDEX` (インデックスの作成/削除) | ローカル ファイルの読み取り/書き込み |

> **ノート：**
>
> これらの権限は不変ではなく、リクエストが変更されると変更されます。
