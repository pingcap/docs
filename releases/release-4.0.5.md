---
title: TiDB 4.0.5 Release Notes
summary: TiDB 4.0.5は2020年8月31日にリリースされました。この新バージョンには、互換性の変更、新機能、改善、バグ修正、そしてTiKV、 TiFlash、ツール、PD、 TiDB Lightningのアップデートが含まれています。主な変更点としては、TiDBとの統合ログ形式のサポート、パフォーマンスの最適化、様々な問題に対するバグ修正、 TiFlash内のデータstorageにおける保存時暗号化のサポートなどが挙げられます。
---

# TiDB 4.0.5 リリースノート {#tidb-4-0-5-release-notes}

発売日：2020年8月31日

TiDB バージョン: 4.0.5

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `drop partition`と`truncate partition`のジョブ引数を変更して、複数のパーティション[＃18930](https://github.com/pingcap/tidb/pull/18930)のID配列をサポートする
    -   `add partition`レプリカ[＃18865](https://github.com/pingcap/tidb/pull/18865)をチェックするための削除専用状態を追加します

## 新機能 {#new-features}

-   TiKV

    -   エラー[＃8387](https://github.com/tikv/tikv/pull/8387)のエラーコードを定義する

-   TiFlash

    -   TiDBによる統合ログ形式をサポート

-   ツール

    -   TiCDC

        -   Kafka SSL 接続[＃764](https://github.com/pingcap/tiflow/pull/764)サポート
        -   古い値[＃708](https://github.com/pingcap/tiflow/pull/708)出力をサポート
        -   列フラグ[＃796](https://github.com/pingcap/tiflow/pull/796)を追加する
        -   以前のバージョン[＃799](https://github.com/pingcap/tiflow/pull/799)の DDL ステートメントとテーブル スキーマの出力をサポート

## 改善点 {#improvements}

-   TiDB

    -   大規模なユニオンクエリ`DecodePlan`のパフォーマンスを最適化します[＃18941](https://github.com/pingcap/tidb/pull/18941)
    -   `Region cache miss`エラー発生時の GC ロックスキャン回数を減らす[＃18876](https://github.com/pingcap/tidb/pull/18876)
    -   統計フィードバックがクラスターパフォーマンスに与える影響を軽減する[＃18772](https://github.com/pingcap/tidb/pull/18772)
    -   RPC応答が返される前に操作をキャンセルする機能をサポート[＃18580](https://github.com/pingcap/tidb/pull/18580)
    -   TiDBメトリックプロファイル[＃18531](https://github.com/pingcap/tidb/pull/18531)を生成するためのHTTP APIを追加する
    -   分散パーティションテーブルのサポート[＃17863](https://github.com/pingcap/tidb/pull/17863)
    -   Grafana [＃18679](https://github.com/pingcap/tidb/pull/18679)で各インスタンスの詳細なメモリ使用量を追加する
    -   `EXPLAIN` [＃18892](https://github.com/pingcap/tidb/pull/18892)の結果の`BatchPointGet`の演算子の詳細な実行時間情報を表示します
    -   `EXPLAIN` [＃18817](https://github.com/pingcap/tidb/pull/18817)の結果の`PointGet`の演算子の詳細な実行時間情報を表示します
    -   `remove()` [＃18395](https://github.com/pingcap/tidb/pull/18395)の`Consume`潜在的なデッドロックを警告する
    -   `StrToInt`と`StrToFloat`の動作を改良し、JSON を`date` 、 `time` 、 `timestamp`型に変換することをサポートする[＃18159](https://github.com/pingcap/tidb/pull/18159)
    -   `TableReader`演算子[＃18392](https://github.com/pingcap/tidb/pull/18392)のメモリ使用量の制限をサポート
    -   `batch cop`リクエスト[＃18999](https://github.com/pingcap/tidb/pull/18999)を再試行する際にバックオフを何度も行わないようにする
    -   `ALTER TABLE`アルゴリズム[＃19270](https://github.com/pingcap/tidb/pull/19270)の互換性を向上
    -   単一のパーティションテーブルを内側[＃19151](https://github.com/pingcap/tidb/pull/19151)に`IndexJoin`サポートします
    -   ログに無効な行が含まれている場合でもログファイルの検索をサポート[＃18579](https://github.com/pingcap/tidb/pull/18579)

-   PD

    -   特別なエンジン（ TiFlashなど）を備えた店舗での散乱領域のサポート[＃2706](https://github.com/tikv/pd/pull/2706)
    -   特定のキー範囲[＃2687](https://github.com/tikv/pd/pull/2687)のリージョンスケジュールを優先するリージョンHTTP API をサポートします。
    -   リージョン分散[＃2684](https://github.com/tikv/pd/pull/2684)後のリーダー分布の改善
    -   TSOリクエスト[＃2678](https://github.com/tikv/pd/pull/2678)テストとログを追加する
    -   リージョンのリーダーが変更された後の無効なキャッシュ更新を回避する[＃2672](https://github.com/tikv/pd/pull/2672)
    -   `store.GetLimit`墓石ストア[＃2743](https://github.com/tikv/pd/pull/2743)を返却できるようにするオプションを追加します
    -   PDリーダーとフォロワー間のリージョンリーダーの変更の同期をサポート[＃2795](https://github.com/tikv/pd/pull/2795)
    -   GCセーフポイントサービス[＃2797](https://github.com/tikv/pd/pull/2797)照会するためのコマンドを追加する
    -   パフォーマンスを向上させるためにフィルターの`region.Clone`の呼び出しを置き換えます[＃2801](https://github.com/tikv/pd/pull/2801)
    -   大規模クラスタのパフォーマンスを向上させるために、リージョンフローキャッシュの更新を無効にするオプションを追加します[＃2848](https://github.com/tikv/pd/pull/2848)

-   TiFlash

    -   CPU、I/O、RAMの使用状況やstorageエンジンのメトリクスを表示するためのGrafanaパネルを追加します。
    -   Raftログの処理ロジックを最適化することでI/O操作を削減
    -   ブロックされた`add partition` DDL文のリージョンスケジュールを高速化する
    -   DeltaTree のデルタデータの圧縮を最適化して、読み取りと書き込みの増幅を削減します。
    -   複数のスレッドを使用してスナップショットを前処理することにより、リージョンショットの適用パフォーマンスを最適化します。
    -   TiFlashの読み取り負荷が低いときに開くファイル記述子の数を最適化して、システムリソースの消費を削減します。
    -   TiFlashの再起動時に作成される不要な小さなファイルの数を最適化します
    -   データstorage時の暗号化をサポート
    -   データ転送にTLSをサポート

-   ツール

    -   TiCDC

        -   TSO [＃801](https://github.com/pingcap/tiflow/pull/801)取得頻度を下げる

    -   バックアップと復元 (BR)

        -   いくつかのログを最適化する[＃428](https://github.com/pingcap/br/pull/428)

    -   Dumpling

        -   MySQL [＃121](https://github.com/pingcap/dumpling/pull/121)のロック時間を短縮するために、接続が作成された後に FTWRL を解放します。

    -   TiDB Lightning

        -   いくつかのログを最適化する[＃352](https://github.com/pingcap/tidb-lightning/pull/352)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `builtinCastRealAsDecimalSig`関数[＃18967](https://github.com/pingcap/tidb/pull/18967)で`ErrTruncate/Overflow`エラーが誤って処理されるために発生する`should ensure all columns have the same length`エラーを修正します。
    -   パーティションテーブル[＃18837](https://github.com/pingcap/tidb/pull/18837)で`pre_split_regions`テーブルオプションが機能しない問題を修正
    -   大規模なトランザクションが途中で終了する可能性がある問題を修正[＃18813](https://github.com/pingcap/tidb/pull/18813)
    -   `collation`関数を使用すると間違ったクエリ結果が返される問題を修正[＃18735](https://github.com/pingcap/tidb/pull/18735)
    -   `getAutoIncrementID()`関数が`tidb_snapshot`セッション変数を考慮しないバグを修正しました。これにより、ダンパーツールが`table not exist`エラー[＃18692](https://github.com/pingcap/tidb/pull/18692)で失敗する可能性があります。
    -   SQL文の`unknown column error` `select a from t having t.a` [＃18434](https://github.com/pingcap/tidb/pull/18434)のように修正する
    -   パーティションキーが整数型[＃18186](https://github.com/pingcap/tidb/pull/18186)の場合、64 ビットの符号なし型をハッシュパーティションテーブルに書き込むとオーバーフローが発生し、予期しない負の数になるというpanic問題を修正しました。
    -   `char`関数[＃18122](https://github.com/pingcap/tidb/pull/18122)の誤った動作を修正
    -   `ADMIN REPAIR TABLE`文が範囲パーティション[＃17988](https://github.com/pingcap/tidb/pull/17988)式内の整数を解析できない問題を修正しました
    -   `SET CHARSET`文[＃17289](https://github.com/pingcap/tidb/pull/17289)の誤った動作を修正する
    -   間違った照合順序設定によって関数`collation`の間違った結果が発生するバグを修正しました[＃17231](https://github.com/pingcap/tidb/pull/17231)
    -   `STR_TO_DATE`のフォーマットトークン &#39;%r&#39;、 &#39;%h&#39; の処理が MySQL [＃18727](https://github.com/pingcap/tidb/pull/18727)と矛盾している問題を修正しました。
    -   `cluster_info`表[＃18413](https://github.com/pingcap/tidb/pull/18413)の TiDB バージョン情報が PD/TiKV のバージョン情報と一致しない問題を修正しました。
    -   悲観的トランザクションの既存のチェックを修正[＃19004](https://github.com/pingcap/tidb/pull/19004)
    -   `union select for update`実行すると同時競合[＃19006](https://github.com/pingcap/tidb/pull/19006)発生する可能性がある問題を修正
    -   `apply` `PointGet`演算子[＃19046](https://github.com/pingcap/tidb/pull/19046)の子がある場合の間違ったクエリ結果を修正しました
    -   `IndexLookUp` `Apply`演算子[＃19496](https://github.com/pingcap/tidb/pull/19496)の内側にある場合に発生する誤った結果を修正します。
    -   `anti-semi-join`クエリ[＃19472](https://github.com/pingcap/tidb/pull/19472)の誤った結果を修正
    -   `BatchPointGet` [＃19456](https://github.com/pingcap/tidb/pull/19456)の誤った使用法によって生じた誤った結果を修正
    -   `UnionScan` `Apply`演算子[＃19496](https://github.com/pingcap/tidb/pull/19496)の内側にある場合に発生する誤った結果を修正します。
    -   `EXECUTE`文を使用して高価なクエリログ[＃17419](https://github.com/pingcap/tidb/pull/17419)を出力することで発生するpanicを修正
    -   結合キーが`ENUM`または`SET`場合のインデックス結合エラーを修正しました[＃19235](https://github.com/pingcap/tidb/pull/19235)
    -   インデックス列[＃19358](https://github.com/pingcap/tidb/pull/19358)に`NULL`値が存在する場合にクエリ範囲を構築できない問題を修正しました
    -   グローバル構成の更新によって発生するデータ競合の問題を修正[＃17964](https://github.com/pingcap/tidb/pull/17964)
    -   大文字スキーマ[＃19286](https://github.com/pingcap/tidb/pull/19286)で文字セットを変更するときに発生するpanic問題を修正
    -   ディスクスピルアクション[＃18970](https://github.com/pingcap/tidb/pull/18970)中に一時ディレクトリを変更することによって発生する予期しないエラーを修正しました
    -   10進数型[＃19131](https://github.com/pingcap/tidb/pull/19131)の間違ったハッシュキーを修正
    -   `PointGet`と`BatchPointGet`演算子がパーティション選択構文を考慮せず、誤った結果を得る問題を修正しました[＃19141](https://github.com/pingcap/tidb/issues/19141)
    -   `Apply`演算子と`UnionScan`演算子[＃19104](https://github.com/pingcap/tidb/issues/19104)を一緒に使用した場合の誤った結果を修正
    -   インデックス付き仮想生成列が間違った値を返すバグを修正[＃17989](https://github.com/pingcap/tidb/issues/17989)
    -   同時実行によるpanicを修正するために実行時統計のロックを追加します[＃18983](https://github.com/pingcap/tidb/pull/18983)

-   TiKV

    -   Hibernate リージョンが有効な場合のリーダー選出を高速化[＃8292](https://github.com/tikv/tikv/pull/8292)
    -   スケジュール[＃8357](https://github.com/tikv/tikv/pull/8357)中のメモリリークの問題を修正
    -   リーダーがすぐに休止状態にならないようにするための`hibernate-timeout`構成項目を追加します[＃8208](https://github.com/tikv/tikv/pull/8208)

-   PD

    -   リーダー交代時にTSOリクエストが失敗する可能性があるバグを修正[＃2666](https://github.com/tikv/pd/pull/2666)
    -   配置ルールが有効になっているときに、リージョンレプリカを最適な状態にスケジュールできないことがある問題を修正しました[＃2720](https://github.com/tikv/pd/pull/2720)
    -   配置ルールが有効になっているときに`Balance Leader`機能しない問題を修正[＃2726](https://github.com/tikv/pd/pull/2726)
    -   不健全なストアがストア負荷統計からフィルタリングされない問題を修正[＃2805](https://github.com/tikv/pd/pull/2805)

-   TiFlash

    -   データベースまたはテーブルの名前に特殊文字が含まれている場合、以前のバージョンからアップグレードした後にTiFlash が正常に起動できない問題を修正しました。
    -   初期化中に例外がスローされた場合にTiFlashプロセスを終了できない問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ概要ログ[＃472](https://github.com/pingcap/br/pull/472)で合計 KV と合計バイト数が重複して計算される問題を修正しました
        -   このモードに切り替えてから最初の5分間はインポートモードが機能しない問題を修正しました[＃473](https://github.com/pingcap/br/pull/473)

    -   Dumpling

        -   FTWRLロックが時間内に解除されない問題を修正[＃128](https://github.com/pingcap/dumpling/pull/128)

    -   TiCDC

        -   失敗した`changefeed`削除できない問題を修正[＃782](https://github.com/pingcap/tiflow/pull/782)
        -   ハンドルインデックス[＃787](https://github.com/pingcap/tiflow/pull/787)として1つの一意のインデックスを選択して無効なイベント`delete`修正します
        -   GCセーフポイントが停止した`changefeed` [＃797](https://github.com/pingcap/tiflow/pull/797)のチェックポイントを超えて転送されるバグを修正
        -   ネットワークI/O待機によりタスクの終了がブロックされるバグを修正[＃825](https://github.com/pingcap/tiflow/pull/825)
        -   不要なデータが誤って下流に複製される可能性があるバグを修正[＃743](https://github.com/pingcap/tiflow/issues/743)

    -   TiDB Lightning

        -   TiDBバックエンド[＃357](https://github.com/pingcap/tidb-lightning/pull/357)使用時の空のバイナリ/16進リテラルの構文エラーを修正
