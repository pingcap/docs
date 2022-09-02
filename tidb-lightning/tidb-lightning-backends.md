---
title: TiDB Lightning Import Modes
summary: Learn how to choose different import modes of TiDB Lightning.
---

# TiDB Lightningインポート モード {#tidb-lightning-import-modes}

TiDB Lightningは、2 つの[バックエンド](/tidb-lightning/tidb-lightning-glossary.md#back-end)で 2 つのインポート モードをサポートします。バックエンドは、 TiDB Lightningがターゲット クラスタにデータをインポートする方法を決定します。

-   **Local-backend** : TiDB Lightningは、最初にデータをキーと値のペアにエンコードし、並べ替えてローカルの一時ディレクトリに保存し、これらのキーと値のペアを各 TiKV ノードに*アップロード*します。次に、 TiDB Lightningは TiKV 取り込みインターフェイスを呼び出して、データを TiKV の RocksDB に書き込みます。初期化されたデータのインポートについては、インポート速度が速い local-backend を検討してください。

-   **TiDB バックエンド**: TiDB Lightningは、最初にデータを SQL ステートメントにエンコードし、次にこれらのステートメントを実行してデータをインポートします。ターゲット クラスターが実稼働環境にある場合、またはターゲット テーブルに既にデータがある場合は、TiDB バックエンドを検討してください。

| バックエンド                   | ローカル バックエンド    | TiDB バックエンド   |
| :----------------------- | :------------- | :------------ |
| スピード                     | 高速 (~500 GB/時) | 遅い (~50 GB/時) |
| リソース使用量                  | 高い             | 低い            |
| ネットワーク帯域幅の使用             | 高い             | 低い            |
| インポート中のACIDコンプライアンス      | いいえ            | はい            |
| 対象テーブル                   | 空である必要があります    | 移入可能          |
| サポートされている TiDB のバージョン    | = v4.0.0       | 全て            |
| TiDB はインポート中にサービスを提供できます | いいえ            | はい            |

> **注**:
>
> -   ローカル バックエンド モードで運用中の TiDB クラスターにデータをインポートしないでください。これは、オンライン アプリケーションに深刻な影響を与えます。
> -   デフォルトでは、複数のTiDB Lightningインスタンスを開始して、同じ TiDB クラスターにデータをインポートすることはできません。代わりに、 [並行輸入品](/tidb-lightning/tidb-lightning-distributed-import.md)機能を使用する必要があります。
> -   複数のTiDB Lightningインスタンスを使用して同じターゲット データベースにデータをインポートする場合は、複数のバックエンドを使用しないでください。たとえば、ローカル バックエンドと TiDB バックエンドの両方を使用して TiDB クラスターにデータをインポートしないでください。

## ローカル バックエンド {#local-backend}

TiDB Lightningは、TiDB v4.0.3 で local-backend を導入しています。 local-backend を使用することで、TiDB クラスター &gt;= v4.0.0 にデータをインポートできます。

### Configuration / コンフィグレーションと例 {#configuration-and-examples}

```toml
[Lightning]
# Specifies the database to store the execution results. If you do not want to create this schema, set this value to an empty string.
# task-info-schema-name = 'lightning_task_info'

[tikv-importer]
backend = "local"
# When the backend is 'local', whether to detect and resolve conflicting records (unique key conflict).
# The following three resolution strategies are supported:
#  - none: does not detect duplicate records, which has the best performance in the three
#    strategies, but might lead to inconsistent data in the target TiDB.
#  - record: only records conflicting records to the `lightning_task_info.conflict_error_v1`
#    table on the target TiDB. Note that the required version of the target TiKV is not
#    earlier than v5.2.0; otherwise, it falls back to 'none'.
#  - remove: records all conflicting records, like the 'record' strategy. But it removes all
#    conflicting records from the target table to ensure a consistent state in the target TiDB.
# duplicate-resolution = 'none'

# The directory of local KV sorting in the local-backend mode. SSD is recommended, and the
# directory should be set on a different disk from `data-source-dir` to improve import
# performance.
# The sorted-kv-dir directory should have free space greater than the size of the largest
# table in the upstream. If the space is insufficient, the import will fail.
sorted-kv-dir = ""
# The concurrency that TiKV writes KV data in the local-backend mode. When the network
# transmission speed between TiDB Lightning and TiKV exceeds 10 Gigabit, you can increase
# this value accordingly.
# range-concurrency = 16
# The number of KV pairs sent in one request in the local-backend mode.
# send-kv-pairs = 32768

[tidb]
# The target cluster information. The address of any tidb-server from the cluster.
host = "172.16.31.1"
port = 4000
user = "root"
# Configure the password to connect to TiDB. Either plaintext or Base64 encoded.
password = ""
# Required in the local-backend mode. Table schema information is fetched from TiDB via this status-port.
status-port = 10080
# Required in the local-backend mode. The address of any pd-server from the cluster.
pd-addr = "172.16.31.4:2379"
```

### 紛争解決 {#conflict-resolution}

`duplicate-resolution`構成では、競合する可能性のあるデータを解決するための 3 つの戦略が提供されます。

-   `none` (デフォルト): 重複レコードを検出しません。これは、3 つの戦略で最高のパフォーマンスを発揮しますが、ターゲット TiDB でデータの一貫性が失われる可能性があります。
-   `record` : 競合するレコードのみをターゲット TiDB の`lightning_task_info.conflict_error_v1`テーブルに記録します。ターゲット TiKV の必要なバージョンは v5.2.0 より前ではないことに注意してください。それ以外の場合は、&#39;none&#39; にフォールバックします。
-   `remove` : &#39;record&#39; 戦略のように、競合するすべてのレコードを記録します。ただし、競合するすべてのレコードをターゲット テーブルから削除して、ターゲット TiDB で一貫した状態を確保します。

データ ソースに競合するデータがあるかどうかわからない場合は、 `remove`の方法をお勧めします。 `none`および`record`の戦略では、ターゲット テーブルから競合するデータが削除されません。つまり、 TiDB Lightningによって生成された一意のインデックスがデータと矛盾する可能性があります。

## TiDB バックエンド {#tidb-backend}

### Configuration / コンフィグレーションと例 {#configuration-and-examples}

```toml
[tikv-importer]
# The backend mode. To use TiDB-backed, set it to "tidb".
backend = "tidb"

# Action to do when trying to insert a conflicting data.
# - replace: use new record to replace the existing record.
# - ignore: keep the existing record, and ignore the new record.
# - error: abort the import and report an error.
# on-duplicate = "replace"
```

### 紛争解決 {#conflict-resolution}

TiDB バックエンドは、既に入力されている (空でない) テーブルへのインポートをサポートしています。ただし、新しいデータは、古いデータとの一意キーの競合を引き起こす可能性があります。 `on-duplicate`構成を使用して競合を解決する方法を制御できます。

| 価値        | 競合時のデフォルトの動作         | SQL ステートメント              |
| :-------- | :------------------- | :----------------------- |
| `replace` | 新しいレコードが古いレコードに置き換わる | `REPLACE INTO ...`       |
| `ignore`  | 古い記録を保持し、新しい記録を無視する  | `INSERT IGNORE INTO ...` |
| `error`   | インポートを中止             | `INSERT INTO ...`        |

## こちらもご覧ください {#see-also}

-   [並行してデータをインポートする](/tidb-lightning/tidb-lightning-distributed-import.md)
