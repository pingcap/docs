---
title: DM-worker Introduction
summary: DM-worker の機能について学びます。
---

# DMワーカー紹介 {#dm-worker-introduction}

DM-worker は、MySQL/MariaDB から TiDB にデータを移行するために使用されるツールです。

以下の機能があります:

-   任意のMySQLまたはMariaDBインスタンスのセカンダリデータベースとして機能します
-   MySQL/MariaDBからbinlogイベントを読み取り、ローカルstorageに保存します。
-   単一の DM ワーカーは、1 つの MySQL/MariaDB インスタンスのデータを複数の TiDB インスタンスに移行することをサポートします。
-   複数の DM ワーカーは、複数の MySQL/MariaDB インスタンスのデータを 1 つの TiDB インスタンスに移行することをサポートします。

## DMワーカー処理ユニット {#dm-worker-processing-unit}

DM ワーカー タスクには、リレー ログ、ダンプ処理ユニット、ロード処理ユニット、binlogレプリケーションなど、複数のロジック ユニットが含まれます。

### リレーログ {#relay-log}

リレー ログは、アップストリーム MySQL/MariaDB からのbinlogデータを永続的に保存し、binlogレプリケーションのbinlogイベントにアクセスする機能を提供します。

その原理と機能はMySQLのリレーログに似ています。詳細については[MySQLリレーログ](https://dev.mysql.com/doc/refman/8.0/en/replica-logs-relaylog.html)参照してください。

### ダンプ処理装置 {#dump-processing-unit}

ダンプ処理ユニットは、アップストリームの MySQL/MariaDB から完全なデータをローカル ディスクにダンプします。

### 負荷処理装置 {#load-processing-unit}

ロード処理ユニットは、ダンプ処理ユニットのダンプされたファイルを読み取り、これらのファイルを下流の TiDB にロードします。

### Binlog複製/同期処理ユニット {#binlog-replication-sync-processing-unit}

Binlogログレプリケーション/同期処理ユニットは、上流の MySQL/MariaDB のbinlogイベントまたはリレーログのbinlogイベントを読み取り、これらのイベントを SQL ステートメントに変換し、下流の TiDB にこれらのステートメントを適用します。

## DMワーカーに必要な権限 {#privileges-required-by-dm-worker}

このセクションでは、DM-worker に必要な上流および下流のデータベース ユーザーの権限と、それぞれの処理ユニットに必要なユーザー権限について説明します。

### 上流データベースユーザー権限 {#upstream-database-user-privileges}

アップストリーム データベース (MySQL/MariaDB) ユーザーには次の権限が必要です。

| 特権                   | 範囲    |
| :------------------- | :---- |
| `SELECT`             | テーブル  |
| `RELOAD`             | グローバル |
| `REPLICATION SLAVE`  | グローバル |
| `REPLICATION CLIENT` | グローバル |

`db1`から TiDB にデータを移行する必要がある場合は、次の`GRANT`ステートメントを実行します。

```sql
GRANT RELOAD,REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'your_user'@'your_wildcard_of_host';
GRANT SELECT ON db1.* TO 'your_user'@'your_wildcard_of_host';
```

他のデータベースから TiDB にデータを移行する必要がある場合は、それぞれのデータベースのユーザーに同じ権限が付与されていることを確認してください。

### 下流データベースユーザー権限 {#downstream-database-user-privileges}

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

移行する必要があるデータベースまたはテーブルに対して次の`GRANT`ステートメントを実行します。

```sql
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER,INDEX ON db.table TO 'your_user'@'your_wildcard_of_host';
GRANT ALL ON dm_meta.* TO 'your_user'@'your_wildcard_of_host';
```

### 各処理ユニットに必要な最小限の権限 {#minimal-privilege-required-by-each-processing-unit}

| 処理装置           | 最小限のアップストリーム（MySQL/MariaDB）権限                                                                              | 最小限のダウンストリーム (TiDB) 権限                                                                                                                                                                                | 最小限のシステム権限         |
| :------------- | :--------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------- |
| リレーログ          | `REPLICATION SLAVE` (binlogを読み取る)<br/> `REPLICATION CLIENT` ( `show master status` , `show slave status` ) | ヌル                                                                                                                                                                                                    | ローカルファイルの読み取り/書き込み |
| ごみ             | `SELECT`<br/> `RELOAD` (読み取りロックがかかったテーブルをフラッシュし、テーブルのロックを解除します）                                            | ヌル                                                                                                                                                                                                    | ローカルファイルを書き込む      |
| 負荷             | ヌル                                                                                                         | `SELECT` (チェックポイント履歴を照会する)<br/> `CREATE` (データベース/テーブルを作成する)<br/> `DELETE` （チェックポイントを削除）<br/> `INSERT` (ダンプデータを挿入)                                                                                     | ローカルファイルの読み取り/書き込み |
| Binlogレプリケーション | `REPLICATION SLAVE` (binlogを読み取る)<br/> `REPLICATION CLIENT` ( `show master status` , `show slave status` ) | `SELECT` (インデックスと列を表示)<br/> `INSERT` （DML）<br/> `UPDATE` (DML)<br/> `DELETE` （DML）<br/> `CREATE` (データベース/テーブルを作成する)<br/> `DROP` (データベース/テーブルを削除)<br/> `ALTER` （テーブルを変更する）<br/> `INDEX` (インデックスの作成/削除) | ローカルファイルの読み取り/書き込み |

> **注記：**
>
> これらの権限は不変ではなく、リクエストが変更されると変更されます。
