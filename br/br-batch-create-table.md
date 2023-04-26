---
title: Batch Create Table
summary: Learn how to use the Batch Create Table feature. When restoring data, BR can create tables in batches to speed up the restore process.
---

# テーブルのバッチ作成 {#batch-create-table}

データを復元するとき、バックアップと復元 (BR) は、ターゲットの TiDB クラスターにデータベースとテーブルを作成し、バックアップ データをテーブルに復元します。 TiDB v6.0.0 より前のバージョンでは、 BR は[シリアル実行](#implementation)実装を使用して復元プロセスでテーブルを作成します。ただし、 BR が多数のテーブル (ほぼ 50000) を含むデータを復元する場合、この実装ではテーブルの作成に多くの時間がかかります。

テーブル作成プロセスを高速化し、データの復元時間を短縮するために、TiDB v6.0.0 で Batch Create Table 機能が導入されました。この機能はデフォルトで有効になっています。

> **ノート：**
>
> -   Batch Create Table 機能を使用するには、TiDB とBR の両方が v6.0.0 以降である必要があります。 TiDB またはBR のいずれかが v6.0.0 より前の場合、 BR はシリアル実行の実装を使用します。
> -   クラスター管理ツール ( TiUPなど) を使用していて、TiDB とBR がv6.0.0 以降のバージョンであるか、TiDB とBRが v6.0.0 より前のバージョンから v6.0.0 以降にアップグレードされているとします。 .

## 利用シーン {#usage-scenario}

大量のテーブル (たとえば 50000 テーブル) を含むデータを復元する必要がある場合は、バッチ作成テーブル機能を使用して復元プロセスを高速化できます。

詳細な効果については、 [バッチ作成テーブル機能のテスト](#feature-test)を参照してください。

## バッチ作成テーブルを使用 {#use-batch-create-table}

BR は、デフォルトで Batch Create Table 機能を有効にします。v6.0.0 以降では、リストア プロセスを高速化するためにデフォルト設定が`--ddl-batch-size=128`になっています。したがって、このパラメーターを構成する必要はありません。 `--ddl-batch-size=128`バッチでテーブルを作成することを意味し、各バッチには 128 個のテーブルがあります。

この機能を無効にするには、 `--ddl-batch-size` ～ `1`を設定します。次のコマンド例を参照してください。

```shell
br restore full \
--storage local:///br_data/ --pd "${PD_IP}:2379" --log-file restore.log \
--ddl-batch-size=1
```

この機能を無効にすると、 BR は代わりに[シリアル実行の実装](#implementation)を使用します。

## 実装 {#implementation}

-   v6.0.0 より前のシリアル実行の実装:

    データを復元するとき、 BR はターゲットの TiDB クラスターにデータベースとテーブルを作成し、バックアップ データをテーブルに復元します。テーブルを作成するために、 BR は最初に TiDB 内部 API を呼び出し、次にテーブル作成タスクを処理します。これは、 `Create Table`ステートメントの実行と同様に機能します。 TiDB DDL 所有者はテーブルを順次作成します。 DDL 所有者がテーブルを作成すると、それに応じて DDL スキーマのバージョンが変更され、各バージョンの変更が他の TiDB DDL ワーカー ( BRを含む) に同期されます。したがって、多数のテーブルを復元する場合、シリアル実行の実装には時間がかかります。

-   v6.0.0 以降のバッチ作成テーブルの実装:

    デフォルトでは、 BR は複数のバッチでテーブルを作成し、各バッチには 128 個のテーブルがあります。この実装を使用すると、 BR がテーブルのバッチを 1 つ作成するときに、TiDB スキーマのバージョンが 1 回だけ変更されます。この実装により、テーブル作成の速度が大幅に向上します。

## 機能テスト {#feature-test}

このセクションでは、バッチ作成テーブル機能に関するテスト情報について説明します。テスト環境は次のとおりです。

-   クラスタ構成:

    -   15 個の TiKV インスタンス。各 TiKV インスタンスには、16 個の CPU コア、80 GB のメモリ、および RPC 要求を処理するための 16 個のスレッド ( [`import.num-threads`](/tikv-configuration-file.md#num-threads) = 16) が装備されています。
    -   3 つの TiDB インスタンス。各 TiDB インスタンスには、16 個の CPU コア、32 GB のメモリが搭載されています。
    -   3 つの PD インスタンス。各 PD インスタンスには、16 個の CPU コア、32 GB のメモリが搭載されています。

-   復元するデータのサイズ: 16.16 TB

テスト結果は次のとおりです。

```
'[2022/03/12 22:37:49.060 +08:00] [INFO] [collector.go:67] ["Full restore success summary"] [total-ranges=751760] [ranges-succeed=751760] [ranges-failed=0] [split-region=1h33m18.078448449s] [restore-ranges=542693] [total-take=1h41m35.471476438s] [restore-data-size(after-compressed)=8.337TB] [Size=8336694965072] [BackupTS=431773933856882690] [total-kv=148015861383] [total-kv-size=16.16TB] [average-speed=2.661GB/s]'
```

テスト結果から、 `tikv_count`つの TiKV インスタンスを復元する平均速度が 181.65 MB/秒 ( `average-speed`に等しい) であることがわかります。
