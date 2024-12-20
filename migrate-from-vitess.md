---
title: Migrate Data from Vitess to TiDB
summary: Vitess から TiDB にデータを移行するためのツールについて学習します。
---

# Vitess から TiDB へのデータの移行 {#migrate-data-from-vitess-to-tidb}

このドキュメントでは、 [ヴィテス](https://vitess.io/)から TiDB にデータを移行するために使用できるツールについて説明します。

Vitess のバックエンドは MySQL に基づいているため、Vitess から TiDB にデータを移行する場合、 [Dumpling](/dumpling-overview.md) 、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 、 [TiDB データ移行 (DM)](/dm/dm-overview.md)など、MySQL に適用されるのと同じ移行ツールを使用できます。これらのツールは、データ移行のために Vitess 内の各シャードに対して設定する必要があることに注意してください。

通常、データ移行の前に、 DM タスクを`task-mode` ～ `all`および`import-mode` ～ `physical`に設定することが推奨されます。詳細については、 [タスク構成ファイル テンプレート (詳細)](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)参照してください。

データ サイズが 10 TiB を超える場合は、次の 2 つの手順でインポートを実行することをお勧めします。

1.  既存のデータをインポートするには、 DumplingとTiDB Lightning を使用します。
2.  増分データをインポートするには DM を使用します。

これらのツールに加えて、 [Vitess 用 Debezium コネクタ](https://debezium.io/documentation/reference/connectors/vitess.html)も使用できます。このコネクタを使用すると、 [カフカコネクト](https://kafka.apache.org/documentation/#connect)または[アパッチフリンク](https://nightlies.apache.org/flink/flink-docs-stable/)使用して、Vitess から TiDB に変更をストリーミングできます。

Vitess と TiDB はどちらも MySQL プロトコルと SQL 方言をサポートしているため、アプリケーション レベルでの変更は小さいと予想されます。ただし、シャーディングやその他の実装固有の側面を直接管理するタスクの場合、変更は大きくなる可能性があります。Vitess から TiDB へのデータ移行を容易にするために、TiDB は[`VITESS_HASH()`](/functions-and-operators/tidb-functions.md)関数を導入しています。この関数は、Vitess の HASH 関数と互換性のある文字列のハッシュを返します。

## 例 {#examples}

### DumplingとTiDB Lightning {#dumpling-and-tidb-lightning}

次の 2 つの例は、 DumplingとTiDB Lightning が連携して Vitess から TiDB にデータを移行する方法を示しています。

-   この例では、 TiDB Lightning は[論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)使用します。これは、最初にデータを SQL ステートメントにエンコードし、次に SQL ステートメントを実行してデータをインポートします。

    ![Vitess to TiDB Migration with TiDB backend](/media/vitess_to_tidb.png)

-   この例では、 TiDB Lightning は[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)使用してデータを TiKV に直接取り込みます。

    ![Vitess to TiDB Migration with local backend](/media/vitess_to_tidb_dumpling_local.png)

### DM {#dm}

次の例は、Vitess から TiDB にデータを移行する[DM](/dm/dm-overview.md)を示しています。

![Vitess to TiDB with DM](/media/vitess_to_tidb_dm.png)
