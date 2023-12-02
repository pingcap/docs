---
title: TiDB Data Migration Overview
summary: Learn about the Data Migration tool, the architecture, the key components, and features.
---

<!-- markdownlint-disable MD007 -->

# TiDB データ移行の概要 {#tidb-data-migration-overview}

<!--
![star](https://img.shields.io/github/stars/pingcap/tiflow?style=for-the-badge&logo=github) ![license](https://img.shields.io/github/license/pingcap/tiflow?style=for-the-badge) ![forks](https://img.shields.io/github/forks/pingcap/tiflow?style=for-the-badge)
-->

[TiDB データ移行](https://github.com/pingcap/tiflow/tree/release-7.5/dm) (DM) は、統合されたデータ移行タスク管理プラットフォームであり、MySQL 互換データベース (MySQL、MariaDB、 Aurora MySQL など) から TiDB への完全なデータ移行と増分データ レプリケーションをサポートします。データ移行の運用コストを削減し、トラブルシューティング プロセスを簡素化するのに役立ちます。

## 基本的な機能 {#basic-features}

-   **MySQLとの互換性。** DM は、MySQL 5.7プロトコル、およびMySQL 5.7のほとんどの機能と構文と互換性があります。
-   **DML および DDL イベントをレプリケートします。** MySQL binlogでの DML および DDL イベントの解析とレプリケートをサポートします。
-   **MySQL シャードの移行とマージ。** DM は、複数の MySQL データベース インスタンスをアップストリームから 1 つの TiDB データベース ダウンストリームに移行およびマージすることをサポートします。さまざまな移行シナリオに合わせてレプリケーション ルールのカスタマイズをサポートします。アップストリーム MySQL シャードの DDL 変更を自動的に検出して処理できるため、運用コストが大幅に削減されます。
-   **各種フィルター。**イベント タイプ、正規表現、および SQL 式を事前定義して、データ移行プロセス中に MySQLbinlogイベントをフィルタリングして除外できます。
-   **一元管理。** DM はクラスター内の数千のノードをサポートします。多数のデータ移行タスクを同時に実行および管理できます。
-   **サードパーティのオンライン スキーマ変更プロセスの最適化。** MySQL エコシステムでは、gh-ost や pt-osc などのツールが広く使用されています。 DM は変更プロセスを最適化し、中間データの不必要な移行を回避します。詳細は[オンライン-ddl](/dm/dm-online-ddl-tool-support.md)を参照してください。
-   **高可用性。** DM は、さまざまなノード上で自由にスケジュールできるデータ移行タスクをサポートしています。少数のノードがクラッシュしても、実行中のタスクは影響を受けません。

## クイックインストール {#quick-installation}

次のコマンドを実行して DM をインストールします。

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
tiup install dm dmctl
```

## 使用制限 {#usage-restrictions}

DM ツールを使用する前に、次の制限事項に注意してください。

-   データベースのバージョン要件

    -   MySQLバージョン5.5～5.7

    -   MySQL バージョン 8.0 (実験的機能)

    -   MariaDB バージョン &gt;= 10.1.2 (実験的機能)

    > **注記：**
    >
    > 上流の MySQL/MariaDB サーバー間にプライマリとセカンダリの移行構造がある場合は、次のバージョンを選択します。
    >
    > -   MySQL バージョン &gt; 5.7.1
    > -   MariaDB バージョン &gt;= 10.1.3

-   DDL 構文の互換性

    -   現在、TiDB は、MySQL がサポートするすべての DDL ステートメントと互換性があるわけではありません。 DM は TiDB パーサーを使用して DDL ステートメントを処理するため、TiDB パーサーによってサポートされる DDL 構文のみをサポートします。詳細は[MySQL の互換性](/mysql-compatibility.md#ddl-operations)を参照してください。

    -   DM は、互換性のない DDL ステートメントが発生するとエラーを報告します。このエラーを解決するには、dmctl を使用して手動で処理し、この DDL ステートメントをスキップするか、指定された DDL ステートメントに置き換える必要があります。詳細は[異常な SQL ステートメントをスキップまたは置換する](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements)を参照してください。

    -   DM は、ビュー関連の DDL ステートメントおよび DML ステートメントをダウンストリーム TiDB クラスターに複製しません。ダウンストリーム TiDB クラスターにビューを手動で作成することをお勧めします。

-   GBK 文字セットの互換性

    -   DM は、v5.4.0 より前の TiDB クラスターへの`charset=GBK`テーブルの移行をサポートしていません。

## 貢献する {#contributing}

DM オープンソース プロジェクトにぜひご参加ください。皆様のご貢献を心よりお待ちしております。詳細については、 [貢献.md](https://github.com/pingcap/tiflow/blob/release-7.5/dm/CONTRIBUTING.md)を参照してください。

## コミュニティサポート {#community-support}

DM については、オンライン ドキュメントを通じて学習できます。ご質問がございましたら、 [GitHub](https://github.com/pingcap/tiflow/tree/release-7.5/dm)でお問い合わせください。

## ライセンス {#license}

DM は Apache 2.0 ライセンスに準拠しています。詳細については、 [ライセンス](https://github.com/pingcap/tiflow/blob/release-7.5/LICENSE)を参照してください。

## DMバージョン {#dm-versions}

v5.4 より前では、DM ドキュメントは TiDB ドキュメントから独立していました。これらの以前のバージョンの DM ドキュメントにアクセスするには、次のリンクのいずれかをクリックします。

-   [DM v5.3 ドキュメント](https://docs.pingcap.com/tidb-data-migration/v5.3)
-   [DM v2.0 ドキュメント](https://docs.pingcap.com/tidb-data-migration/v2.0/)
-   [DM v1.0 ドキュメント](https://docs.pingcap.com/tidb-data-migration/v1.0/)

> **注記：**
>
> -   2021 年 10 月以降、DM の GitHub リポジトリは[ピンキャップ/ティフロー](https://github.com/pingcap/tiflow/tree/release-7.5/dm)に移動されました。 DM に問題がある場合は、フィードバックのために`pingcap/tiflow`リポジトリに問題を送信してください。
> -   以前のバージョン (v1.0 および v2.0) では、DM は TiDB から独立したバージョン番号を使用します。 v5.3 以降、DM は TiDB と同じバージョン番号を使用します。 DM v2.0 の次のバージョンは DM v5.3 です。 DM v2.0 から v5.3 への互換性の変更はなく、アップグレード プロセスは通常のアップグレードと同じですが、バージョン番号が増加するだけです。
