---
title: DM-worker Introduction
summary: Learn the features of DM-worker.
---

# DMワーカーの紹介 {#dm-worker-introduction}

DM-workerは、MySQL/MariaDBからTiDBにデータを移行するために使用されるツールです。

次の機能があります。

-   MySQLまたはMariaDBインスタンスのセカンダリデータベースとして機能します
-   MySQL / MariaDBからbinlogイベントを読み取り、ローカルストレージに保持します
-   1人のDMワーカーが、1つのMySQL/MariaDBインスタンスのデータを複数のTiDBインスタンスに移行することをサポートします
-   複数のDMワーカーは、複数のMySQL/MariaDBインスタンスのデータを1つのTiDBインスタンスに移行することをサポートします

## DM-worker処理ユニット {#dm-worker-processing-unit}

DM-workerタスクには、リレーログ、ダンプ処理ユニット、ロード処理ユニット、binlogレプリケーションなどの複数のロジックユニットが含まれています。

### リレーログ {#relay-log}

リレーログは、アップストリームのMySQL / MariaDBからのbinlogデータを永続的に保存し、binlogレプリケーションのbinlogイベントにアクセスする機能を提供します。

その理論的根拠と機能は、MySQLのリレーログに似ています。詳細については、 [MySQLリレーログ](https://dev.mysql.com/doc/refman/5.7/en/replica-logs-relaylog.html)を参照してください。

### ダンプ処理装置 {#dump-processing-unit}

ダンプ処理ユニットは、アップストリームのMySQL/MariaDBからローカルディスクに完全なデータをダンプします。

### 負荷処理装置 {#load-processing-unit}

ロード処理装置は、ダンプ処理装置のダンプされたファイルを読み取り、これらのファイルをダウンストリームのTiDBにロードします。

### Binlogレプリケーション/同期処理ユニット {#binlog-replication-sync-processing-unit}

Binlogレプリケーション/同期処理ユニットは、アップストリームのMySQL / MariaDBのbinlogイベントまたはリレーログのbinlogイベントを読み取り、これらのイベントをSQLステートメントに変換してから、これらのステートメントをダウンストリームのTiDBに適用します。

## DM-workerに必要な権限 {#privileges-required-by-dm-worker}

このセクションでは、DM-workerに必要なアップストリームおよびダウンストリームのデータベースユーザーの特権と、それぞれの処理装置に必要なユーザー特権について説明します。

### アップストリームデータベースのユーザー権限 {#upstream-database-user-privileges}

アップストリームデータベース（MySQL / MariaDB）ユーザーには、次の権限が必要です。

| 特権                   | 範囲    |
| :------------------- | :---- |
| `SELECT`             | テーブル  |
| `RELOAD`             | グローバル |
| `REPLICATION SLAVE`  | グローバル |
| `REPLICATION CLIENT` | グローバル |

データを`db1`からTiDBに移行する必要がある場合は、次の`GRANT`のステートメントを実行します。

```sql
GRANT RELOAD,REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'your_user'@'your_wildcard_of_host'
GRANT SELECT ON db1.* TO 'your_user'@'your_wildcard_of_host';
```

他のデータベースからTiDBにデータを移行する必要がある場合は、それぞれのデータベースのユーザーに同じ権限が付与されていることを確認してください。

### ダウンストリームデータベースのユーザー権限 {#downstream-database-user-privileges}

ダウンストリームデータベース（TiDB）ユーザーには、次の権限が必要です。

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

移行する必要のあるデータベースまたはテーブルに対して、次の`GRANT`のステートメントを実行します。

```sql
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX  ON db.table TO 'your_user'@'your_wildcard_of_host';
```

### 各処理装置に必要な最小限の特権 {#minimal-privilege-required-by-each-processing-unit}

| 処理装置           | 最小限のアップストリーム（MySQL / MariaDB）特権                                                                          | 最小限のダウンストリーム（TiDB）特権                                                                                                                                                                                       | 最小限のシステム特権         |
| :------------- | :------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------- |
| リレーログ          | `REPLICATION SLAVE` （binlogを読み取ります）<br/> `REPLICATION CLIENT` （ `show master status` `show slave status` | ヌル                                                                                                                                                                                                         | ローカルファイルの読み取り/書き込み |
| ごみ             | `SELECT`<br/> `RELOAD` （読み取りロックを使用してテーブルをフラッシュし、テーブルのロックを解除します）                                          | ヌル                                                                                                                                                                                                         | ローカルファイルを書き込む      |
| ロード            | ヌル                                                                                                       | `SELECT` （チェックポイント履歴を照会する）<br/> `CREATE` （データベース/テーブルを作成します）<br/> `DELETE` （チェックポイントを削除します）<br/> `INSERT` （ダンプデータを挿入します）                                                                                   | ローカルファイルの読み取り/書き込み |
| Binlogレプリケーション | `REPLICATION SLAVE` （binlogを読み取ります）<br/> `REPLICATION CLIENT` （ `show master status` `show slave status` | `SELECT` （インデックスと列を表示）<br/> `INSERT` （DML）<br/> `UPDATE` （DML）<br/> `DELETE` （DML）<br/> `CREATE` （データベース/テーブルを作成します）<br/> `DROP` （データベース/テーブルを削除します）<br/> `ALTER` （テーブルを変更します）<br/> `INDEX` （インデックスを作成/削除） | ローカルファイルの読み取り/書き込み |

> **ノート：**
>
> これらの特権は不変ではなく、要求が変更されると変更されます。
