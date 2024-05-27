---
title: Online Unsafe Recovery
summary: Online Unsafe Recovery の使用方法を学びます。
---

# オンラインの安全でない回復 {#online-unsafe-recovery}

> **警告：**
>
> オンライン アンセーフ リカバリは、損失を伴うリカバリの一種です。この機能を使用すると、データとデータ インデックスの整合性は保証されません。

レプリカが永久的に破損し、TiKV 上のデータの一部が読み取りおよび書き込み不能になった場合は、オンライン アンセーフ リカバリ機能を使用して、損失を伴うリカバリ操作を実行できます。

## 機能の説明 {#feature-description}

TiDB では、ユーザーが定義したレプリカ ルールに従って、同じデータが複数のストアに同時に保存される場合があります。これにより、1 つまたはいくつかのストアが一時的にオフラインになったり破損したりした場合でも、データの読み取りと書き込みが引き続き可能になります。ただし、リージョンのレプリカのほとんどまたはすべてが短期間にオフラインになると、そのリージョンは一時的に使用できなくなり、読み取りや書き込みができなくなります。

あるデータ範囲の複数のレプリカが永久的な損傷 (ディスクの損傷など) などの問題に遭遇し、これらの問題が原因でストアがオフラインのままになっているとします。この場合、このデータ範囲は一時的に使用できなくなります。クラスターを再び使用し、データの巻き戻しやデータ損失も受け入れる場合は、理論上は、障害が発生したレプリカをグループから手動で削除することで、レプリカの大部分を再編成できます。これにより、アプリケーション レイヤー サービスがこのデータ範囲 (古いか空である可能性があります) を再び読み書きできるようになります。

この場合、損失許容データを含む一部のストアが永久的に破損している場合は、オンライン アンセーフ リカバリを使用して損失のあるリカバリ操作を実行できます。この機能を使用すると、PD はリージョンスケジューリング (分割と結合を含む) を自動的に一時停止し、すべてのストアからデータ シャードのメタデータを収集し、グローバルな観点からリアルタイムで完全なリカバリ プランを生成します。次に、PD はすべての存続ストアにプランを配布して、データ リカバリ タスクを実行させます。さらに、データ リカバリ プランが配布されると、PD は定期的にリカバリの進行状況を監視し、必要に応じてプランを再送信します。

## ユーザーシナリオ {#user-scenarios}

オンライン安全でない回復機能は、次のシナリオに適しています。

-   ストアが永久的に破損すると、ストアを再起動できなくなるため、アプリケーション サービスのデータは読み取りおよび書き込みができなくなります。
-   データの損失を受け入れ、影響を受けるデータを読み取りおよび書き込み可能にすることができます。
-   ワンストップのオンラインデータ復旧操作を実行したい。

## 使用法 {#usage}

### 前提条件 {#prerequisites}

Online Unsafe Recovery を使用する前に、次の要件が満たされていることを確認してください。

-   確かに、オフライン ストアでは一部のデータが利用できなくなります。
-   オフライン ストアは自動的に回復または再起動できません。

### ステップ1. 回復できないストアを指定する {#step-1-specify-the-stores-that-cannot-be-recovered}

自動リカバリをトリガーするには、 PD Controlを使用して[`unsafe remove-failed-stores &#x3C;store_id>[,&#x3C;store_id>,...]`](/pd-control.md#unsafe-remove-failed-stores-store-ids--show)実行し、リカバリできない**すべての**TiKV ノードをカンマで区切って指定します。

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores <store_id1,store_id2,...>
```

コマンドが`Success`を返す場合、 PD Controlはタスクを PD に正常に登録しました。これは、要求が受け入れられたことを意味するだけで、リカバリが正常に実行されたことを意味するわけではありません。リカバリ タスクはバックグラウンドで実行されます。リカバリの進行状況を確認するには、 [`show`](#step-2-check-the-recovery-progress-and-wait-for-the-completion)使用します。

コマンドが`Failed`を返す場合、 PD Controlはタスクを PD に登録できませんでした。考えられるエラーは次のとおりです。

-   `unsafe recovery is running` : 進行中の回復タスクがすでに存在します。
-   `invalid input store x doesn't exist` : 指定されたストアIDは存在しません。
-   `invalid input store x is up and connected` : ID を持つ指定されたストアはまだ正常であり、回復する必要はありません。

リカバリ タスクの最長時間を指定するには、 `--timeout <seconds>`オプションを使用します。このオプションを指定しない場合、最長時間はデフォルトで 5 分になります。タイムアウトが発生すると、リカバリが中断され、エラーが返されます。

> **注記：**
>
> -   このコマンドはすべてのピアから情報を収集する必要があるため、メモリ使用量が増加する可能性があります (100,000 ピアでは 500 MiB のメモリを使用すると推定されます)。
> -   コマンドの実行中に PD が再起動すると、リカバリが中断され、タスクを再度トリガーする必要があります。
> -   コマンドが実行されると、指定されたストアは Tombstone ステータスに設定され、これらのストアを再起動できなくなります。
> -   コマンドの実行中は、すべてのスケジュール タスクと分割/マージが一時停止され、回復が成功または失敗した後に自動的に再開されます。

### ステップ2. 回復の進行状況を確認し、完了するまで待ちます {#step-2-check-the-recovery-progress-and-wait-for-the-completion}

上記のストア削除コマンドが正常に実行されたら、 PD Controlを使用して[`unsafe remove-failed-stores show`](/pd-control.md#config-show--set-option-value--placement-rules)実行し、削除の進行状況を確認できます。

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores show
```

回復プロセスには複数の段階があります。

-   `collect report` : PD が TiKV からレポートを収集し、グローバル情報を取得する初期段階。
-   `tombstone tiflash learner` : 異常な領域のうち、他の正常なピアよりも新しいTiFlash学習者を削除して、このような極端な状況や起こり得るpanicを防ぎます。
-   `force leader for commit merge` : 特別な段階。コミット マージが完了していない場合、極端な状況に備えて、コミット マージのあるリージョンに対して最初に`force leader`実行されます。
-   `force leader` : 正常でないリージョンに、残りの正常なピアの中からRaftリーダーを割り当てるように強制します。
-   `demote failed voter` : リージョンの失敗した投票者を学習者に降格し、その後、リージョンは通常どおりRaftリーダーを選出できます。
-   `create empty region` : キー範囲内のスペースを埋めるために空のリージョンを作成します。これは、一部のリージョンのすべてのレプリカを含むストアが破損しているケースを解決するためのものです。

上記の各ステージは、情報、時間、詳細な復旧計画を含む JSON 形式で出力されます。例:

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

PD はリカバリ プランを正常にディスパッチした後、TiKV が実行結果を報告するのを待機します。上記の出力の最後の段階である`Collecting reports from alive stores`に示されているように、この出力の部分には、PD がリカバリ プランをディスパッチし、TiKV からレポートを受信する詳細なステータスが表示されます。

リカバリプロセス全体は複数のステージを要し、1 つのステージが複数回再試行される可能性があります。通常、推定所要時間はストアハートビートの 3 ～ 10 周期です (ストアハートビートの 1 周期はデフォルトで 10 秒です)。リカバリが完了すると、コマンド出力の最後のステージに`"Unsafe recovery finished"` 、影響を受けるリージョンが属するテーブル ID (存在しない場合、または RawKV が使用されている場合は、出力にテーブル ID は表示されません)、および影響を受ける SQL メタ リージョンが表示されます。例:

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

影響を受けるテーブル ID を取得したら、クエリ`INFORMATION_SCHEMA.TABLES`実行して、影響を受けるテーブル名を表示できます。

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, TIDB_TABLE_ID FROM INFORMATION_SCHEMA.TABLES WHERE TIDB_TABLE_ID IN (64, 27);
```

> **注記：**
>
> -   回復操作により、一部の不合格投票者が不合格学習者になりました。その後、PD スケジュールでは、これらの不合格学習者を削除するのに少し時間が必要です。
> -   新しい店舗を随時追加することをお勧めします。

タスク中にエラーが発生した場合、出力の最後のステージに`"Unsafe recovery failed"`とエラー メッセージが表示されます。例:

```json
{
    "info": "Unsafe recovery failed: <error>",
    "time": "......"
}
```

### ステップ 3. データとインデックスの一貫性をチェックする (RawKV では必要ありません) {#step-3-check-the-consistency-of-data-and-index-not-required-for-rawkv}

> **注記：**
>
> データの読み取りと書き込みは可能ですが、データが失われないということではありません。

リカバリが完了した後、データとインデックスが不整合になる可能性があります。SQLコマンド[`ADMIN CHECK`](/sql-statements/sql-statement-admin-check-table-index.md)を使用して、影響を受けたテーブルのデータとインデックスの整合性を確認してください。

```sql
ADMIN CHECK TABLE table_name;
```

不整合なインデックスがある場合は、古いインデックスの名前を変更し、新しいインデックスを作成してから、古いインデックスを削除することで、インデックスの不整合を修正できます。

1.  古いインデックスの名前を変更します:

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

### ステップ 4: 回復不可能なストアを削除する (オプション) {#step-4-remove-unrecoverable-stores-optional}

<SimpleTab>
<div label="Stores deployed using TiUP">

1.  回復不可能なノードを削除します。

    ```bash
    tiup cluster scale-in <cluster-name> -N <host> --force
    ```

2.  Tombstone ノードをクリーンアップします。

    ```bash
    tiup cluster prune <cluster-name>
    ```

</div>
<div label="Stores deployed using TiDB Operator">

1.  `PersistentVolumeClaim`削除します。

    ```bash
    kubectl delete -n ${namespace} pvc ${pvc_name} --wait=false
    ```

2.  TiKV Pod を削除し、新しく作成された TiKV Pod がクラスターに参加するのを待ちます。

    ```bash
    kubectl delete -n ${namespace} pod ${pod_name}
    ```

</div>
</SimpleTab>
