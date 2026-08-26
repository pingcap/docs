---
title: DM-worker Introduction
summary: DM-worker の機能について学びます。
---

# DMワーカー紹介 {#dm-worker-introduction}

DM-worker は、TiDB Data Migration (DM) のコンポーネントであり、DM-master によって割り当てられたタスクとサブタスクを実行します。フルおよび増分移行では、1つの MySQL 互換ソースインスタンスからデータをダンプし、ダンプしたデータをターゲット TiDB クラスターにロードします。その後、レプリケーションクライアントとしてソース Binlog を読み取り、イベントを変換およびフィルタリングして、ターゲットに適用します。DM-master は、ソースとサブタスクのステータスについて DM-worker に問い合わせます。

## 主要な概念 {#key-concepts}

- ワーカーインスタンスがオフラインになると、DM-master はそのタスクを別の利用可能なワーカーに自動的に再スケジュールして、データレプリケーションを再開できます。これはフルエクスポート/インポートフェーズ中には適用されないことに注意してください。
- 1 つの DM-worker プロセスは、一度に **1つ** の上流ソースデータベースインスタンスに接続します。シャードテーブルのマージ時など、複数のソースから移行するには、複数の DM-worker プロセスを実行する必要があります。

> **Note:**
>
> DM-worker は MySQL 互換の Binlog クライアントであり、スタンバイデータベースのレプリカサーバーではありません。MySQL 互換ソースから TiDB ターゲットへデータを読み取って再生します。ソース TiDB クラスターからデータをレプリケートするには、[TiCDC](/ticdc/ticdc-overview.md) を使用してください。

## DM-worker 処理ユニット {#dm-worker-processing-units}

タスクモードに応じて、DM-worker のサブタスクは ダンプ、ロード、Binlog複製/同期の各処理ユニットを実行します。DM-worker は、バインドされたソースに対してオプションのリレーログ処理ユニットを実行することもできます。

### リレーログ {#relay-log}

リレーログはオプションであり、デフォルトでは無効になっています。有効にすると、DM-worker は上流 Binlog イベントをローカルディスクに保存してから、Binlog replication 処理ユニットがそれらを読み取ります。長時間実行されるフル移行やブロックされたタスクが上流 Binlog の保持期間を超える可能性がある場合、または同じソースに対する複数のタスクで単一の Binlog ストリームを共有する必要がある場合は、リレーログを有効にしてください。リレーログはディスク、I/O、CPU リソースを消費し、レプリケーションレイテンシーを増加させる可能性があります。設定および運用の詳細については、[データ移行リレーログ](/dm/relay-log.md) を参照してください。

### ダンプ処理装置 {#dump-processing-unit}

ダンプ処理ユニットは、アップストリームの MySQL/MariaDB から完全なデータをローカルディスクにダンプします。

### ロード処理装置 {#load-processing-unit}

ロード処理ユニットは、ダンプ処理ユニットのダンプされたファイルを読み取り、これらのファイルを下流の TiDB にロードします。

### Binlog複製/同期処理ユニット {#binlog-replication-sync-processing-unit}

Binlogログレプリケーション/同期処理ユニットは、上流の MySQL/MariaDB のbinlogイベントまたはリレーログのbinlogイベントを読み取り、これらのイベントを SQL ステートメントに変換し、下流の TiDB にこれらのステートメントを適用します。

## DMワーカーに必要な権限 {#privileges-required-by-dm-worker}

このセクションでは、DM-worker に必要な上流および下流のデータベースユーザーの権限と、それぞれの処理ユニットに必要なユーザー権限について説明します。

### 上流データベースユーザー権限 {#upstream-database-user-privileges}

上流データベースユーザーに必要な権限は、データベースの種類 (MySQL/MariaDB) とバージョンによって異なります。

> **Note:**
>
> - `FLUSH TABLES WITH READ LOCK` (FTWRL) が許可されていないマネージド MySQL サービス (Amazon RDS、Aurora、ApsaraDB RDS for MySQL、Azure Database for MySQL、Google Cloud SQL など) から移行する場合は、`LOCK TABLES` 権限も付与してください。デフォルトの `consistency=auto` 設定では、FTWRL が使用できないときに DM は `LOCK TABLES` にフォールバックします。
>
>     ```sql
>     GRANT LOCK TABLES ON db1.* TO 'your_user'@'your_wildcard_of_host';
>     ```
>
> - 他のデータベースから TiDB にデータを移行する必要がある場合は、それぞれのデータベースのユーザーに同じ権限が付与されていることを確認してください。

#### MySQL および MariaDB（MariaDB 10.5.2 より前） {#mysql-and-mariadb-before-mariadb-1052}

MySQL、および 10.5.2 より前の MariaDB バージョンでは、ユーザーに次の権限が必要です。

| 権限 | 範囲 |
|:----|:----|
| `SELECT` | Tables |
| `RELOAD` | Global |
| `REPLICATION SLAVE` | Global |
| `REPLICATION CLIENT` | Global |

これらの権限を付与するには、次のステートメントを実行します。

```sql
GRANT RELOAD, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'your_user'@'your_wildcard_of_host';
GRANT SELECT ON `db1`.* TO 'your_user'@'your_wildcard_of_host';
```

10.5.2 より前の MariaDB からフルデータエクスポートを行う場合は、ダンプユニットが InnoDB メタデータをクエリできるように、`PROCESS` も付与してください。

```sql
GRANT PROCESS ON *.* TO 'your_user'@'your_wildcard_of_host';
```

#### MariaDB 10.5.2 から 10.5.8 {#mariadb-1052-to-1058}

[MariaDB 10.5.2](https://mariadb.com/docs/release-notes/community-server/old-releases/10.5/10.5.2) 以降では、`REPLICATION CLIENT` 権限は `BINLOG MONITOR` に名前変更され、いくつかのレプリケーションステートメントでは `SUPER` を分割して作成された新しい権限が使用されます。MariaDB 10.5.2 から 10.5.8 では、ユーザーに次の権限が必要です。

| 権限 | 範囲 | 説明 |
|:---|:---|:---|
| `SELECT` | Tables | フルデータエクスポートに必要です。 |
| `PROCESS` | Global | フルデータエクスポート中の InnoDB メタデータクエリに必要です。 |
| `RELOAD` | Global | `FLUSH TABLES WITH READ LOCK` に必要です。 |
| `BINLOG MONITOR` | Global | `REPLICATION CLIENT` から名前変更され、Binlog の監視を可能にします。 |
| `REPLICATION SLAVE` | Global | Binlog イベントの読み取りを可能にします。 |
| `REPLICATION SLAVE ADMIN` | Global | レプリケーションステータスの管理を可能にします (たとえば、`SHOW SLAVE STATUS`)。 |
| `REPLICATION MASTER ADMIN`| Global | マスターの監視を可能にします (たとえば、`SHOW SLAVE HOSTS`)。 |

これらの権限を付与するには、次のステートメントを実行します。

```sql
GRANT PROCESS, RELOAD, BINLOG MONITOR, REPLICATION SLAVE, REPLICATION SLAVE ADMIN, REPLICATION MASTER ADMIN ON *.* TO 'your_user'@'your_wildcard_of_host';
GRANT SELECT ON `db1`.* TO 'your_user'@'your_wildcard_of_host';
```

#### MariaDB 10.5.9 以降 {#mariadb-1059-or-later}

[MariaDB 10.5.9](https://mariadb.com/docs/release-notes/community-server/old-releases/10.5/10.5.9) 以降では、`SHOW SLAVE STATUS` と `SHOW REPLICA STATUS` に `REPLICA MONITOR` 権限が必要です。MariaDB は `SHOW GRANTS` でこの権限を `SLAVE MONITOR` として表示します。MariaDB 10.5.2 から 10.5.8 に記載された権限に加えて、`REPLICA MONITOR` を付与してください。

```sql
GRANT PROCESS, RELOAD, BINLOG MONITOR, REPLICATION SLAVE, REPLICATION SLAVE ADMIN, REPLICATION MASTER ADMIN, REPLICA MONITOR ON *.* TO 'your_user'@'your_wildcard_of_host';
GRANT SELECT ON `db1`.* TO 'your_user'@'your_wildcard_of_host';
```

> **Note:**
>
> MariaDB はこれらの権限を MySQL とは異なる形で報告するため、アカウントに必要な権限がある場合でも、`dmctl check-task` が権限エラーを報告することがあります。
>
> DM v8.5.6 で、事前チェックがレプリケーション権限、dump 権限、または dump 接続数チェックに対して `[code=26005] fail to check synchronization configuration` を返す場合は、タスク設定ファイルに次の項目のみを追加してください。
>
> ```yaml
> ignore-checking-items:
>   - replication_privilege
>   - dump_privilege
>   - conn_number
> ```
>
> この回避策では、MariaDB 権限パーサーの影響を受ける 3つのチェックのみをスキップします。使用する前に、対応する権限と接続上限を手動で確認してください。詳細については、[DM precheck](/dm/dm-precheck.md) を参照してください。

> **Note:**
>
> 一部の古い MariaDB リリースでは、ダンプユニットが InnoDB メタデータをクエリするために `PROCESS` だけでは不十分です。DM v8.5.6 では、この動作は ダンプユニットが MariaDB 10.4.34 で `INNODB_TABLESPACES_SCRUBBING` を、または MariaDB 10.5.1 と 10.5.2 で `INNODB_TABLESPACES_ENCRYPTION` をクエリするときに発生します。同じスモークテストでは、MariaDB 10.5.9、10.6.13、10.11.16 は `SUPER` なしで完了します。
>
> ダンプユニットが次のエラーを返す場合は、`SUPER` を付与してください。`SUPER` は広範な権限であるため、この正確なエラーが発生し、かつセキュリティポリシーで許可されている場合にのみ付与してください。
>
> ```
> Error 1227 (42000): Access denied; you need (at least one of) the SUPER privilege(s) for this operation
> ```

### 下流データベースユーザー権限 {#downstream-database-user-privileges}

ダウンストリームデータベース (TiDB) ユーザーには、次の権限が必要です。

| 権限       | 範囲          |
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

次の表は、MySQL および 10.5.2 より前の MariaDB バージョンについて、各処理ユニットに必要な最小限の権限を示しています。MariaDB 10.5.2 以降については、前のセクションの権限表を参照してください。

| 処理装置           | 最小限のアップストリーム（MySQL/MariaDB）権限                                                                              | 最小限のダウンストリーム (TiDB) 権限                                                                                                                                                                                | 最小限のシステム権限         |
| :------------- | :--------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------- |
| リレーログ          | `REPLICATION SLAVE` (binlogを読み取る)<br/> `REPLICATION CLIENT` ( `SHOW MASTER STATUS` , `SHOW SLAVE STATUS` ) | ヌル                                                                                                                                                                                                    | ローカルファイルの読み取り/書き込み |
| ダンプ             | `SELECT`<br/> `RELOAD` (`FLUSH TABLES WITH READ LOCK`)<br/>`PROCESS` (MariaDB のみ、InnoDB メタデータクエリ用)                                            | ヌル                                                                                                                                                                                                    | ローカルファイルを書き込む      |
| ロード             | ヌル                                                                                                         | `SELECT` (チェックポイント履歴を照会する)<br/> `CREATE` (データベース/テーブルを作成する)<br/> `DELETE` （チェックポイントを削除）<br/> `INSERT` (ダンプデータを挿入)                                                                                     | ローカルファイルの読み取り/書き込み |
| Binlogレプリケーション | `REPLICATION SLAVE` (binlogを読み取る)<br/> `REPLICATION CLIENT` ( `SHOW MASTER STATUS` , `SHOW SLAVE STATUS` ) | `SELECT` (インデックスと列を表示)<br/> `INSERT` （DML）<br/> `UPDATE` (DML)<br/> `DELETE` （DML）<br/> `CREATE` (データベース/テーブルを作成する)<br/> `DROP` (データベース/テーブルを削除)<br/> `ALTER` （テーブルを変更する）<br/> `INDEX` (インデックスの作成/削除) | ローカルファイルの読み取り/書き込み |
