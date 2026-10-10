---
title: OPTIMIZE TABLE
summary: "{{{ .lake }}} でテーブルを最適化するには、履歴データを圧縮または削除して、ストレージ容量を節約し、クエリ性能を向上させます。"
---

# OPTIMIZE TABLE

{{{ .lake }}} でテーブルを最適化するには、履歴データを圧縮または削除して、ストレージ容量を節約し、クエリ性能を向上させます。

<details>
  <summary>最適化する理由</summary>
    <div>{{{ .lake }}} は、ブロック単位で構成された Parquet 形式を使用してテーブルにデータを保存します。さらに、{{{ .lake }}} はタイムトラベル機能をサポートしており、テーブルを変更する各操作によって、テーブルに加えられた変更を記録して反映する Parquet ファイルが生成されます。</div><br/>

   <div>時間の経過とともにテーブルに Parquet ファイルが蓄積されると、性能上の問題やストレージ要件の増加につながる可能性があります。テーブル性能を最適化するために、不要になった履歴 Parquet ファイルを削除できます。この最適化により、クエリ性能の向上と、テーブルが使用するストレージ容量の削減が期待できます。</div>
</details>

## {{{ .lake }}} のデータストレージ: Snapshot、Segment、Block {#lake-data-storage-snapshot-segment-and-block}

Snapshot、segment、block は、{{{ .lake }}} がデータストレージに使用する概念です。{{{ .lake }}} はこれらを使用して、テーブルデータを保存するための階層構造を構築します。

![データストレージ構造](/media/tidb-cloud-lake/storage-structure.PNG)

{{{ .lake }}} は、データ更新時にテーブルの snapshot を自動的に作成します。snapshot は、テーブルの segment メタデータのあるバージョンを表します。

{{{ .lake }}} を使用する際、過去バージョンのテーブルデータを [AT](/tidb-cloud-lake/sql/at.md) 句で取得およびクエリするときに、snapshot ID を指定して snapshot にアクセスすることが最も多くなります。

snapshot は JSON ファイルであり、テーブルデータ自体は保存せず、その snapshot がリンクしている segment を示します。テーブルに対して [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md) を実行すると、そのテーブルに保存されている snapshot を確認できます。

segment は JSON ファイルで、データが保存されているストレージブロック（最小 1、最大 1,000）を整理します。snapshot ID を指定した snapshot に対して [FUSE_SEGMENT](/tidb-cloud-lake/sql/fuse-segment.md) を実行すると、その snapshot が参照している segment を確認できます。

{{{ .lake }}} は実際のテーブルデータを Parquet ファイルに保存し、各 Parquet ファイルを block と見なします。snapshot ID を指定した snapshot に対して [FUSE_BLOCK](/tidb-cloud-lake/sql/fuse-block.md) を実行すると、その snapshot が参照している block を確認できます。

{{{ .lake }}} は、snapshot、segment、block ファイルを保存するために、各データベースおよびテーブルに一意の ID を作成し、それらをオブジェクトストレージ上の `<bucket_name>/<tenant_id>/<db_id>/<table_id>/` パスに保存します。各 snapshot、segment、block ファイルには UUID（32 文字の小文字 16 進文字列）を使用した名前が付けられます。

| ファイル | 形式 | ファイル名 | ストレージフォルダ |
|----------|---------|---------------------------------|-----------------------------------------------------|
| Snapshot | JSON    | `<32bitUUID>_<version>.json`    | `<bucket_name>/<tenant_id>/<db_id>/<table_id>/_ss/` |
| Segment  | JSON    | `<32bitUUID>_<version>.json`    | `<bucket_name>/<tenant_id>/<db_id>/<table_id>/_sg/` |
| Block    | parquet | `<32bitUUID>_<version>.parquet` | `<bucket_name>/<tenant_id>/<db_id>/<table_id>/_b/`  |

## テーブルの最適化 {#table-optimizations}

{{{ .lake }}} では、理想的な block サイズとして 100MB（非圧縮）または 1,000,000 行を目安とし、各 segment は 1,000 block で構成されることが推奨されます。テーブル最適化を最大化するには、[Segment Compaction](#segment-compaction) や [Block Compaction](#block-compaction) など、さまざまな最適化手法をいつどのように適用するかを明確に理解することが重要です。

- cluster key を含むテーブルに対して COPY INTO または REPLACE INTO コマンドでデータを書き込む場合、{{{ .lake }}} は re-clustering プロセスに加えて、segment および block の compact プロセスも自動的に開始します。

- Segment と block compaction は、クラスター環境での分散実行をサポートしています。ENABLE_DISTRIBUTED_COMPACT を 1 に設定することで有効化できます。これにより、クラスター環境でのデータクエリ性能とスケーラビリティの向上に役立ちます。

  ```sql
  SET enable_distributed_compact = 1;
  ```

### Segment Compaction {#segment-compaction}

テーブルに小さな segment（1 segment あたり `100 blocks` 未満）が多すぎる場合は、segment を compact します。

```sql
SELECT
  block_count,
  segment_count,
  IF(
              block_count / segment_count < 100,
              'The table needs segment compact now',
              'The table does not need segment compact now'
    ) AS advice
FROM
  fuse_snapshot('your-database', 'your-table')
    LIMIT 1;
```

**Syntax**

```sql
OPTIMIZE TABLE [database.]table_name COMPACT SEGMENT [LIMIT <segment_count>]
```

小さな segment をより大きな segment にマージすることで、テーブルデータを compact します。

- LIMIT オプションは、compact する segment の最大数を設定します。この場合、{{{ .lake }}} は最新の segment を選択して compact します。

**Example**

```sql
-- Check whether need segment compact
SELECT
  block_count,
  segment_count,
  IF(
              block_count / segment_count < 100,
              'The table needs segment compact now',
              'The table does not need segment compact now'
    ) AS advice
FROM
  fuse_snapshot('hits', 'hits');

+-------------+---------------+-------------------------------------+
| block_count | segment_count | advice                              |
+-------------+---------------+-------------------------------------+
|         751 |            32 | The table needs segment compact now |
+-------------+---------------+-------------------------------------+

-- Compact segment
OPTIMIZE TABLE hits COMPACT SEGMENT;

-- Check again
SELECT
  block_count,
  segment_count,
  IF(
              block_count / segment_count < 100,
              'The table needs segment compact now',
              'The table does not need segment compact now'
    ) AS advice
FROM
  fuse_snapshot('hits', 'hits')
    LIMIT 1;

+-------------+---------------+---------------------------------------------+
| block_count | segment_count | advice                                      |
+-------------+---------------+---------------------------------------------+
|         751 |             1 | The table does not need segment compact now |
+-------------+---------------+---------------------------------------------+
```

### Block Compaction {#block-compaction}

テーブルに多数の小さな block がある場合、または挿入、削除、更新された行の割合が高い場合は、block を compact します。

各 block の非圧縮サイズが理想サイズである `100MB` に近いかどうかで確認できます。

サイズが `50MB` 未満の場合は、小さな block が多すぎることを示すため、block compaction を実行することを推奨します。

```sql
SELECT
  block_count,
  humanize_size(bytes_uncompressed / block_count) AS per_block_uncompressed_size,
  IF(
              bytes_uncompressed / block_count / 1024 / 1024 < 50,
              'The table needs block compact now',
              'The table does not need block compact now'
    ) AS advice
FROM
  fuse_snapshot('your-database', 'your-table')
    LIMIT 1;
```

> **Note:**
>
> まず segment compaction を実行し、その後に block compaction を実行することを推奨します。

**Syntax**

```sql
OPTIMIZE TABLE [database.]table_name COMPACT [LIMIT <segment_count>]
```

小さな block と segment をより大きなものにマージすることで、テーブルデータを compact します。

- このコマンドは、既存のストレージファイルに影響を与えることなく、最新のテーブルデータに対する新しい snapshot（compact 済みの segment および block を含む）を作成します。そのため、履歴データを purge するまではストレージ容量は解放されません。

- 対象テーブルのサイズによっては、実行完了までかなり時間がかかる場合があります。

- LIMIT オプションは、compact する segment の最大数を設定します。この場合、{{{ .lake }}} は最新の segment を選択して compact します。

- {{{ .lake }}} は、compact 処理の後に clustered table を自動的に re-cluster します。

**Example**

```sql
OPTIMIZE TABLE my_database.my_table COMPACT LIMIT 50;
```