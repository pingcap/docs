---
title: Upstream and Downstream Clusters Data Validation and Snapshot Read
summary: TiDB アップストリーム クラスターとダウンストリーム クラスターのデータを確認する方法を学習します。
---

# 上流および下流のクラスタのデータ検証とスナップショットの読み取り {#upstream-and-downstream-clusters-data-validation-and-snapshot-read}

TiCDCを使用してTiDBの上流および下流クラスターを構築する場合、レプリケーションを停止することなく、上流および下流で一貫性のあるスナップショット読み取りやデータ整合性検証を実行する必要がある場合があります。通常のレプリケーションモードでは、TiCDCはデータの結果整合性のみを保証しますが、レプリケーションプロセス中のデータの整合性は保証できません。そのため、動的に変化するデータの一貫性読み取りを実行することは困難です。このようなニーズに対応するため、TiCDCはSyncpoint機能を提供します。

SyncpointはTiDBが提供するスナップショット機能を利用し、TiCDCがレプリケーションプロセス中に上流と下流のスナップショット間で一貫性のある`ts-map`を維持できるようにします。これにより、動的データの整合性検証の問題が静的スナップショットデータの整合性検証の問題に変換され、ほぼリアルタイムの検証効果が得られます。

## 同期ポイントを有効にする {#enable-syncpoint}

Syncpoint 機能を有効にすると、 [一貫性のあるスナップショット読み取り](#consistent-snapshot-read)と[データ一貫性検証](#data-consistency-validation)使用できるようになります。

Syncpoint機能を有効にするには、レプリケーションタスクの作成時にTiCDC構成項目の値を`enable-sync-point`から`true`設定します。Syncpointを有効にすると、TiCDCは以下の情報を下流のTiDBクラスターに書き込みます。

1.  レプリケーション中、TiCDC は定期的に ( `sync-point-interval`で設定) アップストリームとダウンストリームの間でスナップショットを調整し、アップストリームとダウンストリームの TSO 対応をダウンストリーム`tidb_cdc.syncpoint_v1`テーブルに保存します。
2.  レプリケーション中、TiCDC は定期的に ( `sync-point-interval`で設定) `SET GLOBAL tidb_external_ts = @@tidb_current_ts`実行し、バックアップ クラスターにレプリケートされた一貫性のあるスナップショット ポイントを設定します。

次の TiCDC 構成例では、レプリケーション タスクの作成時に Syncpoint を有効にします。

```toml
# Enables SyncPoint.
enable-sync-point = true

# Aligns the upstream and downstream snapshots every 5 minutes
sync-point-interval = "5m"

# Cleans up the ts-map data in the downstream tidb_cdc.syncpoint_v1 table every hour
sync-point-retention = "1h"
```

## 一貫性のあるスナップショット読み取り {#consistent-snapshot-read}

> **注記：**
>
> 一貫性のあるスナップショット読み取りを実行する前に、 [同期ポイント機能を有効にしました](#enable-syncpoint)あることを確認してください。複数のレプリケーションタスクが同じ下流 TiDB クラスターを使用し、同期ポイントが有効になっている場合、各タスクはそれぞれのレプリケーションの進行状況に基づいて`tidb_external_ts`と`ts-map`更新します。この場合、 `ts-map`テーブルからレコードを読み取ることで、レプリケーションタスクレベルで一貫性のあるスナップショット読み取りを設定する必要があります。また、下流アプリケーションが`tidb_enable_external_ts_read`使用してデータを読み取ることは避ける必要があります。複数のレプリケーションタスクが互いに干渉し、結果に矛盾が生じる可能性があるためです。

バックアップ クラスターからデータを照会する必要がある場合は、アプリケーションがバックアップ クラスター上でトランザクション的に一貫性のあるデータを取得するように`SET GLOBAL|SESSION tidb_enable_external_ts_read = ON;`設定できます。

さらに、 `ts-map`クエリして、スナップショット読み取りの以前の時点を選択することもできます。

## データ一貫性検証 {#data-consistency-validation}

> **注記：**
>
> データ一貫性検証を実行する前に、 [同期ポイント機能を有効にしました](#enable-syncpoint)あることを確認してください。

アップストリーム クラスターとダウンストリーム クラスターのデータを検証するには、sync-diff-inspector で`snapshot`設定するだけです。

### ステップ1: <code>ts-map</code>を取得する {#step-1-obtain-code-ts-map-code}

ダウンストリームTiDBクラスターで次のSQL文を実行すると、アップストリームTSO（ `primary_ts` ）とダウンストリームTSO（ `secondary_ts` ）を取得できます。

```sql
select * from tidb_cdc.syncpoint_v1;
+------------------+----------------+--------------------+--------------------+---------------------+
| ticdc_cluster_id | changefeed     | primary_ts         | secondary_ts       | created_at          |
+------------------+----------------+--------------------+--------------------+---------------------+
| default          | test-2 | 435953225454059520 | 435953235516456963 | 2022-09-13 08:40:15 |
+------------------+----------------+--------------------+--------------------+---------------------+
```

前述の`syncpoint_v1`表のフィールドの説明は次のとおりです。

-   `ticdc_cluster_id` : このレコード内の TiCDC クラスターの ID。
-   `changefeed` : このレコード内の変更フィードのID。異なるTiCDCクラスターに同じ名前の変更フィードが存在する可能性があるため、変更フィードによって挿入された`ts-map` IDをTiCDCクラスターIDと変更フィードIDで確認する必要があります。
-   `primary_ts` : アップストリーム データベース スナップショットのタイムスタンプ。
-   `secondary_ts` : ダウンストリーム データベース スナップショットのタイムスタンプ。
-   `created_at` : このレコードが挿入された時刻。

### ステップ2: スナップショットを構成する {#step-2-configure-snapshot}

次に、 [ステップ1](#step-1-obtain-ts-map)で取得した`ts-map`情報を使用して、上流データベースと下流データベースのスナップショット情報を設定します。

セクション`Datasource config`の構成例を次に示します。

```toml
######################### Datasource config ########################
[data-sources.uptidb]
    host = "172.16.0.1"
    port = 4000
    user = "root"
    password = ""
    snapshot = "435953225454059520"

[data-sources.downtidb]
    host = "172.16.0.2"
    port = 4000
    user = "root"
    snapshot = "435953235516456963"
```

## 注記 {#notes}

-   TiCDCが変更フィードを作成する前に、TiCDC構成項目`enable-sync-point`の値が`true`に設定されていることを確認してください。この設定によってのみ、同期ポイントが有効になり、 `ts-map`下流に保存されます。構成項目`sync-point-interval`のデフォルト形式は`"h m s"` （例： `"1h30m30s"` ）で、最小値は`"30s"`です。完全な構成情報については、 [TiCDC タスク構成ファイル](/ticdc/ticdc-changefeed-config.md)参照してください。
-   Syncpointを使用してデータ検証を実行する場合、TiKVのガベージコレクション（GC）時間を変更する必要があります。これは、データチェック中にスナップショットに対応する履歴データがGCによって収集されないようにするためです。GC時間を1時間に変更し、チェック後に設定を復元することをお勧めします。
-   上記の例は`Datasource config`の部分のみを示しています。完全な設定については[sync-diff-inspector ユーザーガイド](/sync-diff-inspector/sync-diff-inspector-overview.md)を参照してください。
-   v6.4.0 以降では、権限`SYSTEM_VARIABLES_ADMIN`または`SUPER`持つ changefeed のみが TiCDC Syncpoint 機能を使用できます。
-   v8.2.0 以降、TiCDC は`primary_ts`値の生成ルールに次の調整を加えます。

    -   TiCDC が新しい`primary_ts`生成するときは、その値は`sync-point-interval`の整数倍である必要があります。
    -   TiCDCは新しいチェンジフィードごとに初期値`primary_ts`計算します。この初期値はチェンジフィードの開始時刻（ `startTs` ）以上であり、 `sync-point-interval`の最小の整数倍です。

    この設定は、データレプリケーション中に異なる変更フィードの同期ポイントを揃えるために使用されます。例えば、複数の下流クラスタは、 [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)番目のステートメントを実行することで、同じ`primary_ts`の同期ポイントの`secondary_ts`状態に復元することができ、下流クラスタ間でデータの一貫性が確保されます。
