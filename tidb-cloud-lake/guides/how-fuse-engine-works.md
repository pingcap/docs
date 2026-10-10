---
title: Fuse Engine の仕組み
summary: Fuse Engine は {{{ .lake }}} の中核となるストレージエンジンであり、クラウドオブジェクトストレージ上でペタバイト規模のデータを効率的に管理できるよう最適化されています。デフォルトでは、{{{ .lake }}} で作成されたテーブルは自動的にこのエンジン (ENGINE=FUSE) を使用します。Git に着想を得たスナップショットベースの設計により、強力なデータバージョニング機能 (Time Travel など) を実現し、高度な pruning と indexing によって高いクエリ性能を提供します。
---

# Fuse Engine の仕組み

## Fuse Engine {#fuse-engine}

Fuse Engine は {{{ .lake }}} の中核となるストレージエンジンであり、**ペタバイト規模**のデータを**クラウドオブジェクトストレージ**上で効率的に管理できるよう最適化されています。デフォルトでは、{{{ .lake }}} で作成されたテーブルは自動的にこのエンジン (`ENGINE=FUSE`) を使用します。Git に着想を得たスナップショットベースの設計により、強力なデータバージョニング機能 (Time Travel など) を実現し、高度な pruning と indexing によって**高いクエリ性能**を提供します。

このドキュメントでは、その中核となる概念と動作の仕組みを説明します。

## 中核となる概念 {#core-concepts}

Fuse Engine は、Git を模した 3 つの中核構造を使ってデータを整理します。

* **Snapshots (Git の Commit に相当):** 特定の Segments を参照することで、ある時点におけるテーブルの状態を定義する不変の参照です。Time Travel を可能にします。
* **Segments (Git の Tree に相当):** 高速なデータスキップ (pruning) に使用される要約統計情報を持つ Blocks の集合です。Snapshots 間で共有できます。
* **Blocks (Git の Blob に相当):** 実際の行データと、より細かい粒度の pruning のためのカラムレベルの詳細な統計情報を保持する不変のデータファイル (Parquet 形式) です。

```
                         Table HEAD
                             │
                             ▼
     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
     │  SEGMENT A    │◄────│  SNAPSHOT 2   │────►│  SEGMENT B    │
     │               │     │ Previous:     │     │               │
     └───────┬───────┘     │ SNAPSHOT 1    │     └───────┬───────┘
             │             └───────────────┘             │
             │                     │                     │
             │                     ▼                     │
             │             ┌───────────────┐             │
             │             │  SNAPSHOT 1   │             │
             │             │               │             │
             │             └───────────────┘             │
             │                                           │
             ▼                                           ▼
     ┌───────────────┐                           ┌───────────────┐
     │   BLOCK 1     │                           │   BLOCK 2     │
     │ (cloud.txt)   │                           │(warehouse.txt)│
     └───────────────┘                           └───────────────┘
```

## 書き込みの仕組み {#how-writing-works}

テーブルにデータを追加すると、Fuse Engine は一連のオブジェクトを作成します。このプロセスを順を追って見ていきましょう。

### ステップ 1: テーブルを作成する {#step-1-create-a-table}

```sql
CREATE TABLE git(file VARCHAR, content VARCHAR);
```

この時点では、テーブルは存在していますがデータは含まれていません。

```
(Empty table with no data)
```

### ステップ 2: 最初のデータを挿入する {#step-2-insert-first-data}

```sql
INSERT INTO git VALUES('cloud.txt', '2022/05/06, Datalake, Cloud');
```

最初の挿入後、Fuse Engine は初期の snapshot、segment、block を作成します。

```
         Table HEAD
             │
             ▼
     ┌───────────────┐
     │  SNAPSHOT 1   │
     │               │
     └───────┬───────┘
             │
             ▼
     ┌───────────────┐
     │  SEGMENT A    │
     │               │
     └───────┬───────┘
             │
             ▼
     ┌───────────────┐
     │   BLOCK 1     │
     │ (cloud.txt)   │
     └───────────────┘
```

### ステップ 3: さらにデータを挿入する {#step-3-insert-more-data}

```sql
INSERT INTO git VALUES('warehouse.txt', '2022/05/07, Datalake, Warehouse');
```

さらにデータを挿入すると、Fuse Engine は元の segment と新しい segment の両方を参照する新しい snapshot を作成します。

```
                         Table HEAD
                             │
                             ▼
     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
     │  SEGMENT A    │◄────│  SNAPSHOT 2   │────►│  SEGMENT B    │
     │               │     │ Previous:     │     │               │
     └───────┬───────┘     │ SNAPSHOT 1    │     └───────┬───────┘
             │             └───────────────┘             │
             │                     │                     │
             │                     ▼                     │
             │             ┌───────────────┐             │
             │             │  SNAPSHOT 1   │             │
             │             │               │             │
             │             └───────────────┘             │
             │                                           │
             ▼                                           ▼
     ┌───────────────┐                           ┌───────────────┐
     │   BLOCK 1     │                           │   BLOCK 2     │
     │ (cloud.txt)   │                           │(warehouse.txt)│
     └───────────────┘                           └───────────────┘
```

## 読み取りの仕組み {#how-reading-works}

データをクエリするとき、Fuse Engine はスマートな pruning を使用して効率的に対象データを見つけます。

```
Query: SELECT * FROM git WHERE file = 'cloud.txt';

                         Table HEAD
                             │
                             ▼
     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
     │  SEGMENT A    │◄────│  SNAPSHOT 2   │────►│  SEGMENT B    │
     │    CHECK      │     │               │     │    CHECK      │
     └───────┬───────┘     └───────────────┘     └───────────────┘
             │                                          ✗
             │                                    (Skip - doesn't contain
             │                                     'cloud.txt')
             ▼
     ┌───────────────┐
     │   BLOCK 1     │
     │    CHECK      │
     └───────┬───────┘
             │
             │ ✓ (Contains 'cloud.txt')
             ▼
        Read this block
```

### スマート pruning のプロセス {#smart-pruning-process}

```
┌─────────────────────────────────────────┐
│ Query: WHERE file = 'cloud.txt'         │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Check SEGMENT A                         │
│ Min file value: 'cloud.txt'             │
│ Max file value: 'cloud.txt'             │
│                                         │
│ Result: ✓ Might contain 'cloud.txt'     │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Check SEGMENT B                         │
│ Min file value: 'warehouse.txt'         │
│ Max file value: 'warehouse.txt'         │
│                                         │
│ Result: ✗ Cannot contain 'cloud.txt'    │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Check BLOCK 1 in SEGMENT A              │
│ Min file value: 'cloud.txt'             │
│ Max file value: 'cloud.txt'             │
│                                         │
│ Result: ✓ Contains 'cloud.txt'          │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│ Read only BLOCK 1                       │
└─────────────────────────────────────────┘
```

## スナップショットベースの機能 {#snapshot-based-features}

Fuse Engine のスナップショットアーキテクチャにより、強力なデータ管理機能が実現されます。

### Time Travel {#time-travel}

任意の時点に存在していた状態のデータをクエリできます。完全な監査証跡とエラーリカバリを備え、データのブランチ、タグ付け、ガバナンスを可能にします。

### Zero-Copy Schema Evolution {#zero-copy-schema-evolution}

基盤となるデータファイルを**一切書き換えることなく**、テーブル構造（カラムの追加、カラムの削除、名前変更、型変更）を変更できます。

- 変更は、新しい Snapshot に記録されるメタデータのみの操作です。
- これは即時に実行され、ダウンタイムを必要とせず、高コストなデータ移行作業を回避できます。古いデータにも元のスキーマで引き続きアクセスできます。

## クエリ高速化のための高度なインデックス機能（Fuse Engine） {#advanced-indexing-for-query-acceleration-fuse-engine}

統計情報を使った基本的な block/segment pruning に加えて、Fuse Engine は特定のクエリパターンをさらに高速化するための専用セカンダリインデックスを提供します。

| インデックスタイプ          | 簡単な説明                                         | 次のようなクエリを高速化                         | クエリ例のスニペット                   |
| :------------------ | :-------------------------------------------------------- | :-------------------------------------------------- | :-------------------------------------- |
| **Aggregate Index** | 指定したグループに対する集計結果を事前計算する       | `COUNT`、`SUM`、`AVG`... + `GROUP BY` をより高速化          | `SELECT COUNT(*)... GROUP BY city`      |
| **Full-Text Index** | テキスト内の高速なキーワード検索のための転置インデックス        | `MATCH` を使ったテキスト検索（例: ログ）              | `WHERE MATCH(log_entry, 'error')`     |
| **JSON Index**      | JSON ドキュメント内の特定のパス/キーにインデックスを作成する       | 特定の JSON パス/値によるフィルタリング             | `WHERE event_data:user.id = 123`      |
| **Bloom Filter Index** | 一致しない block をすばやくスキップするための確率的チェック | 高速なポイントルックアップ（`=`）および `IN` リストのフィルタリング      | `WHERE user_id = 'xyz'` |

## 比較: {{{ .lake }}} Fuse Engine と Apache Iceberg {#comparison-lake-fuse-engine-vs-apache-iceberg}

_**Note:** この比較は、**テーブルフォーマット機能**に特化したものです。{{{ .lake }}} のネイティブなテーブルフォーマットとして、Fuse は進化を続けており、**使いやすさとパフォーマンス**の向上を目指しています。ここに示す機能は現時点のものであり、今後変更される可能性があります。_

| 機能                 | Apache Iceberg                     | {{{ .lake }}} Fuse Engine                 |
| :---------------------- | :--------------------------------- | :----------------------------------- |
| **メタデータ構造**  | Manifest Lists -> Manifest Files -> Data Files | **Snapshot** -> Segments -> Blocks   |
| **統計情報レベル**   | ファイルレベル（+Partition）            | **マルチレベル**（Snapshot、Segment、Block）→ より細かな pruning |
| **Pruning 性能**        | 良好（File/Partition 統計情報）      | **非常に優秀**（マルチレベル統計情報 + セカンダリインデックス） |
| **スキーマエボリューション** | サポートあり（メタデータ変更）        | **Zero-Copy**（メタデータのみ、即時） |
| **データクラスタリング**     | ソート（書き込み時）     | **自動**最適化（バックグラウンド） |
| **ストリーミングサポート**   | 基本的なストリーミング取り込み          | **高度な Incremental**（Insert/Update の追跡） |