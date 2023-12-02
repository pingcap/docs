---
title: TiDB Binlog Overview
summary: Learn overview of the cluster version of TiDB Binlog.
---

# TiDBBinlogクラスタの概要 {#tidb-binlog-cluster-overview}

このドキュメントでは、TiDB Binlogのクラスター バージョンのアーキテクチャと展開について紹介します。

TiDB Binlog は、 TiDB からbinlogデータを収集し、ダウンストリーム プラットフォームにほぼリアルタイムのバックアップとレプリケーションを提供するために使用されるツールです。

TiDB Binlog には次の機能があります。

-   **データ複製:** TiDB クラスター内のデータを他のデータベースに複製します。
-   **リアルタイムのバックアップと復元:** TiDB クラスター内のデータをバックアップし、クラスターに障害が発生した場合に TiDB クラスターを復元します。

> **注記：**
>
> -   TiDB Binlog は、 TiDB v5.0 で導入された一部の機能と互換性がなく、一緒に使用することはできません。詳細は[ノート](#notes)を参照してください。
> -   TiDB v7.5.0 以降、TiDB Binlogのデータ レプリケーション機能のテクニカル サポートは提供されなくなりました。データ レプリケーションの代替ソリューションとして[TiCDC](/ticdc/ticdc-overview.md)を使用することを強くお勧めします。
> -   TiDB v7.5.0 は TiDB Binlogのリアルタイム バックアップおよび復元機能を引き続きサポートしていますが、このコンポーネントは将来のバージョンでは完全に非推奨になります。データ回復の代替ソリューションとして[PITR](/br/br-pitr-guide.md)を使用することをお勧めします。

## TiDBBinlogアーキテクチャ {#tidb-binlog-architecture}

TiDB Binlogアーキテクチャは次のとおりです。

![TiDB Binlog architecture](/media/tidb-binlog-cluster-architecture.png)

TiDB Binlogクラスターは、 PumpとDrainerで構成されます。

### Pump {#pump}

[Pump](https://github.com/pingcap/tidb-binlog/blob/release-7.5/pump)は、TiDB で生成されたバイナリ ログを記録し、トランザクションのコミット時間に基づいてバイナリ ログを並べ替え、消費するためにバイナリ ログをDrainerに送信するために使用されます。

### Drainer {#drainer}

[Drainer](https://github.com/pingcap/tidb-binlog/tree/release-7.5/drainer) 、各Pumpからバイナリログを収集してマージし、binlogをSQL または特定の形式のデータに変換し、データを特定のダウンストリーム プラットフォームにレプリケートします。

### <code>binlogctl</code>ガイド {#code-binlogctl-code-guide}

[`binlogctl`](https://github.com/pingcap/tidb-binlog/tree/release-7.5/binlogctl)は、次の機能を備えた TiDB Binlogの操作ツールです。

-   TiDB クラスターの現在の`tso`取得する
-   Pump・Drainerの状態確認
-   Pump/Drainerの状態を変更する
-   Pump/Drainerの一時停止または停止

## 主な特徴 {#main-features}

-   複数のポンプが水平​​方向にスケールアウトできるクラスターを形成します
-   TiDB は、組み込みのPumpクライアントを使用してbinlogを各Pumpに送信します。
-   Pumpはビンログを保存し、ビンログを順番にDrainerに送信します
-   Drainer は、各Pumpのバイナリログを読み取り、バイナリログをマージしてソートし、バイナリログをダウンストリームに送信します。
-   Drainerサポート[リレーログ](/tidb-binlog/tidb-binlog-relay-log.md) ． Drainer は、リレー ログによって、ダウンストリーム クラスターが一貫した状態にあることを確認します。

## ノート {#notes}

-   v5.1 では、v5.0 で導入されたクラスター化インデックス機能と TiDB Binlogの間の非互換性が解決されました。 TiDB Binlogと TiDB サーバーを v5.1 にアップグレードし、 TiDB Binlog を有効にすると、TiDB はクラスター化インデックスを使用したテーブルの作成をサポートします。クラスター化インデックスを使用して作成されたテーブルに対するデータの挿入、削除、更新は、 TiDB Binlogを介してダウンストリームにレプリケートされます。 TiDB Binlogを使用してクラスター化インデックスを持つテーブルをレプリケートする場合は、次の点に注意してください。

    -   アップグレード シーケンスを手動で制御してクラスターを v5.0 から v5.1 にアップグレードした場合は、TiDBサーバーを v5.1 にアップグレードする前に、TiDB binlogが v5.1 にアップグレードされていることを確認してください。
    -   アップストリームとダウンストリームの間で TiDB クラスター化インデックス テーブルの構造が一貫していることを確認するために、システム変数[`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)を同じ値に設定することをお勧めします。

-   TiDB Binlog は、 TiDB v5.0 で導入された以下の機能と互換性がないため、併用することはできません。

    -   [TiDB クラスター化インデックス](/clustered-indexes.md#limitations) : TiDB Binlogが有効になった後、TiDB は主キーとして非単一整数列を持つクラスター化インデックスの作成を許可しません。作成されたクラスター化インデックス テーブルのデータの挿入、削除、更新は、 TiDB Binlogを介してダウンストリームに複製されません。クラスター化インデックスを使用してテーブルをレプリケートする必要がある場合は、クラスターを v5.1 にアップグレードするか、代わりに[TiCDC](/ticdc/ticdc-overview.md)を使用してください。
    -   TiDB システム変数[tidb_enable_async_commit](/system-variables.md#tidb_enable_async_commit-new-in-v50) : TiDB Binlogが有効になった後は、このオプションを有効にしてもパフォーマンスを向上させることはできません。 TiDB Binlogの代わりに[TiCDC](/ticdc/ticdc-overview.md)使用することをお勧めします。
    -   TiDB システム変数[tidb_enable_1pc](/system-variables.md#tidb_enable_1pc-new-in-v50) : TiDB Binlogが有効になった後は、このオプションを有効にしてもパフォーマンスを向上させることはできません。 TiDB Binlogの代わりに[TiCDC](/ticdc/ticdc-overview.md)使用することをお勧めします。

-   Drainer は、MySQL、TiDB、Kafka、またはローカル ファイルへのバイナリログのレプリケートをサポートしています。 Drainer がサポートしていない他の宛先にバイナリ ログをレプリケートする必要がある場合は、binlogをKafka にレプリケートし、binlogコンシューマ プロトコルに従ってカスタマイズされた処理のために Kafka でデータを読み取るようにDrainerを設定できます。 [Binlog Consumer Clientユーザー ガイド](/tidb-binlog/binlog-consumer-client.md)を参照してください。

-   増分データのリカバリに TiDB Binlogを使用するには、構成`db-type`から`file` (プロト バッファー形式のローカル ファイル) を設定します。 Drainer は、 binlog を指定された[プロトバッファフォーマット](https://github.com/pingcap/tidb-binlog/blob/release-7.5/proto/pb_binlog.proto)のデータに変換し、そのデータをローカル ファイルに書き込みます。このように、 [Reparo](/tidb-binlog/tidb-binlog-reparo.md)使用してデータを段階的に回復できます。

    `db-type`の値に注意してください。

    -   TiDB バージョンが 2.1.9 より前の場合は、 `db-type="pb"`を設定します。
    -   TiDB バージョンが 2.1.9 以降の場合は、 `db-type="file"`または`db-type="pb"`を設定します。

-   ダウンストリームが MySQL、MariaDB、または別の TiDB クラスターの場合は、 [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)を使用してデータ レプリケーション後にデータを検証できます。
