---
title: TiDB 4.0 GA Release Notes
---

# TiDB 4.0 GA リリースノート {#tidb-4-0-ga-release-notes}

発売日：2020年5月28日

TiDB バージョン: 4.0.0

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   トラブルシューティングを容易にするために、大規模なトランザクションのエラー メッセージを最適化する[#17219](https://github.com/pingcap/tidb/pull/17219)

-   TiCDC
    -   `Changefeed`構成ファイルの構造を最適化して使いやすさを改善する[#588](https://github.com/pingcap/tiflow/pull/588)
    -   設定項目を`ignore-txn-start-ts`追加し、トランザクションフィルタリング時の条件を`commit_ts`から`start_ts`に変更[#589](https://github.com/pingcap/tiflow/pull/589)

## 重要なバグ修正 {#important-bug-fixes}

-   TiKV
    -   Backup &amp; Restore (BR) を使用してバックアップするときに発生する`DefaultNotFound`エラーを修正します[#7937](https://github.com/tikv/tikv/pull/7937)
    -   順不同によるシステムパニックの修正`ReadIndex`パッケージ[#7930](https://github.com/tikv/tikv/pull/7930)
    -   TiKV の再起動後にスナップショット ファイルを誤って削除することによって引き起こされるシステム パニックを修正します[#7927](https://github.com/tikv/tikv/pull/7927)

-   TiFlash
    -   `Raft Admin Command`の処理ロジックが正しくないためにシステムがパニックになったときに発生する可能性のあるデータ損失の問題を修正します。

## 新機能 {#new-features}

-   TiDB
    -   retry-commit フェーズ[#16849](https://github.com/pingcap/tidb/pull/16849)で`goroutines`の数を制御する`committer-concurrency`構成項目を追加します。
    -   `show table partition regions`構文[#17294](https://github.com/pingcap/tidb/pull/17294)をサポート
    -   `tmp-storage-quota`構成項目を追加して、TiDBサーバーが使用する一時ディスク領域を制限します[#15700](https://github.com/pingcap/tidb/pull/15700)
    -   テーブルの作成および変更時に、パーティションテーブルが一意のプレフィックス インデックスを使用するかどうかのチェックをサポートします[#17213](https://github.com/pingcap/tidb/pull/17213)
    -   `insert/replace into tbl_name partition` ( `partition_name_list` ) ステートメント[#17313](https://github.com/pingcap/tidb/pull/17313)サポート
    -   `Distinct`関数[#17240](https://github.com/pingcap/tidb/pull/17240)使用時の`collations`の値のチェックをサポート
    -   ハッシュパーティションプルーニング中の`is null`フィルター条件をサポート[#17310](https://github.com/pingcap/tidb/pull/17310)
    -   分割されたテーブルで`admin check index` 、 `admin cleanup index` 、および`admin recover index`をサポート[#17392](https://github.com/pingcap/tidb/pull/17392) [#17405](https://github.com/pingcap/tidb/pull/17405) [#17317](https://github.com/pingcap/tidb/pull/17317)
    -   `in`式[#17320](https://github.com/pingcap/tidb/pull/17320)のレンジ パーティション プルーニングをサポート

-   TiFlash
    -   Learnerがデータを読み取るときに、 `Lock CF`の値の 1 から`min commit ts`までの修飾された`TSO`に対応するデータのフィルタリングをサポートします。
    -   `TIMESTAMP`型の値が`1970-01-01 00:00:00`未満の場合に誤った計算結果を回避するために、システムが明示的にエラーを報告する機能を追加します
    -   ログ検索時の正規表現でのフラグの使用をサポート

-   TiKV
    -   `ascii_bin`および`latin1_bin`エンコーディング[#7919](https://github.com/tikv/tikv/pull/7919)の照合順序ルールをサポート

-   PD
    -   組み込み TiDB ダッシュボード[#2457](https://github.com/pingcap/pd/pull/2457)のリバース プロキシ リソース プレフィックスの指定をサポート
    -   PD クライアントリージョン[#2443](https://github.com/pingcap/pd/pull/2443)のインターフェイスで`pending peer`と`down peer`情報を返すサポート
    -   `Direction of hotspot move leader` 、 `Direction of hotspot move peer` 、 `Hot cache read entry number` [#2448](https://github.com/pingcap/pd/pull/2448)などの監視項目を追加

-   ツール
    -   バックアップと復元 (BR)
        -   `Sequence`と`View` [#242](https://github.com/pingcap/br/pull/242)のバックアップと復元をサポート
    -   TiCDC
        -   `Changefeed` [#561](https://github.com/pingcap/tiflow/pull/561)の作成時に`Sink URI`の有効性をチェックするサポート
        -   システムの起動時に PD と TiKV のバージョンがシステム要件を満たしているかどうかの確認をサポート[#570](https://github.com/pingcap/tiflow/pull/570)
        -   同じスケジューリング タスク生成サイクルで複数のテーブルのスケジューリングをサポート[#572](https://github.com/pingcap/tiflow/pull/572)
        -   HTTP API [#591](https://github.com/pingcap/tiflow/pull/591)にノード ロールに関する情報を追加する

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiDB を無効にしてバッチ コマンドをTiFlash [#17307](https://github.com/pingcap/tidb/pull/17307)に送信することにより、メッセージの送受信時に予期しないタイムアウトが発生する問題を修正します。
    -   パーティションのプルーニング中に符号付き整数と符号なし整数を誤って区別する問題を修正し、パフォーマンスを向上させます[#17230](https://github.com/pingcap/tidb/pull/17230)
    -   互換性がないため v3.1.1 から v4.0 へのアップグレードが失敗する問題を修正します`mysql.user`テーブル[#17300](https://github.com/pingcap/tidb/pull/17300)
    -   `update`ステートメント[#17305](https://github.com/pingcap/tidb/pull/17305)のパーティションの選択が正しくない問題を修正します。
    -   TiKV [#17380](https://github.com/pingcap/tidb/pull/17380)から不明なエラー メッセージを受信したときのシステム パニックを修正
    -   `key`パーティション分割されたテーブルを作成するときに、不適切な処理ロジックによって引き起こされるシステム パニックを修正します[#17242](https://github.com/pingcap/tidb/pull/17242)
    -   オプティマイザーの処理ロジックが正しくないため、間違った`Index Merge Join`プランが選択される問題を修正[#17365](https://github.com/pingcap/tidb/pull/17365)
    -   Grafana [#16561](https://github.com/pingcap/tidb/pull/16561)の`SELECT`ステートメントの不正確な`duration`モニタリング メトリックの問題を修正します。
    -   システム エラーが発生したときに GC ワーカーがブロックされる問題を修正します[#16915](https://github.com/pingcap/tidb/pull/16915)
    -   ブール列の`UNIQUE`制約により、比較[#17306](https://github.com/pingcap/tidb/pull/17306)で誤った結果が生じる問題を修正します
    -   `tidb_opt_agg_push_down`が有効で、パーティションテーブルをプッシュ ダウンするときに、不適切な処理ロジックによって引き起こされるシステム パニックを修正します[#17328](https://github.com/pingcap/tidb/pull/17328)
    -   場合によっては失敗した TiKV ノードにアクセスする問題を修正します[#17342](https://github.com/pingcap/tidb/pull/17342)
    -   `tidb.toml`の`isolation-read`設定項目が有効にならない問題を修正[#17322](https://github.com/pingcap/tidb/pull/17322)
    -   `hint`を使用してストリーム アグリゲーション[#17347](https://github.com/pingcap/tidb/pull/17347)を適用すると、処理ロジックが正しくないために出力結果の順序が正しくない問題を修正します。
    -   `insert`が異なる`SQL_MODE` [#17314](https://github.com/pingcap/tidb/pull/17314)の下で DIV を処理する動作を修正します

-   TiFlash

    -   検索ログ機能での正規表現のマッチング動作が他のコンポーネントと矛盾する問題を修正
    -   デフォルトで`Raft Compact Log Command`の遅延処理の最適化を無効にすることで、ノードが大量のデータを書き込む際に過剰な再起動時間が発生する問題を修正します。
    -   一部のシナリオで TiDB が`DROP DATABASE`ステートメントを正しく処理しないために、システムが起動に失敗する問題を修正します。
    -   `Server_info`のCPU情報の収集方法が他のコンポーネントと異なる問題を修正
    -   `batch coprocessor`が有効な場合に`Query`ステートメントを実行すると、エラー`Too Many Pings`が報告される問題を修正します。
    -   TiFlash が関連情報をレポートしないため、Dashboard が正しい`deploy path`情報を表示できない問題を修正します。

-   TiKV

    -   BR [#7937](https://github.com/tikv/tikv/pull/7937)を使用してバックアップするときに発生する`DefaultNotFound`エラーを修正します。
    -   順不同によるシステムパニックの修正`ReadIndex`パケット[#7930](https://github.com/tikv/tikv/pull/7930)
    -   読み取り要求のコールバック関数が呼び出されないため、予期しないエラーが返される問題を修正[#7921](https://github.com/tikv/tikv/pull/7921)
    -   TiKV の再起動時にスナップショット ファイルを誤って削除することによって発生するシステム パニックを修正します[#7927](https://github.com/tikv/tikv/pull/7927)
    -   storage暗号化[#7898](https://github.com/tikv/tikv/pull/7898)の処理ロジックが正しくないため、 `master key`をローテーションできない問題を修正
    -   storageの暗号化を有効にすると、受信したスナップショットの`lock cf`ファイルが暗号化されない問題を修正[#7922](https://github.com/tikv/tikv/pull/7922)

-   PD

    -   pd-ctl [#2446](https://github.com/pingcap/pd/pull/2446)を使用して`evict-leader-scheduler`または`grant-leader-scheduler`を削除するときの 404 エラーを修正します。
    -   TiFlashレプリカが存在する場合、 `presplit`機能が正しく動作しない場合がある問題を修正[#2447](https://github.com/pingcap/pd/pull/2447)

-   ツール

    -   バックアップと復元 (BR)
        -   BR がクラウドstorage[#298](https://github.com/pingcap/br/pull/298)からデータを復元するときに、ネットワークの問題によりデータの復元が失敗する問題を修正します。
    -   TiCDC
        -   データ競合によるシステムパニックの修正[#565](https://github.com/pingcap/tiflow/pull/565) [#566](https://github.com/pingcap/tiflow/pull/566)
        -   不適切な処理ロジックによるリソース リークまたはシステムのブロックを修正する[#574](https://github.com/pingcap/tiflow/pull/574) [#586](https://github.com/pingcap/tiflow/pull/586)
        -   CLI が PD [#579](https://github.com/pingcap/tiflow/pull/579)に接続できないためにコマンド ラインがスタックする問題を修正します。
