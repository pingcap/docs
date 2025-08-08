---
title: Periodically Delete Data Using TTL (Time to Live)
summary: Time to Live（TTL）は、TiDBデータの有効期間を行レベルで管理できる機能です。このドキュメントでは、TTLを使用して古いデータを自動的に期限切れにして削除する方法を説明します。
---

# TTL（Time to Live）を使用して期限切れのデータを定期的に削除する {#periodically-delete-expired-data-using-ttl-time-to-live}

Time to Live（TTL）は、TiDBデータの有効期間を行レベルで管理できる機能です。TTL属性を持つテーブルの場合、TiDBは自動的にデータ有効期間をチェックし、期限切れのデータを行レベルで削除します。この機能は、一部のシナリオにおいてstorage容量を効果的に節約し、パフォーマンスを向上させることができます。

TTL の一般的なシナリオを次に示します。

-   確認コードと短縮 URL を定期的に削除します。
-   不要な履歴注文を定期的に削除します。
-   計算の中間結果を自動的に削除します。

TTLは、オンラインの読み取りおよび書き込みワークロードに影響を与えることなく、不要なデータを定期的かつタイムリーにクリーンアップできるように設計されています。TTLは、異なるジョブを異なるTiDBノードに同時にディスパッチし、テーブル単位でデータを並列に削除します。TTLは、すべての期限切れデータが即座に削除されることを保証するものではありません。つまり、一部のデータが期限切れになったとしても、バックグラウンドTTLジョブによってデータが削除されるまで、クライアントは有効期限からしばらく経ってからそのデータを読み取る可能性があります。

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

    上記の例では、テーブル`t1`を作成し、TTL タイムスタンプ列に`created_at`指定しています。これはデータの作成時刻を示します。また、テーブル内で行が保持できる最長期間を 3 か月から`INTERVAL 3 MONTH`に設定しています。この値よりも長く保持されるデータは、後で削除されます。

-   期限切れのデータをクリーンアップする機能を有効または無効にするには、 `TTL_ENABLE`属性を設定します。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF';
    ```

    `TTL_ENABLE` `OFF`に設定した場合、他の TTL オプションが設定されていても、TiDB はこのテーブル内の期限切れデータを自動的にクリーンアップしません。TTL 属性を持つテーブルの場合、デフォルトでは`TTL_ENABLE`が`ON`なります。

-   MySQL との互換性を保つために、コメントを使用して TTL 属性を設定できます。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) /*T![ttl] TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF'*/;
    ```

    TiDBでは、テーブルのTTL属性を使用するか、コメントを使用してTTLを設定することは同等です。MySQLでは、コメントは無視され、通常のテーブルが作成されます。

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

TTL は[データ型のデフォルト値](/data-type-default-values.md)と組み合わせて使用できます。以下に一般的な使用例を2つ示します。

-   列のデフォルト値を現在の作成時刻に指定し、この列をTTLタイムスタンプ列として使用するには、 `DEFAULT CURRENT_TIMESTAMP`使用します。3か月前に作成されたレコードは期限切れになります。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

-   列のデフォルト値を作成時刻または最終更新時刻として指定し、その列をTTLタイムスタンプ列として使用します。3ヶ月間更新されていないレコードは期限切れとなります。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

### TTLと生成された列 {#ttl-and-generated-columns}

TTLと[生成された列](/generated-columns.md)を組み合わせて使用すると、複雑な有効期限ルールを設定できます。例：

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

上記のステートメントでは、 `expire_at`列をTTLタイムスタンプ列として使用し、メッセージの種類に応じて有効期限を設定します。メッセージが画像の場合、5日後に有効期限が切れます。それ以外の場合は、30日後に有効期限が切れます。

TTL は[JSON型](/data-type-json.md)と一緒に使用できます。例:

```sql
CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_info JSON,
    created_at DATE AS (JSON_EXTRACT(order_info, '$.created_at')) VIRTUAL
) TTL = `created_at` + INTERVAL 3 month;
```

## TTLジョブ {#ttl-job}

TiDBは、TTL属性を持つ各テーブルに対して、期限切れデータをクリーンアップするためのバックグラウンドジョブを内部的にスケジュールします。これらのジョブの実行周期は、テーブルのTTL属性`TTL_JOB_INTERVAL`設定することでカスタマイズできます。次の例では、テーブル`orders`のバックグラウンドクリーンアップジョブを24時間ごとに1回実行するよう設定しています。

```sql
ALTER TABLE orders TTL_JOB_INTERVAL = '24h';
```

デフォルトでは`TTL_JOB_INTERVAL` `1h`に設定されています。

TTLジョブを実行する際、TiDBはテーブルを最大64個のタスクに分割します。分割の最小単位はリージョンです。これらのタスクは分散実行されます。システム変数[`tidb_ttl_running_tasks`](/system-variables.md#tidb_ttl_running_tasks-new-in-v700)設定することで、クラスター全体で同時実行可能なTTLタスクの数を制限できます。ただし、すべての種類のテーブルのすべてのTTLジョブをタスクに分割できるわけではありません。どの種類のテーブルのTTLジョブをタスクに分割できないかの詳細については、セクション[制限事項](#limitations)を参照してください。

TTL ジョブの実行を無効にするには、 `TTL_ENABLE='OFF'`テーブル オプションを設定することに加えて、 [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650)グローバル変数を設定してクラスター全体で TTL ジョブの実行を無効にすることもできます。

```sql
SET @@global.tidb_ttl_job_enable = OFF;
```

シナリオによっては、TTLジョブを特定の時間枠でのみ実行したい場合があります。この場合、グローバル変数[`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650)と[`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650)設定することで、時間枠を指定できます。例：

```sql
SET @@global.tidb_ttl_job_schedule_window_start_time = '01:00 +0000';
SET @@global.tidb_ttl_job_schedule_window_end_time = '05:00 +0000';
```

上記のステートメントでは、TTLジョブをUTCの1:00から5:00の間にのみスケジュールできます。デフォルトでは、時間枠は`00:00 +0000`から`23:59 +0000`に設定されており、ジョブはいつでもスケジュールできます。

## 可観測性 {#observability}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションはTiDBセルフマネージドにのみ適用されます。現在、 TiDB CloudはTTLメトリクスを提供していません。

</CustomContent>

TiDBはTTLに関する実行時情報を定期的に収集し、Grafanaでこれらのメトリクスを視覚化したチャートを提供します。これらのメトリクスは、GrafanaのTiDB -&gt; TTLパネルで確認できます。

<CustomContent platform="tidb">

メトリックの詳細については、 [TiDB 監視メトリクス](/grafana-tidb-dashboard.md)の TTL セクションを参照してください。

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

    列`table_id`パーティションテーブルの ID であり、列`parent_table_id`テーブルの ID で、 [`information_schema.tables`](/information-schema/information-schema-tables.md)の ID に対応します。テーブルがパーティションテーブルでない場合、2 つの ID は同じになります。

    列`{last, current}_job_{start_time, finish_time, ttl_expire}` 、それぞれ、前回または現在実行中のTTLジョブで使用された開始時刻、終了時刻、有効期限を示します。列`last_job_summary`は、前回のTTLタスクの実行ステータス（合計行数、成功行数、失敗行数など）を示します。

-   `mysql.tidb_ttl_task`テーブルには、実行中の TTL サブタスクに関する情報が含まれています。TTL ジョブは複数のサブタスクに分割され、このテーブルには現在実行中のサブタスクが記録されます。

-   `mysql.tidb_ttl_job_history`テーブルには、実行された TTL ジョブに関する情報が含まれています。TTL ジョブの履歴は 90 日間保存されます。

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

    列`table_id`パーティションテーブルの ID であり、 `parent_table_id`はテーブルの ID で、 `information_schema.tables`の ID に対応します。 `table_schema` 、 `table_name` 、および`partition_name` 、データベース、テーブル名、およびパーティション名に対応します。 `create_time` 、 `finish_time` 、および`ttl_expire` 、TTL タスクの作成時刻、終了時刻、および有効期限を示します。 `expired_rows`と`deleted_rows` 、期限切れの行数と正常に削除された行数を示します。

## TiDBツールとの互換性 {#compatibility-with-tidb-tools}

TTL は、他の TiDB 移行、バックアップ、およびリカバリ ツールでも使用できます。

| ツール名           | サポートされる最小バージョン | 説明                                                                                                                                                                  |
| -------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| バックアップと復元 (BR) | バージョン6.6.0     | BRを使用してデータをリストアすると、テーブルの`TTL_ENABLE`属性が`OFF`に設定されます。これにより、TiDB はバックアップとリストア後に期限切れのデータを直ちに削除しなくなります。各テーブルの TTL を再度有効にするには、 `TTL_ENABLE`属性を手動でオンにする必要があります。           |
| TiDB Lightning | バージョン6.6.0     | TiDB Lightingを使用してデータをインポートすると、インポートされたテーブルの属性`TTL_ENABLE` `OFF`に設定されます。これにより、TiDBはインポート後に期限切れのデータをすぐに削除しなくなります。各テーブルのTTLを再度有効にするには、属性`TTL_ENABLE`を手動でオンにする必要があります。 |
| TiCDC          | バージョン7.0.0     | ダウンストリームの`TTL_ENABLE`属性は自動的に`OFF`に設定されます。アップストリームのTTL削除はダウンストリームに同期されます。そのため、重複削除を防ぐため、ダウンストリームテーブルの`TTL_ENABLE`属性は強制的に`OFF`に設定されます。                                |

## SQLとの互換性 {#compatibility-with-sql}

| 機能名                                                                         | 説明                                                                                                                                                                               |
| :-------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)       | `FLASHBACK TABLE`指定すると、テーブルの`TTL_ENABLE`属性が`OFF`に設定されます。これにより、TiDBはフラッシュバック後に期限切れのデータを直ちに削除しなくなります。各テーブルのTTLを再度有効にするには、 `TTL_ENABLE`属性を手動でオンにする必要があります。                          |
| [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) | `FLASHBACK DATABASE`指定すると、テーブルの`TTL_ENABLE`属性が`OFF`に設定され、 `TTL_ENABLE`属性は変更されません。これにより、TiDBはフラッシュバック後に期限切れのデータを直ちに削除しなくなります。各テーブルのTTLを再度有効にするには、 `TTL_ENABLE`属性を手動でオンにする必要があります。 |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)   | `FLASHBACK CLUSTER`システム変数[`TIDB_TTL_JOB_ENABLE`](/system-variables.md#tidb_ttl_job_enable-new-in-v650)を`OFF`に設定し、属性`TTL_ENABLE`の値は変更しません。                                        |

## 制限事項 {#limitations}

現在、TTL 機能には次の制限があります。

-   TTL 属性は、ローカル一時テーブルやグローバル一時テーブルなどの一時テーブルには設定できません。
-   TTL 属性を持つテーブルは、外部キー制約のプライマリ テーブルとして他のテーブルから参照されることをサポートしていません。
-   すべての期限切れデータが直ちに削除されることは保証されません。期限切れデータが削除されるタイミングは、バックグラウンドクリーンアップジョブのスケジュール間隔とスケジュールウィンドウによって異なります。
-   [クラスター化インデックス](/clustered-indexes.md)使用するテーブルの場合、TTL ジョブは、次のシナリオでのみ複数のサブタスクに分割できます。
    -   主キーまたは複合主キーの最初の列は、 `INTEGER`またはバイナリ文字列型です。バイナリ文字列型は主に以下のものを指します。
        -   `CHAR(N) CHARACTER SET BINARY`
        -   `VARCHAR(N) CHARACTER SET BINARY`
        -   `BINARY(N)`
        -   `VARBINARY(N)`
        -   `BIT(N)`
    -   主キーまたは複合主キーの最初の列の文字セットは`utf8`または`utf8mb4`であり、照合順序は`utf8_bin` 、 `utf8mb4_bin` 、または`utf8mb4_0900_bin`です。
    -   主キーの最初の列の文字セットタイプが`utf8`または`utf8mb4`あるテーブルの場合、サブタスクは表示可能なASCII文字の範囲に基づいてのみ分割されます。多くの主キー値に同じASCIIプレフィックスが付いている場合、タスクの分割が不均一になる可能性があります。
    -   TTLジョブを複数のサブタスクに分割できないテーブルの場合、TTLジョブは単一のTiDBノードで順次実行されます。テーブルに大量のデータが含まれている場合、TTLジョブの実行速度が遅くなる可能性があります。

## よくある質問 {#faqs}

<CustomContent platform="tidb">

-   削除がデータ サイズを比較的安定させるのに十分な速さであるかどうかをどのように判断すればよいでしょうか?

    [Grafana `TiDB`ダッシュボード](/grafana-tidb-dashboard.md)のパネル`TTL Insert Rows Per Hour`は、過去 1 時間に挿入された行の総数を記録します。対応する`TTL Delete Rows Per Hour`は、過去 1 時間に TTL タスクによって削除された行の総数を記録します。7 `TTL Insert Rows Per Hour`長期間にわたって`TTL Delete Rows Per Hour`よりも高い場合、挿入率が削除率を上回り、データの総量が増加することを意味します。例：

    ![insert fast example](/media/ttl/insert-fast.png)

    TTLは期限切れの行がすぐに削除されることを保証するものではなく、現在挿入されている行は将来のTTLタスクで削除されるため、TTLによる削除速度が短期間で挿入速度よりも遅い場合でも、必ずしもTTLの速度が遅すぎることを意味するわけではないことに注意してください。状況をその文脈で考慮する必要があります。

-   TTL タスクのボトルネックがスキャンにあるか削除にあるかをどのように判断すればよいですか?

    パネル`TTL Scan Worker Time By Phase`と`TTL Delete Worker Time By Phase`を見てください。スキャンワーカーが`dispatch`フェーズにある時間の割合がかなり多く、削除ワーカーが`idle`フェーズにあることがほとんどない場合、スキャンワーカーは削除ワーカーによる削除の完了を待機しています。この時点でクラスターリソースにまだ余裕がある場合は、 `tidb_ttl_ delete_worker_count`増やして削除ワーカーの数を増やすことを検討してください。例：

    ![scan fast example](/media/ttl/scan-fast.png)

    対照的に、スキャンワーカーが第`dispatch`フェーズにほとんどいないのに、削除ワーカーが第`idle`フェーズに長時間いる場合、スキャンワーカーは比較的忙しい状態です。例えば、

    ![delete fast example](/media/ttl/delete-fast.png)

    TTLジョブにおけるスキャンと削除の割合はマシン構成とデータ分布に左右されるため、各時点の監視データは実行中のTTLジョブの代表値に過ぎません。表`mysql.tidb_ttl_job_history`を参照することで、特定の時点で実行中のTTLジョブと、そのジョブに対応する表を確認できます。

-   `tidb_ttl_scan_worker_count`と`tidb_ttl_delete_worker_count`適切に設定するにはどうすればいいでしょうか?

    1.  `tidb_ttl_scan_worker_count`または`tidb_ttl_delete_worker_count`値を増やすかどうかを検討するには、「TTL タスクのボトルネックがスキャンにあるか削除にあるかを判断するにはどうすればよいでしょうか?」という質問を参照してください。
    2.  TiKV ノードの数が多い場合は、値を`tidb_ttl_scan_worker_count`増やすと、TTL タスクのワークロードのバランスがより取れます。

    TTLワーカーが多すぎると負荷が大きくなるため、TiDBのCPUレベルとTiKVのディスクおよびCPU使用率を併せて評価する必要があります。さまざまなシナリオやニーズ（TTLを可能な限り高速化する必要があるか、他のクエリへのTTLの影響を軽減する必要があるかなど）に応じて、 `tidb_ttl_scan_worker_count`と`tidb_ttl_delete_worker_count`の値を調整することで、TTLスキャンと削除の速度を向上させたり、TTLタスクによるパフォーマンスへの影響を軽減したりできます。

</CustomContent>
<CustomContent platform="tidb-cloud">

-   `tidb_ttl_scan_worker_count`と`tidb_ttl_delete_worker_count`適切に設定するにはどうすればいいでしょうか?

    TiKV ノードの数が多い場合は、値を`tidb_ttl_scan_worker_count`増やすと、TTL タスクのワークロードのバランスがより取れます。

    しかし、TTLワーカーが多すぎると負荷が大きくなるため、TiDBのCPU使用率とTiKVのディスクおよびCPU使用率を併せて評価する必要があります。様々なシナリオやニーズ（TTLを可能な限り高速化する必要があるか、他のクエリへのTTLの影響を軽減する必要があるかなど）に応じて、 `tidb_ttl_scan_worker_count`と`tidb_ttl_delete_worker_count`の値を調整することで、TTLスキャンと削除の速度を向上させたり、TTLタスクによるパフォーマンスへの影響を軽減したりできます。

</CustomContent>
