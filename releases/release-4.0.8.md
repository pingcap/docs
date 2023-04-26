---
title: TiDB 4.0.8 Release Notes
---

# TiDB 4.0.8 リリースノート {#tidb-4-0-8-release-notes}

発売日：2020年10月30日

TiDB バージョン: 4.0.8

## 新機能 {#new-features}

-   TiDB

    -   新しい集約関数のサポート`APPROX_PERCENTILE` [#20197](https://github.com/pingcap/tidb/pull/20197)

-   TiFlash

    -   `CAST`関数を押し下げるサポート

-   ツール

    -   TiCDC

        -   スナップショット レベルの一貫性のあるレプリケーションのサポート[#932](https://github.com/pingcap/tiflow/pull/932)

## 改良点 {#improvements}

-   TiDB

    -   `Selectivity()` [#20154](https://github.com/pingcap/tidb/pull/20154)の貪欲な検索手順で選択性の低いインデックスを優先する
    -   コプロセッサーのランタイム統計[#19264](https://github.com/pingcap/tidb/pull/19264)に、より多くの RPC ランタイム情報を記録します。
    -   遅いログの解析を高速化して、クエリのパフォーマンスを向上させる[#20556](https://github.com/pingcap/tidb/pull/20556)
    -   SQL オプティマイザが潜在的な新しい計画を検証しているときに、より多くのデバッグ情報を記録するために、計画のバインド段階でタイムアウト実行計画を待ちます[#20530](https://github.com/pingcap/tidb/pull/20530)
    -   スロー ログの実行リトライ時間とスロー クエリの結果を加算します。 [#20495](https://github.com/pingcap/tidb/pull/20495) [#20494](https://github.com/pingcap/tidb/pull/20494)
    -   `table_storage_stats`システム テーブル[#20431](https://github.com/pingcap/tidb/pull/20431)を追加します。
    -   `INSERT` / `UPDATE` / `REPLACE`ステートメントの RPC ランタイム統計情報を追加します[#20430](https://github.com/pingcap/tidb/pull/20430)
    -   `EXPLAIN FOR CONNECTION` [#20384](https://github.com/pingcap/tidb/pull/20384)の結果にオペレーター情報を追加します
    -   TiDB エラー ログを、クライアントの接続/切断アクティビティのレベル`DEBUG`に調整します[#20321](https://github.com/pingcap/tidb/pull/20321)
    -   コプロセッサー・キャッシュ[#20293](https://github.com/pingcap/tidb/pull/20293)のモニター・メトリックを追加します
    -   悲観的ロックキーのランタイム情報を追加[#20199](https://github.com/pingcap/tidb/pull/20199)
    -   ランタイム情報に時間消費情報のセクションを 2 つ追加し、スパン[#20187](https://github.com/pingcap/tidb/pull/20187)を`trace`追加します。
    -   トランザクション コミットのランタイム情報をスロー ログ[#20185](https://github.com/pingcap/tidb/pull/20185)に追加します。
    -   インデックス マージ結合を無効にする[#20599](https://github.com/pingcap/tidb/pull/20599)
    -   ISO 8601 および一時文字列リテラルのタイムゾーン サポートを追加します[#20670](https://github.com/pingcap/tidb/pull/20670)

-   TiKV

    -   **Fast-Tune**パネル ページを追加して、パフォーマンス診断を支援します[#8804](https://github.com/tikv/tikv/pull/8804)
    -   ログ[#8746](https://github.com/tikv/tikv/pull/8746)からユーザー データをリダクションする`security.redact-info-log`構成項目を追加します。
    -   エラー コード[#8877](https://github.com/tikv/tikv/pull/8877)のメタファイルを再フォーマットします。
    -   `pessimistic-txn.pipelined`構成の動的変更を有効にする[#8853](https://github.com/tikv/tikv/pull/8853)
    -   デフォルトでメモリプロファイリング機能を有効にする[#8801](https://github.com/tikv/tikv/pull/8801)

-   PD

    -   エラーのメタファイルを生成します[#3090](https://github.com/pingcap/pd/pull/3090)
    -   オペレーター[#3009](https://github.com/pingcap/pd/pull/3009)の追加情報を追加します。

-   TiFlash

    -   Raftログの監視メトリクスを追加
    -   `cop`タスクのメモリ使用量の監視メトリクスを追加
    -   データ削除時の`min`指数`max`より正確にする
    -   データ量が少ない場合のクエリ パフォーマンスの向上
    -   標準エラー コードをサポートする`errors.toml`ファイルを追加します。

-   ツール

    -   バックアップと復元 (BR)

        -   `split`と`ingest` [#427](https://github.com/pingcap/br/pull/427)をパイプライン処理して復元プロセスを高速化する
        -   PD スケジューラの手動復元をサポート[#530](https://github.com/pingcap/br/pull/530)
        -   `remove`スケジューラの代わりに`pause`スケジューラを使用する[#551](https://github.com/pingcap/br/pull/551)

    -   TiCDC

        -   MySQL シンクの統計を定期的に出力する[#1023](https://github.com/pingcap/tiflow/pull/1023)

    -   Dumpling

        -   データのダンプリングを S3 ストレージに直接サポート[#155](https://github.com/pingcap/dumpling/pull/155)
        -   ビューのダンプをサポート[#158](https://github.com/pingcap/dumpling/pull/158)
        -   生成された列のみを含むテーブルのダンプをサポート[#166](https://github.com/pingcap/dumpling/pull/166)

    -   TiDB Lightning

        -   マルチバイトの CSV 区切り文字と区切り文字をサポート[#406](https://github.com/pingcap/tidb-lightning/pull/406)
        -   一部の PD スケジューラを無効にして復元プロセスを高速化する[#408](https://github.com/pingcap/tidb-lightning/pull/408)
        -   v4.0 クラスターでチェックサム GC セーフポイントに GC-TTL API を使用して、GC エラー[#396](https://github.com/pingcap/tidb-lightning/pull/396)を回避します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   パーティション化されたテーブルを使用するときに発生する予期しないpanicを修正します[#20565](https://github.com/pingcap/tidb/pull/20565)
    -   インデックス マージ ジョイン[#20427](https://github.com/pingcap/tidb/pull/20427)を使用してアウター サイドをフィルター処理すると、アウター ジョインの誤った結果が返される問題を修正
    -   データが長すぎる場合、データを`BIT`型に変換すると`NULL`値が返される問題を修正[#20363](https://github.com/pingcap/tidb/pull/20363)
    -   `BIT`型列[#20340](https://github.com/pingcap/tidb/pull/20340)の破損した既定値を修正します。
    -   `BIT`型を`INT64`型に変換する際に発生する可能性があったオーバーフローエラーを修正[#20312](https://github.com/pingcap/tidb/pull/20312)
    -   ハイブリッド型列[#20297](https://github.com/pingcap/tidb/pull/20297)の列最適化の伝播で発生する可能性のある間違った結果を修正します。
    -   プラン キャッシュ[#20246](https://github.com/pingcap/tidb/pull/20246)から古いプランを保存するときに発生する可能性があるpanicを修正します。
    -   `FROM_UNIXTIME`と`UNION ALL`を併用すると返ってくる結果が誤って切り捨てられる不具合を修正[#20240](https://github.com/pingcap/tidb/pull/20240)
    -   `Enum`型の値を`Float`型[#20235](https://github.com/pingcap/tidb/pull/20235)に変換すると間違った結果が返される場合がある問題を修正
    -   `RegionStore.accessStore` [#20210](https://github.com/pingcap/tidb/pull/20210)のpanicの可能性を修正
    -   最大符号なし整数を`BatchPointGet` [#20205](https://github.com/pingcap/tidb/pull/20205)でソートしたときに返される間違った結果を修正
    -   `Enum`と`Set`の保磁力が違うバグを修正[#20364](https://github.com/pingcap/tidb/pull/20364)
    -   あいまいな`YEAR`変換[#20292](https://github.com/pingcap/tidb/pull/20292)の問題を修正します。
    -   **KV 持続時間**パネルに`store0` [#20260](https://github.com/pingcap/tidb/pull/20260)含まれている場合に発生する間違ったレポート結果の問題を修正します。
    -   `out of range`エラー[#20252](https://github.com/pingcap/tidb/pull/20252)にもかかわらず`Float`型データが誤って挿入される問題を修正
    -   生成された列が不正な`NULL`値を処理しないバグを修正[#20216](https://github.com/pingcap/tidb/pull/20216)
    -   範囲外の`YEAR`型データの不正確なエラー情報を修正[#20170](https://github.com/pingcap/tidb/pull/20170)
    -   悲観的トランザクションの再試行中に発生する可能性がある予期しない`invalid auto-id`エラーを修正します[#20134](https://github.com/pingcap/tidb/pull/20134)
    -   `ALTER TABLE`を使用して`Enum` / `Set`タイプ[#20046](https://github.com/pingcap/tidb/pull/20046)を変更すると、制約がチェックされない問題を修正します。
    -   同時実行に複数のオペレーターが使用されている場合に記録される`cop`タスクの間違ったランタイム情報を修正します[#19947](https://github.com/pingcap/tidb/pull/19947)
    -   読み取り専用のシステム変数をセッション変数として明示的に選択できない問題を修正します[#19944](https://github.com/pingcap/tidb/pull/19944)
    -   重複`ORDER BY`条件が最適でない実行計画を引き起こす可能性があるという問題を修正します[#20333](https://github.com/pingcap/tidb/pull/20333)
    -   フォント サイズが最大許容値[#20637](https://github.com/pingcap/tidb/pull/20637)を超えると、生成されたメトリック プロファイルが失敗する可能性があるという問題を修正します。

-   TiKV

    -   暗号化におけるミューテックスの競合により、pd-worker のハートビートの処理が遅くなるというバグを修正します[#8869](https://github.com/tikv/tikv/pull/8869)
    -   メモリプロファイルが誤って生成される問題を修正[#8790](https://github.com/tikv/tikv/pull/8790)
    -   storageクラスが[#8763](https://github.com/tikv/tikv/pull/8763)に指定されている場合に、GCS でデータベースをバックアップできない問題を修正しました。
    -   リージョンが再起動または新しく分割されたときに、学習者がリーダーを見つけられないバグを修正します[#8864](https://github.com/tikv/tikv/pull/8864)

-   PD

    -   TiDB ダッシュボードの Key Visualizer が PDpanicを引き起こす場合があるバグを修正[#3096](https://github.com/pingcap/pd/pull/3096)
    -   PD ストアが 10 分以上ダウンした場合に PD がpanicになる可能性があるバグを修正します[#3069](https://github.com/pingcap/pd/pull/3069)

-   TiFlash

    -   ログ メッセージの間違ったタイムスタンプの問題を修正
    -   マルチディスクTiFlashの展開中に、間違った容量が原因でTiFlashレプリカの作成が失敗する問題を修正します。
    -   TiFlash が再起動後に破損したデータ ファイルに関するエラーをスローする可能性があるバグを修正します。
    -   TiFlash がクラッシュした後、壊れたファイルがディスクに残る可能性がある問題を修正します。
    -   プロキシが最新のRaftリース情報に追いつかない場合、学習者の読み取り中にインデックスの待機に時間がかかることがあるというバグを修正します
    -   古くなったRaftログを再生しているときに、プロキシが Key-Value エンジンに過剰なリージョン状態情報を書き込むバグを修正

-   ツール

    -   バックアップと復元 (BR)

        -   `send on closed channel`復元中のpanicを修正[#559](https://github.com/pingcap/br/pull/559)

    -   TiCDC

        -   GC セーフポイント[#979](https://github.com/pingcap/tiflow/pull/979)の更新に失敗したために発生した予期しない終了を修正します。
        -   mod リビジョン キャッシュが正しくないため、タスク ステータスが予期せずフラッシュされる問題を修正します[#1017](https://github.com/pingcap/tiflow/pull/1017)
        -   予期しない空の Maxwell メッセージを修正する[#978](https://github.com/pingcap/tiflow/pull/978)

    -   TiDB Lightning

        -   間違った列情報の問題を修正します[#420](https://github.com/pingcap/tidb-lightning/pull/420)
        -   ローカルモード[#418](https://github.com/pingcap/tidb-lightning/pull/418)でリージョン情報の取得を再試行するときに発生する無限ループを修正します。
