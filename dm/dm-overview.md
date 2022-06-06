---
title: Data Migration Overview
summary: Learn about the Data Migration tool, the architecture, the key components, and features.
---

<!-- markdownlint-disable MD007 -->

# データ移行の概要 {#data-migration-overview}

[TiDBデータ移行](https://github.com/pingcap/dm) （DM）は統合データ移行タスク管理プラットフォームであり、MySQL互換データベース（MySQL、MariaDB、 Aurora MySQLなど）からTiDBへの完全なデータ移行と増分データレプリケーションをサポートします。データ移行の運用コストを削減し、トラブルシューティングプロセスを簡素化するのに役立ちます。データ移行にDMを使用する場合は、次の操作を実行する必要があります。

-   DMクラスターをデプロイする
-   アップストリームデータソースを作成し、データソースアクセス情報を保存します
-   データ移行タスクを作成して、データをデータソースからTiDBに移行します

データ移行タスクには、完全なデータ移行と増分データレプリケーションの2つの段階があります。

-   完全なデータ移行：対応するテーブルのテーブル構造をデータソースからTiDBに移行してから、データソースに格納されているデータを読み取り、TiDBクラスタに書き込みます。
-   インクリメンタルデータレプリケーション：完全なデータ移行が完了すると、データソースからの対応するテーブルの変更が読み取られ、TiDBクラスタに書き込まれます。

## DMバージョン {#dm-versions}

このドキュメントは、DMの最新の安定バージョンであるDMv5.4に適用されます。

v5.4より前では、DMドキュメントはTiDBドキュメントから独立しています。これらの以前のバージョンのDMドキュメントにアクセスするには、次のリンクのいずれかをクリックします。

-   [DMv5.3のドキュメント](https://docs.pingcap.com/tidb-data-migration/v5.3)
-   [DMv2.0のドキュメント](https://docs.pingcap.com/tidb-data-migration/v2.0/)
-   [DMv1.0のドキュメント](https://docs.pingcap.com/tidb-data-migration/v1.0/) （DMの最も初期の安定バージョンであるため、お勧めしません）

> **ノート：**
>
> -   2021年10月以降、DMのGitHubリポジトリは[pingcap / tiflow](https://github.com/pingcap/tiflow/tree/master/dm)に移動されました。 DMに問題がある場合は、フィードバックのために`pingcap/tiflow`リポジトリに問題を送信してください。
> -   以前のバージョン（v1.0およびv2.0）では、DMはTiDBに依存しないバージョン番号を使用します。 v5.3以降、DMはTiDBと同じバージョン番号を使用します。 DMv2.0の次のバージョンはDMv5.3です。 DM v2.0からv5.3への互換性の変更はなく、アップグレードプロセスは通常のアップグレードと同じで、バージョン番号が増えるだけです。

## 基本的な機能 {#basic-features}

このセクションでは、DMが提供する基本的なデータ移行機能について説明します。

![DM Core Features](/media/dm/dm-core-features.png)

### スキーマおよびテーブルレベルでのリストの移行をブロックおよび許可する {#block-and-allow-lists-migration-at-the-schema-and-table-levels}

[リストのフィルタリングルールをブロックして許可する](/dm/dm-key-features.md#block-and-allow-table-lists)は、MySQLの`replication-rules-db`機能に似ており、一部のデータベースのみまたは一部のテーブルのみのすべての操作をフィルタリングまたは複製するために使用でき`replication-rules-table` 。

### Binlogイベントフィルタリング {#binlog-event-filtering}

[binlogイベントフィルタリング](/dm/dm-key-features.md#binlog-event-filter)つの機能は、DMがソースデータベース内の特定のテーブルから特定のタイプのSQLステートメントをフィルタリングできることを意味します。たとえば、表`test`の`INSERT`のステートメントすべてをフィルタリングできます。 `sbtest`または、スキーマ`test`の`TRUNCATE TABLE`のステートメントすべてをフィルタリングします。

### スキーマとテーブルのルーティング {#schema-and-table-routing}

[スキーマとテーブルのルーティング](/dm/dm-key-features.md#table-routing)の機能は、DMがソースデータベースの特定のテーブルをダウンストリームの指定されたテーブルに移行できることを意味します。たとえば、テーブル構造とデータをテーブル`test`から移行できます。ソースデータベースの`sbtest1`を表`test`に追加します。 TiDBでは`sbtest2` 。これは、シャーディングされたデータベースとテーブルをマージおよび移行するためのコア機能でもあります。

## 高度な機能 {#advanced-features}

### シャードのマージと移行 {#shard-merge-and-migration}

DMは、元のシャーディングされたインスタンスとテーブルをソースデータベースからTiDBにマージおよび移行することをサポートしていますが、いくつかの制限があります。詳細については、 [ペシミスティックモードでのDDL使用制限のシャーディング](/dm/feature-shard-merge-pessimistic.md#restrictions)および[楽観的モードでのDDL使用制限のシャーディング](/dm/feature-shard-merge-optimistic.md#restrictions)を参照してください。

### 移行プロセスにおけるサードパーティのオンラインスキーマ変更ツールの最適化 {#optimization-for-third-party-online-schema-change-tools-in-the-migration-process}

MySQLエコシステムでは、gh-ostやpt-oscなどのツールが広く使用されています。 DMは、これらのツールをサポートして、不要な中間データの移行を回避します。詳しくは[オンラインDDLツール](/dm/dm-key-features.md#online-ddl-tools)をご覧ください

### SQL式を使用して特定の行の変更をフィルタリングする {#filter-certain-row-changes-using-sql-expressions}

インクリメンタルレプリケーションのフェーズでは、DMはSQL式の構成をサポートして、特定の行の変更を除外します。これにより、データをより詳細にレプリケートできます。詳細については、 [SQL式を使用して特定の行の変更をフィルタリングする](/dm/feature-expression-filter.md)を参照してください。

## 使用制限 {#usage-restrictions}

DMツールを使用する前に、次の制限に注意してください。

-   データベースのバージョン要件

    -   MySQLバージョン&gt;5.5

    -   MariaDBバージョン&gt;=10.1.2

    > **ノート：**
    >
    > アップストリームのMySQL/MariaDBサーバー間にプライマリ-セカンダリ移行構造がある場合は、次のバージョンを選択します。
    >
    > -   MySQLバージョン&gt;5.7.1
    > -   MariaDBバージョン&gt;=10.1.3

    > **警告：**
    >
    > DMを使用してMySQL8.0からTiDBにデータを移行することは、実験的機能です（DM v2.0以降に導入されました）。実稼働環境で使用することはお勧めし**ません**。

-   DDL構文の互換性

    -   現在、TiDBはMySQLがサポートするすべてのDDLステートメントと互換性があるわけではありません。 DMはTiDBパーサーを使用してDDLステートメントを処理するため、TiDBパーサーでサポートされているDDL構文のみをサポートします。詳細については、 [MySQLの互換性](/mysql-compatibility.md#ddl)を参照してください。

    -   DMは、互換性のないDDLステートメントを検出すると、エラーを報告します。このエラーを解決するには、このDDLステートメントをスキップするか、指定されたDDLステートメントに置き換えることにより、dmctlを使用して手動で処理する必要があります。詳細については、 [異常なSQLステートメントをスキップまたは置換します](/dm/dm-faq.md#how-to-handle-incompatible-ddl-statements)を参照してください。

-   シャーディングは競合とマージします

    -   シャーディングされたテーブル間に競合が存在する場合は、 [自動インクリメント主キーの競合の処理](/dm/shard-merge-best-practices.md#handle-conflicts-of-auto-increment-primary-key)を参照して競合を解決します。それ以外の場合、データ移行はサポートされていません。競合するデータは互いにカバーし合い、データの損失を引き起こす可能性があります。

    -   その他のシャーディングDDL移行の制限については、 [ペシミスティックモードでのDDL使用制限のシャーディング](/dm/feature-shard-merge-pessimistic.md#restrictions)および[楽観的モードでのDDL使用制限のシャーディング](/dm/feature-shard-merge-optimistic.md#restrictions)を参照してください。

-   データソースのMySQLインスタンスの切り替え

    DM-workerが仮想IP（VIP）を介してアップストリームMySQLインスタンスに接続する場合、VIP接続を別のMySQLインスタンスに切り替えると、DMは異なる接続で同時に新しいMySQLインスタンスと古いMySQLインスタンスに接続する可能性があります。この状況では、DMに移行されたbinlogは、DMが受け取る他のアップストリームステータスと一致しないため、予測できない異常やデータの損傷が発生します。 DMに必要な変更を手動で行うには、 [仮想IPを介したDM-worker接続の切り替え](/dm/usage-scenario-master-slave-switch.md#switch-dm-worker-connection-via-virtual-ip)を参照してください。

-   GBK文字セットの互換性

    -   DMは、v5.4.0より前のTiDBクラスターへの`charset=GBK`のテーブルの移行をサポートしていません。
