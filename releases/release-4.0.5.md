---
title: TiDB 4.0.5 Release Notes
---

# TiDB 4.0.5 リリースノート {#tidb-4-0-5-release-notes}

発売日：2020年8月31日

TiDB バージョン: 4.0.5

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   複数のパーティションの ID 配列をサポートするように`drop partition`と`truncate partition`のジョブ引数を変更します[#18930](https://github.com/pingcap/tidb/pull/18930)
    -   `add partition`レプリカをチェックするための削除のみの状態を追加します[#18865](https://github.com/pingcap/tidb/pull/18865)

## 新機能 {#new-features}

-   TiKV

    -   エラー[#8387](https://github.com/tikv/tikv/pull/8387)のエラー コードを定義します。

-   TiFlash

    -   TiDB との統合ログ形式をサポート

-   ツール

    -   TiCDC

        -   Kafka SSL 接続のサポート[#764](https://github.com/pingcap/tiflow/pull/764)
        -   古い値の出力をサポート[#708](https://github.com/pingcap/tiflow/pull/708)
        -   列フラグ[#796](https://github.com/pingcap/tiflow/pull/796)を追加します。
        -   以前のバージョンの DDL ステートメントとテーブル スキーマの出力をサポート[#799](https://github.com/pingcap/tiflow/pull/799)

## 改良点 {#improvements}

-   TiDB

    -   大きなユニオン クエリに対して`DecodePlan`のパフォーマンスを最適化する[#18941](https://github.com/pingcap/tidb/pull/18941)
    -   `Region cache miss`エラー発生時の GC ロックスキャン回数を減らす[#18876](https://github.com/pingcap/tidb/pull/18876)
    -   クラスターのパフォーマンスに対する統計的フィードバックの影響を緩和する[#18772](https://github.com/pingcap/tidb/pull/18772)
    -   RPC 応答が返される前の操作のキャンセルをサポート[#18580](https://github.com/pingcap/tidb/pull/18580)
    -   HTTP API を追加して TiDB メトリクス プロファイルを生成する[#18531](https://github.com/pingcap/tidb/pull/18531)
    -   分散分割テーブルのサポート[#17863](https://github.com/pingcap/tidb/pull/17863)
    -   Grafana [#18679](https://github.com/pingcap/tidb/pull/18679)の各インスタンスの詳細なメモリ使用量を追加
    -   `EXPLAIN` [#18892](https://github.com/pingcap/tidb/pull/18892)の結果で`BatchPointGet`演算子の詳細なランタイム情報を表示します
    -   `EXPLAIN` [#18817](https://github.com/pingcap/tidb/pull/18817)の結果で`PointGet`演算子の詳細なランタイム情報を表示します
    -   `remove()` [#18395](https://github.com/pingcap/tidb/pull/18395)分の`Consume`の潜在的なデッドロックを警告する
    -   `StrToInt`と`StrToFloat`の動作を改良し、JSON を`date` 、 `time` 、および`timestamp`型に変換することをサポートします[#18159](https://github.com/pingcap/tidb/pull/18159)
    -   `TableReader`オペレーター[#18392](https://github.com/pingcap/tidb/pull/18392)のメモリ使用量の制限をサポート
    -   `batch cop`リクエスト[#18999](https://github.com/pingcap/tidb/pull/18999)を再試行するときにバックオフが何度も発生しないようにする
    -   `ALTER TABLE`アルゴリズムの互換性を改善[#19270](https://github.com/pingcap/tidb/pull/19270)
    -   内側にシングルパーティションテーブルサポート`IndexJoin`を作成する[#19151](https://github.com/pingcap/tidb/pull/19151)
    -   ログに無効な行が含まれている場合でも、ログ ファイルの検索をサポート[#18579](https://github.com/pingcap/tidb/pull/18579)

-   PD

    -   特殊なエンジン ( TiFlashなど) を備えたストアでの領域の分散をサポート[#2706](https://github.com/tikv/pd/pull/2706)
    -   リージョン HTTP API をサポートして、特定のキー範囲[#2687](https://github.com/tikv/pd/pull/2687)のリージョンスケジューリングを優先します
    -   リージョン分散後のリーダー分布を改善する[#2684](https://github.com/tikv/pd/pull/2684)
    -   TSO 要求[#2678](https://github.com/tikv/pd/pull/2678)のテストとログをさらに追加します。
    -   リージョンのリーダーが変更された後の無効なキャッシュ更新を回避する[#2672](https://github.com/tikv/pd/pull/2672)
    -   `store.GetLimit`廃棄済みストアを返すことを許可するオプションを追加します[#2743](https://github.com/tikv/pd/pull/2743)
    -   PD リーダーとフォロワー間のリージョンリーダーの変更の同期をサポートします[#2795](https://github.com/tikv/pd/pull/2795)
    -   GC safepoint サービスをクエリするコマンドを追加します[#2797](https://github.com/tikv/pd/pull/2797)
    -   フィルター内の`region.Clone`呼び出しを置き換えて、パフォーマンスを向上させます[#2801](https://github.com/tikv/pd/pull/2801)
    -   リージョンフロー キャッシュの更新を無効にするオプションを追加して、大規模なクラスター[#2848](https://github.com/tikv/pd/pull/2848)のパフォーマンスを向上させます。

-   TiFlash

    -   CPU、I/O、RAM 使用量のメトリックとstorageエンジンのメトリックを表示するための Grafana パネルを追加します。
    -   Raftログの処理ロジックを最適化して I/O 操作を削減する
    -   ブロックされた`add partition` DDL ステートメントのリージョンスケジューリングを高速化する
    -   DeltaTree のデルタ データの圧縮を最適化して、読み取りと書き込みの増幅を減らします
    -   複数のスレッドを使用してスナップショットを前処理することにより、リージョンのスナップショットを適用するパフォーマンスを最適化します
    -   TiFlashの読み取り負荷が低いときにファイル記述子を開く数を最適化して、システム リソースの消費を削減します。
    -   TiFlash の再起動時に作成される不要な小さなファイルの数を最適化します
    -   データstorageの保存時の暗号化をサポート
    -   データ転送用の TLS をサポート

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

    -   `builtinCastRealAsDecimalSig`関数で`ErrTruncate/Overflow`エラーが誤って処理されるために発生する`should ensure all columns have the same length`エラーを修正します[#18967](https://github.com/pingcap/tidb/pull/18967)
    -   パーティションテーブル[#18837](https://github.com/pingcap/tidb/pull/18837)で`pre_split_regions`テーブル オプションが機能しない問題を修正します。
    -   大規模なトランザクションが途中で終了する可能性がある問題を修正します[#18813](https://github.com/pingcap/tidb/pull/18813)
    -   `collation`関数を使用すると間違ったクエリ結果が得られる問題を修正[#18735](https://github.com/pingcap/tidb/pull/18735)
    -   `getAutoIncrementID()`関数が`tidb_snapshot`セッション変数を考慮しないというバグを修正します。これにより、ダンパー ツールが`table not exist`エラー[#18692](https://github.com/pingcap/tidb/pull/18692)で失敗する可能性があります。
    -   `select a from t having t.a` [#18434](https://github.com/pingcap/tidb/pull/18434)のような SQL ステートメントの`unknown column error`を修正します
    -   パーティション キーが整数型[#18186](https://github.com/pingcap/tidb/pull/18186)の場合、64 ビットの符号なし型をハッシュパーティションテーブルに書き込むとオーバーフローが発生し、予期しない負の数が返されるというpanicの問題を修正します。
    -   `char`関数の間違った動作を修正[#18122](https://github.com/pingcap/tidb/pull/18122)
    -   `ADMIN REPAIR TABLE`ステートメントが範囲パーティション[#17988](https://github.com/pingcap/tidb/pull/17988)の式で整数を解析できないという問題を修正します
    -   `SET CHARSET`ステートメント[#17289](https://github.com/pingcap/tidb/pull/17289)の間違った動作を修正します。
    -   `collation`関数[#17231](https://github.com/pingcap/tidb/pull/17231)の間違った結果につながる間違った照合順序設定によって引き起こされたバグを修正します。
    -   `STR_TO_DATE`のフォーマット トークン &#39;%r&#39;、&#39;%h&#39; の処理が MySQL [#18727](https://github.com/pingcap/tidb/pull/18727)の処理と矛盾する問題を修正
    -   `cluster_info`テーブルの TiDB のバージョン情報が PD/TiKV のバージョン情報と一致しない問題を修正[#18413](https://github.com/pingcap/tidb/pull/18413)
    -   悲観的トランザクションの既存のチェックを修正します[#19004](https://github.com/pingcap/tidb/pull/19004)
    -   `union select for update`を実行すると同時競合[#19006](https://github.com/pingcap/tidb/pull/19006)が発生する可能性がある問題を修正
    -   `apply`に`PointGet`演算子[#19046](https://github.com/pingcap/tidb/pull/19046)の子がある場合の間違ったクエリ結果を修正
    -   `IndexLookUp` `Apply`演算子[#19496](https://github.com/pingcap/tidb/pull/19496)の内側にある場合に発生する誤った結果を修正します。
    -   `anti-semi-join`クエリの誤った結果を修正する[#19472](https://github.com/pingcap/tidb/pull/19472)
    -   `BatchPointGet` [#19456](https://github.com/pingcap/tidb/pull/19456)の誤った使用による誤った結果を修正
    -   `UnionScan` `Apply`演算子[#19496](https://github.com/pingcap/tidb/pull/19496)の内側にある場合に発生する誤った結果を修正します。
    -   `EXECUTE`ステートメントを使用して高価なクエリ ログ[#17419](https://github.com/pingcap/tidb/pull/17419)を出力することによって引き起こされるpanicを修正します。
    -   結合キーが`ENUM`または`SET` [#19235](https://github.com/pingcap/tidb/pull/19235)の場合のインデックス結合エラーを修正
    -   インデックス列[#19358](https://github.com/pingcap/tidb/pull/19358)に`NULL`値が存在する場合、クエリ範囲を構築できない問題を修正
    -   グローバル構成の更新によって発生するデータ競合の問題を修正します[#17964](https://github.com/pingcap/tidb/pull/17964)
    -   大文字のスキーマで文字セットを変更するときに発生するpanicの問題を修正します[#19286](https://github.com/pingcap/tidb/pull/19286)
    -   ディスク スピル アクション中に一時ディレクトリを変更することによって発生する予期しないエラーを修正します[#18970](https://github.com/pingcap/tidb/pull/18970)
    -   [#19131](https://github.com/pingcap/tidb/pull/19131)進数型の間違ったハッシュ キーを修正します。
    -   `PointGet`および`BatchPointGet`演算子がパーティション選択構文を考慮せず、誤った結果が得られる問題を修正します[#19141](https://github.com/pingcap/tidb/issues/19141)
    -   `Apply`演算子を`UnionScan`演算子[#19104](https://github.com/pingcap/tidb/issues/19104)と一緒に使用した場合の誤った結果を修正します。
    -   インデックス付き仮想生成列が間違った値[#17989](https://github.com/pingcap/tidb/issues/17989)を返すバグを修正
    -   ランタイム統計のロックを追加して、同時実行によるpanicを修正します[#18983](https://github.com/pingcap/tidb/pull/18983)

-   TiKV

    -   Hibernate リージョンが有効な場合にリーダー選出を高速化する[#8292](https://github.com/tikv/tikv/pull/8292)
    -   スケジュール[#8357](https://github.com/tikv/tikv/pull/8357)中のメモリリークの問題を修正します。
    -   リーダーがあまりにも早く休止状態になるのを防ぐために、 `hibernate-timeout`構成項目を追加します[#8208](https://github.com/tikv/tikv/pull/8208)

-   PD

    -   リーダー交代時にTSOリクエストが失敗する場合がある不具合を修正[#2666](https://github.com/tikv/pd/pull/2666)
    -   配置ルールが有効になっている場合、リージョンレプリカを最適な状態にスケジュールできないことがある問題を修正します[#2720](https://github.com/tikv/pd/pull/2720)
    -   配置ルールが有効な場合に`Balance Leader`が機能しない問題を修正します[#2726](https://github.com/tikv/pd/pull/2726)
    -   異常なストアがストア負荷統計から除外されない問題を修正します[#2805](https://github.com/tikv/pd/pull/2805)

-   TiFlash

    -   データベースまたはテーブルの名前に特殊文字が含まれている場合、以前のバージョンからアップグレードした後、 TiFlash が正常に起動できない問題を修正します。
    -   初期化中に例外がスローされると、 TiFlashプロセスが終了できない問題を修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ サマリー ログ[#472](https://github.com/pingcap/br/pull/472)で合計 KV と合計バイト数の計算が重複する問題を修正します。
        -   このモードに切り替えた後、最初の 5 分間はインポート モードが機能しないという問題を修正します[#473](https://github.com/pingcap/br/pull/473)

    -   Dumpling

        -   FTWRL ロックが時間内に解除されない問題を修正[#128](https://github.com/pingcap/dumpling/pull/128)

    -   TiCDC

        -   失敗した`changefeed`が削除できない問題を修正[#782](https://github.com/pingcap/tiflow/pull/782)
        -   ハンドル インデックス[#787](https://github.com/pingcap/tiflow/pull/787)として 1 つの一意のインデックスを選択して、無効な`delete`イベントを修正します。
        -   停止した`changefeed` [#797](https://github.com/pingcap/tiflow/pull/797)のチェックポイントを超えて GC セーフポイントが転送されるバグを修正
        -   ネットワーク I/O 待機がタスクの終了をブロックするバグを修正します[#825](https://github.com/pingcap/tiflow/pull/825)
        -   一部の不要なデータが誤ってダウンストリームに複製される可能性があるバグを修正します[#743](https://github.com/pingcap/tiflow/issues/743)

    -   TiDB Lightning

        -   TiDB バックエンド[#357](https://github.com/pingcap/tidb-lightning/pull/357)使用時の空のバイナリ/16 進リテラルの構文エラーを修正
