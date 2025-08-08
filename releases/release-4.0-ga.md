---
title: TiDB 4.0 GA Release Notes
summary: TiDB 4.0.0 GA は 2020 年 5 月 28 日にリリースされました。このバージョンでは、大規模トランザクションのエラー メッセージが最適化され、Changefeed` 構成ファイルの使いやすさが向上し、新しい構成項目とさまざまな構文および関数のサポートが追加され、TiKV、 TiFlash、PD、およびツールの複数のバグと問題が修正され、PD の新しい監視項目とさまざまな機能のサポートが追加され、バックアップと復元 (BR) と TiCDC のさまざまな問題が修正されました。
---

# TiDB 4.0 GA リリースノート {#tidb-4-0-ga-release-notes}

発売日：2020年5月28日

TiDB バージョン: 4.0.0

## 互換性の変更 {#compatibility-changes}

-   TiDB
    -   大規模トランザクションのエラーメッセージを最適化してトラブルシューティングを容易にします[＃17219](https://github.com/pingcap/tidb/pull/17219)

-   TiCDC
    -   `Changefeed`設定ファイルの構造を最適化して使いやすさを向上[＃588](https://github.com/pingcap/tiflow/pull/588)
    -   `ignore-txn-start-ts`構成項目を追加し、トランザクションフィルタリング[＃589](https://github.com/pingcap/tiflow/pull/589)の条件を`commit_ts`から`start_ts`に変更します。

## 重要なバグ修正 {#important-bug-fixes}

-   TiKV
    -   バックアップと復元（BR） [＃7937](https://github.com/tikv/tikv/pull/7937)を使用してバックアップするときに発生する`DefaultNotFound`エラーを修正します
    -   順序がずれたパッケージ`ReadIndex`によるシステムパニックを修正[＃7930](https://github.com/tikv/tikv/pull/7930)
    -   TiKV の再起動後にスナップショットファイルを誤って削除することで発生するシステムパニックを修正[＃7927](https://github.com/tikv/tikv/pull/7927)

-   TiFlash
    -   `Raft Admin Command`の誤った処理ロジックによりシステムがパニックになったときに発生する可能性のあるデータ損失の問題を修正しました。

## 新機能 {#new-features}

-   TiDB
    -   再試行コミットフェーズ[＃16849](https://github.com/pingcap/tidb/pull/16849)の`goroutines`数を制御するための`committer-concurrency`構成項目を追加します。
    -   `show table partition regions`構文[＃17294](https://github.com/pingcap/tidb/pull/17294)サポートする
    -   TiDBサーバー[＃15700](https://github.com/pingcap/tidb/pull/15700)が使用する一時ディスク領域を制限するための`tmp-storage-quota`構成項目を追加します
    -   テーブルの作成時および変更時に、パーティションテーブルが一意のプレフィックスインデックスを使用しているかどうかのチェックをサポート[＃17213](https://github.com/pingcap/tidb/pull/17213)
    -   `insert/replace into tbl_name partition` （ `partition_name_list` ）の声明[＃17313](https://github.com/pingcap/tidb/pull/17313)支持する
    -   `Distinct`関数[＃17240](https://github.com/pingcap/tidb/pull/17240)使用するときに`collations`の値をチェックする機能をサポート
    -   ハッシュパーティションプルーニング[＃17310](https://github.com/pingcap/tidb/pull/17310)中の`is null`フィルタ条件をサポート
    -   パーティションテーブル[＃17392](https://github.com/pingcap/tidb/pull/17392) [＃17405](https://github.com/pingcap/tidb/pull/17405) [＃17317](https://github.com/pingcap/tidb/pull/17317)で`admin check index` 、 `admin cleanup index` 、 `admin recover index`サポート
    -   `in`式[＃17320](https://github.com/pingcap/tidb/pull/17320)範囲パーティションプルーニングをサポート

-   TiFlash
    -   Learnerがデータを読み取る際に、 `Lock CF`の`TSO`から`min commit ts`の条件を満たすデータをフィルタリングすることをサポートします。
    -   `TIMESTAMP`種類の値が`1970-01-01 00:00:00`未満の場合に誤った計算結果を回避するために、システムが明示的にエラーを報告する機能を追加します。
    -   ログ検索時に正規表現でフラグの使用をサポート

-   TiKV
    -   `ascii_bin`と`latin1_bin`エンコード[＃7919](https://github.com/tikv/tikv/pull/7919)の照合順序規則をサポート

-   PD
    -   組み込み TiDB ダッシュボード[＃2457](https://github.com/pingcap/pd/pull/2457)リバース プロキシ リソース プレフィックスの指定をサポート
    -   PDクライアントリージョン[＃2443](https://github.com/pingcap/pd/pull/2443)のインターフェースで`pending peer`と`down peer`情報を返すことをサポート
    -   `Direction of hotspot move leader` `Direction of hotspot move peer` `Hot cache read entry number`監視項目[＃2448](https://github.com/pingcap/pd/pull/2448)追加する

-   ツール
    -   バックアップと復元 (BR)
        -   `Sequence`と`View`のバックアップと復元をサポート[＃242](https://github.com/pingcap/br/pull/242)
    -   TiCDC
        -   `Changefeed` [＃561](https://github.com/pingcap/tiflow/pull/561)作成時に`Sink URI`の有効性チェックをサポート
        -   システム起動時にPDとTiKVのバージョンがシステム要件を満たしているかどうかのチェックをサポート[＃570](https://github.com/pingcap/tiflow/pull/570)
        -   同じスケジュールタスク生成サイクル[＃572](https://github.com/pingcap/tiflow/pull/572)で複数のテーブルのスケジュールをサポート
        -   HTTP API [＃591](https://github.com/pingcap/tiflow/pull/591)にノードの役割に関する情報を追加する

## バグ修正 {#bug-fixes}

-   TiDB

    -   TiDB がTiFlash [＃17307](https://github.com/pingcap/tidb/pull/17307)にバッチコマンドを送信しないようにすることで、メッセージの送受信時に予期しないタイムアウトが発生する問題を修正しました。
    -   パーティションプルーニング中に符号付き整数と符号なし整数を誤って区別する問題を修正し、パフォーマンスが向上しました[＃17230](https://github.com/pingcap/tidb/pull/17230)
    -   互換性のない`mysql.user`テーブル[＃17300](https://github.com/pingcap/tidb/pull/17300)が原因でv3.1.1からv4.0へのアップグレードが失敗する問題を修正しました
    -   `update`文[＃17305](https://github.com/pingcap/tidb/pull/17305)でパーティションの選択が誤っている問題を修正
    -   TiKV [＃17380](https://github.com/pingcap/tidb/pull/17380)から不明なエラーメッセージを受信したときにシステムパニックが発生する問題を修正
    -   `key`パーティション[＃17242](https://github.com/pingcap/tidb/pull/17242)テーブルを作成するときに誤った処理ロジックによって発生するシステムパニックを修正しました。
    -   オプティマイザ処理ロジック[＃17365](https://github.com/pingcap/tidb/pull/17365)誤りにより間違った`Index Merge Join`プランが選択される問題を修正
    -   Grafana [＃16561](https://github.com/pingcap/tidb/pull/16561)の`SELECT`ステートメントの`duration`監視メトリックが不正確であるという問題を修正しました
    -   システムエラーが発生したときにGCワーカーがブロックされる問題を修正[＃16915](https://github.com/pingcap/tidb/pull/16915)
    -   ブール列の制約`UNIQUE`が比較[＃17306](https://github.com/pingcap/tidb/pull/17306)で誤った結果をもたらす問題を修正
    -   `tidb_opt_agg_push_down`が有効になっていて、集計関数がパーティションテーブル[＃17328](https://github.com/pingcap/tidb/pull/17328)をプッシュダウンしたときに、誤った処理ロジックによって発生するシステムパニックを修正しました。
    -   一部のケースで障害が発生した TiKV ノードにアクセスできない問題を修正[＃17342](https://github.com/pingcap/tidb/pull/17342)
    -   `tidb.toml`の`isolation-read`設定項目が有効にならない問題を修正[＃17322](https://github.com/pingcap/tidb/pull/17322)
    -   `hint`使用してストリーム集約[＃17347](https://github.com/pingcap/tidb/pull/17347)強制する場合に、処理ロジックが間違っているために出力結果の順序が間違っている問題を修正しました。
    -   `insert`異なる`SQL_MODE` [＃17314](https://github.com/pingcap/tidb/pull/17314)の下で DIV を処理する動作を修正

-   TiFlash

    -   検索ログ機能における正規表現のマッチング動作が他のコンポーネントと一致しない問題を修正しました
    -   デフォルトで遅延処理の最適化`Raft Compact Log Command`無効にすることで、ノードが大量のデータを書き込むときに過剰な再起動時間がかかる問題を修正しました。
    -   一部のシナリオで TiDB が`DROP DATABASE`ステートメントを誤って処理するため、システムの起動に失敗する問題を修正しました。
    -   `Server_info`の CPU 情報を収集する方法が他のコンポーネントと異なる問題を修正しました
    -   `batch coprocessor`が有効な場合に`Query`文を実行するとエラー`Too Many Pings`が報告される問題を修正しました
    -   TiFlashが関連情報を報告しないため、ダッシュボードに正しい`deploy path`情報が表示されない問題を修正しました。

-   TiKV

    -   BR [＃7937](https://github.com/tikv/tikv/pull/7937)を使用してバックアップするときに発生する`DefaultNotFound`エラーを修正します
    -   順序が乱れた`ReadIndex`パケット[＃7930](https://github.com/tikv/tikv/pull/7930)によるシステムパニックを修正
    -   読み取り要求コールバック関数が呼び出されないために予期しないエラーが返される問題を修正[＃7921](https://github.com/tikv/tikv/pull/7921)
    -   TiKV の再起動時にスナップショットファイルを誤って削除することで発生するシステムパニックを修正[＃7927](https://github.com/tikv/tikv/pull/7927)
    -   storage暗号化[＃7898](https://github.com/tikv/tikv/pull/7898)処理ロジックが正しくないため、 `master key`回転できない問題を修正しました
    -   storage暗号化が有効になっているときに、スナップショットの受信ファイル`lock cf`が暗号化されない問題を修正しました[＃7922](https://github.com/tikv/tikv/pull/7922)

-   PD

    -   pd-ctl [＃2446](https://github.com/pingcap/pd/pull/2446)を使用して`evict-leader-scheduler`または`grant-leader-scheduler`削除するときに発生する 404 エラーを修正しました
    -   TiFlashレプリカが存在する場合に`presplit`機能が正しく動作しない可能性がある問題を修正しました[＃2447](https://github.com/pingcap/pd/pull/2447)

-   ツール

    -   バックアップと復元 (BR)
        -   BRがクラウドstorage[＃298](https://github.com/pingcap/br/pull/298)からデータを復元する際にネットワークの問題によりデータの復元が失敗する問題を修正
    -   TiCDC
        -   データ競合によるシステムパニックを修正[＃565](https://github.com/pingcap/tiflow/pull/565) [＃566](https://github.com/pingcap/tiflow/pull/566)
        -   誤った処理ロジックによるリソースリークやシステムブロックを修正する[＃574](https://github.com/pingcap/tiflow/pull/574) [＃586](https://github.com/pingcap/tiflow/pull/586)
        -   CLIがPD [＃579](https://github.com/pingcap/tiflow/pull/579)に接続できないためにコマンドラインが停止する問題を修正しました
