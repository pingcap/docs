---
title: Periodically Delete Data Using TTL (Time to Live)
summary: Time to live (TTL) is a feature that allows you to manage TiDB data lifetime at the row level. In this document, you can learn how to use TTL to automatically expire and delete old data.
---

# TTL (Time to Live) を使用して期限切れデータを定期的に削除する {#periodically-delete-expired-data-using-ttl-time-to-live}

Time to Live (TTL) は、TiDB データの有効期間を行レベルで管理できるようにする機能です。 TTL 属性を持つテーブルの場合、TiDB はデータの有効期間を自動的にチェックし、期限切れのデータを行レベルで削除します。この機能により、storage領域を効果的に節約し、一部のシナリオでパフォーマンスを向上させることができます。

以下に、TTL の一般的なシナリオをいくつか示します。

-   確認コードと短縮 URL は定期的に削除してください。
-   不要な過去の注文を定期的に削除します。
-   計算の途中結果を自動的に削除します。

TTL は、オンラインの読み取りおよび書き込みのワークロードに影響を与えることなく、ユーザーが不要なデータを定期的かつタイムリーにクリーンアップできるように設計されています。 TTL は、異なるジョブを異なる TiDB ノードに同時にディスパッチし、テーブル単位で並行してデータを削除します。 TTL は、期限切れのすべてのデータが直ちに削除されることを保証しません。つまり、一部のデータが期限切れであっても、そのデータがバックグラウンド TTL ジョブによって削除されるまで、クライアントは期限切れ後しばらくしてからそのデータを読み取る可能性があります。

## 構文 {#syntax}

[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)または[`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)ステートメントを使用して、テーブルの TTL 属性を構成できます。

### TTL属性を持つテーブルを作成する {#create-a-table-with-a-ttl-attribute}

-   TTL 属性を持つテーブルを作成します。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

    前の例では、テーブル`t1`を作成し、データの作成時間を示す TTL タイムスタンプ列として`created_at`を指定します。この例では、行がテーブル内に存在できる最長期間を 3 か月から`INTERVAL 3 MONTH`に設定します。この値よりも長く存続するデータは後で削除されます。

-   `TTL_ENABLE`属性を設定して、期限切れデータのクリーンアップ機能を有効または無効にします。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF';
    ```

    `TTL_ENABLE`が`OFF`に設定されている場合、他の TTL オプションが設定されている場合でも、TiDB はこのテーブル内の期限切れデータを自動的にクリーンアップしません。 TTL 属性を持つテーブルの場合、デフォルトでは`TTL_ENABLE`が`ON`になります。

-   MySQL との互換性を保つために、コメントを使用して TTL 属性を設定できます。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP
    ) /*T![ttl] TTL = `created_at` + INTERVAL 3 MONTH TTL_ENABLE = 'OFF'*/;
    ```

    TiDB では、テーブル TTL 属性を使用すること、またはコメントを使用して TTL を構成することは同等です。 MySQL では、コメントは無視され、通常のテーブルが作成されます。

### テーブルの TTL 属性を変更する {#modify-the-ttl-attribute-of-a-table}

-   テーブルの TTL 属性を変更します。

    ```sql
    ALTER TABLE t1 TTL = `created_at` + INTERVAL 1 MONTH;
    ```

    前述のステートメントを使用すると、既存の TTL 属性を持つテーブルを変更したり、TTL 属性のないテーブルに TTL 属性を追加したりできます。

-   TTL 属性を持つテーブルの値`TTL_ENABLE`を変更します。

    ```sql
    ALTER TABLE t1 TTL_ENABLE = 'OFF';
    ```

-   テーブルのすべての TTL 属性を削除するには:

    ```sql
    ALTER TABLE t1 REMOVE TTL;
    ```

### TTL とデータ型のデフォルト値 {#ttl-and-the-default-values-of-data-types}

TTL は[データ型のデフォルト値](/data-type-default-values.md)と併用できます。以下に 2 つの一般的な使用例を示します。

-   列のデフォルト値を現在の作成時刻として指定し、この列を TTL タイムスタンプ列として使用するには、 `DEFAULT CURRENT_TIMESTAMP`を使用します。 3 か月前に作成されたレコードは期限切れになります。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

-   列のデフォルト値を作成時刻または最終更新時刻として指定し、この列を TTL タイムスタンプ列として使用します。 3 か月間更新されなかったレコードは期限切れになります。

    ```sql
    CREATE TABLE t1 (
        id int PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) TTL = `created_at` + INTERVAL 3 MONTH;
    ```

### TTL と生成された列 {#ttl-and-generated-columns}

TTL と[生成された列](/generated-columns.md)を併用して、複雑な有効期限ルールを構成できます。例えば：

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

前述のステートメントでは、 `expire_at`列を TTL タイムスタンプ列として使用し、メッセージ タイプに応じて有効期限を設定します。メッセージが画像の場合、有効期限は 5 日です。それ以外の場合は、30 日で期限切れになります。

TTL は[JSONタイプ](/data-type-json.md)と併用できます。例えば：

```sql
CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_info JSON,
    created_at DATE AS (JSON_EXTRACT(order_info, '$.created_at')) VIRTUAL
) TTL = `created_at` + INTERVAL 3 month;
```

## TTLジョブ {#ttl-job}

TTL 属性を持つテーブルごとに、TiDB は有効期限切れのデータをクリーンアップするバックグラウンド ジョブを内部的にスケジュールします。テーブルに`TTL_JOB_INTERVAL`属性を設定することで、これらのジョブの実行期間をカスタマイズできます。次の例では、テーブル`orders`のバックグラウンド クリーンアップ ジョブが 24 時間ごとに実行されるように設定します。

```sql
ALTER TABLE orders TTL_JOB_INTERVAL = '24h';
```

デフォルトでは`TTL_JOB_INTERVAL` `1h`に設定されます。

TTL ジョブを実行するとき、TiDB はテーブルを最大 64 のタスクに分割します。リージョンは最小単位です。これらのタスクは分散的に実行されます。システム変数[`tidb_ttl_running_tasks`](/system-variables.md#tidb_ttl_running_tasks-new-in-v700)を設定することで、クラスター全体での同時 TTL タスクの数を制限できます。ただし、すべての種類のテーブルのすべての TTL ジョブをタスクに分割できるわけではありません。どの種類のテーブルの TTL ジョブをタスクに分割できないかについて詳しくは、 [制限事項](#limitations)セクションを参照してください。

TTL ジョブの実行を無効にするには、 `TTL_ENABLE='OFF'`テーブル オプションを設定するだけでなく、 [`tidb_ttl_job_enable`](/system-variables.md#tidb_ttl_job_enable-new-in-v650)グローバル変数を設定してクラスター全体で TTL ジョブの実行を無効にすることもできます。

```sql
SET @@global.tidb_ttl_job_enable = OFF;
```

シナリオによっては、特定の時間枠内でのみ TTL ジョブの実行を許可したい場合があります。この場合、 [`tidb_ttl_job_schedule_window_start_time`](/system-variables.md#tidb_ttl_job_schedule_window_start_time-new-in-v650)と[`tidb_ttl_job_schedule_window_end_time`](/system-variables.md#tidb_ttl_job_schedule_window_end_time-new-in-v650)グローバル変数を設定して時間枠を指定できます。例えば：

```sql
SET @@global.tidb_ttl_job_schedule_window_start_time = '01:00 +0000';
SET @@global.tidb_ttl_job_schedule_window_end_time = '05:00 +0000';
```

前述のステートメントでは、TTL ジョブを UTC 1:00 から 5:00 の間でのみスケジュールできます。デフォルトでは、時間枠は`00:00 +0000` ～ `23:59 +0000`に設定されており、いつでもジョブをスケジュールできます。

## 可観測性 {#observability}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションは、TiDB セルフホスト型にのみ適用されます。現在、 TiDB Cloud はTTL メトリクスを提供していません。

</CustomContent>

TiDB は、TTL に関するランタイム情報を定期的に収集し、Grafana でこれらのメトリックの視覚化されたグラフを提供します。これらのメトリクスは、Grafana の [TiDB -&gt; TTL] パネルで確認できます。

<CustomContent platform="tidb">

メトリクスの詳細については、 [TiDB モニタリングメトリクス](/grafana-tidb-dashboard.md)の TTL セクションを参照してください。

</CustomContent>

さらに、TiDB には、TTL ジョブに関する詳細情報を取得するための 3 つのテーブルが用意されています。

-   `mysql.tidb_ttl_table_status`テーブルには、すべての TTL テーブルについて以前に実行された TTL ジョブと進行中の TTL ジョブに関する情報が含まれています。

    ```sql
    MySQL [(none)]> SELECT * FROM mysql.tidb_ttl_table_status LIMIT 1\G;
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
    ```

    列`table_id`はパーティションテーブルの ID で、列`parent_table_id`はテーブルの ID であり、 `infomation_schema.tables`の ID に対応します。テーブルがパーティションテーブルでない場合、2 つの ID は同じです。

    列`{last, current}_job_{start_time, finish_time, ttl_expire}`は、最後または現在の実行の TTL ジョブによって使用された開始時間、終了時間、および有効期限をそれぞれ記述します。 `last_job_summary`列目は、総行数、成功した行数、失敗した行数など、最後の TTL タスクの実行ステータスを示します。

-   `mysql.tidb_ttl_task`テーブルには、進行中の TTL サブタスクに関する情報が含まれています。 TTL ジョブは多くのサブタスクに分割されており、このテーブルには現在実行中のサブタスクが記録されます。

-   `mysql.tidb_ttl_job_history`テーブルには、実行された TTL ジョブに関する情報が含まれています。 TTL ジョブ履歴の記録は 90 日間保存されます。

    ```sql
    MySQL [(none)]> SELECT * FROM mysql.tidb_ttl_job_history LIMIT 1\G;
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
    ```

    列`table_id`はパーティションテーブルの ID で、列`parent_table_id`はテーブルの ID であり、 `infomation_schema.tables`の ID に対応します。 `table_schema` `table_name`データベース、テーブル名、パーティション名に対応します`partition_name` `create_time` 、 `finish_time` 、 `ttl_expire`は、ＴＴＬタスクの作成時刻、終了時刻、有効期限を示す。 `expired_rows`と`deleted_rows` 、期限切れの行の数と正常に削除された行の数を示します。

## TiDB ツールとの互換性 {#compatibility-with-tidb-tools}

TTL は、他の TiDB 移行、バックアップ、およびリカバリ ツールと併用できます。

| ツール名           | サポートされる最小バージョン | 説明                                                                                                                                                                        |
| -------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| バックアップと復元 (BR) | v6.6.0         | BRを使用してデータを復元すると、テーブルの`TTL_ENABLE`属性が`OFF`に設定されます。これにより、バックアップと復元後に TiDB が期限切れのデータをすぐに削除することがなくなります。各テーブルの TTL を再度有効にするには、 `TTL_ENABLE`属性を手動でオンにする必要があります。                |
| TiDB Lightning | v6.6.0         | TiDB Lighting を使用してデータをインポートすると、インポートされたテーブルの`TTL_ENABLE`属性が`OFF`に設定されます。これにより、TiDB がインポート後に期限切れのデータをすぐに削除するのを防ぎます。各テーブルの TTL を再度有効にするには、 `TTL_ENABLE`属性を手動でオンにする必要があります。 |
| TiCDC          | v7.0.0         | ダウンストリームの`TTL_ENABLE`属性は自動的に`OFF`に設定されます。アップストリームの TTL 削除はダウンストリームに同期されます。したがって、重複した削除を防ぐために、下流テーブルの`TTL_ENABLE`属性は強制的に`OFF`に設定されます。                                      |

## SQLとの互換性 {#compatibility-with-sql}

| 機能名                                                                                         | 説明                                                                                                                                                                                   |
| :------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)                       | `FLASHBACK TABLE`指定すると、テーブルの`TTL_ENABLE`属性が`OFF`に設定されます。これにより、TiDB がフラッシュバック後に期限切れのデータをすぐに削除するのを防ぎます。各テーブルの TTL を再度有効にするには、 `TTL_ENABLE`属性を手動でオンにする必要があります。                          |
| [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md)                 | `FLASHBACK DATABASE`指定すると、テーブルの`TTL_ENABLE`属性が`OFF`に設定され、 `TTL_ENABLE`属性は変更されません。これにより、TiDB がフラッシュバック後に期限切れのデータをすぐに削除するのを防ぎます。各テーブルの TTL を再度有効にするには、 `TTL_ENABLE`属性を手動でオンにする必要があります。 |
| [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) | `FLASHBACK CLUSTER TO TIMESTAMP`指定すると、システム変数[`TIDB_TTL_JOB_ENABLE`](/system-variables.md#tidb_ttl_job_enable-new-in-v650) `OFF`に設定され、 `TTL_ENABLE`属性の値は変更されません。                      |

## 制限事項 {#limitations}

現在、TTL 機能には次の制限があります。

-   TTL 属性は、ローカル一時テーブルやグローバル一時テーブルなどの一時テーブルには設定できません。
-   TTL 属性を持つテーブルは、外部キー制約の主テーブルとして他のテーブルから参照されることをサポートしません。
-   期限切れのデータがすべて直ちに削除されるという保証はありません。期限切れのデータが削除される時間は、バックグラウンド クリーンアップ ジョブのスケジュール間隔とスケジュール期間によって異なります。
-   [クラスター化インデックス](/clustered-indexes.md)を使用するテーブルの場合、主キーが整数でもバイナリ文字列タイプでもない場合、TTL ジョブを複数のタスクに分割することはできません。これにより、TTL ジョブが単一の TiDB ノード上で順次実行されます。テーブルに大量のデータが含まれている場合、TTL ジョブの実行が遅くなる可能性があります。
-   [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)では TTL は使用できません。

## よくある質問 {#faqs}

<CustomContent platform="tidb">

-   データ サイズを比較的安定に保つのに十分な速度で削除されているかどうかを判断するにはどうすればよいですか?

    [Grafana `TiDB`ダッシュボード](/grafana-tidb-dashboard.md)のパネル`TTL Insert Rows Per Hour`は、前の 1 時間に挿入された行の合計数を記録します。対応する`TTL Delete Rows Per Hour`前の 1 時間に TTL タスクによって削除された行の合計数を記録します。 `TTL Insert Rows Per Hour`が`TTL Delete Rows Per Hour`より高い状態が長期間続く場合は、挿入率が削除率よりも高く、データの総量が増加することを意味します。例えば：

    ![insert fast example](/media/ttl/insert-fast.png)

    TTL では、期限切れの行がすぐに削除されることは保証されず、TTL の削除速度が短い挿入速度よりも遅い場合でも、現在挿入されている行は将来の TTL タスクで削除されることに注意してください。この期間は、必ずしも TTL の速度が遅すぎることを意味するわけではありません。状況をその文脈で考慮する必要があります。

-   TTL タスクのボトルネックがスキャンまたは削除にあるのかどうかを判断するにはどうすればよいですか?

    `TTL Scan Worker Time By Phase`と`TTL Delete Worker Time By Phase`のパネルを見てください。スキャン ワーカーが大部分の時間にわたって`dispatch`フェーズにあり、削除ワーカーが`idle`フェーズにあることはほとんどない場合、スキャン ワーカーは削除ワーカーが削除を完了するのを待っています。この時点でクラスター リソースがまだ空いている場合は、 `tidb_ttl_ delete_worker_count`を増やして削除ワーカーの数を増やすことを検討できます。例えば：

    ![scan fast example](/media/ttl/scan-fast.png)

    対照的に、スキャン ワーカーが`dispatch`フェーズにいることはほとんどなく、削除ワーカーが長期間にわたって`idle`フェーズにある場合、スキャン ワーカーは比較的ビジーです。例えば：

    ![delete fast example](/media/ttl/delete-fast.png)

    TTL ジョブにおけるスキャンと削除の割合はマシンの構成とデータ分散に関連しているため、各瞬間の監視データは実行中の TTL ジョブを表すだけです。テーブル`mysql.tidb_ttl_job_history`を読み取ると、特定の時点で実行されている TTL ジョブと、そのジョブに対応するテーブルを判断できます。

-   `tidb_ttl_scan_worker_count`と`tidb_ttl_delete_worker_count`適切に設定するにはどうすればよいですか?

    1.  「TTL タスクのボトルネックがスキャンまたは削除にあるかどうかを判断するには?」という質問を参照してください。 `tidb_ttl_scan_worker_count`または`tidb_ttl_delete_worker_count`のどちらの値を増やすかを検討します。
    2.  TiKV ノードの数が多い場合、値`tidb_ttl_scan_worker_count`を増やすと、TTL タスクのワークロードのバランスがより良くなります。

    TTL ワーカーが多すぎると大きな負荷がかかるため、TiDB の CPU レベルと TiKV のディスクと CPU の使用率を合わせて評価する必要があります。さまざまなシナリオやニーズ (TTL をできるだけ高速化する必要があるか、他のクエリに対する TTL の影響を軽減する必要があるか) に応じて、 `tidb_ttl_scan_worker_count`と`tidb_ttl_delete_worker_count`の値を調整して、TTL スキャンと削除の速度を向上させることができます。 TTL タスクによってもたらされるパフォーマンスへの影響を軽減します。

</CustomContent>
<CustomContent platform="tidb-cloud">

-   `tidb_ttl_scan_worker_count`と`tidb_ttl_delete_worker_count`適切に設定するにはどうすればよいですか?

    TiKV ノードの数が多い場合、値`tidb_ttl_scan_worker_count`を増やすと、TTL タスクのワークロードのバランスがより良くなります。

    ただし、TTL ワーカーが多すぎると大きな負荷がかかるため、TiDB の CPU レベルと TiKV のディスクと CPU の使用率を合わせて評価する必要があります。さまざまなシナリオやニーズ (TTL をできるだけ高速化する必要があるか、他のクエリに対する TTL の影響を軽減する必要があるか) に応じて、 `tidb_ttl_scan_worker_count`と`tidb_ttl_delete_worker_count`の値を調整して、TTL スキャンと削除の速度を向上させることができます。 TTL タスクによってもたらされるパフォーマンスへの影響を軽減します。

</CustomContent>
