---
title: TiDB 2.1.17 Release Notes
---

# TiDB 2.1.17 リリースノート {#tidb-2-1-17-release-notes}

発売日：2019年9月11日

TiDB バージョン: 2.1.17

TiDB Ansible バージョン: 2.1.17

-   新機能
    -   TiDB の`SHOW TABLE REGIONS`構文に`WHERE`句を追加します。
    -   TiKVとPDに設定項目を確認する機能`config-check`を追加
    -   pd-ctl に`remove-tombstone`コマンドを追加して、トゥームストーン ストア レコードをクリアします。
    -   Reparoに`worker-count`と`txn-batch`設定項目を追加して回復速度を制御します

-   改善点
    -   積極的にプッシュするオペレーターをサポートすることで、PD のスケジューリング プロセスを最適化します。
    -   TiKV の起動プロセスを最適化し、ノードの再起動によって生じるジッターを軽減します。

-   変化した行動
    -   TiDB スロー クエリ ログの`start ts`最後の再試行時刻から最初の実行時刻に変更します。
    -   TiDB スロー クエリ ログの`Index_ids`フィールドを`Index_names`フィールドに置き換えて、スロー クエリ ログの使いやすさを向上させます。
    -   TiDB の構成ファイルに`split-region-max-num`パラメータを追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を変更します。これは、デフォルト構成では 1,000 から 10,000 に増加します。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `EvalSubquery` `Executor` [#11811](https://github.com/pingcap/tidb/pull/11811)構築中にエラーが発生した場合、エラーメッセージが正しく返されない問題を修正
    -   外部テーブルの行数がインデックス検索結合の単一バッチの行数よりも大きい場合、クエリ結果が正しくなくなる可能性がある問題を修正します。インデックスルックアップ結合の機能範囲を拡張します。 `UnionScan` `IndexJoin` [#11843](https://github.com/pingcap/tidb/pull/11843)のサブノードとして使用できます
    -   統計フィードバック プロセス中に無効なキーが発生する可能性がある状況に備えて、無効なキー ( `invalid encoded key flag 252`など) の表示を`SHOW STAT_BUCKETS`構文に追加します[#12098](https://github.com/pingcap/tidb/pull/12098)
-   SQL実行エンジン
    -   `CAST`関数が数値型[#11712](https://github.com/pingcap/tidb/pull/11712)を変換するときに、最初に`UINT`に変換される数値によって引き起こされるいくつかの誤った結果 ( `select cast(13835058000000000000 as double)`など) を修正しました。
    -   `DIV`計算の被除数が小数で、この計算に負の数[#11812](https://github.com/pingcap/tidb/pull/11812)含まれる場合、計算結果が正しくなくなることがある問題を修正
    -   `SELECT` / `EXPLAIN`ステートメントの実行時に一部の文字列が`INT`タイプに変換されることによって引き起こされる MySQL の非互換性の問題を修正する`ConvertStrToIntStrict`関数を追加します[#11892](https://github.com/pingcap/tidb/pull/11892)
    -   `EXPLAIN ... FOR CONNECTION`を使用した場合に`stmtCtx`の設定が間違っているため、 `Explain`結果が正しくなくなることがある問題[#11978](https://github.com/pingcap/tidb/pull/11978)修正
    -   整数の結果がオーバーフローした場合に`unaryMinus`進数以外の結果が発生するために、関数によって返される結果が MySQL と互換性がないという問題を修正します[#11990](https://github.com/pingcap/tidb/pull/11990)
    -   `LOAD DATA`ステートメントの実行時のカウント順序により`last_insert_id()`正しくなくなる可能性がある問題を修正[#11994](https://github.com/pingcap/tidb/pull/11994)
    -   ユーザーが明示的と暗黙的な混合方法で自動インクリメント列データを書き込む場合、 `last_insert_id()`が正しくない可能性がある問題を修正します[#12001](https://github.com/pingcap/tidb/pull/12001)
    -   `JSON_UNQUOTE`関数のオーバークオートのバグを修正します。二重引用符 ( `"` ) で囲まれた値のみを引用符で囲む必要があります。たとえば、「 `SELECT JSON_UNQUOTE("\\\\")` 」の結果は「 `\\` 」になります (変更されません) [#12096](https://github.com/pingcap/tidb/pull/12096)
-   サーバ
    -   TiDB トランザクション[#11878](https://github.com/pingcap/tidb/pull/11878)を再試行する際に、最後の再試行時刻から最初の実行時刻までのスロー クエリ ログに記録される変更`start ts`
    -   トランザクションのキーの数を`LockResolver`に追加して、リージョン全体でのスキャン操作を回避し、キーの数が減ったときにロックを解決するコストを削減します[#11889](https://github.com/pingcap/tidb/pull/11889)
    -   スロークエリログ[#11886](https://github.com/pingcap/tidb/pull/11886)で`succ`フィールドの値が正しくない可能性がある問題を修正します。
    -   スロー クエリ ログの使いやすさを向上させるために、スロー クエリ ログの`Index_ids`フィールドを`Index_names`フィールドに置き換えます[#12063](https://github.com/pingcap/tidb/pull/12063)
    -   `Duration`に`-`含まれる場合 ( `select time(‘--’)`など)、TiDB が`-` EOF エラーに解析することによって引き起こされる接続切断の問題を修正します[#11910](https://github.com/pingcap/tidb/pull/11910)
    -   無効なリージョンを`RegionCache`からより迅速に削除して、このリージョン[#11931](https://github.com/pingcap/tidb/pull/11931)に送信されるリクエストの数を減らします。
    -   `Insert Into … Select`構文で`oom-action = "cancel"`と OOM が発生した場合の OOMpanic問題の誤った処理によって引き起こされる接続切断の問題を修正します[#12126](https://github.com/pingcap/tidb/pull/12126)
-   DDL
    -   `tikvSnapshot`の逆スキャン インターフェイスを追加して、DDL 履歴ジョブを効率的にクエリします。このインターフェースを使用した後、 `ADMIN SHOW DDL JOBS`の実行時間が大幅に短縮されました[#11789](https://github.com/pingcap/tidb/pull/11789)
    -   `CREATE TABLE ... PRE_SPLIT_REGION`構文を改善します。3 `PRE_SPLIT_REGION = N` [#11797](https://github.com/pingcap/tidb/pull/11797/files)場合、事前分割領域の数を 2^(N-1) から 2^N に変更します。
    -   オンライン ワークロードへの大きな影響を避けるために、 `Add Index`操作のバックグラウンド ワーカー スレッドのデフォルト パラメータ値を減らします[#11875](https://github.com/pingcap/tidb/pull/11875)
    -   `SPLIT TABLE`構文動作を改善します。領域[#11929](https://github.com/pingcap/tidb/pull/11929)を分割するために`SPLIT TABLE ... REGIONS N`使用される場合、N データリージョンと 1 つのインデックスリージョンを生成します。
    -   構成ファイルに`split-region-max-num`パラメータ (デフォルトでは`10000` ) を追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を調整できるようにします[#12080](https://github.com/pingcap/tidb/pull/12080)
    -   システムがbinlog [#12121](https://github.com/pingcap/tidb/pull/12121)を書き込むときにこの句`PRE_SPLIT_REGIONS`コメントされていないことが原因で、ダウンストリーム MySQL で`CREATE TABLE`句を解析できない問題を修正します。
    -   `SHOW TABLE … REGIONS`と`SHOW TABLE .. INDEX … REGIONS`に`WHERE`サブ節を追加します[#12124](https://github.com/pingcap/tidb/pull/12124)
-   モニター
    -   `connection_transient_failure_count`監視メトリックを追加して、 `tikvclient` [#12092](https://github.com/pingcap/tidb/pull/12092)の gRPC 接続エラーをカウントします。

## TiKV {#tikv}

-   場合によってはリージョン内のキーのカウントの誤った結果を修正[#5415](https://github.com/tikv/tikv/pull/5415)
-   TiKV に`config-check`オプションを追加して、TiKV 構成項目が有効かどうかを確認します[#5391](https://github.com/tikv/tikv/pull/5391)
-   起動プロセスを最適化して、ノード[#5277](https://github.com/tikv/tikv/pull/5277)の再起動によって生じるジッターを軽減します。
-   場合によっては、ロックの解決プロセスを最適化し、トランザクションのロックの解決を高速化します[#5339](https://github.com/tikv/tikv/pull/5339)
-   `get_txn_commit_info`プロセスを最適化してトランザクションのコミットを高速化する[#5062](https://github.com/tikv/tikv/pull/5062)
-   Raft 関連のログの簡略化[#5425](https://github.com/tikv/tikv/pull/5425)
-   場合によっては TiKV が異常終了する問題を解決[#5441](https://github.com/tikv/tikv/pull/5441)

## PD {#pd}

-   PD に`config-check`オプションを追加して、PD 構成アイテムが有効かどうかを確認します[#1725](https://github.com/pingcap/pd/pull/1725)
-   pd-ctl に`remove-tombstone`コマンドを追加して、廃棄ストア レコード[#1705](https://github.com/pingcap/pd/pull/1705)クリアをサポートします。
-   スケジューリングを高速化するためにオペレーターを積極的にプッシュするサポート[#1686](https://github.com/pingcap/pd/pull/1686)

## ツール {#tools}

-   TiDBBinlog
    -   Reparoに`worker-count`と`txn-batch`設定項目を追加して回復速度を制御します[#746](https://github.com/pingcap/tidb-binlog/pull/746)
    -   Drainerのメモリ使用量を最適化して並列実行効率を向上[#735](https://github.com/pingcap/tidb-binlog/pull/735)
    -   場合によってはPumpが正常に終了できない不具合を修正[#739](https://github.com/pingcap/tidb-binlog/pull/739)
    -   Pumpの`LevelDB`の処理ロジックを最適化してGC [#720](https://github.com/pingcap/tidb-binlog/pull/720)の実行効率を向上
-   TiDB Lightning
    -   チェックポイント[#239](https://github.com/pingcap/tidb-lightning/pull/239)からデータを再インポートすることによって tidb-lightning がクラッシュする可能性があるバグを修正

## TiDB Ansible {#tidb-ansible}

-   Spark バージョンを 2.4.3 に更新し、TiSpark バージョン[#919](https://github.com/pingcap/tidb-ansible/pull/927) Spark 2.4.3 と互換性のある 2.2.0 に更新します[#914](https://github.com/pingcap/tidb-ansible/pull/914)
-   リモートマシンのパスワードの有効期限が切れた場合に待ち時間が長くなる問題を修正[#937](https://github.com/pingcap/tidb-ansible/pull/937) 、 [#948](https://github.com/pingcap/tidb-ansible/pull/948)
