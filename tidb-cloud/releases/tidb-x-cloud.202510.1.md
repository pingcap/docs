---
title: TiDB-X-CLOUD.202510.1 リリースノート
summary: TiDB-X-CLOUD.202510.1 カーネルの機能について説明します。
---

# TiDB-X-CLOUD.202510.1 Release Notes

**リリース日**: 2026年4月28日

**適用される TiDB Cloud プラン**: {{{ .premium }}}

**TiDB X カーネルバージョン**: `TiDB-X-CLOUD.202510.1`

{{{ .premium }}} は、`TiDB-X-CLOUD.202510.1` カーネルを使用して、2026年4月28日よりパブリックプレビューで利用できます。

`TiDB-X-CLOUD.202510.1` では、次のようになります。

- `202510` は、このカーネルバージョンのベースラインコードブランチが 2025 年 10 月に作成されたことを示しており、リリース日とは異なります。
- `1` は、`TiDB-X-CLOUD.202510` ベースラインブランチからビルドされた最初のパッチリリースであることを示します。

`TiDB-X-CLOUD.202510.1` カーネルは [TiDB v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0/) カーネルをベースとしており、TiDB v8.5.0 で導入された機能と改善の大部分を含んでいます。

さらに、[TiDB v8.5.0](https://docs.pingcap.com/tidb/stable/release-8.5.0/) カーネルと比較して、`TiDB-X-CLOUD.202510.1` カーネルでは次の機能が導入されています。

## 新しい TiDB X アーキテクチャ {#new-tidb-x-architecture}

* TiDB X アーキテクチャを導入しました。これは、クラウドネイティブなオブジェクトストレージを TiDB の中核とする、クラウドネイティブな共有ストレージアーキテクチャです。

    このアーキテクチャにより、AI 時代のワークロードに向けて、弾力的なスケーラビリティ、予測可能なパフォーマンス、そして最適化された総保有コスト（TCO）を実現します。

    TiDB X は、[従来の TiDB](https://docs.pingcap.com/tidbcloud/tidb-architecture/?plan=premium) の shared-nothing アーキテクチャから、クラウドネイティブな共有ストレージアーキテクチャへの本質的な進化を表しています。shared-nothing から共有ストレージアーキテクチャへ移行することで、TiDB X は結合されたノードの物理的な制約に対処し、次の技術目標を達成します。

    - **スケーリングの高速化**: 物理データ移行の必要をなくすことで、スケーリング性能を最大 10 倍向上させます。
    - **タスク分離**: バックグラウンドのメンテナンスタスク（compaction など）とオンラインのトランザクション処理トラフィックの間で、干渉が発生しないようにします。
    - **リソースの弾力性**: コンピュートリソースがストレージ容量とは独立してスケールする、真の「pay-as-you-go」モデルを実現します。

    詳細は、[TiDB X Architecture](https://docs.pingcap.com/tidbcloud/tidb-x-architecture/?plan=premium) を参照してください。

## パフォーマンス機能 {#performance-features}

* 特定のテーブルのデータ再分散をサポートしました（実験的） [#63260](https://github.com/pingcap/tidb/issues/63260) @[bufferflies](https://github.com/bufferflies)

    PD は、クラスター内のすべての TiKV ノードに対して、データができるだけ均等に分散されるよう自動的にスケジューリングします。ただし、この自動スケジューリングはクラスター全体を対象としています。そのため、クラスター全体でのデータ分散が均衡していても、特定のテーブルのデータは TiKV ノード間で不均一に分散されている場合があります。

   これで、[`SHOW TABLE DISTRIBUTION`](https://docs.pingcap.com/tidbcloud/sql-statement-show-table-distribution/?plan=premium) ステートメントを使用して、特定のテーブルのデータがすべての TiKV ノードにどのように分散されているかを確認できます。データ分散が不均衡な場合は、[`DISTRIBUTE TABLE`](https://docs.pingcap.com/tidbcloud/sql-statement-distribute-table/?plan=premium) ステートメントを使用して、テーブルのデータを再分散（実験的）し、負荷分散を改善できます。

    特定のテーブルのデータ再分散は、タイムアウト制限のある 1 回限りのタスクであることに注意してください。分散タスクがタイムアウトまでに完了しない場合、自動的に終了します。

    詳細は、[documentation](https://docs.pingcap.com/tidbcloud/sql-statement-distribute-table/?plan=premium) を参照してください。

* DDL ステートメントに埋め込まれた `ANALYZE` をサポートしました [#57948](https://github.com/pingcap/tidb/issues/57948) @[terry1purcell](https://github.com/terry1purcell) @[AilinKid](https://github.com/AilinKid)

    この機能は、次の種類の DDL ステートメントに適用されます。

    - 新しいインデックスを作成する DDL ステートメント: [`ADD INDEX`](https://docs.pingcap.com/tidbcloud/sql-statement-add-index/?plan=premium)
    - 既存のインデックスを再編成する DDL ステートメント: [`MODIFY COLUMN`](https://docs.pingcap.com/tidbcloud/sql-statement-modify-column/?plan=premium) および [`CHANGE COLUMN`](https://docs.pingcap.com/tidbcloud/sql-statement-change-column/?plan=premium)

    この機能を有効にすると、新規または再編成されたインデックスがユーザーから見えるようになる前に、TiDB が自動的に `ANALYZE`（統計情報収集）操作を実行します。これにより、インデックス作成または再編成の直後に統計情報が一時的に利用できないことで発生する、オプティマイザの不正確な見積もりや、潜在的な実行計画の変更を防ぎます。

     詳細は、[documentation](https://docs.pingcap.com/tidbcloud/ddl_embedded_analyze/?plan=premium) を参照してください。

## 制限事項 {#limitations}

TiDB X と 従来の TiDB のアーキテクチャの違いにより、TiDB X カーネルは 従来の TiDB カーネルの次のストレージ機能をサポートしていません。

- [TiKV MVCC In-Memory Engine (IME)](https://docs.pingcap.com/tidb/v8.5/tikv-in-memory-engine)
- [Follower Read](https://docs.pingcap.com/tidb/v8.5/follower-read)

制限事項の詳細については、[Limited SQL features on TiDB X Instances](https://docs.pingcap.com/tidbcloud/limited-sql-features-tidb-x/?plan=premium) を参照してください。