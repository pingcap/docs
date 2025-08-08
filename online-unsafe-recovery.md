---
title: Online Unsafe Recovery
summary: Online Unsafe Recovery の使用方法を学びます。
---

# オンラインの安全でない回復 {#online-unsafe-recovery}

> **警告：**
>
> オンラインアンセーフリカバリは、非可逆リカバリの一種です。この機能を使用すると、データとデータインデックスの整合性は保証されません。

レプリカが永久的に破損し、TiKV 上のデータの一部が読み取りおよび書き込み不能になった場合は、オンライン非安全リカバリ機能を使用して、損失を伴うリカバリ操作を実行できます。

## 機能の説明 {#feature-description}

TiDBでは、ユーザーが定義したレプリカルールに従って、同じデータが複数のストアに同時に保存される場合があります。これにより、1つまたは少数のストアが一時的にオフラインになったり破損したりした場合でも、データの読み取りと書き込みが引き続き可能になります。ただし、あるリージョンのレプリカのほとんどまたはすべてが短期間でオフラインになった場合、そのリージョンは一時的に利用できなくなり、読み取りも書き込みもできなくなります。

あるデータ範囲の複数のレプリカに永続的な損傷（ディスク損傷など）が発生し、その結果ストアがオフラインになったとします。この場合、このデータ範囲は一時的に利用できなくなります。クラスターを再び使用可能にし、データの巻き戻しやデータ損失を許容する場合、理論上は、障害が発生したレプリカをグループから手動で削除することで、レプリカの大部分を再編成できます。これにより、アプリケーション層サービスは、このデータ範囲（古いか空になっている可能性があります）を再び読み書きできるようになります。

このような場合、損失許容データを含む一部のストアが恒久的に破損した場合、オンラインアンセーフリカバリを使用して、損失を伴うリカバリ操作を実行できます。この機能を使用すると、PDはリージョンのスケジューリング（分割とマージを含む）を自動的に一時停止し、すべてのストアからデータシャードのメタデータを収集し、グローバルな視点からリアルタイムで完全なリカバリプランを生成します。その後、PDは、すべての残存ストアにプランを配布し、データリカバリタスクを実行させます。さらに、データリカバリプランが配布されると、PDは定期的にリカバリの進行状況を監視し、必要に応じてプランを再送信します。

## ユーザーシナリオ {#user-scenarios}

オンライン安全でない回復機能は、次のシナリオに適しています。

-   ストアが永久的に破損すると、ストアを再起動できなくなるため、アプリケーション サービスのデータは読み取りおよび書き込み不能になります。
-   データの損失を受け入れ、影響を受けるデータを読み取りおよび書き込み可能にすることができます。
-   ワンストップのオンラインデータ復旧操作を実行したい。

## 使用法 {#usage}

### 前提条件 {#prerequisites}

Online Unsafe Recovery を使用する前に、次の要件が満たされていることを確認してください。

-   確かに、オフライン ストアでは一部のデータが利用できなくなります。
-   オフライン ストアは自動的に回復または再起動できません。

### ステップ1. 回復できないストアを指定する {#step-1-specify-the-stores-that-cannot-be-recovered}

自動リカバリをトリガーするには、 PD Controlを使用して[`unsafe remove-failed-stores &#x3C;store_id>[,&#x3C;store_id>,...]`](/pd-control.md#unsafe-remove-failed-stores-store-ids--show)実行し、リカバリできない**すべての**TiKV ノードとTiFlashノードをコンマで区切って指定します。

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores <store_id1,store_id2,...>
```

> **注記：**
>
> -   上記のコマンドでは、回復不可能な**すべての**TiKVノードとTiFlashノードが一度に指定されていることを確認してください。回復不可能なノードを省略すると、回復プロセスがブロックされる可能性があります。
> -   短期間内（1 日以内など）にオンライン アンセーフ リカバリを既に実行している場合は、このコマンドの後続の実行に、以前に処理された TiKV ノードとTiFlashノードがまだ含まれていることを確認してください。

リカバリタスクの最長時間を指定するには、 `--timeout <seconds>`オプションを使用します。このオプションを指定しない場合、デフォルトの最長時間は5分です。タイムアウトが発生すると、リカバリは中断され、エラーが返されます。

コマンドが`Success`返した場合、 PD Control はタスクを PD に正常に登録しました。これはリクエストが承認されたことのみを意味し、リカバリが正常に実行されたことを意味するものではありません。リカバリタスクはバックグラウンドで実行されます。リカバリの進行状況を確認するには、 [`show`](#step-2-check-the-recovery-progress-and-wait-for-the-completion)使用してください。

コマンドが`Failed`返す場合、 PD ControlはタスクをPDに登録できませんでした。考えられるエラーは次のとおりです。

-   `unsafe recovery is running` : 進行中の回復タスクがすでに存在します。
-   `invalid input store x doesn't exist` ：指定されたストア ID は存在しません。
-   `invalid input store x is up and connected` : ID を持つ指定されたストアはまだ正常であり、回復する必要はありません。

[`pd-recover`](/pd-recover.md)ような災害復旧操作後にPDが復旧不可能なTiKVノードのストア情報を失い、特定のストアIDが不明になった場合は、 `--auto-detect`モードを使用できます。このモードでは、PDは未登録または以前に登録されたが強制的に削除されたTiKVノードからレプリカを自動的に削除できます。

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores --auto-detect
```

> **注記：**
>
> -   安全でないリカバリではすべてのピアから情報を収集する必要があるため、メモリ使用量が増加する可能性があります (100,000 のピアは 500 MiB のメモリを使用すると推定されます)。
> -   コマンドの実行中に PD が再起動すると、リカバリが中断され、タスクを再度トリガーする必要があります。
> -   コマンドを実行すると、指定されたストアは Tombstone ステータスに設定され、これらのストアを再起動できなくなります。
> -   コマンドの実行中は、すべてのスケジュール タスクと分割/マージが一時停止され、回復が成功または失敗した後に自動的に再開されます。

### ステップ2. 回復の進行状況を確認し、完了を待ちます {#step-2-check-the-recovery-progress-and-wait-for-the-completion}

上記のストア削除コマンドが正常に実行されたら、 PD Controlを使用して[`unsafe remove-failed-stores show`](/pd-control.md#config-show--set-option-value--placement-rules)実行し、削除の進行状況を確認できます。

```bash
pd-ctl -u <pd_addr> unsafe remove-failed-stores show
```

回復プロセスには複数の段階があります。

-   `collect report` : PD が TiKV からレポートを収集し、グローバル情報を取得する初期段階。
-   `tombstone tiflash learner` : 異常な領域のうち、他の正常なピアよりも新しいTiFlash学習者を削除して、このような極端な状況やpanicの可能性を防ぎます。
-   `force leader for commit merge` : 特別な段階。コミットマージが完了していない場合、極端な状況を想定して、コミットマージが行われたリージョンに対してまず`force leader`実行されます。
-   `force leader` : 正常でないリージョンに、残りの正常なピアの中からRaftリーダーを割り当てるように強制します。
-   `demote failed voter` : リージョンの失敗した投票者を学習者に降格し、その後、リージョンは通常どおりRaftリーダーを選出できます。
-   `create empty region` : キー範囲の空き領域を埋めるために空のリージョンを作成します。これは、一部のリージョンのすべてのレプリカを含むストアが破損しているケースを解決するためのものです。

上記の各ステージは、情報、時間、詳細な復旧計画を含むJSON形式で出力されます。例：

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

PDはリカバリプランのディスパッチに成功した後、TiKVからの実行結果の報告を待ちます。上記の出力の最後の段階である`Collecting reports from alive stores`に示されているように、この出力にはPDによるリカバリプランのディスパッチとTiKVからの報告受信の詳細なステータスが表示されています。

リカバリプロセス全体は複数の段階に分かれており、1つの段階が複数回再試行される場合もあります。通常、推定所要時間はストアハートビートの3～10周期分です（ストアハートビートビートの1周期はデフォルトで10秒です）。リカバリが完了すると、コマンド出力の最後の段階に`"Unsafe recovery finished"` 、影響を受けたリージョンが属するテーブルID（テーブルIDがない場合、またはRawKVが使用されている場合は、出力にテーブルIDは表示されません）、および影響を受けたSQLメタリージョンが表示されます。例：

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
> -   回復操作により、一部の投票失敗者が学習失敗者になりました。そのため、PDスケジュールではこれらの学習失敗者を削除するのに時間がかかります。
> -   新しい店舗を随時追加することをお勧めします。

タスク実行中にエラーが発生した場合、出力の最後のステージに`"Unsafe recovery failed"`とエラーメッセージが表示されます。例：

```json
{
    "info": "Unsafe recovery failed: <error>",
    "time": "......"
}
```

### ステップ3. データとインデックスの整合性をチェックする（RawKVの場合は必要ありません） {#step-3-check-the-consistency-of-data-and-index-not-required-for-rawkv}

> **注記：**
>
> データの読み取りおよび書き込みは可能ですが、データの損失がないわけではありません。

リカバリが完了した後、データとインデックスに不整合が発生する可能性があります。SQLコマンド[`ADMIN CHECK`](/sql-statements/sql-statement-admin-check-table-index.md)を使用して、影響を受けたテーブルのデータとインデックスの整合性を確認してください。

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

### ステップ4: 回復不可能なストアを削除する（オプション） {#step-4-remove-unrecoverable-stores-optional}

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

1.  `PersistentVolumeClaim`を削除します。

    ```bash
    kubectl delete -n ${namespace} pvc ${pvc_name} --wait=false
    ```

2.  TiKV ポッドを削除し、新しく作成された TiKV ポッドがクラスターに参加するのを待ちます。

    ```bash
    kubectl delete -n ${namespace} pod ${pod_name}
    ```

</div>
</SimpleTab>
