---
title: TiDB Lightning Import Mode
summary: Learn how to choose different import modes of TiDB Lightning.
---

# TiDBLightningインポートモード {#tidb-lightning-import-modes}

TiDB Lightningは、2つの[バックエンド](/tidb-lightning/tidb-lightning-glossary.md#back-end)で2つのインポートモードをサポートします。バックエンドは、TiDBLightningがデータをターゲットクラスタにインポートする方法を決定します。

-   **ローカルバックエンド**：TiDB Lightningは、最初にデータをキーと値のペアにエンコードし、並べ替えてローカルの一時ディレクトリに保存し、これらのキーと値のペアを各TiKVノードに*アップロード*します。次に、TiDB LightningはTiKV取り込みインターフェイスを呼び出して、TiKVのRocksDBにデータを書き込みます。初期化されたデータのインポートについては、インポート速度が速いため、ローカルバックエンドを検討してください。

-   **TiDBバックエンド**：TiDB Lightningは、最初にデータをSQLステートメントにエンコードし、次にこれらのステートメントを実行してデータをインポートします。ターゲットクラスタが実稼働環境にある場合、またはターゲットテーブルにすでにデータがある場合は、TiDBバックエンドを検討してください。

| バックエンド                  | ローカルバックエンド    | TiDB-バックエンド     |
| :---------------------- | :------------ | :-------------- |
| スピード                    | 高速（〜500GB /時） | 遅い（〜50 GB / hr） |
| リソースの使用                 | 高い            | 低い              |
| ネットワーク帯域幅の使用            | 高い            | 低い              |
| インポート中のACIDコンプライアンス     | いいえ           | はい              |
| ターゲットテーブル               | 空である必要があります   | 移入可能            |
| サポートされているTiDBバージョン      | = v4.0.0      | 全て              |
| TiDBはインポート中にサービスを提供できます | いいえ           | はい              |

> **注**：
>
> -   ローカルバックエンドモードで本番環境のTiDBクラスタにデータをインポートしないでください。これは、オンラインアプリケーションに深刻な影響を及ぼします。
> -   デフォルトでは、複数のTiDB Lightningインスタンスを起動して、同じTiDBクラスタにデータをインポートすることはできません。代わりに、 [並列インポート](/tidb-lightning/tidb-lightning-distributed-import.md)つの機能を使用する必要があります。
> -   複数のTiDBLightningインスタンスを使用して同じターゲットデータベースにデータをインポートする場合は、複数のバックエンドを使用しないでください。たとえば、ローカルバックエンドとTiDBバックエンドの両方を使用してデータをTiDBクラスタにインポートしないでください。

## ローカルバックエンド {#local-backend}

TiDB Lightningでは、TiDBv4.0.3にローカルバックエンドが導入されています。ローカルバックエンドを使用すると、データをTiDBクラスター&gt;=v4.0.0にインポートできます。

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

`duplicate-resolution`つの構成は、競合する可能性のあるデータを解決するための3つの戦略を提供します。

-   `none` （デフォルト）：重複レコードを検出しません。これは、3つの戦略で最高のパフォーマンスを発揮しますが、ターゲットTiDBのデータに一貫性がなくなる可能性があります。
-   `record` ：競合するレコードのみをターゲットTiDBの`lightning_task_info.conflict_error_v1`テーブルに記録します。ターゲットTiKVの必要なバージョンはv5.2.0より前ではないことに注意してください。それ以外の場合は、「none」にフォールバックします。
-   `remove` ：「レコード」戦略のように、競合するすべてのレコードを記録します。ただし、ターゲットテーブルから競合するすべてのレコードを削除して、ターゲットTiDBで一貫した状態を確保します。

データソースに競合するデータがあるかどうかわからない場合は、 `remove`の戦略をお勧めします。 `none`と`record`の戦略では、競合するデータがターゲットテーブルから削除されません。つまり、TiDBLightningによって生成された一意のインデックスがデータと矛盾している可能性があります。

## TiDB-バックエンド {#tidb-backend}

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

TiDBバックエンドは、すでに入力されている（空でない）テーブルへのインポートをサポートします。ただし、新しいデータにより、古いデータとの一意のキーの競合が発生する可能性があります。 `on-duplicate`の構成を使用して、競合を解決する方法を制御できます。

| 価値        | 競合時のデフォルトの動作          | SQLステートメント               |
| :-------- | :-------------------- | :----------------------- |
| `replace` | 新しいレコードが古いレコードを置き換えます | `REPLACE INTO ...`       |
| `ignore`  | 古い記録を保持し、新しい記録を無視します  | `INSERT IGNORE INTO ...` |
| `error`   | インポートを中止する            | `INSERT INTO ...`        |

## も参照してください {#see-also}

-   [データを並行してインポートする](/tidb-lightning/tidb-lightning-distributed-import.md)
