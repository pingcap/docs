---
title: REGEXP_SPLIT_TO_TABLE
summary: 正規表現パターンを使用して文字列を分割し、各セグメントをテーブルとして返します。
---

# REGEXP_SPLIT_TO_TABLE

正規表現パターンを使用して文字列を分割し、各セグメントをテーブルとして返します。

## 構文 {#syntax}

```sql
REGEXP_SPLIT_TO_TABLE(string, pattern [, flags text])
```

| Parameter    | 説明                                                           |
|--------------|----------------------------------------------------------------|
| `string`     | 分割する入力文字列（VARCHAR 型）                               |
| `pattern`    | 分割に使用する正規表現パターン（VARCHAR 型）                   |
| `flags text` | 正規表現の動作を変更するためのフラグ文字列です。               |

**サポートされる `flags` Parameter:**

以下の文字を組み合わせることでマッチング動作を制御できる、柔軟な正規表現の設定オプションを提供します。

* `i` (case-insensitive): パターンマッチングで大文字と小文字を区別しません。
* `c` (case-sensitive): パターンマッチングで大文字と小文字を区別します（デフォルトの動作）。
* `n` or `m` (multi-line): 複数行モードを有効にします。このモードでは、`^` と `$` はそれぞれ文字列全体の先頭と末尾だけでなく、各行の先頭と末尾にもマッチします。ドット `.` は改行文字にマッチしません。
* `s` (single-line): 単一行モード（dot-matches-newline とも呼ばれます）を有効にします。このモードでは、ドット `.` は改行文字を含む任意の文字にマッチします。
* `x` (ignore-whitespace): パターン内の空白文字を無視します（パターンの可読性が向上します）。
* `q` (literal): `pattern` を正規表現ではなくリテラル文字列として扱います。

## 例 {#examples}

### 基本的な行生成 {#basic-row-generation}

```sql
SELECT REGEXP_SPLIT_TO_TABLE('one,two,three', ',');
┌─────────┐
│ one     │
│ two     │
│ three   │
└─────────┘
```

### ログの解析 {#log-parsing}

```sql
SELECT REGEXP_SPLIT_TO_TABLE('ERR:404:File Not Found', ':');
┌──────────────────┐
│ ERR              │
│ 404              │
│ File Not Found   │
└──────────────────┘
```

### flag text を使用する {#with-flag-text}

```sql
SELECT regexp_split_to_table('One_Two_Three', '[_-]', 'i')

╭────────╮
│ One    │
│ Two    │
│ Three  │
╰────────╯

```

### ネストした使用方法 {#nested-usage}

```sql
WITH data AS (
  SELECT 'id=123,name=John' AS kv_pairs
)
SELECT
  REGEXP_SPLIT_TO_TABLE(kv_pairs, ',') AS pair
FROM data;
┌──────────────┐
│ id=123       │
│ name=John    │
└──────────────┘
```

## 関連項目 {#see-also}

- [SPLIT](/tidb-cloud-lake/sql/split.md): 単純な文字列分割用
- [REGEXP_SPLIT_TO_ARRAY](/tidb-cloud-lake/sql/regexp-split-array.md): 文字列を配列に分割します