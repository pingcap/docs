---
title: TiDB Binlog Overview
summary: Learn overview of the cluster version of TiDB Binlog.
---

# TiDBBinlogクラスターの概要 {#tidb-binlog-cluster-overview}

このドキュメントでは、TiDBBinlogのクラスタバージョンのアーキテクチャとデプロイメントを紹介します。

TiDB Binlogは、TiDBからbinlogデータを収集し、ダウンストリームプラットフォームにほぼリアルタイムのバックアップとレプリケーションを提供するために使用されるツールです。

TiDBBinlogには次の機能があります。

-   **データ複製：** TiDBクラスタのデータを他のデータベースに複製します
-   **リアルタイムのバックアップと復元：** TiDBクラスタ内のデータをバックアップし、クラスタに障害が発生したときにTiDBクラスタを復元します

> **ノート：**
>
> TiDB Binlogは、TiDB v5.0で導入された一部の機能と互換性がなく、一緒に使用することはできません。詳細については、 [ノート](#notes)を参照してください。 TiDBBinlogの代わりに[TiCDC](/ticdc/ticdc-overview.md)を使用することをお勧めします。

## TiDBBinlogアーキテクチャ {#tidb-binlog-architecture}

TiDBBinlogアーキテクチャは次のとおりです。

![TiDB Binlog architecture](/media/tidb-binlog-cluster-architecture.png)

TiDB Binlogクラスタは、ポンプとドレイナーで構成されています。

### ポンプ {#pump}

[ポンプ](https://github.com/pingcap/tidb-binlog/blob/master/pump)は、TiDBで生成されたbinlogを記録し、トランザクションのコミット時間に基づいてbinlogをソートし、消費のためにbinlogをDrainerに送信するために使用されます。

### ドレイナー {#drainer}

[ドレイナー](https://github.com/pingcap/tidb-binlog/tree/master/drainer)は、各ポンプからbinlogを収集してマージし、binlogをSQLまたは特定の形式のデータに変換し、データを特定のダウンストリームプラットフォームに複製します。

### <code>binlogctl</code>ガイド {#code-binlogctl-code-guide}

[`binlogctl`](https://github.com/pingcap/tidb-binlog/tree/master/binlogctl)は、次の機能を備えたTiDBBinlogの操作ツールです。

-   TiDBクラスタの現在の`tso`を取得する
-   ポンプ/ドレイナーの状態を確認する
-   ポンプ/ドレイナーの状態の変更
-   ポンプ/ドレイナーの一時停止または閉鎖

## 主な特徴 {#main-features}

-   複数のポンプがクラスタを形成し、水平方向にスケールアウトできます
-   TiDBは、組み込みのPump Clientを使用して、binlogを各Pumpに送信します
-   Pumpはbinlogを保存し、binlogをDrainerに順番に送信します
-   Drainerは、各ポンプのbinlogを読み取り、binlogをマージして並べ替え、binlogをダウンストリームに送信します。
-   ドレイナーは[リレーログ](/tidb-binlog/tidb-binlog-relay-log.md)をサポートします。リレーログによって、Drainerはダウンストリームクラスターが一貫した状態にあることを確認します。

## ノート {#notes}

-   v5.1では、v5.0で導入されたクラスター化インデックス機能とTiDBBinlogの間の非互換性が解決されました。 TiDBBinlogとTiDBServerをv5.1にアップグレードし、TiDB Binlogを有効にすると、TiDBはクラスター化インデックスを使用したテーブルの作成をサポートします。クラスター化インデックスを使用して作成されたテーブルでのデータの挿入、削除、および更新は、TiDBBinlogを介してダウンストリームに複製されます。 TiDB Binlogを使用してクラスター化インデックスを使用してテーブルを複製する場合は、次の点に注意してください。

    -   アップグレードシーケンスを手動で制御してクラスタをv5.0からv5.1にアップグレードした場合は、TiDBサーバーをv5.1にアップグレードする前に、TiDBbinlogがv5.1にアップグレードされていることを確認してください。
    -   システム変数[`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)を同じ値に構成して、アップストリームとダウンストリームの間でTiDBクラスター化インデックステーブルの構造に一貫性を持たせることをお勧めします。

-   TiDB Binlogは、TiDB v5.0で導入された次の機能と互換性がなく、一緒に使用することはできません。

    -   [TiDBクラスター化インデックス](/clustered-indexes.md#limitations) ：TiDB Binlogが有効になった後、TiDBは、主キーとして非単一整数列を使用してクラスター化インデックスを作成することを許可しません。作成されたクラスター化インデックステーブルのデータの挿入、削除、および更新は、TiDBBinlogを介してダウンストリームに複製されません。クラスタ化インデックスを使用してテーブルをレプリケートする必要がある場合は、クラスタをv5.1にアップグレードするか、代わりに[TiCDC](/ticdc/ticdc-overview.md)を使用してください。
    -   TiDBシステム変数[tidb_enable_async_commit](/system-variables.md#tidb_enable_async_commit-new-in-v50) ：TiDB Binlogを有効にした後、このオプションを有効にしてもパフォーマンスを向上させることはできません。 TiDBBinlogの代わりに[TiCDC](/ticdc/ticdc-overview.md)を使用することをお勧めします。
    -   TiDBシステム変数[tidb_enable_1pc](/system-variables.md#tidb_enable_1pc-new-in-v50) ：TiDB Binlogを有効にした後、このオプションを有効にしてもパフォーマンスを向上させることはできません。 TiDBBinlogの代わりに[TiCDC](/ticdc/ticdc-overview.md)を使用することをお勧めします。

-   TiDB Binlogは、TiDB v4.0.7で導入された次の機能と互換性がなく、一緒に使用することはできません。

    -   TiDBシステム変数[tidb_enable_amend_pessimistic_txn](/system-variables.md#tidb_enable_amend_pessimistic_txn-new-in-v407) ：2つの機能には互換性の問題があります。それらを一緒に使用すると、TiDBBinlogがデータを一貫して複製しないという問題が発生する可能性があります。

-   Drainerは、binlogのMySQL、TiDB、Kafka、またはローカルファイルへの複製をサポートしています。 binlogを他のDrainerのサポートされていない宛先に複製する必要がある場合は、binlogをKafkaに複製し、Kafkaのデータを読み取って、binlogコンシューマープロトコルに従ってカスタマイズされた処理を行うようにDrainerを設定できます。 [Binlogコンシューマークライアントユーザーガイド](/tidb-binlog/binlog-consumer-client.md)を参照してください。

-   増分データを回復するためにTiDBBinlogを使用するには、config `db-type`を`file` （proto buffer形式のローカルファイル）に設定します。 Drainerは、binlogを指定された[プロトバッファ形式](https://github.com/pingcap/tidb-binlog/blob/master/proto/pb_binlog.proto)のデータに変換し、そのデータをローカルファイルに書き込みます。このように、 [レパロ](/tidb-binlog/tidb-binlog-reparo.md)を使用してデータを段階的に回復できます。

    `db-type`の値に注意してください：

    -   TiDBのバージョンが2.1.9より前の場合は、 `db-type="pb"`を設定します。
    -   TiDBのバージョンが2.1.9以降の場合は、 `db-type="file"`または`db-type="pb"`を設定します。

-   ダウンストリームがMySQL、MariaDB、または別のTiDBクラスタの場合、 [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)を使用して、データ複製後にデータを検証できます。
