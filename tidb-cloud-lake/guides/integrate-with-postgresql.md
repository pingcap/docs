---
title: PostgreSQL Integration Task
summary: このページでは、PostgreSQL データベースから {{{ .lake }}} にデータを同期する PostgreSQL integration task を作成する方法について説明します。
---

# PostgreSQL Integration Task

このページでは、PostgreSQL データベースから {{{ .lake }}} にデータを同期する PostgreSQL integration task を作成する方法について説明します。PostgreSQL タスクは、完全な `Snapshot` ロード (load)、継続的な `Change Data Capture (CDC)`、またはその両方の組み合わせをサポートします。

まず再利用可能な PostgreSQL 接続設定を作成する必要がある場合は、[PostgreSQL - Credentials](/tidb-cloud-lake/guides/postgresql-credentials.md) を参照してください。

## Sync Modes {#sync-modes}

| Sync Mode      | 説明                                                                                                  |
|----------------|-------------------------------------------------------------------------------------------------------|
| Snapshot       | ソーステーブルから 1 回限りの完全なデータロードを実行します。初期データ移行や定期的な一括インポートに最適です。 |
| CDC Only       | PostgreSQL の logical replication を使用して、リアルタイムの変更（insert、update、delete）を継続的に取得します。マージ操作には primary key が必要です。 |
| Snapshot + CDC | 最初に完全な snapshot を実行し、その後シームレスに継続的な CDC に移行します。ほとんどのユースケースで推奨されます。 |

## Prerequisites {#prerequisites}

PostgreSQL データ統合を設定する前に、PostgreSQL インスタンスが次の要件を満たしていることを確認してください。

- **PostgreSQL - Credentials** データソースがすでに作成されていること
- 対象の PostgreSQL インスタンスに {{{ .lake }}} から到達できること
- PostgreSQL バージョン 10 以降

### Enable Logical Replication {#enable-logical-replication}

CDC および Snapshot + CDC モードでは、PostgreSQL WAL (Write-Ahead Log) を logical レベルで設定する必要があります。

```ini title='postgresql.conf'
wal_level = logical
max_replication_slots = 4
max_wal_senders = 4
```

設定を変更した後、変更を有効にするために PostgreSQL を再起動してください。

### Create a Dedicated User (Recommended) {#create-a-dedicated-user-recommended}

データレプリケーションに必要な権限を持つ PostgreSQL ユーザーを作成します。

```sql
CREATE USER lake_cdc WITH PASSWORD 'your_password' REPLICATION;
GRANT CONNECT ON DATABASE your_database TO lake_cdc;
GRANT USAGE ON SCHEMA public TO lake_cdc;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO lake_cdc;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO lake_cdc;
```

### Create Publication and Replication Slot (Required for CDC) {#create-publication-and-replication-slot-required-for-cdc}

CDC および Snapshot + CDC モードでは、publication と replication slot が存在している必要があります。`CREATE PUBLICATION ... FOR ALL TABLES` には superuser 権限が必要であり、個別のテーブルを追加するにはテーブル所有者である必要があるため、これらのオブジェクトは CDC タスクを開始する前にデータベース所有者または superuser が作成する必要があります。

次のコマンドを superuser またはデータベース所有者として実行してください。

```sql
-- Create a publication that includes the tables you want to replicate
CREATE PUBLICATION bend_cdc_pub FOR ALL TABLES;

-- Create a logical replication slot
SELECT * FROM pg_create_logical_replication_slot('bend_cdc_slot', 'pgoutput');

-- Grant the dedicated user permission to use the replication slot
ALTER ROLE lake_cdc WITH REPLICATION;
```

> **Note:**
>
> すべてのテーブルではなく特定のテーブルのみをレプリケートする必要がある場合は、次を使用できます。
>
> ```sql
> CREATE PUBLICATION bend_cdc_pub FOR TABLE table1, table2;
> ```
>
> これにより superuser 要件は回避できますが、列挙したテーブルの所有権は引き続き必要です。

### Network Access {#network-access}

PostgreSQL インスタンスに {{{ .lake }}} からアクセスできることを確認してください。ファイアウォールルールと security group を確認し、PostgreSQL ポートへの inbound 接続を許可してください。

## Creating a PostgreSQL Integration Task {#creating-a-postgresql-integration-task}

### Step 1: Basic Info {#step-1-basic-info}

1. **Data** > **Data Integration** に移動し、**Create Task** をクリックします。

2. 基本設定を構成します。

    | フィールド                 | 必須    | 説明                                                                                      |
    |----------------------------|-------------|-------------------------------------------------------------------------------------------|
    | **Data Source**             | はい         | ドロップダウンから既存の **PostgreSQL - Credentials** データソースを選択します                    |
    | **Name**                   | はい         | この integration task の名前                                                                 |
    | **Source Database**        | —           | 選択したデータソースに基づいて自動的に表示されます                                        |
    | **Source Table**           | はい         | PostgreSQL データベースから同期するテーブルを選択します                                            |
    | **Sync Mode**             | はい         | **Snapshot**、**CDC Only**、**Snapshot + CDC** から選択します                                    |
    | **Primary Key**          | 条件付き | マージ操作に使用する一意識別カラムです。CDC Only および Snapshot + CDC モードで必須です |
    | **Sync Interval**        | はい         | 書き込み操作の間隔（秒）（デフォルト: 3）                                      |
    | **Batch Size**            | いいえ          | バッチごとの行数                                                                         |
    | **Allow Delete**          | いいえ          | CDC で DELETE 操作を許可するかどうかを指定します。CDC Only および Snapshot + CDC モードで使用できます       |

#### Snapshot Mode Options {#snapshot-mode-options}

**Snapshot** モードを使用する場合は、追加のオプションを利用できます。

- **Snapshot WHERE Condition**: snapshot 中にデータをフィルタリングする SQL WHERE 句です（例: `created_at > '2024-01-01'`）。これにより、ソースデータの一部のみをロードできます。

### Step 2: Preview Data {#step-2-preview-data}

基本設定を構成した後、**Next** をクリックしてソースデータをプレビューします。

システムは選択した PostgreSQL テーブルからサンプル行を取得し、カラム名とデータ型を表示します。続行する前に、正しいテーブルとカラムが選択されていることを確認してください。

### Step 3: Set Target Table {#step-3-set-target-table}

{{{ .lake }}} 内の宛先を構成します。

| フィールド          | 説明                                                        |
|---------------------|-------------------------------------------------------------|
| **Warehouse**       | 同期の実行先となる {{{ .lake }}} Warehouse を選択します    |
| **Target Database** | {{{ .lake }}} 内の対象データベースを選択します                             |
| **Target Table**    | {{{ .lake }}} 内のテーブル名です（デフォルトはソーステーブル名）     |

システムはソースカラムをターゲットテーブルスキーマに自動的にマッピングします。カラムマッピングを確認し、**Create** をクリックして integration task の作成を完了します。

## Task Behavior by Sync Mode {#task-behavior-by-sync-mode}

| Sync Mode      | 動作                                                                                          |
|----------------|-----------------------------------------------------------------------------------------------|
| Snapshot       | 1 回実行され、完全なデータロードが完了すると自動的に停止します。                           |
| CDC Only       | 手動で停止するまで継続的に実行され、リアルタイムの変更を取得します。                            |
| Snapshot + CDC | 最初に初期 snapshot を完了し、その後、手動で停止するまで継続的な CDC に移行します。   |

CDC タスクでは、停止時に現在の LSN (Log Sequence Number) がチェックポイントとして保存されるため、再起動時に中断した位置からタスクを再開できます。

## Sync Mode Details {#sync-mode-details}

### Snapshot {#snapshot}

Snapshot モードでは、ソーステーブルを 1 回だけ完全に読み取り、すべてのデータを {{{ .lake }}} 内のターゲットテーブルにロードします。

**Use cases:**

- PostgreSQL から {{{ .lake }}} への初期データ移行
- 定期的な完全データ更新
- WHERE 条件フィルタリングを使用した 1 回限りのデータインポート

**Features:**

- WHERE 条件フィルタリングをサポートし、データの一部をロード可能
- 完了後にタスクは自動的に停止

### CDC (Change Data Capture) {#cdc-change-data-capture}

CDC モードでは、logical replication を介して PostgreSQL WAL (Write-Ahead Log) を継続的に監視し、ソーステーブルのリアルタイムな行レベル変更（INSERT、UPDATE、DELETE）を取得します。

**Use cases:**

- リアルタイムデータレプリケーション
- 運用中の PostgreSQL データベースと {{{ .lake }}} の同期維持
- イベント駆動型データパイプライン

**How it works:**

1. logical replication slot を使用して PostgreSQL に接続します
2. `pgoutput` プラグインを介してリアルタイムに行レベルの変更を取得します
3. 変更を {{{ .lake }}} 内の raw staging table に書き込みます
4. primary key を使用して、変更を定期的にターゲットテーブルへマージします
5. クラッシュリカバリのためにチェックポイント（LSN 位置）を保存します

> **Note:**
>
> CDC モードでは、PostgreSQL WAL レベルを `logical` に設定する必要があり、primary key（一意カラム）を指定する必要があります。PostgreSQL ユーザーには `REPLICATION` 権限が必要です。

### Snapshot + CDC {#snapshot-cdc}

このモードは両方のアプローチを組み合わせたものです。最初にソーステーブルの完全な snapshot を実行し、その後シームレスに CDC モードへ移行して継続的に変更を取得します。これはほとんどのデータ統合シナリオで推奨されるモードであり、完全な初期データロードと、その後の継続的なリアルタイム同期を実現します。

## Advanced Configuration {#advanced-configuration}

### Primary Key {#primary-key}

Primary key は、CDC 中の MERGE 操作に使用される一意識別カラムを指定します。変更イベントが取得されると、{{{ .lake }}} はこのキーを使用して、新しい行を挿入するか既存の行を更新するかを判断します。通常は、ソーステーブルの primary key を指定します。

### Sync Interval {#sync-interval}

同期間隔（秒）は、取得した変更をターゲットテーブルにどのくらいの頻度でマージするかを制御します。間隔を短くするとレイテンシーは低くなりますが、リソース使用量が増える可能性があります。デフォルト値の 3 秒は、ほとんどのワークロードに適しています。

### Batch Size {#batch-size}

データロード中にバッチごとに処理する行数を制御します。この値を調整することで、大きなテーブルに対するスループットを最適化できます。システムデフォルトを使用する場合は空欄のままにしてください。

### Allow Delete {#allow-delete}

有効にすると（CDC モードのデフォルト）、PostgreSQL WAL から取得した DELETE 操作が {{{ .lake }}} 内のターゲットテーブルに適用されます。無効にすると、削除は無視され、ターゲットテーブルにはすべての履歴レコードが保持されます。これは、完全な監査証跡を維持したいシナリオで役立ちます。