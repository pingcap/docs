---
title: TiDB 4.0 GA Release Notes
---

# TiDB4.0GAリリースノート {#tidb-4-0-ga-release-notes}

発売日：2020年5月28日

TiDBバージョン：4.0.0

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   トラブルシューティングを容易にするために、大規模なトランザクションのエラーメッセージを最適化する[＃17219](https://github.com/pingcap/tidb/pull/17219)

-   TiCDC
    -   `Changefeed`構成ファイルの構造を最適化して、使いやすさを向上させます[＃588](https://github.com/pingcap/tiflow/pull/588)
    -   `ignore-txn-start-ts`の構成アイテムを追加し、トランザクションのフィルタリング中に条件を`commit_ts`から`start_ts`に変更します[＃589](https://github.com/pingcap/tiflow/pull/589)

## 重要なバグ修正 {#important-bug-fixes}

-   TiKV
    -   Backup＆Restore（BR） [＃7937](https://github.com/tikv/tikv/pull/7937)を使用してバックアップするときに発生する`DefaultNotFound`のエラーを修正します。
    -   故障した`ReadIndex`パッケージによって引き起こされるシステムパニックを修正する[＃7930](https://github.com/tikv/tikv/pull/7930)
    -   TiKVの再起動後にスナップショットファイルを誤って削除することによって引き起こされるシステムパニックを修正します[＃7927](https://github.com/tikv/tikv/pull/7927)

-   TiFlash
    -   `Raft Admin Command`の誤った処理ロジックが原因でシステムがパニックになったときに発生する可能性のあるデータ損失の問題を修正します

## 新機能 {#new-features}

-   TiDB
    -   `committer-concurrency`の構成アイテムを追加して、再試行コミットフェーズ[＃16849](https://github.com/pingcap/tidb/pull/16849)で`goroutines`の数を制御します。
    -   `show table partition regions`構文[＃17294](https://github.com/pingcap/tidb/pull/17294)をサポートします
    -   `tmp-storage-quota`の構成アイテムを追加して、TiDBサーバーが使用する一時ディスク容量を制限します[＃15700](https://github.com/pingcap/tidb/pull/15700)
    -   テーブルの作成および変更時に、パーティション化されたテーブルが一意のプレフィックスインデックスを使用するかどうかのチェックをサポート[＃17213](https://github.com/pingcap/tidb/pull/17213)
    -   `insert/replace into tbl_name partition` （ `partition_name_list` ）ステートメント[＃17313](https://github.com/pingcap/tidb/pull/17313)をサポートする
    -   `Distinct`関数[＃17240](https://github.com/pingcap/tidb/pull/17240)を使用する場合の`collations`の値のチェックをサポートします。
    -   ハッシュパーティションプルーニング[＃17310](https://github.com/pingcap/tidb/pull/17310)中に`is null`フィルター条件をサポートします。
    -   パーティションテーブルで`admin check index` 、および`admin cleanup index`を[＃17317](https://github.com/pingcap/tidb/pull/17317) `admin recover index` [＃17392](https://github.com/pingcap/tidb/pull/17392) [＃17405](https://github.com/pingcap/tidb/pull/17405)
    -   `in`式[＃17320](https://github.com/pingcap/tidb/pull/17320)の範囲パーティションプルーニングをサポートします。

-   TiFlash
    -   学習者がデータを読み取るときに、 `Lock CF`の修飾された`TSO`から`min commit ts`の値に対応するデータの除外をサポートします
    -   `TIMESTAMP`のタイプの値が`1970-01-01 00:00:00`未満の場合に誤った計算結果を回避するために、システムが明示的にエラーを報告する機能を追加します
    -   ログを検索する際の正規表現でのフラグの使用のサポート

-   TiKV
    -   `ascii_bin`および`latin1_bin`エンコーディング[＃7919](https://github.com/tikv/tikv/pull/7919)の照合順序ルールをサポートします

-   PD
    -   組み込みTiDBダッシュボード[＃2457](https://github.com/pingcap/pd/pull/2457)のリバースプロキシリソースプレフィックスの指定をサポート
    -   PDクライアントリージョン[＃2443](https://github.com/pingcap/pd/pull/2443)のインターフェイスで`pending peer`および`down peer`情報を返すことをサポートします。
    -   `Direction of hotspot move leader`などの`Hot cache read entry number` [＃2448](https://github.com/pingcap/pd/pull/2448)を追加し`Direction of hotspot move peer`

-   ツール
    -   バックアップと復元（BR）
        -   `Sequence`と`View`のバックアップと[＃242](https://github.com/pingcap/br/pull/242)をサポートする
    -   TiCDC
        -   [＃561](https://github.com/pingcap/tiflow/pull/561)を作成するときに`Sink URI`の有効性をチェックすることをサポートし`Changefeed`
        -   システム起動時にPDおよびTiKVバージョンがシステム要件を満たしているかどうかのチェックをサポート[＃570](https://github.com/pingcap/tiflow/pull/570)
        -   同じスケジューリングタスク生成サイクル[＃572](https://github.com/pingcap/tiflow/pull/572)で複数のテーブルのスケジューリングをサポートする
        -   [＃591](https://github.com/pingcap/tiflow/pull/591)でノードの役割に関する情報を追加する

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiDBを無効にしてバッチコマンドを[＃17307](https://github.com/pingcap/tidb/pull/17307)に送信することにより、メッセージの送受信時の予期しないタイムアウトの問題を修正します。
    -   パーティションプルーニング中に符号付き整数と符号なし整数を誤って区別する問題を修正しました。これにより、パフォーマンスが向上します[＃17230](https://github.com/pingcap/tidb/pull/17230) 。
    -   互換性のない`mysql.user`テーブル[＃17300](https://github.com/pingcap/tidb/pull/17300)が原因で、v3.1.1からv4.0へのアップグレードが失敗する問題を修正します。
    -   `update`ステートメント[＃17305](https://github.com/pingcap/tidb/pull/17305)のパーティションの誤った選択の問題を修正します。
    -   [＃17380](https://github.com/pingcap/tidb/pull/17380)から不明なエラーメッセージを受信したときのシステムパニックを修正
    -   `key`パーティション化されたテーブルを作成する際の不適切な処理ロジックによって引き起こされるシステムパニックを修正します[＃17242](https://github.com/pingcap/tidb/pull/17242)
    -   オプティマイザ処理ロジック[＃17365](https://github.com/pingcap/tidb/pull/17365)が正しくないために、間違った`Index Merge Join`プランが選択される問題を修正します。
    -   Grafana5の`SELECT`ステートメントの不正確な`duration`モニタリングメトリックの問題を修正し[＃16561](https://github.com/pingcap/tidb/pull/16561)
    -   システムエラーが発生したときにGCワーカーがブロックされる問題を修正します[＃16915](https://github.com/pingcap/tidb/pull/16915)
    -   ブール列の`UNIQUE`制約により、比較[＃17306](https://github.com/pingcap/tidb/pull/17306)で誤った結果が生じる問題を修正します。
    -   `tidb_opt_agg_push_down`が有効で、集計関数がパーティションテーブル[＃17328](https://github.com/pingcap/tidb/pull/17328)をプッシュダウンするときに、誤った処理ロジックによって引き起こされるシステムパニックを修正します。
    -   場合によっては、失敗したTiKVノードにアクセスする問題を修正します[＃17342](https://github.com/pingcap/tidb/pull/17342)
    -   `tidb.toml`の`isolation-read`の構成アイテムが有効にならない問題を修正します[＃17322](https://github.com/pingcap/tidb/pull/17322)
    -   `hint`を使用してストリーム集約を実施する場合の処理ロジックが正しくないために出力結果の順序が正しくない問題を修正します[＃17347](https://github.com/pingcap/tidb/pull/17347)
    -   `insert`が異なる[＃17314](https://github.com/pingcap/tidb/pull/17314)でDIVを処理する動作を修正し`SQL_MODE`

-   TiFlash

    -   検索ログ機能の正規表現の一致動作が他のコンポーネントと矛盾する問題を修正します
    -   デフォルトで`Raft Compact Log Command`の遅延処理最適化を無効にすることにより、ノードが大量のデータを書き込む場合の過剰な再起動時間の問題を修正します。
    -   一部のシナリオでTiDBが`DROP DATABASE`ステートメントを誤って処理するためにシステムが起動しないという問題を修正します
    -   `Server_info`でCPU情報を収集する方法が他のコンポーネントの方法と異なる問題を修正します
    -   `batch coprocessor`が有効になっている場合、 `Query`ステートメントの実行時にエラー`Too Many Pings`が報告される問題を修正します。
    -   TiFlashが関連情報を報告しないため、ダッシュボードが正しい`deploy path`情報を表示できない問題を修正します

-   TiKV

    -   [＃7937](https://github.com/tikv/tikv/pull/7937)を使用してバックアップするときに発生する`DefaultNotFound`のエラーを修正します
    -   異常な`ReadIndex`パケットによって引き起こされるシステムパニックを修正します[＃7930](https://github.com/tikv/tikv/pull/7930)
    -   読み取り要求コールバック関数が呼び出されないために予期しないエラーが返される問題を修正します[＃7921](https://github.com/tikv/tikv/pull/7921)
    -   TiKVの再起動時にスナップショットファイルを誤って削除することによって引き起こされるシステムパニックを修正します[＃7927](https://github.com/tikv/tikv/pull/7927)
    -   ストレージ暗号化[＃7898](https://github.com/tikv/tikv/pull/7898)の処理ロジックが正しくないために`master key`をローテーションできない問題を修正します
    -   ストレージ暗号化が有効になっている場合、スナップショットの受信`lock cf`ファイルが暗号化されない問題を修正します[＃7922](https://github.com/tikv/tikv/pull/7922)

-   PD

    -   pd-ctl5を使用して`evict-leader-scheduler`または`grant-leader-scheduler`を削除するときの404エラーを修正し[＃2446](https://github.com/pingcap/pd/pull/2446)
    -   TiFlashレプリカが存在する場合に`presplit`機能が正しく機能しない可能性があるという問題を修正します[＃2447](https://github.com/pingcap/pd/pull/2447)

-   ツール

    -   バックアップと復元（BR）
        -   BRがクラウドストレージからデータを復元するときにネットワークの問題が原因でデータの復元が失敗する問題を修正します[＃298](https://github.com/pingcap/br/pull/298)
    -   TiCDC
        -   データ競合によって[＃566](https://github.com/pingcap/tiflow/pull/566)れるシステムパニックを修正する[＃565](https://github.com/pingcap/tiflow/pull/565)
        -   不適切な処理ロジックによって[＃586](https://github.com/pingcap/tiflow/pull/586)れるリソースリークまたはシステムのブロックを修正する[＃574](https://github.com/pingcap/tiflow/pull/574)
        -   CLIがPD1に接続できないためにコマンドラインがスタックする問題を修正し[＃579](https://github.com/pingcap/tiflow/pull/579)
