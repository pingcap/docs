---
title: TiDB Dashboard Cluster Diagnostic Page
summary: TiDB Dashboardのクラスタ診断機能は、クラスタの問題を診断し、結果をWebページにまとめます。ダッシュボードまたはブラウザからこのページにアクセスできます。指定した期間の診断レポートと比較レポートを生成します。履歴レポートも利用可能です。
---

# TiDB Dashboardのクラスタ診断ページ {#tidb-dashboard-cluster-diagnostics-page}

TiDB Dashboardのクラスタ診断機能は、指定された時間範囲内でクラスタに存在する可能性のある問題を診断し、診断結果とクラスタ関連の負荷監視情報を診断レポートにまとめます。この診断レポートはウェブページ形式で提供されます。ブラウザからページを保存した後、オフラインでページを閲覧したり、このページのリンクを配布したりできます。

> **Note:**
>
> クラスター診断機能は、クラスターにデプロイされたPrometheusに依存します。この監視コンポーネントのデプロイ方法の詳細については、 [TiUP](/tiup/tiup-overview.md)デプロイメントドキュメントをご覧ください。クラスターに監視コンポーネントがデプロイされていない場合、生成される診断レポートには失敗が表示されます。

## ページにアクセスする {#access-the-page}

クラスター診断ページにアクセスするには、次のいずれかの方法を使用できます。

-   TiDB Dashboardにログインしたら、左側のナビゲーション メニューで**Cluster Diagnostics**をクリックします。

    ![Access Cluster Diagnostics page](/media/dashboard/dashboard-diagnostics-access-v650.png)

-   ブラウザで`http://127.0.0.1:2379/dashboard/#/diagnose`にアクセスしてください。`127.0.0.1:2379`を実際のPDアドレスとポート番号に置き換えてください。

## 診断レポートを生成する {#generate-diagnostic-report}

指定された時間範囲内でクラスターを診断し、クラスターの負荷を確認するには、次の手順に従って診断レポートを生成します。

1.  **Range Start Time**を`2022-05-21 14:40:00`などに設定します。
2.  **Range Duration**を`10 min`などに設定します。
3.  **Start**をクリックします。

![Generate diagnostic report](/media/dashboard/dashboard-diagnostics-gen-report-v650.png)

> **Note:**
>
> レポートの**Range Duration**は1分から60分の範囲にすることをお勧めします。**Range Duration**は60分を超えることはできません。

上記の手順により、 `2022-05-21 14:40:00`から`2022-05-21 14:50:00`の時間範囲の診断レポートが生成されます。 **Start**をクリックすると、以下のインターフェースが表示されます。 **Progress**は診断レポートの進行状況バーです。レポートが生成されたら、 **View Full Report**をクリックしてください。

![Report progress](/media/dashboard/dashboard-diagnostics-gen-process-v650.png)

## 比較レポートを生成する {#generate-comparison-report}

特定の時点でシステム例外が発生した場合（例えば、QPSジッターやレイテンシーの上昇など）、診断レポートを生成できます。このレポートでは、異常な時間帯のシステムと正常な時間帯のシステムを比較します。例えば、

-   異常時間範囲: `2022-05-21 14:40:00` - `2022-05-21 14:45:00`この時間範囲内では、システムは異常です。
-   正常な時間範囲: `2022-05-21 14:30:00` - `2022-05-21 14:35:00`この時間範囲内では、システムは正常です。

前の 2 つの時間範囲の比較レポートを生成するには、次の手順に従います。

1.  システムが異常になる範囲の開始時刻である**Range Start Time**（例： `2022-05-21 14:40:00` ）を設定します。
2.  **Range Duration**を設定します。通常、この期間はシステム異常の継続時間（5分など）です。
3.  **Compare by Baseline**を有効にします。
4.  **Baseline Range Start Time**を設定します。これは、システムが正常である範囲（比較対象）の開始時刻（ `2022-05-21 14:30:00`など）です。
5.  **Start**をクリックします。

![Generate comparison report](/media/dashboard/dashboard-diagnostics-gen-compare-report-v650.png)

次に、レポートが生成されるのを待って、 **View Full Report**をクリックします。

さらに、診断レポートのメインページのリストには、過去の診断レポートが表示されます。クリックすると、これらの過去のレポートを直接表示できます。
