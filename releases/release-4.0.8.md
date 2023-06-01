---
title: TiDB 4.0.8 Release Notes
---

# TiDB 4.0.8 リリースノート {#tidb-4-0-8-release-notes}

発売日：2020年10月30日

TiDB バージョン: 4.0.8

## 新機能 {#new-features}

-   TiDB

    -   新しい集計関数をサポート`APPROX_PERCENTILE` [<a href="https://github.com/pingcap/tidb/pull/20197">#20197</a>](https://github.com/pingcap/tidb/pull/20197)

-   TiFlash

    -   `CAST`関数のプッシュダウンをサポート

-   ツール

    -   TiCDC

        -   スナップショットレベルの整合性のあるレプリケーションをサポート[<a href="https://github.com/pingcap/tiflow/pull/932">#932</a>](https://github.com/pingcap/tiflow/pull/932)

## 改善点 {#improvements}

-   TiDB

    -   `Selectivity()` [<a href="https://github.com/pingcap/tidb/pull/20154">#20154</a>](https://github.com/pingcap/tidb/pull/20154)の貪欲検索手順で選択性の低いインデックスを優先します。
    -   コプロセッサー・ランタイム統計[<a href="https://github.com/pingcap/tidb/pull/19264">#19264</a>](https://github.com/pingcap/tidb/pull/19264)にさらに多くの RPC ランタイム情報を記録します。
    -   遅いログの解析を高速化し、クエリのパフォーマンスを向上させます[<a href="https://github.com/pingcap/tidb/pull/20556">#20556</a>](https://github.com/pingcap/tidb/pull/20556)
    -   SQL オプティマイザーが潜在的な新しいプランを検証しているときに、プラン バインディング ステージで実行プランがタイムアウトになるまで待機し、さらにデバッグ情報を記録します[<a href="https://github.com/pingcap/tidb/pull/20530">#20530</a>](https://github.com/pingcap/tidb/pull/20530)
    -   低速ログの実行再試行時間と低速クエリ結果を追加します[<a href="https://github.com/pingcap/tidb/pull/20495">#20495</a>](https://github.com/pingcap/tidb/pull/20495) [<a href="https://github.com/pingcap/tidb/pull/20494">#20494</a>](https://github.com/pingcap/tidb/pull/20494)
    -   `table_storage_stats`システムテーブル[<a href="https://github.com/pingcap/tidb/pull/20431">#20431</a>](https://github.com/pingcap/tidb/pull/20431)を追加します。
    -   `INSERT` / `UPDATE` / `REPLACE`ステートメントの RPC ランタイム統計情報を追加します[<a href="https://github.com/pingcap/tidb/pull/20430">#20430</a>](https://github.com/pingcap/tidb/pull/20430)
    -   `EXPLAIN FOR CONNECTION` [<a href="https://github.com/pingcap/tidb/pull/20384">#20384</a>](https://github.com/pingcap/tidb/pull/20384)の結果に演算子情報を追加
    -   TiDB エラー ログをクライアントの接続/切断アクティビティ[<a href="https://github.com/pingcap/tidb/pull/20321">#20321</a>](https://github.com/pingcap/tidb/pull/20321)のレベル`DEBUG`に調整します。
    -   コプロセッサーキャッシュ[<a href="https://github.com/pingcap/tidb/pull/20293">#20293</a>](https://github.com/pingcap/tidb/pull/20293)の監視メトリクスを追加
    -   悲観的ロックキーの実行時情報を追加[<a href="https://github.com/pingcap/tidb/pull/20199">#20199</a>](https://github.com/pingcap/tidb/pull/20199)
    -   ランタイム情報に時間消費情報の 2 つの追加セクションと`trace`スパン[<a href="https://github.com/pingcap/tidb/pull/20187">#20187</a>](https://github.com/pingcap/tidb/pull/20187)を追加します。
    -   トランザクションコミットの実行時情報をスローログ[<a href="https://github.com/pingcap/tidb/pull/20185">#20185</a>](https://github.com/pingcap/tidb/pull/20185)に追加します。
    -   インデックスマージジョインを無効にする[<a href="https://github.com/pingcap/tidb/pull/20599">#20599</a>](https://github.com/pingcap/tidb/pull/20599)
    -   ISO 8601 と時間文字列リテラルのタイムゾーン サポートを追加[<a href="https://github.com/pingcap/tidb/pull/20670">#20670</a>](https://github.com/pingcap/tidb/pull/20670)

-   TiKV

    -   パフォーマンス診断を支援する**Fast-Tune**パネル ページを追加します[<a href="https://github.com/tikv/tikv/pull/8804">#8804</a>](https://github.com/tikv/tikv/pull/8804)
    -   ログ[<a href="https://github.com/tikv/tikv/pull/8746">#8746</a>](https://github.com/tikv/tikv/pull/8746)からのユーザー データを編集する`security.redact-info-log`構成アイテムを追加します。
    -   エラーコード[<a href="https://github.com/tikv/tikv/pull/8877">#8877</a>](https://github.com/tikv/tikv/pull/8877)のメタファイルを再フォーマットする
    -   `pessimistic-txn.pipelined`構成の動的変更を有効にする[<a href="https://github.com/tikv/tikv/pull/8853">#8853</a>](https://github.com/tikv/tikv/pull/8853)
    -   メモリプロファイリング機能をデフォルトで有効にする[<a href="https://github.com/tikv/tikv/pull/8801">#8801</a>](https://github.com/tikv/tikv/pull/8801)

-   PD

    -   エラー[<a href="https://github.com/pingcap/pd/pull/3090">#3090</a>](https://github.com/pingcap/pd/pull/3090)のメタファイルを生成する
    -   演算子[<a href="https://github.com/pingcap/pd/pull/3009">#3009</a>](https://github.com/pingcap/pd/pull/3009)の追加情報を追加します。

-   TiFlash

    -   Raftログのモニタリングメトリクスを追加
    -   `cop`タスクのメモリ使用量の監視メトリクスを追加
    -   データ削除時の`min`インデックス`max`精度を高める
    -   データ量が少ない場合のクエリのパフォーマンスを向上させる
    -   標準エラーコードをサポートするために`errors.toml`ファイルを追加します

-   ツール

    -   バックアップと復元 (BR)

        -   `split`と`ingest`をパイプライン化することで復元プロセスを高速化します[<a href="https://github.com/pingcap/br/pull/427">#427</a>](https://github.com/pingcap/br/pull/427)
        -   PD スケジューラの手動復元をサポート[<a href="https://github.com/pingcap/br/pull/530">#530</a>](https://github.com/pingcap/br/pull/530)
        -   `remove`スケジューラの代わりに`pause`スケジューラを使用する[<a href="https://github.com/pingcap/br/pull/551">#551</a>](https://github.com/pingcap/br/pull/551)

    -   TiCDC

        -   MySQL シンクの統計を定期的に出力する[<a href="https://github.com/pingcap/tiflow/pull/1023">#1023</a>](https://github.com/pingcap/tiflow/pull/1023)

    -   Dumpling

        -   S3 ストレージへのダンプリング データの直接サポート[<a href="https://github.com/pingcap/dumpling/pull/155">#155</a>](https://github.com/pingcap/dumpling/pull/155)
        -   ビューのダンプをサポート[<a href="https://github.com/pingcap/dumpling/pull/158">#158</a>](https://github.com/pingcap/dumpling/pull/158)
        -   生成された列のみを含むテーブルのダンプをサポート[<a href="https://github.com/pingcap/dumpling/pull/166">#166</a>](https://github.com/pingcap/dumpling/pull/166)

    -   TiDB Lightning

        -   マルチバイトの CSV 区切り文字と区切り文字をサポート[<a href="https://github.com/pingcap/tidb-lightning/pull/406">#406</a>](https://github.com/pingcap/tidb-lightning/pull/406)
        -   一部の PD スケジューラを無効にして、復元プロセスを高速化します[<a href="https://github.com/pingcap/tidb-lightning/pull/408">#408</a>](https://github.com/pingcap/tidb-lightning/pull/408)
        -   GC エラー[<a href="https://github.com/pingcap/tidb-lightning/pull/396">#396</a>](https://github.com/pingcap/tidb-lightning/pull/396)を回避するには、v4.0 クラスターのチェックサム GC セーフポイントに GC-TTL API を使用します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   パーティションテーブルの使用時に発生する予期しないpanicを修正します[<a href="https://github.com/pingcap/tidb/pull/20565">#20565</a>](https://github.com/pingcap/tidb/pull/20565)
    -   インデックス マージ ジョイン[<a href="https://github.com/pingcap/tidb/pull/20427">#20427</a>](https://github.com/pingcap/tidb/pull/20427)を使用して外側をフィルタリングする場合の外部結合の間違った結果を修正しました。
    -   データが長すぎる場合に`BIT`型に変換すると`NULL`値が返される問題を修正[<a href="https://github.com/pingcap/tidb/pull/20363">#20363</a>](https://github.com/pingcap/tidb/pull/20363)
    -   `BIT`タイプ列[<a href="https://github.com/pingcap/tidb/pull/20340">#20340</a>](https://github.com/pingcap/tidb/pull/20340)の破損したデフォルト値を修正
    -   `BIT`型を`INT64`型[<a href="https://github.com/pingcap/tidb/pull/20312">#20312</a>](https://github.com/pingcap/tidb/pull/20312)に変換する際に発生することがあるオーバーフローエラーを修正
    -   ハイブリッド タイプ カラム[<a href="https://github.com/pingcap/tidb/pull/20297">#20297</a>](https://github.com/pingcap/tidb/pull/20297)の伝播カラム最適化で発生する可能性のある間違った結果を修正しました。
    -   古いプランをプラン キャッシュ[<a href="https://github.com/pingcap/tidb/pull/20246">#20246</a>](https://github.com/pingcap/tidb/pull/20246)から保存するときに発生する可能性があるpanicを修正しました。
    -   `FROM_UNIXTIME`と`UNION ALL`を併用すると返される結果が誤って切り捨てられるバグを修正[<a href="https://github.com/pingcap/tidb/pull/20240">#20240</a>](https://github.com/pingcap/tidb/pull/20240)
    -   `Enum`型の値を`Float`型[<a href="https://github.com/pingcap/tidb/pull/20235">#20235</a>](https://github.com/pingcap/tidb/pull/20235)に変換すると誤った結果が返されることがある問題を修正
    -   `RegionStore.accessStore` [<a href="https://github.com/pingcap/tidb/pull/20210">#20210</a>](https://github.com/pingcap/tidb/pull/20210)のpanicの可能性を修正
    -   最大の符号なし整数を`BatchPointGet` [<a href="https://github.com/pingcap/tidb/pull/20205">#20205</a>](https://github.com/pingcap/tidb/pull/20205)でソートするときに返される間違った結果を修正しました。
    -   `Enum`と`Set`の強制力が間違っているバグを修正[<a href="https://github.com/pingcap/tidb/pull/20364">#20364</a>](https://github.com/pingcap/tidb/pull/20364)
    -   あいまいな`YEAR`変換[<a href="https://github.com/pingcap/tidb/pull/20292">#20292</a>](https://github.com/pingcap/tidb/pull/20292)の問題を修正
    -   **KV期間**パネルに`store0` [<a href="https://github.com/pingcap/tidb/pull/20260">#20260</a>](https://github.com/pingcap/tidb/pull/20260)含まれている場合に発生する誤った結果が報告される問題を修正
    -   `out of range`エラー[<a href="https://github.com/pingcap/tidb/pull/20252">#20252</a>](https://github.com/pingcap/tidb/pull/20252)に関わらず`Float`種類のデータが誤って挿入されてしまう問題を修正
    -   生成されたカラムが不正な`NULL`値[<a href="https://github.com/pingcap/tidb/pull/20216">#20216</a>](https://github.com/pingcap/tidb/pull/20216)を処理しないバグを修正
    -   [<a href="https://github.com/pingcap/tidb/pull/20170">#20170</a>](https://github.com/pingcap/tidb/pull/20170)の範囲外の`YEAR`種データの不正確なエラー情報を修正
    -   悲観的トランザクションの再試行中に発生する可能性がある予期しないエラー`invalid auto-id`を修正します[<a href="https://github.com/pingcap/tidb/pull/20134">#20134</a>](https://github.com/pingcap/tidb/pull/20134)
    -   `ALTER TABLE`を使用して`Enum` / `Set`タイプ[<a href="https://github.com/pingcap/tidb/pull/20046">#20046</a>](https://github.com/pingcap/tidb/pull/20046)を変更するときに制約がチェックされない問題を修正
    -   複数のオペレーターが同時実行に使用された場合に記録される`cop`タスクの誤った実行時情報を修正[<a href="https://github.com/pingcap/tidb/pull/19947">#19947</a>](https://github.com/pingcap/tidb/pull/19947)
    -   読み取り専用のシステム変数をセッション変数として明示的に選択できない問題を修正します[<a href="https://github.com/pingcap/tidb/pull/19944">#19944</a>](https://github.com/pingcap/tidb/pull/19944)
    -   重複`ORDER BY`条件により最適ではない実行プラン[<a href="https://github.com/pingcap/tidb/pull/20333">#20333</a>](https://github.com/pingcap/tidb/pull/20333)が発生する可能性がある問題を修正
    -   フォント サイズが最大許容値[<a href="https://github.com/pingcap/tidb/pull/20637">#20637</a>](https://github.com/pingcap/tidb/pull/20637)を超えると、生成されたメトリック プロファイルが失敗する可能性がある問題を修正します。

-   TiKV

    -   暗号化におけるミューテックスの競合により pd-worker のハートビート処理が遅くなるバグを修正[<a href="https://github.com/tikv/tikv/pull/8869">#8869</a>](https://github.com/tikv/tikv/pull/8869)
    -   メモリプロファイルが誤って生成される問題を修正[<a href="https://github.com/tikv/tikv/pull/8790">#8790</a>](https://github.com/tikv/tikv/pull/8790)
    -   storageクラス[<a href="https://github.com/tikv/tikv/pull/8763">#8763</a>](https://github.com/tikv/tikv/pull/8763)が指定されている場合に GCS でデータベースをバックアップできない問題を修正
    -   リージョンの再起動または新規分割時に学習者がリーダーを見つけられないバグを修正[<a href="https://github.com/tikv/tikv/pull/8864">#8864</a>](https://github.com/tikv/tikv/pull/8864)

-   PD

    -   TiDB Dashboard の Key Visualizer が場合によって PDpanicを引き起こす可能性があるバグを修正[<a href="https://github.com/pingcap/pd/pull/3096">#3096</a>](https://github.com/pingcap/pd/pull/3096)
    -   PD ストアが 10 分以上ダウンしている場合に PD がpanicになる可能性があるバグを修正[<a href="https://github.com/pingcap/pd/pull/3069">#3069</a>](https://github.com/pingcap/pd/pull/3069)

-   TiFlash

    -   ログメッセージ内の間違ったタイムスタンプの問題を修正
    -   マルチディスクTiFlash展開中に、間違った容量によりTiFlashレプリカの作成が失敗する問題を修正
    -   TiFlash が再起動後に破損したデータ ファイルに関するエラーをスローする可能性があるバグを修正
    -   TiFlash がクラッシュした後、壊れたファイルがディスク上に残る可能性がある問題を修正
    -   プロキシが最新のRaftリース情報を追いつけない場合、学習者の読み込み中にインデックス待ちに長時間かかることがあるバグを修正
    -   古いRaftログを再生するときに、プロキシがキー値エンジンにリージョン状態情報を書きすぎるというバグを修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   復元中の`send on closed channel`panicを修正[<a href="https://github.com/pingcap/br/pull/559">#559</a>](https://github.com/pingcap/br/pull/559)

    -   TiCDC

        -   GC セーフポイント[<a href="https://github.com/pingcap/tiflow/pull/979">#979</a>](https://github.com/pingcap/tiflow/pull/979)の更新の失敗によって引き起こされる予期しない終了を修正しました。
        -   不正な Mod リビジョン キャッシュ[<a href="https://github.com/pingcap/tiflow/pull/1017">#1017</a>](https://github.com/pingcap/tiflow/pull/1017)が原因でタスク ステータスが予期せずフラッシュされる問題を修正
        -   予期しない空の Maxwell メッセージを修正する[<a href="https://github.com/pingcap/tiflow/pull/978">#978</a>](https://github.com/pingcap/tiflow/pull/978)

    -   TiDB Lightning

        -   間違った列情報の問題を修正[<a href="https://github.com/pingcap/tidb-lightning/pull/420">#420</a>](https://github.com/pingcap/tidb-lightning/pull/420)
        -   ローカルモード[<a href="https://github.com/pingcap/tidb-lightning/pull/418">#418</a>](https://github.com/pingcap/tidb-lightning/pull/418)でリージョン情報の取得をリトライする際に発生する無限ループを修正
