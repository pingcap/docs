---
title: Maintain a TiFlash Cluster
summary: Learn common operations when you maintain a TiFlash cluster.
---

# TiFlashクラスタの管理 {#maintain-a-tiflash-cluster}

このドキュメントでは、 TiFlashバージョンの確認など、 [TiFlash](/tiflash/tiflash-overview.md)クラスターを保守する場合の一般的な操作を実行する方法について説明します。このドキュメントでは、 TiFlashの重要なログとシステム テーブルも紹介します。

## TiFlashのバージョンを確認する {#check-the-tiflash-version}

TiFlash のバージョンを確認するには 2 つの方法があります。

-   TiFlashのバイナリファイル名が`tiflash`の場合、 `./tiflash version`コマンドを実行することでバージョンを確認できます。

    ただし、上記コマンドを実行するには、 `libtiflash_proxy.so`ダイナミックライブラリを含むディレクトリパスを`LD_LIBRARY_PATH`環境変数に追加する必要があります。これは、 TiFlashの実行が`libtiflash_proxy.so`ダイナミック ライブラリに依存しているためです。

    たとえば、 `tiflash`と`libtiflash_proxy.so`が同じディレクトリにある場合、最初にこのディレクトリに切り替えてから、次のコマンドを使用してTiFlashのバージョンを確認できます。

    ```shell
    LD_LIBRARY_PATH=./ ./tiflash version
    ```

-   TiFlash のバージョンはTiFlashログを参照して確認してください。ログのパスについては、 [`tiflash.toml`ファイル](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)の`[logger]`部分を参照してください。例えば：

        <information>: TiFlash version: TiFlash 0.2.0 master-375035282451103999f3863c691e2fc2

## TiFlash の重要なログ {#tiflash-critical-logs}

| ログ情報                                                                                                                                 | ログの説明                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| `[INFO] [<unknown>] ["KVStore: Start to persist [region 47, applied: term 6 index 10]"] [thread_id=23]`                              | データの複製が開始されます (ログの先頭にある角括弧内の数字はスレッド ID を示します)             |
| `[DEBUG] [<unknown>] ["CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute(): Handling DAG request"] [thread_id=30]`    | DAG リクエストの処理。つまり、 TiFlash がコプロセッサーリクエストの処理を開始します。         |
| `[DEBUG] [<unknown>] ["CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute(): Handle DAG request done"] [thread_id=30]` | DAG リクエストの処理が完了しました。つまり、 TiFlash がコプロセッサーリクエストの処理を終了しました。 |

コプロセッサー要求の先頭または末尾を見つけて、ログの先頭に出力されたスレッド ID を使用してコプロセッサー要求の関連ログを見つけることができます。

## TiFlashシステムテーブル {#tiflash-system-table}

`information_schema.tiflash_replica`システム テーブルの列名とその説明は次のとおりです。

| カラム名            | 説明                                   |
| --------------- | ------------------------------------ |
| テーブルスキーマ        | データベース名                              |
| TABLE_NAME      | テーブル名                                |
| テーブルID          | テーブルID                               |
| REPLICA_COUNT   | TiFlashレプリカの数                        |
| LOCATION_LABELS | リージョン内の複数のレプリカが分散されていることに基づく PD のヒント |
| 利用可能            | 利用可能かどうか (0/1)                       |
| 進捗              | レプリケーションの進行状況 [0.0~1.0]              |
