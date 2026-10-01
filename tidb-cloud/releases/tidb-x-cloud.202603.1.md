---
title: TiDB-X-CLOUD.202603.1 リリースノート
summary: TiDB-X-CLOUD.202603.1 カーネルの機能について説明します。
---

# TiDB-X-CLOUD.202603.1 リリースノート

**リリース日**: 2026年7月16日

**適用対象の TiDB Cloud プラン**: {{{ .essential }}} および {{{ .premium }}}

**TiDB X カーネルバージョン**: `TiDB-X-CLOUD.202603.1`

2026年7月16日以降、新しく作成される {{{ .essential }}} および {{{ .premium }}} インスタンスのデフォルトのカーネルバージョンは `TiDB-X-CLOUD.202603.1` です。

`TiDB-X-CLOUD.202603.1` では、次のようになります。

- `202603` は、このカーネルバージョンのベースラインコードブランチが 2026年3月に作成されたことを示しており、リリース日とは異なります。
- `1` は、`TiDB-X-CLOUD.202603` ベースラインブランチからビルドされた最初のパッチリリースであることを示します。

## 機能 {#features}

### パフォーマンス {#performance}

* 特定の損失のある DDL 操作（`BIGINT → INT` や `CHAR(120) → VARCHAR(60)` など）に対して大幅なパフォーマンス改善を導入しました。データ切り捨てが発生しない場合、これらの操作の実行時間を数時間から数分、数秒、さらには数ミリ秒まで短縮でき、数十倍から数十万倍の性能向上を実現します [#63366](https://github.com/pingcap/tidb/issues/63366) @[wjhuang2016](https://github.com/wjhuang2016) @[tangenta](https://github.com/tangenta) @[fzzf678](https://github.com/fzzf678) <!-- pr: https://github.com/pingcap/tidb/pull/64834, https://github.com/pingcap/tidb/pull/64337, https://github.com/pingcap/tidb/pull/64188, https://github.com/pingcap/tidb/pull/64111, https://github.com/pingcap/tidb/pull/63465, https://github.com/pingcap/tidb/pull/63970, https://github.com/pingcap/tidb/pull/63965 -->

    最適化戦略は次のとおりです。

    - 厳密な SQL モードでは、TiDB は型変換時の潜在的なデータ切り捨てリスクを事前チェックします。
    - データ切り捨てリスクが検出されない場合、TiDB はメタデータのみを更新し、可能な限りインデックスの再構築を回避します。
    - インデックスの再構築が必要な場合、TiDB はより効率的な取り込みプロセスを使用して、インデックス再構築のパフォーマンスを大幅に向上させます。

  次の表は、114 GiB のデータと 6 億行を持つテーブルに対するベンチマークテストに基づく性能改善の例を示しています。テストクラスターは 3 台の TiDB ノード、6 台の TiKV ノード、1 台の PD ノードで構成されています。すべてのノードは 16 CPU コアと 32 GiB のメモリで構成されています。

    | シナリオ | 操作タイプ | 最適化前 | 最適化後 | 性能改善 |
    |----------|----------------|---------------------|--------------------|--------------------------|
    | インデックスなしカラム | `BIGINT → INT` | 2時間34分 | 1分5秒 | 142倍高速 |
    | インデックス付きカラム | `BIGINT → INT` | 6時間25分 | 0.05秒 | 460,000倍高速 |
    | インデックス付きカラム | `CHAR(120) → VARCHAR(60)` | 7時間16分 | 12分56秒 | 34倍高速 |

    上記のテスト結果は、DDL 実行中にデータ切り捨てが発生しないことを前提としています。これらの最適化は、符号付き整数型と符号なし整数型の間の変換、文字セット間の変換、または TiFlash レプリカを持つテーブルには適用されません。

    詳細は、[ドキュメント](https://docs.pingcap.com/tidbcloud/sql-statement-modify-column/?plan=premium)を参照してください。

### 可観測性 {#observability}

* スロークエリに対して、多次元かつきめ細かなトリガールールの定義をサポートしました [#62959](https://github.com/pingcap/tidb/issues/62959) [#64010](https://github.com/pingcap/tidb/issues/64010) @[zimulala](https://github.com/zimulala) <!-- pr: https://github.com/pingcap/tidb/pull/66132, https://github.com/pingcap/tidb/pull/66064, https://github.com/pingcap/tidb/pull/65086 -->

    TiDB Cloud では、デフォルトで 300 ミリ秒を超える SQL クエリがスロークエリと見なされます。スロークエリは、[TiDB Cloud コンソール](https://tidbcloud.com/)の [**Diagnosis**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page) ページにある [**Slow Query**](/tidb-cloud/tune-performance.md#slow-query) タブで確認できます。

    TiDB Cloud では、スロークエリログの出力をより柔軟に制御できるようになりました。[`tidb_slow_log_rules`](https://docs.pingcap.com/tidbcloud/system-variables/?plan=premium#tidb_slow_log_rules) システム変数を使用すると、`Query_time`、`Digest`、`Mem_max`、`KV_total` などの条件に基づいて、セッションレベルおよび SQL レベルで多次元のスロークエリログ出力ルールを定義できます。`WRITE_SLOW_LOG` ヒントを使用すると、特定の SQL 文に対してスロークエリログ出力を強制できます。これにより、スロークエリログをより柔軟かつきめ細かく制御できます。

    詳細は、[ドキュメント](https://docs.pingcap.com/tidbcloud/config-slow-query-trigger-rules/?plan=premium)を参照してください。

### SQL {#sql}

* `FOR UPDATE OF` 句でのテーブルエイリアスの使用をサポートしました [#63035](https://github.com/pingcap/tidb/issues/63035) @[cryo-zd](https://github.com/cryo-zd) <!-- pr: https://github.com/pingcap/tidb/pull/65532 -->

    このリリース以前は、`SELECT ... FOR UPDATE OF <table>` 文のロック句でテーブルエイリアスを参照すると、TiDB がそのエイリアスを正しく解決できず、エイリアスが有効であっても `table not exists` エラーを返すことがありました。

    TiDB は `FOR UPDATE OF` 句でのテーブルエイリアスの使用をサポートします。TiDB は、エイリアス付きテーブルを含む `FROM` 句からロック対象を正しく解決できるようになり、行ロックが期待どおりに有効になります。これにより、MySQL 互換性が向上し、テーブルエイリアスを使用するクエリにおける `SELECT ... FOR UPDATE OF` 文の安定性と信頼性が高まります。

    詳細は、[ドキュメント](https://docs.pingcap.com/tidbcloud/sql-statement-select/?plan=premium)を参照してください。

* インデックスストレージと DML メンテナンスのオーバーヘッドを削減する 部分インデックス をサポートしました [#62664](https://github.com/pingcap/tidb/issues/62664) [#62761](https://github.com/pingcap/tidb/issues/62761) [#62758](https://github.com/pingcap/tidb/issues/62758) [#63447](https://github.com/pingcap/tidb/issues/63447) [#64344](https://github.com/pingcap/tidb/issues/64344) @[YangKeao](https://github.com/YangKeao) @[winoros](https://github.com/winoros) @[wjhuang2016](https://github.com/wjhuang2016) <!-- pr: https://github.com/pingcap/tidb/pull/64434, https://github.com/pingcap/tidb/pull/62762, https://github.com/pingcap/tidb/pull/62759, https://github.com/pingcap/tidb/pull/65051 -->

    TiDB は 部分インデックス をサポートするようになりました。部分インデックス は、インデックスの `WHERE` 句で定義された述語を満たす行だけをインデックス化します。部分インデックス は、`CREATE INDEX ... WHERE ...`、`ALTER TABLE ... ADD INDEX ... WHERE ...`、または `CREATE TABLE` 内のインデックス定義を使用して作成できます。

    部分インデックス は、特定の条件に基づく行のサブセットを頻繁にクエリする場合や、特定の条件下でのみ適用される一意制約が必要な場合に有用です。述語の対象外となる行はインデックスに書き込まれないため、部分インデックス はインデックスストレージの削減に役立ち、`INSERT`、`UPDATE`、`DELETE` 操作時のインデックスメンテナンスのオーバーヘッドも低減できます。

    部分インデックス を効果的に使用するには、一般的なクエリのフィルターに一致する述語を定義してください。TiDB は、クエリ述語が 部分インデックス の述語に一致するか、それを含意する場合にのみ 部分インデックス を選択します。現在、部分インデックス の述語では、基本的な比較演算子（`=`, `!=`, `<`, `<=`, `>`, `>=`）、`IS NULL`、`IS NOT NULL`、および定数値を使った `IN` 述語をサポートしています。

    詳細は、[ドキュメント](https://docs.pingcap.com/tidbcloud/sql-statement-create-index/?plan=premium#partial-indexes)を参照してください。

## 互換性の変更 {#compatibility-changes}

### MySQL 互換性 {#mysql-compatibility}

* Dumpling は、更新された MySQL バイナリログ命名に対応することで、MySQL 8.4 からのデータエクスポートをサポートします。[#53082](https://github.com/pingcap/tidb/issues/53082) @[dveeden](https://github.com/dveeden) <!-- pr: https://github.com/pingcap/tidb/pull/66704 -->

## 改善 {#improvements}

- Parquet ファイルの解析メカニズムを強化し、Parquet 形式データのインポート性能を向上させました [#62906](https://github.com/pingcap/tidb/issues/62906) @[joechenrh](https://github.com/joechenrh) <!-- pr: https://github.com/pingcap/tidb/pull/66564, https://github.com/pingcap/tidb/pull/63979 -->
- `tidb_analyze_column_options` のデフォルト値を `ALL` に変更し、デフォルトで全カラムの統計情報を収集するようにしました [#64992](https://github.com/pingcap/tidb/issues/64992) @[0xPoe](https://github.com/0xPoe) <!-- pr: https://github.com/pingcap/tidb/pull/65020, https://github.com/pingcap/tidb/pull/64994 -->
- 特定の JOIN シナリオで増分処理を使用することで `IndexHashJoin` 演算子の実行ロジックを最適化し、一度に大量のデータをロードすることを回避して、メモリ使用量を大幅に削減し、パフォーマンスを向上させました [#63303](https://github.com/pingcap/tidb/issues/63303) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan) <!-- pr: https://github.com/pingcap/tidb/pull/63723 -->
- グローバルシステム変数 `tidb_enable_batch_query_region` を追加し、TiDB が PD に対してバッチ化されたリージョン問い合わせを使用するかどうかを制御できるようにしました。これにより、リージョン情報取得の効率が向上します。この変数はデフォルトで無効です [#58439](https://github.com/pingcap/tidb/issues/58439) [#8690](https://github.com/tikv/pd/issues/8690) @[JmPotato](https://github.com/JmPotato) <!-- pr: https://github.com/tikv/pd/pull/10139, https://github.com/tikv/pd/pull/10105 -->
- コスト見積もりの前に無関係なインデックスをプルーニングすることで、多数のインデックスを持つテーブルに対するクエリのオプティマイザ性能を向上させ、クエリ計画時間を短縮し、不要な全範囲の範囲外見積もりを回避します [#63856](https://github.com/pingcap/tidb/issues/63856) @[terry1purcell](https://github.com/terry1purcell) @[qw4990](https://github.com/qw4990) <!-- pr: https://github.com/pingcap/tidb/pull/66304, https://github.com/pingcap/tidb/pull/65854, https://github.com/pingcap/tidb/pull/64999, https://github.com/pingcap/tidb/pull/64794, https://github.com/pingcap/tidb/pull/64675, https://github.com/pingcap/tidb/pull/64484, https://github.com/pingcap/tidb/pull/64115, https://github.com/pingcap/tidb/pull/64053, https://github.com/pingcap/tidb/pull/64086, https://github.com/pingcap/tidb/pull/64054 -->
- 一致するプレフィックスインデックス上の `ORDER BY ... LIMIT/OFFSET` クエリに対する 部分順序付きインデックス最適化をサポートしました。`tidb_opt_partial_ordered_index_for_topn` を `COST` に設定すると、TiDB はインデックスの部分順序性を利用してフルテーブルスキャンを削減し、`TOPN` クエリのパフォーマンスを向上できます [#63280](https://github.com/pingcap/tidb/issues/63280) [#65813](https://github.com/pingcap/tidb/issues/65813) [#66338](https://github.com/pingcap/tidb/issues/66338) @[elsa0520](https://github.com/elsa0520) @[xzhangxian1008](https://github.com/xzhangxian1008) @[winoros](https://github.com/winoros) <!-- pr: https://github.com/pingcap/tidb/pull/65314, https://github.com/pingcap/tidb/pull/66268, https://github.com/pingcap/tidb/pull/66181, https://github.com/pingcap/tidb/pull/65799, https://github.com/pingcap/tidb/pull/65533 -->
- ローカルインデックスを持つ高度にパーティション化されたテーブル上の `IndexLookUp` クエリにおけるコプロセッサーリクエストのバーストを緩和し、クエリの安定性を向上させ、性能スパイクを低減しました [#67545](https://github.com/pingcap/tidb/issues/67545) @[gengliqi](https://github.com/gengliqi) <!-- pr: https://github.com/pingcap/tidb/pull/69334 -->
- 実行中の不要な式バッファ割り当てを削減することで、`INSERT ... ON DUPLICATE KEY UPDATE` 文の CPU およびメモリ使用量を最適化しました [#65003](https://github.com/pingcap/tidb/issues/65003) @[windtalker](https://github.com/windtalker) <!-- pr: https://github.com/pingcap/tidb/pull/65244 -->
- タイムスタンプ進行および Leader 選出のロジックを最適化しました [#9981](https://github.com/tikv/pd/issues/9981) @[bufferflies](https://github.com/bufferflies) <!-- pr: https://github.com/tikv/pd/pull/9986 -->
