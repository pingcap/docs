---
title: MySQL Integration Task
summary: MySQL データ統合を使用すると、MySQL データベースから {{{ .lake }}} にデータをリアルタイムで同期できます。完全なスナップショットのロード、継続的な Change Data Capture (CDC)、またはその両方の組み合わせをサポートしています。
---

# MySQL Integration Task

このページでは、MySQL データベースから {{{ .lake }}} にデータを同期する MySQL integration task を作成する方法について説明します。MySQL タスクは、完全な `Snapshot` ロード、継続的な `Change Data Capture (CDC)`、またはその両方の組み合わせをサポートしています。

再利用可能な MySQL 接続設定を先に作成する必要がある場合は、[MySQL - Credentials](/tidb-cloud-lake/guides/mysql-credentials.md) を参照してください。

## Sync Modes {#sync-modes}

| Sync Mode      | 説明                                                                                                  |
|----------------|-------------------------------------------------------------------------------------------------------|
| Snapshot       | ソーステーブルから一度だけ完全なデータのロードを実行します。初回のデータ移行や定期的な一括インポートに最適です。 |
| CDC Only       | MySQL binlog からリアルタイムの変更（insert、update、delete）を継続的に取得します。マージ操作には主キーが必要です。 |
| Snapshot + CDC | 最初に完全なスナップショットを実行し、その後シームレスに継続的な CDC に移行します。ほとんどのユースケースで推奨されます。 |

## Prerequisites {#prerequisites}

MySQL データ統合を設定する前に、MySQL インスタンスが次の要件を満たしていることを確認してください。

- **MySQL - Credentials** データソースがすでに作成されていること
- 対象の MySQL インスタンスに {{{ .lake }}} から到達できること

### Enable Binlog {#enable-binlog}

すべての同期モードで、MySQL のバイナリログを有効にしてください。**CDC Only** および **Snapshot + CDC** では、バイナリログは `ROW` 形式と `FULL` row image を**必ず**使用する必要があります。

```ini title='my.cnf'
[mysqld]
server-id=1
log-bin=mysql-bin
binlog-format=ROW
binlog-row-image=FULL
```

設定を変更した後、変更を有効にするために MySQL を再起動してください。

### Create a Dedicated User (Recommended) {#create-a-dedicated-user-recommended}

データレプリケーションに必要な権限を持つ MySQL ユーザーを作成します。

```sql
CREATE USER 'lake_cdc'@'%' IDENTIFIED BY 'your_password';
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'lake_cdc'@'%';
FLUSH PRIVILEGES;
```

### Network Access {#network-access}

MySQL インスタンスに {{{ .lake }}} からアクセスできることを確認してください。ファイアウォールルールとセキュリティグループを確認し、MySQL ポートへの受信接続を許可してください。

## Creating a MySQL Integration Task {#creating-a-mysql-integration-task}

### Step 1: Basic Info {#step-1-basic-info}

1. **Data** > **Data Integration** に移動し、**Create Task** をクリックします。

    ![Data Integration Page](/media/tidb-cloud-lake/dataintegration-page-with-create-button.png)

2. 基本設定を構成します。

    | フィールド                  | 必須        | 説明                                                                                      |
    |----------------------------|-------------|-------------------------------------------------------------------------------------------|
    | **Data Source**             | Yes         | ドロップダウンから既存の **MySQL - Credentials** データソースを選択します                         |
    | **Name**                   | Yes         | この integration task の名前                                                                  |
    | **Source Database**        | —           | 選択したデータソースに基づいて自動的に表示されます                                                |
    | **Source Table**           | Yes         | MySQL データベースから同期するテーブルを選択します                                               |
    | **Sync Mode**             | Yes         | **Snapshot**、**CDC Only**、または **Snapshot + CDC** から選択します                           |
    | **Primary Key**          | Conditional | マージ操作に使用する一意識別子カラムです。CDC Only および Snapshot + CDC モードで必須です            |
    | **Sync Interval**        | Yes         | 書き込み操作の間隔（秒）（デフォルト: 3）                                                        |
    | **Batch Size**            | No          | バッチごとの行数                                                                              |
    | **Allow Delete**          | No          | CDC で DELETE 操作を許可するかどうか。CDC Only および Snapshot + CDC モードで使用できます          |

    ![Create Task - Basic Info](/media/tidb-cloud-lake/create-mysql-task-step1-basic-info.png)

#### Snapshot Mode Options {#snapshot-mode-options}

**Snapshot** モードを使用する場合、追加オプションを利用できます。

- **Snapshot WHERE Condition**: スナップショット中にデータをフィルタリングする SQL WHERE 句です（例: `created_at > '2024-01-01'`）。これにより、ソースデータの一部のみをロードできます。

- **Archive Schedule**: 定期アーカイブを有効にすると、繰り返しスケジュールに従ってスナップショットを自動実行できます。有効にすると、次のフィールドが表示されます。

| フィールド         | 説明                                                              |
|---------------------|-------------------------------------------------------------------|
| **Cron Expression** | cron 形式のスケジュール（例: 毎日午前 1:00 に実行する `0 1 * * *`）        |
| **Timezone**        | スケジュールのタイムゾーン（デフォルト: UTC）                                 |
| **Mode**            | アーカイブ頻度 — **Daily**、**Weekly**、または **Monthly**                |
| **Time Column**     | アーカイブのパーティション分割に使用する時間ベースのカラム（例: `created_at`） |

### Step 2: Preview Data {#step-2-preview-data}

基本設定を構成したら、**Next** をクリックしてソースデータをプレビューします。

![Preview Data](/media/tidb-cloud-lake/create-mysql-task-preview-data-step.png)

システムは選択した MySQL テーブルからサンプル行を取得し、カラム名とデータ型を表示します。続行する前に、正しいテーブルとカラムが選択されていることを確認してください。

### Step 3: Set Target Table {#step-3-set-target-table}

{{{ .lake }}} 内の宛先を構成します。

| フィールド         | 説明                                                        |
|---------------------|-------------------------------------------------------------|
| **Warehouse**       | 同期の実行に使用する対象の {{{ .lake }}} Warehouse を選択します    |
| **Target Database** | {{{ .lake }}} 内の対象データベースを選択します                             |
| **Target Table**    | {{{ .lake }}} 内のテーブル名です（デフォルトではソーステーブル名になります）     |

![Set Target Table](/media/tidb-cloud-lake/dataintegration-mysql-set-target-table.png)

システムはソースカラムをターゲットテーブルのスキーマに自動的にマッピングします。カラムマッピングを確認し、**Create** をクリックして integration task の作成を完了します。

## Task Behavior by Sync Mode {#task-behavior-by-sync-mode}

| Sync Mode      | 動作                                                                                          |
|----------------|-----------------------------------------------------------------------------------------------|
| Snapshot       | 一度実行され、完全なデータのロードが完了すると自動的に停止します。                                         |
| CDC Only       | 手動で停止するまで継続的に実行され、リアルタイムの変更を取得します。                                         |
| Snapshot + CDC | 最初に初回スナップショットを完了し、その後、手動で停止するまで継続的な CDC に移行します。                      |

CDC タスクでは、停止時に現在の binlog 位置がチェックポイントとして保存されるため、再起動時に中断した位置から再開できます。

## Sync Mode Details {#sync-mode-details}

### Snapshot {#snapshot}

Snapshot モードでは、ソーステーブルを一度だけ完全に読み取り、すべてのデータを {{{ .lake }}} のターゲットテーブルにロードします。

**Use cases:**

- MySQL から {{{ .lake }}} への初回データ移行
- 定期的な完全データ更新
- WHERE 条件によるフィルタリングを伴う一度限りのデータインポート

**Features:**

- WHERE 条件によるフィルタリングをサポートし、データの一部のみをロード可能
- 繰り返しスナップショットのための定期アーカイブスケジュールをサポート
- タスクは完了後に自動停止

### CDC (Change Data Capture) {#cdc-change-data-capture}

CDC モードでは、MySQL binlog を継続的に監視し、ソーステーブルのリアルタイムな行レベル変更（INSERT、UPDATE、DELETE）を取得します。

**Use cases:**

- リアルタイムデータレプリケーション
- 運用中の MySQL データベースと {{{ .lake }}} の同期維持
- イベント駆動型データパイプライン

**How it works:**

1. 一意の server ID を使用して MySQL binlog に接続します
2. 行レベルの変更をリアルタイムで取得します
3. 変更を {{{ .lake }}} の raw staging table に書き込みます
4. 主キーを使用して変更を定期的にターゲットテーブルへマージします
5. クラッシュリカバリのためにチェックポイント（binlog 位置）を保存します

> **Note:**
>
> CDC モードでは、MySQL binlog を ROW 形式で有効にする必要があり、主キー（一意カラム）を指定する必要があります。MySQL ユーザーには `REPLICATION SLAVE` および `REPLICATION CLIENT` 権限が必要です。

### Snapshot + CDC {#snapshot-cdc}

このモードは両方のアプローチを組み合わせたものです。最初にソーステーブルの完全なスナップショットを実行し、その後シームレスに CDC モードへ移行して継続的に変更を取得します。完全な初期データロードと、その後の継続的なリアルタイム同期を実現できるため、ほとんどのデータ統合シナリオで推奨されるモードです。

## Advanced Configuration {#advanced-configuration}

### Primary Key {#primary-key}

Primary Key は、CDC 中の MERGE 操作に使用される一意識別子カラムを指定します。変更イベントが取得されると、{{{ .lake }}} はこのキーを使用して、新しい行を挿入するか既存の行を更新するかを判断します。通常、これはソーステーブルの主キーである必要があります。

### Sync Interval {#sync-interval}

同期間隔（秒）は、取得した変更をターゲットテーブルにどのくらいの頻度でマージするかを制御します。間隔を短くするとレイテンシーは低くなりますが、リソース使用量が増える可能性があります。デフォルト値の 3 秒は、ほとんどのワークロードに適しています。

### Batch Size {#batch-size}

データロード (load) 中にバッチごとに処理する行数を制御します。この値を調整することで、大きなテーブルに対するスループットの最適化に役立ちます。システムのデフォルト値を使用する場合は空欄のままにしてください。

### Allow Delete {#allow-delete}

有効にすると（CDC モードではデフォルト）、MySQL binlog から取得した DELETE 操作が {{{ .lake }}} のターゲットテーブルに適用されます。無効にすると、削除は無視され、ターゲットテーブルにはすべての履歴レコードが保持されます。これは、完全な監査証跡を管理したいシナリオで役立ちます。

### Archive Schedule {#archive-schedule}

Snapshot モードでは、定期アーカイブを構成して、繰り返しスケジュールに従ってスナップショットを自動実行できます。これは、継続的な CDC のオーバーヘッドなしで定期的なデータ更新が必要なシナリオで役立ちます。

- **Cron Expression**: スケジュール設定用の標準 cron 形式（例: 毎日午前 1:00 に実行する `0 1 * * *`）
- **Mode**: **Daily**、**Weekly**、または **Monthly** のアーカイブを選択します
- **Time Column**: 時間ベースのパーティション分割に使用するカラムを指定します（例: `created_at`）
- **Timezone**: スケジュールのタイムゾーンを設定します（デフォルト: UTC）