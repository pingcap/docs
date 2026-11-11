---
title: Migrate Data from TiDB to MySQL-compatible Databases
summary: TiDB から MySQL 互換データベースにデータを移行する方法を学びます。
---

# TiDB から MySQL 互換データベースへのデータ移行 {#migrate-data-from-tidb-to-mysql-compatible-databases}

このドキュメントでは、TiDB クラスターからAurora、MySQL、MariaDB などの MySQL 互換データベースへのデータ移行方法について説明します。プロセス全体は以下の4つのステップで構成されます。

1. 環境を設定します。
2. 全データを移行します。
3. 増分データを移行します。
4. サービスを MySQL 互換クラスターに移行します。

## ステップ1. 環境を設定する {#step-1-set-up-the-environment}

1. TiDB クラスターをアップストリームにデプロイ。

    TiUP Playgroundを使用してTiDBクラスターをデプロイ。詳細については、 [ローカルTiDBクラスターを迅速にデプロイ](/tiup/tiup-playground.md)を参照してください。

    [TiCDC](/ticdc/ticdc-overview.md) は、アップストリーム TiDB クラスターからダウンストリームの MySQL 互換データベースに増分データ変更をレプリケートします。次の例では、TiCDC の `gc-ttl` を `172800` 秒（48 時間）に設定しています。フルデータのエクスポート、インポート、および増分レプリケーションが追いつくまでに必要な時間をカバーする値を選択してください。詳細については、[ステップ2 の GC に関する警告](#step-2-migrate-full-data)を参照してください。

    ```shell
    # Create the TiCDC configuration file
    cat > ticdc.toml <<'EOF'
    gc-ttl = 172800
    EOF
    # Create a TiDB cluster
    tiup playground --db 1 --pd 1 --kv 1 --tiflash 0 --ticdc 1 --ticdc.config ticdc.toml
    # View cluster status
    tiup status
    ```

2. MySQL インスタンスをダウンストリームにデプロイ。

    - ラボ環境では、Docker を使用して次のコマンドを実行することで、MySQL インスタンスをすばやくデプロイできます。

        ```shell
        docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -p 3306:3306 -d mysql
        ```

    - 本番環境では、 [MySQLのインストール](https://dev.mysql.com/doc/refman/8.0/en/installing.html)の手順に従って MySQL インスタンスをデプロイできます。

3. サービスのワークロードをシミュレートします。

    ラボ環境では、 `go-tpc`を使用してTiDBクラスターの上流にデータを書き込めます。これは、TiDBクラスターでイベントの変更を生成するためです。以下のコマンドを実行して、TiDBクラスターに`tpcc`という名前のデータベースを作成し、 TiUP benchを使用してこのデータベースにデータを書き込みます。

    ```shell
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 prepare
    tiup bench tpcc -H 127.0.0.1 -P 4000 -D tpcc --warehouses 4 run --time 300s
    ```

    `go-tpc`の詳細については[TiDBでTPC-Cテストを実行する方法](/benchmark/benchmark-tidb-using-tpcc.md)を参照してください。

## ステップ2. 全データを移行する {#step-2-migrate-full-data}

環境を設定したら、 [Dumpling](/dumpling-overview.md)を使用して上流の TiDB クラスターから完全なデータをエクスポートできます。

> **Note:**
>
> 本番のクラスターでは、GCを無効にしてバックアップを実行すると、クラスターのパフォーマンスに影響する可能性があります。この手順は、オフピーク時に実行することをお勧めします。

1. ガベージコレクション (GC) を無効にします。

    増分移行中に新しく書き込まれたデータが削除されないようにするには、フルデータをエクスポートする前に、上流クラスターのGCを無効にする必要があります。これにより、履歴データが削除されません。TiDB v4.0.0以降のバージョンでは、 Dumplingが[GCをブロックするためにGCセーフポイントを自動的に調整する](/dumpling-overview.md#manually-set-the-tidb-gc-time)なる可能性があります。ただし、 Dumplingの終了後にGCプロセスが開始され、増分変更の移行が失敗する可能性があるため、GCを手動で無効にすることは依然として必要です。

    GC を無効にするには、次のコマンドを実行します。

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=FALSE;
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会します。

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

    ```
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       0 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

    > **Note:**
    >
    > TiCDC の `gc-ttl` のデフォルト値は 24 時間です。後続の[増分レプリケーションタスク](#step-3-migrate-incremental-data)のレプリケーション遅延が `gc-ttl` を超えると、タスクは `ErrGCTTLExceeded` で失敗する可能性があります。長時間の移行では、[ステップ1. 環境を設定する](#step-1-set-up-the-environment) に示すように、TiCDC を起動する前により大きな値を設定してください。詳細については、[TiCDC の `gc-ttl` とは何ですか](/ticdc/ticdc-faq.md#what-is-gc-ttl-in-ticdc)を参照してください。

2. データをバックアップします。

    1. Dumplingを使用して SQL 形式でデータをエクスポートします。

        ```shell
        tiup dumpling -u root -P 4000 -h 127.0.0.1 --filetype sql -t 8 -o ./dumpling_output -r 200000 -F256MiB
        ```

    2. データのエクスポートが完了したら、次のコマンドを実行してメタデータを確認します。メタデータの`Pos`はエクスポート スナップショットの TSO であり、BackupTS として記録できます。

        ```shell
        cat dumpling_output/metadata
        ```

        ```
        Started dump at: 2022-06-28 17:49:54
        SHOW MASTER STATUS:
                Log: tidb-binlog
                Pos: 434217889191428107
                GTID:
        Finished dump at: 2022-06-28 17:49:57
        ```

3. データを復元します。

    MyLoader（オープンソースツール）を使用して、下流のMySQLインスタンスにデータをインポートします。MyLoaderのインストールと使用方法の詳細については、 [MyDumpler/MyLoader](https://github.com/mydumper/mydumper)を参照してください。MyLoaderはv0.10以前のバージョンを使用する必要があります。それ以降のバージョンでは、 Dumplingによってエクスポートされたメタデータファイルを処理できません。

    Dumplingによってエクスポートされた完全なデータを MySQL にインポートするには、次のコマンドを実行します。

    ```shell
    myloader -h 127.0.0.1 -P 3306 -u root -p my-secret-pw -d ./dumpling_output/
    ```

4. (オプション) データを検証します。

    [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)を使用すると、特定の時間に上流と下流の間のデータの整合性をチェックできます。

    ```shell
    sync_diff_inspector -C ./config.yaml
    ```

    sync-diff-inspector の設定方法の詳細については[設定ファイルの説明](/sync-diff-inspector/sync-diff-inspector-overview.md#configuration-file-description)を参照してください。このドキュメントでは、設定は以下のとおりです。

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
            password = "my-secret-pw"
    ######################### Task config #########################
    [task]
            output-dir = "./output"
            source-instances = ["upstream"]
            target-instance = "downstream"
            target-check-tables = ["*.*"]
    ```

## ステップ3. 増分データの移行 {#step-3-migrate-incremental-data}

1. TiCDCをデプロイ。

    完全データ移行が完了したら、増分データをレプリケーションするためのTiCDCクラスターをデプロイして設定します。本番環境では、 [TiCDCをデプロイ](/ticdc/deploy-ticdc.md)の手順に従ってTiCDCをデプロイしてください。このドキュメントでは、テストクラスターの作成時にTiCDCノードが起動済みであるため、TiCDCのデプロイ手順をスキップして、次のステップに進み、変更フィードを作成できます。

2. 変更フィードを作成します。

    > **Note:**
    >
    > 変更フィードを作成する前に、レプリケートする各テーブルに少なくとも 1 つの[有効なインデックス](/ticdc/ticdc-overview.md#valid-index)があることを確認してください。つまり、主キー、またはすべてのカラムが `NOT NULL` として定義され、仮想生成カラムを含まない一意インデックスです。デフォルトでは、TiCDC は有効なインデックスを持たないテーブルのデータ変更をレプリケートしません。後から有効なインデックスを追加すると、それ以降のデータ変更はレプリケートできますが、以前にスキップされた変更は復元されません。詳細については、[DDL レプリケーションルール](/ticdc/ticdc-ddl.md#ddl-allow-list)を参照してください。
    >
    > 有効なインデックスを持たないテーブルについては、有効なインデックスを追加することを推奨します。あるいは、変更フィード設定ファイルの先頭で、任意の `[section]` ヘッダーより前に [`force-replicate = true`](/ticdc/ticdc-changefeed-config.md#force-replicate) を追加し、変更フィード作成時に `--config` を使用してそのファイルを渡すこともできます。このオプションはデータ整合性を保証せず、重複データを引き起こす可能性があります。

    アップストリームクラスターで次のコマンドを実行して、アップストリームクラスターからダウンストリームクラスターへの変更フィードを作成します。

    ```shell
    tiup cdc:v<CLUSTER_VERSION> cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:***@127.0.0.1:3306" --changefeed-id="upstream-to-downstream" --start-ts="434217889191428107"
    ```

    `***` を、[ステップ1. 環境を設定する](#step-1-set-up-the-environment) で設定したダウンストリーム MySQL root アカウントのパスワードに置き換えてください。Docker の例では、`my-secret-pw` を使用します。

    このコマンドのパラメーターは次のとおりです。

    - `--server` : TiCDC クラスター内の任意のノードの IP アドレス
    - `--sink-uri` : 下流クラスターのURI
    - `--changefeed-id` : チェンジフィードID、正規表現の形式でなければなりません、 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`
    - `--start-ts` : 変更フィードの開始タイムスタンプ。バックアップ時刻である必要があります (または[ステップ2. 全データの移行](#step-2-migrate-full-data)の「データのバックアップ」セクションの BackupTS)

    changefeed 構成の詳細については、 [タスク設定ファイル](/ticdc/ticdc-changefeed-config.md)を参照してください。

3. GC を有効にします。

    TiCDCを用いた増分移行では、GCは複製された履歴データのみを削除します。そのため、変更フィードを作成した後、以下のコマンドを実行してGCを有効にする必要があります。詳細については[TiCDCガベージコレクション(GC) セーフポイントの完全な動作は何ですか?](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)を参照してください。

    GC を有効にするには、次のコマンドを実行します。

    ```sql
    MySQL [test]> SET GLOBAL tidb_gc_enable=TRUE;
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    変更が有効になっていることを確認するには、 `tidb_gc_enable`の値を照会します。

    ```sql
    MySQL [test]> SELECT @@global.tidb_gc_enable;
    ```

    ```
    +-------------------------+
    | @@global.tidb_gc_enable |
    +-------------------------+
    |                       1 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

## ステップ4. サービスの移行 {#step-4-migrate-services}

チェンジフィードを作成すると、TiCDC は対象に含まれるアップストリームテーブルからダウンストリームクラスターに変更をレプリケートします。増分レプリケーションが追いつくまで待ってから、読み取りトラフィックをダウンストリームクラスターに徐々に移行してください。書き込みトラフィックがダウンストリームクラスターに移行されるまでは、アップストリームクラスターへの新しい書き込みがレプリケートされるまでにまだ時間がかかるため、ダウンストリームクラスターのクエリ結果は一時的にアップストリームクラスターより遅れる可能性があります。一定期間、読み取りトラフィックを観察してください。下流クラスターが安定している場合は、以下の手順で書き込みトラフィックも下流クラスターに移行できます。

1. アップストリームクラスターの書き込みサービスを停止します。変更フィードを停止する前に、アップストリームのすべてのデータがダウンストリームに複製されていることを確認してください。

    ```shell
    # Stop the changefeed from the upstream cluster to the downstream cluster
    tiup cdc cli changefeed pause -c "upstream-to-downstream" --pd=http://172.16.6.122:2379
    # View the changefeed status
    tiup cdc cli changefeed list
    ```

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
    ```

2. 書き込みサービスを下流クラスターに移行した後、しばらく観察します。下流クラスターが安定している場合は、上流クラスターを破棄できます。
