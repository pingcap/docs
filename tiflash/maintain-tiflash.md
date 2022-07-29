---
title: Maintain a TiFlash Cluster
summary: Learn common operations when you maintain a TiFlash cluster.
---

# TiFlashクラスターを管理する {#maintain-a-tiflash-cluster}

このドキュメントでは、TiFlashのバージョンの確認など、 [TiFlash](/tiflash/tiflash-overview.md)のクラスタを維持するときに一般的な操作を実行する方法について説明します。このドキュメントでは、重要なログとTiFlashのシステムテーブルも紹介しています。

## TiFlashのバージョンを確認してください {#check-the-tiflash-version}

TiFlashのバージョンを確認する方法は2つあります。

-   TiFlashのバイナリファイル名が`tiflash`の場合、 `./tiflash version`コマンドを実行してバージョンを確認できます。

    ただし、上記のコマンドを実行するには、 `libtiflash_proxy.so`のダイナミックライブラリを含むディレクトリパスを`LD_LIBRARY_PATH`の環境変数に追加する必要があります。これは、TiFlashの実行が`libtiflash_proxy.so`ダイナミックライブラリに依存しているためです。

    たとえば、 `tiflash`と`libtiflash_proxy.so`が同じディレクトリにある場合、最初にこのディレクトリに切り替えてから、次のコマンドを使用してTiFlashのバージョンを確認できます。

    {{< copyable "" >}}

    ```shell
    LD_LIBRARY_PATH=./ ./tiflash version
    ```

-   TiFlashログを参照して、TiFlashのバージョンを確認してください。ログパスについては、 [`tiflash.toml`ファイル](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)の`[logger]`の部分を参照してください。例えば：

    ```
    <information>: TiFlash version: TiFlash 0.2.0 master-375035282451103999f3863c691e2fc2
    ```

## TiFlashの重要なログ {#tiflash-critical-logs}

| ログ情報                                                                                                                                 | ログの説明                                           |
| ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| `[INFO] [<unknown>] ["KVStore: Start to persist [region 47, applied: term 6 index 10]"] [thread_id=23]`                              | データの複製が開始されます（ログの先頭にある角括弧内の数字はスレッドIDを示します       |
| `[DEBUG] [<unknown>] ["CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute(): Handling DAG request"] [thread_id=30]`    | DAG要求の処理、つまり、TiFlashがコプロセッサー要求の処理を開始します         |
| `[DEBUG] [<unknown>] ["CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute(): Handle DAG request done"] [thread_id=30]` | DAG要求の処理が完了しました。つまり、TiFlashはコプロセッサー要求の処理を終了します。 |

コプロセッサー要求の開始または終了を見つけて、ログの先頭に印刷されたスレッドIDからコプロセッサー要求の関連ログを見つけることができます。

## TiFlashシステムテーブル {#tiflash-system-table}

`information_schema.tiflash_replica`システムテーブルの列名とその説明は次のとおりです。

| カラム名            | 説明                                |
| --------------- | --------------------------------- |
| TABLE_SCHEMA    | データベース名                           |
| TABLE_NAME      | テーブル名                             |
| TABLE_ID        | テーブルID                            |
| REPLICA_COUNT   | TiFlashレプリカの数                     |
| LOCATION_LABELS | リージョン内の複数のレプリカが分散していることに基づくPDのヒント |
| 利用可能            | 利用可能かどうか（0/1）                     |
| 進捗              | レプリケーションの進行状況[0.0〜1.0]            |
