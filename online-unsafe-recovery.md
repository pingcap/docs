---
title: Online Unsafe Recovery
summary: Learn how to use Online Unsafe Recovery.
---

# オンラインの安全でない回復 {#online-unsafe-recovery}

> **警告：**
>
> Online Unsafe Recovery は、非可逆回復の一種です。この機能を使用する場合、データおよびデータ インデックスの整合性は保証されません。

永久に破損したレプリカにより、TiKV 上のデータの一部が読み取り不能および書き込み不能になった場合、オンラインの安全でない回復機能を使用して、損失のある回復操作を実行できます。

## 機能説明 {#feature-description}

TiDB では、ユーザーが定義したレプリカ ルールに従って、同じデータが同時に複数のストアに格納される場合があります。これにより、1 つまたはいくつかのストアが一時的にオフラインになったり破損したりした場合でも、データの読み取りと書き込みが可能であることが保証されます。ただし、リージョンのほとんどまたはすべてのレプリカが短期間にオフラインになると、リージョンは一時的に使用できなくなり、読み取りまたは書き込みができなくなります。

データ範囲の複数のレプリカで永続的な損傷 (ディスクの損傷など) などの問題が発生し、これらの問題によりストアがオフラインのままになっているとします。この場合、このデータ範囲は一時的に利用できなくなります。クラスターを使用に戻し、データの巻き戻しやデータの損失を受け入れる場合、理論的には、失敗したレプリカをグループから手動で削除することにより、レプリカの大部分を再形成できます。これにより、アプリケーション レイヤー サービスは、このデータ範囲 (古いか空である可能性があります) を再度読み書きできるようになります。

この場合、損失許容データを含む一部のストアが完全に破損した場合、オンラインの安全でない回復を使用して、損失を伴う回復操作を実行できます。この機能を使用すると、PD はリージョンのスケジューリング (分割とマージを含む) を自動的に一時停止し、すべてのストアからデータ シャードのメタデータを収集してから、グローバルな観点から、リアルタイムの完全な復旧計画を生成します。次に、PD は計画をすべての存続しているストアに配布して、データ リカバリ タスクを実行させます。さらに、データ復旧計画が配布されると、PD は定期的に復旧の進行状況を監視し、必要に応じて計画を再送信します。

## ユーザー シナリオ {#user-scenarios}

オンラインの安全でない回復機能は、次のシナリオに適しています。

-   アプリケーション サービスのデータは読み取りも書き込みもできません。これは、ストアが永続的に破損すると、ストアが再起動できなくなるためです。
-   データの損失を受け入れて、影響を受けるデータを読み取りおよび書き込み可能にすることができます。
-   ワンストップのオンライン データ リカバリ操作を実行したい。

## 使用法 {#usage}

### 前提条件 {#prerequisites}

オンラインの安全でない回復を使用する前に、次の要件が満たされていることを確認してください。

-   実際、オフライン ストアによって一部のデータが利用できなくなります。
-   オフライン ストアを自動的に回復または再起動することはできません。

### 手順 1. 復元できないストアを指定する {#step-1-specify-the-stores-that-cannot-be-recovered}

自動回復をトリガーするには、 PD Controlを使用して[`unsafe remove-failed-stores &#x3C;store_id>[,&#x3C;store_id>,...]`](/pd-control.md#unsafe-remove-failed-stores-store-ids--show)実行し、回復できない**すべての**TiKV ノードをカンマで区切って指定します。

{{< copyable "" >}}

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores <store_id1,store_id2,...>
```

コマンドが`Success`を返した場合、 PD Controlはタスクを PD に正常に登録しています。これは、リクエストが受け入れられたことを意味するだけであり、リカバリが正常に実行されたことを意味するものではありません。リカバリ タスクはバックグラウンドで実行されます。回復の進行状況を確認するには、 [`show`](#step-2-check-the-recovery-progress-and-wait-for-the-completion)使用します。

コマンドが`Failed`を返した場合、 PD Controlはタスクを PD に登録できませんでした。考えられるエラーは次のとおりです。

-   `unsafe recovery is running` : 進行中の回復タスクが既に存在します。
-   `invalid input store x doesn't exist` : 指定された店舗IDは存在しません。
-   `invalid input store x is up and connected` : ID で指定されたストアはまだ正常であり、復旧する必要はありません。

回復タスクの最長許容期間を指定するには、 `--timeout <seconds>`オプションを使用します。このオプションが指定されていない場合、最長の期間はデフォルトで 5 分です。タイムアウトが発生すると、リカバリが中断され、エラーが返されます。

> **ノート：**
>
> -   このコマンドはすべてのピアから情報を収集する必要があるため、メモリ使用量が増加する可能性があります (100,000 ピアで 500 MiB のメモリが使用されると推定されます)。
> -   コマンドの実行中に PD が再起動すると、リカバリが中断され、タスクを再度トリガーする必要があります。
> -   コマンドが実行されると、指定されたストアは廃棄状態に設定され、これらのストアを再開することはできません。
> -   コマンドの実行中は、すべてのスケジューリング タスクと分割/マージが一時停止され、復旧が成功または失敗した後に自動的に再開されます。

### ステップ 2. 回復の進行状況を確認し、完了するまで待ちます {#step-2-check-the-recovery-progress-and-wait-for-the-completion}

上記のストア削除コマンドが正常に実行されたら、 PD Control を使用して[`unsafe remove-failed-stores show`](/pd-control.md#config-show--set-option-value--placement-rules)を実行して削除の進行状況を確認できます。

{{< copyable "" >}}

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores show
```

回復プロセスには複数の段階があります。

-   `collect report` : PD が TiKV からレポートを収集し、グローバルな情報を取得する初期段階。
-   `tombstone tiflash learner` : 異常なリージョンの中で、他の正常なピアよりも新しいTiFlashラーナーを削除して、このような極端な状況とpanicの可能性を防ぎます。
-   `force leader for commit merge` : スペシャルステージ。未完了のコミット マージがある場合、極端な状況では、コミット マージのあるリージョンで`force leader`が最初に実行されます。
-   `force leader` : 異常なリージョンに、残りの正常なピアの中からRaftリーダーを割り当てるように強制します。
-   `demote failed voter` : リージョンの失敗した有権者を学習者に降格し、リージョンは通常どおりRaftリーダーを選択できます。
-   `create empty region` : キー範囲のスペースを埋めるために空のリージョンを作成します。これは、一部のリージョンのすべてのレプリカを含むストアが破損した場合を解決するためです。

上記の各段階は、情報、時間、および詳細な復旧計画を含む JSON 形式で出力されます。例えば：

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

PD が復旧計画を正常にディスパッチした後、TiKV が実行結果を報告するのを待ちます。上記の出力の最後の段階である`Collecting reports from alive stores`でわかるように、出力のこの部分には、PD のディスパッチ リカバリ プランと TiKV からのレポートの受信の詳細なステータスが表示されます。

回復プロセス全体には複数の段階があり、1 つの段階が複数回再試行される場合があります。通常、見積もられる期間はストアハートビートの 3 ～ 10 周期です (ストアハートビートの 1 周期はデフォルトで 10 秒です)。リカバリが完了すると、コマンド出力の最後のステージに`"Unsafe recovery finished"` 、影響を受けるリージョンが属するテーブル ID (存在しない場合、または RawKV が使用されている場合、出力にはテーブル ID は表示されません)、および影響を受ける SQL メタが表示されます。地域。例えば：

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

影響を受けるテーブル ID を取得したら、 `INFORMATION_SCHEMA.TABLES`クエリして、影響を受けるテーブル名を表示できます。

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, TIDB_TABLE_ID FROM INFORMATION_SCHEMA.TABLES WHERE TIDB_TABLE_ID IN (64, 27);
```

> **ノート：**
>
> -   回復操作により、一部の失敗した有権者が失敗した学習者になりました。その後、PD スケジューリングでは、これらの失敗した学習者を削除するのに時間がかかります。
> -   時間内に新しい店舗を追加することをお勧めします。

タスク中にエラーが発生した場合、出力の最後の段階に`"Unsafe recovery failed"`とエラー メッセージが表示されます。例えば：

```json
{
    "info": "Unsafe recovery failed: <error>",
    "time": "......"
}
```

### ステップ 3. データとインデックスの一貫性を確認する (RawKV では不要) {#step-3-check-the-consistency-of-data-and-index-not-required-for-rawkv}

> **ノート：**
>
> データは読み書きできますが、データの損失がないわけではありません。

リカバリが完了した後、データとインデックスが矛盾している可能性があります。 SQL コマンド[`ADMIN CHECK`](/sql-statements/sql-statement-admin-check-table-index.md)を使用して、影響を受けるテーブルのデータとインデックスの一貫性を確認します。

```sql
ADMIN CHECK TABLE table_name;
```

一貫性のないインデックスがある場合は、古いインデックスの名前を変更し、新しいインデックスを作成してから古いインデックスを削除することで、インデックスの不整合を修正できます。

1.  古いインデックスの名前を変更します。

    ```sql
    ALTER TABLE table_name RENAME INDEX index_name TO index_name_lame_duck;
    ```

2.  新しいインデックスを作成します。

    ```sql
    ALTER TABLE table_name ADD INDEX index_name (column_name);
    ```

3.  古いインデックスを削除します。

    ```sql
    ALTER TABLE table_name DROP INDEX index_name_lame_duck;
    ```

### 手順 4: 回復不能なストアを削除する (オプション) {#step-4-remove-unrecoverable-stores-optional}

<SimpleTab>
<div label="Stores deployed using TiUP">

1.  回復不能なノードを削除します。

    ```bash
    tiup cluster scale-in <cluster-name> -N <host> --force
    ```

2.  Tombstone ノードをクリーンアップします。

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

2.  TiKV Pod を削除し、新しく作成された TiKV Pod がクラスターに参加するのを待ちます。

    {{< copyable "" >}}

    ```bash
    kubectl delete -n ${namespace} pod ${pod_name}
    ```

</div>
</SimpleTab>
