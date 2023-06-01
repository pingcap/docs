---
title: TiDB 4.0 GA Release Notes
---

# TiDB 4.0 GA リリース ノート {#tidb-4-0-ga-release-notes}

発売日：2020年5月28日

TiDB バージョン: 4.0.0

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   トラブルシューティングを容易にするために、大規模なトランザクションのエラー メッセージを最適化します[<a href="https://github.com/pingcap/tidb/pull/17219">#17219</a>](https://github.com/pingcap/tidb/pull/17219)

-   TiCDC
    -   `Changefeed`設定ファイルの構造を最適化して使いやすさを向上[<a href="https://github.com/pingcap/tiflow/pull/588">#588</a>](https://github.com/pingcap/tiflow/pull/588)
    -   設定項目`ignore-txn-start-ts`を追加し、トランザクションフィルタリング時の条件を`commit_ts`から`start_ts`に変更します[<a href="https://github.com/pingcap/tiflow/pull/589">#589</a>](https://github.com/pingcap/tiflow/pull/589)

## 重要なバグ修正 {#important-bug-fixes}

-   TiKV
    -   バックアップと復元 (BR) [<a href="https://github.com/tikv/tikv/pull/7937">#7937</a>](https://github.com/tikv/tikv/pull/7937)を使用してバックアップするときに発生する`DefaultNotFound`エラーを修正します。
    -   順序が狂っていることによるシステムパニックを修正`ReadIndex`パッケージ[<a href="https://github.com/tikv/tikv/pull/7930">#7930</a>](https://github.com/tikv/tikv/pull/7930)
    -   TiKV の再起動後にスナップショット ファイルを誤って削除することによって引き起こされるシステム パニックを修正します[<a href="https://github.com/tikv/tikv/pull/7927">#7927</a>](https://github.com/tikv/tikv/pull/7927)

-   TiFlash
    -   `Raft Admin Command`の処理ロジックが間違っているためにシステムがパニックになったときに発生する可能性のあるデータ損失の問題を修正します。

## 新機能 {#new-features}

-   TiDB
    -   再試行コミットフェーズ[<a href="https://github.com/pingcap/tidb/pull/16849">#16849</a>](https://github.com/pingcap/tidb/pull/16849)の`goroutines`の数を制御する`committer-concurrency`構成項目を追加します。
    -   `show table partition regions`構文[<a href="https://github.com/pingcap/tidb/pull/17294">#17294</a>](https://github.com/pingcap/tidb/pull/17294)をサポートします。
    -   `tmp-storage-quota`構成項目を追加して、TiDBサーバーが使用する一時ディスク容量を制限します[<a href="https://github.com/pingcap/tidb/pull/15700">#15700</a>](https://github.com/pingcap/tidb/pull/15700)
    -   テーブルの作成および変更時にパーティションテーブルが一意のプレフィックスインデックスを使用しているかどうかのチェックをサポート[<a href="https://github.com/pingcap/tidb/pull/17213">#17213</a>](https://github.com/pingcap/tidb/pull/17213)
    -   `insert/replace into tbl_name partition` ( `partition_name_list` ) ステートメントをサポートします[<a href="https://github.com/pingcap/tidb/pull/17313">#17313</a>](https://github.com/pingcap/tidb/pull/17313)
    -   `Distinct`関数使用時の`collations`の値のチェックをサポート[<a href="https://github.com/pingcap/tidb/pull/17240">#17240</a>](https://github.com/pingcap/tidb/pull/17240)
    -   ハッシュ パーティション プルーニング中の`is null`フィルター条件のサポート[<a href="https://github.com/pingcap/tidb/pull/17310">#17310</a>](https://github.com/pingcap/tidb/pull/17310)
    -   パーティション化されたテーブルで`admin check index` 、 `admin cleanup index` 、および`admin recover index`をサポート[<a href="https://github.com/pingcap/tidb/pull/17392">#17392</a>](https://github.com/pingcap/tidb/pull/17392) [<a href="https://github.com/pingcap/tidb/pull/17405">#17405</a>](https://github.com/pingcap/tidb/pull/17405) [<a href="https://github.com/pingcap/tidb/pull/17317">#17317</a>](https://github.com/pingcap/tidb/pull/17317)
    -   `in`式[<a href="https://github.com/pingcap/tidb/pull/17320">#17320</a>](https://github.com/pingcap/tidb/pull/17320)の範囲パーティション プルーニングをサポートします。

-   TiFlash
    -   Learnerがデータを読み取るときに、 `Lock CF`のうち修飾された`TSO` ～ `min commit ts`値に対応するデータをフィルタリングして除外することをサポートします。
    -   `TIMESTAMP`種類の値が`1970-01-01 00:00:00`未満の場合、誤った計算結果を回避するためにシステムが明示的にエラーを報告する機能を追加
    -   ログを検索する際の正規表現でのフラグの使用のサポート

-   TiKV
    -   `ascii_bin`および`latin1_bin`エンコード[<a href="https://github.com/tikv/tikv/pull/7919">#7919</a>](https://github.com/tikv/tikv/pull/7919)の照合順序ルールをサポート

-   PD
    -   組み込み TiDB ダッシュボード[<a href="https://github.com/pingcap/pd/pull/2457">#2457</a>](https://github.com/pingcap/pd/pull/2457)のリバース プロキシ リソース プレフィックスの指定をサポート
    -   PD クライアントリージョン[<a href="https://github.com/pingcap/pd/pull/2443">#2443</a>](https://github.com/pingcap/pd/pull/2443)のインターフェイスで`pending peer`および`down peer`情報を返すサポート
    -   `Direction of hotspot move leader` 、 `Direction of hotspot move peer` 、 `Hot cache read entry number`などの監視項目を追加[<a href="https://github.com/pingcap/pd/pull/2448">#2448</a>](https://github.com/pingcap/pd/pull/2448)

-   ツール
    -   バックアップと復元 (BR)
        -   `Sequence`と`View` [<a href="https://github.com/pingcap/br/pull/242">#242</a>](https://github.com/pingcap/br/pull/242)のバックアップと復元をサポート
    -   TiCDC
        -   `Changefeed` [<a href="https://github.com/pingcap/tiflow/pull/561">#561</a>](https://github.com/pingcap/tiflow/pull/561)を作成する際の`Sink URI`の有効性チェックをサポート
        -   システム起動時に PD および TiKV バージョンがシステム要件を満たしているかどうかのチェックをサポート[<a href="https://github.com/pingcap/tiflow/pull/570">#570</a>](https://github.com/pingcap/tiflow/pull/570)
        -   同じスケジューリング タスク生成サイクル[<a href="https://github.com/pingcap/tiflow/pull/572">#572</a>](https://github.com/pingcap/tiflow/pull/572)で複数のテーブルのスケジューリングをサポート
        -   HTTP API [<a href="https://github.com/pingcap/tiflow/pull/591">#591</a>](https://github.com/pingcap/tiflow/pull/591)のノードの役割に関する情報を追加

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiDB がTiFlash [<a href="https://github.com/pingcap/tidb/pull/17307">#17307</a>](https://github.com/pingcap/tidb/pull/17307)にバッチ コマンドを送信できるようにすることで、メッセージの送受信時に予期しないタイムアウトが発生する問題を修正しました。
    -   パーティション プルーニング中に符号付き整数と符号なし整数が誤って区別される問題を修正し、パフォーマンスを向上させます[<a href="https://github.com/pingcap/tidb/pull/17230">#17230</a>](https://github.com/pingcap/tidb/pull/17230)
    -   `mysql.user`テーブル[<a href="https://github.com/pingcap/tidb/pull/17300">#17300</a>](https://github.com/pingcap/tidb/pull/17300)に互換性がないために v3.1.1 から v4.0 へのアップグレードが失敗する問題を修正
    -   `update`ステートメント[<a href="https://github.com/pingcap/tidb/pull/17305">#17305</a>](https://github.com/pingcap/tidb/pull/17305)でのパーティションの誤った選択の問題を修正します。
    -   TiKV [<a href="https://github.com/pingcap/tidb/pull/17380">#17380</a>](https://github.com/pingcap/tidb/pull/17380)から不明なエラー メッセージを受信したときのシステム パニックを修正
    -   `key`パーティション[<a href="https://github.com/pingcap/tidb/pull/17242">#17242</a>](https://github.com/pingcap/tidb/pull/17242)のテーブルを作成するときに、不適切な処理ロジックによって引き起こされるシステム パニックを修正しました。
    -   オプティマイザーの処理ロジック[<a href="https://github.com/pingcap/tidb/pull/17365">#17365</a>](https://github.com/pingcap/tidb/pull/17365)が正しくないため、間違った`Index Merge Join`プランが選択される問題を修正
    -   Grafana [<a href="https://github.com/pingcap/tidb/pull/16561">#16561</a>](https://github.com/pingcap/tidb/pull/16561)の`SELECT`ステートメントの不正確な`duration`監視メトリクスの問題を修正
    -   システムエラー発生時に GC ワーカーがブロックされる問題を修正[<a href="https://github.com/pingcap/tidb/pull/16915">#16915</a>](https://github.com/pingcap/tidb/pull/16915)
    -   ブール列の制約`UNIQUE`により、比較[<a href="https://github.com/pingcap/tidb/pull/17306">#17306</a>](https://github.com/pingcap/tidb/pull/17306)で誤った結果が生じる問題を修正します。
    -   `tidb_opt_agg_push_down`が有効で、集計関数がパーティションテーブル[<a href="https://github.com/pingcap/tidb/pull/17328">#17328</a>](https://github.com/pingcap/tidb/pull/17328)をプッシュダウンした場合に、不正な処理ロジックによって引き起こされるシステム パニックを修正しました。
    -   場合によっては障害が発生した TiKV ノードにアクセスする問題を修正します[<a href="https://github.com/pingcap/tidb/pull/17342">#17342</a>](https://github.com/pingcap/tidb/pull/17342)
    -   `tidb.toml`の`isolation-read`設定項目が反映されない問題を修正[<a href="https://github.com/pingcap/tidb/pull/17322">#17322</a>](https://github.com/pingcap/tidb/pull/17322)
    -   `hint`を使用してストリーム集約[<a href="https://github.com/pingcap/tidb/pull/17347">#17347</a>](https://github.com/pingcap/tidb/pull/17347)を強制する場合、不正な処理ロジックにより出力結果の順序が正しくなくなる問題を修正します。
    -   `insert`が異なる`SQL_MODE` [<a href="https://github.com/pingcap/tidb/pull/17314">#17314</a>](https://github.com/pingcap/tidb/pull/17314)で DIV を処理する動作を修正

-   TiFlash

    -   検索ログ機能の正規表現のマッチング動作が他のコンポーネントと矛盾する問題を修正
    -   デフォルトで遅延処理の最適化の`Raft Compact Log Command`を無効にすることで、ノードが大量のデータを書き込むときに過剰な再起動時間がかかる問題を修正しました。
    -   一部のシナリオで TiDB が`DROP DATABASE`ステートメントを誤って処理するため、システムが起動できない問題を修正
    -   `Server_info`のCPU情報の収集方法が他のコンポーネントと異なる問題を修正
    -   `batch coprocessor`が有効な場合に`Query`ステートメントを実行するとエラー`Too Many Pings`が報告される問題を修正
    -   TiFlash が関連情報をレポートしないため、ダッシュボードが正しい`deploy path`情報を表示できない問題を修正

-   TiKV

    -   BR [<a href="https://github.com/tikv/tikv/pull/7937">#7937</a>](https://github.com/tikv/tikv/pull/7937)を使用してバックアップするときに発生するエラー`DefaultNotFound`を修正
    -   順序の乱れによるシステム パニックを修正`ReadIndex`パケット[<a href="https://github.com/tikv/tikv/pull/7930">#7930</a>](https://github.com/tikv/tikv/pull/7930)
    -   リードリクエストのコールバック関数が呼び出されていないため、予期せぬエラーが返される問題を修正[<a href="https://github.com/tikv/tikv/pull/7921">#7921</a>](https://github.com/tikv/tikv/pull/7921)
    -   TiKV の再起動時にスナップショット ファイルが誤って削除されることによって引き起こされるシステム パニックを修正します[<a href="https://github.com/tikv/tikv/pull/7927">#7927</a>](https://github.com/tikv/tikv/pull/7927)
    -   storage暗号化[<a href="https://github.com/tikv/tikv/pull/7898">#7898</a>](https://github.com/tikv/tikv/pull/7898)の処理ロジックが正しくないため、 `master key`をローテーションできない問題を修正
    -   storage暗号化が有効になっている場合、受信したスナップショットの`lock cf`が暗号化されない問題を修正します[<a href="https://github.com/tikv/tikv/pull/7922">#7922</a>](https://github.com/tikv/tikv/pull/7922)

-   PD

    -   pd-ctl [<a href="https://github.com/pingcap/pd/pull/2446">#2446</a>](https://github.com/pingcap/pd/pull/2446)を使用して`evict-leader-scheduler`または`grant-leader-scheduler`を削除するときの404エラーを修正
    -   TiFlashレプリカが存在する場合、 `presplit`機能が正しく動作しない場合がある問題を修正[<a href="https://github.com/pingcap/pd/pull/2447">#2447</a>](https://github.com/pingcap/pd/pull/2447)

-   ツール

    -   バックアップと復元 (BR)
        -   BR がクラウドstorage[<a href="https://github.com/pingcap/br/pull/298">#298</a>](https://github.com/pingcap/br/pull/298)からデータを復元するときに、ネットワークの問題によりデータの復元が失敗する問題を修正します。
    -   TiCDC
        -   データ競合によるシステムパニックを修正[<a href="https://github.com/pingcap/tiflow/pull/565">#565</a>](https://github.com/pingcap/tiflow/pull/565) [<a href="https://github.com/pingcap/tiflow/pull/566">#566</a>](https://github.com/pingcap/tiflow/pull/566)
        -   不適切な処理ロジックによって引き起こされるリソース リークまたはシステムのブロックを修正します[<a href="https://github.com/pingcap/tiflow/pull/574">#574</a>](https://github.com/pingcap/tiflow/pull/574) [<a href="https://github.com/pingcap/tiflow/pull/586">#586</a>](https://github.com/pingcap/tiflow/pull/586)
        -   CLI が PD [<a href="https://github.com/pingcap/tiflow/pull/579">#579</a>](https://github.com/pingcap/tiflow/pull/579)に接続できないためにコマンド ラインがスタックする問題を修正
