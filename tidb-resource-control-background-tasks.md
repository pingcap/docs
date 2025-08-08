---
title: Use Resource Control to Manage Background Tasks
summary: リソース制御を通じてバックグラウンド タスクを制御する方法を紹介します。
---

# リソース制御を使用してバックグラウンドタスクを管理する {#use-resource-control-to-manage-background-tasks}

> **警告：**
>
> この機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://docs.pingcap.com/tidb/stable/support)報告を行ってください。
>
> リソース制御におけるバックグラウンドタスク管理は、TiKVによるCPU/IO使用率のリソースクォータの動的調整に基づいています。そのため、各インスタンスの利用可能なリソースクォータに依存します。複数のコンポーネントまたはインスタンスを単一のサーバーにデプロイする場合、 `cgroup`を通じて各インスタンスに適切なリソースクォータを設定する必要があります。TiUP PlaygroundなどのTiUPリソースとのデプロイでは、期待される効果を得ることが困難です。

> **注記：**
>
> この機能は[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでは利用できません。

データのバックアップや自動統計収集などのバックグラウンドタスクは、優先度が低いにもかかわらず、多くのリソースを消費します。これらのタスクは通常、定期的または不定期に実行されます。実行中は多くのリソースを消費するため、オンラインの高優先度タスクのパフォーマンスに影響を与えます。

バージョン7.4.0以降、 [TiDB リソース制御](/tidb-resource-control-ru-groups.md)機能はバックグラウンドタスクの管理をサポートします。タスクがバックグラウンドタスクとしてマークされると、TiKVは他のフォアグラウンドタスクのパフォーマンスへの影響を回避するため、このタイプのタスクで使用されるリソースを動的に制限します。TiKVは、すべてのフォアグラウンドタスクによって消費されるCPUおよびIOリソースをリアルタイムで監視し、インスタンスの合計リソース制限に基づいて、バックグラウンドタスクで使用できるリソースしきい値を計算します。すべてのバックグラウンドタスクは、実行中にこのしきい値によって制限されます。

## <code>BACKGROUND</code>パラメータ {#code-background-code-parameters}

-   `TASK_TYPES` : バックグラウンドタスクとして管理する必要があるタスクの種類を指定します。複数のタスクの種類を指定する場合は、カンマ ( `,` ) で区切ります。
-   `UTILIZATION_LIMIT` : 各 TiKV ノード上でバックグラウンドタスクが消費できるリソースの最大割合（0～100）を制限します。デフォルトでは、TiKV はノードの総リソースとフォアグラウンドタスクが現在占有しているリソースに基づいて、バックグラウンドタスクに利用可能なリソースを計算します`UTILIZATION_LIMIT`に設定すると、バックグラウンドタスクに割り当てられるリソースはこの制限を超えません。

TiDB は次の種類のバックグラウンド タスクをサポートしています。

<CustomContent platform="tidb">

-   `lightning` : [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用してインポートタスクを実行します。TiDB TiDB Lightningの物理インポートモードと論理インポートモードの両方がサポートされています。
-   `br` : [BR](/br/backup-and-restore-overview.md)を使用してバックアップおよび復元タスクを実行します。PITR はサポートされていません。
-   `ddl` : Reorg DDL のバッチ データ書き戻しフェーズ中のリソース使用量を制御します。
-   `stats` : 手動で実行されるか、TiDB によって自動的にトリガーされる[統計を収集する](/statistics.md#collect-statistics)タスク。
-   `background` : 予約済みのタスクタイプ。システム変数[`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-new-in-v740)使用して、現在のセッションのタスクタイプを`background`に指定できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `lightning` : [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)を使用してインポートタスクを実行します。TiDB TiDB Lightningの物理インポートモードと論理インポートモードの両方がサポートされています。
-   `br` : [BR](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)を使用してバックアップおよび復元タスクを実行します。PITR はサポートされていません。
-   `ddl` : Reorg DDL のバッチ データ書き戻しフェーズ中のリソース使用量を制御します。
-   `stats` : 手動で実行されるか、TiDB によって自動的にトリガーされる[統計を収集する](/statistics.md#collect-statistics)タスク。
-   `background` : 予約済みのタスクタイプ。システム変数[`tidb_request_source_type`](/system-variables.md#tidb_request_source_type-new-in-v740)使用して、現在のセッションのタスクタイプを`background`に指定できます。

</CustomContent>

デフォルトでは、バックグラウンドタスクとしてマークされているタスクタイプは`""`で、バックグラウンドタスクの管理は無効になっています。バックグラウンドタスクの管理を有効にするには、リソースグループ`default`のバックグラウンドタスクタイプを手動で変更する必要があります。バックグラウンドタスクが識別され、マッチングされると、リソース制御が自動的に実行されます。つまり、システムリソースが不足している場合、バックグラウンドタスクの優先度は自動的に最低に下げられ、フォアグラウンドタスクの実行が確保されます。

> **注記：**
>
> 現在、すべてのリソースグループのバックグラウンドタスクは`default`リソースグループにバインドされています。3 を通じてバックグラウンドタスクの種類をグローバルに管理できます。他`default`リソースグループへのバックグラウンドタスクのバインドは現在サポートされていません。

## 例 {#examples}

1.  `br`と`ddl`バックグラウンド タスクとしてマークし、バックグラウンド タスクのリソース制限を 30% に設定して、リソース グループ`default`を変更します。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES='br,ddl', UTILIZATION_LIMIT=30);
    ```

2.  `default`リソース グループを変更して、バックグラウンド タスクの種類を既定値に戻します。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=NULL;
    ```

3.  `default`リソースグループを変更して、バックグラウンドタスクの種類を空に設定します。この場合、このリソースグループのすべてのタスクはバックグラウンドタスクとして扱われません。

    ```sql
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="");
    ```

4.  `default`リソース グループのバックグラウンド タスクの種類をビュー。

    ```sql
    SELECT * FROM information_schema.resource_groups WHERE NAME="default";
    ```

    出力は次のようになります。

        +---------+------------+----------+-----------+-------------+-------------------------------------------+
        | NAME    | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND                                |
        +---------+------------+----------+-----------+-------------+-------------------------------------------+
        | default | UNLIMITED  | MEDIUM   | YES       | NULL        | TASK_TYPES='br,ddl', UTILIZATION_LIMIT=30 |
        +---------+------------+----------+-----------+-------------+-------------------------------------------+

5.  現在のセッションのタスクを明示的にバックグラウンドタイプとしてマークするには、 `tidb_request_source_type`使用してタスクタイプを明示的に指定します。例を以下に示します。

    ```sql
    SET @@tidb_request_source_type="background";
    /* Add background task type */
    ALTER RESOURCE GROUP `default` BACKGROUND=(TASK_TYPES="background");
    /* Execute LOAD DATA in the current session */
    LOAD DATA INFILE "s3://resource-control/Lightning/test.customer.aaaa.csv"
    ```
