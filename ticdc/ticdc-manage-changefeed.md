---
title: Manage Changefeeds
summary: TiCDC 変更フィードを管理する方法を学習します。
---

# チェンジフィードを管理する {#manage-changefeeds}

このドキュメントでは、TiCDC コマンドライン ツール`cdc cli`を使用して TiCDC 変更フィードを作成および管理する方法について説明します。また、TiCDC の HTTP インターフェイス経由で変更フィードを管理することもできます。詳細については、 [TiCDC オープンAPI](/ticdc/ticdc-open-api.md)参照してください。

## レプリケーションタスクを作成する {#create-a-replication-task}

レプリケーション タスクを作成するには、次のコマンドを実行します。

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"upstream_id":7178706266519722477,"namespace":"default","id":"simple-replication-task","sink_uri":"mysql://root:xxxxx@127.0.0.1:4000/?time-zone=","create_time":"2024-12-26T15:05:46.679218+08:00","start_ts":438156275634929669,"engine":"unified","config":{"case_sensitive":false,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":true,"bdr_mode":false,"sync_point_interval":30000000000,"sync_point_retention":3600000000000,"filter":{"rules":["test.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v8.1.2"}
```

## レプリケーションタスクリストをクエリする {#query-the-replication-task-list}

レプリケーション タスク リストを照会するには、次のコマンドを実行します。

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

-   `checkpoint` TiCDC がこの時点より前にデータをダウンストリームにすでに複製していることを示します。
-   `state`レプリケーション タスクの状態を示します。
    -   `normal` : レプリケーション タスクは正常に実行されます。
    -   `stopped` : レプリケーション タスクが停止されています (手動で一時停止されています)。
    -   `error` : レプリケーション タスクが停止しました (エラーにより)。
    -   `removed` : レプリケーション タスクは削除されています。この状態のタスクは、 `--all`オプションを指定した場合にのみ表示されます。このオプションを指定していない場合にこれらのタスクを表示するには、 `changefeed query`コマンドを実行します。
    -   `finished` : レプリケーション タスクは終了しました (データは`target-ts`にレプリケートされています)。この状態のタスクは、 `--all`オプションを指定した場合にのみ表示されます。このオプションを指定していない場合にこれらのタスクを表示するには、 `changefeed query`コマンドを実行します。

## 特定のレプリケーションタスクをクエリする {#query-a-specific-replication-task}

特定のレプリケーション タスクをクエリするには、 `changefeed query`コマンドを実行します。クエリ結果には`-s` `--simple`を指定すると、基本的なレプリケーション状態とチェックポイント情報のみを含むクエリ結果が簡略化されます。この引数を指定しないと、詳細なタスク構成、レプリケーション状態、およびレプリケーション テーブル情報が出力されます。

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

上記のコマンドと結果:

-   `state` 、現在の変更フィードのレプリケーション状態です。各状態は`changefeed list`の状態と一致している必要があります。
-   `tso`ダウンストリームに正常に複製された現在の変更フィード内の最大のトランザクション TSO を表します。
-   `checkpoint`ダウンストリームに正常に複製された現在の変更フィード内の最大トランザクション TSO に対応する時間を表します。
-   `error`現在の変更フィードでエラーが発生したかどうかを記録します。

```shell
cdc cli changefeed query --server=http://10.0.10.25:8300 --changefeed-id=simple-replication-task
```

```shell
{
  "info": {
    "sink-uri": "mysql://127.0.0.1:3306/?max-txn-row=20\u0026worker-count=4",
    "opts": {},
    "create-time": "2020-08-27T10:33:41.687983832+08:00",
    "start-ts": 419036036249681921,
    "target-ts": 0,
    "admin-job-type": 0,
    "sort-engine": "unified",
    "sort-dir": ".",
    "config": {
      "case-sensitive": false,
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

上記のコマンドと結果:

-   `info` 、クエリされた変更フィードのレプリケーション構成です。
-   `status` 、クエリされた変更フィードのレプリケーション状態です。
    -   `resolved-ts` : 現在のチェンジフィードにおける最大のトランザクション`TS`この`TS` TiKV から TiCDC に正常に送信されたことに注意してください。
    -   `checkpoint-ts` : 現在の`changefeed`における最大のトランザクション`TS` 。この`TS`ダウンストリームに正常に書き込まれたことに注意してください。
    -   `admin-job-type` : 変更フィードのステータス:
        -   `0` : 状態は正常です。
        -   `1` : タスクは一時停止されています。タスクが一時停止されると、複製された`processor`秒がすべて終了します。タスクの構成とレプリケーション ステータスは保持されるため、 `checkpoint-ts`からタスクを再開できます。
        -   `2` : タスクが再開されます。レプリケーション タスクは`checkpoint-ts`から再開されます。
        -   `3` : タスクが削除されます。タスクが削除されると、すべての`processor`が終了し、レプリケーション タスクの構成情報がクリアされます。レプリケーション ステータスのみが、後のクエリのために保持されます。
-   `task-status`クエリされた変更フィード内の各レプリケーション サブタスクの状態を示します。

## レプリケーションタスクを一時停止する {#pause-a-replication-task}

レプリケーション タスクを一時停止するには、次のコマンドを実行します。

```shell
cdc cli changefeed pause --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

上記のコマンドでは、

-   `--changefeed-id=uuid`一時停止するレプリケーション タスクに対応する変更フィードの ID を表します。

## レプリケーションタスクを再開する {#resume-a-replication-task}

一時停止したレプリケーション タスクを再開するには、次のコマンドを実行します。

```shell
cdc cli changefeed resume --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

-   `--changefeed-id=uuid`再開するレプリケーション タスクに対応する変更フィードの ID を表します。
-   `--overwrite-checkpoint-ts` : v6.2.0 以降では、レプリケーション タスクを再開する開始 TSO を指定できます。TiCDC は、指定された TSO からデータのプルを開始します。引数は`now`または特定の TSO (434873584621453313 など) を受け入れます。指定された TSO は、(GC セーフ ポイント、CurrentTSO] の範囲内である必要があります。この引数が指定されていない場合、TiCDC はデフォルトで現在の`checkpoint-ts`からデータを複製します。
-   `--no-confirm` : レプリケーションが再開されたときに、関連情報を確認する必要はありません。デフォルトは`false`です。

> **注記：**
>
> -   `--overwrite-checkpoint-ts` （ `t2` ）で指定されたTSOがchangefeed（ `t1` ）の現在のチェックポイントTSOよりも大きい場合、 `t1`と`t2`の間のデータは下流に複製されません。これによりデータ損失が発生します。13 `cdc cli changefeed query`実行すると`t1`取得できます。
> -   `--overwrite-checkpoint-ts` （ `t2` ）で指定されたTSOがチェンジフィード（ `t1` ）の現在のチェックポイントTSOよりも小さい場合、TiCDCは古い時点（ `t2` ）からデータをプルし、データの重複が発生する可能性があります（たとえば、ダウンストリームがMQシンクの場合）。

## レプリケーションタスクを削除する {#remove-a-replication-task}

レプリケーション タスクを削除するには、次のコマンドを実行します。

```shell
cdc cli changefeed remove --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

上記のコマンドでは、

-   `--changefeed-id=uuid`削除するレプリケーション タスクに対応する変更フィードの ID を表します。

## タスク構成の更新 {#update-task-configuration}

TiCDC は、レプリケーション タスクの構成の変更をサポートしています (動的ではありません)。changefeed 構成を変更するには、タスクを一時停止し、構成を変更してから、タスクを再開します。

```shell
cdc cli changefeed pause -c test-cf --server=http://10.0.10.25:8300
cdc cli changefeed update -c test-cf --server=http://10.0.10.25:8300 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-count=8" --config=changefeed.toml
cdc cli changefeed resume -c test-cf --server=http://10.0.10.25:8300
```

現在、次の構成項目を変更できます。

-   変更フィードの`sink-uri` 。
-   changefeed 構成ファイルとファイル内のすべての構成項目。
-   チェンジフィードの`target-ts` 。

## レプリケーションサブタスクの処理単位を管理する（ <code>processor</code> ） {#manage-processing-units-of-replication-sub-tasks-code-processor-code}

-   `processor`リストをクエリします:

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

-   特定のレプリケーション タスクのステータスに対応する特定の変更フィードに対してクエリを実行します。

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

    上記のコマンドでは、

    -   `status.tables` : 各キー番号はレプリケーション テーブルの ID を表し、TiDB のテーブルの`tidb_table_id`に相当します。
    -   `resolved-ts` : 現在のプロセッサ内のソートされたデータの中で最大の TSO。
    -   `checkpoint-ts` : 現在のプロセッサでダウンストリームに正常に書き込まれた最大の TSO。

## 照合の新しいフレームワークを有効にしてテーブルを複製する {#replicate-tables-with-the-new-framework-for-collations-enabled}

v4.0.15、v5.0.4、v5.1.1、v5.2.0 以降、TiCDC は[照合のための新しいフレームワーク](/character-set-and-collation.md#new-framework-for-collations)が有効になっているテーブルをサポートします。

## 有効なインデックスのないテーブルを複製する {#replicate-tables-without-a-valid-index}

v4.0.8 以降、TiCDC はタスク構成を変更することで、有効なインデックスを持たないテーブルのレプリケーションをサポートしています。この機能を有効にするには、changefeed 構成ファイルで次のように構成します。

```toml
force-replicate = true
```

> **警告：**
>
> `force-replicate` `true`に設定すると、データの一貫性が保証されません。有効なインデックスのないテーブルの場合、 `INSERT`や`REPLACE`などの操作は再入可能ではないため、データの冗長性が発生するリスクがあります。TiCDC は、レプリケーション プロセス中にデータが少なくとも 1 回だけ配布されることを保証します。そのため、この機能を有効にして有効なインデックスのないテーブルをレプリケートすると、確実にデータの冗長性が発生します。データの冗長性を受け入れない場合は、 `AUTO RANDOM`属性を持つ主キー列を追加するなど、有効なインデックスを追加することをお勧めします。

## 統合ソーター {#unified-sorter}

> **注記：**
>
> v6.0.0 以降、TiCDC はデフォルトで DB Sorter エンジンを使用し、Unified Sorter を使用しなくなりました。1 `sort engine`を構成しないことをお勧めします。

統合ソーターは TiCDC のソート エンジンです。次のシナリオによって発生する OOM の問題を軽減できます。

-   TiCDC のデータ複製タスクは長時間一時停止され、その間に大量の増分データが蓄積され、複製が必要になります。
-   データ複製タスクは早いタイムスタンプから開始されるため、大量の増分データを複製する必要が生じます。

v4.0.13 以降で`cdc cli`使用して作成された changefeed では、Unified Sorter がデフォルトで有効になっています。v4.0.13 より前に存在していた changefeed では、以前の構成が使用されます。

変更フィードで Unified Sorter 機能が有効になっているかどうかを確認するには、次のサンプル コマンドを実行します (PD インスタンスの IP アドレスが`http://10.0.10.25:2379`であると想定)。

```shell
cdc cli --server="http://10.0.10.25:8300" changefeed query --changefeed-id=simple-replication-task | grep 'sort-engine'
```

上記のコマンドの出力で、値`sort-engine`が「unified」の場合、変更フィードで Unified Sorter が有効になっていることを意味します。

> **注記：**
>
> -   サーバーで、レイテンシーが長く、帯域幅が制限されている機械式ハード ドライブやその他のstorageデバイスが使用されている場合、Unified Sorter のパフォーマンスは大幅に低下します。
> -   デフォルトでは、Unified Sorter は`data_dir`使用して一時ファイルを保存します。空きディスク容量が 500 GiB 以上であることを確認することをお勧めします。本番環境では、各ノードの空きディスク容量が (業務で許容される`checkpoint-ts`遅延) * (業務ピーク時のアップストリーム書き込みトラフィック) より大きいことを確認することをお勧めします。また、 `changefeed`作成後に大量の履歴データを複製する予定がある場合は、各ノードの空き容量が複製されたデータの量より大きいことを確認してください。
