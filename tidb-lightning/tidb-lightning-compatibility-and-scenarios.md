---
title: Compatibility of TiDB Lightning and IMPORT INTO with TiCDC and Log Backup
summary: IMPORT INTO およびTiDB Lightning とログ バックアップおよび TiCDC との互換性について説明します。
---

# TiDB Lightningと IMPORT INTO と TiCDC およびログ バックアップとの互換性 {#compatibility-of-tidb-lightning-and-import-into-with-ticdc-and-log-backup}

このドキュメントでは、 TiDB Lightningおよび[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)と[ログバックアップ](/br/br-pitr-guide.md)および[ティCDC](/ticdc/ticdc-overview.md)との互換性、およびいくつかの特殊な使用シナリオについて説明します。

## <code>IMPORT INTO</code>とTiDB Lightningの比較 {#code-import-into-code-vs-tidb-lightning}

[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) TiDB Lightningの物理インポートモードと統合されますが、いくつか違いがあります。詳細については[`IMPORT INTO`とTiDB Lightningの比較](/tidb-lightning/import-into-vs-tidb-lightning.md)参照してください。

## ログバックアップおよびTiCDCとの互換性 {#compatibility-with-log-backup-and-ticdc}

-   TiDB Lightning [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md) 、ログ バックアップおよび TiCDC と互換性があります。

-   TiDB Lightning [物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md) 、ログ バックアップおよび TiCDC と互換性がありません。その理由は、物理インポート モードでは、ソース データのエンコードされた KV ペアが TiKV に直接取り込まれるため、このプロセス中に TiKV が対応する変更ログを生成しないからです。このような変更ログがないと、関連データをログ バックアップでバックアップできず、TiCDC でレプリケートできません。

-   クラスター内でTiDB Lightningと TiCDC を一緒に使用するには、 [TiDB Lightningとの互換性](/ticdc/ticdc-compatibility.md#compatibility-with-tidb-lightning)参照してください。

-   `IMPORT INTO`ログ バックアップおよび TiCDC と互換性がありません。その理由は、 `IMPORT INTO`ではソース データのエンコードされた KV ペアも TiKV に直接取り込まれるためです。

## TiDB Lightning論理インポート モードのシナリオ {#scenarios-for-tidb-lightning-logical-import-mode}

TiDB Lightning論理インポート モードがアプリケーションのパフォーマンス要件を満たすことができ、アプリケーションでインポートされたテーブルを TiCDC を使用してダウンストリームにバックアップまたは複製する必要がある場合は、 TiDB Lightning論理インポート モードを使用することをお勧めします。

## TiDB Lightning物理インポート モードのシナリオ {#scenarios-for-tidb-lightning-physical-import-mode}

このセクションでは、 TiDB Lightning を[ログバックアップ](/br/br-pitr-guide.md)および[ティCDC](/ticdc/ticdc-overview.md)と一緒に使用する方法について説明します。

TiDB Lightning論理インポート モードがアプリケーションのパフォーマンス要件を満たさず、 TiDB Lightning物理インポート モードを使用する必要があり、インポートされたテーブルを TiCDC を使用してダウンストリームにバックアップまたは複製する必要がある場合は、次のシナリオが推奨されます。

### ログバックアップで使用される {#used-with-log-backup}

次のようにさまざまなシナリオで実行できます。

-   シナリオ1: 物理インポートモードのテーブルはバックアップする必要がない

    このシナリオでは、 [ピトル](/br/br-log-architecture.md#process-of-pitr)有効になっている場合、 TiDB Lightning の起動後に互換性チェックでエラーが報告されます。これらのテーブルにバックアップや[ログバックアップ](/br/br-pitr-guide.md)必要ないことが確実な場合は、 [TiDB Lightning構成ファイル](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)の`Lightning.check-requirements`パラメータを`false`に変更して、インポート タスクを再開できます。

-   シナリオ2: 物理インポートが完了した後、テーブルに対して新しいDML操作は行われません。

    このシナリオでは増分データ書き込みは行われないため、 [テーブルをバックアップする](/br/br-snapshot-manual.md#back-up-a-table)で説明したように、 TiDB Lightning物理インポート モードでデータのインポートを完了した後、テーブルのテーブル レベルのスナップショット バックアップを実行するだけで十分です。

    データ復旧では、テーブルのスナップショットデータが復元されます。手順については[テーブルを復元する](/br/br-snapshot-manual.md#restore-a-table)参照してください。

-   シナリオ 3: 物理インポートが完了した後、テーブルに対して新しい DML 操作が実行されます (サポートされていません)

    このシナリオでは、このテーブルに対して[完全なスナップショットバックアップ](/br/br-snapshot-guide.md)または[ログバックアップ](/br/br-pitr-guide.md)いずれかのみを選択できます。このテーブルの完全なスナップショット データとログ バックアップ データの両方をバックアップおよび復元することはできません。

### TiCDC で使用 {#used-with-ticdc}

TiCDC を物理インポート モードで使用することは、短期的には互換性がありません。これは、TiCDC がTiDB Lightning物理インポート モードの書き込み速度に追いつけず、クラスター レプリケーションのレイテンシーが増加する可能性があるためです。

次のようにさまざまなシナリオで実行できます。

-   シナリオ 1: テーブルを TiCDC によってダウンストリームに複製する必要はありません。

    このシナリオでは、TiCDC changefeed が有効になっている場合、 TiDB Lightning の起動後に互換性チェックでエラーが報告されます。これらのテーブルにバックアップや[ログバックアップ](/br/br-pitr-guide.md)必要ないことが確実な場合は、 [TiDB Lightning構成ファイル](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)の`Lightning.check-requirements`パラメータを`false`に変更して、インポート タスクを再開できます。

-   シナリオ 2: テーブルを TiCDC によってダウンストリームに複製する必要があります。

    このシナリオでは、TiCDC changefeed が有効になっている場合、 TiDB Lightning の起動後に互換性チェックでエラーが報告されます。アップストリーム TiDB クラスターの[TiDB Lightning構成ファイル](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)の`Lightning.check-requirements`パラメータを`false`に変更し、インポート タスクを再起動する必要があります。

    アップストリーム TiDB クラスターのインポート タスクが完了したら、 TiDB Lightning を使用してダウンストリーム TiDB クラスターに同じデータをインポートします。ダウンストリームに Redshift や Snowflake などのデータベースがある場合は、クラウドstorageサービスから CSV、SQL、または Parquet ファイルを読み取り、そのデータをデータベースに書き込むように構成できます。

## <code>IMPORT INTO</code>のシナリオ {#scenarios-for-code-import-into-code}

このセクションでは、 `IMPORT INTO` [ログバックアップ](/br/br-pitr-guide.md)および[ティCDC](/ticdc/ticdc-overview.md)と一緒に使用する方法について説明します。

### ログバックアップで使用される {#used-with-log-backup}

次のようにさまざまなシナリオで実行できます。

-   シナリオ 1: テーブルをバックアップする必要がない

    このシナリオでは、 [ピトル](/br/br-log-architecture.md#process-of-pitr)が有効になっている場合、 `IMPORT INTO`ステートメントを送信した後に互換性チェックでエラーが報告されます。これらのテーブルにバックアップや[ログバックアップ](/br/br-pitr-guide.md)必要ないことが確実な場合は、そのステートメントの[`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions)に`DISABLE_PRECHECK` (v8.0.0 で導入) を含めて、再送信することができます。このようにして、データ インポート タスクは互換性チェックを無視し、データを直接インポートします。

-   シナリオ2: インポートが完了した後、テーブルに対して新しいDML操作は行われません。

    このシナリオでは増分データ書き込みは行われないため、 [テーブルをバックアップする](/br/br-snapshot-manual.md#back-up-a-table)で説明したように、データのインポートが完了したら、テーブルのテーブルレベルのスナップショット バックアップを実行するだけで十分です。

    データ復旧では、テーブルのスナップショットデータが復元されます。手順については[テーブルを復元する](/br/br-snapshot-manual.md#restore-a-table)参照してください。

-   シナリオ 3: インポートが完了した後、テーブルに対して新しい DML 操作が実行されます (サポートされていません)

    このシナリオでは、このテーブルに対して[完全なスナップショットバックアップ](/br/br-snapshot-guide.md)または[ログバックアップ](/br/br-pitr-guide.md)いずれかのみを選択できます。このテーブルの完全なスナップショット データとログ バックアップ データの両方をバックアップおよび復元することはできません。

### TiCDC で使用 {#used-with-ticdc}

次のようにさまざまなシナリオで実行できます。

-   シナリオ 1: テーブルを TiCDC によってダウンストリームに複製する必要はありません。

    このシナリオでは、TiCDC の変更フィードが有効になっている場合、 `IMPORT INTO`ステートメントを送信した後に互換性チェックでエラーが報告されます。これらのテーブルを TiCDC で複製する必要がないことが確実な場合は、そのステートメントの[`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions)に`DISABLE_PRECHECK` (v8.0.0 で導入) を含めて、再送信することができます。このように、データ インポート タスクは互換性チェックを無視し、データを直接インポートします。

-   シナリオ 2: テーブルを TiCDC によってダウンストリームに複製する必要があります。

    このシナリオでは、TiCDC の変更フィードが有効になっている場合、 `IMPORT INTO`ステートメントを送信した後に互換性チェックでエラーが報告されます。そのステートメントの[`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions)に`DISABLE_PRECHECK` (v8.0.0 で導入) を含めて、再送信することができます。このように、データ インポート タスクは互換性チェックを無視し、データを直接インポートします。

    アップストリーム TiDB クラスターのインポート タスクが完了したら、 `IMPORT INTO`使用してダウンストリーム TiDB クラスターに同じデータをインポートします。ダウンストリームに Redshift や Snowflake などのデータベースがある場合は、クラウドstorageサービスから CSV、SQL、または Parquet ファイルを読み取り、そのデータをデータベースに書き込むように構成できます。
