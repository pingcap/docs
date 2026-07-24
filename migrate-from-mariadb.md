---
title: Migrate Data from MariaDB to TiDB
summary: MariaDBからTiDBへのデータ移行方法を学びましょう。
---

# MariaDBからTiDBへのデータ移行 {#migrate-data-from-mariadb-to-tidb}

このドキュメントでは、MariaDBサーバー環境からTiDBクラスタへデータを移行する方法について説明します。

## 前提条件 {#prerequisites}

適切な移行戦略を選択してください。

-   最初の戦略は、 [Dumplingでデータをダンプし、 TiDB Lightningでデータを復元する](#dump-data-with-dumpling-and-restore-data-with-tidb-lightning)です。これは MariaDB のすべてのバージョンで機能します。この戦略の欠点は、より多くのダウンタイムが必要になることです。
-   2 番目の戦略は、 [DMを使用してデータを複製する](#replicate-data-with-dm)ことです。 DM は MariaDB のすべてのバージョンをサポートしているわけではありません。サポートされているバージョンは、 [DM互換性カタログ](/dm/dm-compatibility-catalog.md#compatibility-catalog-of-tidb-data-migration)に記載されています。

これら2つの戦略以外にも、あなたの状況に特化した戦略が存在する可能性があります。例えば、以下のような戦略です。

-   オブジェクトリレーショナルマッピング（ORM）の機能を使用して、データを再デプロイおよび移行してください。
-   移行作業中は、アプリケーションを修正してMariaDBとTiDBの両方から書き込みを行えるようにしてください。

この文書では、最初の2つの戦略のみを取り上げています。

選択した戦略に基づいて、以下のものを準備してください。

-   **ダンプとリストアの**戦略について：
    -   [Dumpling](/dumpling-overview.md)と[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)をインストールしてください。
    -   Dumpling がデータをエクスポートするために MariaDBサーバー上で [必要な権限](/dumpling-overview.md#required-privileges)を持っていることを確認してください。
-   **データレプリケーション**戦略として、[データ移行（DM）](/dm/dm-overview.md)を設定します。

## 互換性を確認してください {#check-compatibility}

TiDBは[MySQLと互換性あり](/mysql-compatibility.md)。MySQLとMariaDBには多くの共通機能がありますが、移行前に知っておくべきMariaDB固有の機能の中には、TiDBと互換性がないものがあるかもしれません。

このセクションの項目を確認するだけでなく、MariaDB ドキュメントの[互換性と相違点](https://mariadb.com/docs/release-notes/community-server/about/compatibility-and-differences)も確認することをお勧めします。

### 認証 {#authentication}

[MySQLとのセキュリティ互換性](/security-compatibility-with-mysql.md)ドキュメントには、TiDBがサポートする認証方法が記載されています。TiDBはMariaDBの一部の認証方法をサポートしていません。そのため、アカウント用に新しいパスワードハッシュを作成するか、その他の特別な対策を講じる必要がある場合があります。

使用されている認証方法を確認するには、次のステートメントを実行します。

```sql
SELECT
  plugin,
  COUNT(*)
FROM
  mysql.user
GROUP BY
  plugin;
```

```sql
+-----------------------+----------+
| plugin                | COUNT(*) |
+-----------------------+----------+
| mysql_native_password |       11 |
+-----------------------+----------+
1 row in set (0.002 sec)
```

### システムバージョン管理されたテーブル {#system-versioned-tables}

TiDB は[システムバージョン管理されたテーブル](https://mariadb.com/docs/server/reference/sql-structure/temporal-tables/system-versioned-tables)サポートしていません。ただし、TiDB は[`AS OF TIMESTAMP`](/as-of-timestamp.md)をサポートしており、システム バージョン管理テーブルの使用例の一部を置き換える可能性があります。

影響を受けるテーブルは、以下のステートメントで確認できます。

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME
FROM
  information_schema.tables
WHERE
  TABLE_TYPE='SYSTEM VERSIONED';
```

```sql
+--------------+------------+
| TABLE_SCHEMA | TABLE_NAME |
+--------------+------------+
| test         | t          |
+--------------+------------+
1 row in set (0.005 sec)
```

システムのバージョン管理を削除するには、 `ALTER TABLE`ステートメントを実行します。

```sql
MariaDB [test]> ALTER TABLE t DROP SYSTEM VERSIONING;
Query OK, 0 rows affected (0.071 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

### シーケンス {#sequences}

MariaDBとTiDBはどちらも[`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)をサポートしています。しかし、DMは現在この機能をサポートしていません。移行中はシーケンスの作成、変更、削除を行わないことを推奨し、移行後にこの点を特にテストすることをお勧めします。

シーケンスを使用しているかどうかを確認するには、次のステートメントを実行してください。

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME
FROM
  information_schema.tables
WHERE
  TABLE_TYPE='SEQUENCE';
```

```sql
+--------------+------------+
| TABLE_SCHEMA | TABLE_NAME |
+--------------+------------+
| test         | s1         |
+--------------+------------+
1 row in set (0.016 sec)
```

### ストレージエンジン {#storage-engines}

MariaDB は`InnoDB` 、 `MyISAM` 、 `Aria`などのストレージデータ用のストレージ エンジンを提供しています。これらのデータ形式は TiDB で直接サポートされていませんが、移行は問題なく行えます。ただし、 `CONNECT`ストレージエンジンや`Spider`など、サーバー外にデータを配置するエンジンもあります。これらのテーブルを TiDB に移行することはできますが、TiDB は TiDB クラスタ外にデータを保存する機能を提供していません。

使用しているストレージエンジンを確認するには、次のステートメントを実行してください。

```sql
SELECT
  ENGINE,
  COUNT(*)
FROM
  information_schema.tables
GROUP BY
  ENGINE;
```

```sql
+--------------------+----------+
| ENGINE             | COUNT(*) |
+--------------------+----------+
| NULL               |      101 |
| Aria               |       38 |
| CSV                |        2 |
| InnoDB             |        6 |
| MEMORY             |       67 |
| MyISAM             |        1 |
| PERFORMANCE_SCHEMA |       81 |
+--------------------+----------+
7 rows in set (0.009 sec)
```

### 構文 {#syntax}

MariaDB は`RETURNING` 、 `DELETE` 、および`INSERT`ステートメントに対して`REPLACE`キーワードをサポートしています。TiDB はこれらをサポートしていません。移行に影響があるかどうかを確認するために、アプリケーションとクエリのログを確認することをお勧めします。

### データ型 {#data-types}

MariaDB は、 `UUID` 、 `INET4` 、 `INET6` 。

これらのデータ型を確認するには、次のステートメントを実行します。

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME,
  COLUMN_NAME,
  DATA_TYPE
FROM
  information_schema.columns
WHERE
  DATA_TYPE IN('INET4','INET6','UUID');
```

```sql
+--------------+------------+-------------+-----------+
| TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME | DATA_TYPE |
+--------------+------------+-------------+-----------+
| test         | u1         | u           | uuid      |
| test         | u1         | i4          | inet4     |
| test         | u1         | i6          | inet6     |
+--------------+------------+-------------+-----------+
3 rows in set (0.026 sec)

```

### 文字セットと照合順序 {#character-set-and-collation}

TiDB は、MariaDB でよく使用される`latin1_swedish_ci`照合順序をサポートしていません。

TiDB は、MariaDB 11.6 以降のバージョンの照合順序の照合順序である`utf8mb4_uca1400_ai_ci`サポートしていません。代わりに`utf8mb4_0900_ai_ci`を使用してください。これら 2 つの照合順序は[Unicode照合アルゴリズム（UCA）](http://www.unicode.org/reports/tr10/) : `utf8mb4_0900_ai_ci`は UCA 9.0.0 を使用し、 `utf8mb4_uca1400_ai_ci`は UCA 14.0.0 を使用します。

TiDBがサポートする照合順序を確認するには、TiDBで次のステートメントを実行してください。

```sql
SHOW COLLATION;
```

```sql
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| ascii_bin          | ascii   |  65 | Yes     | Yes      |       1 | PAD SPACE     |
| binary             | binary  |  63 | Yes     | Yes      |       1 | NO PAD        |
| gbk_bin            | gbk     |  87 |         | Yes      |       1 | PAD SPACE     |
| gbk_chinese_ci     | gbk     |  28 | Yes     | Yes      |       1 | PAD SPACE     |
| latin1_bin         | latin1  |  47 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_bin           | utf8    |  83 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_general_ci    | utf8    |  33 |         | Yes      |       1 | PAD SPACE     |
| utf8_unicode_ci    | utf8    | 192 |         | Yes      |       8 | PAD SPACE     |
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       8 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
13 rows in set (0.00 sec)
```

現在使用しているテーブルの列がどの照合順序を使用しているかを確認するには、次のステートメントを使用できます。

```sql
SELECT
  TABLE_SCHEMA,
  COLLATION_NAME,
  COUNT(*)
FROM
  information_schema.columns
GROUP BY
  TABLE_SCHEMA, COLLATION_NAME
ORDER BY
  COLLATION_NAME;
```

```sql
+--------------------+--------------------+----------+
| TABLE_SCHEMA       | COLLATION_NAME     | COUNT(*) |
+--------------------+--------------------+----------+
| sys                | NULL               |      562 |
| test               | NULL               |       14 |
| mysql              | NULL               |       84 |
| performance_schema | NULL               |      892 |
| information_schema | NULL               |      421 |
| mysql              | latin1_swedish_ci  |       34 |
| performance_schema | utf8mb3_bin        |       38 |
| mysql              | utf8mb3_bin        |       61 |
| sys                | utf8mb3_bin        |       40 |
| information_schema | utf8mb3_general_ci |      375 |
| performance_schema | utf8mb3_general_ci |      244 |
| sys                | utf8mb3_general_ci |      386 |
| mysql              | utf8mb3_general_ci |       67 |
| mysql              | utf8mb4_bin        |        8 |
+--------------------+--------------------+----------+
14 rows in set (0.045 sec)
```

[文字セットと照合順序](/character-set-and-collation.md)も参照してください。

### インデックスの長さ {#index-length}

次の例に示すように、MariaDB はインデックスを自動的にプレフィックス インデックスに変換し、インデックスが最大キー長を超える場合は警告を返します。MariaDB とは異なり、TiDB は MySQL の動作に従います。つまり、自動変換は行わず、代わりにエラーを返します。したがって、MariaDB DDL を TiDB に移行する際、インデックス付き列が TiDB でサポートされる最大キー長を超える可能性がある場合は、プレフィックス インデックスを明示的に作成するようにスクリプトを変更する必要があります。

    MariaDB> \W
    Show warnings enabled.
    MariaDB> CREATE TABLE t1(id SERIAL, c1 VARCHAR(800));
    Query OK, 0 rows affected (0.024 sec)

    MariaDB> ALTER TABLE t1 ADD INDEX(c1);
    Query OK, 0 rows affected, 1 warning (0.031 sec)
    Records: 0  Duplicates: 0  Warnings: 1

    Note (Code 1071): Specified key was too long; max key length is 3072 bytes
    MariaDB> SHOW CREATE TABLE t1\G
    *************************** 1. row ***************************
           Table: t1
    Create Table: CREATE TABLE `t1` (
      `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
      `c1` varchar(800) DEFAULT NULL,
      UNIQUE KEY `id` (`id`),
      KEY `c1` (`c1`(768))
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci
    1 row in set (0.001 sec)

MariaDBには、最大キー長を超える一意インデックスに対する特別な処理機能もあります。例えば、次の例では、MariaDBは`USING HASH`列に`TEXT`一意インデックスを作成します。TiDBにはこの機能はありません。

    MariaDB> CREATE TABLE t2 (id SERIAL PRIMARY KEY, c1 TEXT NOT NULL);
    Query OK, 0 rows affected (0.015 sec)

    MariaDB> ALTER TABLE t2 ADD INDEX regular_index_c1 (c1);
    Query OK, 0 rows affected, 1 warning (0.034 sec)
    Records: 0  Duplicates: 0  Warnings: 1

    Note (Code 1071): Specified key was too long; max key length is 3072 bytes
    MariaDB> ALTER TABLE t2 ADD UNIQUE INDEX unique_index_c1 (c1);
    Query OK, 0 rows affected (0.048 sec)
    Records: 0  Duplicates: 0  Warnings: 0

    MariaDB> SHOW CREATE TABLE t2\G
    *************************** 1. row ***************************
           Table: t2
    Create Table: CREATE TABLE `t2` (
      `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
      `c1` text NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `unique_index_c1` (`c1`) USING HASH,
      KEY `regular_index_c1` (`c1`(768))
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci
    1 row in set (0.001 sec)

TiDB の長いテキスト列に一意性を持たせるには、生成ハッシュ列を追加し、その生成ハッシュ列に一意インデックスを作成します。手順は次のとおりです。

    tidb> CREATE TABLE t1 (id int PRIMARY KEY, c1 TEXT NOT NULL);
    Query OK, 0 rows affected (0.102 sec)

    tidb> ALTER TABLE t1 ADD COLUMN c1_hash BINARY(32) AS (UNHEX(SHA2(c1,256)));
    Query OK, 0 rows affected (0.242 sec)

    tidb> ALTER TABLE t1 ADD UNIQUE KEY (c1_hash);
    Query OK, 0 rows affected (0.363 sec)

    tidb> INSERT INTO t1(id,c1) VALUES (1,'aaa');
    Query OK, 1 row affected (0.015 sec)

    tidb> INSERT INTO t1(id,c1) VALUES (2,'bbb');
    Query OK, 1 row affected (0.006 sec)

    tidb> INSERT INTO t1(id,c1) VALUES (3,'aaa');
    ERROR 1062 (23000): Duplicate entry '\x984\x87m\xCF\xB0\\xB1g\xA5\xC2IS\xEB\xA5\x8CJ\xC8\x9B\x1A\xDFW' for key 't1.c1_hash'
    tidb>

## Dumplingでデータをダンプし、 TiDB Lightningでデータを復元する。 {#dump-data-with-dumpling-and-restore-data-with-tidb-lightning}

この方法は、アプリケーションをオフラインにしてデータを移行し、その後、移行したデータを使用するようにアプリケーションを再構成することを前提としています。

> **Note:**
>
> 本番で実行する前に、まずテスト環境または開発環境でこの作業を行うことを強くお勧めします。これは、互換性の問題がないかを確認するためと、移行にかかる時間を把握するためです。

MariaDBからTiDBへデータを移行するには、以下の手順を実行してください。

1.  アプリケーションを停止してください。アプリケーションをオフラインにしてください。これにより、移行中または移行後にMariaDB内のデータが変更されることがなくなります。

2.  MariaDBに[`tiup dumpling`](/dumpling-overview.md#use-dumpling-to-export-data)コマンドを使用してデータをダンプします。

    ```shell
    tiup dumpling --port 3306 --host 127.0.0.1 --user root --password secret -F 256MB  -o /data/backup
    ```

3.  `tiup tidb-lightning`コマンドを使用してデータを復元します。 TiDB Lightning の構成方法と実行方法の詳細については、 [TiDB Lightningを使い始めよう](/get-started-with-tidb-lightning.md)を参照してください。

4.  ユーザーアカウントと権限を移行します。ユーザーと権限を移行する方法の詳細については、[輸出ユーザーと助成金](#export-users-and-grants)を参照してください。

5.  アプリケーションを再構成してください。TiDBサーバーに接続できるように、アプリケーションの設定を変更する必要があります。

6.  クリーンアップ。移行が成功したことを確認したら、MariaDB のデータの最終バックアップを作成し、サーバーを停止します。これにより、 TiUP、 Dumpling、 TiDB Lightningなどのツールを削除することもできます。

## DMを使用してデータを複製する {#replicate-data-with-dm}

この方法は、レプリケーションを設定し、アプリケーションを停止してレプリケーションが追いつくまで待機し、その後アプリケーションを再構成してTiDBを使用するようにすることを前提としています。

DMを使用するには、 [TiUPクラスター](/dm/deploy-a-dm-cluster-using-tiup.md)または[TiDB Operator](/tidb-operator-overview.md)を使用して一連のDMサービスをデプロイする必要があります。その後、 `dmctl`を使用してDMサービスを構成します。

> **Note:**
>
> 本番で実行する前に、まずテスト環境または開発環境でこの作業を行うことを強くお勧めします。これは、互換性の問題がないかを確認するためと、移行にかかる時間を把握するためです。

### ステップ1. 準備する {#step-1-prepare}

MariaDB でbinlogを有効にし、 `binlog_format=ROW` 、 `binlog_row_image=FULL` 、および`binlog_legacy_event_pos=ON`を設定します。また、 `binlog_annotate_row_events=OFF`および`log_bin_compress=OFF`も設定します。

`SUPER`権限、または`BINLOG MONITOR`と`REPLICATION MASTER ADMIN`の権限を持つアカウントが必要です。また、このアカウントには、移行するスキーマに対する読み取り権限も必要です。

`SUPER`権限を持つアカウントを使用していない場合は、TiDB が MariaDB 固有の権限を確認する方法をまだ知らないため、DM 構成に以下を追加する必要があるかもしれません。

```yaml
ignore-checking-items: ["replication_privilege"]
```

DM を使用してアップストリームからダウンストリームにデータを移行する前に、事前チェックによりアップストリームのデータベース構成のエラーを検出し、移行がスムーズに行われるようにします。詳細については、[移行タスクの事前チェック](/dm/dm-precheck.md)参照してください。

### ステップ2．データの複製 {#step-2-replicate-data}

[TiDB Data Migrationクイックスタートガイド](/dm/quick-start-with-dm.md)に従って、MariaDB から TiDB にデータをレプリケートします。

MariaDBからMariaDBへのレプリケーションのように、最初に初期データをコピーする必要はありません。DMが自動的にコピーしてくれます。

### ステップ3．ユーザーアカウントと権限を移行する {#step-3-migrate-user-accounts-and-permissions}

ユーザーと権限を移行する方法については[輸出ユーザーと助成金](#export-users-and-grants)を参照してください。

### ステップ4．データをテストする {#step-4-test-your-data}

データがレプリケートされたら、そのデータに対して読み取り専用クエリを実行して検証できます。詳細については、[アプリケーションをテストしてください](#test-your-application)を参照してください。

### ステップ5．切り替える {#step-5-switch-over}

TiDBに切り替えるには、以下の手順を実行する必要があります。

1.  アプリケーションを停止してください。
2.  レプリケーション遅延を監視してください。遅延時間は0秒になるはずです。
3.  アプリケーションの設定を変更してTiDBに接続するようにし、再度起動してください。

レプリケーションの遅延を確認するには、 `dmctl`を介して[`query-status &#x3C;taskname>`](/dm/dm-query-status.md#detailed-query-result)を実行し、 `"synced: true"`内の`subTaskStatus`を確認します。

### ステップ6．片付け {#step-6-clean-up}

移行が成功したことを確認したら、MariaDB のデータの最終バックアップを作成し、サーバーを停止できます。これにより、DM クラスターを停止して削除することもできます。

## 輸出ユーザーと助成金 {#export-users-and-grants}

[`pt-show-grants`](https://docs.percona.com/percona-toolkit/pt-show-grants.html)を使用できます。これは Percona Toolkit の一部で、MariaDB からユーザーと権限をエクスポートし、TiDB にロードするために使用されます。

## アプリケーションをテストしてください {#test-your-application}

`sysbench`のような汎用ツールを使ってテストすることも可能ですが、アプリケーションの特定の機能をテストすることを強くお勧めします。例えば、アプリケーションのコピーを、データの一時コピーとともにTiDBクラスタに対して実行してみてください。

このようなテストを行うことで、アプリケーションとTiDBの互換性およびパフォーマンスが検証されます。アプリケーションとTiDBのログファイルを監視して、対処が必要な警告がないか確認する必要があります。アプリケーションで使用しているデータベースドライバ（例えば、 Javaベースのアプリケーションの場合はMySQL Connector/J）がテストされていることを確認してください。必要に応じて、JMeterなどのアプリケーションを使用してアプリケーションに負荷をかけることもできます。

## データの検証 {#validate-data}

[sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)を使用して、MariaDB と TiDB のデータが同一で​​あるかどうかを検証できます。
