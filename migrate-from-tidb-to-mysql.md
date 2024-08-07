---
title: Migrate Data from TiDB to MySQL-compatible Databases
summary: TiDB から MySQL 互換データベースにデータを移行する方法を学びます。
---

# TiDB から MySQL 互換データベースにデータを移行する {#migrate-data-from-tidb-to-mysql-compatible-databases}

このドキュメントでは、TiDB クラスターからAurora、MySQL、MariaDB などの MySQL 互換データベースにデータを移行する方法について説明します。プロセス全体には、次の 4 つのステップが含まれます。

1.  環境を設定します。
2.  全データを移行します。
3.  増分データを移行します。
4.  サービスを MySQL 互換クラスターに移行します。

## ステップ1. 環境を設定する {#step-1-set-up-the-environment}

1.  TiDB クラスターをアップストリームにデプロイ。

    TiUP Playground を使用して TiDB クラスターをデプロイ。詳細については、 [TiUPを使用してオンライン TiDBクラスタをデプロイおよび管理](/tiup/tiup-cluster.md)を参照してください。

    ```shell
    # Create a TiDB cluster
    tiup playground --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1
    # View cluster status
    tiup status
    ```

2.  MySQL インスタンスをダウンストリームにデプロイ。

    -   ラボ環境では、Docker を使用して次のコマンドを実行することで、MySQL インスタンスをすばやくデプロイできます。

        ```shell
        docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -p 3306:3306 -d mysql
        ```

    -   本番環境では、 [MySQLのインストール](https://dev.mysql.com/doc/refman/8.0/en/installing.html)手順に従って MySQL インスタンスをデプロイできます。

3.  サービスのワークロードをシミュレートします。

    ラボ環境では、 `go-tpc`使用して TiDB クラスターのアップストリームにデータを書き込むことができます。これは、TiDB クラスターでイベントの変更を生成するためです。次のコマンドを実行して、TiDB クラスターに`tpcc`という名前のデータベースを作成し、 TiUPベンチを使用してこのデータベースにデータを書き込みます。

    ```shell
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 prepare
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 run --time 300s
    ```

    `go-tpc`の詳細については[TiDB で TPC-C テストを実行する方法](/benchmark/benchmark-tidb-using-tpcc.md)を参照してください。

## ステップ2. 全データを移行する {#step-2-migrate-full-data}

環境を設定したら、 [Dumpling](/dumpling-overview.md)使用して上流の TiDB クラスターから完全なデータをエクスポートできます。

> **注記：**
>
> 本番クラスターでは、GC を無効にしてバックアップを実行すると、クラスターのパフォーマンスに影響する可能性があります。この手順は、オフピーク時に完了することをお勧めします。

1.  ガベージコレクション (GC) を無効にします。

    増分移行中に新しく書き込まれたデータが削除されないようにするには、完全なデータをエクスポートする前に、アップストリーム クラスターの GC を無効にする必要があります。この方法では、履歴データは削除されません。TiDB v4.0.0 以降のバージョンでは、 Dumpling が[GCセーフポイントを自動的に調整してGCをブロックする](/dumpling-overview.md#manually-set-the-tidb-gc-time)なる可能性があります。ただし、 Dumplingの終了後に GC プロセスが開始され、増分変更の移行が失敗する可能性があるため、GC を手動で無効にする必要があります。

    GC を無効にするには、次のコマンドを実行します。

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=FALSE;
    ```

        Query OK, 0 rows affected (0.01 sec)

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会します。

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

        +-------------------------+：
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       0 |
        +-------------------------+
        1 row in set (0.00 sec)

2.  バックアップデータ。

    1.  Dumplingを使用して SQL 形式でデータをエクスポートします。

        ```shell
        tiup dumpling -u root -P 4000 -h 127.0.0.1 --filetype sql -t 8 -o ./dumpling_output -r 200000 -F256MiB
        ```

    2.  データのエクスポートが完了したら、次のコマンドを実行してメタデータを確認します。メタデータの`Pos`エクスポート スナップショットの TSO であり、BackupTS として記録できます。

        ```shell
        cat dumpling_output/metadata
        ```

            Started dump at: 2022-06-28 17:49:54
            SHOW MASTER STATUS:
                    Log: tidb-binlog
                    Pos: 434217889191428107
                    GTID:
            Finished dump at: 2022-06-28 17:49:57

3.  データを復元します。

    MyLoader (オープンソース ツール) を使用して、ダウンストリーム MySQL インスタンスにデータをインポートします。MyLoader のインストール方法と使用方法の詳細については、 [マイダンプラー/マイローダー](https://github.com/mydumper/mydumper)を参照してください。MyLoader v0.10 以前のバージョンを使用する必要があることに注意してください。それ以降のバージョンでは、 Dumplingによってエクスポートされたメタデータ ファイルを処理できません。

    Dumplingによってエクスポートされた完全なデータを MySQL にインポートするには、次のコマンドを実行します。

    ```shell
    myloader -h 127.0.0.1 -P 3306 -d ./dumpling_output/
    ```

4.  (オプション) データを検証します。

    [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)使用すると、特定の時点でのアップストリームとダウンストリーム間のデータの一貫性をチェックできます。

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    sync-diff-inspector の設定方法の詳細については、 [コンフィグレーションファイルの説明](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)参照してください。このドキュメントでは、設定は次のとおりです。

    ```toml
    # Diff Configuration.
    ######################### Datasource config #########################
    [data-sources]
    [data-sources.upstream]
            host = "127.0.0.1" # Replace the value with the IP address of your upstream cluster
            port = 4000
            user = "root"
            password = ""
            snapshot = "434217889191428107" # Set snapshot to the actual backup time (BackupTS in the "Back up data" section in [Step 2. Migrate full data](#step-2-migrate-full-data))
    [data-sources.downstream]
            host = "127.0.0.1" # Replace the value with the IP address of your downstream cluster
            port = 3306
            user = "root"
            password = ""
    ######################### Task config #########################
    [task]
            output-dir = "./output"
            source-instances = ["upstream"]
            target-instance = "downstream"
            target-check-tables = ["*.*"]
    ```

## ステップ3. 増分データを移行する {#step-3-migrate-incremental-data}

1.  TiCDC をデプロイ。

    完全なデータ移行が完了したら、増分データをレプリケートするための TiCDC クラスターをデプロイして構成します。本番環境では、 [TiCDC をデプロイ](/ticdc/deploy-ticdc.md)手順に従って TiCDC をデプロイします。このドキュメントでは、テスト クラスターの作成時に TiCDC ノードが起動されています。したがって、TiCDC をデプロイする手順をスキップして、次の手順に進み、変更フィードを作成できます。

2.  変更フィードを作成します。

    アップストリーム クラスターで次のコマンドを実行して、アップストリーム クラスターからダウンストリーム クラスターへの変更フィードを作成します。

    ```shell
    tiup cdc:v<CLUSTER_VERSION> cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:@127.0.0.1:3306" --changefeed-id="upstream-to-downstream" --start-ts="434217889191428107"
    ```

    このコマンドのパラメータは次のとおりです。

    -   `--server` : TiCDC クラスター内の任意のノードの IP アドレス
    -   `--sink-uri` : ダウンストリーム クラスターの URI
    -   `--changefeed-id` : チェンジフィードID、正規表現の形式でなければなりません、 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`
    -   `--start-ts` : 変更フィードの開始タイムスタンプ。バックアップ時間 (または[ステップ2. 全データを移行する](#step-2-migrate-full-data)の「データのバックアップ」セクションの BackupTS) である必要があります。

    changefeed 構成の詳細については、 [タスク設定ファイル](/ticdc/ticdc-changefeed-config.md)参照してください。

3.  GC を有効にします。

    TiCDC を使用した増分移行では、GC はレプリケートされた履歴データのみを削除します。そのため、チェンジフィードを作成した後、以下のコマンドを実行して GC を有効にする必要があります。詳細については、 [TiCDCガベージコレクション（GC）セーフポイントの完全な動作は何ですか？](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)参照してください。

    GC を有効にするには、次のコマンドを実行します。

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=TRUE;
    ```

        Query OK, 0 rows affected (0.01 sec)

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会します。

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

        +-------------------------+
        | @@global.tidb_gc_enable |
        +-------------------------+
        |                       1 |
        +-------------------------+
        1 row in set (0.00 sec)

## ステップ4. サービスを移行する {#step-4-migrate-services}

チェンジフィードを作成すると、アップストリーム クラスターに書き込まれたデータは、低レイテンシーでダウンストリーム クラスターにレプリケートされます。読み取りトラフィックをダウンストリーム クラスターに徐々に移行できます。一定期間、読み取りトラフィックを観察します。ダウンストリーム クラスターが安定している場合は、次の手順で書き込みトラフィックもダウンストリーム クラスターに移行できます。

1.  アップストリーム クラスターの書き込みサービスを停止します。変更フィードを停止する前に、すべてのアップストリーム データがダウンストリームに複製されていることを確認してください。

    ```shell
    # Stop the changefeed from the upstream cluster to the downstream cluster
    tiup cdc cli changefeed pause -c "upstream-to-downstream" --pd=http://172.16.6.122:2379
    # View the changefeed status
    tiup cdc cli changefeed list
    ```

        [
          {
            "id": "upstream-to-downstream",
            "summary": {
            "state": "stopped",  # Ensure that the status is stopped
            "tso": 434218657561968641,
            "checkpoint": "2022-06-28 18:38:45.685", # This time should be later than the time of stopping writing
            "error": null
            }
          }
        ]

2.  書き込みサービスをダウンストリーム クラスターに移行した後、しばらく観察します。ダウンストリーム クラスターが安定している場合は、アップストリーム クラスターを破棄できます。
