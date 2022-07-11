---
title: TiDB 4.0.5 Release Notes
---

# TiDB4.0.5リリースノート {#tidb-4-0-5-release-notes}

発売日：2020年8月31日

TiDBバージョン：4.0.5

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   複数のパーティションのID配列をサポートするように`drop partition`と`truncate partition`のジョブ引数を変更します[＃18930](https://github.com/pingcap/tidb/pull/18930)
    -   `add partition`のレプリカをチェックするための削除専用状態を追加します[＃18865](https://github.com/pingcap/tidb/pull/18865)

## 新機能 {#new-features}

-   TiKV

    -   エラーのエラーコードを定義する[＃8387](https://github.com/tikv/tikv/pull/8387)

-   TiFlash

    -   TiDBで統合ログ形式をサポートする

-   ツール

    -   TiCDC

        -   KafkaSSL接続をサポート[＃764](https://github.com/pingcap/tiflow/pull/764)
        -   古い値の出力をサポート[＃708](https://github.com/pingcap/tiflow/pull/708)
        -   列フラグを追加する[＃796](https://github.com/pingcap/tiflow/pull/796)
        -   以前のバージョン[＃799](https://github.com/pingcap/tiflow/pull/799)のDDLステートメントとテーブルスキーマの出力をサポートします

## 改善 {#improvements}

-   TiDB

    -   大きなユニオンクエリに対して`DecodePlan`のパフォーマンスを最適化する[＃18941](https://github.com/pingcap/tidb/pull/18941)
    -   `Region cache miss`のエラーが発生したときにGCロックスキャンの数を減らします[＃18876](https://github.com/pingcap/tidb/pull/18876)
    -   統計的フィードバックがクラスタのパフォーマンスに与える影響を緩和する[＃18772](https://github.com/pingcap/tidb/pull/18772)
    -   RPC応答が返される前のキャンセル操作をサポート[＃18580](https://github.com/pingcap/tidb/pull/18580)
    -   HTTP APIを追加して、TiDBメトリックプロファイルを生成します[＃18531](https://github.com/pingcap/tidb/pull/18531)
    -   分割テーブルの分散をサポート[＃17863](https://github.com/pingcap/tidb/pull/17863)
    -   Grafana1の各インスタンスの詳細なメモリ使用量を追加し[＃18679](https://github.com/pingcap/tidb/pull/18679)
    -   [＃18892](https://github.com/pingcap/tidb/pull/18892)の結果に`BatchPointGet`演算子の詳細な実行時情報を表示し`EXPLAIN`
    -   [＃18817](https://github.com/pingcap/tidb/pull/18817)の結果に`PointGet`演算子の詳細な実行時情報を表示し`EXPLAIN`
    -   [＃18395](https://github.com/pingcap/tidb/pull/18395) `remove()`の`Consume`の潜在的なデッドロックを警告する
    -   `StrToInt`と`StrToFloat`の動作を[＃18159](https://github.com/pingcap/tidb/pull/18159)し、JSONを`date` 、および`time`タイプに変換することをサポートします`timestamp`
    -   `TableReader`オペレーターのメモリ使用量の制限をサポート[＃18392](https://github.com/pingcap/tidb/pull/18392)
    -   `batch cop`のリクエストを再試行するときにバックオフを何度も回避する[＃18999](https://github.com/pingcap/tidb/pull/18999)
    -   `ALTER TABLE`アルゴリズムの互換性を向上させる[＃19270](https://github.com/pingcap/tidb/pull/19270)
    -   内側の単一パーティションテーブルサポート`IndexJoin`を作成します[＃19151](https://github.com/pingcap/tidb/pull/19151)
    -   ログに無効な行が含まれている場合でもログファイルの検索をサポート[＃18579](https://github.com/pingcap/tidb/pull/18579)

-   PD

    -   特別なエンジン（TiFlashなど）を備えた店舗での散乱領域のサポート[＃2706](https://github.com/tikv/pd/pull/2706)
    -   リージョンHTTPAPIをサポートして、特定のキー範囲のリージョンスケジューリングに優先順位を付けます[＃2687](https://github.com/tikv/pd/pull/2687)
    -   領域散乱後のリーダー分布を改善する[＃2684](https://github.com/tikv/pd/pull/2684)
    -   TSOリクエストのテストとログをさらに追加する[＃2678](https://github.com/tikv/pd/pull/2678)
    -   リージョンのリーダーが変更された後の無効なキャッシュ更新を回避する[＃2672](https://github.com/tikv/pd/pull/2672)
    -   `store.GetLimit`がトゥームストーンストアを返すことを許可するオプションを追加します[＃2743](https://github.com/tikv/pd/pull/2743)
    -   PDリーダーとフォロワーの間でリージョンリーダーの変更を同期することをサポートする[＃2795](https://github.com/tikv/pd/pull/2795)
    -   GCセーフポイントサービスをクエリするためのコマンドを追加する[＃2797](https://github.com/tikv/pd/pull/2797)
    -   パフォーマンスを向上させるために、フィルターの`region.Clone`の呼び出しを置き換えます[＃2801](https://github.com/tikv/pd/pull/2801)
    -   大規模クラスタのパフォーマンスを向上させるために、リージョンフローキャッシュの更新を無効にするオプションを追加します[＃2848](https://github.com/tikv/pd/pull/2848)

-   TiFlash

    -   Grafanaパネルをさらに追加して、CPU、I / O、RAM使用量のメトリック、およびストレージエンジンのメトリックを表示します
    -   Raftログの処理ロジックを最適化することにより、I/O操作を削減します
    -   ブロックされた`add partition`ステートメントのリージョンスケジューリングを高速化
    -   DeltaTreeのデルタデータの圧縮を最適化して、読み取りと書き込みの増幅を減らします
    -   複数のスレッドを使用してスナップショットを前処理することにより、リージョンスナップショットを適用するパフォーマンスを最適化します
    -   TiFlashの読み取り負荷が低いときに開くファイル記述子の数を最適化して、システムリソースの消費を削減します
    -   TiFlashの再起動時に作成される不要な小さなファイルの数を最適化する
    -   データストレージの保存時の暗号化をサポート
    -   データ転送にTLSをサポート

-   ツール

    -   TiCDC

        -   [＃801](https://github.com/pingcap/tiflow/pull/801)を取得する頻度を下げる

    -   バックアップと復元（BR）

        -   一部のログを最適化する[＃428](https://github.com/pingcap/br/pull/428)

    -   Dumpling

        -   MySQL [＃121](https://github.com/pingcap/dumpling/pull/121)のロック時間を短縮するために、接続が作成された後にFTWRLを解放します

    -   TiDB Lightning

        -   一部のログを最適化する[＃352](https://github.com/pingcap/tidb-lightning/pull/352)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `builtinCastRealAsDecimalSig`関数[＃18967](https://github.com/pingcap/tidb/pull/18967)で`ErrTruncate/Overflow`エラーが正しく処理されなかったために発生した`should ensure all columns have the same length`エラーを修正します。
    -   `pre_split_regions`テーブルオプションがパーティションテーブル[＃18837](https://github.com/pingcap/tidb/pull/18837)で機能しない問題を修正します
    -   大規模なトランザクションが途中で終了する可能性がある問題を修正します[＃18813](https://github.com/pingcap/tidb/pull/18813)
    -   `collation`関数を使用すると間違ったクエリ結果が得られる問題を修正します[＃18735](https://github.com/pingcap/tidb/pull/18735)
    -   `getAutoIncrementID()`関数が`tidb_snapshot`セッション変数を考慮しないというバグを修正します。これにより、ダンパーツールが`table not exist`エラー[＃18692](https://github.com/pingcap/tidb/pull/18692)で失敗する可能性があります。
    -   [＃18434](https://github.com/pingcap/tidb/pull/18434)のようなSQLステートメントの`unknown column error`を修正し`select a from t having t.a`
    -   パーティションキーが整数型[＃18186](https://github.com/pingcap/tidb/pull/18186)の場合、64ビットの符号なし型をハッシュパーティションテーブルに書き込むとオーバーフローが発生し、予期しない負の数が発生するというpanicの問題を修正します。
    -   `char`関数[＃18122](https://github.com/pingcap/tidb/pull/18122)の間違った動作を修正します
    -   `ADMIN REPAIR TABLE`ステートメントが範囲パーティション[＃17988](https://github.com/pingcap/tidb/pull/17988)の式の整数を解析できない問題を修正します
    -   `SET CHARSET`ステートメント[＃17289](https://github.com/pingcap/tidb/pull/17289)の誤った動作を修正します
    -   `collation`関数[＃17231](https://github.com/pingcap/tidb/pull/17231)の間違った結果につながる間違った照合順序設定によって引き起こされたバグを修正します
    -   フォーマットトークン&#39;％r&#39;、&#39;％h&#39;の`STR_TO_DATE`の処理がMySQL3の処理と矛盾する問題を修正し[＃18727](https://github.com/pingcap/tidb/pull/18727)
    -   TiDBのバージョン情報が`cluster_info`表[＃18413](https://github.com/pingcap/tidb/pull/18413)のPD/TiKVのバージョン情報と矛盾する問題を修正します。
    -   悲観的なトランザクションの既存のチェックを修正する[＃19004](https://github.com/pingcap/tidb/pull/19004)
    -   `union select for update`を実行すると同時レース[＃19006](https://github.com/pingcap/tidb/pull/19006)が発生する可能性がある問題を修正します
    -   `apply`に`PointGet`演算子[＃19046](https://github.com/pingcap/tidb/pull/19046)の子がある場合の誤ったクエリ結果を修正します
    -   `IndexLookUp`が`Apply`演算子[＃19496](https://github.com/pingcap/tidb/pull/19496)の内側にあるときに発生する誤った結果を修正します
    -   `anti-semi-join`クエリの誤った結果を修正[＃19472](https://github.com/pingcap/tidb/pull/19472)
    -   [＃19456](https://github.com/pingcap/tidb/pull/19456)の誤った使用によって引き起こされた誤った結果を修正し`BatchPointGet`
    -   `UnionScan`が`Apply`演算子[＃19496](https://github.com/pingcap/tidb/pull/19496)の内側にあるときに発生する誤った結果を修正します
    -   `EXECUTE`ステートメントを使用して高価なクエリログ[＃17419](https://github.com/pingcap/tidb/pull/17419)を出力することによって引き起こされるpanicを修正します
    -   結合キーが`ENUM`または`SET`の場合のインデックス結合エラーを修正し[＃19235](https://github.com/pingcap/tidb/pull/19235)た
    -   インデックス列[＃19358](https://github.com/pingcap/tidb/pull/19358)に`NULL`の値が存在する場合、クエリ範囲を構築できない問題を修正します。
    -   グローバル構成の更新によって引き起こされるデータ競合の問題を修正します[＃17964](https://github.com/pingcap/tidb/pull/17964)
    -   大文字スキーマ[＃19286](https://github.com/pingcap/tidb/pull/19286)の文字セットを変更するときに発生するpanicの問題を修正します
    -   ディスクスピルアクション中に一時ディレクトリを変更することによって引き起こされる予期しないエラーを修正します[＃18970](https://github.com/pingcap/tidb/pull/18970)
    -   10進タイプ[＃19131](https://github.com/pingcap/tidb/pull/19131)の間違ったハッシュキーを修正します
    -   `PointGet`および`BatchPointGet`演算子がパーティション選択構文を考慮せず、誤った結果を取得する問題を修正します[＃19141](https://github.com/pingcap/tidb/issues/19141)
    -   `Apply`演算子を`UnionScan`演算子と一緒に使用した場合の誤った結果を修正します[＃19104](https://github.com/pingcap/tidb/issues/19104)
    -   インデックス付きの仮想生成列が間違った値を返す原因となるバグを修正します[＃17989](https://github.com/pingcap/tidb/issues/17989)
    -   実行時統計のロックを追加して、同時実行によって引き起こされるpanicを修正します[＃18983](https://github.com/pingcap/tidb/pull/18983)

-   TiKV

    -   Hibernateリージョンが有効になっている場合のリーダー選挙のスピードアップ[＃8292](https://github.com/tikv/tikv/pull/8292)
    -   スケジューリング中のメモリリークの問題を修正[＃8357](https://github.com/tikv/tikv/pull/8357)
    -   リーダーが休止状態になるのが速すぎるのを防ぐために、 `hibernate-timeout`の構成アイテムを追加します[＃8208](https://github.com/tikv/tikv/pull/8208)

-   PD

    -   リーダーの変更時にTSOリクエストが失敗する可能性があるバグを修正します[＃2666](https://github.com/tikv/pd/pull/2666)
    -   配置ルールが有効になっている場合、リージョンレプリカを最適な状態にスケジュールできないことがある問題を修正します[＃2720](https://github.com/tikv/pd/pull/2720)
    -   配置ルールが有効になっていると`Balance Leader`が機能しない問題を修正します[＃2726](https://github.com/tikv/pd/pull/2726)
    -   異常なストアがストアの負荷統計からフィルタリングされない問題を修正します[＃2805](https://github.com/tikv/pd/pull/2805)

-   TiFlash

    -   データベースまたはテーブルの名前に特殊文字が含まれている場合、以前のバージョンからアップグレードした後、TiFlashが正常に起動しない問題を修正します
    -   初期化中に例外がスローされた場合にTiFlashプロセスが終了できない問題を修正します

-   ツール

    -   バックアップと復元（BR）

        -   バックアップサマリーログ[＃472](https://github.com/pingcap/br/pull/472)の合計KVと合計バイトの重複計算の問題を修正します。
        -   このモードに切り替えてから最初の5分間はインポートモードが機能しないという問題を修正します[＃473](https://github.com/pingcap/br/pull/473)

    -   Dumpling

        -   FTWRLロックが時間[＃128](https://github.com/pingcap/dumpling/pull/128)で解放されない問題を修正します

    -   TiCDC

        -   失敗した`changefeed`を削除できないという問題を修正します[＃782](https://github.com/pingcap/tiflow/pull/782)
        -   ハンドルインデックス[＃787](https://github.com/pingcap/tiflow/pull/787)として1つの一意のインデックスを選択することにより、無効な`delete`イベントを修正します。
        -   GCセーフポイントが停止した`changefeed`のチェックポイントを超えて転送されるバグを修正し[＃797](https://github.com/pingcap/tiflow/pull/797)
        -   ネットワークI/O待機がタスクの終了をブロックするバグを修正します[＃825](https://github.com/pingcap/tiflow/pull/825)
        -   一部の不要なデータが誤ってダウンストリームに複製される可能性があるバグを修正します[＃743](https://github.com/pingcap/tiflow/issues/743)

    -   TiDB Lightning

        -   TiDBバックエンド[＃357](https://github.com/pingcap/tidb-lightning/pull/357)を使用する場合の空のバイナリ/16進リテラルの構文エラーを修正しました
