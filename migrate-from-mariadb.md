---
title: Migrate Data from MariaDB to TiDB
summary: MariaDBからTiDBへのデータ移行には、DumplingとTiDB Lightningを使用する方法やDMを使用してデータをレプリケートする方法があります。移行前に互換性を確認し、ユーザーアカウントと権限を移行します。移行後はアプリケーションを再構成し、データをテストして検証します。同期差分インスペクターを使用してデータの一貫性を確認します。
---

# MariaDB から TiDB へのデータの移行 {#migrate-data-from-mariadb-to-tidb}

このドキュメントでは、MariaDBサーバーインストールから TiDB クラスターにデータを移行する方法について説明します。

## 前提条件 {#prerequisites}

適切な移行戦略を選択してください。

-   最初の戦略は[Dumplingでデータをダンプし、 TiDB Lightningでデータを復元する](#dump-data-with-dumpling-and-restore-data-with-tidb-lightning)です。これは MariaDB のすべてのバージョンで機能します。この戦略の欠点は、より多くのダウンタイムが必要になることです。
-   2 番目の戦略は、 [DMを使用してデータをレプリケートする](#replicate-data-with-dm) DM を使用して MariaDB から TiDB に移行することです。 DM は MariaDB のすべてのバージョンをサポートしているわけではありません。サポートされているバージョンは[DM互換性カタログ](/dm/dm-compatibility-catalog.md#compatibility-catalog-of-tidb-data-migration)にリストされています。

これら 2 つの戦略以外にも、状況に応じて利用できる他の戦略がある可能性があります。例えば：

-   オブジェクト リレーショナル マッピング (ORM) の機能を使用して、データを再展開および移行します。
-   移行の進行中に、MariaDB と TiDB の両方から書き込むようにアプリケーションを変更します。

このドキュメントでは、最初の 2 つの戦略のみを説明します。

選択した戦略に基づいて以下を準備します。

-   **ダンプと復元の**戦略については、次のとおりです。
    -   [Dumpling](/dumpling-overview.md)と[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)をインストールします。
    -   データをエクスポートするには、 Dumpling用の MariaDBサーバー上に[必要な権限](/dumpling-overview.md#required-privileges)あることを確認してください。
-   **データ複製**戦略については、 [データ移行 (DM)](/dm/dm-overview.md)を設定します。

## 互換性を確認する {#check-compatibility}

TiDB は[MySQLと互換性がある](/mysql-compatibility.md)であり、MySQL と MariaDB には多くの共通機能があります。ただし、TiDB と互換性のない MariaDB 固有の機能が存在する可能性があるため、移行前に注意しておく必要があります。

このセクションの項目を確認するだけでなく、MariaDB ドキュメントの[互換性と相違点](https://mariadb.com/kb/en/compatibility-differences/)も確認することをお勧めします。

### 認証 {#authentication}

[MySQL とのSecurity互換性](/security-compatibility-with-mysql.md)文書には、TiDB がサポートする認証方法がリストされています。 TiDB は、MariaDB のいくつかの認証方法をサポートしていません。これは、アカウントの新しいパスワード ハッシュを作成するか、他の特定の措置を講じる必要がある可能性があることを意味します。

どの認証方法が使用されているかを確認するには、次のステートメントを実行します。

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

### システムのバージョン管理されたテーブル {#system-versioned-tables}

TiDB は[システムのバージョン管理されたテーブル](https://mariadb.com/kb/en/system-versioned-tables/)をサポートしていません。ただし、TiDB は[`AS OF TIMESTAMP`](/as-of-timestamp.md)をサポートしており、システム バージョン管理テーブルの使用例の一部を置き換える可能性があります。

次のステートメントを使用して、影響を受けるテーブルを確認できます。

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

MariaDB と TiDB は両方とも[`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)をサポートします。ただし、現在 DM ではサポートされていません。移行中はシーケンスを作成、変更、または削除せず、特に移行後にこれをテストすることをお勧めします。

シーケンスを使用しているかどうかを確認するには、次のステートメントを実行します。

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

MariaDB は、 `InnoDB` 、 `MyISAM` 、 `Aria`などのローカル データ用のstorageエンジンを提供します。データ形式は TiDB によって直接サポートされていませんが、これらの移行は問題なく機能します。ただし、 `CONNECT`storageエンジンや`Spider`など、一部のエンジンはサーバーの外部にデータを配置します。このようなテーブルを TiDB に移行することはできますが、TiDB には TiDB クラスターの外部にデータを保存する機能がありません。

使用しているstorageエンジンを確認するには、次のステートメントを実行します。

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

MariaDB は、 `DELETE` 、 `INSERT` 、および`REPLACE`ステートメントの`RETURNING`キーワードをサポートします。 TiDB はそれらをサポートしていません。アプリケーションを調べてログをクエリし、それが移行に影響を与えるかどうかを確認してください。

### データ型 {#data-types}

MariaDB は、TiDB がサポートしていない一部のデータ型 ( `UUID` 、 `INET4` 、および`INET6`など) をサポートします。

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

TiDB がサポートする照合順序を確認するには、TiDB で次のステートメントを実行します。

```sql
SHOW COLLATION;
```

```sql
+--------------------+---------+-----+---------+----------+---------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen |
+--------------------+---------+-----+---------+----------+---------+
| ascii_bin          | ascii   |  65 | Yes     | Yes      |       1 |
| binary             | binary  |  63 | Yes     | Yes      |       1 |
| gbk_bin            | gbk     |  87 |         | Yes      |       1 |
| gbk_chinese_ci     | gbk     |  28 | Yes     | Yes      |       1 |
| latin1_bin         | latin1  |  47 | Yes     | Yes      |       1 |
| utf8_bin           | utf8    |  83 | Yes     | Yes      |       1 |
| utf8_general_ci    | utf8    |  33 |         | Yes      |       1 |
| utf8_unicode_ci    | utf8    | 192 |         | Yes      |       1 |
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       1 |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       1 |
+--------------------+---------+-----+---------+----------+---------+
13 rows in set (0.0012 sec)
```

現在のテーブルの列が使用している照合順序を確認するには、次のステートメントを使用できます。

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

## Dumplingでデータをダンプし、 TiDB Lightningでデータを復元する {#dump-data-with-dumpling-and-restore-data-with-tidb-lightning}

この方法は、アプリケーションをオフラインにしてデータを移行し、移行されたデータを使用するようにアプリケーションを再構成することを前提としています。

> **注記：**
>
> これを本番で実行する前に、まずアプリケーションのテスト インスタンスまたは開発インスタンスでこれを実行することを強くお勧めします。これは、互換性の問題の可能性を確認することと、移行にかかる時間を把握することの両方を目的としています。

MariaDB から TiDB にデータを移行するには、次の手順を実行します。

1.  アプリケーションを停止します。アプリケーションをオフラインにします。これにより、移行中または移行後に MariaDB 内のデータが変更されないことが保証されます。

2.  [`tiup dumpling`](/dumpling-overview.md#use-dumpling-to-export-data)コマンドで MariaDB にデータをダンプします。

    ```shell
    tiup dumpling --port 3306 --host 127.0.0.1 --user root --password secret -F 256MB  -o /data/backup
    ```

3.  `tiup tidb-lightning`コマンドを使用してデータを復元します。 TiDB Lightningの構成方法と実行方法の詳細については、 [TiDB Lightningを始めましょう](/get-started-with-tidb-lightning.md)を参照してください。

4.  ユーザーアカウントと権限を移行します。ユーザーと権限を移行する方法の詳細については、 [ユーザーと許可をエクスポートする](#export-users-and-grants)を参照してください。

5.  アプリケーションを再構成します。 TiDBサーバーに接続できるようにアプリケーション構成を変更する必要があります。

6.  掃除。移行が成功したことを確認したら、MariaDB 内のデータの最終バックアップを作成し、サーバーを停止できます。これは、 TiUP、 Dumpling、 TiDB Lightningなどのツールを削除できることも意味します。

## DMを使用してデータをレプリケートする {#replicate-data-with-dm}

この方法は、レプリケーションを設定し、アプリケーションを停止してレプリケーションが追いつくのを待ってから、TiDB を使用するようにアプリケーションを再構成することを前提としています。

DM を使用するには、 [TiUPクラスター](/dm/deploy-a-dm-cluster-using-tiup.md)または[TiDB Operator](/tidb-operator-overview.md)を使用して DM サービスのセットをデプロイする必要があります。その後、 `dmctl`使用して DM サービスを構成します。

> **注記：**
>
> これを本番で実行する前に、まずアプリケーションのテスト インスタンスまたは開発インスタンスでこれを実行することを強くお勧めします。これは、互換性の問題の可能性を確認することと、移行にかかる時間を把握することの両方を目的としています。

### ステップ 1. 準備する {#step-1-prepare}

MariaDB でバイナリログが有効になっていて、 `binlog_format`が`ROW`に設定されていることを確認してください。 `binlog_annotate_row_events=OFF`と`log_bin_compress=OFF`を設定することも推奨されます。

また、 `SUPER`アクセス許可、または`BINLOG MONITOR`と`REPLICATION MASTER ADMIN`アクセス許可を持つアカウントも必要です。このアカウントには、移行するスキーマに対する読み取り権限も必要です。

`SUPER`権限を持つアカウントを使用していない場合は、TiDB が MariaDB 固有の権限を確認する方法をまだ認識していないため、DM 構成に次の内容を追加する必要がある場合があります。

```yaml
ignore-checking-items: ["replication_privilege"]
```

DM を使用してアップストリームからダウンストリームにデータを移行する前に、事前チェックによりアップストリームのデータベース構成のエラーを検出し、移行がスムーズに行われるようにします。詳細については、 [移行タスクの事前チェック](/dm/dm-precheck.md)を参照してください。

### ステップ 2. データを複製する {#step-2-replicate-data}

[TiDB データ移行のクイック スタート ガイド](/dm/quick-start-with-dm.md)に従って、MariaDB から TiDB にデータをレプリケートします。

MariaDB から MariaDB へのレプリケーションの場合のように、最初に初期データをコピーする必要はなく、DM がこれを実行します。

### ステップ 3. ユーザーアカウントと権限を移行する {#step-3-migrate-user-accounts-and-permissions}

ユーザーと権限を移行する方法については[ユーザーと許可をエクスポートする](#export-users-and-grants)参照してください。

### ステップ 4. データをテストする {#step-4-test-your-data}

データがレプリケートされたら、そのデータに対して読み取り専用クエリを実行して検証できます。詳細については、 [アプリケーションをテストする](#test-your-application)を参照してください。

### ステップ 5. 切り替え {#step-5-switch-over}

TiDB に切り替えるには、次のことを行う必要があります。

1.  アプリケーションを停止します。
2.  レプリケーション遅延を監視します。遅延は 0 秒になるはずです。
3.  TiDB に接続するようにアプリケーションの構成を変更し、再度起動します。

レプリケーションの遅延を確認するには、 [`query-status &#x3C;taskname>`](/dm/dm-query-status.md#detailed-query-result)から`dmctl`を実行し、 `subTaskStatus`で`"synced: true"`を確認します。

### ステップ6.クリーンアップ {#step-6-clean-up}

移行が成功したことを確認したら、MariaDB 内のデータの最終バックアップを作成し、サーバーを停止できます。これは、DM クラスターを停止して削除できることも意味します。

## ユーザーと許可をエクスポートする {#export-users-and-grants}

[`pt-show-grants`](https://docs.percona.com/percona-toolkit/pt-show-grants.html)を使用できます。これは、MariaDB からユーザーと許可をエクスポートし、これらを TiDB にロードする Percona ツールキットの一部です。

## アプリケーションをテストする {#test-your-application}

`sysbench`などの汎用ツールをテストに使用することもできますが、アプリケーションの特定の機能をテストすることを強くお勧めします。たとえば、データの一時コピーを使用して、アプリケーションのコピーを TiDB クラスターに対して実行します。

このようなテストにより、アプリケーションの TiDB との互換性とパフォーマンスが検証されます。アプリケーションと TiDB のログ ファイルを監視して、対処する必要がある警告があるかどうかを確認する必要があります。アプリケーションが使用しているデータベース ドライバー (たとえば、 Javaベースのアプリケーションの MySQL Connector/J) がテストされていることを確認してください。必要に応じて、JMeter などのアプリケーションを使用して、アプリケーションに負荷をかけることもできます。

## データの検証 {#validate-data}

[同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)使用すると、MariaDB と TiDB のデータが同一で​​あるかどうかを検証できます。
