---
title: TiDB 4.0.5 Release Notes
---

# TiDB 4.0.5 リリースノート {#tidb-4-0-5-release-notes}

発売日：2020年8月31日

TiDB バージョン: 4.0.5

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   複数のパーティションの ID 配列をサポートするように`drop partition`と`truncate partition`のジョブ引数を変更します[#18930](https://github.com/pingcap/tidb/pull/18930)
    -   `add partition`レプリ​​カ[#18865](https://github.com/pingcap/tidb/pull/18865)をチェックするための削除専用状態を追加します。

## 新機能 {#new-features}

-   TiKV

    -   エラー[#8387](https://github.com/tikv/tikv/pull/8387)のエラー コードを定義する

-   TiFlash

    -   TiDB による統一ログ形式のサポート

-   ツール

    -   TiCDC

        -   Kafka SSL 接続のサポート[#764](https://github.com/pingcap/tiflow/pull/764)
        -   古い値[#708](https://github.com/pingcap/tiflow/pull/708)の出力をサポート
        -   列フラグを追加します[#796](https://github.com/pingcap/tiflow/pull/796)
        -   以前のバージョン[#799](https://github.com/pingcap/tiflow/pull/799)の DDL ステートメントとテーブル スキーマの出力をサポート

## 改善点 {#improvements}

-   TiDB

    -   大きなユニオンクエリに対する`DecodePlan`のパフォーマンスを最適化する[#18941](https://github.com/pingcap/tidb/pull/18941)
    -   `Region cache miss`エラー発生時の GC ロック スキャンの数を減らす[#18876](https://github.com/pingcap/tidb/pull/18876)
    -   クラスターのパフォーマンスに対する統計フィードバックの影響を緩和する[#18772](https://github.com/pingcap/tidb/pull/18772)
    -   RPC 応答が返される前に操作をキャンセルできるようになりました[#18580](https://github.com/pingcap/tidb/pull/18580)
    -   HTTP API を追加して TiDB メトリック プロファイルを生成する[#18531](https://github.com/pingcap/tidb/pull/18531)
    -   分散パーティションテーブルのサポート[#17863](https://github.com/pingcap/tidb/pull/17863)
    -   Grafana [#18679](https://github.com/pingcap/tidb/pull/18679)の各インスタンスの詳細なメモリ使用量を追加します。
    -   `EXPLAIN` [#18892](https://github.com/pingcap/tidb/pull/18892)の結果の`BatchPointGet`オペレーターの詳細な実行時情報を表示します。
    -   `EXPLAIN` [#18817](https://github.com/pingcap/tidb/pull/18817)の結果の`PointGet`オペレーターの詳細な実行時情報を表示します。
    -   `remove()` [#18395](https://github.com/pingcap/tidb/pull/18395)分の`Consume`の潜在的なデッドロックを警告します
    -   `StrToInt`と`StrToFloat`の動作を改良し、JSON の`date` 、 `time` 、および`timestamp`タイプへの変換をサポートします[#18159](https://github.com/pingcap/tidb/pull/18159)
    -   `TableReader`オペレータ[#18392](https://github.com/pingcap/tidb/pull/18392)のメモリ使用量の制限をサポート
    -   `batch cop`リクエスト[#18999](https://github.com/pingcap/tidb/pull/18999)を再試行するときにバックオフが多すぎることを避けます。
    -   `ALTER TABLE`アルゴリズムの互換性を向上[#19270](https://github.com/pingcap/tidb/pull/19270)
    -   単一のパーティションテーブルのサポート`IndexJoin`内側[#19151](https://github.com/pingcap/tidb/pull/19151)にします。
    -   ログに無効な行が含まれている場合でもログ ファイルの検索をサポートします[#18579](https://github.com/pingcap/tidb/pull/18579)

-   PD

    -   特別なエンジン ( TiFlashなど) を備えたストアでの散乱領域のサポート[#2706](https://github.com/tikv/pd/pull/2706)
    -   特定のキー範囲[#2687](https://github.com/tikv/pd/pull/2687)のリージョンスケジュールを優先するリージョンHTTP API をサポートします。
    -   リージョン分散[#2684](https://github.com/tikv/pd/pull/2684)後のリーダーの分布を改善します。
    -   TSO リクエスト[#2678](https://github.com/tikv/pd/pull/2678)のテストとログを追加します。
    -   リージョンのリーダーが変更された後の無効なキャッシュ更新を回避する[#2672](https://github.com/tikv/pd/pull/2672)
    -   `store.GetLimit`墓石ストア[#2743](https://github.com/tikv/pd/pull/2743)を返せるようにするオプションを追加します。
    -   PD リーダーとフォロワー間のリージョンリーダーの変更の同期をサポート[#2795](https://github.com/tikv/pd/pull/2795)
    -   GC セーフポイント サービスをクエリするためのコマンドを追加します[#2797](https://github.com/tikv/pd/pull/2797)
    -   パフォーマンスを向上させるためにフィルターの`region.Clone`呼び出しを置き換えます[#2801](https://github.com/tikv/pd/pull/2801)
    -   大規模クラスター[#2848](https://github.com/tikv/pd/pull/2848)のパフォーマンスを向上させるために、リージョンフロー キャッシュの更新を無効にするオプションを追加します。

-   TiFlash

    -   CPU、I/O、RAM 使用率のメトリクスとstorageエンジンのメトリクスを表示するための Grafana パネルを追加します。
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

        -   TSO [#801](https://github.com/pingcap/tiflow/pull/801)を取得する頻度を下げる

    -   バックアップと復元 (BR)

        -   一部のログを最適化する[#428](https://github.com/pingcap/br/pull/428)

    -   Dumpling

        -   MySQL [#121](https://github.com/pingcap/dumpling/pull/121)のロック時間を短縮するために、接続が作成された後に FTWRL を解放します。

    -   TiDB Lightning

        -   一部のログを最適化する[#352](https://github.com/pingcap/tidb-lightning/pull/352)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `builtinCastRealAsDecimalSig`関数[#18967](https://github.com/pingcap/tidb/pull/18967)で`ErrTruncate/Overflow`エラーが正しく処理されないために発生する`should ensure all columns have the same length`エラーを修正
    -   `pre_split_regions`テーブル オプションがパーティションテーブル[#18837](https://github.com/pingcap/tidb/pull/18837)で機能しない問題を修正
    -   大規模なトランザクションが途中で終了する可能性がある問題を修正します[#18813](https://github.com/pingcap/tidb/pull/18813)
    -   `collation`関数を使用すると間違ったクエリ結果が得られる問題を修正します[#18735](https://github.com/pingcap/tidb/pull/18735)
    -   `getAutoIncrementID()`関数が`tidb_snapshot`セッション変数を考慮しないバグを修正します。これにより、ダンパー ツールが`table not exist`エラー[#18692](https://github.com/pingcap/tidb/pull/18692)で失敗する可能性があります。
    -   `select a from t having t.a` [#18434](https://github.com/pingcap/tidb/pull/18434)のような SQL ステートメントの`unknown column error`を修正します。
    -   パーティション キーが整数型[#18186](https://github.com/pingcap/tidb/pull/18186)の場合、64 ビットの符号なし型をハッシュパーティションテーブルに書き込むとオーバーフローが発生し、予期しない負の数値が取得されるというpanicの問題を修正します。
    -   `char`関数[#18122](https://github.com/pingcap/tidb/pull/18122)の誤った動作を修正します。
    -   `ADMIN REPAIR TABLE`ステートメントが範囲パーティション[#17988](https://github.com/pingcap/tidb/pull/17988)の式内の整数を解析できない問題を修正します。
    -   `SET CHARSET`ステートメント[#17289](https://github.com/pingcap/tidb/pull/17289)の誤った動作を修正します。
    -   `collation`関数[#17231](https://github.com/pingcap/tidb/pull/17231)の間違った結果につながる間違った照合順序設定によって引き起こされるバグを修正しました。
    -   `STR_TO_DATE`のフォーマット トークン &#39;%r&#39;、&#39;%h&#39; の処理が MySQL [#18727](https://github.com/pingcap/tidb/pull/18727)の処理と矛盾する問題を修正
    -   TiDB のバージョン情報が`cluster_info`表[#18413](https://github.com/pingcap/tidb/pull/18413)の PD/TiKV のバージョン情報と一致しない問題を修正
    -   悲観的トランザクションの既存のチェックを修正します[#19004](https://github.com/pingcap/tidb/pull/19004)
    -   `union select for update`を実行すると同時レース[#19006](https://github.com/pingcap/tidb/pull/19006)が発生する可能性がある問題を修正
    -   `apply`に`PointGet`演算子の子がある場合の間違ったクエリ結果を修正[#19046](https://github.com/pingcap/tidb/pull/19046)
    -   `IndexLookUp` `Apply`演算子[#19496](https://github.com/pingcap/tidb/pull/19496)の内側にある場合に発生する誤った結果を修正しました。
    -   `anti-semi-join`クエリの間違った結果を修正[#19472](https://github.com/pingcap/tidb/pull/19472)
    -   `BatchPointGet` [#19456](https://github.com/pingcap/tidb/pull/19456)の誤った使用によって引き起こされる誤った結果を修正
    -   `UnionScan` `Apply`演算子[#19496](https://github.com/pingcap/tidb/pull/19496)の内側にある場合に発生する誤った結果を修正しました。
    -   `EXECUTE`ステートメントを使用して高価なクエリ ログを出力することによって引き起こされるpanicを修正します[#17419](https://github.com/pingcap/tidb/pull/17419)
    -   結合キーが`ENUM`または`SET`の場合のインデックス結合エラーを修正[#19235](https://github.com/pingcap/tidb/pull/19235)
    -   インデックス列[#19358](https://github.com/pingcap/tidb/pull/19358)に`NULL`値が存在する場合、クエリ範囲を構築できない問題を修正
    -   グローバル構成[#17964](https://github.com/pingcap/tidb/pull/17964)の更新によって発生するデータ競合の問題を修正します。
    -   大文字のスキーマ[#19286](https://github.com/pingcap/tidb/pull/19286)の文字セットを変更するときに発生するpanic問題を修正します。
    -   ディスク流出アクション[#18970](https://github.com/pingcap/tidb/pull/18970)中に一時ディレクトリを変更することによって引き起こされる予期しないエラーを修正しました。
    -   10 進数タイプ[#19131](https://github.com/pingcap/tidb/pull/19131)の間違ったハッシュ キーを修正
    -   `PointGet`および`BatchPointGet`演算子がパーティション選択構文を考慮せず、誤った結果が得られる問題を修正します[#19141](https://github.com/pingcap/tidb/issues/19141)
    -   `Apply`演算子を`UnionScan`演算子と併用した場合の誤った結果を修正しました[#19104](https://github.com/pingcap/tidb/issues/19104)
    -   インデックス付きの仮想生成列が間違った値[#17989](https://github.com/pingcap/tidb/issues/17989)を返す原因となるバグを修正
    -   実行時統計のロックを追加して、同時実行によって引き起こされるpanicを修正します[#18983](https://github.com/pingcap/tidb/pull/18983)

-   TiKV

    -   Hibernateリージョンが有効な場合、リーダーの選出を高速化します[#8292](https://github.com/tikv/tikv/pull/8292)
    -   スケジュール[#8357](https://github.com/tikv/tikv/pull/8357)中のメモリリークの問題を修正する
    -   リーダーが急速に休止状態になるのを防ぐために`hibernate-timeout`設定項目を追加します[#8208](https://github.com/tikv/tikv/pull/8208)

-   PD

    -   リーダーチェンジ[#2666](https://github.com/tikv/pd/pull/2666)時にTSOリクエストが失敗する場合があるバグを修正
    -   配置ルールが有効になっている場合、リージョンレプリカを最適な状態にスケジュールできない場合がある問題を修正します[#2720](https://github.com/tikv/pd/pull/2720)
    -   配置ルールが有効な場合に`Balance Leader`が機能しない問題を修正[#2726](https://github.com/tikv/pd/pull/2726)
    -   異常なストアがストア負荷統計からフィルタリングされない問題を修正[#2805](https://github.com/tikv/pd/pull/2805)

-   TiFlash

    -   データベースまたはテーブルの名前に特殊文字が含まれている場合、以前のバージョンからアップグレードした後、 TiFlash が正常に起動できない問題を修正
    -   初期化中に例外がスローされた場合、 TiFlashプロセスが終了できない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ概要ログ[#472](https://github.com/pingcap/br/pull/472)で合計 KV と合計バイト数が重複して計算される問題を修正しました。
        -   このモードに切り替えた後、最初の 5 分間インポート モードが機能しない問題を修正します[#473](https://github.com/pingcap/br/pull/473)

    -   Dumpling

        -   FTWRLロックが時間[#128](https://github.com/pingcap/dumpling/pull/128)に解除されない問題を修正

    -   TiCDC

        -   失敗した`changefeed`が削除できない問題を修正[#782](https://github.com/pingcap/tiflow/pull/782)
        -   ハンドル インデックス[#787](https://github.com/pingcap/tiflow/pull/787)として一意のインデックスを 1 つ選択して、無効な`delete`イベントを修正します。
        -   GCセーフポイントが停止`changefeed` [#797](https://github.com/pingcap/tiflow/pull/797)のチェックポイントを超えて転送されるバグを修正
        -   ネットワーク I/O 待機により終了するタスクがブロックされるバグを修正[#825](https://github.com/pingcap/tiflow/pull/825)
        -   不要なデータが誤って下流側に複製される場合があるバグを修正[#743](https://github.com/pingcap/tiflow/issues/743)

    -   TiDB Lightning

        -   TiDB バックエンド[#357](https://github.com/pingcap/tidb-lightning/pull/357)を使用する場合の空のバイナリ/16 進リテラルの構文エラーを修正しました。
