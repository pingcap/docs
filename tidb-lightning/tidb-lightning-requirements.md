---
title: TiDB Lightning Requirements for the Target Database
summary: Learn prerequisites for running TiDB Lightning.
---

# ターゲット データベースのTiDB Lightning要件 {#tidb-lightning-requirements-for-the-target-database}

TiDB Lightningを使用する前に、環境が要件を満たしているかどうかを確認する必要があります。これにより、インポート中のエラーを減らし、インポートを確実に成功させることができます。

## ターゲット データベースの権限 {#privileges-of-the-target-database}

インポート モードと有効な機能に基づいて、ターゲット データベース ユーザーに異なる権限を付与する必要があります。次の表に参考情報を示します。

<table><tr><td></td><td>特徴</td><td>範囲</td><td>必要な権限</td><td>備考</td></tr><tr><td rowspan="2">必須</td><td rowspan="2">基本関数</td><td>対象表</td><td>作成、選択、挿入、更新、削除、削除、変更</td><td>DROP は、tidb-lightning-ctl が checkpoint-destroy-all コマンドを実行する場合にのみ必要です。</td></tr><tr><td>対象データベース</td><td>作成</td><td></td></tr><tr><td rowspan="4">必須</td><td>論理インポート モード</td><td>information_schema.columns</td><td>選択する</td><td></td></tr><tr><td rowspan="3">物理インポート モード</td><td>mysql.tidb</td><td>選択する</td><td></td></tr><tr><td>-</td><td>素晴らしい</td><td></td></tr><tr><td>-</td><td> RESTRICTED_VARIABLES_ADMIN、RESTRICTED_TABLES_ADMIN</td><td>対象の TiDB で SEM が有効になっている場合に必要</td></tr><tr><td>おすすめされた</td><td>競合検出、最大エラー</td><td>lightning.task-info-schema-name 用に設定されたスキーマ</td><td>選択、挿入、更新、削除、作成、削除</td><td>必要ない場合は、値を &quot;&quot; に設定する必要があります。</td></tr><tr><td>オプション</td><td>並行輸入</td><td>lightning.meta-schema-name 用に構成されたスキーマ</td><td>選択、挿入、更新、削除、作成、削除</td><td>必要ない場合は、値を &quot;&quot; に設定する必要があります。</td></tr><tr><td>オプション</td><td>checkpoint.driver = &quot;mysql&quot;</td><td> checkpoint.schema 設定</td><td>選択、挿入、更新、削除、作成、削除</td><td>チェックポイント情報がファイルではなくデータベースに格納されている場合に必要</td></tr></table>

## ターゲット データベースのストレージ スペース {#storage-space-of-the-target-database}

ターゲットの TiKV クラスターには、インポートされたデータを保存するのに十分なディスク容量が必要です。 [標準のハードウェア要件](/hardware-and-software-requirements.md)に加えて、ターゲット TiKV クラスターのstorage容量は**、データ ソースのサイズ x レプリカの数 x 2**より大きくなければなりません。たとえば、クラスターがデフォルトで 3 つのレプリカを使用する場合、ターゲット TiKV クラスターには、データ ソースのサイズの 6 倍を超えるstorageスペースが必要です。次の理由により、式には x 2 があります。

-   インデックスは余分なスペースを必要とする場合があります。
-   RocksDB には空間増幅効果があります。

Dumplingによって MySQL からエクスポートされた正確なデータ量を計算することは困難です。ただし、次の SQL ステートメントを使用して information_schema.tables テーブルのデータ長フィールドを要約することにより、データ量を見積もることができます。

すべてのスキーマのサイズを MiB で計算します。 ${schema_name} をスキーマ名に置き換えます。

```sql
SELECT table_schema, SUM(data_length)/1024/1024 AS data_length, SUM(index_length)/1024/1024 AS index_length, SUM(data_length+index_length)/1024/1024 AS sum FROM information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_schema;
```

最大テーブルのサイズを MiB で計算します。 ${schema_name} をスキーマ名に置き換えます。

{{< copyable "" >}}

```sql
SELECT table_name, table_schema, SUM(data_length)/1024/1024 AS data_length, SUM(index_length)/1024/1024 AS index_length,sum(data_length+index_length)/1024/1024 AS sum FROM information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_name,table_schema ORDER BY sum DESC LIMIT 5;
```
