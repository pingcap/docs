---
title: MATCH
summary: インデックス付きカラム内でキーワード一致を検索し、`WHERE` 句でのみ使用できます。
---

# MATCH

`MATCH` は、指定したカラム内で与えられたキーワードを含む行を検索します。この関数は `WHERE` 句でのみ使用できます。

> **Note:**
>
> {{{ .lake }}} の MATCH 関数は、Elasticsearch の [MATCH](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-functions-search.html#sql-functions-search-match) に着想を得ています。

## 構文 {#syntax}

```sql
MATCH('<columns>', '<keywords>'[, '<options>'])
```

- `<columns>`: 検索対象のカラムをカンマ区切りで指定します。`^<boost>` を付けると、他のカラムより高い重みを設定できます。
- `<keywords>`: 検索する語句です。たとえば `rust*` のように、接尾辞一致には `*` を付けます。
- `<options>`: 検索を微調整するための、`key=value` ペアをセミコロン区切りで指定する任意のリストです。

## オプション {#options}

| オプション | 値 | 説明 | 例 |
|--------|--------|-------------|---------|
| `fuzziness` | `1` または `2` | 指定した Levenshtein 距離内でキーワードを一致させます。 | `MATCH('summary, tags', 'pedestrain', 'fuzziness=1')` は、正しいスペルの `pedestrian` を含む行に一致します。 |
| `operator` | `OR` (デフォルト) または `AND` | ブール演算子が指定されていない場合に、複数のキーワードをどのように組み合わせるかを制御します。 | `MATCH('summary, tags', 'traffic light red', 'operator=AND')` は両方の単語を必要とします。 |
| `lenient` | `true` または `false` | `true` の場合、解析エラーを抑制し、空の結果セットを返します。 | `MATCH('summary, tags', '()', 'lenient=true')` は、エラーの代わりに行を返しません。 |

## 例 {#examples}

多くの AI パイプラインでは、検索用に人が読める要約を実体化しつつ、構造化メタデータを `VARIANT` カラムに格納することがあります。次の例では、JSON ペイロードから抽出したドライブレコーダーのフレーム要約とタグを保存します。

### 例: 検索可能な要約を作成する {#example-build-searchable-summaries}

```sql
CREATE OR REPLACE TABLE frame_notes (
  id INT,
  camera STRING,
  summary STRING,
  tags STRING,
  INVERTED INDEX idx_notes (summary, tags)
);

INSERT INTO frame_notes VALUES
  (1, 'dashcam_front',
      'Green light at Market & 5th with pedestrian entering the crosswalk',
      'downtown commute green-light pedestrian'),
  (2, 'dashcam_front',
      'Vehicle stopped at Mission & 6th red traffic light with cyclist ahead',
      'stop urban red-light cyclist'),
  (3, 'dashcam_front',
      'School zone caution sign in SOMA with pedestrian waiting near crosswalk',
      'school-zone caution pedestrian');
```

### 例: Boolean AND {#example-boolean-and}

```sql
SELECT id, summary
FROM frame_notes
WHERE MATCH('summary, tags', 'traffic light red', 'operator=AND');
-- Returns id 2
```

### 例: あいまい一致 {#example-fuzzy-matching}

```sql
SELECT id, summary
FROM frame_notes
WHERE MATCH('summary^2, tags', 'pedestrain', 'fuzziness=1');
-- Returns ids 1 and 3
```