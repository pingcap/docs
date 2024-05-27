---
title: TiDB Binlog Overview
summary: TiDB Binlogのクラスター バージョンの概要を学習します。
---

# TiDBBinlogクラスタの概要 {#tidb-binlog-cluster-overview}

このドキュメントでは、 TiDB Binlogのクラスター バージョンのアーキテクチャとデプロイメントについて説明します。

TiDB Binlog は、TiDB からbinlogデータを収集し、下流のプラットフォームにほぼリアルタイムのバックアップとレプリケーションを提供するツールです。

TiDB Binlog には次の機能があります。

-   **データレプリケーション:** TiDBクラスタ内のデータを他のデータベースに複製する
-   **リアルタイムのバックアップと復元:** TiDB クラスター内のデータをバックアップし、クラスターに障害が発生したときに TiDB クラスターを復元します。

> **注記：**
>
> -   TiDB Binlog はTiDB v5.0 で導入された一部の機能と互換性がなく、併用できません。詳細については[ノート](#notes)を参照してください。
> -   TiDB v7.5.0 以降、TiDB Binlogのデータ レプリケーション機能のテクニカル サポートは提供されなくなりました。データ レプリケーションの代替ソリューションとして[ティCDC](/ticdc/ticdc-overview.md)を使用することを強くお勧めします。
> -   TiDB v7.5.0 では、TiDB Binlogのリアルタイム バックアップと復元機能が引き続きサポートされていますが、このコンポーネントは将来のバージョンでは完全に廃止される予定です。データ復旧の代替ソリューションとして[ピトル](/br/br-pitr-guide.md)を使用することをお勧めします。

## TiDBBinlogアーキテクチャ {#tidb-binlog-architecture}

TiDB Binlogアーキテクチャは次のとおりです。

![TiDB Binlog architecture](/media/tidb-binlog-cluster-architecture.png)

TiDB Binlogクラスターは、 PumpとDrainerで構成されています。

### Pump {#pump}

[Pump](https://github.com/pingcap/tidb-binlog/blob/release-8.1/pump)は、TiDB で生成されたバイナリログを記録し、トランザクションのコミット時間に基づいてバイナリログをソートし、消費のためにDrainerにバイナリログを送信するために使用されます。

### Drainer {#drainer}

[Drainer](https://github.com/pingcap/tidb-binlog/tree/release-8.1/drainer)各Pumpからバイナリログを収集してマージし、binlogをSQL または特定の形式のデータに変換し、データを特定のダウンストリーム プラットフォームに複製します。

### <code>binlogctl</code>ガイド {#code-binlogctl-code-guide}

[`binlogctl`](https://github.com/pingcap/tidb-binlog/tree/release-8.1/binlogctl) 、以下の機能を備えた TiDB Binlogの操作ツールです。

-   TiDBクラスタの現在の`tso`取得
-   Pump/Drainerの状態を確認する
-   Pump/Drainerの状態を変更する
-   Pump/Drainerの一時停止または閉鎖

## 主な特徴 {#main-features}

-   複数のポンプが水平​​方向にスケールアウトできるクラスターを形成する
-   TiDBは組み込みのPumpクライアントを使用して各Pumpにbinlogを送信します。
-   Pumpはバイナリログを保存し、順番にDrainerにバイナリログを送信します。
-   Drainerは各Pumpのバイナリログを読み取り、バイナリログをマージしてソートし、バイナリログを下流に送信します。
-   Drainer は[リレーログ](/tidb-binlog/tidb-binlog-relay-log.md)サポートします。リレー ログによって、 Drainer は下流のクラスターが一貫した状態であることを確認します。

## ノート {#notes}

-   v5.1 では、v5.0 で導入されたクラスター化インデックス機能と TiDB Binlog間の非互換性が解決されました。 TiDB Binlogと TiDB Server を v5.1 にアップグレードし、 TiDB Binlogを有効にすると、 TiDB はクラスター化インデックスを持つテーブルの作成をサポートするようになり、クラスター化インデックスを持つ作成されたテーブルへのデータの挿入、削除、更新は、 TiDB Binlogを介してダウンストリームにレプリケートされます。 TiDB Binlogを使用してクラスター化インデックスを持つテーブルをレプリケートする場合は、次の点に注意してください。

    -   アップグレード シーケンスを手動で制御してクラスターを v5.0 から v5.1 にアップグレードした場合は、TiDBサーバーをv5.1 にアップグレードする前に、TiDB binlogが v5.1 にアップグレードされていることを確認してください。
    -   アップストリームとダウンストリーム間の TiDB クラスター化インデックス テーブルの構造が一貫していることを確認するには、システム変数[`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)を同じ値に設定することをお勧めします。

-   TiDB Binlog は、TiDB v5.0 で導入された次の機能と互換性がなく、一緒に使用することはできません。

    -   [TiDB クラスター化インデックス](/clustered-indexes.md#limitations) : TiDB Binlogを有効にすると、 TiDB では、主キーとして単一でない整数列を持つクラスター化インデックスの作成が許可されなくなります。作成されたクラスター化インデックス テーブルのデータ挿入、削除、および更新は、 TiDB Binlogを介して下流に複製されません。クラスター化インデックスを持つテーブルを複製する必要がある場合は、クラスターを v5.1 にアップグレードするか、代わりに[ティCDC](/ticdc/ticdc-overview.md)使用してください。
    -   TiDB システム変数[tidb_enable_async_commit](/system-variables.md#tidb_enable_async_commit-new-in-v50) : TiDB Binlogを有効にした後、このオプションを有効にしてもパフォーマンスは向上しません。 TiDB Binlogの代わりに[ティCDC](/ticdc/ticdc-overview.md)使用することをお勧めします。
    -   TiDB システム変数[tidb_enable_1pc](/system-variables.md#tidb_enable_1pc-new-in-v50) : TiDB Binlogを有効にした後、このオプションを有効にしてもパフォーマンスは向上しません。 TiDB Binlogの代わりに[ティCDC](/ticdc/ticdc-overview.md)使用することをお勧めします。

-   Drainer は、MySQL、TiDB、Kafka、またはローカル ファイルへの binlog の複製をサポートしています。DrainerがDrainerしていない他の宛先に binlog を複製する必要がある場合は、 Drainerを設定してbinlogを Kafka に複製し、Kafka でデータを読み取って、 binlogコンシューマー プロトコルに従ってカスタマイズされた処理を行うことができます。1 [Binlog Consumer Clientユーザー ガイド](/tidb-binlog/binlog-consumer-client.md)参照してください。

-   TiDB Binlogを使用して増分データを回復するには、config `db-type`を`file` (proto buffer 形式のローカル ファイル) に設定します。Drainerは、 binlogを指定された[プロトバッファフォーマット](https://github.com/pingcap/tidb-binlog/blob/release-8.1/proto/pb_binlog.proto)のデータに変換し、ローカル ファイルに書き込みます。このようにして、 [Reparo](/tidb-binlog/tidb-binlog-reparo.md)を使用してデータを増分的に回復できます。

    `db-type`の値に注目してください:

    -   TiDB バージョンが 2.1.9 より前の場合は、 `db-type="pb"`設定します。
    -   TiDB バージョンが 2.1.9 以降の場合は、 `db-type="file"`または`db-type="pb"`設定します。

-   ダウンストリームが MySQL、MariaDB、または別の TiDB クラスターの場合は、 [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)使用してデータ複製後のデータを検証できます。
