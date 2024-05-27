---
title: Periodically Delete Data Using TTL (Time to Live)
summary: Time to Live (TTL) は、行レベルで TiDB データの有効期間を管理できる機能です。このドキュメントでは、TTL を使用して古いデータを自動的に期限切れにして削除する方法について説明します。
---

# TTL (Time to Live) を使用して期限切れのデータを定期的に削除する {#periodically-delete-expired-data-using-ttl-time-to-live}

Time to Live (TTL) は、行レベルで TiDB データの有効期間を管理できる機能です。TTL 属性を持つテーブルの場合、TiDB は自動的にデータの有効期間をチェックし、行レベルで期限切れのデータを削除します。この機能により、一部のシナリオではstorageスペースを効果的に節約し、パフォーマンスを向上させることができます。

TTL の一般的なシナリオを以下に示します。

-   確認コードと短縮 URL を定期的に削除してください。
-   不要な履歴注文を定期的に削除します。
-   計算の中間結果を自動的に削除します。

TTL は、オンラインの読み取りおよび書き込みワークロードに影響を与えることなく、ユーザーが不必要なデータを定期的かつタイムリーにクリーンアップできるように設計されています。TTL は、異なるジョブを異なる TiDB ノードに同時にディスパッチして、テーブル単位でデータを並行して削除します。TTL では、期限切れのデータがすぐに削除されることは保証されません。つまり、一部のデータが期限切れになった場合でも、バックグラウンド TTL ジョブによってそのデータが削除されるまで、クライアントは有効期限が切れてからしばらく経ってからそのデータを読み取る可能性があります。

## 構文 {#syntax}

[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)または[`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)ステートメントを使用して、テーブルの TTL 属性を設定できます。

### TTL属性を持つテーブルを作成する {#create-a-table-with-a-ttl-attribute}

-   TTL 属性を持つテーブルを作成します。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

    前の例では、テーブル`t1`を作成し、データの作成時刻を示す TTL タイムスタンプ列として`created_at`を指定します。また、この例では、行がテーブル内で存続できる最長期間を 3 か月から`INTERVAL 3 MONTH`に設定します。この値よりも長く存続するデータは後で削除されます。

-   期限切れのデータをクリーンアップする機能を有効または無効にするには、 `TTL_ENABLE`属性を設定します。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF';
    ```

    `TTL_ENABLE` `OFF`に設定されている場合、他の TTL オプションが設定されていても、TiDB はこのテーブル内の期限切れデータを自動的にクリーンアップしません。TTL 属性を持つテーブルの場合、デフォルトでは`TTL_ENABLE`が`ON`なります。

-   MySQL との互換性を保つために、コメントを使用して TTL 属性を設定できます。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) /*T![ttl] TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF'*/;
    ```

    TiDB では、テーブル TTL 属性を使用するか、コメントを使用して TTL を構成することは同等です。MySQL では、コメントは無視され、通常のテーブルが作成されます。

### テーブルのTTL属性を変更する {#modify-the-ttl-attribute-of-a-table}

-   テーブルの TTL 属性を変更します。

    ```sql
    ALTER TABLE t1 TTL = `created_at` + INTERVAL 1 MONTH;
    ```

    上記のステートメントを使用して、既存の TTL 属性を持つテーブルを変更したり、TTL 属性のないテーブルに TTL 属性を追加したりできます。

-   TTL 属性を持つテーブルの値を`TTL_ENABLE`に変更します。

    ```sql
    ALTER TABLE t1 TTL_ENABLE = 'OFF';
    ```

-   テーブルのすべての TTL 属性を削除するには:

    ```sql
    ALTER TABLE t1 REMOVE TTL;
    ```

### TTLとデータ型のデフォルト値 {#ttl-and-the-default-values-of-data-types}

TTL は[データ型のデフォルト値](/data-type-default-values.md)と一緒に使用できます。次に、一般的な使用例を 2 つ示します。

-   `DEFAULT CURRENT_TIMESTAMP`使用すると、列のデフォルト値を現在の作成時刻として指定し、この列を TTL タイムスタンプ列として使用します。3 か月前に作成されたレコードは期限切れです。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

-   列のデフォルト値を作成時刻または最終更新時刻として指定し、この列を TTL タイムスタンプ列として使用します。3 か月間更新されていないレコードは期限切れになります。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

### TTLと生成された列 {#ttl-and-generated-columns}

TTL を[生成された列](/generated-columns.md)と組み合わせて使用​​すると、複雑な有効期限ルールを設定できます。例:

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

上記のステートメントは、 `expire_at`列を TTL タイムスタンプ列として使用し、メッセージの種類に応じて有効期限を設定します。メッセージが画像の場合、5 日で有効期限が切れます。それ以外の場合は、30 日で有効期限が切れます。

TTL を[JSON型](/data-type-json.md)と一緒に使用できます。例:

```sql
CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_info JSON,
    created_at DATE AS (JSON_EXTRACT(order_info, '$.created_at')) VIRTUAL
) TTL = `created_at` + INTERVAL 3 month;
```

## TTLジョブ {#ttl-job}

TTL 属性を持つ各テーブルについて、TiDB は期限切れのデータをクリーンアップするためのバックグラウンド ジョブを内部的にスケジュールします。テーブルの`TTL_JOB_INTERVAL`属性を設定することで、これらのジョブの実行期間をカスタマイズできます。次の例では、テーブル`orders`のバックグラウンド クリーンアップ ジョブを 24 時間ごとに 1 回実行するように設定します。

```sql
ALTER TABLE orders TTL_JOB_INTERVAL = '24h';
```

デフォルトでは`TTL_JOB_INTERVAL`は`1h`に設定されています。

TTL ジョブを実行すると、TiDB はテーブルを最大 64 個のタスクに分割します。最小単位はリージョンです。これらのタスクは分散して実行されます。システム変数[`tidb_ttl_running_tasks`](/system-variables.md#tidb_ttl_running_tasks-new-in-v700)を設定することで、クラスター全体で同時実行可能な TTL タスクの数を制限できます。ただし、すべての種類のテーブルのすべての TTL ジョブをタスクに分割できるわけではありません。どの種類のテーブルの TTL ジョブをタスクに分割できないかの詳細については、セクション[制限事項](#limitations)を参照してください。

TTL ジョブの実行を無効にするには、 `TTL_ENABLE='OFF'`テーブル オプションを設定することに加えて、 [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650)グローバル変数を設定してクラスター全体で TTL ジョブの実行を無効にすることもできます。

```sql
SET @@global.tidb_ttl_job_enable = OFF;
```

シナリオによっては、TTL ジョブを特定の時間枠でのみ実行できるようにしたい場合があります。この場合、グローバル変数[`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650)と[`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650)を設定して時間枠を指定できます。例:

```sql
SET @@global.tidb_ttl_job_schedule_window_start_time = '01:00 +0000';
SET @@global.tidb_ttl_job_schedule_window_end_time = '05:00 +0000';
```

上記のステートメントでは、TTL ジョブを UTC の 1:00 から 5:00 の間にのみスケジュールできます。デフォルトでは、時間ウィンドウは`00:00 +0000`から`23:59 +0000`に設定されており、ジョブをいつでもスケジュールできます。

## 可観測性 {#observability}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションは、TiDB セルフホストにのみ適用されます。現在、 TiDB Cloud はTTL メトリックを提供していません。

</CustomContent>

TiDB は定期的に TTL に関する実行時情報を収集し、Grafana でこれらのメトリックの視覚化されたグラフを提供します。これらのメトリックは、Grafana の TiDB -&gt; TTL パネルで確認できます。

<CustomContent platform="tidb">

メトリックの詳細については、 [TiDB モニタリング メトリック](/grafana-tidb-dashboard.md)の TTL セクションを参照してください。

</CustomContent>

さらに、TiDB は TTL ジョブに関する詳細情報を取得するための 3 つのテーブルを提供します。

-   `mysql.tidb_ttl_table_status`テーブルには、すべての TTL テーブルについて、以前に実行された TTL ジョブと進行中の TTL ジョブに関する情報が含まれています。

    ```sql
    TABLE mysql.tidb_ttl_table_status LIMIT 1\G
    ```

        *************************** 1. row ***************************
                              table_id: 85
                       parent_table_id: 85
                      table_statistics: NULL
                           last_job_id: 0b4a6d50-3041-4664-9516-5525ee6d9f90
                   last_job_start_time: 2023-02-15 20:43:46
                  last_job_finish_time: 2023-02-15 20:44:46
                   last_job_ttl_expire: 2023-02-15 19:43:46
                      last_job_summary: {"total_rows":4369519,"success_rows":4369519,"error_rows":0,"total_scan_task":64,"scheduled_scan_task":64,"finished_scan_task":64}
                        current_job_id: NULL
                  current_job_owner_id: NULL
                current_job_owner_addr: NULL
             current_job_owner_hb_time: NULL
                current_job_start_time: NULL
                current_job_ttl_expire: NULL
                     current_job_state: NULL
                    current_job_status: NULL
        current_job_status_update_time: NULL
        1 row in set (0.040 sec)

    列`table_id`はパーティションテーブルの ID であり、列`parent_table_id`テーブルの ID で、列[`information_schema.tables`](/information-schema/information-schema-tables.md)の ID に対応します。テーブルがパーティションテーブルでない場合、2 つの ID は同じになります。

    列`{last, current}_job_{start_time, finish_time, ttl_expire}`は、それぞれ、前回または現在の実行の TTL ジョブで使用された開始時刻、終了時刻、有効期限を示します。列`last_job_summary`は、行の合計数、成功した行の数、失敗した行の数など、最後の TTL タスクの実行ステータスを示します。

-   `mysql.tidb_ttl_task`テーブルには、進行中の TTL サブタスクに関する情報が含まれています。TTL ジョブは多くのサブタスクに分割され、このテーブルには現在実行中のサブタスクが記録されます。

-   `mysql.tidb_ttl_job_history`テーブルには、実行された TTL ジョブに関する情報が含まれています。TTL ジョブ履歴の記録は 90 日間保持されます。

    ```sql
    TABLE mysql.tidb_ttl_job_history LIMIT 1\G
    ```

        *************************** 1. row ***************************
                   job_id: f221620c-ab84-4a28-9d24-b47ca2b5a301
                 table_id: 85
          parent_table_id: 85
             table_schema: test_schema
               table_name: TestTable
           partition_name: NULL
              create_time: 2023-02-15 17:43:46
              finish_time: 2023-02-15 17:45:46
               ttl_expire: 2023-02-15 16:43:46
             summary_text: {"total_rows":9588419,"success_rows":9588419,"error_rows":0,"total_scan_task":63,"scheduled_scan_task":63,"finished_scan_task":63}
             expired_rows: 9588419
             deleted_rows: 9588419
        error_delete_rows: 0
                   status: finished

    列`table_id`はパーティションテーブルの ID で、 `parent_table_id`テーブルの ID で、 `information_schema.tables`の ID に対応します。 `table_schema` 、 `table_name` 、および`partition_name` 、データベース、テーブル名、およびパーティション名に対応します。 `create_time` 、 `finish_time` 、および`ttl_expire` 、TTL タスクの作成時刻、終了時刻、および有効期限を示します。 `expired_rows`と`deleted_rows` 、期限切れの行数と正常に削除された行数を示します。

## TiDBツールとの互換性 {#compatibility-with-tidb-tools}

TTL は、他の TiDB 移行、バックアップ、およびリカバリ ツールでも使用できます。

| ツール名           | サポートされる最小バージョン | 説明                                                                                                                                                                           |
| -------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| バックアップと復元 (BR) | バージョン6.6.0     | BRを使用してデータを復元すると、テーブルの`TTL_ENABLE`属性が`OFF`に設定されます。これにより、バックアップと復元後に TiDB が期限切れのデータをすぐに削除することがなくなります。各テーブルの TTL を再度有効にするには、 `TTL_ENABLE`属性を手動でオンにする必要があります。                   |
| TiDB Lightning | バージョン6.6.0     | TiDB Lighting を使用してデータをインポートすると、インポートされたテーブルの`TTL_ENABLE`属性が`OFF`に設定されます。これにより、TiDB がインポート後に期限切れのデータをすぐに削除することがなくなります。各テーブルの TTL を再度有効にするには、 `TTL_ENABLE`属性を手動でオンにする必要があります。 |
| ティCDC          | バージョン7.0.0     | ダウンストリームの`TTL_ENABLE`属性は自動的に`OFF`に設定されます。アップストリームの TTL 削除はダウンストリームに同期されます。したがって、重複削除を防ぐために、ダウンストリーム テーブルの`TTL_ENABLE`属性は強制的に`OFF`に設定されます。                                    |

## SQLとの互換性 {#compatibility-with-sql}

| 機能名                                                                         | 説明                                                                                                                                                                                 |
| :-------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)       | `FLASHBACK TABLE` 、テーブルの`TTL_ENABLE`属性を`OFF`に設定します。これにより、フラッシュバック後に TiDB が期限切れのデータをすぐに削除することがなくなります。各テーブルの TTL を再度有効にするには、 `TTL_ENABLE`属性を手動でオンにする必要があります。                         |
| [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) | `FLASHBACK DATABASE`はテーブルの`TTL_ENABLE`属性を`OFF`に設定し、 `TTL_ENABLE`属性は変更されません。これにより、フラッシュバック後に TiDB が期限切れのデータをすぐに削除することがなくなります。各テーブルの TTL を再度有効にするには、 `TTL_ENABLE`属性を手動でオンにする必要があります。 |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)   | `FLASHBACK CLUSTER`はシステム変数[`TIDB_TTL_JOB_ENABLE`](/system-variables.md#tidb_ttl_job_enable-new-in-v650)を`OFF`に設定し、属性`TTL_ENABLE`の値は変更しません。                                         |

## 制限事項 {#limitations}

現在、TTL 機能には次の制限があります。

-   TTL 属性は、ローカル一時テーブルやグローバル一時テーブルなどの一時テーブルには設定できません。
-   TTL 属性を持つテーブルは、外部キー制約のプライマリ テーブルとして他のテーブルから参照されることをサポートしていません。
-   すべての期限切れデータがすぐに削除されることは保証されません。期限切れデータが削除される時間は、バックグラウンド クリーンアップ ジョブのスケジュール間隔とスケジュール ウィンドウによって異なります。
-   [クラスター化インデックス](/clustered-indexes.md)を使用するテーブルの場合、主キーが整数型でもバイナリ文字列型でもない場合は、TTL ジョブを複数のタスクに分割できません。これにより、TTL ジョブは単一の TiDB ノードで順番に実行されます。テーブルに大量のデータが含まれている場合、TTL ジョブの実行が遅くなる可能性があります。
-   TTLは[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)では使用できません。

## よくある質問 {#faqs}

<CustomContent platform="tidb">

-   削除がデータ サイズを比較的安定させるのに十分な速さであるかどうかをどのように判断すればよいでしょうか?

    [Grafana `TiDB`ダッシュボード](/grafana-tidb-dashboard.md)では、パネル`TTL Insert Rows Per Hour`は過去 1 時間に挿入された行の合計数を記録します。対応する`TTL Delete Rows Per Hour`は、過去 1 時間に TTL タスクによって削除された行の合計数を記録します。7 `TTL Insert Rows Per Hour`長期間にわたって`TTL Delete Rows Per Hour`よりも高い場合は、挿入率が削除率よりも高く、データの合計量が増加することを意味します。例:

    ![insert fast example](/media/ttl/insert-fast.png)

    注意すべき点は、TTL は期限切れの行がすぐに削除されることを保証するものではなく、現在挿入されている行は将来の TTL タスクで削除されるため、短期間で TTL 削除の速度が挿入の速度よりも遅い場合でも、必ずしも TTL の速度が遅すぎることを意味するわけではないということです。状況をその文脈で考慮する必要があります。

-   TTL タスクのボトルネックがスキャンにあるか削除にあるかをどのように判断できますか?

    `TTL Scan Worker Time By Phase`と`TTL Delete Worker Time By Phase`パネルを見てください。スキャン ワーカーが`dispatch`フェーズに多くの時間いるのに、削除ワーカーが`idle`フェーズにほとんどいない場合、スキャン ワーカーは削除ワーカーが削除を完了するのを待っています。この時点でクラスター リソースがまだ空いている場合は、 `tidb_ttl_ delete_worker_count`を増やして削除ワーカーの数を増やすことを検討できます。例:

    ![scan fast example](/media/ttl/scan-fast.png)

    対照的に、スキャン ワーカーが第`dispatch`フェーズにほとんどなく、削除ワーカーが第`idle`フェーズに長時間ある場合、スキャン ワーカーは比較的ビジー状態です。例:

    ![delete fast example](/media/ttl/delete-fast.png)

    TTL ジョブのスキャンと削除の割合はマシン構成とデータ分布に関連しているため、各瞬間の監視データは実行中の TTL ジョブのみを表します。表`mysql.tidb_ttl_job_history`を読むと、特定の瞬間にどの TTL ジョブが実行されているか、およびジョブに対応する表を確認できます。

-   `tidb_ttl_scan_worker_count`と`tidb_ttl_delete_worker_count`適切に設定するにはどうすればいいですか?

    1.  「TTL タスクのボトルネックがスキャンにあるか削除にあるかを判断するにはどうすればよいでしょうか?」という質問を参照して、 `tidb_ttl_scan_worker_count`または`tidb_ttl_delete_worker_count`の値を増やすかどうかを検討してください。
    2.  TiKV ノードの数が多い場合は、値を`tidb_ttl_scan_worker_count`増やすと、TTL タスクのワークロードがより均等になります。

    TTL ワーカーが多すぎると大きな負担がかかるため、TiDB の CPU レベルと TiKV のディスクおよび CPU 使用率を一緒に評価する必要があります。さまざまなシナリオとニーズ (TTL を可能な限り高速化する必要があるか、TTL が他のクエリに与える影響を減らす必要があるか) に応じて、 `tidb_ttl_scan_worker_count`と`tidb_ttl_delete_worker_count`の値を調整して、TTL スキャンと削除の速度を向上させたり、TTL タスクによってもたらされるパフォーマンスへの影響を減らしたりすることができます。

</CustomContent>
<CustomContent platform="tidb-cloud">

-   `tidb_ttl_scan_worker_count`と`tidb_ttl_delete_worker_count`適切に設定するにはどうすればいいですか?

    TiKV ノードの数が多い場合は、値を`tidb_ttl_scan_worker_count`増やすと、TTL タスクのワークロードがより均等になります。

    ただし、TTL ワーカーが多すぎると大きな負担がかかるため、TiDB の CPU レベルと TiKV のディスクおよび CPU 使用率を一緒に評価する必要があります。さまざまなシナリオとニーズ (TTL を可能な限り高速化する必要があるか、TTL が他のクエリに与える影響を減らす必要があるか) に応じて、 `tidb_ttl_scan_worker_count`と`tidb_ttl_delete_worker_count`の値を調整して、TTL スキャンと削除の速度を向上させたり、TTL タスクによってもたらされるパフォーマンスへの影響を減らしたりすることができます。

</CustomContent>
