---
title: TiDB Dashboard Resource Manager Page
summary: TiDBダッシュボードのリソースマネージャページは、クラスタ管理者がリソースグループを作成し、クォータを設定することでリソース分離を実装するのに役立ちます。クラスタ容量を推定し、リソース消費量を監視するための方法を提供します。このページには、TiDBダッシュボードまたはブラウザからアクセスできます。このページには、構成、容量推定、およびメトリックのセクションがあります。容量推定方法には、ハードウェアの展開と実際のワークロードが含まれます。監視メトリックには、消費されたRUの合計、リソースグループによる消費RU、TiDB CPUクォータと使用量、TiKV CPUクォータと使用量、TiKV IO MBpsが含まれます。
---

# TiDBダッシュボードリソースマネージャーページ {#tidb-dashboard-resource-manager-page}

[リソース管理](/tidb-resource-control.md)機能を使用してリソース分離を実装するには、クラスタ管理者がリソースグループを作成し、各グループにクォータを設定する必要があります。リソース計画を行う前に、クラスタ全体の容量を把握しておく必要があります。このドキュメントでは、リソース制御に関する情報を参照することで、リソース計画前にクラスタの容量を見積もり、より効果的にリソースを割り当てることができます。

## ページにアクセスする {#access-the-page}

リソース マネージャー ページにアクセスするには、次の 2 つの方法のいずれかを使用できます。

-   TiDB ダッシュボードにログインしたら、左側のナビゲーション メニューで**[リソース マネージャー] を**クリックします。

-   ブラウザで[http://127.0.0.1:2379/ダッシュボード/#/リソースマネージャー](http://127.0.0.1:2379/dashboard/#/resource_manager)アクセスしてください。3 `127.0.0.1:2379`実際のPDインスタンスのアドレスとポートに置き換えてください。

## リソースマネージャーページ {#resource-manager-page}

次の図は、リソース マネージャーの詳細ページを示しています。

![TiDB Dashboard: Resource Manager](/media/dashboard/dashboard-resource-manager-info.png)

リソース マネージャー ページには、次の 3 つのセクションがあります。

-   コンフィグレーション: このセクションには、TiDBの`RESOURCE_GROUPS`テーブルから取得したデータが表示されます。すべてのリソースグループに関する情報が含まれています。詳細については、 [`RESOURCE_GROUPS`](/information-schema/information-schema-resource-groups.md)参照してください。

-   容量の見積もり：リソース計画を立てる前に、クラスター全体の容量を把握する必要があります。以下のいずれかの方法を使用できます。

    -   [実際の作業負荷に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)
    -   [ハードウェアの展開に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

-   メトリクス: パネル上のメトリクスを観察することで、クラスターの現在の全体的なリソース消費状態を把握できます。

## 容量の見積もり {#estimate-capacity}

リソース計画を立てる前に、クラスター全体の容量を把握しておく必要があります。TiDBは、現在のクラスターの[リクエストユニット（RU）](/tidb-resource-control.md#what-is-request-unit-ru#what-is-request-unit-ru)の容量を見積もる2つの方法を提供しています。

-   [ハードウェアの展開に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-hardware-deployment)

    TiDB は次のワークロード タイプを受け入れます。

    -   `tpcc` : 大量のデータ書き込みを伴うワークロードに適用されます。これは`TPC-C`と同様のワークロードモデルに基づいて推定されます。
    -   `oltp_write_only` : 大量のデータ書き込みを伴うワークロードに適用されます。これは`sysbench oltp_write_only`と同様のワークロードモデルに基づいて推定されます。
    -   `oltp_read_write` : データの読み取りと書き込みが均等なワークロードに適用されます。これは`sysbench oltp_read_write`と同様のワークロードモデルに基づいて推定されます。
    -   `oltp_read_only` : 大量のデータ読み取りを伴うワークロードに適用されます。これは`sysbench oltp_read_only`と同様のワークロードモデルに基づいて推定されます。

    ![Calibrate by Hardware](/media/dashboard/dashboard-resource-manager-calibrate-by-hardware.png)

    **ユーザーリソースグループの合計RUは**、 `default`リソースグループを除くすべてのユーザーリソースグループのRUの合計量を表します。この値が推定容量を超えると、システムはアラートをトリガーします。デフォルトでは、システムは定義済みの`default`リソースグループに無制限の使用量を割り当てます。すべてのユーザーが`default`リソースグループに属している場合、リソースはリソース制御が無効になっている場合と同じように割り当てられます。

-   [実際の作業負荷に基づいて容量を見積もる](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)

    ![Calibrate by Workload](/media/dashboard/dashboard-resource-manager-calibrate-by-workload.png)

    推定期間を10分から24時間まで選択できます。使用されるタイムゾーンはフロントエンドユーザーのタイムゾーンと同じです。

    -   時間ウィンドウの範囲が 10 分から 24 時間の範囲外の場合、次のエラーが表示されます`ERROR 1105 (HY000): the duration of calibration is too short, which could lead to inaccurate output. Please make the duration between 10m0s and 24h0m0s` 。

    -   [実際の作業負荷に基づく容量推定](/sql-statements/sql-statement-calibrate-resource.md#estimate-capacity-based-on-actual-workload)機能の監視メトリックには、 `tikv_cpu_quota` 、 `tidb_server_maxprocs` 、 `resource_manager_resource_unit` 、 `process_cpu_usage`含まれます。CPUクォータ監視データが空の場合、対応する監視メトリック名（例： `Error 1105 (HY000): There is no CPU quota metrics, metrics 'tikv_cpu_quota' is empty` ）にエラーが発生します。

    -   時間枠内のワークロードが低すぎる場合、または`resource_manager_resource_unit`と`process_cpu_usage`監視データが欠落している場合は、エラーが報告されます`Error 1105 (HY000): The workload in selected time window is too low, with which TiDB is unable to reach a capacity estimation; please select another time window with higher workload, or calibrate resource by hardware instead`また、TiKVはmacOSのCPU使用率を監視しないため、実際のワークロードに基づく容量推定をサポートしておらず、このエラーも報告されます。

    [メトリクス](#metrics)セクションの**CPU 使用率**を使用して適切な時間範囲を選択できます。

> **注記：**
>
> 容量推定機能を使用するには、現在のログインユーザーが権限`SUPER`または`RESOURCE_GROUP_ADMIN` 、および一部のシステムテーブルに対する権限`SELECT`持っている必要があります。この機能を使用する前に、現在のユーザーがこれらの権限を持っていることを確認してください。権限がない場合、一部の機能が正しく動作しない可能性があります。詳細については、 [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md#privileges)参照してください。

## メトリクス {#metrics}

パネル上のメトリクスを観察することで、クラスター全体の現在のリソース消費状況を把握できます。監視メトリクスとその意味は次のとおりです。

-   消費された RU の合計: リアルタイムでカウントされた要求ユニットの合計消費量。
-   リソース グループによって消費された RU: リソース グループによってリアルタイムで消費された要求ユニットの数。
-   TiDB
    -   CPU クォータ: TiDB の最大 CPU 使用量。
    -   CPU 使用率: すべての TiDB インスタンスの合計 CPU 使用率。
-   TiKV
    -   CPU クォータ: TiKV の最大 CPU 使用量。
    -   CPU 使用率: すべての TiKV インスタンスの合計 CPU 使用率。
    -   IO MBps: すべての TiKV インスタンスの合計 I/O スループット。
