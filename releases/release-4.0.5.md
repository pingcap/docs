---
title: TiDB 4.0.5 Release Notes
---

# TiDB 4.0.5 リリースノート {#tidb-4-0-5-release-notes}

発売日：2020年8月31日

TiDB バージョン: 4.0.5

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   複数のパーティションの ID 配列をサポートするように`drop partition`と`truncate partition`のジョブ引数を変更します[<a href="https://github.com/pingcap/tidb/pull/18930">#18930</a>](https://github.com/pingcap/tidb/pull/18930)
    -   `add partition`レプリカ[<a href="https://github.com/pingcap/tidb/pull/18865">#18865</a>](https://github.com/pingcap/tidb/pull/18865)をチェックするための削除専用状態を追加します。

## 新機能 {#new-features}

-   TiKV

    -   エラー[<a href="https://github.com/tikv/tikv/pull/8387">#8387</a>](https://github.com/tikv/tikv/pull/8387)のエラー コードを定義する

-   TiFlash

    -   TiDB による統一ログ形式のサポート

-   ツール

    -   TiCDC

        -   Kafka SSL 接続のサポート[<a href="https://github.com/pingcap/tiflow/pull/764">#764</a>](https://github.com/pingcap/tiflow/pull/764)
        -   古い値[<a href="https://github.com/pingcap/tiflow/pull/708">#708</a>](https://github.com/pingcap/tiflow/pull/708)の出力をサポート
        -   列フラグを追加します[<a href="https://github.com/pingcap/tiflow/pull/796">#796</a>](https://github.com/pingcap/tiflow/pull/796)
        -   以前のバージョン[<a href="https://github.com/pingcap/tiflow/pull/799">#799</a>](https://github.com/pingcap/tiflow/pull/799)の DDL ステートメントとテーブル スキーマの出力をサポート

## 改善点 {#improvements}

-   TiDB

    -   大きなユニオンクエリに対する`DecodePlan`のパフォーマンスを最適化する[<a href="https://github.com/pingcap/tidb/pull/18941">#18941</a>](https://github.com/pingcap/tidb/pull/18941)
    -   `Region cache miss`エラー発生時の GC ロック スキャンの数を減らす[<a href="https://github.com/pingcap/tidb/pull/18876">#18876</a>](https://github.com/pingcap/tidb/pull/18876)
    -   クラスターのパフォーマンスに対する統計フィードバックの影響を緩和する[<a href="https://github.com/pingcap/tidb/pull/18772">#18772</a>](https://github.com/pingcap/tidb/pull/18772)
    -   RPC 応答が返される前に操作をキャンセルできるようになりました[<a href="https://github.com/pingcap/tidb/pull/18580">#18580</a>](https://github.com/pingcap/tidb/pull/18580)
    -   HTTP API を追加して TiDB メトリック プロファイルを生成する[<a href="https://github.com/pingcap/tidb/pull/18531">#18531</a>](https://github.com/pingcap/tidb/pull/18531)
    -   分散パーティションテーブルのサポート[<a href="https://github.com/pingcap/tidb/pull/17863">#17863</a>](https://github.com/pingcap/tidb/pull/17863)
    -   Grafana [<a href="https://github.com/pingcap/tidb/pull/18679">#18679</a>](https://github.com/pingcap/tidb/pull/18679)の各インスタンスの詳細なメモリ使用量を追加します。
    -   `EXPLAIN` [<a href="https://github.com/pingcap/tidb/pull/18892">#18892</a>](https://github.com/pingcap/tidb/pull/18892)の結果の`BatchPointGet`オペレーターの詳細な実行時情報を表示します。
    -   `EXPLAIN` [<a href="https://github.com/pingcap/tidb/pull/18817">#18817</a>](https://github.com/pingcap/tidb/pull/18817)の結果の`PointGet`オペレーターの詳細な実行時情報を表示します。
    -   `remove()` [<a href="https://github.com/pingcap/tidb/pull/18395">#18395</a>](https://github.com/pingcap/tidb/pull/18395)分の`Consume`の潜在的なデッドロックを警告します
    -   `StrToInt`と`StrToFloat`の動作を改良し、JSON の`date` 、 `time` 、および`timestamp`タイプへの変換をサポートします[<a href="https://github.com/pingcap/tidb/pull/18159">#18159</a>](https://github.com/pingcap/tidb/pull/18159)
    -   `TableReader`オペレータ[<a href="https://github.com/pingcap/tidb/pull/18392">#18392</a>](https://github.com/pingcap/tidb/pull/18392)のメモリ使用量の制限をサポート
    -   `batch cop`リクエスト[<a href="https://github.com/pingcap/tidb/pull/18999">#18999</a>](https://github.com/pingcap/tidb/pull/18999)を再試行するときにバックオフが多すぎることを避けます。
    -   `ALTER TABLE`アルゴリズムの互換性を向上[<a href="https://github.com/pingcap/tidb/pull/19270">#19270</a>](https://github.com/pingcap/tidb/pull/19270)
    -   単一のパーティションテーブルのサポート`IndexJoin`内側[<a href="https://github.com/pingcap/tidb/pull/19151">#19151</a>](https://github.com/pingcap/tidb/pull/19151)にします。
    -   ログに無効な行が含まれている場合でもログ ファイルの検索をサポートします[<a href="https://github.com/pingcap/tidb/pull/18579">#18579</a>](https://github.com/pingcap/tidb/pull/18579)

-   PD

    -   特別なエンジン ( TiFlashなど) を備えたストアでの散乱領域のサポート[<a href="https://github.com/tikv/pd/pull/2706">#2706</a>](https://github.com/tikv/pd/pull/2706)
    -   特定のキー範囲[<a href="https://github.com/tikv/pd/pull/2687">#2687</a>](https://github.com/tikv/pd/pull/2687)のリージョンスケジュールを優先するリージョンHTTP API をサポートします。
    -   リージョン分散[<a href="https://github.com/tikv/pd/pull/2684">#2684</a>](https://github.com/tikv/pd/pull/2684)後のリーダーの分布を改善します。
    -   TSO リクエスト[<a href="https://github.com/tikv/pd/pull/2678">#2678</a>](https://github.com/tikv/pd/pull/2678)のテストとログを追加します。
    -   リージョンのリーダーが変更された後の無効なキャッシュ更新を回避する[<a href="https://github.com/tikv/pd/pull/2672">#2672</a>](https://github.com/tikv/pd/pull/2672)
    -   `store.GetLimit`墓石ストア[<a href="https://github.com/tikv/pd/pull/2743">#2743</a>](https://github.com/tikv/pd/pull/2743)を返せるようにするオプションを追加します。
    -   PD リーダーとフォロワー間のリージョンリーダーの変更の同期をサポート[<a href="https://github.com/tikv/pd/pull/2795">#2795</a>](https://github.com/tikv/pd/pull/2795)
    -   GC セーフポイント サービスをクエリするためのコマンドを追加します[<a href="https://github.com/tikv/pd/pull/2797">#2797</a>](https://github.com/tikv/pd/pull/2797)
    -   パフォーマンスを向上させるためにフィルターの`region.Clone`呼び出しを置き換えます[<a href="https://github.com/tikv/pd/pull/2801">#2801</a>](https://github.com/tikv/pd/pull/2801)
    -   大規模クラスター[<a href="https://github.com/tikv/pd/pull/2848">#2848</a>](https://github.com/tikv/pd/pull/2848)のパフォーマンスを向上させるために、リージョンフロー キャッシュの更新を無効にするオプションを追加します。

-   TiFlash

    -   CPU、I/O、RAM 使用率のメトリクスとstorageエンジンのメトリクスを表示する Grafana パネルを追加します。
    -   Raftログの処理ロジックを最適化することで I/O 操作を削減します。
    -   ブロックされた`add partition` DDL ステートメントのリージョンスケジューリングを高速化する
    -   DeltaTree でデルタ データの圧縮を最適化し、読み取りおよび書き込みの増幅を削減します。
    -   複数のスレッドを使用してスナップショットを前処理することにより、リージョンスナップショットを適用するパフォーマンスを最適化します。
    -   TiFlashの読み取り負荷が低いときに開くファイル記述子の数を最適化し、システム リソースの消費を削減します。
    -   TiFlash の再起動時に作成される不要な小さなファイルの数を最適化します。
    -   データstorageの保存時の暗号化をサポート
    -   データ転送にTLSをサポート

-   ツール

    -   TiCDC

        -   TSO [<a href="https://github.com/pingcap/tiflow/pull/801">#801</a>](https://github.com/pingcap/tiflow/pull/801)を取得する頻度を下げる

    -   バックアップと復元 (BR)

        -   一部のログを最適化する[<a href="https://github.com/pingcap/br/pull/428">#428</a>](https://github.com/pingcap/br/pull/428)

    -   Dumpling

        -   MySQL [<a href="https://github.com/pingcap/dumpling/pull/121">#121</a>](https://github.com/pingcap/dumpling/pull/121)のロック時間を短縮するために、接続が作成された後に FTWRL を解放します。

    -   TiDB Lightning

        -   一部のログを最適化する[<a href="https://github.com/pingcap/tidb-lightning/pull/352">#352</a>](https://github.com/pingcap/tidb-lightning/pull/352)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `builtinCastRealAsDecimalSig`関数[<a href="https://github.com/pingcap/tidb/pull/18967">#18967</a>](https://github.com/pingcap/tidb/pull/18967)で`ErrTruncate/Overflow`エラーが正しく処理されないために発生する`should ensure all columns have the same length`エラーを修正
    -   `pre_split_regions`テーブル オプションがパーティションテーブル[<a href="https://github.com/pingcap/tidb/pull/18837">#18837</a>](https://github.com/pingcap/tidb/pull/18837)で機能しない問題を修正
    -   大規模なトランザクションが途中で終了する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/18813">#18813</a>](https://github.com/pingcap/tidb/pull/18813)
    -   `collation`関数を使用すると間違ったクエリ結果が得られる問題を修正します[<a href="https://github.com/pingcap/tidb/pull/18735">#18735</a>](https://github.com/pingcap/tidb/pull/18735)
    -   `getAutoIncrementID()`関数が`tidb_snapshot`セッション変数を考慮しないバグを修正します。これにより、ダンパー ツールが`table not exist`エラー[<a href="https://github.com/pingcap/tidb/pull/18692">#18692</a>](https://github.com/pingcap/tidb/pull/18692)で失敗する可能性があります。
    -   `select a from t having t.a` [<a href="https://github.com/pingcap/tidb/pull/18434">#18434</a>](https://github.com/pingcap/tidb/pull/18434)のような SQL ステートメントの`unknown column error`を修正します。
    -   パーティション キーが整数型[<a href="https://github.com/pingcap/tidb/pull/18186">#18186</a>](https://github.com/pingcap/tidb/pull/18186)の場合、64 ビットの符号なし型をハッシュパーティションテーブルに書き込むとオーバーフローが発生し、予期しない負の数値が取得されるというpanicの問題を修正します。
    -   `char`関数[<a href="https://github.com/pingcap/tidb/pull/18122">#18122</a>](https://github.com/pingcap/tidb/pull/18122)の誤った動作を修正します。
    -   `ADMIN REPAIR TABLE`ステートメントが範囲パーティション[<a href="https://github.com/pingcap/tidb/pull/17988">#17988</a>](https://github.com/pingcap/tidb/pull/17988)の式内の整数を解析できない問題を修正します。
    -   `SET CHARSET`ステートメント[<a href="https://github.com/pingcap/tidb/pull/17289">#17289</a>](https://github.com/pingcap/tidb/pull/17289)の誤った動作を修正します。
    -   `collation`関数[<a href="https://github.com/pingcap/tidb/pull/17231">#17231</a>](https://github.com/pingcap/tidb/pull/17231)の間違った結果につながる間違った照合順序設定によって引き起こされるバグを修正しました。
    -   `STR_TO_DATE`のフォーマット トークン &#39;%r&#39;、&#39;%h&#39; の処理が MySQL [<a href="https://github.com/pingcap/tidb/pull/18727">#18727</a>](https://github.com/pingcap/tidb/pull/18727)の処理と矛盾する問題を修正
    -   TiDB のバージョン情報が`cluster_info`表[<a href="https://github.com/pingcap/tidb/pull/18413">#18413</a>](https://github.com/pingcap/tidb/pull/18413)の PD/TiKV のバージョン情報と一致しない問題を修正
    -   悲観的トランザクションの既存のチェックを修正します[<a href="https://github.com/pingcap/tidb/pull/19004">#19004</a>](https://github.com/pingcap/tidb/pull/19004)
    -   `union select for update`を実行すると同時レース[<a href="https://github.com/pingcap/tidb/pull/19006">#19006</a>](https://github.com/pingcap/tidb/pull/19006)が発生する可能性がある問題を修正
    -   `apply`に`PointGet`演算子の子がある場合の間違ったクエリ結果を修正[<a href="https://github.com/pingcap/tidb/pull/19046">#19046</a>](https://github.com/pingcap/tidb/pull/19046)
    -   `IndexLookUp` `Apply`演算子[<a href="https://github.com/pingcap/tidb/pull/19496">#19496</a>](https://github.com/pingcap/tidb/pull/19496)の内側にある場合に発生する誤った結果を修正しました。
    -   `anti-semi-join`クエリの間違った結果を修正[<a href="https://github.com/pingcap/tidb/pull/19472">#19472</a>](https://github.com/pingcap/tidb/pull/19472)
    -   `BatchPointGet` [<a href="https://github.com/pingcap/tidb/pull/19456">#19456</a>](https://github.com/pingcap/tidb/pull/19456)の誤った使用によって引き起こされる誤った結果を修正
    -   `UnionScan` `Apply`演算子[<a href="https://github.com/pingcap/tidb/pull/19496">#19496</a>](https://github.com/pingcap/tidb/pull/19496)の内側にある場合に発生する誤った結果を修正しました。
    -   `EXECUTE`ステートメントを使用して高価なクエリ ログを出力することによって引き起こされるpanicを修正します[<a href="https://github.com/pingcap/tidb/pull/17419">#17419</a>](https://github.com/pingcap/tidb/pull/17419)
    -   結合キーが`ENUM`または`SET`の場合のインデックス結合エラーを修正[<a href="https://github.com/pingcap/tidb/pull/19235">#19235</a>](https://github.com/pingcap/tidb/pull/19235)
    -   インデックス列[<a href="https://github.com/pingcap/tidb/pull/19358">#19358</a>](https://github.com/pingcap/tidb/pull/19358)に`NULL`値が存在する場合、クエリ範囲を構築できない問題を修正
    -   グローバル構成[<a href="https://github.com/pingcap/tidb/pull/17964">#17964</a>](https://github.com/pingcap/tidb/pull/17964)の更新によって発生するデータ競合の問題を修正します。
    -   大文字のスキーマ[<a href="https://github.com/pingcap/tidb/pull/19286">#19286</a>](https://github.com/pingcap/tidb/pull/19286)の文字セットを変更するときに発生するpanic問題を修正します。
    -   ディスク流出アクション[<a href="https://github.com/pingcap/tidb/pull/18970">#18970</a>](https://github.com/pingcap/tidb/pull/18970)中に一時ディレクトリを変更することによって引き起こされる予期しないエラーを修正しました。
    -   10 進数タイプ[<a href="https://github.com/pingcap/tidb/pull/19131">#19131</a>](https://github.com/pingcap/tidb/pull/19131)の間違ったハッシュ キーを修正
    -   `PointGet`および`BatchPointGet`演算子がパーティション選択構文を考慮せず、誤った結果が得られる問題を修正します[<a href="https://github.com/pingcap/tidb/issues/19141">#19141</a>](https://github.com/pingcap/tidb/issues/19141)
    -   `Apply`演算子を`UnionScan`演算子と併用した場合の誤った結果を修正しました[<a href="https://github.com/pingcap/tidb/issues/19104">#19104</a>](https://github.com/pingcap/tidb/issues/19104)
    -   インデックス付きの仮想生成列が間違った値[<a href="https://github.com/pingcap/tidb/issues/17989">#17989</a>](https://github.com/pingcap/tidb/issues/17989)を返す原因となるバグを修正
    -   実行時統計のロックを追加して、同時実行によって引き起こされるpanicを修正します[<a href="https://github.com/pingcap/tidb/pull/18983">#18983</a>](https://github.com/pingcap/tidb/pull/18983)

-   TiKV

    -   Hibernateリージョンが有効な場合、リーダーの選出を高速化します[<a href="https://github.com/tikv/tikv/pull/8292">#8292</a>](https://github.com/tikv/tikv/pull/8292)
    -   スケジュール[<a href="https://github.com/tikv/tikv/pull/8357">#8357</a>](https://github.com/tikv/tikv/pull/8357)中のメモリリークの問題を修正する
    -   リーダーが急速に休止状態になるのを防ぐために`hibernate-timeout`設定項目を追加します[<a href="https://github.com/tikv/tikv/pull/8208">#8208</a>](https://github.com/tikv/tikv/pull/8208)

-   PD

    -   リーダーチェンジ[<a href="https://github.com/tikv/pd/pull/2666">#2666</a>](https://github.com/tikv/pd/pull/2666)時にTSOリクエストが失敗する場合があるバグを修正
    -   配置ルールが有効になっている場合、リージョンレプリカを最適な状態にスケジュールできない場合がある問題を修正します[<a href="https://github.com/tikv/pd/pull/2720">#2720</a>](https://github.com/tikv/pd/pull/2720)
    -   配置ルールが有効な場合に`Balance Leader`が機能しない問題を修正[<a href="https://github.com/tikv/pd/pull/2726">#2726</a>](https://github.com/tikv/pd/pull/2726)
    -   異常なストアがストア負荷統計からフィルタリングされない問題を修正[<a href="https://github.com/tikv/pd/pull/2805">#2805</a>](https://github.com/tikv/pd/pull/2805)

-   TiFlash

    -   データベースまたはテーブルの名前に特殊文字が含まれている場合、以前のバージョンからアップグレードした後、 TiFlash が正常に起動できない問題を修正
    -   初期化中に例外がスローされた場合、 TiFlashプロセスが終了できない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ概要ログ[<a href="https://github.com/pingcap/br/pull/472">#472</a>](https://github.com/pingcap/br/pull/472)で合計 KV と合計バイト数が重複して計算される問題を修正しました。
        -   このモードに切り替えた後、最初の 5 分間インポート モードが機能しない問題を修正します[<a href="https://github.com/pingcap/br/pull/473">#473</a>](https://github.com/pingcap/br/pull/473)

    -   Dumpling

        -   FTWRLロックが時間[<a href="https://github.com/pingcap/dumpling/pull/128">#128</a>](https://github.com/pingcap/dumpling/pull/128)に解除されない問題を修正

    -   TiCDC

        -   失敗した`changefeed`が削除できない問題を修正[<a href="https://github.com/pingcap/tiflow/pull/782">#782</a>](https://github.com/pingcap/tiflow/pull/782)
        -   ハンドル インデックス[<a href="https://github.com/pingcap/tiflow/pull/787">#787</a>](https://github.com/pingcap/tiflow/pull/787)として一意のインデックスを 1 つ選択して、無効な`delete`イベントを修正します。
        -   GCセーフポイントが停止`changefeed` [<a href="https://github.com/pingcap/tiflow/pull/797">#797</a>](https://github.com/pingcap/tiflow/pull/797)のチェックポイントを超えて転送されるバグを修正
        -   ネットワーク I/O 待機により終了するタスクがブロックされるバグを修正[<a href="https://github.com/pingcap/tiflow/pull/825">#825</a>](https://github.com/pingcap/tiflow/pull/825)
        -   不要なデータが誤って下流側に複製される場合があるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/743">#743</a>](https://github.com/pingcap/tiflow/issues/743)

    -   TiDB Lightning

        -   TiDB バックエンド[<a href="https://github.com/pingcap/tidb-lightning/pull/357">#357</a>](https://github.com/pingcap/tidb-lightning/pull/357)を使用する場合の空のバイナリ/16 進リテラルの構文エラーを修正しました。
