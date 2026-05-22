---
title: TiDB Data Migration Overview
summary: データ移行ツール、そのアーキテクチャ、主要コンポーネント、および機能について学びましょう。
---

<!-- markdownlint-disable MD007 -->

# TiDBデータ移行の概要 {#tidb-data-migration-overview}

<!--
![star](https://img.shields.io/github/stars/pingcap/tiflow?style=for-the-badge&logo=github) ![license](https://img.shields.io/github/license/pingcap/tiflow?style=for-the-badge) ![forks](https://img.shields.io/github/forks/pingcap/tiflow?style=for-the-badge)
-->

[TiDBデータ移行](https://github.com/pingcap/tiflow/tree/release-8.5/dm)(DM)は、統合データ移行タスク管理プラットフォームであり、MySQL互換データベース（MySQL、MariaDB、 Aurora MySQLなど）からTiDBへのフルデータ移行と増分データレプリケーションをサポートします。データ移行の運用コストを削減し、トラブルシューティングプロセスを簡素化するのに役立ちます。

## 基本機能 {#basic-features}

-   **MySQLとの互換性。DM**はMySQLプロトコルと互換性があり、 MySQL 5.7およびMySQL 8.0のほとんどの機能と構文に対応しています。
-   **DMLおよびDDLイベントの複製。MySQL**binlog内のDMLおよびDDLイベントの解析と複製をサポートします。
-   **MySQLシャードの移行とマージ。DM**は、複数のMySQLデータベースインスタンスを上流から下流の1つのTiDBデータベースに移行およびマージすることをサポートします。さまざまな移行シナリオに合わせてレプリケーションルールをカスタマイズできます。上流のMySQLシャードのDDL変更を自動的に検出して処理できるため、運用コストを大幅に削減できます。
-   **さまざまな種類のフィルタ。**イベントタイプ、正規表現、SQL式を事前に定義することで、データ移行プロセス中にMySQLbinlogイベントをフィルタリングできます。
-   **集中管理。DM**はクラスター内の数千ノードをサポートし、多数のデータ移行タスクを同時に実行および管理できます。
-   **サードパーティのオンラインスキーマ変更プロセスの最適化。MySQL**エコシステムでは、gh-ostやpt-oscなどのツールが広く使用されています。DMは、中間データの不要な移行を回避するために変更プロセスを最適化します。詳細は、[オンラインDDL](/dm/dm-online-ddl-tool-support.md)参照してください。
-   **高可用性。DM**は、データ移行タスクを異なるノードに自由にスケジュールすることをサポートします。少数のノードがクラッシュしても、実行中のタスクには影響しません。

## クイックインストール {#quick-installation}

DMをインストールするには、以下のコマンドを実行してください。

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
tiup install dm dmctl
```

## 使用制限 {#usage-restrictions}

DMツールを使用する前に、以下の制限事項にご注意ください。

-   データベースのバージョン要件

    -   MySQL バージョン 5.6 ～ 8.0

    -   MariaDB バージョン &gt;= 10.1.2 (実験的機能)

    > **注記：**
    >
    > 上流のMySQL/MariaDBサーバー間にプライマリ/セカンダリ移行構造がある場合は、次のバージョンを選択してください。
    >
    > -   MySQLバージョン &gt; 5.7.1
    > -   MariaDB バージョン &gt;= 10.1.3

-   DDL構文の互換性

    -   現在、TiDBはMySQLがサポートするすべてのDDLステートメントと互換性があるわけではありません。DMはTiDBパーサーを使用してDDLステートメントを処理するため、TiDBパーサーがサポートするDDL構文のみをサポートします。詳細については、 [MySQLとの互換性](/mysql-compatibility.md#ddl-operations)参照してください。

    -   DM は、互換性のない DDL ステートメントが発生するとエラーを報告します。このエラーを解決するには、dmctl を使用して手動で処理し、この DDL ステートメントをスキップするか、指定された DDL ステートメントに置き換える必要があります。詳細については、 [異常な SQL ステートメントをスキップまたは置換します](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements)参照してください。

    -   DMは、ビュー関連のDDLステートメントおよびDMLステートメントをダウンストリームのTiDBクラスターに複製しません。ダウンストリームのTiDBクラスターでビューを手動で作成することをお勧めします。

-   GBK文字セットとの互換性

    -   DM は、v5.4.0 より前の TiDB クラスターへの`charset=GBK`テーブルの移動をサポートしていません。

-   Binlogの互換性

    -   DM は、MySQL 8.0 の新機能binlog [トランザクションペイロードイベント](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html)イベントをサポートしていません。 binlog Transaction_payload_event を使用すると、アップストリームとダウンストリームの間でデータの不整合が発生する可能性があります。

-   ベクトルデータ型の複製

    -   DMは、MySQLベクトルデータ型をTiDBに移行または複製することをサポートしていません。

## 貢献する {#contributing}

DMオープンソースプロジェクトへのご参加を歓迎いたします。皆様のご貢献を心よりお待ちしております。詳細については、 [CONTRIBUTING.md](https://github.com/pingcap/tiflow/blob/release-8.5/dm/CONTRIBUTING.md)をご覧ください。

## コミュニティのサポート {#community-support}

DMについては、オンラインドキュメントで詳しく学ぶことができます。ご質問があれば、 [GitHub](https://github.com/pingcap/tiflow/tree/release-8.5/dm)でお問い合わせください。

## ライセンス {#license}

DM は Apache 2.0 ライセンスに準拠しています。詳細については、 [ライセンス](https://github.com/pingcap/tiflow/blob/release-8.5/LICENSE)を参照してください。

## DM版 {#dm-versions}

バージョン5.4より前のDMドキュメントは、TiDBドキュメントとは独立しています。これらの以前のバージョンのDMドキュメントにアクセスするには、以下のリンクのいずれかをクリックしてください。

-   [DM v5.3 ドキュメント](https://docs-archive.pingcap.com/tidb-data-migration/v5.3/)
-   [DM v2.0 ドキュメント](https://docs-archive.pingcap.com/tidb-data-migration/v2.0/)
-   [DM v1.0 ドキュメント](https://docs-archive.pingcap.com/tidb-data-migration/v1.0/)

> **注記：**
>
> -   2021年10月以降、DMのGitHubリポジトリは[pingcap/tiflow](https://github.com/pingcap/tiflow/tree/master/dm)に移行しました。DMに問題がある場合は、フィードバックのために`pingcap/tiflow`リポジトリに問題を報告してください。
> -   以前のバージョン（v1.0およびv2.0）では、DMはTiDBとは独立したバージョン番号を使用していました。v5.3以降、DMはTiDBと同じバージョン番号を使用するようになりました。DM v5.3はDM v2.0に互換性の変更はなく、アップグレードプロセスは標準的なもので、バージョン番号を上げるだけです。
