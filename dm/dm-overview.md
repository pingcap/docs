---
title: TiDB Data Migration Overview
summary: データ移行ツール、アーキテクチャ、主要コンポーネント、および機能について学習します。
---

<!-- markdownlint-disable MD007 -->

# TiDB データ移行の概要 {#tidb-data-migration-overview}

<!--
![star](https://img.shields.io/github/stars/pingcap/tiflow?style=for-the-badge&logo=github) ![license](https://img.shields.io/github/license/pingcap/tiflow?style=for-the-badge) ![forks](https://img.shields.io/github/forks/pingcap/tiflow?style=for-the-badge)
-->

[TiDBデータ移行](https://github.com/pingcap/tiflow/tree/release-8.5/dm)は、MySQL互換データベース（MySQL、MariaDB、 Aurora MySQLなど）からTiDBへの完全なデータ移行と増分データレプリケーションをサポートする統合データ移行タスク管理プラットフォームです。データ移行の運用コストを削減し、トラブルシューティングプロセスを簡素化します。

## 基本機能 {#basic-features}

-   **MySQL との互換性。DM**は、MySQL プロトコルおよびMySQL 5.7と MySQL 8.0 のほとんどの機能と構文と互換性があります。
-   **DML および DDL イベントのレプリケーション。MySQL** binlog内の DML および DDL イベントの解析とレプリケーションをサポートします。
-   **MySQLシャードの移行とマージ。DM**は、上流の複数のMySQLデータベースインスタンスを下流の1つのTiDBデータベースに移行およびマージする機能をサポートします。また、様々な移行シナリオに合わせてレプリケーションルールをカスタマイズできます。上流のMySQLシャードのDDL変更を自動的に検出・処理できるため、運用コストを大幅に削減できます。
-   **さまざまな種類のフィルター。**イベントタイプ、正規表現、SQL 式を事前に定義して、データ移行プロセス中に MySQLbinlogイベントを除外できます。
-   **一元管理。DM**はクラスター内の数千ノードをサポートします。多数のデータ移行タスクを同時に実行・管理できます。
-   **サードパーティのオンラインスキーマ変更プロセスの最適化。MySQL**エコシステムでは、gh-ostやpt-oscなどのツールが広く使用されています。DMは、中間データの不要な移行を回避するために変更プロセスを最適化します。詳細については、 [オンラインDDL](/dm/dm-online-ddl-tool-support.md)参照してください。
-   **高可用性。DM**は、データ移行タスクを異なるノード間で自由にスケジュール設定できます。少数のノードがクラッシュしても、実行中のタスクは影響を受けません。

## クイックインストール {#quick-installation}

DM をインストールするには、次のコマンドを実行します。

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
tiup install dm dmctl
```

## 使用制限 {#usage-restrictions}

DM ツールを使用する前に、次の制限に注意してください。

-   データベースのバージョン要件

    -   MySQL バージョン 5.6 ～ 8.0

    -   MariaDB バージョン &gt;= 10.1.2 (実験的機能)

    > **注記：**
    >
    > アップストリーム MySQL/MariaDB サーバー間にプライマリ - セカンダリ移行構造がある場合は、次のバージョンを選択します。
    >
    > -   MySQLバージョン &gt; 5.7.1
    > -   MariaDB バージョン &gt;= 10.1.3

-   DDL構文の互換性

    -   現在、TiDBはMySQLがサポートするすべてのDDL文と互換性がありません。DMはTiDBパーサーを使用してDDL文を処理するため、TiDBパーサーがサポートするDDL構文のみをサポートします。詳細については、 [MySQLの互換性](/mysql-compatibility.md#ddl-operations)参照してください。

    -   DMは互換性のないDDL文を検出するとエラーを報告します。このエラーを解決するには、dmctlを使用して手動で処理する必要があります。このDDL文をスキップするか、指定されたDDL文に置き換えます。詳細については、 [異常なSQL文をスキップまたは置換する](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements)参照してください。

    -   DMは、ビュー関連のDDL文とDML文を下流TiDBクラスタに複製しません。下流TiDBクラスタにビューを手動で作成することをお勧めします。

-   GBK文字セットの互換性

    -   DM は、v5.4.0 より前の TiDB クラスターへの`charset=GBK`テーブルの移行をサポートしていません。

-   Binlogの互換性

    -   DMはMySQL 8.0の新機能binlog [トランザクションペイロードイベント](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html)をサポートしていません。binlog Transaction_payload_eventを使用すると、上流と下流の間でデータの不整合が発生する可能性があります。

-   ベクトルデータ型の複製

    -   DM は、MySQL ベクトル データ型の TiDB への移行または複製をサポートしていません。

## 貢献 {#contributing}

DMオープンソースプロジェクトへのご参加をお待ちしております。皆様のご貢献を心よりお待ちしております。詳細は[貢献.md](https://github.com/pingcap/tiflow/blob/release-8.5/dm/CONTRIBUTING.md)ご覧ください。

## コミュニティサポート {#community-support}

DMの詳細については、オンラインドキュメントをご覧ください。ご質問がございましたら、 [GitHub](https://github.com/pingcap/tiflow/tree/release-8.5/dm)までお問い合わせください。

## ライセンス {#license}

DMはApache 2.0ライセンスに準拠しています。詳細については[ライセンス](https://github.com/pingcap/tiflow/blob/release-8.5/LICENSE)参照してください。

## DMバージョン {#dm-versions}

バージョン5.4より前のDMドキュメントは、TiDBドキュメントとは独立しています。以前のバージョンのDMドキュメントにアクセスするには、以下のリンクのいずれかをクリックしてください。

-   [DM v5.3 ドキュメント](https://docs-archive.pingcap.com/tidb-data-migration/v5.3/)
-   [DM v2.0 ドキュメント](https://docs-archive.pingcap.com/tidb-data-migration/v2.0/)
-   [DM v1.0 ドキュメント](https://docs-archive.pingcap.com/tidb-data-migration/v1.0/)

> **注記：**
>
> -   2021年10月より、DMのGitHubリポジトリは[ピングキャップ/ティフロー](https://github.com/pingcap/tiflow/tree/release-8.5/dm)に移行しました。DMで問題が発生した場合は、 `pingcap/tiflow`リポジトリに問題を報告してフィードバックをお寄せください。
> -   以前のバージョン（v1.0およびv2.0）では、DMはTiDBとは独立したバージョン番号を使用していました。v5.3以降、DMはTiDBと同じバージョン番号を使用します。DM v2.0の次のバージョンはDM v5.3です。DM v2.0からv5.3への互換性の変更はなく、アップグレードプロセスは通常のアップグレードと同じで、バージョン番号の増加のみです。
