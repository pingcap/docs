---
title: クラスターキー
summary: クラスターキーはデータを自動的に整理し、大規模テーブルのクエリ性能を大幅に向上させます。{{{ .lake }}} はバックグラウンドですべてのクラスタリング操作をシームレスかつ継続的に管理するため、クラスターキーを定義するだけで、残りは {{{ .lake }}} が処理します。
---

# クラスターキー

クラスターキーはデータを自動的に整理し、大規模テーブルのクエリ性能を大幅に向上させます。{{{ .lake }}} はバックグラウンドですべてのクラスタリング操作をシームレスかつ継続的に管理するため、クラスターキーを定義するだけで、残りは {{{ .lake }}} が処理します。

## どのような問題を解決するのか {#what-problem-does-it-solve}

適切に整理されていない大規模テーブルは、性能面と管理面で大きな課題を引き起こします。

| 問題 | 影響 | 自動クラスタリングのソリューション |
|---------|--------|------------------------------|
| **フルテーブルスキャン** | フィルタ条件がある場合でも、クエリがテーブル全体を読み取る | データを自動的に整理し、関連するブロックのみを読み取る |
| **ランダムなデータアクセス** | 類似データがストレージ全体に分散している | 関連するデータを継続的にまとめて配置する |
| **低速なフィルタクエリ** | WHERE 句が不要な行までスキャンする | 関係のないブロックを完全に自動スキップする |
| **高い I/O コスト** | 使用しない大量のデータを読み取る | データ転送を自動的に最小化する |
| **手動管理** | テーブルを監視し、手動で再クラスタリングする必要がある | 管理不要 - バックグラウンドで自動最適化 |
| **リソース管理** | クラスタリング処理用のコンピュートを割り当てる必要がある | {{{ .lake }}} がすべてのクラスタリングリソースを自動的に処理する |

**例**: 数百万件の商品を持つ EC テーブルを考えます。クラスタリングがない場合、`WHERE category IN ('Electronics', 'Computers')` のクエリでは、すべての商品カテゴリをスキャンする必要があります。category による自動クラスタリングを使用すると、{{{ .lake }}} は Electronics と Computers の商品を継続的にまとめて配置するため、1000 以上のブロックではなく 2 つのブロックだけをスキャンすれば済みます。

## 自動クラスタリングの利点 {#benefits-of-automatic-clustering}

**管理のしやすさ**: {{{ .lake }}} により、次の作業が不要になります。

- クラスタリング済みテーブルの状態監視
- 再クラスタリング処理の手動実行
- クラスタリング用コンピュートリソースの割り当て
- メンテナンス時間帯のスケジューリング

**仕組み**: クラスターキーを定義すると、{{{ .lake }}} は自動的に次を実行します。

- DML 操作によるテーブル変更を監視する
- テーブルが再クラスタリングの恩恵を受けるタイミングを評価する
- バックグラウンドでクラスタリング最適化を実行する
- 最適なデータ配置を継続的に維持する

必要なのは、各テーブルに対して適切であればクラスタリングキーを定義することだけです。その後の管理はすべて {{{ .lake }}} が自動的に行います。

## 仕組み {#how-it-works}

クラスターキーは、指定したカラムに基づいてデータをストレージブロック（Parquet ファイル）に整理します。

![Cluster Key Visualization](/media/tidb-cloud-lake/clustered.png)

1. **データ整理** → 類似した値を隣接するブロックにまとめる
2. **メタデータ作成** → 高速検索のためにブロックと値の対応関係を保存する
3. **クエリ最適化** → クエリ時に関連するブロックのみを読み取る
4. **性能向上** → スキャンする行数が減り、結果が速く返る

## クイックセットアップ {#quick-setup}

```sql
-- Create table with cluster key
CREATE TABLE sales (
    order_id INT,
    order_date TIMESTAMP,
    region VARCHAR,
    amount DECIMAL
) CLUSTER BY (region);

-- Or add cluster key to existing table
ALTER TABLE sales CLUSTER BY (region, order_date);
```

## 適切なクラスターキーの選び方 {#choosing-the-right-cluster-key}

最も一般的なクエリフィルタに基づいてカラムを選択します。

| クエリパターン | 推奨されるクラスターキー | 例 |
|---------------|------------------------|---------|
| 単一カラムでフィルタする | そのカラム | `CLUSTER BY (region)` |
| 複数カラムでフィルタする | 複数カラム | `CLUSTER BY (region, category)` |
| 日付範囲クエリ | 日付 / timestamp カラム | `CLUSTER BY (order_date)` |
| 高カーディナリティのカラム | 式を使って値の種類を減らす | `CLUSTER BY (DATE(created_at))` |

### 良いクラスターキーと悪いクラスターキー {#good-vs-bad-cluster-keys}

| ✅ 良い選択肢 | ❌ 悪い選択肢 |
|----------------|----------------|
| 頻繁にフィルタされるカラム | ほとんど使われないカラム |
| 中程度のカーディナリティ（100～10K 値） | Boolean カラム（値の種類が少なすぎる） |
| 日付 / 時刻カラム | 一意 ID カラム（値の種類が多すぎる） |
| リージョン、category、status | ランダムまたは hash カラム |

## 性能の監視 {#monitoring-performance}

```sql
-- Check clustering effectiveness
SELECT * FROM clustering_information('database_name', 'table_name');

-- Key metrics to watch:
-- average_depth: Lower is better (< 2 ideal)
-- average_overlaps: Lower is better
-- block_depth_histogram: More blocks at depth 1-2
```

## 再クラスタリングが必要なタイミング {#when-to-re-cluster}

データ変更により、テーブルは時間の経過とともに整理状態が崩れていきます。

```sql
-- Check if re-clustering is needed
SELECT IF(average_depth > 2 * LEAST(GREATEST(total_block_count * 0.001, 1), 16),
          'Re-cluster needed',
          'Clustering is good')
FROM clustering_information('your_database', 'your_table');

-- Re-cluster the table
ALTER TABLE your_table RECLUSTER;
```

## 性能チューニング {#performance-tuning}

### カスタムブロックサイズ {#custom-block-size}

より良い性能のためにブロックサイズを調整します。

```sql
-- Smaller blocks = fewer rows per query
ALTER TABLE sales SET OPTIONS(
    ROW_PER_BLOCK = 100000,
    BLOCK_SIZE_THRESHOLD = 52428800
);
```

### 自動再クラスタリング {#automatic-re-clustering}

- `COPY INTO` と `REPLACE INTO` は自動的に再クラスタリングをトリガーします
- クラスタリングメトリクスを定期的に監視してください
- `average_depth` が高くなりすぎたら再クラスタリングしてください

## ベストプラクティス {#best-practices}

| 実践 | 利点 |
|----------|---------|
| **シンプルに始める** | まずは単一カラムのクラスターキーを使う |
| **メトリクスを監視する** | clustering_information を定期的に確認する |
| **性能をテストする** | クラスタリング前後でクエリ速度を測定する |
| **定期的に再クラスタリングする** | データ変更後もクラスタリング状態を維持する |
| **コストを考慮する** | クラスタリングはコンピュートリソースを消費する |

## 重要な注意事項 {#important-notes}

**クラスターキーを使うべき場合:**

- 大規模テーブル（数百万行以上）
- クエリ性能が遅い
- フィルタベースのクエリが多い
- 分析ワークロード

**使うべきでない場合:**

- 小規模テーブル
- ランダムアクセスパターン
- 頻繁に変化するデータ

---

*クラスターキーは、予測可能なフィルタパターンを持ち、頻繁にクエリされる大規模テーブルで最も効果を発揮します。まずは最も一般的な WHERE 句のカラムから始めてください。*