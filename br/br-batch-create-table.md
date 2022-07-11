---
title: Batch Create Table
summary: Learn how to use the Batch Create Table feature. When restoring data, BR can create tables in batches to speed up the restore process.
---

# テーブルのバッチ作成 {#batch-create-table}

データを復元する場合、Backup＆Restore（BR）はターゲットTiDBクラスタにデータベースとテーブルを作成してから、バックアップデータをテーブルに復元します。 TiDB v6.0.0より前のバージョンでは、BRは[シリアル実行](#implementation-principles)実装を使用して、復元プロセスでテーブルを作成します。ただし、BRが多数のテーブル（約50000）のデータを復元する場合、この実装ではテーブルの作成に多くの時間がかかります。

テーブル作成プロセスを高速化し、データの復元時間を短縮するために、TiDBv6.0.0ではテーブルのバッチ作成機能が導入されています。この機能はデフォルトで有効になっています。

> **ノート：**
>
> -   テーブルのバッチ作成機能を使用するには、TiDBとBRの両方がv6.0.0以降であることが期待されます。 TiDBまたはBRのいずれかがv6.0.0より前の場合、BRはシリアル実行の実装を使用します。
> -   クラスタ管理ツール（TiUPなど）を使用していて、TiDBとBRがv6.0.0以降のバージョンであるか、TiDBとBRがv6.0.0より前のバージョンからv6.0.0以降にアップグレードされているとします。 。この場合、BRはデフォルトでテーブルのバッチ作成機能を有効にします。

## 使用シナリオ {#usage-scenario}

50000テーブルなど、大量のテーブルを含むデータを復元する必要がある場合は、テーブルのバッチ作成機能を使用して、復元プロセスを高速化できます。

詳細な効果については、 [テーブル機能のバッチ作成をテストする](#test-for-the-batch-create-table-feature)を参照してください。

## テーブルのバッチ作成機能を使用する {#use-the-batch-create-table-feature}

BRは、デフォルトでバッチ作成テーブル機能を有効にします。v6.0.0以降のデフォルト構成は`--ddl-batch-size=128`で、復元プロセスを高速化します。したがって、このパラメーターを構成する必要はありません。 `--ddl-batch-size=128`は、BRがバッチでテーブルを作成することを意味します。各バッチには128個のテーブルがあります。

この機能を無効にするには、 `--ddl-batch-size`から`0`に設定します。次のコマンド例を参照してください。

{{< copyable "" >}}

```shell
br restore full -s local:///br_data/ --pd 172.16.5.198:2379 --log-file restore.log --ddl-batch-size=0
```

この機能を無効にすると、BRは代わりに[シリアル実行の実装](#implementation-principles)を使用します。

## 実装の原則 {#implementation-principles}

-   v6.0.0より前のシリアル実行の実装：

    データを復元する場合、BRはターゲットTiDBクラスタにデータベースとテーブルを作成してから、バックアップデータをテーブルに復元します。テーブルを作成するために、BRは最初にTiDB内部APIを呼び出し、次にテーブル作成タスクを処理します。これは、BRによる`Create Table`ステートメントの実行と同様に機能します。 TiDB DDL所有者は、テーブルを順番に作成します。 DDL所有者がテーブルを作成すると、それに応じてDDLスキーマのバージョンが変更され、各バージョンの変更は他のTiDB DDLワーカー（BRを含む）に同期されます。したがって、BRが多数のテーブルを復元する場合、シリアル実行の実装には時間がかかります。

-   v6.0.0以降のバッチ作成テーブルの実装：

    デフォルトでは、BRは複数のバッチでテーブルを作成し、各バッチには128個のテーブルがあります。この実装を使用すると、BRがテーブルのバッチを1つ作成するときに、TiDBスキーマのバージョンは1回だけ変更されます。この実装により、テーブル作成の速度が大幅に向上します。

## テーブルのバッチ作成機能をテストする {#test-for-the-batch-create-table-feature}

このセクションでは、テーブルのバッチ作成機能に関するテスト情報について説明します。テスト環境は次のとおりです。

-   クラスター構成：

    -   15個のTiKVインスタンス。各TiKVインスタンスには、16個のCPUコア、80 GBのメモリ、およびRPC要求を処理するための16個のスレッドが装備されています（ [`import.num-threads`](/tikv-configuration-file.md#num-threads) = 16）。
    -   3つのTiDBインスタンス。各TiDBインスタンスには、16個のCPUコア、32GBのメモリが搭載されています。
    -   3つのPDインスタンス。各PDインスタンスには、16個のCPUコア、32GBのメモリが搭載されています。

-   復元するデータのサイズ：16.16 TB

テスト結果は次のとおりです。

```
'[2022/03/12 22:37:49.060 +08:00] [INFO] [collector.go:67] ["Full restore success summary"] [total-ranges=751760] [ranges-succeed=751760] [ranges-failed=0] [split-region=1h33m18.078448449s] [restore-ranges=542693] [total-take=1h41m35.471476438s] [restore-data-size(after-compressed)=8.337TB] [Size=8336694965072] [BackupTS=431773933856882690] [total-kv=148015861383] [total-kv-size=16.16TB] [average-speed=2.661GB/s]'
```

テスト結果から、1つのTiKVインスタンスを復元する平均速度は181.65 MB / s（ `average-speed`に等しい）であることがわかり`tikv_count` 。
