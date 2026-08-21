---
title: リソースのキャリブレーション
summary: TiDB Cloud Dedicated クラスターの RU 容量を見積もり、リソースグループにリソースを割り当てる方法を学びます。
---

# リソースのキャリブレーション

[Request Unit (RU)](/tidb-resource-control-ru-groups.md#what-is-request-unit-ru) は、システムリソースの消費を表すリソース抽象化単位です。[resource groups](/tidb-resource-control-ru-groups.md) にリソースを割り当てる前に、まずクラスター全体の RU 容量を見積もることを推奨します。

TiDB Cloud Dedicated クラスターでは、TiDB Cloud コンソールの **Monitoring** ページにある **Calibrate Resource** 機能を使用して RU 容量を見積もることができます。この機能は、すべての TiDB Cloud Dedicated クラスターで利用できます。

> **Note:**
>
> 見積もり容量は、ハードウェア仕様または過去の統計に基づいて計算されるため、クラスターの実際の容量と差異が生じる場合があります。

## クラスター容量を見積もる {#estimate-the-cluster-capacity}

1. [**My TiDB**](https://tidbcloud.com/tidbs) ページで、対象のクラスター名をクリックして概要ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、まず左上のコンボボックスを使用して対象の組織に切り替えてください。

2. 左側のナビゲーションペインで **Monitoring** をクリックし、次に **Calibrate Resource** をクリックします。

3. 次のいずれかのキャリブレーション方法を選択します。

    - **Calibrate by Hardware**: 現在のクラスター設定と選択したワークロードモデルに基づいて容量を見積もります。次のワークロードタイプがサポートされており、デフォルトのワークロードタイプは `TPCC` です。

        - `TPCC`: データ書き込みが多いワークロードに適用されます。`TPC-C` に類似したワークロードモデルに基づいて見積もられます。
        - `OLTP_WRITE_ONLY`: データ書き込みが多いワークロードに適用されます。`sysbench oltp_write_only` に類似したワークロードモデルに基づいて見積もられます。
        - `OLTP_READ_WRITE`: データの読み取りと書き込みが均等なワークロードに適用されます。`sysbench oltp_read_write` に類似したワークロードモデルに基づいて見積もられます。
        - `OLTP_READ_ONLY`: データ読み取りが多いワークロードに適用されます。`sysbench oltp_read_only` に類似したワークロードモデルに基づいて見積もられます。

    - **Calibrate by Workload**: 選択した時間枠内の実際のワークロードに基づいて容量を見積もります。時間枠は 10分から 24時間までです。

        選択した時間枠内のワークロードが低すぎる場合、TiDB は容量見積もりを生成できません。この場合は、より高いワークロードの別の時間枠を選択するか、代わりにハードウェアに基づいてリソースをキャリブレーションしてください。

4. 次のカードで見積もり結果を確認します。

    - **Estimated Capacity**: クラスターの推定総 RU 容量です。
    - **Total RU of user resource groups**: `default` リソースグループを除く、すべてのユーザーリソースグループに割り当てられた RU の総量です。この値が推定容量を超えると、システムはアラートをトリガーします。

このページには、クラスターの現在のリソース消費を把握するのに役立つ次のメトリクスチャートも表示されます。

- **Total RU Consumed**: リアルタイムで集計された Request Units の総消費量です。
- **RU Consumed by Resource Groups**: リソースグループごとにリアルタイムで消費された Request Units の数です。

## リソース割り当てを変更する {#change-the-resource-allocation}

リソースグループのリソース割り当てを変更するには、次のステートメントを使用します。

```sql
ALTER RESOURCE GROUP <resource group name> RU_PER_SEC=<#ru> [BURSTABLE];
```

リソースグループの詳細については、[Use Resource Control to Achieve Resource Group Limitation and Flow Control](/tidb-resource-control-ru-groups.md) を参照してください。

## 制限事項 {#limitations}

- `CALIBRATE RESOURCE` ステートメントは TiDB Cloud Dedicated ではサポートされていません。クラスターの RU 容量を見積もるには、TiDB Cloud コンソールの **Calibrate Resource** 機能を使用してください。
- **Calibrate Resource** 機能は TiDB Cloud Dedicated クラスターでのみ利用可能であり、{{{ .starter }}}, {{{ .essential }}}, または {{{ .premium }}} インスタンスでは利用できません。