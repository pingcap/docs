---
title: TiDB Lightning Requirements for the Target Database
summary: TiDB Lightning を実行するための前提条件について説明します。
---

# ターゲットデータベースのTiDB Lightning要件 {#tidb-lightning-requirements-for-the-target-database}

TiDB Lightningを使用する前に、環境が要件を満たしているかどうかを確認する必要があります。これにより、インポート時のエラーが軽減され、インポートが確実に成功します。

## ターゲットデータベースの権限 {#privileges-of-the-target-database}

インポートモードと有効な機能に基づいて、ターゲットデータベースユーザーには異なる権限を付与する必要があります。次の表にその例を示します。

<table><tr><td></td><td>特徴</td><td>範囲</td><td>必要な権限</td><td>備考</td></tr><tr><td rowspan="2">必須</td><td rowspan="2">基本関数</td><td>ターゲットテーブル</td><td>作成、選択、挿入、更新、削除、ドロップ、変更</td><td>DROP は、tidb-lightning-ctl が checkpoint-destroy-all コマンドを実行する場合にのみ必要です。</td></tr><tr><td>ターゲットデータベース</td><td>作成する</td><td></td></tr><tr><td rowspan="4">必須</td><td>論理インポートモード</td><td>情報スキーマ列</td><td>選択</td><td></td></tr><tr><td rowspan="3">物理インポートモード</td><td>mysql.tidb</td><td>選択</td><td></td></tr><tr><td>-</td><td>素晴らしい</td><td></td></tr><tr><td>-</td><td>制限付き変数管理者、制限付きテーブル管理者</td><td>ターゲットTiDBがSEMを有効にする場合に必要</td></tr><tr><td>推奨</td><td>競合検出、最大エラー</td><td>lightning.task-info-schema-name 用に設定されたスキーマ</td><td>選択、挿入、更新、削除、作成、削除</td><td>必要でない場合は、値を &quot;&quot; に設定する必要があります</td></tr><tr><td>オプション</td><td>並行輸入</td><td>lightning.meta-schema-name 用に設定されたスキーマ</td><td>選択、挿入、更新、削除、作成、削除</td><td>必要でない場合は、値を &quot;&quot; に設定する必要があります</td></tr><tr><td>オプション</td><td>チェックポイント.ドライバー = &quot;mysql&quot;</td><td> checkpoint.schema 設定</td><td>選択、挿入、更新、削除、作成、削除</td><td>チェックポイント情報がファイルではなくデータベースに保存される場合に必要</td></tr></table>

## 対象データベースのストレージスペース {#storage-space-of-the-target-database}

ターゲットTiKVクラスターには、インポートしたデータを保存するための十分なディスク容量が必要です。1 に加え[標準的なハードウェア要件](/hardware-and-software-requirements.md) 、ターゲットTiKVクラスターのstorage容量**は、データソースのサイズ × レプリカ数 × 2**よりも大きくなければなりません。例えば、クラスターがデフォルトで3つのレプリカを使用する場合、ターゲットTiKVクラスターにはデータソースのサイズの6倍よりも大きなstorage容量が必要です。式に x 2 が含まれているのは、以下の理由によるものです。

-   インデックスは余分なスペースを占める可能性があります。
-   RocksDB には空間増幅効果があります。

DumplingがMySQLからエクスポートするデータ量を正確に計算することは困難です。ただし、次のSQL文を使用してinformation_schema.tablesテーブルの`DATA_LENGTH`フィールドを集計することで、データ量を概算できます。

```sql
-- Calculate the size of all schemas
SELECT
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(DATA_LENGTH)) AS 'Data Size',
  FORMAT_BYTES(SUM(INDEX_LENGTH)) 'Index Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_SCHEMA;

-- Calculate the 5 largest tables
SELECT 
  TABLE_NAME,
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(data_length)) AS 'Data Size',
  FORMAT_BYTES(SUM(index_length)) AS 'Index Size',
  FORMAT_BYTES(SUM(data_length+index_length)) AS 'Total Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_NAME,
  TABLE_SCHEMA
ORDER BY
  SUM(DATA_LENGTH+INDEX_LENGTH) DESC
LIMIT
  5;
```
