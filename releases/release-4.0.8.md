---
title: TiDB 4.0.8 Release Notes
summary: TiDB 4.0.8は2020年10月30日にリリースされました。新機能には、新しい集計関数「APPROX_PERCENTILE」のサポートと、 TiFlashにおける「CAST」関数のプッシュダウンが含まれます。TiDB、TiKV、PD、 TiFlashの機能強化に加え、TiDB、TiKV、PD、 TiFlash、バックアップとリストア（BR）、TiCDC、 TiDB Lightningのバグ修正も実装されました。
---

# TiDB 4.0.8 リリースノート {#tidb-4-0-8-release-notes}

発売日：2020年10月30日

TiDB バージョン: 4.0.8

## 新機能 {#new-features}

-   TiDB

    -   新しい集計関数`APPROX_PERCENTILE` [＃20197](https://github.com/pingcap/tidb/pull/20197)をサポート

-   TiFlash

    -   `CAST`関数を押し下げるサポート

-   ツール

    -   TiCDC

        -   スナップショットレベルの一貫性のあるレプリケーションをサポート[＃932](https://github.com/pingcap/tiflow/pull/932)

## 改善点 {#improvements}

-   TiDB

    -   `Selectivity()` [＃20154](https://github.com/pingcap/tidb/pull/20154)の貪欲探索手順で選択性の低いインデックスを優先する
    -   コプロセッサー実行時統計[＃19264](https://github.com/pingcap/tidb/pull/19264)にRPC実行時情報をさらに記録します。
    -   スローログの解析を高速化してクエリパフォーマンスを向上させる[＃20556](https://github.com/pingcap/tidb/pull/20556)
    -   SQL オプティマイザが潜在的な新しいプランを検証しているときに、より多くのデバッグ情報を記録するために、プラン バインディング ステージ中にタイムアウト実行プランを待機します[＃20530](https://github.com/pingcap/tidb/pull/20530)
    -   スローログに実行再試行時間を追加し、スロークエリの結果[＃20495](https://github.com/pingcap/tidb/pull/20495) [＃20494](https://github.com/pingcap/tidb/pull/20494)
    -   `table_storage_stats`システムテーブル[＃20431](https://github.com/pingcap/tidb/pull/20431)を追加する
    -   `INSERT` `REPLACE`のRPC実行時統計情報`UPDATE`追加する[＃20430](https://github.com/pingcap/tidb/pull/20430)
    -   `EXPLAIN FOR CONNECTION` [＃20384](https://github.com/pingcap/tidb/pull/20384)の結果に演算子情報を追加します
    -   クライアントの接続/切断アクティビティ[＃20321](https://github.com/pingcap/tidb/pull/20321)のTiDBエラーログを`DEBUG`レベルに調整します。
    -   コプロセッサーキャッシュ[＃20293](https://github.com/pingcap/tidb/pull/20293)の監視メトリックを追加します。
    -   悲観的ロックキー[＃20199](https://github.com/pingcap/tidb/pull/20199)のランタイム情報を追加
    -   実行時間情報に時間消費情報のセクションを2つ追加し、 `trace`スパン[＃20187](https://github.com/pingcap/tidb/pull/20187)
    -   スローログ[＃20185](https://github.com/pingcap/tidb/pull/20185)にトランザクションコミットの実行時情報を追加する
    -   インデックスマージ結合[＃20599](https://github.com/pingcap/tidb/pull/20599)を無効にする
    -   時間文字列リテラルに ISO 8601 とタイムゾーンのサポートを追加[＃20670](https://github.com/pingcap/tidb/pull/20670)

-   TiKV

    -   パフォーマンス診断を支援するための**Fast-Tune**パネルページを追加[＃8804](https://github.com/tikv/tikv/pull/8804)
    -   ログからユーザーデータを削除する`security.redact-info-log`構成項目を追加します[＃8746](https://github.com/tikv/tikv/pull/8746)
    -   エラーコード[＃8877](https://github.com/tikv/tikv/pull/8877)のメタファイルを再フォーマットする
    -   `pessimistic-txn.pipelined`構成[＃8853](https://github.com/tikv/tikv/pull/8853)動的に変更できるようにする
    -   メモリプロファイリング機能をデフォルトで有効にする[＃8801](https://github.com/tikv/tikv/pull/8801)

-   PD

    -   エラーのメタファイルを生成する[＃3090](https://github.com/pingcap/pd/pull/3090)
    -   オペレータ[＃3009](https://github.com/pingcap/pd/pull/3009)追加情報を追加します

-   TiFlash

    -   Raftログの監視メトリックを追加する
    -   `cop`タスクのメモリ使用量の監視メトリックを追加します
    -   データが削除されたときに`min`インデックス`max`より正確にする
    -   データ量が少ない場合のクエリパフォーマンスを向上
    -   標準エラーコードをサポートするために`errors.toml`ファイルを追加します

-   ツール

    -   バックアップと復元 (BR)

        -   `split`と`ingest`パイプライン化して復元プロセスを高速化します[＃427](https://github.com/pingcap/br/pull/427)
        -   PDスケジューラ[＃530](https://github.com/pingcap/br/pull/530)手動復元をサポート
        -   `remove`スケジューラの代わりに`pause`スケジューラを使用する[＃551](https://github.com/pingcap/br/pull/551)

    -   TiCDC

        -   MySQLシンクの統計情報を定期的に印刷する[＃1023](https://github.com/pingcap/tiflow/pull/1023)

    -   Dumpling

        -   S3ストレージへのダンプリングデータの直接サポート[＃155](https://github.com/pingcap/dumpling/pull/155)
        -   ダンプビューのサポート[＃158](https://github.com/pingcap/dumpling/pull/158)
        -   生成された列のみを含むテーブルのダンプをサポート[＃166](https://github.com/pingcap/dumpling/pull/166)

    -   TiDB Lightning

        -   マルチバイトCSV区切り文字とセパレーターをサポート[＃406](https://github.com/pingcap/tidb-lightning/pull/406)
        -   一部のPDスケジューラを無効にして復元プロセスを高速化します[＃408](https://github.com/pingcap/tidb-lightning/pull/408)
        -   v4.0 クラスタのチェックサム GC セーフポイントに GC-TTL API を使用して、GC エラー[＃396](https://github.com/pingcap/tidb-lightning/pull/396)を回避します。

## バグ修正 {#bug-fixes}

-   TiDB

    -   パーティションテーブルの使用時に発生する予期しないpanicを修正[＃20565](https://github.com/pingcap/tidb/pull/20565)
    -   インデックスマージ結合[＃20427](https://github.com/pingcap/tidb/pull/20427)を使用して外側をフィルタリングする際の外側結合の誤った結果を修正しました
    -   データが長すぎる場合、データを`BIT`型に変換するときに`NULL`値が返される問題を修正しました[＃20363](https://github.com/pingcap/tidb/pull/20363)
    -   `BIT`型列[＃20340](https://github.com/pingcap/tidb/pull/20340)の破損したデフォルト値を修正
    -   `BIT`型を`INT64`型に変換するときに発生する可能性のあるオーバーフローエラーを修正しました[＃20312](https://github.com/pingcap/tidb/pull/20312)
    -   ハイブリッド型列[＃20297](https://github.com/pingcap/tidb/pull/20297)の列伝播最適化で誤った結果が発生する可能性があった問題を修正しました。
    -   プランキャッシュ[＃20246](https://github.com/pingcap/tidb/pull/20246)から古いプランを保存するときに発生する可能性のあるpanicを修正しました
    -   `FROM_UNIXTIME`と`UNION ALL`一緒に使用すると返される結果が誤って切り捨てられるバグを修正しました[＃20240](https://github.com/pingcap/tidb/pull/20240)
    -   `Enum`型の値を`Float`型に変換すると間違った結果が返される可能性がある問題を修正しました[＃20235](https://github.com/pingcap/tidb/pull/20235)
    -   `RegionStore.accessStore` [#20210](https://github.com/pingcap/tidb/pull/20210)の可能性のあるpanicを修正
    -   `BatchPointGet` [#20205](https://github.com/pingcap/tidb/pull/20205)で最大の符号なし整数をソートしたときに返される誤った結果を修正しました
    -   `Enum`と`Set`の強制力が間違っているバグを修正[＃20364](https://github.com/pingcap/tidb/pull/20364)
    -   曖昧な`YEAR`変換[＃20292](https://github.com/pingcap/tidb/pull/20292)の問題を修正
    -   **KV期間**パネルに`store0` [＃20260](https://github.com/pingcap/tidb/pull/20260)が含まれている場合に発生する誤った報告結果の問題を修正しました
    -   `out of range`エラー[＃20252](https://github.com/pingcap/tidb/pull/20252)に関係なく`Float`タイプのデータが誤って挿入される問題を修正
    -   生成された列が不正な`NULL`値を処理できないバグを修正しました[＃20216](https://github.com/pingcap/tidb/pull/20216)
    -   範囲外の`YEAR`型データ[＃20170](https://github.com/pingcap/tidb/pull/20170)の不正確なエラー情報を修正
    -   悲観的トランザクション再試行中に発生する可能性のある予期しないエラー`invalid auto-id`を修正[＃20134](https://github.com/pingcap/tidb/pull/20134)
    -   `ALTER TABLE`使用して`Enum`タイプ[＃20046](https://github.com/pingcap/tidb/pull/20046) `Set`するときに制約がチェックされない問題を修正
    -   複数の演算子を並行処理に使用した場合に記録される`cop`タスクの誤った実行時間情報を修正[＃19947](https://github.com/pingcap/tidb/pull/19947)
    -   読み取り専用システム変数をセッション変数として明示的に選択できない問題を修正[＃19944](https://github.com/pingcap/tidb/pull/19944)
    -   重複した`ORDER BY`条件により、最適ではない実行プラン[＃20333](https://github.com/pingcap/tidb/pull/20333)が発生する可能性がある問題を修正しました。
    -   フォントサイズが最大許容値[＃20637](https://github.com/pingcap/tidb/pull/20637)を超えると、生成されたメトリックプロファイルが失敗する可能性がある問題を修正しました。

-   TiKV

    -   暗号化時のミューテックスの競合によりpd-workerのハートビート処理が遅くなるバグを修正[＃8869](https://github.com/tikv/tikv/pull/8869)
    -   メモリプロファイルが誤って生成される問題を修正[＃8790](https://github.com/tikv/tikv/pull/8790)
    -   storageクラス[＃8763](https://github.com/tikv/tikv/pull/8763)が指定されている場合に GCS 上のデータベースをバックアップできない問題を修正しました
    -   リージョンが再起動されたり、新しく分割されたりしたときに学習者がリーダーを見つけられないバグを修正[＃8864](https://github.com/tikv/tikv/pull/8864)

-   PD

    -   TiDBダッシュボードのキービジュアライザーがPDpanicを引き起こす可能性があるバグを修正[＃3096](https://github.com/pingcap/pd/pull/3096)
    -   PDストアが10分以上ダウンした場合にPDがpanic可能性があるバグを修正[＃3069](https://github.com/pingcap/pd/pull/3069)

-   TiFlash

    -   ログメッセージのタイムスタンプが間違っている問題を修正
    -   マルチディスクTiFlash展開中に、間違った容量が原因でTiFlashレプリカの作成が失敗する問題を修正しました。
    -   再起動後にTiFlashが壊れたデータファイルに関するエラーをスローする可能性があるバグを修正しました
    -   TiFlashがクラッシュした後に壊れたファイルがディスク上に残る可能性がある問題を修正しました
    -   プロキシが最新のRaftリース情報に追いつけない場合、学習者の読み取り中にインデックスを待つのに長い時間がかかる可能性があるというバグを修正しました。
    -   古いRaftログを再生中にプロキシがキー値エンジンに過剰なリージョン状態情報を書き込むバグを修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   復元中に発生し`send on closed channel`panicを修正[＃559](https://github.com/pingcap/br/pull/559)

    -   TiCDC

        -   GCセーフポイント[＃979](https://github.com/pingcap/tiflow/pull/979)更新失敗によって発生する予期しない終了を修正しました
        -   不正なmodリビジョンキャッシュ[＃1017](https://github.com/pingcap/tiflow/pull/1017)が原因でタスクステータスが予期せずフラッシュされる問題を修正

    -   TiDB Lightning

        -   列情報の誤りの問題を修正[＃420](https://github.com/pingcap/tidb-lightning/pull/420)
        -   ローカルモード[＃418](https://github.com/pingcap/tidb-lightning/pull/418)でリージョン情報の取得を再試行する際に発生する無限ループを修正しました
