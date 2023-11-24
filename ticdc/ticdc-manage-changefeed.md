---
title: Manage Changefeeds
summary: Learn how to manage TiCDC changefeeds.
---

# 変更フィードの管理 {#manage-changefeeds}

このドキュメントでは、TiCDC コマンドライン ツール`cdc cli`を使用して TiCDC 変更フィードを作成および管理する方法について説明します。 TiCDC の HTTP インターフェイスを介して変更フィードを管理することもできます。詳細は[TiCDC OpenAPI](/ticdc/ticdc-open-api.md)を参照してください。

## レプリケーションタスクを作成する {#create-a-replication-task}

次のコマンドを実行してレプリケーション タスクを作成します。

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"upstream_id":7178706266519722477,"namespace":"default","id":"simple-replication-task","sink_uri":"mysql://root:xxxxx@127.0.0.1:4000/?time-zone=","create_time":"2022-12-19T15:05:46.679218+08:00","start_ts":438156275634929669,"engine":"unified","config":{"case_sensitive":true,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":true,"bdr_mode":false,"sync_point_interval":30000000000,"sync_point_retention":3600000000000,"filter":{"rules":["test.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v6.5.0"}
```

## レプリケーションタスクリストのクエリ {#query-the-replication-task-list}

次のコマンドを実行して、レプリケーション タスク リストをクエリします。

```shell
cdc cli changefeed list --server=http://10.0.10.25:8300
```

```shell
[{
    "id": "simple-replication-task",
    "summary": {
      "state": "normal",
      "tso": 417886179132964865,
      "checkpoint": "2020-07-07 16:07:44.881",
      "error": null
    }
}]
```

-   `checkpoint` 、この時点より前に TiCDC がすでにデータをダウンストリームに複製していたことを示します。
-   `state`レプリケーション タスクの状態を示します。
    -   `normal` : レプリケーションタスクは正常に実行されます。
    -   `stopped` : レプリケーション タスクは停止されています (手動で一時停止されています)。
    -   `error` : レプリケーションタスクは（エラーにより）停止されています。
    -   `removed` : レプリケーションタスクは削除されます。この状態のタスクは、 `--all`オプションを指定した場合にのみ表示されます。このオプションが指定されていない場合にこれらのタスクを表示するには、 `changefeed query`コマンドを実行します。
    -   `finished` : レプリケーション タスクが終了しました (データは`target-ts`にレプリケートされます)。この状態のタスクは、オプション`--all`を指定した場合にのみ表示されます。このオプションが指定されていない場合にこれらのタスクを表示するには、 `changefeed query`コマンドを実行します。

## 特定のレプリケーションタスクをクエリする {#query-a-specific-replication-task}

特定のレプリケーション タスクをクエリするには、 `changefeed query`コマンドを実行します。クエリ結果には、タスク情報とタスクの状態が含まれます。 `--simple`または`-s`引数を指定すると、基本的なレプリケーション状態とチェックポイント情報のみを含むクエリ結果を簡素化できます。この引数を指定しない場合は、詳細なタスク構成、レプリケーション状態、レプリケーションテーブル情報が出力されます。

```shell
cdc cli changefeed query -s --server=http://10.0.10.25:8300 --changefeed-id=simple-replication-task
```

```shell
{
 "state": "normal",
 "tso": 419035700154597378,
 "checkpoint": "2020-08-27 10:12:19.579",
 "error": null
}
```

前述のコマンドと結果は次のようになります。

-   `state`は、現在の変更フィードのレプリケーション状態です。各状態は`changefeed list`の状態と一致している必要があります。
-   `tso`ダウンストリームに正常にレプリケートされた現在の変更フィード内の最大のトランザクション TSO を表します。
-   `checkpoint`ダウンストリームに正常にレプリケートされた、現在の変更フィード内の最大トランザクション TSO の対応する時間を表します。
-   `error`現在の変更フィードでエラーが発生したかどうかを記録します。

```shell
cdc cli changefeed query --server=http://10.0.10.25:8300 --changefeed-id=simple-replication-task
```

```shell
{
  "info": {
    "sink-uri": "mysql://127.0.0.1:3306/?max-txn-row=20\u0026worker-number=4",
    "opts": {},
    "create-time": "2020-08-27T10:33:41.687983832+08:00",
    "start-ts": 419036036249681921,
    "target-ts": 0,
    "admin-job-type": 0,
    "sort-engine": "unified",
    "sort-dir": ".",
    "config": {
      "case-sensitive": true,
      "enable-old-value": false,
      "filter": {
        "rules": [
          "*.*"
        ],
        "ignore-txn-start-ts": null,
        "ddl-allow-list": null
      },
      "mounter": {
        "worker-num": 16
      },
      "sink": {
        "dispatchers": null,
      },
      "scheduler": {
        "type": "table-number",
        "polling-time": -1
      }
    },
    "state": "normal",
    "history": null,
    "error": null
  },
  "status": {
    "resolved-ts": 419036036249681921,
    "checkpoint-ts": 419036036249681921,
    "admin-job-type": 0
  },
  "count": 0,
  "task-status": [
    {
      "capture-id": "97173367-75dc-490c-ae2d-4e990f90da0f",
      "status": {
        "tables": {
          "47": {
            "start-ts": 419036036249681921
          }
        },
        "operation": null,
        "admin-job-type": 0
      }
    }
  ]
}
```

前述のコマンドと結果は次のようになります。

-   `info`は、クエリされた変更フィードのレプリケーション構成です。
-   `status`は、クエリされた変更フィードのレプリケーション状態です。
    -   `resolved-ts` : 現在の変更フィード内の最大のトランザクション`TS` 。この`TS` TiKV から TiCDC に正常に送信されたことに注意してください。
    -   `checkpoint-ts` : 現在のトランザクション`TS`の中で最大のトランザクション`changefeed` 。この`TS`ダウンストリームに正常に書き込まれていることに注意してください。
    -   `admin-job-type` : チェンジフィードのステータス:
        -   `0` : 正常な状態です。
        -   `1` : タスクは一時停止されています。タスクが一時停止されると、複製されたすべての`processor`が終了します。タスクの構成とレプリケーションのステータスは保持されるため、タスクを`checkpiont-ts`から再開できます。
        -   `2` : タスクが再開されます。レプリケーション タスクは`checkpoint-ts`から再開されます。
        -   `3` : タスクは削除されます。タスクが削除されると、複製されたすべての`processor`が終了し、複製タスクの構成情報がクリアされます。レプリケーション ステータスのみが後のクエリのために保持されます。
-   `task-status`クエリされた変更フィード内の各レプリケーション サブタスクの状態を示します。

## レプリケーションタスクを一時停止する {#pause-a-replication-task}

次のコマンドを実行して、レプリケーション タスクを一時停止します。

```shell
cdc cli changefeed pause --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

前述のコマンドでは次のようになります。

-   `--changefeed-id=uuid`一時停止するレプリケーション タスクに対応する変更フィードの ID を表します。

## レプリケーションタスクを再開する {#resume-a-replication-task}

次のコマンドを実行して、一時停止したレプリケーション タスクを再開します。

```shell
cdc cli changefeed resume --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

-   `--changefeed-id=uuid`再開するレプリケーション タスクに対応する変更フィードの ID を表します。
-   `--overwrite-checkpoint-ts` : v6.2.0 以降、レプリケーション タスクを再開する開始 TSO を指定できます。 TiCDC は、指定された TSO からのデータのプルを開始します。引数は`now`または特定の TSO (434873584621453313 など) を受け入れます。指定された TSO は、(GC セーフ ポイント, CurrentTSO] の範囲内にある必要があります。この引数が指定されていない場合、TiCDC はデフォルトで現在の`checkpoint-ts`からデータを複製します。
-   `--no-confirm` : レプリケーション再開時に関連情報を確認する必要はありません。デフォルトは`false`です。

> **注記：**
>
> -   `--overwrite-checkpoint-ts` ( `t2` ) で指定された TSO が、変更フィード ( `t1` ) の現在のチェックポイント TSO より大きい場合、 `t1`と`t2`の間のデータはダウンストリームにレプリケートされません。これにより、データ損失が発生します。 `cdc cli changefeed query`実行すると`t1`取得できます。
> -   `--overwrite-checkpoint-ts` ( `t2` ) で指定された TSO が、変更フィード ( `t1` ) の現在のチェックポイント TSO より小さい場合、TiCDC は古い時点からデータをプルします ( `t2` )。これにより、データの重複が発生する可能性があります (たとえば、ダウンストリームが MQ シンクの場合) ）。

## レプリケーションタスクを削除する {#remove-a-replication-task}

次のコマンドを実行して、レプリケーション タスクを削除します。

```shell
cdc cli changefeed remove --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

前述のコマンドでは次のようになります。

-   `--changefeed-id=uuid`削除するレプリケーション タスクに対応する変更フィードの ID を表します。

## タスク構成を更新する {#update-task-configuration}

TiCDC は、レプリケーション タスクの構成の変更をサポートします (動的ではありません)。変更フィード構成を変更するには、タスクを一時停止し、構成を変更してからタスクを再開します。

```shell
cdc cli changefeed pause -c test-cf --server=http://10.0.10.25:8300
cdc cli changefeed update -c test-cf --server=http://10.0.10.25:8300 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-number=8" --config=changefeed.toml
cdc cli changefeed resume -c test-cf --server=http://10.0.10.25:8300
```

現在、次の構成項目を変更できます。

-   チェンジフィードの`sink-uri` 。
-   変更フィード構成ファイルとそのファイル内のすべての構成項目。
-   チェンジフィードの`target-ts` 。

## レプリケーションサブタスクの処理単位を管理する ( <code>processor</code> ) {#manage-processing-units-of-replication-sub-tasks-code-processor-code}

-   `processor`リストをクエリします。

    ```shell
    cdc cli processor list --server=http://10.0.10.25:8300
    ```

    ```shell
    [
            {
                    "id": "9f84ff74-abf9-407f-a6e2-56aa35b33888",
                    "capture-id": "b293999a-4168-4988-a4f4-35d9589b226b",
                    "changefeed-id": "simple-replication-task"
            }
    ]
    ```

-   特定のレプリケーション タスクのステータスに対応する特定の変更フィードをクエリします。

    ```shell
    cdc cli processor query --server=http://10.0.10.25:8300 --changefeed-id=simple-replication-task --capture-id=b293999a-4168-4988-a4f4-35d9589b226b
    ```

    ```shell
    {
      "status": {
        "tables": {
          "56": {    # 56 ID of the replication table, corresponding to tidb_table_id of a table in TiDB
            "start-ts": 417474117955485702
          }
        },
        "operation": null,
        "admin-job-type": 0
      },
      "position": {
        "checkpoint-ts": 417474143881789441,
        "resolved-ts": 417474143881789441,
        "count": 0
      }
    }
    ```

    前述のコマンドでは次のようになります。

    -   `status.tables` : 各キー番号はレプリケーション テーブルの ID を表し、TiDB 内のテーブルの`tidb_table_id`に対応します。
    -   `resolved-ts` : 現在のプロセッサでソートされたデータの中で最大の TSO。
    -   `checkpoint-ts` : 現在のプロセッサのダウンストリームに正常に書き込まれた最大の TSO。

## 行変更イベントの履歴値を出力します。 {#output-the-historical-value-of-a-row-changed-event}

デフォルト構成では、レプリケーション タスクの TiCDC オープン プロトコル出力の行変更イベントには、変更された値のみが含まれ、変更前の値は含まれません。したがって、出力値は、TiCDC オープン プロトコルのコンシューマー側で行変更イベントの履歴値として使用できません。

v4.0.5 以降、TiCDC は行変更イベントの履歴値の出力をサポートします。この機能を有効にするには、ルート レベルの変更フィード構成ファイルで次の構成を指定します。

```toml
enable-old-value = true
```

この機能は、v5.0 以降、デフォルトで有効になっています。この機能を有効にした後の TiCDC オープン プロトコルの出力形式については、 [TiCDC オープン プロトコル - 行変更イベント](/ticdc/ticdc-open-protocol.md#row-changed-event)を参照してください。

## 照合順序の新しいフレームワークを有効にしてテーブルをレプリケートする {#replicate-tables-with-the-new-framework-for-collations-enabled}

v4.0.15、v5.0.4、v5.1.1、および v5.2.0 以降、TiCDC は[照合順序の新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)を有効にしたテーブルをサポートします。

## 有効なインデックスのないテーブルをレプリケートする {#replicate-tables-without-a-valid-index}

v4.0.8 以降、TiCDC はタスク構成を変更することで、有効なインデックスを持たないテーブルの複製をサポートします。この機能を有効にするには、changefeed 構成ファイルで次のように構成します。

```toml
enable-old-value = true
force-replicate = true
```

> **警告：**
>
> 有効なインデックスのないテーブルの場合、 `INSERT`や`REPLACE`などの操作は再入可能ではないため、データの冗長性が生じるリスクがあります。 TiCDC は、レプリケーション プロセス中にデータが少なくとも 1 回だけ配布されることを保証します。したがって、この機能を有効にして有効なインデックスのないテーブルを複製すると、確実にデータの冗長性が生じます。データの冗長性を受け入れない場合は、 `AUTO RANDOM`属性を持つ主キー列を追加するなど、効果的なインデックスを追加することをお勧めします。

## 統合ソーター {#unified-sorter}

> **注記：**
>
> v6.0.0 以降、TiCDC はデフォルトで DB ソーター エンジンを使用し、統合ソーターを使用しなくなりました。 `sort engine`項目は設定しないことをお勧めします。

統合ソーターは、TiCDC のソート エンジンです。次のシナリオによって引き起こされる OOM 問題を軽減できます。

-   TiCDC のデータ複製タスクは長時間停止され、その間に大量の増分データが蓄積され、複製する必要があります。
-   データ複製タスクは早いタイムスタンプから開始されるため、大量の増分データを複製する必要があります。

v4.0.13 以降`cdc cli`使用して作成された変更フィードの場合、統合ソーターはデフォルトで有効になっています。 v4.0.13 より前に存在していた変更フィードの場合は、以前の構成が使用されます。

統合ソーター機能が変更フィードで有効になっているかどうかを確認するには、次のコマンド例を実行できます (PD インスタンスの IP アドレスが`http://10.0.10.25:2379`であると仮定します)。

```shell
cdc cli --server="http://10.0.10.25:8300" changefeed query --changefeed-id=simple-replication-task | grep 'sort-engine'
```

上記のコマンドの出力で、値`sort-engine`が「unified」の場合、変更フィードで統合ソーターが有効になっていることを意味します。

> **注記：**
>
> -   サーバーが機械式ハード ドライブや、レイテンシーが長い、または帯域幅が制限されているその他のstorageデバイスを使用している場合、Unified Sorter のパフォーマンスは大きな影響を受けます。
> -   デフォルトでは、Unified Sorter は一時ファイルの保存に`data_dir`を使用します。ディスクの空き容量が 500 GiB 以上であることを確認することをお勧めします。本番環境の場合、各ノードの空きディスク容量が (ビジネスで許容される最大`checkpoint-ts`遅延) * (ビジネスのピーク時のアップストリーム書き込みトラフィック) よりも大きいことを確認することをお勧めします。さらに、 `changefeed`の作成後に大量の履歴データをレプリケートする予定がある場合は、各ノードの空き領域がレプリケートされたデータの量よりも大きいことを確認してください。
