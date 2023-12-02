---
title: DM-worker Introduction
summary: Learn the features of DM-worker.
---

# DMワーカー紹介 {#dm-worker-introduction}

DM-worker は、MySQL/MariaDB から TiDB にデータを移行するために使用されるツールです。

次のような特徴があります。

-   MySQL または MariaDB インスタンスのセカンダリ データベースとして機能します
-   MySQL/MariaDB からbinlogイベントを読み取り、ローカルstorageに保存します。
-   単一の DM ワーカーは、1 つの MySQL/MariaDB インスタンスのデータを複数の TiDB インスタンスに移行することをサポートします。
-   複数の DM ワーカーは、複数の MySQL/MariaDB インスタンスのデータを 1 つの TiDB インスタンスに移行することをサポートします。

## DMワーカー処理装置 {#dm-worker-processing-unit}

DM ワーカー タスクには、リレー ログ、ダンプ処理ユニット、ロード処理ユニット、binlogレプリケーションなどの複数の論理ユニットが含まれています。

### リレーログ {#relay-log}

リレー ログは、上流の MySQL/MariaDB からのbinlogデータを永続的に保存し、binlogレプリケーションのbinlogイベントにアクセスする機能を提供します。

その原理と機能は MySQL のリレー ログに似ています。詳細は[MySQLリレーログ](https://dev.mysql.com/doc/refman/8.0/en/replica-logs-relaylog.html)を参照してください。

### ダンプ処理ユニット {#dump-processing-unit}

ダンプ処理ユニットは、上流の MySQL/MariaDB からローカル ディスクに完全なデータをダンプします。

### ロード処理ユニット {#load-processing-unit}

ロード処理ユニットは、ダンプ処理ユニットのダンプされたファイルを読み取り、これらのファイルを下流の TiDB にロードします。

### Binlogレプリケーション/同期処理ユニット {#binlog-replication-sync-processing-unit}

Binlogレプリケーション/同期処理ユニットは、アップストリーム MySQL/MariaDB のbinlogイベントまたはリレー ログのbinlogイベントを読み取り、これらのイベントを SQL ステートメントに変換し、これらのステートメントをダウンストリーム TiDB に適用します。

## DM ワーカーに必要な権限 {#privileges-required-by-dm-worker}

このセクションでは、DM ワーカーに必要な上流および下流のデータベース ユーザーの権限、およびそれぞれの処理ユニットに必要なユーザー権限について説明します。

### 上流データベースのユーザー権限 {#upstream-database-user-privileges}

上流データベース (MySQL/MariaDB) ユーザーには次の権限が必要です。

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

### ダウンストリームデータベースのユーザー権限 {#downstream-database-user-privileges}

ダウンストリーム データベース (TiDB) ユーザーには次の権限が必要です。

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

移行する必要があるデータベースまたはテーブルに対して次の`GRANT`ステートメントを実行します。

```sql
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX ON db.table TO 'your_user'@'your_wildcard_of_host';
GRANT ALL ON dm_meta.* TO 'your_user'@'your_wildcard_of_host';
```

### 各処理ユニットに必要な最小限の権限 {#minimal-privilege-required-by-each-processing-unit}

| 処理装置           | 最小限のアップストリーム (MySQL/MariaDB) 権限                                                                              | 最小限のダウンストリーム (TiDB) 権限                                                                                                                                                                               | 最小限のシステム権限         |
| :------------- | :----------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------- |
| リレーログ          | `REPLICATION SLAVE` (binlogを読み取ります)<br/> `REPLICATION CLIENT` ( `show master status` 、 `show slave status` ) | ヌル                                                                                                                                                                                                   | ローカルファイルの読み取り/書き込み |
| ごみ             | `SELECT`<br/> `RELOAD` (読み取りロックでテーブルをフラッシュし、テーブルのロックを解除します）                                                  | ヌル                                                                                                                                                                                                   | ローカルファイルの書き込み      |
| 負荷             | ヌル                                                                                                           | `SELECT` (チェックポイント履歴を問い合わせる)<br/> `CREATE` (データベース/テーブルを作成します)<br/> `DELETE` (チェックポイントを削除)<br/> `INSERT` (ダンプデータを挿入)                                                                                 | ローカルファイルの読み取り/書き込み |
| Binlogレプリケーション | `REPLICATION SLAVE` (binlogを読み取ります)<br/> `REPLICATION CLIENT` ( `show master status` 、 `show slave status` ) | `SELECT` (インデックスと列を表示)<br/> `INSERT` (DML)<br/> `UPDATE` (DML)<br/> `DELETE` (DML)<br/> `CREATE` (データベース/テーブルを作成します)<br/> `DROP` (データベース/テーブルを削除)<br/> `ALTER` (テーブルを変更)<br/> `INDEX` (インデックスの作成/削除) | ローカルファイルの読み取り/書き込み |

> **注記：**
>
> これらの権限は不変ではなく、リクエストの変更に応じて変更されます。
