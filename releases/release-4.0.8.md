---
title: TiDB 4.0.8 Release Notes
---

# TiDB4.0.8リリースノート {#tidb-4-0-8-release-notes}

発売日：2020年10月30日

TiDBバージョン：4.0.8

## 新機能 {#new-features}

-   TiDB

    -   新しい集計関数をサポートする`APPROX_PERCENTILE` [＃20197](https://github.com/pingcap/tidb/pull/20197)

-   TiFlash

    -   `CAST`の関数のプッシュダウンをサポート

-   ツール

    -   TiCDC

        -   スナップショットレベルの一貫したレプリケーションをサポートする[＃932](https://github.com/pingcap/tiflow/pull/932)

## 改善点 {#improvements}

-   TiDB

    -   `Selectivity()` [＃20154](https://github.com/pingcap/tidb/pull/20154)の欲張り検索手順では、選択性の低いインデックスを優先します。
    -   コプロセッサーランタイム統計にRPCランタイム情報をさらに記録する[＃19264](https://github.com/pingcap/tidb/pull/19264)
    -   遅いログの解析を高速化して、クエリのパフォーマンスを向上させます[＃20556](https://github.com/pingcap/tidb/pull/20556)
    -   SQLオプティマイザーが潜在的な新しいプランを検証しているときに、プランのバインド段階でタイムアウト実行プランを待機して、より多くのデバッグ情報を記録します[＃20530](https://github.com/pingcap/tidb/pull/20530)
    -   遅いログと遅いクエリ結果に実行再試行時間を追加し[＃20494](https://github.com/pingcap/tidb/pull/20494) [＃20495](https://github.com/pingcap/tidb/pull/20495)
    -   `table_storage_stats`のシステムテーブルを追加します[＃20431](https://github.com/pingcap/tidb/pull/20431)
    -   `INSERT`ステートメントの[＃20430](https://github.com/pingcap/tidb/pull/20430)ランタイム統計情報を追加し`UPDATE` `REPLACE`
    -   [＃20384](https://github.com/pingcap/tidb/pull/20384)の結果にオペレーター情報を追加し`EXPLAIN FOR CONNECTION`
    -   クライアント接続/切断アクティビティのTiDBエラーログを`DEBUG`レベルに調整します[＃20321](https://github.com/pingcap/tidb/pull/20321)
    -   コプロセッサーキャッシュ[＃20293](https://github.com/pingcap/tidb/pull/20293)の監視メトリックを追加します
    -   ペシミスティックロックキーの実行時情報を追加する[＃20199](https://github.com/pingcap/tidb/pull/20199)
    -   ランタイム情報と`trace`スパン[＃20187](https://github.com/pingcap/tidb/pull/20187)に時間消費情報の2つのセクションを追加します。
    -   遅いログにトランザクションコミットの実行時情報を追加します[＃20185](https://github.com/pingcap/tidb/pull/20185)
    -   インデックスマージ結合を無効にする[＃20599](https://github.com/pingcap/tidb/pull/20599)
    -   一時的な文字列リテラルのISO8601とタイムゾーンのサポートを追加します[＃20670](https://github.com/pingcap/tidb/pull/20670)

-   TiKV

    -   **Fast-Tune**パネルページを追加して、パフォーマンス診断を支援します[＃8804](https://github.com/tikv/tikv/pull/8804)
    -   ログ[＃8746](https://github.com/tikv/tikv/pull/8746)からユーザーデータを編集する`security.redact-info-log`の構成アイテムを追加します。
    -   エラーコードのメタファイルを再フォーマットする[＃8877](https://github.com/tikv/tikv/pull/8877)
    -   `pessimistic-txn.pipelined`構成の動的変更を有効にする[＃8853](https://github.com/tikv/tikv/pull/8853)
    -   デフォルトでメモリプロファイリング機能を有効にする[＃8801](https://github.com/tikv/tikv/pull/8801)

-   PD

    -   エラーのメタファイルを生成する[＃3090](https://github.com/pingcap/pd/pull/3090)
    -   オペレーター[＃3009](https://github.com/pingcap/pd/pull/3009)の追加情報を追加します

-   TiFlash

    -   Raftログの監視メトリックを追加します
    -   `cop`のタスクのメモリ使用量の監視メトリックを追加します
    -   データが削除されたときに`min` `max`をより正確にする
    -   データ量が少ない場合のクエリパフォーマンスの向上
    -   標準エラーコードをサポートするために`errors.toml`のファイルを追加します

-   ツール

    -   バックアップと復元（BR）

        -   `split`と[＃427](https://github.com/pingcap/br/pull/427)をパイプライン化することにより、復元プロセスを高速化し`ingest` 。
        -   PDスケジューラの手動復元のサポート[＃530](https://github.com/pingcap/br/pull/530)
        -   `remove`のスケジューラーの代わりに`pause`のスケジューラーを使用する[＃551](https://github.com/pingcap/br/pull/551)

    -   TiCDC

        -   MySQLシンクで統計を定期的に出力する[＃1023](https://github.com/pingcap/tiflow/pull/1023)

    -   Dumpling

        -   S3ストレージへのデータの直接ダンプリングをサポート[＃155](https://github.com/pingcap/dumpling/pull/155)
        -   ビューのダンプをサポート[＃158](https://github.com/pingcap/dumpling/pull/158)
        -   生成された列のみを含むテーブルのダンプをサポート[＃166](https://github.com/pingcap/dumpling/pull/166)

    -   TiDB Lightning

        -   マルチバイトCSV区切り文字と区切り文字をサポート[＃406](https://github.com/pingcap/tidb-lightning/pull/406)
        -   一部のPDスケジューラーを無効にすることにより、復元プロセスを高速化します[＃408](https://github.com/pingcap/tidb-lightning/pull/408)
        -   GCエラーを回避するためにv4.0クラスタのチェックサムGCセーフポイントにGC-TTLAPIを使用する[＃396](https://github.com/pingcap/tidb-lightning/pull/396)

## バグの修正 {#bug-fixes}

-   TiDB

    -   パーティションテーブルの使用時に発生する予期しないpanicを修正する[＃20565](https://github.com/pingcap/tidb/pull/20565)
    -   インデックスマージ結合[＃20427](https://github.com/pingcap/tidb/pull/20427)を使用して外側をフィルタリングするときの外側結合の誤った結果を修正しました
    -   データが長すぎる場合にデータを`BIT`タイプに変換すると、 `NULL`の値が返される問題を修正します[＃20363](https://github.com/pingcap/tidb/pull/20363)
    -   `BIT`タイプの列[＃20340](https://github.com/pingcap/tidb/pull/20340)の破損したデフォルト値を修正します
    -   `BIT`タイプを`INT64`タイプ[＃20312](https://github.com/pingcap/tidb/pull/20312)に変換するときに発生する可能性のあるオーバーフローエラーを修正します
    -   ハイブリッドタイプの列[＃20297](https://github.com/pingcap/tidb/pull/20297)の伝播列の最適化で発生する可能性のある誤った結果を修正します。
    -   プランキャッシュから古いプランを保存するときに発生する可能性のあるpanicを修正する[＃20246](https://github.com/pingcap/tidb/pull/20246)
    -   `FROM_UNIXTIME`と`UNION ALL`を一緒に使用すると、返される結果が誤って切り捨てられるバグを修正します[＃20240](https://github.com/pingcap/tidb/pull/20240)
    -   `Enum`タイプの値を`Float`タイプ[＃20235](https://github.com/pingcap/tidb/pull/20235)に変換すると、間違った結果が返される可能性がある問題を修正します。
    -   [＃20210](https://github.com/pingcap/tidb/pull/20210)の考えられるpanicを修正し`RegionStore.accessStore`
    -   最大符号なし整数を`BatchPointGet`でソートするときに返される間違った結果を修正し[＃20205](https://github.com/pingcap/tidb/pull/20205)
    -   `Enum`と`Set`の強制力が間違っているというバグを修正します[＃20364](https://github.com/pingcap/tidb/pull/20364)
    -   あいまいな`YEAR`変換[＃20292](https://github.com/pingcap/tidb/pull/20292)の問題を修正します
    -   **KV期間**パネルに[＃20260](https://github.com/pingcap/tidb/pull/20260)が含まれている場合に発生する誤った報告結果の問題を修正し`store0`
    -   `out of range`エラー[＃20252](https://github.com/pingcap/tidb/pull/20252)に関係なく、 `Float`タイプのデータが誤って挿入される問題を修正します。
    -   生成された列が不正な`NULL`値を処理しないというバグを修正します[＃20216](https://github.com/pingcap/tidb/pull/20216)
    -   範囲[＃20170](https://github.com/pingcap/tidb/pull/20170)外の`YEAR`タイプのデータの不正確なエラー情報を修正します
    -   悲観的なトランザクションの再試行中に発生する可能性のある予期しない`invalid auto-id`エラーを修正します[＃20134](https://github.com/pingcap/tidb/pull/20134)
    -   `ALTER TABLE`を使用して`Enum`タイプ`Set`を変更すると、制約がチェックされない問題を修正し[＃20046](https://github.com/pingcap/tidb/pull/20046) 。
    -   並行性[＃19947](https://github.com/pingcap/tidb/pull/19947)に複数の演算子が使用されている場合に記録される`cop`のタスクの誤ったランタイム情報を修正します
    -   読み取り専用のシステム変数をセッション変数として明示的に選択できない問題を修正します[＃19944](https://github.com/pingcap/tidb/pull/19944)
    -   重複`ORDER BY`条件が次善の実行プラン[＃20333](https://github.com/pingcap/tidb/pull/20333)を引き起こす可能性があるという問題を修正します
    -   フォントサイズが最大許容値を超えると、生成されたメトリックプロファイルが失敗する可能性がある問題を修正します[＃20637](https://github.com/pingcap/tidb/pull/20637)

-   TiKV

    -   暗号化におけるミューテックスの競合により、pd-workerがハートビートをゆっくり処理するバグを修正します[＃8869](https://github.com/tikv/tikv/pull/8869)
    -   メモリプロファイルが誤って生成される問題を修正します[＃8790](https://github.com/tikv/tikv/pull/8790)
    -   ストレージクラスが指定されている場合にGCSでデータベースをバックアップできない問題を修正[＃8763](https://github.com/tikv/tikv/pull/8763)
    -   リージョンが再起動または新たに分割されたときに学習者がリーダーを見つけることができないバグを修正します[＃8864](https://github.com/tikv/tikv/pull/8864)

-   PD

    -   TiDBダッシュボードのキービジュアライザーが場合によってはPDpanicを引き起こす可能性があるバグを修正します[＃3096](https://github.com/pingcap/pd/pull/3096)
    -   PDストアが10分以上ダウンした場合にPDがpanicになる可能性があるバグを修正します[＃3069](https://github.com/pingcap/pd/pull/3069)

-   TiFlash

    -   ログメッセージの誤ったタイムスタンプの問題を修正します
    -   マルチディスクTiFlashの展開中に、容量が間違っているとTiFlashレプリカの作成が失敗する問題を修正します
    -   再起動後にTiFlashが壊れたデータファイルに関するエラーをスローする可能性があるバグを修正します
    -   TiFlashがクラッシュした後、壊れたファイルがディスクに残る可能性がある問題を修正します
    -   プロキシが最新のRaftリース情報に追いつかない場合、学習者の読み取り中にインデックスを待機するのに長い時間がかかる可能性があるバグを修正します
    -   古いRaftログの再生中に、プロキシがキー値エンジンに大量のリージョン状態情報を書き込むバグを修正しました

-   ツール

    -   バックアップと復元（BR）

        -   復元中の`send on closed channel`のpanicを修正[＃559](https://github.com/pingcap/br/pull/559)

    -   TiCDC

        -   GCセーフポイント[＃979](https://github.com/pingcap/tiflow/pull/979)の更新の失敗によって引き起こされた予期しない終了を修正します
        -   modリビジョンキャッシュが正しくないためにタスクステータスが予期せずフラッシュされる問題を修正します[＃1017](https://github.com/pingcap/tiflow/pull/1017)
        -   予期しない空のMaxwellメッセージを修正する[＃978](https://github.com/pingcap/tiflow/pull/978)

    -   TiDB Lightning

        -   間違った列情報の問題を修正する[＃420](https://github.com/pingcap/tidb-lightning/pull/420)
        -   ローカルモードでリージョン情報の取得を再試行するときに発生する無限ループを修正します[＃418](https://github.com/pingcap/tidb-lightning/pull/418)
