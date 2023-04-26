---
title: Periodically Delete Data Using TTL (Time to Live)
summary: Time to live (TTL) is a feature that allows you to manage TiDB data lifetime at the row level. In this document, you can learn how to use TTL to automatically expire and delete old data.
---

# TTL (Time to Live) を使用して期限切れのデータを定期的に削除する {#periodically-delete-expired-data-using-ttl-time-to-live}

Time to Live (TTL) は、TiDB データの有効期間を行レベルで管理できるようにする機能です。 TTL 属性を持つテーブルの場合、TiDB はデータの有効期間を自動的にチェックし、期限切れのデータを行レベルで削除します。この機能により、storageスペースを効果的に節約し、一部のシナリオでパフォーマンスを向上させることができます。

次に、TTL の一般的なシナリオをいくつか示します。

-   確認コードと短縮 URL を定期的に削除します。
-   不要な履歴注文を定期的に削除します。
-   計算の中間結果を自動的に削除します。

TTL は、ユーザーがオンラインの読み取りおよび書き込みワークロードに影響を与えることなく、不要なデータを定期的かつタイムリーにクリーンアップできるように設計されています。 TTL は、異なるジョブを異なる TiDB ノードに同時にディスパッチし、テーブル単位でデータを並列に削除します。 TTL は、有効期限が切れたすべてのデータがすぐに削除されることを保証するものではありません。つまり、一部のデータが期限切れになっていても、バックグラウンド TTL ジョブによってそのデータが削除されるまで、有効期限が切れた後もクライアントがそのデータを読み取る可能性があります。

> **警告：**
>
> これは実験的機能です。本番環境で使用することはお勧めしません。 [TiDB CloudServerless Tier](https://docs.pingcap.com/tidbcloud/select-cluster-tier#serverless-tier-beta)は TTL を使用できません。

## 構文 {#syntax}

[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)または[`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)ステートメントを使用して、テーブルの TTL 属性を構成できます。

### TTL 属性を持つテーブルを作成する {#create-a-table-with-a-ttl-attribute}

-   TTL 属性を持つテーブルを作成します。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

    前の例では、テーブル`t1`を作成し、データの作成時刻を示す TTL タイムスタンプ列として`created_at`を指定します。この例では、行がテーブルに存在できる最長期間を 3 か月から`INTERVAL 3 MONTH`に設定しています。この値よりも長く存続するデータは後で削除されます。

-   `TTL_ENABLE`属性を設定して、期限切れデータのクリーンアップ機能を有効または無効にします。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF';
    ```

    `TTL_ENABLE`が`OFF`に設定されている場合、他の TTL オプションが設定されていても、TiDB はこのテーブルの期限切れデータを自動的にクリーンアップしません。 TTL 属性を持つテーブルの場合、 `TTL_ENABLE`はデフォルトで`ON`です。

-   MySQL との互換性を保つために、コメントを使用して TTL 属性を設定できます。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) /*T![ttl] TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF'*/;
    ```

    TiDB では、テーブル TTL 属性を使用するか、コメントを使用して TTL を構成することは同等です。 MySQL ではコメントは無視され、通常のテーブルが作成されます。

### テーブルの TTL 属性を変更する {#modify-the-ttl-attribute-of-a-table}

-   テーブルの TTL 属性を変更します。

    ```sql
    ALTER TABLE t1 TTL = `created_at` + INTERVAL 1 MONTH;
    ```

    前述のステートメントを使用して、既存の TTL 属性を持つテーブルを変更したり、TTL 属性を持たないテーブルに TTL 属性を追加したりできます。

-   TTL 属性を持つテーブルの値を`TTL_ENABLE`に変更します。

    ```sql
    ALTER TABLE t1 TTL_ENABLE = 'OFF';
    ```

-   テーブルのすべての TTL 属性を削除するには:

    ```sql
    ALTER TABLE t1 REMOVE TTL;
    ```

### TTL とデータ型のデフォルト値 {#ttl-and-the-default-values-of-data-types}

TTL は[データ型のデフォルト値](/data-type-default-values.md)と一緒に使用できます。次に、2 つの一般的な使用例を示します。

-   列のデフォルト値を現在の作成時刻として指定し、この列を TTL タイムスタンプ列として使用するには、 `DEFAULT CURRENT_TIMESTAMP`を使用します。 3 か月前に作成されたレコードは期限切れです。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

-   列のデフォルト値を作成時間または最新の更新時間として指定し、この列を TTL タイムスタンプ列として使用します。 3 か月間更新されていないレコードは期限切れになります。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

### TTL および生成列 {#ttl-and-generated-columns}

TTL を[生成された列](/generated-columns.md) (実験的機能) と共に使用して、複雑な有効期限ルールを構成できます。例えば：

```sql
CREATE TABLE message (
    id int PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image bool,
    expire_at TIMESTAMP AS (IF(image,
            created_at + INTERVAL 5 DAY,
            created_at + INTERVAL 30 DAY
    ))
) TTL = `expire_at` + INTERVAL 0 DAY;
```

上記のステートメントは、 `expire_at`列を TTL タイムスタンプ列として使用し、メッセージ タイプに従って有効期限を設定します。メッセージが画像の場合、有効期限は 5 日です。それ以外の場合、有効期限は 30 日です。

[JSON タイプ](/data-type-json.md)とともに TTL を使用できます。例えば：

```sql
CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_info JSON,
    created_at DATE AS (JSON_EXTRACT(order_info, '$.created_at')) VIRTUAL
) TTL = `created_at` + INTERVAL 3 month;
```

## TTL ジョブ {#ttl-job}

TTL 属性を持つテーブルごとに、TiDB は期限切れのデータをクリーンアップするバックグラウンド ジョブを内部的にスケジュールします。 [`tidb_ttl_job_run_interval`](/system-variables.md#tidb_ttl_job_run_interval-new-in-v650)グローバル変数を設定することで、これらのジョブの実行期間をカスタマイズできます。次の例では、バックグラウンド クリーンアップ ジョブを 24 時間ごとに実行するように設定します。

```sql
SET @@global.tidb_ttl_job_run_interval = '24h';
```

TTL ジョブの実行を無効にするには、 `TTL_ENABLE='OFF'`テーブル オプションを設定するだけでなく、 [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650)グローバル変数を設定してクラスター全体で TTL ジョブの実行を無効にすることもできます。

```sql
SET @@global.tidb_ttl_job_enable = OFF;
```

シナリオによっては、特定の時間枠でのみ TTL ジョブの実行を許可したい場合があります。この場合、 [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650)と[`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650)グローバル変数を設定して時間枠を指定できます。例えば：

```sql
SET @@global.tidb_ttl_job_schedule_window_start_time = '01:00 +0000';
SET @@global.tidb_ttl_job_schedule_window_end_time = '05:00 +0000';
```

上記のステートメントでは、TTL ジョブを UTC の 1:00 から 5:00 の間でのみスケジュールできます。デフォルトでは、時間枠は`00:00 +0000`から`23:59 +0000`に設定されており、ジョブをいつでもスケジュールできます。

## 指標とグラフの監視 {#monitoring-metrics-and-charts}

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> このセクションは、オンプレミスの TiDB にのみ適用されます。現在、 TiDB Cloud はTTL メトリックを提供していません。

</CustomContent>

TiDB は TTL に関するランタイム情報を定期的に収集し、Grafana でこれらのメトリックの視覚化されたグラフを提供します。これらのメトリックは、Grafana の TiDB -&gt; TTL パネルで確認できます。

<CustomContent platform="tidb">

メトリックの詳細については、 [TiDB 監視指標](/grafana-tidb-dashboard.md)の TTL セクションを参照してください。

</CustomContent>

## TiDB ツールとの互換性 {#compatibility-with-tidb-tools}

実験的機能として、TTL 機能はBR、 TiDB Lightning、TiCDC などのデータのインポートおよびエクスポート ツールと互換性がありません。

## 制限事項 {#limitations}

現在、TTL 機能には次の制限があります。

-   TTL 属性は、ローカル一時テーブルおよびグローバル一時テーブルを含む一時テーブルには設定できません。
-   TTL 属性を持つテーブルは、外部キー制約のプライマリ テーブルとして他のテーブルから参照されることをサポートしていません。
-   期限切れのデータがすべてすぐに削除されることは保証されていません。期限切れのデータが削除される時間は、バックグラウンド クリーンアップ ジョブのスケジュール間隔とスケジュール ウィンドウによって異なります。
-   現在、1 つのテーブルは、特定の時間に 1 つの TiDB ノードでのみクリーンアップ ジョブを実行できます。これは、一部のシナリオ (たとえば、テーブルが非常に大きい場合) でパフォーマンスのボトルネックを引き起こす可能性があります。この問題は、将来のリリースで最適化される予定です。
