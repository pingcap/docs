---
title: READ_FILE
summary: stage からファイルを読み取り、その生バイトを返します。
---

# READ_FILE

stage からファイルを読み取り、その内容を生バイトとして返します。

`READ_FILE` は、ドキュメント、画像、モデル入力など、stage に配置されたアセットを下流のデータセットにパッケージ化したい場合に便利です。たとえば、学習データを Lance にアンロード (unload) する場合に使用できます。

## 構文 {#syntax}

```sql
READ_FILE('@<stage>/<path-to-file>')
READ_FILE('@<stage>', '<path-to-file>')
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `@<stage>/<path-to-file>` | 完全な stage ファイルパスです。この式は、`@` で始まる stage ファイルパスに解決される必要があります。 |
| `@<stage>` | 2 引数形式での stage 名です。`@assets` のような定数の stage 参照を使用します。 |
| `<path-to-file>` | stage からの相対ファイルパスです。文字列リテラル、カラム、または文字列に解決される式を指定できます。 |

## 戻り値の型 {#return-type}

`BINARY`

いずれかの引数が `NULL` の場合、結果は `NULL` になります。

## 使用上の注意 {#usage-notes}

- `READ_FILE` は stage からファイルを読み取ります。{{{ .lake }}} サーバー上のローカルファイルは読み取りません。
- 対象はディレクトリではなく、ファイルである必要があります。
- 呼び出し元には stage を読み取る権限が必要です。

## 例 {#examples}

完全な stage パスを使用してファイルを読み取ります。

```sql
SELECT TO_HEX(READ_FILE('@data/csv/prefix/ab.csv'));
```

結果:

```text
31
```

stage 名と相対パスを組み合わせてファイルを読み取ります。

```sql
SELECT TO_HEX(READ_FILE('@data', 'csv/prefix/ab.csv'));
```

結果:

```text
31
```

定数の stage と行ごとの相対パスを組み合わせて複数のファイルを読み取ります。

```sql
CREATE OR REPLACE TABLE read_file_rel_paths(path STRING);

INSERT INTO read_file_rel_paths VALUES
  ('csv/prefix/ab.csv'),
  ('csv/prefix/ab/cd.csv'),
  (NULL);

SELECT path, TO_HEX(READ_FILE('@data', path))
FROM read_file_rel_paths
ORDER BY path;
```

結果:

```text
+----------------------+--------------------------------+
| path                 | to_hex(read_file('@data',path)) |
+----------------------+--------------------------------+
| csv/prefix/ab.csv    | 31                             |
| csv/prefix/ab/cd.csv | 32                             |
| NULL                 | NULL                           |
+----------------------+--------------------------------+
```