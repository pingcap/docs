---
title: Migrate Data from Vitess to TiDB
summary: Vitess から TiDB にデータを移行するためのツールについて学習します。
---

# Vitess から TiDB へのデータ移行 {#migrate-data-from-vitess-to-tidb}

このドキュメントでは、 [ヴィテス](https://vitess.io/)から TiDB にデータを移行するために使用できるツールについて説明します。

VitessのバックエンドはMySQLベースであるため、VitessからTiDBにデータを移行する際には、MySQLに適用できるものと同じ移行ツール[TiDB データ移行 (DM)](/dm/dm-overview.md) [Dumpling](/dumpling-overview.md)など[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用できます。これらのツールは、データ移行のためにVitess内の各シャードに対して設定する必要があることに注意してください。

通常、データ移行前にDMタスクを`task-mode` ～ `all` ～ `physical`に設定することを推奨します。詳細については、 [タスク構成ファイルテンプレート（上級）](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) `import-mode`してください。

データ サイズが 10 TiB を超える場合は、2 つの手順でインポートを実行することをお勧めします。

1.  既存のデータをインポートするには、 DumplingとTiDB Lightning を使用します。
2.  DM を使用して増分データをインポートします。

これらのツールに加えて、 [Vitess用Debeziumコネクタ](https://debezium.io/documentation/reference/connectors/vitess.html)も使用できます。このコネクタを使用すると、 [カフカコネクト](https://kafka.apache.org/documentation/#connect)または[アパッチフリンク](https://nightlies.apache.org/flink/flink-docs-stable/)使用して、Vitess から TiDB に変更をストリーミングできます。

VitessとTiDBはどちらもMySQLプロトコルとSQL方言をサポートしているため、アプリケーションレベルでの変更は小さくなると予想されます。ただし、シャーディングやその他の実装固有の側面を直接管理するタスクでは、変更が大きくなる可能性があります。VitessからTiDBへのデータ移行を容易にするために、TiDBはVitessのHASH関数と互換性のある文字列のハッシュを返す[`VITESS_HASH()`](/functions-and-operators/tidb-functions.md)関数を導入しています。

## 例 {#examples}

### DumplingとTiDB Lightning {#dumpling-and-tidb-lightning}

次の 2 つの例は、 DumplingとTiDB Lightningが連携して Vitess から TiDB にデータを移行する方法を示しています。

-   この例では、 TiDB Lightning は[論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)使用します。これは、最初にデータを SQL ステートメントにエンコードし、次に SQL ステートメントを実行してデータをインポートします。

    ![Vitess to TiDB Migration with TiDB backend](/media/vitess_to_tidb.png)

-   この例では、 TiDB Lightning は[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)を使用してデータを TiKV に直接取り込みます。

    ![Vitess to TiDB Migration with local backend](/media/vitess_to_tidb_dumpling_local.png)

### DM {#dm}

次の例は、Vitess から TiDB にデータを移行する[DM](/dm/dm-overview.md)を示しています。

![Vitess to TiDB with DM](/media/vitess_to_tidb_dm.png)
