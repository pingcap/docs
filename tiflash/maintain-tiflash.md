---
title: Maintain a TiFlash Cluster
summary: TiFlashクラスターを保守する際の一般的な操作を学習します。
---

# TiFlashクラスタを管理 {#maintain-a-tiflash-cluster}

このドキュメントでは、 TiFlash のバージョン確認など、 [TiFlash](/tiflash/tiflash-overview.md)クラスタのメンテナンス時によく行われる操作について説明します。また、 TiFlashの重要なログとシステムテーブルについても紹介します。

## TiFlashのバージョンを確認する {#check-the-tiflash-version}

TiFlash のバージョンを確認するには、次の 2 つの方法があります。

-   TiFlashのバイナリファイル名が`tiflash`の場合、 `./tiflash version`コマンドを実行することでバージョンを確認できます。

    ただし、上記のコマンドを実行するには、 `libtiflash_proxy.so`動的ライブラリを含むディレクトリパスを`LD_LIBRARY_PATH`環境変数に追加する必要があります。これは、 TiFlashの実行が`libtiflash_proxy.so`動的ライブラリに依存しているためです。

    たとえば、 `tiflash`と`libtiflash_proxy.so`同じディレクトリにある場合は、まずこのディレクトリに切り替えて、次のコマンドを使用してTiFlash のバージョンを確認できます。

    ```shell
    LD_LIBRARY_PATH=./ ./tiflash version
    ```

-   TiFlash のログを参照して、 TiFlash のバージョンを確認してください。ログのパスについては、 [`tiflash.toml`ファイル](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)の`[logger]`部分を参照してください。例えば、以下のようになります。

        <information>: TiFlash version: TiFlash 0.2.0 master-375035282451103999f3863c691e2fc2

## TiFlashの重要なログ {#tiflash-critical-logs}

| ログ情報                                                                                                                                 | ログの説明                                             |
| ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| `[INFO] [<unknown>] ["KVStore: Start to persist [region 47, applied: term 6 index 10]"] [thread_id=23]`                              | データの複製が開始されます（ログの先頭の角括弧内の数字はスレッドIDを表します）          |
| `[DEBUG] [<unknown>] ["CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute(): Handling DAG request"] [thread_id=30]`    | DAG要求の処理、つまりTiFlashがコプロセッサー要求の処理を開始する             |
| `[DEBUG] [<unknown>] ["CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute(): Handle DAG request done"] [thread_id=30]` | DAG要求の処理が完了しました。つまり、 TiFlashがコプロセッサー要求の処理を完了しました。 |

コプロセッサー要求の開始または終了を見つけ、ログの先頭に印刷されているスレッド ID を通じてコプロセッサー要求の関連ログを見つけることができます。

## TiFlashシステムテーブル {#tiflash-system-table}

`information_schema.tiflash_replica`システム テーブルの列名とその説明は次のとおりです。

| カラム名     | 説明                                        |
| -------- | ----------------------------------------- |
| テーブルスキーマ | データベース名                                   |
| テーブル名    | テーブル名                                     |
| テーブルID   | テーブルID                                    |
| レプリカ数    | TiFlashレプリカの数                             |
| 場所ラベル    | PDのヒント。リージョン内の複数のレプリカが分散されているかどうかに基づいている。 |
| 利用可能     | 利用可能かどうか（0/1）                             |
| 進捗       | レプリケーションの進行状況 [0.0~1.0]                   |
