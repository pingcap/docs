---
title: Kafka Consumer Integration Task (Preview)
summary: Kafka トピックからメッセージを継続的に消費し、メッセージ内容を内部オブジェクトストレージ（tenant Stage）に保存する Kafka Consumer タスクを作成します。
---

# Kafka Consumer Integration Task (Preview)

このページでは、Kafka トピックからメッセージを継続的に消費し、メッセージ内容を内部オブジェクトストレージ（tenant Stage）に保存する Kafka Consumer タスクの作成方法について説明します。

S3、MySQL、PostgreSQL のデータ統合タスクとは異なり、Kafka Consumer タスクは通常のターゲットテーブルに直接書き込みません。タスクを作成して開始した後、`@kafka_consumer/<task_name>/` の stage パスを使用して保存されたメッセージオブジェクトを確認し、SQL でその内容をクエリできます。

先に再利用可能な Kafka 接続設定を作成する必要がある場合は、[Kafka - Credentials（プレビュー）](/tidb-cloud-lake/guides/kafka-credentials.md) を参照してください。

## ユースケース {#use-cases}

- Kafka トピックから JSON メッセージを継続的に取り込み
- まず Kafka メッセージを内部オブジェクトストレージに保存し、その後 SQL でクエリまたは処理
- リアルタイムまたはニアリアルタイムのデータパイプライン向けに、生の Kafka メッセージオブジェクトを保持

## ワークフロー {#workflow}

1. 上流システムが Kafka トピックにメッセージを書き込みます。
2. Kafka Consumer タスクが指定されたトピックからメッセージを読み取ります。
3. タスクはメッセージをバッチ単位で内部オブジェクトストレージ（tenant Stage）に保存します。
4. ユーザーは `@kafka_consumer/<task_name>/` を通じて生成されたオブジェクトを確認します。
5. ユーザーは stage からメッセージ内容をクエリし、必要に応じて後続のロード (load) や変換を実行します。

> **Note:**
>
> Kafka Consumer タスクは、Kafka メッセージ内容を含むオブジェクトファイルを保存します。メッセージを業務テーブルに書き込む必要がある場合は、stage のクエリ結果に基づいて、後続の `INSERT INTO ... SELECT`、`COPY INTO`、またはその他の処理を実行してください。

## 前提条件 {#prerequisites}

Kafka Consumer タスクを作成する前に、以下を確認してください。

- **Kafka - Credentials** データソースがすでに作成されている
- プラットフォームがネットワーク経由で Kafka ブローカーにアクセスできる
- Kafka データソース内の認証方式、TLS 設定、およびアカウント情報が正しい
- Kafka ユーザーに対象トピックの読み取り権限がある
- 対象トピック内のメッセージが、タスクで選択した **Data Format** と一致している

## Kafka Consumer タスクの作成 {#creating-a-kafka-consumer-task}

### ステップ 1: 基本情報 {#step-1-basic-info}

1. **Data** > **Data Integration** に移動し、**Create Task** をクリックします。
2. Kafka データソースを選択し、基本パラメータを設定します。

    | フィールド | 必須 | 説明 |
    |-------|----------|-------------|
    | **Data Source** | はい | ドロップダウンから既存の **Kafka - Credentials** データソースを選択します |
    | **Name** | はい | Kafka Consumer タスクの名前 |
    | **Topics** | はい | 消費する Kafka トピック。複数のトピックはカンマで区切ります。例: `topic-1,topic-2` |
    | **Data Format** | はい | Kafka メッセージのデータ形式。現在は **JSON** のみです |
    | **Start Position** | はい | コミット済みオフセットが存在しない場合の開始位置。**Latest** と **Earliest** をサポートします |
    | **Max Batch Bytes** | いいえ | バッチごとの最大データサイズ。デフォルト値は **16 MiB** です |
    | **Max Batch Wait Interval** | いいえ | バッチごとの最大待機時間。デフォルト値は **1 Minute** です |

    > **Note:**
    >
    > **Latest** は新しいメッセージのみを消費し、**Earliest** は Kafka に保持されている最も古いメッセージから開始します。この設定は、Consumer Group にコミット済みオフセットがない場合にのみ適用され、既存のオフセットはリセットしません。

### ステップ 2: データのプレビュー {#step-2-preview-data}

基本設定の完了後、**Next** をクリックして **Preview Data Info** に進みます。

システムは、指定された Kafka トピックからサンプルメッセージの読み取りを試みます。メッセージが利用可能な場合、ページには 1 ～ 2 件の JSON メッセージが表示されるため、トピック、データ形式、およびメッセージ構造を確認できます。

プレビュー可能なメッセージがない場合、ページには **No sample data available** と表示されます。そのままタスクの作成を続行できますが、トピックにすでにメッセージが含まれているか、および選択した **Start Position** でサンプルデータを読み取れるかを確認することを推奨します。

### ステップ 3: 結果の確認 {#step-3-result-viewing}

**Result Viewing** ステップで、Kafka Consumer タスクを実行する **Warehouse** を選択します。

タスクの開始後、Kafka メッセージを読み取り、それらを内部オブジェクトストレージ（tenant Stage）に保存します。ページには SQL の例が表示されます。`LIST @kafka_consumer/<task_name>/` を使用して生成されたオブジェクトを確認し、stage クエリを使用してメッセージ内容を読み取ることができます。

```sql
-- List stage objects:
LIST @kafka_consumer/<task_name>/;

-- Query object data (replace with the correct PATTERN path):
SELECT $1
FROM @kafka_consumer (
    FILE_FORMAT=>'ndjson',
    PATTERN=>'<task_name>/year=YYYY/month=MM/day=DD/hour=HH/.*[.]ndjson'
);
```

**Create** をクリックしてタスクを作成します。

## タスクの動作 {#task-behavior}

Kafka Consumer タスクは継続的に実行されます。開始後、指定されたトピックからメッセージを消費し、手動で停止するまで、それらをバッチ単位で内部オブジェクトストレージ内のオブジェクトファイルとして保存します。

| シナリオ | 動作 |
|----------|----------|
| トピックに新しいメッセージが存在する | メッセージを読み取り、tenant Stage に書き込みます |
| バッチサイズが **Max Batch Bytes** に達する | 現在のバッチをオブジェクトストレージに書き込みます |
| 待機時間が **Max Batch Wait Interval** に達する | バッチがサイズ上限に達していなくても、現在のバッチをオブジェクトストレージに書き込みます |
| 書き込み操作が成功する | 後で継続できるように消費の進行状況を保存します |
| タスクを手動で停止する | 消費を停止し、保存済みのメッセージオブジェクトは保持します |

## 保存されたメッセージのクエリ {#query-saved-messages}

Kafka Consumer タスクは、`@kafka_consumer/<task_name>/` パス配下にメッセージオブジェクトを保存します。タスクが開始されてオブジェクトが書き込まれた後、タスク詳細ページを開き、**Data Browsing** タブに切り替えると、UTC 時間単位でオブジェクト数とオブジェクト一覧を確認できます。

SQL を使用して最初にオブジェクトを一覧表示し、その後、実際のパスに基づいて内容をクエリすることもできます。

```sql
LIST @kafka_consumer/<task_name>/;
```

```sql
SELECT $1
FROM @kafka_consumer (
    FILE_FORMAT=>'ndjson',
    PATTERN=>'<task_name>/year=YYYY/month=MM/day=DD/hour=HH/.*[.]ndjson'
);
```

メッセージを業務テーブルに書き込む必要がある場合は、クエリ結果に基づいて後続の変換またはロードを続行してください。

## 高度な設定 {#advanced-configuration}

### Runtime Size {#runtime-size}

Kafka Consumer タスクでは Runtime Size の変更をサポートしています。Runtime Size を変更する前にタスクを停止し、**Edit** メニューから編集ページを開き、**Runtime Size** セクションで適切なランタイムサイズを選択して変更を保存してください。タスクを再起動すると、新しいランタイムサイズで実行されます。

> **Note:**
>
> 利用可能なランタイムサイズと価格は、課金プランによって異なります。コンソールに表示されるオプションと料金ドキュメントを正しい情報源として使用してください。