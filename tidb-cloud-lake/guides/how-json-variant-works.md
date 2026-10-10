---
title: TiDB Cloud Lake JSON (Variant) の仕組み
summary: TiDB Cloud Lake は、ネイティブなバイナリレイアウトと自動 JSON インデックスを組み合わせることで JSON 分析を再構築し、半構造化データを第一級のカラムのように扱えるようにします。
---

# TiDB Cloud Lake JSON (Variant) の仕組み

関連情報:

- [Variant データ型](/tidb-cloud-lake/sql/variant.md)
- [半構造化関数](/tidb-cloud-lake/guides/load-semi-structured-data.md)

{{{ .lake }}} は、ネイティブなバイナリレイアウトと自動 JSON インデックスを組み合わせることで JSON 分析を再構築し、半構造化データを第一級のカラムのように扱えるようにします。

## Variant が重要な理由 {#why-variant-matters}

{{{ .lake }}} は JSON の柔軟性を保ちながら、MPP の速度を実現します。ドキュメントをそのまま取り込み、使い慣れた SQL でクエリでき、エンジンがその背後で性能面を支えます。これを可能にする 2 つの柱があります。

- コンパクトな **JSONB** レイアウトにより、型情報が実行エンジンから見える状態に保たれます。
- 自動 **virtual columns**（{{{ .lake }}} の JSON インデックス）により、頻繁に使われるパスが手作業なしで表面化されます。

ストレージからクエリまで、このガイドではこれら 2 つの考え方によって、生の JSON ペイロード（たとえば `orders.data`）が最適化された型付きカラムへと変わる流れを追います。

## JSON ストレージレイアウト {#json-storage-layout}

{{{ .lake }}} は、Variant 値を分析向けに最適化されたバイナリ形式である JSONB に保存します。実際には、これは次のことを意味します。

- **型付きストレージ** – 数値、ブール値、タイムスタンプ、decimal はネイティブなまま保持されるため、比較はバイナリレベルで安全に行えます。
- **予測可能なレイアウト** – フィールドには長さプレフィックスと正規化されたキー順序が付与され、再パースのオーバーヘッドを排除します。
- **ゼロコピーアクセス** – 演算子は、スキャンやソート時に JSON テキストを再構築する代わりに、JSONB バッファを直接読み取ります。

各 Variant カラムは、完全性を保つために生の JSONB ドキュメントを保持します。`data['user']['id']` のようなパスが繰り返し現れる場合、{{{ .lake }}} はそれらを pushdown に使える型付きの補助カラムに格納します。

## 自動 JSON インデックス生成 {#automatic-json-index-generation}

新しいデータが {{{ .lake }}} に到着すると、軽量なインデックス作成パイプラインが直ちに JSON ブロックをスキャンし、virtual columns として実体化する価値のあるホットパス、つまり {{{ .lake }}} 組み込みの JSON インデックスを検出します。

### 取り込みフロー {#ingestion-flow}

{{{ .lake }}} は入力バッチを調べ、繰り返し現れるアクセスパターンを型付きカラムに変換します。

```
┌───────────────────────────────────────────────┐
│ Variant Ingestion Flow                        │
├──────────────┬────────────────────────────────┤
│ Sample Rows  │ Peek at the first rows in block │
│ Detect Paths │ Keep stable leaf key paths      │
│ Infer Types  │ Pick native column types        │
│ Materialize  │ Write values to virtual Parquet │
│ Register     │ Attach metadata to base column  │
└──────────────┴────────────────────────────────┘
```

### 軽量な設計 {#lightweight-by-design}

このパイプラインは、少数の軽量なヒューリスティクスに基づいています。

```
┌─────────────────────────────┬──────────────────────────────────────────────┐
│ Step                        │ Heuristic                                    │
├─────────────────────────────┼──────────────────────────────────────────────┤
│ Sampling                    │ Inspect only the first 10 rows of each block │
│ Null & non-leaf filtering   │ Skip paths dominated by NULL or pointing to  │
│                             │ objects/arrays                               │
│ Stability check             │ Promote only leaf paths that stay consistent │
│                             │ across the sample (max 1,000 per block)      │
│ Deduplication               │ Use hashing to avoid analysing the same path │
│                             │ repeatedly                                    │
│ Fallback                    │ Keep the original JSONB document when no     │
│                             │ candidate survives                           │
└─────────────────────────────┴──────────────────────────────────────────────┘
```

その結果、JSON を一度ロード (load) するだけで、繰り返し現れるパターンが静かに最適化された型付きカラムへと変換され、DDL もチューニングも不要です。

### Virtual columns は自動 JSON インデックス {#virtual-columns-are-automatic-json-indexes}

この文脈での「virtual column」は、単に **{{{ .lake }}} の JSON インデックス** を意味します。取り込みフローは、`data['items'][0]['price']` のようなパスが十分に安定しているかを判断し、ネイティブ型を推論し、それらの値をメタデータ付きのカラムナ形式の補助領域に書き込みます。DDL も設定項目も不要です。ネストされた JSON はコンパクトな JSONB 形式のまま保持され、プリミティブなパスはネイティブな数値、文字列、またはブール値になります。

```
Raw JSON block ──(auto sampling)──▶ Candidate paths ──(stable?)──▶ JSON index
```

{{{ .lake }}} は別個の B-tree を構築する代わりに、JSON パスの値をカラムナ構造にスナップショットします。

```
JSON Path    ───────────▶  Virtual Column (typed values + stats + location)
```

クエリ時には、プランナーはこれらの事前抽出済みの値へ直接ジャンプできます。これはインデックスにヒットするのと同様ですが、インデックスエントリが存在しない場合でも完全な JSON にフォールバックできます。

### JSON インデックスメタデータ {#json-index-metadata}

各ブロックとともに保存されるメタデータは、追加カラムの概要を示します。

```
┌────────────────────────────┬───────────────────────┐
│ Virtual Column Metadata    │ Example               │
├────────────────────────────┼───────────────────────┤
│ Column Id & JSON Path      │ v123 -> ['user']['id'] │
│ Type Code                  │ UInt64 / String       │
│ Byte Offset & Length       │ Where values live     │
│ Row Count                  │ Matches base block    │
│ Statistics                 │ Min / Max / NDV       │
└────────────────────────────┴───────────────────────┘
```

ライターはこれらの詳細をテーブルスナップショットにまとめ、補助データをメインブロックと一緒に保存します。各エントリは JSON パス、ネイティブ型、バイトオフセット、統計情報を保持しているため、{{{ .lake }}} は必要に応じて抽出済みの値へ直接ジャンプしたり、元の JSON にフォールバックしたりできます。

## JSON インデックスを使ったクエリ実行 {#query-execution-with-json-indexes}

インデックスが作成されると、読み取りパスは 3 つの素早い判断に集約されます。

```
┌──────────────┐   rewrite paths   ┌────────────────────┐
│ SQL Planner  │------------------>│ Virtual Column Map │
└──────┬───────┘                   └─────────┬──────────┘
       │ pushdown request                   │ per-block check
       ▼                                    ▼
┌──────────────┐   has virtual?   ┌────────────────────┐
│ Fuse Storage │----------------->│ Virtual File Read  │
└──────┬───────┘        │        └─────────┬──────────┘
       │ no             └------------------┘ fallback
       ▼
┌──────────────┐
│ JSONB Reader │
└──────┬───────┘
       ▼
┌──────────────┐
│ Query Output │
└──────────────┘
```

- プランニング時に、{{{ .lake }}} は `get_by_keypath` のような呼び出しを、メタデータ上インデックスが存在する場合は直接 virtual column を読む形に書き換えます。
- ストレージ層は virtual column が存在する場合にそれを参照し、その Parquet スライスだけを読み取ります。要求されたすべてのパスがインデックス化されていれば、元の JSON カラムをスキップすることもできます。
- それ以外の場合は、JSONB カラム上で `get_by_keypath` を評価する形にフォールバックし、セマンティクスを維持します。
- フィルタ、projection、統計情報は、JSON 文字列を再パースする代わりにネイティブ型に対して動作します。

内部では、{{{ .lake }}} は各 virtual column がどの JSON パスから生成されたかを追跡しているため、生のドキュメントをスキップできる場面と、再度開く必要がある場面を正確に判断できます。

## Variant データの操作 {#working-with-variant-data}

インデックス作成は内部で処理されるため、Variant カラムは使い慣れた構文や関数で操作できます。

### Virtual columns の確認 {#inspect-virtual-columns}

[`SHOW VIRTUAL COLUMNS`](/tidb-cloud-lake/sql/show-virtual-columns.md) を使用すると、テーブルに対して自動生成された virtual columns を一覧表示できます。これにより、{{{ .lake }}} がどの JSON パスを実体化したかを確認できます。

### アクセス構文 {#access-syntax}

{{{ .lake }}} は Snowflake スタイルと PostgreSQL スタイルの両方のセレクタを理解します。どちらのスタイルを選んでも、エンジンは同じキーパスパーサーを通して処理し、JSON インデックスを再利用します。`orders` の例を続けると、ネストされたフィールドには次のようにアクセスできます。

```sql title="Snowflake-style examples"
SELECT data['user']['profile']['name'],
       data:user:profile.settings.theme,
       data['items'][0]['price']
FROM orders;
```

```sql title="PostgreSQL-style examples"
SELECT data->'user'->'profile'->>'name',
       data#>>'{user,profile,settings,theme}',
       data @> '{"user":{"id":123}}'
FROM orders;
```

### 主な関数 {#function-highlights}

パスアクセサに加えて、{{{ .lake }}} には豊富な Variant ツールキットが用意されています。

- **パースとキャスト**: `parse_json`, `try_parse_json`, `to_variant`, `to_jsonb_binary`
- **ナビゲーションと projection**: `get_path`, `get_by_keypath`, `flatten`, arrow (`->`, `->>`), path (`#>`, `#>>`) および containment 演算子 (`@>`, `?`)
- **変更**: `object_insert`, `object_remove_keys`, 連結 (`||`), `array_*` ヘルパー
- **分析**: `json_extract_keys`, `json_length`, `jsonb_array_elements`, `json_array_agg` などの集約関数

すべての関数は、ベクトル化エンジン内の JSONB バッファに対して直接動作します。

## パフォーマンス特性 {#performance-characteristics}

- 生の JSON スキャンとの内部ベンチマーク比較:
    - 単一パスのルックアップ: **約 3 倍高速**、スキャンデータ量は **約 26 分の 1**
    - 複数パスの projection: **約 1.4 倍高速**、読み取りデータ量は **約 5.5 分の 1**
    - Predicate pushdown は bloom/inverted indexes と組み合わせてブロックを絞り込めます。
- JSON の形状が安定しているほど、インデックス対象となるパスが増えます。

## Variant データに対する {{{ .lake }}} の利点 {#lake-advantages-for-variant-data}

- **Snowflake 互換の表面積** – 既存のクエリや UDF をそのまま持ち込めます。
- **ネイティブ JSONB 実行** – 型付きエンコーディングとベクトル化演算子により、文字列の組み替えを回避します。
- **自動 JSON インデックス** – サンプリング、メタデータ、pushdown により、半構造化データを構造化データのように扱えます。
- **運用効率** – virtual blocks は通常の Fuse blocks とライフサイクル管理ツールを共有するため、ストレージとコンピュートの予測可能性を保てます。

自動 JSON インデックスにより、{{{ .lake }}} は柔軟なドキュメントと高性能分析の間のギャップを縮め、半構造化データを Warehouse における第一級の存在にします。