---
title: TiDB Integration Task (Preview)
summary: フル Snapshot ロード、継続的な CDC、またはその両方を使用して、TiDB クラスターから TiDB Cloud Lake にデータをレプリケートします。
---

# TiDB Integration Task (Preview)

TiDB integration task は、TiDB クラスターから TiDB Cloud Lake にデータをレプリケートします。Dumpling エクスポートからのフル `Snapshot` ロード、TiCDC changefeed からの継続的な `Change Data Capture (CDC)`、またはその両方の組み合わせをサポートします。

再利用可能なステージング用バケット設定を先に作成する必要がある場合は、[TiDB データソース](/tidb-cloud-lake/guides/tidb-data-source.md) を参照してください。

## ユースケース {#use-cases}

- 分析のために TiDB データベースとテーブルを TiDB Cloud Lake に移行する
- TiCDC を通じて TiDB Cloud Lake を TiDB と継続的に同期させる
- シャーディングされたデータベースを、1 つのタスク内でソースごとのターゲットデータベースに統合する
- フルロード (load) を 1 回だけ実行する、またはフルロードと継続的な変更キャプチャを組み合わせる

## 同期モード {#sync-modes}

| 同期モード | 説明 |
|-----------|-------------|
| Snapshot | Dumpling エクスポートから 1 回限りのフルデータロードを実行します。初期移行や定期的な一括更新に最適です。 |
| CDC Only | TiCDC changefeed を継続的に消費し、リアルタイムの変更（挿入、更新、削除）を適用します。 |
| Snapshot + CDC | 最初にフルスナップショットを実行し、その後継続的な CDC に移行します。ほとんどのユースケースで推奨されます。 |

## 前提条件 {#prerequisites}

TiDB integration task を作成する前に、以下を確認してください。

- **TiDB** データソースがすでに作成されていること。
- データソースで設定したオブジェクトストレージのバケットに、TiDB Cloud Lake から到達できること。
- 同期したいテーブルの TiCDC / Dumpling エクスポートが、タスクで参照するプレフィックス配下のバケットに書き込まれていること。

## TiDB Integration Task の作成 {#creating-a-tidb-integration-task}

このセクションでは、TiDB Cloud Lake で TiDB integration task を作成する手順を説明します。

### Step 1: 基本設定を構成する {#step-1-configure-basic-settings}

1. **Data** > **Data Integration** に移動し、**Create Task** をクリックします。
2. **TiDB** データソースを選択し、基本設定を構成します。

| フィールド | 必須 | 説明 |
|-------|----------|-------------|
| **Data Source** | はい | 既存の **TiDB - Credentials** データソースを選択します。ここから新規作成することもできます |
| **Name** | はい | このデータ統合タスクの名前 |
| **Sync Mode** | はい | **Snapshot**、**CDC Only**、または **Snapshot + CDC** を選択します |
| **Table Rules** | はい | 同期するソースオブジェクトを選択するルールです。[Table Rules](#table-rules) を参照してください |
| **Max Matched Tables** | いいえ | ルールが一致できるテーブル数の上限です。空欄のままにすると、システムのデフォルト値 (500) が使用されます |
| **Dumpling S3 Prefix** | はい (Snapshot modes) | Dumpling エクスポートを格納するバケットプレフィックスです。例: `dumpling/export` |
| **Table Parallelism** | いいえ | 同時にロードするテーブル数です（デフォルト: 4） |
| **Warehouse** | はい | タスクの実行に使用する TiDB Cloud Lake Warehouse |

### Table Rules {#table-rules}

1 行に 1 つのルールを入力します。各ルールは `schemaPattern.tablePattern` の形式で、除外する場合は先頭に `!` を付けます。

```text
app.orders             an exact table
shard_*.*              every table of every shard_ database
!*.tmp_*               exclude temporary tables
```

ルールは最後から最初の順に評価されます。データベースパターンとテーブルパターンの両方に最初に一致したルールが結果を決定します。どのルールにも一致しないオブジェクトは除外されます。除外ルールのみを含むリストには、暗黙的に先頭に `*.*` が追加されます。

一致した各ソースデータベースは、それぞれ独自のターゲットデータベースに書き込まれるため、異なるソースデータベース内で同名のテーブルは分離されたままになります。これは、1 つのタスクで複数のソースデータベースを同期する唯一の方法です。

**Preview Matched Tables** をクリックすると、現在のルールを、プレフィックス配下に実際に存在するオブジェクトに対して評価できます。プレビューには、一致したソースデータベースとテーブル、および導出されたターゲットデータベースとテーブルが表示されます。

### Snapshot Options {#snapshot-options}

同期モードにスナップショットが含まれる場合、追加オプションによって Dumpling エクスポートのロード方法を制御できます。

| フィールド                          | デフォルト | 説明                                                                                                              |
| ------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Auto Create Table**          | Yes     | ソーススキーマからターゲットテーブルを自動的に作成します                                                             |
| **Purge After Load**           | No      | ロード成功後にバケットからソースオブジェクトを削除します。削除権限が必要です                                |
| **On Error**                   | Abort   | **Abort** は最初のエラーで停止します。**Continue** は失敗した行をスキップしてロードを継続します                                     |
| **CSV Separator**              | `,`     | Dumpling エクスポートで使用されるフィールド区切り文字                                                                              |
| **Skip Header Rows**           | Yes     | 先頭行にカラム名が含まれているかどうかを指定します。エクスポートにヘッダー行がある場合は **YES** を選択します                             |
| **Export Escaped Backslashes** | No      | Dumpling の `--escape-backslash` 設定と一致している必要があります。 |

### ターゲット名の接頭辞と接尾辞 {#target-name-affixes}

ターゲットのデータベース名とテーブル名は、ソース名から導出され、必要に応じて接頭辞や接尾辞を付けられます。

```text
target database = targetDatabasePrefix + sourceDatabase + targetDatabaseSuffix
target table    = targetTablePrefix    + sourceTable    + targetTableSuffix
```

接頭辞と接尾辞を空のままにすると、ソース名がそのまま使用されます。接頭辞と接尾辞には、英字、数字、アンダースコアのみを使用できます。

たとえば、データベース接頭辞が `src_` の場合、ソースデータベース `shard_1` とテーブル `orders` は `src_shard_1.orders` に書き込まれます。

### Step 2: タスクを作成する {#step-2-create-the-task}

設定を確認し、**Create** をクリックしてデータ統合タスクを作成します。

## 同期モードごとのタスク動作 {#task-behavior-by-sync-mode}

| 同期モード | 動作 |
|-----------|----------|
| Snapshot | 1 回実行され、フルロードの完了後に自動的に停止します。 |
| CDC Only | 手動で停止するまで継続的に実行され、changefeed イベントを消費します。 |
| Snapshot + CDC | 最初にフルスナップショットを完了し、その後、手動で停止するまで継続的な CDC に移行します。 |

CDC タスクでは、進行状況はチェックポイントとして保存されます。タスクを停止して再起動すると、先頭から再ロードするのではなく、保存された位置から再開します。

## 詳細設定 {#advanced-configuration}

以下の設定は、検出、ロード (load)、マージを調整するタスクレベルのパラメーターです。

| パラメータ | デフォルト | 説明 |
|-----------|---------|-------------|
| **Table Parallelism** | 4 | 同時に処理するテーブル数を制御します。値を大きくするとスループットは向上しますが、より多くの Warehouse リソースを消費します。 |
| **Poll Interval** | 60 seconds | 新しい changefeed / エクスポートオブジェクトを検出するために、タスクがステージング用バケットを一覧表示する頻度（およびオプションの SQS キューを消費する頻度）です。間隔を短くするとレイテンシーは低下しますが、その分 list リクエストが増えます。OSS では、検出はポーリングのみを使用します。 |
| **Batch File Count** | 100 | バッチごとに処理する CDC イベントファイルの最大数です。メモリ使用量とスループットのバランスを取るために調整します。 |
| **Merge Interval** | 30 seconds | キャプチャした変更をターゲットテーブルにマージする頻度です。間隔を短くするとレイテンシーは低下しますが、マージ処理は増加します。 |
| **Allow Delete** | Disabled | changefeed からキャプチャされた `DELETE` 操作をターゲットテーブルに適用するかどうかを指定します。無効な場合、削除は無視され、履歴行は保持されます。 |
| **Max Matched Tables** | 500 | ルールが一致できるソーステーブル数の上限です。ルールがこの上限を超えると、該当する一致項目が一覧表示されてタスクは失敗します。 |