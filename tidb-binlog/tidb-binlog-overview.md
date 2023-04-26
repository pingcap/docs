---
title: TiDB Binlog Overview
summary: Learn overview of the cluster version of TiDB Binlog.
---

# TiDB Binlogクラスタの概要 {#tidb-binlog-cluster-overview}

このドキュメントでは、TiDB Binlogのクラスター バージョンのアーキテクチャと展開について紹介します。

TiDB Binlog は、 TiDB からbinlogデータを収集し、ダウンストリーム プラットフォームにほぼリアルタイムのバックアップとレプリケーションを提供するために使用されるツールです。

TiDB Binlog には次の機能があります。

-   **データ複製:** TiDB クラスタ内のデータを他のデータベースに複製します
-   **リアルタイムのバックアップと復元:** TiDB クラスター内のデータをバックアップし、クラスターに障害が発生したときに TiDB クラスターを復元します。

> **ノート：**
>
> TiDB Binlog は、 TiDB v5.0 で導入された一部の機能と互換性がなく、一緒に使用することはできません。詳細については、 [ノート](#notes)を参照してください。 TiDB Binlogの代わりに[TiCDC](/ticdc/ticdc-overview.md)使用することをお勧めします。

## TiDB Binlogアーキテクチャ {#tidb-binlog-architecture}

TiDB Binlogアーキテクチャは次のとおりです。

![TiDB Binlog architecture](/media/tidb-binlog-cluster-architecture.png)

TiDB BinlogクラスタはPumpとDrainerで構成されています。

### Pump {#pump}

[Pump](https://github.com/pingcap/tidb-binlog/blob/master/pump)は、TiDB で生成されたバイナリログを記録し、トランザクションのコミット時間に基づいてバイナリログをソートし、バイナリログをDrainerに送信して消費するために使用されます。

### Drainer {#drainer}

[Drainer](https://github.com/pingcap/tidb-binlog/tree/master/drainer) 、各Pumpからバイナリログを収集してマージし、binlogをSQL または特定の形式のデータに変換し、データを特定のダウンストリーム プラットフォームにレプリケートします。

### <code>binlogctl</code>ガイド {#code-binlogctl-code-guide}

[`binlogctl`](https://github.com/pingcap/tidb-binlog/tree/master/binlogctl)は、次の機能を備えた TiDB Binlogの操作ツールです。

-   TiDB クラスターの現在の`tso`取得する
-   Pump・Drainerの状態確認
-   Pump/Drainerの状態を変更する
-   Pump/Drainerの一時停止または閉鎖

## 主な特徴 {#main-features}

-   複数のポンプがクラスターを形成し、水平方向にスケールアウトできます
-   TiDB は組み込みのPump Client を使用してbinlogを各Pumpに送信します
-   Pumpはバイナリログを保存し、バイナリログを順番にDrainerに送信します
-   Drainer は各Pumpのバイナリログを読み取り、バイナリログをマージしてソートし、バイナリログを下流に送信します
-   Drainerサポート[中継ログ](/tidb-binlog/tidb-binlog-relay-log.md) .リレー ログによって、 Drainer はダウンストリーム クラスターが一貫した状態にあることを確認します。

## ノート {#notes}

-   v5.1 では、v5.0 で導入されたクラスター化インデックス機能と TiDB Binlogの間の非互換性が解決されました。 TiDB Binlogと TiDB Server を v5.1 にアップグレードして TiDB Binlogを有効にすると、TiDB はクラスター化インデックスを使用したテーブルの作成をサポートします。クラスター化されたインデックスを使用して作成されたテーブルでのデータの挿入、削除、および更新は、TiDB Binlogを介してダウンストリームにレプリケートされます。 TiDB Binlogを使用してクラスター化インデックスを含むテーブルを複製する場合は、次の点に注意してください。

    -   アップグレード シーケンスを手動で制御してクラスターを v5.0 から v5.1 にアップグレードした場合は、TiDBサーバーを v5.1 にアップグレードする前に、TiDB binlogが v5.1 にアップグレードされていることを確認してください。
    -   システム変数[`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)を同じ値に構成して、上流と下流の間で TiDB クラスター化インデックス テーブルの構造が一貫していることを確認することをお勧めします。

-   TiDB Binlog は、 TiDB v5.0 で導入された次の機能と互換性がなく、一緒に使用することはできません。

    -   [TiDB クラスタ化インデックス](/clustered-indexes.md#limitations) : TiDB Binlogが有効になった後、TiDB は単一でない整数列を主キーとするクラスター化インデックスの作成を許可しません。作成されたクラスター化インデックス テーブルのデータの挿入、削除、および更新は、TiDB Binlogを介してダウンストリームに複製されません。クラスター化インデックスを使用してテーブルを複製する必要がある場合は、クラスターを v5.1 にアップグレードするか、代わりに[TiCDC](/ticdc/ticdc-overview.md)を使用してください。
    -   TiDB システム変数[tidb_enable_async_commit](/system-variables.md#tidb_enable_async_commit-new-in-v50) : TiDB Binlogを有効にすると、このオプションを有効にしてもパフォーマンスは向上しません。 TiDB Binlogの代わりに[TiCDC](/ticdc/ticdc-overview.md)使用することをお勧めします。
    -   TiDB システム変数[tidb_enable_1pc](/system-variables.md#tidb_enable_1pc-new-in-v50) : TiDB Binlogを有効にすると、このオプションを有効にしてもパフォーマンスは向上しません。 TiDB Binlogの代わりに[TiCDC](/ticdc/ticdc-overview.md)使用することをお勧めします。

-   TiDB Binlog は、 TiDB v4.0.7 で導入された次の機能と互換性がなく、一緒に使用することはできません。

    -   TiDB システム変数[tidb_enable_amend_pessimistic_txn](/system-variables.md#tidb_enable_amend_pessimistic_txn-new-in-v407) : 2 つの機能には互換性の問題があります。それらを一緒に使用すると、TiDB Binlog がデータを不整合に複製するという問題が発生する可能性があります。

-   Drainer は、バイナリログを MySQL、TiDB、Kafka、またはローカル ファイルに複製することをサポートしています。 Binlog を他のDrainer のサポートされていない宛先に複製する必要がある場合は、 Drainer を設定してbinlog をKafka に複製し、Kafka でデータを読み取って、 binlogコンシューマ プロトコルに従ってカスタマイズされた処理を行うことができます。 [Binlog Consumer Clientユーザー ガイド](/tidb-binlog/binlog-consumer-client.md)を参照してください。

-   増分データの回復に TiDB Binlogを使用するには、config `db-type`から`file` (proto バッファー形式のローカル ファイル) を設定します。 Drainer はbinlog を指定された[プロト バッファ形式](https://github.com/pingcap/tidb-binlog/blob/master/proto/pb_binlog.proto)のデータに変換し、そのデータをローカル ファイルに書き込みます。このように、 [Reparo](/tidb-binlog/tidb-binlog-reparo.md)使用してデータを段階的に回復できます。

    `db-type`の値に注意してください。

    -   TiDB のバージョンが 2.1.9 より前の場合は、 `db-type="pb"`を設定します。
    -   TiDB のバージョンが 2.1.9 以降の場合は、 `db-type="file"`または`db-type="pb"`を設定します。

-   ダウンストリームが MySQL、MariaDB、または別の TiDB クラスターである場合、 [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)を使用して、データのレプリケーション後にデータを検証できます。
