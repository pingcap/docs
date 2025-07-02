---
title: Compatibility of TiDB Lightning and IMPORT INTO with TiCDC and Log Backup
summary: IMPORT INTO およびTiDB Lightning とログ バックアップおよび TiCDC との互換性について説明します。
---

# TiDB Lightningと IMPORT INTO と TiCDC およびログバックアップとの互換性 {#compatibility-of-tidb-lightning-and-import-into-with-ticdc-and-log-backup}

このドキュメントでは、 TiDB Lightningおよび[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)と[ログバックアップ](/br/br-pitr-guide.md)および[TiCDC](/ticdc/ticdc-overview.md)の互換性、およびいくつかの特殊な使用シナリオについて説明します。

## <code>IMPORT INTO</code>とTiDB Lightning の比較 {#code-import-into-code-vs-tidb-lightning}

[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) TiDB Lightningの物理インポートモードと統合されていますが、いくつかの違いがあります。詳細は[`IMPORT INTO`とTiDB Lightning の比較](/tidb-lightning/import-into-vs-tidb-lightning.md)ご覧ください。

## ログバックアップおよびTiCDCとの互換性 {#compatibility-with-log-backup-and-ticdc}

-   TiDB Lightning [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md) 、ログ バックアップおよび TiCDC と互換性があります。

-   TiDB Lightning [物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md) 、ログバックアップおよびTiCDCと互換性がありません。これは、物理インポートモードがソースデータのエンコードされたKVペアをTiKVに直接取り込むため、TiKVがこの処理中に該当する変更ログを生成できないためです。変更ログが生成されないと、ログバックアップによる関連データのバックアップやTiCDCによるレプリケーションが実行できません。

-   クラスター内でTiDB Lightningと TiCDC を一緒に使用するには、 [TiDB Lightningとの互換性](/ticdc/ticdc-compatibility.md#compatibility-with-tidb-lightning)参照してください。

-   `IMPORT INTO`はログバックアップおよびTiCDCと互換性がありません。これは、 `IMPORT INTO`ではソースデータのエンコードされたKVペアもTiKVに直接取り込まれるためです。

## TiDB Lightning論理インポートモードのシナリオ {#scenarios-for-tidb-lightning-logical-import-mode}

TiDB Lightning論理インポート モードがアプリケーションのパフォーマンス要件を満たすことができ、アプリケーションでインポートされたテーブルを TiCDC を使用してダウンストリームにバックアップまたは複製する必要がある場合は、 TiDB Lightning論理インポート モードを使用することをお勧めします。

## TiDB Lightning物理インポートモードのシナリオ {#scenarios-for-tidb-lightning-physical-import-mode}

このセクションでは、TiDB Lightning を[ログバックアップ](/br/br-pitr-guide.md)および[TiCDC](/ticdc/ticdc-overview.md)と一緒に使用する方法について説明します。

TiDB Lightning論理インポート モードがアプリケーションのパフォーマンス要件を満たしていない場合、 TiDB Lightning物理インポート モードを使用する必要があり、インポートされたテーブルを TiCDC を使用してダウンストリームにバックアップまたは複製する必要がある場合は、次のシナリオが推奨されます。

### ログバックアップで使用される {#used-with-log-backup}

このシナリオでは、 [PITR](/br/br-log-architecture.md#process-of-pitr)有効になっている場合、 TiDB Lightning の起動後に互換性チェックでエラーが報告されます。これらのテーブルのバックアップが不要であることが確実な場合は、 [TiDB Lightning構成ファイル](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)の`Lightning.check-requirements`パラメータを`false`に変更してインポートタスクを再開できます。

TiDB Lightning物理インポートモードでインポートされたデータは、ログバックアップではバックアップできません。テーブルをバックアップする必要がある場合は、 [テーブルをバックアップする](/br/br-snapshot-manual.md#back-up-a-table)で説明されているように、インポート後にテーブルレベルのスナップショットバックアップを実行することをお勧めします。

### TiCDC で使用される {#used-with-ticdc}

TiCDC を物理インポート モードで使用することは、短期的には互換性がありません。これは、TiCDC がTiDB Lightning物理インポート モードの書き込み速度に追いつけず、クラスター レプリケーションのレイテンシーが長くなる可能性があるためです。

次のようにさまざまなシナリオで実行できます。

-   シナリオ 1: テーブルを TiCDC によってダウンストリームに複製する必要はありません。

    このシナリオでは、TiCDC の changefeed が有効になっている場合、 TiDB Lightning の起動後に互換性チェックでエラーが報告されます。これらのテーブルにバックアップや[ログバックアップ](/br/br-pitr-guide.md)必要ないことが確実な場合は、 [TiDB Lightning構成ファイル](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)の`Lightning.check-requirements`パラメータを`false`に変更してインポートタスクを再開できます。

-   シナリオ 2: テーブルを TiCDC によってダウンストリームに複製する必要があります。

    このシナリオでは、TiCDC の changefeed が有効になっている場合、 TiDB Lightning の起動後に互換性チェックでエラーが報告されます。上流 TiDB クラスターの[TiDB Lightning構成ファイル](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)パラメータ`Lightning.check-requirements`を`false`に変更し、インポートタスクを再起動する必要があります。

    上流TiDBクラスタのインポートタスクが完了したら、 TiDB Lightningを使用して、同じデータを下流TiDBクラスタにインポートします。下流にRedshiftやSnowflakeなどのデータベースがある場合は、クラウドstorageサービスからCSV、SQL、またはParquetファイルを読み取り、データベースに書き込むように設定できます。

## <code>IMPORT INTO</code>のシナリオ {#scenarios-for-code-import-into-code}

このセクションでは、 `IMPORT INTO` [ログバックアップ](/br/br-pitr-guide.md)および[TiCDC](/ticdc/ticdc-overview.md)と一緒に使用する方法について説明します。

### ログバックアップで使用される {#used-with-log-backup}

このシナリオでは、 [PITR](/br/br-log-architecture.md#process-of-pitr)有効になっている場合、 `IMPORT INTO`文を送信した後に互換性チェックでエラーが報告されます。これらのテーブルにバックアップが必要ないことが確実な場合は、その文の[`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions)に`DISABLE_PRECHECK` （バージョン 8.0.0 で導入）を含めて再送信してください。これにより、データインポートタスクは互換性チェックを無視し、データを直接インポートします。

`IMPORT INTO`でインポートしたデータは、ログバックアップではバックアップできません。テーブルをバックアップする必要がある場合は、 [テーブルをバックアップする](/br/br-snapshot-manual.md#back-up-a-table)で説明されているように、インポート後にテーブルレベルのスナップショットバックアップを実行できます。

### TiCDC で使用される {#used-with-ticdc}

次のようにさまざまなシナリオで実行できます。

-   シナリオ 1: テーブルを TiCDC によってダウンストリームに複製する必要はありません。

    このシナリオでは、TiCDC の changefeed が有効になっている場合、 `IMPORT INTO`ステートメントを送信した後に互換性チェックでエラーが報告されます。これらのテーブルを TiCDC で複製する必要がないことが確実な場合は、そのステートメントの[`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions)に`DISABLE_PRECHECK` (v8.0.0 で導入) を含めて再送信できます。これにより、データインポートタスクは互換性チェックを無視し、データを直接インポートします。

-   シナリオ 2: テーブルを TiCDC によってダウンストリームに複製する必要があります。

    このシナリオでは、TiCDC の changefeed が有効になっている場合、 `IMPORT INTO`ステートメントを送信した後に互換性チェックでエラーが報告されます。そのステートメントの[`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions)に`DISABLE_PRECHECK` (v8.0.0 で導入) を含めて再送信することができます。これにより、データインポートタスクは互換性チェックを無視し、データを直接インポートします。

    上流 TiDB クラスターのインポートタスクが完了したら、 `IMPORT INTO`使用して下流 TiDB クラスターに同じデータをインポートします。下流に Redshift や Snowflake などのデータベースがある場合は、クラウドstorageサービスから CSV、SQL、または Parquet ファイルを読み取り、データベースに書き込むように設定できます。
