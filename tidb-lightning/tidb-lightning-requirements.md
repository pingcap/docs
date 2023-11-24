---
title: TiDB Lightning Requirements for the Target Database
summary: Learn prerequisites for running TiDB Lightning.
---

# ターゲット データベースのTiDB Lightning要件 {#tidb-lightning-requirements-for-the-target-database}

TiDB Lightningを使用する前に、環境が要件を満たしているかどうかを確認する必要があります。これにより、インポート中のエラーが軽減され、インポートが確実に成功します。

## ターゲットデータベースの権限 {#privileges-of-the-target-database}

インポート モードと有効な機能に基づいて、ターゲット データベース ユーザーに異なる権限を付与する必要があります。次の表は参考資料です。

<table><tr><td></td><td>特徴</td><td>範囲</td><td>必要な権限</td><td>備考</td></tr><tr><td rowspan="2">必須</td><td rowspan="2">基本関数</td><td>ターゲットテーブル</td><td>作成、選択、挿入、更新、削除、ドロップ、変更</td><td>DROP は、tdb-lightning-ctl がcheckpoint-destroy-all コマンドを実行する場合にのみ必要です。</td></tr><tr><td>ターゲットデータベース</td><td>作成する</td><td></td></tr><tr><td rowspan="4">必須</td><td>論理インポートモード</td><td>情報スキーマ.列</td><td>選択する</td><td></td></tr><tr><td rowspan="3">物理インポートモード</td><td>mysql.tidb</td><td>選択する</td><td></td></tr><tr><td>-</td><td>素晴らしい</td><td></td></tr><tr><td>-</td><td> RESTRICTED_VARIABLES_ADMIN、RESTRICTED_TABLES_ADMIN</td><td>ターゲット TiDB が SEM を有効にする場合に必要</td></tr><tr><td>推奨</td><td>競合検出、最大エラー</td><td>lightning.task-info-schema-name に設定されたスキーマ</td><td>選択、挿入、更新、削除、作成、ドロップ</td><td>必要ない場合は、値を「」に設定する必要があります。</td></tr><tr><td>オプション</td><td>並行輸入品</td><td>lightning.meta-schema-name に設定されたスキーマ</td><td>選択、挿入、更新、削除、作成、ドロップ</td><td>必要ない場合は、値を「」に設定する必要があります。</td></tr><tr><td>オプション</td><td>チェックポイント.ドライバー = &quot;mysql&quot;</td><td>チェックポイント.スキーマ設定</td><td>選択、挿入、更新、削除、作成、ドロップ</td><td>チェックポイント情報がファイルではなくデータベースに保存される場合に必要です</td></tr></table>

## ターゲットデータベースのストレージスペース {#storage-space-of-the-target-database}

ターゲット TiKV クラスターには、インポートされたデータを保存するのに十分なディスク容量が必要です。 [標準的なハードウェア要件](/hardware-and-software-requirements.md)に加えて、ターゲット TiKV クラスターのstorage容量は**、データ ソースのサイズ x レプリカの数 x 2**より大きくなければなりません。たとえば、クラスターがデフォルトで 3 つのレプリカを使用する場合、ターゲット TiKV クラスターにはデータ ソースのサイズの 6 倍を超えるstorageスペースが必要です。この式には x 2 が含まれています。その理由は次のとおりです。

-   インデックスには余分なスペースが必要になる場合があります。
-   RocksDB には空間増幅効果があります。

Dumplingによって MySQL からエクスポートされる正確なデータ量を計算することは困難です。ただし、次の SQL ステートメントを使用して、information_schema.tables テーブルの`DATA_LENGTH`フィールドを要約することで、データ量を見積もることができます。

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
