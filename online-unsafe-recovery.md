---
title: Online Unsafe Recovery
summary: Learn how to use Online Unsafe Recovery.
---

# オンラインの安全でないリカバリ {#online-unsafe-recovery}

> **警告：**
>
> オンラインの安全でないリカバリは、損失を伴うリカバリの一種です。この機能を使用すると、データとデータ インデックスの整合性は保証されません。

レプリカが永久に破損し、TiKV 上のデータの一部が読み取りおよび書き込み不能になった場合は、オンライン安全でないリカバリ機能を使用して、損失を伴うリカバリ操作を実行できます。

## 機能の説明 {#feature-description}

TiDB では、ユーザーが定義したレプリカ ルールに従って、同じデータが複数のストアに同時に保存される場合があります。これにより、1 つまたは少数のストアが一時的にオフラインになったり破損したりしても、データは引き続き読み取りおよび書き込み可能であることが保証されます。ただし、リージョンのほとんどまたはすべてのレプリカが短期間にオフラインになると、リージョンは一時的に使用できなくなり、読み取りまたは書き込みができなくなります。

データ範囲の複数のレプリカで永久的な損傷 (ディスク損傷など) などの問題が発生し、これらの問題によりストアがオフラインのままになったとします。この場合、このデータ範囲は一時的に利用できなくなります。クラスターを使用状態に戻し、データの巻き戻しやデータ損失を許容する場合は、理論的には、失敗したレプリカをグループから手動で削除することで、大部分のレプリカを再形成できます。これにより、アプリケーション層サービスがこのデータ範囲 (古いか空である可能性があります) を再び読み書きできるようになります。

この場合、損失耐性のあるデータを含む一部のストアが永続的に破損した場合は、オンライン安全でないリカバリを使用して損失を伴うリカバリ操作を実行できます。この機能を使用すると、PD はリージョンのスケジューリング (分割とマージを含む) を自動的に一時停止し、すべてのストアからデータ シャードのメタデータを収集し、グローバルな観点からリアルタイムで完全な復旧計画を生成します。次に、PD は、存続しているすべての店舗に計画を配布して、データ回復タスクを実行させます。さらに、データ復旧計画が配布されると、PD は定期的に復旧の進行状況を監視し、必要に応じて計画を再送信します。

## ユーザーシナリオ {#user-scenarios}

オンラインの安全でないリカバリ機能は、次のシナリオに適しています。

-   ストアが永続的に損傷するとストアが再起動できなくなるため、アプリケーション サービスのデータは読み取りも書き込みもできなくなります。
-   データ損失を受け入れ、影響を受けるデータを読み取りおよび書き込み可能にすることができます。
-   ワンストップのオンライン データ復旧操作を実行したいと考えています。

## 使用法 {#usage}

### 前提条件 {#prerequisites}

オンラインの安全でないリカバリを使用する前に、次の要件が満たされていることを確認してください。

-   実際、オフライン ストアでは一部のデータが利用できなくなります。
-   オフライン ストアは自動的に回復したり再開したりすることはできません。

### ステップ 1. 回復できないストアを指定する {#step-1-specify-the-stores-that-cannot-be-recovered}

自動リカバリをトリガーするには、 PD Controlを使用して[`unsafe remove-failed-stores &#x3C;store_id>[,&#x3C;store_id>,...]`](/pd-control.md#unsafe-remove-failed-stores-store-ids--show)を実行し、リカバリできない**すべての**TiKV ノードをカンマで区切って指定します。

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores <store_id1,store_id2,...>
```

コマンドが`Success`を返した場合、 PD Controlはタスクを PD に正常に登録しています。これは、リクエストが受け入れられたことを意味するだけであり、リカバリが正常に実行されたことを意味するものではありません。回復タスクはバックグラウンドで実行されます。リカバリの進行状況を確認するには、 [`show`](#step-2-check-the-recovery-progress-and-wait-for-the-completion)を使用します。

コマンドが`Failed`を返した場合、 PD Controlはタスクを PD に登録できませんでした。考えられるエラーは次のとおりです。

-   `unsafe recovery is running` : 進行中のリカバリタスクがすでに存在します。
-   `invalid input store x doesn't exist` : 指定されたストアIDは存在しません。
-   `invalid input store x is up and connected` : ID を持つ指定されたストアはまだ正常であるため、回復する必要はありません。

回復タスクの最長許容期間を指定するには、 `--timeout <seconds>`オプションを使用します。このオプションが指定されていない場合、デフォルトでは最長期間は 5 分になります。タイムアウトが発生すると、リカバリは中断され、エラーが返されます。

> **注記：**
>
> -   このコマンドはすべてのピアから情報を収集する必要があるため、メモリ使用量が増加する可能性があります (100,000 ピアが 500 MiB のメモリを使用すると推定されます)。
> -   コマンドの実行中に PD が再起動すると、リカバリが中断されるため、タスクを再度トリガーする必要があります。
> -   コマンドが実行されると、指定されたストアは廃棄状態に設定され、これらのストアを再起動することはできません。
> -   コマンドの実行中は、すべてのスケジュール タスクと分割/マージが一時停止され、リカバリが成功または失敗した後に自動的に再開されます。

### ステップ 2. 回復の進行状況を確認し、完了を待ちます。 {#step-2-check-the-recovery-progress-and-wait-for-the-completion}

上記のストア削除コマンドが正常に実行されたら、 PD Control を使用して[`unsafe remove-failed-stores show`](/pd-control.md#config-show--set-option-value--placement-rules)を実行して削除の進行状況を確認できます。

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores show
```

回復プロセスには複数の段階が考えられます。

-   `collect report` : PD が TiKV からレポートを収集し、グローバル情報を取得する初期段階。
-   `tombstone tiflash learner` : 異常なリージョンのうち、他の正常なピアよりも新しいTiFlashラーナーを削除して、このような極端な状況やpanicの可能性を防ぎます。
-   `force leader for commit merge` : スペシャルステージ。未完了のコミット マージがある場合、極端な状況に備えて、コミット マージのあるリージョンに対して最初に`force leader`が実行されます。
-   `force leader` : 異常なリージョンに、残りの正常なピアの中でRaftリーダーを割り当てるよう強制します。
-   `demote failed voter` : 地域の落選者を学習者に降格し、地域は通常どおりRaftリーダーを選択できるようになります。
-   `create empty region` : キー範囲のスペースを埋める空のリージョンを作成します。これは、一部のリージョンのすべてのレプリカを含むストアが破損している場合を解決するためです。

上記の各段階は、情報、時間、詳細な復旧計画を含む JSON 形式で出力されます。例えば：

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

PD は復旧計画のディスパッチに成功した後、TiKV が実行結果を報告するのを待ちます。上記の出力の最後の段階である`Collecting reports from alive stores`に見られるように、出力のこの部分には、PD による復旧計画のディスパッチと TiKV からのレポートの受信の詳細なステータスが表示されます。

回復プロセス全体には複数の段階が必要で、1 つの段階が複数回再試行される場合があります。通常、推定期間はストアハートビートの 3 ～ 10 周期です (デフォルトでは、ストアハートビートの 1 周期は 10 秒です)。リカバリが完了すると、コマンド出力の最後のステージに`"Unsafe recovery finished"` 、影響を受けるリージョンが属するテーブル ID (リージョンがない場合、または RawKV が使用されている場合、出力にはテーブル ID は表示されません)、および影響を受ける SQL メタが表示されます。地域。例えば：

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

影響を受けるテーブル ID を取得したら、 `INFORMATION_SCHEMA.TABLES`クエリして影響を受けるテーブル名を表示できます。

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, TIDB_TABLE_ID FROM INFORMATION_SCHEMA.TABLES WHERE TIDB_TABLE_ID IN (64, 27);
```

> **注記：**
>
> -   回復作戦により、投票に失敗した人の一部が学習に失敗した人になった。その後、PD スケジューリングでは、これらの失敗した学習者を削除するために時間がかかります。
> -   適時に新しいストアを追加することをお勧めします。

タスク中にエラーが発生した場合、出力の最後のステージに`"Unsafe recovery failed"`とエラー メッセージが表示されます。例えば：

```json
{
    "info": "Unsafe recovery failed: <error>",
    "time": "......"
}
```

### ステップ 3. データとインデックスの一貫性を確認します (RawKV には必要ありません) {#step-3-check-the-consistency-of-data-and-index-not-required-for-rawkv}

> **注記：**
>
> データの読み書きは可能ですが、データの損失がないわけではありません。

リカバリの完了後、データとインデックスに不整合が生じる可能性があります。 SQL コマンド[`ADMIN CHECK`](/sql-statements/sql-statement-admin-check-table-index.md)を使用して、影響を受けるテーブルのデータとインデックスの整合性を確認します。

```sql
ADMIN CHECK TABLE table_name;
```

一貫性のないインデックスがある場合は、古いインデックスの名前を変更し、新しいインデックスを作成して、古いインデックスを削除することで、インデックスの不一致を修正できます。

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

### ステップ 4: 回復不可能なストアを削除する (オプション) {#step-4-remove-unrecoverable-stores-optional}

<SimpleTab>
<div label="Stores deployed using TiUP">

1.  回復不可能なノードを削除します。

    ```bash
    tiup cluster scale-in <cluster-name> -N <host> --force
    ```

2.  トゥームストーン ノードをクリーンアップします。

    ```bash
    tiup cluster prune <cluster-name>
    ```

</div>
<div label="Stores deployed using TiDB Operator">

1.  `PersistentVolumeClaim`を削除します。

    ```bash
    kubectl delete -n ${namespace} pvc ${pvc_name} --wait=false
    ```

2.  TiKV ポッドを削除し、新しく作成された TiKV ポッドがクラスターに参加するまで待ちます。

    ```bash
    kubectl delete -n ${namespace} pod ${pod_name}
    ```

</div>
</SimpleTab>
