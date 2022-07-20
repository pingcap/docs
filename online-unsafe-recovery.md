---
title: Online Unsafe Recovery
summary: Learn how to use Online Unsafe Recovery.
---

# オンラインの安全でない回復 {#online-unsafe-recovery}

> **警告：**
>
> オンラインの安全でないリカバリは、損失のあるリカバリの一種です。この機能を使用する場合、データとデータインデックスの整合性は保証されません。

恒久的に損傷したレプリカが原因でTiKV上のデータの一部が読み取りおよび書き込み不能になった場合、オンラインの安全でない回復機能を使用して、不可逆回復操作を実行できます。

## 機能の説明 {#feature-description}

TiDBでは、ユーザーが定義したレプリカルールに従って、同じデータが同時に複数のストアに保存される場合があります。これにより、1つまたはいくつかのストアが一時的にオフラインになったり破損したりした場合でも、データの読み取りと書き込みが可能になります。ただし、リージョンのほとんどまたはすべてのレプリカが短期間にオフラインになると、リージョンは一時的に使用できなくなり、読み取りまたは書き込みができなくなります。

データ範囲の複数のレプリカで永続的な損傷（ディスクの損傷など）などの問題が発生し、これらの問題によってストアがオフラインのままになるとします。この場合、このデータ範囲は一時的に利用できません。クラスタを再び使用し、データの巻き戻しまたはデータの損失も受け入れる場合は、理論的には、障害が発生したレプリカをグループから手動で削除することで、レプリカの大部分を再形成できます。これにより、アプリケーション層サービスは、このデータ範囲（古くなっているか空である可能性があります）を再度読み書きできます。

この場合、損失耐性のあるデータを持つ一部のストアが恒久的に損傷している場合は、OnlineUnsafeRecoveryを使用して損失のある回復操作を実行できます。この機能を使用すると、PDはリージョンのスケジューリング（分割とマージを含む）を自動的に一時停止し、すべてのストアからデータシャードのメタデータを収集し、グローバルな観点から、リアルタイムで完全なリカバリプランを生成します。次に、PDは、存続しているすべてのストアに計画を配布して、データ回復タスクを実行させます。さらに、データ回復計画が配布されると、PDは定期的に回復の進行状況を監視し、必要に応じて計画を再送信します。

## ユーザーシナリオ {#user-scenarios}

オンラインの安全でないリカバリ機能は、次のシナリオに適しています。

-   永続的に破損したストアが原因でストアの再起動に失敗するため、アプリケーションサービスのデータは読み取りおよび書き込みできません。
-   データの損失を受け入れ、影響を受けるデータを読み取りおよび書き込み可能にすることができます。
-   ワンストップのオンラインデータ回復操作を実行したい。

## 使用法 {#usage}

### 前提条件 {#prerequisites}

Online Unsafe Recoveryを使用する前に、次の要件が満たされていることを確認してください。

-   オフラインストアでは、実際に一部のデータが使用できなくなります。
-   オフラインストアを自動的に回復または再開することはできません。

### 手順1.復旧できない店舗を指定する {#step-1-specify-the-stores-that-cannot-be-recovered}

PD Controlを使用して、回復できないTiKVノードを指定し、 [`unsafe remove-failed-stores &#x3C;store_id>[,&#x3C;store_id>,...]`](/pd-control.md#unsafe-remove-failed-stores-store-ids--show)を実行して自動回復をトリガーします。

{{< copyable "" >}}

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores <store_id1,store_id2,...>
```

コマンドが`Success`を返す場合、 PD ControlはタスクをPDに正常に登録しています。これは、要求が受け入れられたことを意味するだけであり、リカバリが正常に実行されたことを意味するものではありません。リカバリタスクはバックグラウンドで実行されます。回復の進行状況を確認するには、 [`show`](#step-2-check-the-recovery-progress-and-wait-for-the-completion)を使用します。

コマンドが`Failed`を返す場合、 PD ControlはタスクをPDに登録できませんでした。考えられるエラーは次のとおりです。

-   `unsafe recovery is running` ：すでに進行中のリカバリタスクがあります。
-   `invalid input store x doesn't exist` ：指定されたストアIDは存在しません。
-   `invalid input store x is up and connected` ：IDを持つ指定されたストアはまだ正常であり、リカバリーされるべきではありません。

リカバリタスクの最長許容期間を指定するには、 `--timeout <seconds>`オプションを使用します。このオプションが指定されていない場合、最長の時間はデフォルトで5分です。タイムアウトが発生すると、リカバリが中断され、エラーが返されます。

> **ノート：**
>
> -   このコマンドはすべてのピアから情報を収集する必要があるため、メモリ使用量が増加する可能性があります（100,000ピアは500 MiBのメモリを使用すると推定されます）。
> -   コマンドの実行中にPDが再始動した場合、リカバリーは中断され、タスクを再度トリガーする必要があります。
> -   コマンドが実行されると、指定されたストアはトゥームストーンステータスに設定され、これらのストアを再開することはできません。
> -   コマンドの実行中は、すべてのスケジューリングタスクと分割/マージが一時停止され、リカバリが成功または失敗した後に自動的に再開されます。

### 手順2.リカバリの進行状況を確認し、完了を待ちます {#step-2-check-the-recovery-progress-and-wait-for-the-completion}

上記のストア削除コマンドが正常に実行されたら、 PD Controlを使用して、 [`unsafe remove-failed-stores show`](/pd-control.md#config-show--set-option-value--placement-rules)を実行することで削除の進行状況を確認できます。

{{< copyable "" >}}

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores show
```

回復プロセスには、複数の可能な段階があります。

-   `collect report` ：PDがTiKVからレポートを収集し、グローバル情報を取得する初期段階。
-   `tombstone tiflash learner` ：不健康な地域の中で、他の健康な仲間よりも新しいTiFlash学習者を削除して、このような極端な状況と起こりうるpanicを防ぎます。
-   `force leader for commit merge` ：特別なステージ。未完了のコミットマージがある場合、極端な状況の場合、最初にコミットマージのあるリージョンで`force leader`が実行されます。
-   `force leader` ：不健康な地域に、残りの健康な仲間の中にRaftリーダーを割り当てるように強制します。
-   `demote failed voter` ：リージョンの失敗した有権者を学習者に降格します。その後、リージョンは通常どおりRaftリーダーを選択できます。
-   `create empty region` ：キー範囲のスペースを埋めるために空の領域を作成します。これは、一部のリージョンのすべてのレプリカを含むストアが破損している場合を解決するためです。

上記の各段階は、情報、時間、詳細な復旧計画を含むJSON形式で出力されます。例えば：

```json
[
    {
        "info": "Unsafe recovery enters collect report stage: failed stores 4, 5, 6",
        "time": "......"
    },
    {
        "info": "Unsafe recovery enters force leader stage",
        "time": "......",
        "actions": {
            "store 1": [
                "force leader on regions: 1001, 1002"
            ],
            "store 2": [
                "force leader on regions: 1003"
            ]
        }
    },
    {
        "info": "Unsafe recovery enters demote failed voter stage",
        "time": "......",
        "actions": {
            "store 1": [
                "region 1001 demotes peers { id:101 store_id:4 }, { id:102 store_id:5 }",
                "region 1002 demotes peers { id:103 store_id:5 }, { id:104 store_id:6 }",
            ],
            "store 2": [
                "region 1003 demotes peers { id:105 store_id:4 }, { id:106 store_id:6 }",
            ]
        }
    },
    {
        "info": "Collecting reports from alive stores(1/3)",
        "time": "......",
        "details": [
            "Stores that have not dispatched plan: ",
            "Stores that have reported to PD: 4",
            "Stores that have not reported to PD: 5, 6",
        ]
    }
]
```

PDはリカバリプランを正常にディスパッチした後、TiKVが実行結果を報告するのを待ちます。上記の出力の最終段階である`Collecting reports from alive stores`でわかるように、出力のこの部分は、PDディスパッチングリカバリプランとTiKVからのレポートの受信の詳細なステータスを示しています。

リカバリプロセス全体には複数の段階があり、1つの段階が複数回再試行される場合があります。通常、推定継続時間はストアハートビートの3〜10期間です（ストアハートビートの1期間はデフォルトで10秒です）。リカバリが完了した後、コマンド出力の最後のステージには`"Unsafe recovery finished"` 、影響を受けるリージョンが属するテーブルID（存在しないか、RawKVが使用されている場合、出力にはテーブルIDは表示されません）、および影響を受けるSQLメタが表示されます。地域。例えば：

```json
{
    "info": "Unsafe recovery finished",
    "time": "......",
    "details": [
        "Affected table ids: 64, 27",
        "Affected meta regions: 1001",
    ]
}
```

> **ノート：**
>
> -   回復作戦は、失敗した有権者の一部を失敗した学習者に変えました。次に、PDスケジューリングは、これらの失敗した学習者を削除するためにしばらく時間が必要です。
> -   時間内に新しい店舗を追加することをお勧めします。

タスク中にエラーが発生した場合、出力の最後のステージに`"Unsafe recovery failed"`とエラーメッセージが表示されます。例えば：

```json
{
    "info": "Unsafe recovery failed: <error>",
    "time": "......"
}
```

### ステップ3.データとインデックスの整合性を確認します（RawKVには必要ありません） {#step-3-check-the-consistency-of-data-and-index-not-required-for-rawkv}

リカバリが完了した後、データとインデックスに一貫性がない可能性があります。 SQLコマンド`ADMIN CHECK` 、および`ADMIN RECOVER`を使用して、影響を受けるテーブルの整合性（ `"Unsafe recovery finished"`の出力からIDを取得でき`ADMIN CLEANUP` ）をチェックして、データの整合性とインデックスの整合性を確認し、テーブルを回復します。

> **ノート：**
>
> データの読み取りと書き込みは可能ですが、データの損失がないことを意味するものではありません。

### ステップ4：回復不能なストアを削除する（オプション） {#step-4-remove-unrecoverable-stores-optional}

<SimpleTab>
<div label="Stores deployed using TiUP">

{{< copyable "" >}}

```bash
tiup cluster prune <cluster-name>
```

</div>
<div label="Stores deployed using TiDB Operator">

1.  `PersistentVolumeClaim`を削除します。

    {{< copyable "" >}}

    ```bash
    kubectl delete -n ${namespace} pvc ${pvc_name} --wait=false
    ```

2.  TiKVポッドを削除し、新しく作成されたTiKVポッドがクラスタに参加するのを待ちます。

    {{< copyable "" >}}

    ```bash
    kubectl delete -n ${namespace} pod ${pod_name}
    ```

</div>
</SimpleTab>
