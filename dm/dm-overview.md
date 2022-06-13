---
title: Data Migration Overview
summary: Learn about the Data Migration tool, the architecture, the key components, and features.
---

<!-- markdownlint-disable MD007 -->

# データ移行の概要 {#data-migration-overview}

<!--
![star](https://img.shields.io/github/stars/pingcap/tiflow?style=for-the-badge&logo=github) ![license](https://img.shields.io/github/license/pingcap/tiflow?style=for-the-badge) ![forks](https://img.shields.io/github/forks/pingcap/tiflow?style=for-the-badge)
-->

[TiDBデータ移行](https://github.com/pingcap/dm) （DM）は統合データ移行タスク管理プラットフォームであり、MySQL互換データベース（MySQL、MariaDB、 Aurora MySQLなど）からTiDBへの完全なデータ移行と増分データ複製をサポートします。データ移行の運用コストを削減し、トラブルシューティングプロセスを簡素化するのに役立ちます。

## 基本的な機能 {#basic-features}

-   **MySQLとの互換性。** DMは、MySQL 5.7プロトコル、およびMySQL5.7のほとんどの機能と構文と互換性があります。
-   **DMLおよびDDLイベントの複製。** MySQLbinlogでのDMLおよびDDLイベントの解析と複製をサポートします。
-   **MySQLシャードの移行とマージ。** DMは、アップストリームの複数のMySQLデータベースインスタンスをダウンストリームの1つのTiDBデータベースに移行およびマージすることをサポートします。さまざまな移行シナリオに合わせたレプリケーションルールのカスタマイズをサポートします。アップストリームのMySQLシャードのDDL変更を自動的に検出して処理できるため、運用コストが大幅に削減されます。
-   **さまざまな種類のフィルター。**イベントタイプ、正規表現、およびSQL式を事前定義して、データ移行プロセス中にMySQLbinlogイベントを除外できます。
-   **一元管理。** DMは、クラスタの数千のノードをサポートします。多数のデータ移行タスクを同時に実行および管理できます。
-   **サードパーティのオンラインスキーマ変更プロセスの最適化。** MySQLエコシステムでは、gh-ostやpt-oscなどのツールが広く使用されています。 DMは、変更プロセスを最適化して、中間データの不要な移行を回避します。詳細については、 [online-ddl](/dm/dm-key-features.md#online-ddl-tools)を参照してください。
-   **高可用性。** DMは、さまざまなノードで自由にスケジュールできるデータ移行タスクをサポートしています。少数のノードがクラッシュしても、実行中のタスクは影響を受けません。

## クイックインストール {#quick-installation}

次のコマンドを実行してDMをインストールします。

{{< copyable "" >}}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
tiup install dm dmctl
```

## 使用制限 {#usage-restrictions}

DMツールを使用する前に、次の制限に注意してください。

-   データベースのバージョン要件

    -   MySQLバージョン5.5〜5.7

    -   MySQLバージョン8.0（実験的機能）

    -   MariaDBバージョン&gt;=10.1.2（実験的機能）

    > **ノート：**
    >
    > アップストリームのMySQL/MariaDBサーバー間にプライマリ-セカンダリ移行構造がある場合は、次のバージョンを選択します。
    >
    > -   MySQLバージョン&gt;5.7.1
    > -   MariaDBバージョン&gt;=10.1.3

-   DDL構文の互換性

    -   現在、TiDBはMySQLがサポートするすべてのDDLステートメントと互換性があるわけではありません。 DMはTiDBパーサーを使用してDDLステートメントを処理するため、TiDBパーサーでサポートされているDDL構文のみをサポートします。詳細については、 [MySQLの互換性](/mysql-compatibility.md#ddl)を参照してください。

    -   DMは、互換性のないDDLステートメントを検出すると、エラーを報告します。このエラーを解決するには、このDDLステートメントをスキップするか、指定されたDDLステートメントに置き換えることにより、dmctlを使用して手動で処理する必要があります。詳細については、 [異常なSQLステートメントをスキップまたは置換します](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements)を参照してください。

-   GBK文字セットの互換性

    -   DMは、v5.4.0より前のTiDBクラスターへの`charset=GBK`のテーブルの移行をサポートしていません。

## 貢献 {#contributing}

DMオープンソーシングプロジェクトにご参加いただけます。どうぞよろしくお願いいたします。詳細については、 [CONTRIBUTING.md](https://github.com/pingcap/tiflow/blob/master/dm/CONTRIBUTING.md)を参照してください。

## コミュニティサポート {#community-support}

DMについては、オンラインドキュメントから学ぶことができます。ご不明な点がございましたら、 [GitHub](https://github.com/pingcap/tiflow/tree/master/dm)までお問い合わせください。

## ライセンス {#license}

DMはApache2.0ライセンスに準拠しています。詳細については、 [ライセンス](https://github.com/pingcap/tiflow/blob/master/dm/LICENSE)を参照してください。

## DMバージョン {#dm-versions}

v5.4より前では、DMドキュメントはTiDBドキュメントから独立しています。これらの以前のバージョンのDMドキュメントにアクセスするには、次のリンクのいずれかをクリックします。

-   [DMv5.3のドキュメント](https://docs.pingcap.com/tidb-data-migration/v5.3)
-   [DMv2.0のドキュメント](https://docs.pingcap.com/tidb-data-migration/v2.0/)
-   [DMv1.0のドキュメント](https://docs.pingcap.com/tidb-data-migration/v1.0/)

> **ノート：**
>
> -   2021年10月以降、DMのGitHubリポジトリは[pingcap / tiflow](https://github.com/pingcap/tiflow/tree/master/dm)に移動されました。 DMに問題がある場合は、フィードバックのために`pingcap/tiflow`リポジトリに問題を送信してください。
> -   以前のバージョン（v1.0およびv2.0）では、DMはTiDBに依存しないバージョン番号を使用します。 v5.3以降、DMはTiDBと同じバージョン番号を使用します。 DMv2.0の次のバージョンはDMv5.3です。 DM v2.0からv5.3への互換性の変更はなく、アップグレードプロセスは通常のアップグレードと同じですが、バージョン番号が増えるだけです。
