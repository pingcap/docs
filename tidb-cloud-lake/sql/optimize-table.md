---
title: OPTIMIZE TABLE
summary: "{{{ .lake }}} でのテーブルの最適化では、履歴データのコンパクションまたは削除を行い、ストレージ容量を節約してクエリ性能を向上させます。"
---

# OPTIMIZE TABLE

{{{ .lake }}} でのテーブルの最適化では、履歴データのコンパクションまたは削除を行い、ストレージ容量を節約してクエリ性能を向上させます。

<details>
  <summary>最適化する理由</summary>
    <div>{{{ .lake }}} は、ブロック単位で構成された Parquet 形式を使用してテーブルにデータを保存します。さらに、{{{ .lake }}} はタイムトラベル機能をサポートしており、テーブルを変更する各操作によって、テーブルに加えられた変更を記録して反映する Parquet ファイルが生成されます。</div><br/>

   <div>時間の経過とともにテーブルに Parquet ファイルが蓄積されると、性能上の問題やストレージ要件の増加につながる可能性があります。テーブル性能を最適化するために、不要になった履歴 Parquet ファイルを削除できます。この最適化により、クエリ性能の向上と、テーブルが使用するストレージ容量の削減が期待できます。</div>
</details>

## {{{ .lake }}} のデータストレージ: Snapshot、Segment、Block {#-lake--data-storage-snapshot-segment-and-block}

スナップショット、セグメント、ブロックは、{{{ .lake }}} がデータストレージに使用する概念です。{{{ .lake }}} はこれらを使用して、テーブルデータを保存するための階層構造を構築します。

![データストレージ構造](/media/tidb-cloud-lake/storage-structure.PNG)

{{{ .lake }}} は、データ更新時にテーブルのスナップショットを自動的に作成します。スナップショットは、テーブルのセグメントメタデータのあるバージョンを表します。

{{{ .lake }}} を使用する際、過去バージョンのテーブルデータを [AT](/tidb-cloud-lake/sql/at.md) 句で取得およびクエリするときに、スナップショット ID を指定してスナップショットにアクセスすることが最も多くなります。

スナップショットは JSON ファイルであり、テーブルデータ自体は保存せず、そのスナップショットがリンクしているセグメントを示します。テーブルに対して [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md) を実行すると、そのテーブルに保存されているスナップショットを確認できます。

セグメントは JSON ファイルで、データが保存されているストレージブロック（最小 1、最大 1,000）を整理します。スナップショット ID を指定したスナップショットに対して [FUSE_SEGMENT](/tidb-cloud-lake/sql/fuse-segment.md) を実行すると、そのスナップショットが参照しているセグメントを確認できます。

{{{ .lake }}} は実際のテーブルデータを Parquet ファイルに保存し、各 Parquet ファイルをブロックと見なします。スナップショット ID を指定したスナップショットに対して [FUSE_BLOCK](/tidb-cloud-lake/sql/fuse-block.md) を実行すると、そのスナップショットが参照しているブロックを確認できます。

{{{ .lake }}} は、スナップショット、セグメント、ブロックファイルを保存するために、各データベースおよびテーブルに一意の ID を作成し、それらをオブジェクトストレージ上の `<bucket_name>/<tenant_id>/<db_id>/<table_id>/` パスに保存します。各スナップショット、セグメント、ブロックファイルには UUID（32 文字の小文字 16 進文字列）を使用した名前が付けられます。

| ファイル | 形式 | ファイル名 | ストレージフォルダ |
|----------|---------|---------------------------------|-----------------------------------------------------|
| Snapshot | JSON    | `<32bitUUID>_<version>.json`    | `<bucket_name>/<tenant_id>/<db_id>/<table_id>/_ss/` |
| Segment  | JSON    | `<32bitUUID>_<version>.json`    | `<bucket_name>/<tenant_id>/<db_id>/<table_id>/_sg/` |
| Block    | parquet | `<32bitUUID>_<version>.parquet` | `<bucket_name>/<tenant_id>/<db_id>/<table_id>/_b/`  |

## テーブルの最適化 {#table-optimizations}

{{{ .lake }}} では、理想的なブロックサイズとして 100MB（非圧縮）または 1,000,000 行を目安とし、各セグメントは 1,000 ブロックで構成されることが推奨されます。テーブル最適化を最大化するには、[セグメントのコンパクション](#segment-compaction) や [ブロックのコンパクション](#block-compaction) など、さまざまな最適化手法をいつどのように適用するかを明確に理解することが重要です。

- クラスターキーを含むテーブルに対して COPY INTO または REPLACE INTO コマンドでデータを書き込む場合、{{{ .lake }}} は再クラスタリングプロセスに加えて、セグメントおよびブロックのコンパクションも自動的に開始します。

- セグメントとブロックのコンパクションは、クラスター環境での分散実行をサポートしています。ENABLE_DISTRIBUTED_COMPACT を 1 に設定することで有効化できます。これにより、クラスター環境でのデータクエリ性能とスケーラビリティの向上に役立ちます。

  ```sql
  SET enable_distributed_compact = 1;
  ```

### セグメントのコンパクション {#segment-compaction}

テーブルに小さなセグメント（1 セグメントあたり `100 blocks` 未満）が多すぎる場合は、セグメントのコンパクションを実行します。

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

**構文**

```sql
OPTIMIZE TABLE [database.]table_name COMPACT SEGMENT [LIMIT <segment_count>]
```

小さなセグメントをより大きなセグメントにマージすることで、テーブルデータのコンパクションを実行します。

- LIMIT オプションは、コンパクションの対象とするセグメントの最大数を設定します。この場合、{{{ .lake }}} は最新のセグメントを選択してコンパクションを実行します。

**例**

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

### ブロックのコンパクション {#block-compaction}

テーブルに多数の小さなブロックがある場合、または挿入、削除、更新された行の割合が高い場合は、ブロックのコンパクションを実行します。

各ブロックの非圧縮サイズが理想サイズである `100MB` に近いかどうかで確認できます。

サイズが `50MB` 未満の場合は、小さなブロックが多すぎることを示すため、ブロックのコンパクションを実行することを推奨します。

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
> まずセグメントのコンパクションを実行し、その後にブロックのコンパクションを実行することを推奨します。

**構文**

```sql
OPTIMIZE TABLE [database.]table_name COMPACT [LIMIT <segment_count>]
```

小さなブロックとセグメントをより大きなものにマージすることで、テーブルデータのコンパクションを実行します。

- このコマンドは、既存のストレージファイルに影響を与えることなく、最新のテーブルデータに対する新しいスナップショット（コンパクション済みのセグメントおよびブロックを含む）を作成します。そのため、履歴データを削除するまではストレージ容量は解放されません。

- 対象テーブルのサイズによっては、実行完了までかなり時間がかかる場合があります。

- LIMIT オプションは、コンパクションの対象とするセグメントの最大数を設定します。この場合、{{{ .lake }}} は最新のセグメントを選択してコンパクションを実行します。

- {{{ .lake }}} は、コンパクションの後にクラスタリングされたテーブルを自動的に再クラスタリングします。

**例**

```sql
OPTIMIZE TABLE my_database.my_table COMPACT LIMIT 50;
```