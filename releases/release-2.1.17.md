---
title: TiDB 2.1.17 Release Notes
summary: "TiDB 2.1.17 リリースノート: 新機能には、SHOW TABLE REGIONS` の `WHERE` 句、TiKV および PD の `config-check` 機能、pd-ctl の `remove-tombstone` コマンド、 Reparoの `worker-count` および `txn-batch` 構成項目が含まれます。PD のスケジュール プロセスと TiKV の起動プロセスが改善されました。TiDB スロー クエリ ログと構成ファイルの動作が変更されました。SQL オプティマイザー、SQL 実行エンジン、サーバー、DDL、モニター、TiKV、PD、TiDB Binlog、 TiDB Lightning、および TiDB Ansible の修正と最適化が行われました。"
---

# TiDB 2.1.17 リリースノート {#tidb-2-1-17-release-notes}

発売日：2019年9月11日

TiDB バージョン: 2.1.17

TiDB Ansible バージョン: 2.1.17

-   新機能
    -   TiDBの`SHOW TABLE REGIONS`構文に`WHERE`句を追加する
    -   TiKVとPDに`config-check`機能を追加して構成項目をチェックする
    -   pd-ctlに`remove-tombstone`コマンドを追加して、tombstoneストアのレコードをクリアします。
    -   Reparoに`worker-count`と`txn-batch`設定項目を追加して回復速度を制御します

-   改善点
    -   積極的にプッシュするオペレータをサポートすることでPDのスケジュールプロセスを最適化します
    -   TiKV の起動プロセスを最適化し、ノードの再起動によって発生するジッターを軽減します。

-   動作の変更
    -   TiDB スロークエリログの最後の再試行時刻から最初の実行時刻への変更`start ts`
    -   TiDB スロー クエリ ログの`Index_ids`フィールドを`Index_names`フィールドに置き換えて、スロー クエリ ログの使いやすさを向上させます。
    -   TiDB の構成ファイルに`split-region-max-num`パラメータを追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を変更します。デフォルト構成では、1,000 から 10,000 に増加されます。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `EvalSubquery`ビルド`Executor` 中にエラーが発生したときにエラーメッセージが正しく返されない問題を修正 [＃11811](https://github.com/pingcap/tidb/pull/11811)
    -   インデックスルックアップ結合において、外部テーブルの行数が単一バッチの行数より多い場合にクエリ結果が正しくない可能性がある問題を修正しました。インデックスルックアップ結合の機能範囲を拡張しました。1 `UnionScan` `IndexJoin` のサブノードとして使用できます。 [＃11843](https://github.com/pingcap/tidb/pull/11843)
    -   統計フィードバック処理中に無効なキーが発生する可能性がある状況に備えて、 `SHOW STAT_BUCKETS`構文に無効なキー（ `invalid encoded key flag 252`など）の表示を追加します[＃12098](https://github.com/pingcap/tidb/pull/12098)
-   SQL実行エンジン
    -   `CAST`関数が数値型を変換するときに最初に`UINT`に変換される数値によって発生するいくつかの誤った結果 ( `select cast(13835058000000000000 as double)`など) を修正しました。 [＃11712](https://github.com/pingcap/tidb/pull/11712)
    -   `DIV`計算の被除数が小数で、この計算に負の数が含まれている場合に計算結果が正しくない可能性がある問題を修正しました。 [＃11812](https://github.com/pingcap/tidb/pull/11812)
    -   `SELECT` / `EXPLAIN`文を実行するときに一部の文字列が`INT`型に変換されることで発生する MySQL の非互換性の問題を修正するために`ConvertStrToIntStrict`関数を追加します [＃11892](https://github.com/pingcap/tidb/pull/11892)
    -   `EXPLAIN ... FOR CONNECTION`が使用されているときに`stmtCtx`の設定が間違っているために`Explain`結果が正しくない可能性がある問題を修正しました[＃11978](https://github.com/pingcap/tidb/pull/11978)
    -   `unaryMinus`関数によって返される結果が MySQL と互換性がない問題を修正しました。これは、整数結果がオーバーフローしたときに非小数点結果になるためです。 [＃11990](https://github.com/pingcap/tidb/pull/11990)
    -   `LOAD DATA`文の実行時にカウント順序が原因で`last_insert_id()`間違っている可能性がある問題を修正しました[＃11994](https://github.com/pingcap/tidb/pull/11994)
    -   ユーザーがAUTO_INCREMENT列データを明示的・暗黙的に混合して書き込む場合に`last_insert_id()`間違っている可能性がある問題を修正[＃12001](https://github.com/pingcap/tidb/pull/12001)
    -   関数`JSON_UNQUOTE`引用符の過剰使用に関するバグを修正しました。二重引用符で囲まれた値 ( `"` ) のみ引用符で囲まないようにします。例えば、「 `SELECT JSON_UNQUOTE("\\\\")` 」の結果は「 `\\` 」（変更なし）になります[＃12096](https://github.com/pingcap/tidb/pull/12096)
-   サーバ
    -   TiDBトランザクション再試行する際、最後の再試行時刻から最初の実行時刻までの変更`start ts`スロークエリログに記録される [＃11878](https://github.com/pingcap/tidb/pull/11878)
    -   `LockResolver`のトランザクションのキーの数を追加して、リージョン全体のスキャン操作を回避し、キーの数が減ったときにロックを解決するコストを削減します[＃11889](https://github.com/pingcap/tidb/pull/11889)
    -   スロークエリログで`succ`フィールドの値が正しくない可能性がある問題を修正しました [＃11886](https://github.com/pingcap/tidb/pull/11886)
    -   スロークエリログの`Index_ids`フィールドを`Index_names`フィールドに置き換えて、スロークエリログの使いやすさを向上させます。 [＃12063](https://github.com/pingcap/tidb/pull/12063)
    -   `Duration` `-`が含まれる場合 ( `select time(‘--')`など)、TiDB が`-` EOF エラーとして解析することによって発生する接続切断の問題を修正しました[＃11910](https://github.com/pingcap/tidb/pull/11910)
    -   無効なリージョンを`RegionCache`からより迅速に削除して、このリージョンに送信されるリクエストの数を減らします。 [＃11931](https://github.com/pingcap/tidb/pull/11931)
    -   `oom-action = "cancel"`と OOM が`Insert Into … Select`構文で発生したときに OOM panicの問題を誤って処理することによって発生する接続切断の問題を修正しました。 [＃12126](https://github.com/pingcap/tidb/pull/12126)
-   DDL
    -   `tikvSnapshot`にリバーススキャンインターフェースを追加し、DDL履歴ジョブを効率的にクエリできるようにします。このインターフェースを使用することで、 `ADMIN SHOW DDL JOBS`実行時間が大幅に短縮されます[＃11789](https://github.com/pingcap/tidb/pull/11789)
    -   `CREATE TABLE ... PRE_SPLIT_REGION`構文の改善: `PRE_SPLIT_REGION = N` の場合、事前分割されるリージョンの数を 2^(N-1) から 2^N に変更します。 [＃11797](https://github.com/pingcap/tidb/pull/11797/files)
    -   オンラインワークロードに大きな影響を与えないように、 `Add Index`操作のバックグラウンドワーカースレッドのデフォルトパラメータ値を減らします[＃11875](https://github.com/pingcap/tidb/pull/11875)
    -   `SPLIT TABLE`構文の動作を改善します。`SPLIT TABLE ... REGIONS N`を使用して領域を分割すると、N 個のデータリージョンと 1 つのインデックスリージョンが生成されます。 [＃11929](https://github.com/pingcap/tidb/pull/11929)
    -   設定ファイルに`split-region-max-num`パラメータ（デフォルトでは`10000` ）を追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を調整可能にします[＃12080](https://github.com/pingcap/tidb/pull/12080)
    -   システムがbinlog書き込むときに、この句のコメントが解除された`PRE_SPLIT_REGIONS`原因で、下流のMySQLで`CREATE TABLE`句を解析できない問題を修正しました。 [＃12121](https://github.com/pingcap/tidb/pull/12121)
    -   `SHOW TABLE … REGIONS`と`SHOW TABLE .. INDEX … REGIONS`の`WHERE` のサブ条項を追加する [＃12124](https://github.com/pingcap/tidb/pull/12124)
-   モニター
    -   `tikvclient` の gRPC 接続エラーをカウントするための`connection_transient_failure_count`監視メトリックを追加します。 [＃12092](https://github.com/pingcap/tidb/pull/12092)

## TiKV {#tikv}

-   一部のケースでリージョン内のキーのカウント結果が誤っていた問題を修正[＃5415](https://github.com/tikv/tikv/pull/5415)
-   TiKVに`config-check`オプションを追加して、TiKV構成項目が有効かどうかを確認する[＃5391](https://github.com/tikv/tikv/pull/5391)
-   ノードの再起動によって発生するジッターを軽減するために起動プロセスを最適化します。 [＃5277](https://github.com/tikv/tikv/pull/5277)
-   場合によってはロック解決プロセスを最適化して、トランザクションのロック解決を高速化します。 [＃5339](https://github.com/tikv/tikv/pull/5339)
-   `get_txn_commit_info`プロセスを最適化してトランザクションのコミットを高速化する[＃5062](https://github.com/tikv/tikv/pull/5062)
-   Raft関連のログを簡素化する[＃5425](https://github.com/tikv/tikv/pull/5425)
-   TiKVが一部のケースで異常終了する問題を解決[＃5441](https://github.com/tikv/tikv/pull/5441)

## PD {#pd}

-   PDに`config-check`オプションを追加して、PD構成項目が有効かどうかを確認する[＃1725](https://github.com/pingcap/pd/pull/1725)
-   pd-ctlに`remove-tombstone`コマンドを追加して、tombstoneストアレコードのクリアをサポートする[＃1705](https://github.com/pingcap/pd/pull/1705)
-   オペレーターのスケジュール調整を積極的に促進するサポート[＃1686](https://github.com/pingcap/pd/pull/1686)

## ツール {#tools}

-   TiDB Binlog
    -   Reparoに`worker-count`と`txn-batch`設定項目を追加して回復速度を制御[＃746](https://github.com/pingcap/tidb-binlog/pull/746)
    -   Drainerのメモリ使用量を最適化して並列実行効率を向上させる[＃735](https://github.com/pingcap/tidb-binlog/pull/735)
    -   Pumpが正常に終了できないことがあるバグを修正[＃739](https://github.com/pingcap/tidb-binlog/pull/739)
    -   Pumpの`LevelDB`の処理ロジックを最適化し、GC の実行効率を向上させる [＃720](https://github.com/pingcap/tidb-binlog/pull/720)
-   TiDB Lightning
    -   チェックポイントからデータを再インポートするとtidb-lightningがクラッシュする可能性があるバグを修正しました [＃239](https://github.com/pingcap/tidb-lightning/pull/239)

## TiDB Ansible {#tidb-ansible}

-   Sparkバージョンを2.4.3にアップデートし、TiSparkバージョンをSpark 2.4.3 [＃914](https://github.com/pingcap/tidb-ansible/pull/914) 、 と互換性のある2.2.0にアップデートします。 [＃919](https://github.com/pingcap/tidb-ansible/pull/927)
-   リモートマシンのパスワードの有効期限が切れたときに長い待ち時間が発生する問題を修正[＃937](https://github.com/pingcap/tidb-ansible/pull/937) , [＃948](https://github.com/pingcap/tidb-ansible/pull/948)
