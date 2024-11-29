---
title: TiDB Data Migration Overview
summary: データ移行ツール、アーキテクチャ、主要コンポーネント、および機能について学習します。
---

<!-- markdownlint-disable MD007 -->

# TiDB データ移行の概要 {#tidb-data-migration-overview}

<!--
![star](https://img.shields.io/github/stars/pingcap/tiflow?style=for-the-badge&logo=github) ![license](https://img.shields.io/github/license/pingcap/tiflow?style=for-the-badge) ![forks](https://img.shields.io/github/forks/pingcap/tiflow?style=for-the-badge)
-->

[TiDB データ移行](https://github.com/pingcap/tiflow/tree/release-8.1/dm) (DM) は、MySQL 互換データベース (MySQL、MariaDB、 Aurora MySQL など) から TiDB への完全なデータ移行と増分データレプリケーションをサポートする統合データ移行タスク管理プラットフォームです。データ移行の運用コストを削減し、トラブルシューティング プロセスを簡素化するのに役立ちます。

## 基本機能 {#basic-features}

-   **MySQL との互換性。DM**は、MySQL プロトコルおよびMySQL 5.7と MySQL 8.0 のほとんどの機能と構文と互換性があります。
-   **DML および DDL イベントのレプリケーション。MySQL** binlog内の DML および DDL イベントの解析とレプリケーションをサポートします。
-   **MySQL シャードの移行とマージ。DM**は、上流の複数の MySQL データベース インスタンスを下流の 1 つの TiDB データベースに移行およびマージすることをサポートします。さまざまな移行シナリオに合わせてレプリケーション ルールをカスタマイズできます。上流の MySQL シャードの DDL 変更を自動的に検出して処理できるため、運用コストが大幅に削減されます。
-   **さまざまな種類のフィルター。**データ移行プロセス中に MySQLbinlogイベントをフィルター処理するために、イベント タイプ、正規表現、SQL 式を事前定義できます。
-   **集中管理。DM**はクラスター内の数千のノードをサポートします。多数のデータ移行タスクを同時に実行および管理できます。
-   **サードパーティのオンラインスキーマ変更プロセスの最適化。MySQL**エコシステムでは、gh-ost や pt-osc などのツールが広く使用されています。DM は、中間データの不要な移行を回避するために変更プロセスを最適化します。詳細については、 [オンラインDDL](/dm/dm-online-ddl-tool-support.md)参照してください。
-   **高可用性。DM**は、異なるノード上で自由にスケジュールされるデータ移行タスクをサポートします。少数のノードがクラッシュしても、実行中のタスクは影響を受けません。

## クイックインストール {#quick-installation}

DM をインストールするには、次のコマンドを実行します。

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
tiup install dm dmctl
```

## 使用制限 {#usage-restrictions}

DM ツールを使用する前に、次の制限に注意してください。

-   データベースのバージョン要件

    -   MySQL バージョン 5.6 ~ 8.0

    -   MariaDB バージョン &gt;= 10.1.2 (実験的機能)

    > **注記：**
    >
    > アップストリーム MySQL/MariaDB サーバー間にプライマリ - セカンダリ移行構造がある場合は、次のバージョンを選択します。
    >
    > -   MySQL バージョン &gt; 5.7.1
    > -   MariaDB バージョン &gt;= 10.1.3

-   DDL構文の互換性

    -   現在、TiDB は MySQL がサポートするすべての DDL ステートメントと互換性がありません。DM は DDL ステートメントの処理に TiDB パーサーを使用するため、TiDB パーサーでサポートされる DDL 構文のみをサポートします。詳細については、 [MySQL 互換性](/mysql-compatibility.md#ddl-operations)参照してください。

    -   DM は、互換性のない DDL 文に遭遇するとエラーを報告します。このエラーを解決するには、この DDL 文をスキップするか、指定された DDL 文に置き換えるかして、dmctl を使用して手動で処理する必要があります。詳細については、 [異常なSQL文をスキップまたは置換する](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements)参照してください。

    -   DM は、ビュー関連の DDL ステートメントと DML ステートメントをダウンストリーム TiDB クラスターに複製しません。ダウンストリーム TiDB クラスターにビューを手動で作成することをお勧めします。

-   GBK 文字セットの互換性

    -   DM は、v5.4.0 より前の TiDB クラスターへの`charset=GBK`のテーブルの移行をサポートしていません。

-   Binlogの互換性

    -   DM は MySQL 8.0 の新機能binlog [トランザクションペイロードイベント](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html)をサポートしていません。binlog binlogを使用すると、アップストリームとダウンストリームの間でデータの不整合が発生する可能性があります。

## 貢献する {#contributing}

DM オープンソース プロジェクトへの参加を歓迎します。あなたの貢献は大歓迎です。詳細については、 [貢献.md](https://github.com/pingcap/tiflow/blob/release-8.1/dm/CONTRIBUTING.md)参照してください。

## コミュニティサポート {#community-support}

DM の詳細については、オンライン ドキュメントをご覧ください。ご質問がある場合は、 [GitHub](https://github.com/pingcap/tiflow/tree/release-8.1/dm)までお問い合わせください。

## ライセンス {#license}

DM は Apache 2.0 ライセンスに準拠しています。詳細については[ライセンス](https://github.com/pingcap/tiflow/blob/release-8.1/LICENSE)参照してください。

## DM バージョン {#dm-versions}

v5.4 より前の DM ドキュメントは TiDB ドキュメントから独立しています。以前のバージョンの DM ドキュメントにアクセスするには、次のいずれかのリンクをクリックしてください。

-   [DM v5.3 ドキュメント](https://docs.pingcap.com/tidb-data-migration/v5.3)
-   [DM v2.0 ドキュメント](https://docs.pingcap.com/tidb-data-migration/v2.0/)
-   [DM v1.0 ドキュメント](https://docs.pingcap.com/tidb-data-migration/v1.0/)

> **注記：**
>
> -   2021 年 10 月より、DM の GitHub リポジトリは[ピンキャップ/tiflow](https://github.com/pingcap/tiflow/tree/release-8.1/dm)に移動されました。DM で問題が発生した場合は、フィードバックを得るために`pingcap/tiflow`リポジトリに問題を送信してください。
> -   以前のバージョン (v1.0 および v2.0) では、DM は TiDB とは独立したバージョン番号を使用します。v5.3 以降、DM は TiDB と同じバージョン番号を使用します。DM v2.0 の次のバージョンは DM v5.3 です。DM v2.0 から v5.3 への互換性の変更はなく、アップグレード プロセスは通常のアップグレードと同じで、バージョン番号の増加のみです。
