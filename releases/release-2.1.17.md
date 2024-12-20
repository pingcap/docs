---
title: TiDB 2.1.17 Release Notes
summary: 「TiDB 2.1.17 リリース ノート 新機能には、SHOW TABLE REGIONS` の `WHERE` 句、TiKV および PD の `config-check` 機能、pd-ctl の `remove-tombstone` コマンド、 Reparoの `worker-count` および `txn-batch` 構成項目が含まれます。PD のスケジュール プロセスと TiKV の開始プロセスが改善されました。TiDB スロー クエリ ログと構成ファイルの動作が変更されました。SQL オプティマイザー、SQL 実行エンジン、サーバー、DDL、モニター、TiKV、PD、TiDB Binlog、 TiDB Lightning、および TiDB Ansible の修正と最適化が行われました。」
---

# TiDB 2.1.17 リリースノート {#tidb-2-1-17-release-notes}

発売日: 2019年9月11日

TiDB バージョン: 2.1.17

TiDB Ansible バージョン: 2.1.17

-   新機能
    -   TiDBの`SHOW TABLE REGIONS`の構文に`WHERE`句を追加する
    -   TiKVとPDに`config-check`機能を追加して構成項目をチェックする
    -   pd-ctl に`remove-tombstone`コマンドを追加して、トゥームストーン ストアのレコードをクリアします。
    -   Reparoに`worker-count`と`txn-batch`設定項目を追加して回復速度を制御します

-   改善点
    -   積極的にプッシュするオペレーターをサポートすることでPDのスケジュールプロセスを最適化します
    -   TiKV の起動プロセスを最適化し、ノードの再起動によって発生するジッターを軽減します。

-   行動の変化
    -   TiDB スロークエリログの最後の再試行時間から最初の実行時間への変更`start ts`
    -   TiDB スロークエリログの`Index_ids`フィールドを`Index_names`フィールドに置き換えて、スロークエリログの使いやすさを向上させます。
    -   TiDB の構成ファイルに`split-region-max-num`パラメータを追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を変更します。デフォルト構成では、1,000 から 10,000 に増加されます。

## ティビ {#tidb}

-   SQL オプティマイザー
    -   `EvalSubquery`ビルド`Executor` [＃11811](https://github.com/pingcap/tidb/pull/11811)中にエラーが発生したときにエラーメッセージが正しく返されない問題を修正
    -   Index Lookup Joinで外部テーブルの行数が1バッチの行数より多い場合にクエリ結果が正しくない可能性がある問題を修正しました。Index Lookup Joinの機能範囲を拡張しました`UnionScan` `IndexJoin` [＃11843](https://github.com/pingcap/tidb/pull/11843)のサブノードとして使用できます。
    -   統計フィードバック処理中に無効なキーが発生する可能性がある状況に備えて、 `SHOW STAT_BUCKETS`構文に無効なキー（ `invalid encoded key flag 252`など）の表示を追加します[＃12098](https://github.com/pingcap/tidb/pull/12098)
-   SQL実行エンジン
    -   `CAST`関数が数値型[＃11712](https://github.com/pingcap/tidb/pull/11712)変換するときに、最初に`UINT`に変換される数値によって発生するいくつかの誤った結果 ( `select cast(13835058000000000000 as double)`など) を修正しました。
    -   `DIV`計算の被除数が小数で、この計算に負の数[＃11812](https://github.com/pingcap/tidb/pull/11812)が含まれている場合に計算結果が不正確になる可能性がある問題を修正しました。
    -   `SELECT`ステートメント`EXPLAIN` [＃11892](https://github.com/pingcap/tidb/pull/11892)実行するときに一部の文字列が`INT`型に変換されることで発生する MySQL の非互換性の問題を修正するために`ConvertStrToIntStrict`関数を追加します。
    -   `EXPLAIN ... FOR CONNECTION`が使用されている場合に`stmtCtx`の設定が間違っているために`Explain`結果が正しくない可能性がある問題を修正しました[＃11978](https://github.com/pingcap/tidb/pull/11978)
    -   `unaryMinus`関数によって返される結果が MySQL と互換性がない問題を修正しました。これは、整数結果が[＃11990](https://github.com/pingcap/tidb/pull/11990)をオーバーフローしたときに 10 進数以外の結果になるためです。
    -   `LOAD DATA`文の実行時にカウント順序が原因で`last_insert_id()`が間違っている可能性がある問題を修正しました[＃11994](https://github.com/pingcap/tidb/pull/11994)
    -   ユーザーが自動増分列データを明示的・暗黙的に混合して書き込む場合に`last_insert_id()`が間違っている可能性がある問題を修正[＃12001](https://github.com/pingcap/tidb/pull/12001)
    -   `JSON_UNQUOTE`関数の引用符の過剰使用バグを修正: 二重引用符で囲まれた値 ( `"` ) のみ引用符を外す必要があります。たとえば、「 `SELECT JSON_UNQUOTE("\\\\")` 」の結果は「 `\\` 」になります (変更なし) [＃12096](https://github.com/pingcap/tidb/pull/12096)
-   サーバ
    -   TiDBトランザクション[＃11878](https://github.com/pingcap/tidb/pull/11878)を再試行する際、最後の再試行時間から最初の実行時間までの変更`start ts`がスロークエリログに記録される
    -   `LockResolver`のトランザクションのキーの数を追加して、リージョン全体のスキャン操作を回避し、キーの数が減った場合にロックを解決するコストを削減します[＃11889](https://github.com/pingcap/tidb/pull/11889)
    -   スロークエリログ[＃11886](https://github.com/pingcap/tidb/pull/11886)でフィールド`succ`の値が正しくない可能性がある問題を修正
    -   スロークエリログの`Index_ids`フィールドを`Index_names`フィールドに置き換えて、スロークエリログ[＃12063](https://github.com/pingcap/tidb/pull/12063)の使いやすさを向上させます。
    -   `Duration`に`-`含まれる場合 ( `select time(‘--')`など)、TiDB が`-` EOF エラーとして解析することで発生する接続切断の問題を修正しました[＃11910](https://github.com/pingcap/tidb/pull/11910)
    -   無効なリージョンを`RegionCache`からより迅速に削除して、このリージョン[＃11931](https://github.com/pingcap/tidb/pull/11931)に送信されるリクエストの数を減らします。
    -   `oom-action = "cancel"`と OOM が`Insert Into … Select`構文[＃12126](https://github.com/pingcap/tidb/pull/12126)で発生したときに OOMpanicの問題を誤って処理することによって発生する接続切断の問題を修正しました。
-   DDL
    -   `tikvSnapshot`のリバーススキャンインターフェースを追加して、DDL 履歴ジョブを効率的にクエリします。このインターフェースを使用すると、 `ADMIN SHOW DDL JOBS`の実行時間が大幅に短縮されます[＃11789](https://github.com/pingcap/tidb/pull/11789)
    -   `CREATE TABLE ... PRE_SPLIT_REGION`構文の改善： `PRE_SPLIT_REGION = N` [＃11797](https://github.com/pingcap/tidb/pull/11797/files)の場合、事前分割領域の数を2^(N-1)から2^Nに変更します。
    -   オンラインワークロードに大きな影響を与えないように、 `Add Index`操作のバックグラウンドワーカースレッドのデフォルトパラメータ値を減らします[＃11875](https://github.com/pingcap/tidb/pull/11875)
    -   `SPLIT TABLE`構文の動作を改善します`SPLIT TABLE ... REGIONS N`使用して領域[＃11929](https://github.com/pingcap/tidb/pull/11929)を分割すると、N 個のデータリージョンと 1 つのインデックスリージョンが生成されます。
    -   設定ファイルに`split-region-max-num`パラメータ（デフォルトでは`10000` ）を追加して、 `SPLIT TABLE`構文で許可されるリージョンの最大数を調整可能にします[＃12080](https://github.com/pingcap/tidb/pull/12080)
    -   システムがbinlog[＃12121](https://github.com/pingcap/tidb/pull/12121)書き込むときに、この句のコメントが解除された`PRE_SPLIT_REGIONS`が原因で、下流のMySQLで`CREATE TABLE`句を解析できない問題を修正しました。
    -   `SHOW TABLE … REGIONS`と`SHOW TABLE .. INDEX … REGIONS`の`WHERE` [＃12124](https://github.com/pingcap/tidb/pull/12124)のサブ条項を追加する
-   モニター
    -   `tikvclient` [＃12092](https://github.com/pingcap/tidb/pull/12092)のgRPC接続エラーをカウントするために`connection_transient_failure_count`監視メトリックを追加します。

## ティクヴ {#tikv}

-   一部のケースでリージョン内のキーをカウントした結果が誤っていた問題を修正[＃5415](https://github.com/tikv/tikv/pull/5415)
-   TiKVに`config-check`オプションを追加して、TiKV構成項目が有効かどうかを確認します[＃5391](https://github.com/tikv/tikv/pull/5391)
-   起動プロセスを最適化して、ノードの再起動によって発生するジッターを軽減する[＃5277](https://github.com/tikv/tikv/pull/5277)
-   トランザクション[＃5339](https://github.com/tikv/tikv/pull/5339)のロック解決を高速化するために、場合によってはロック解決プロセスを最適化します。
-   `get_txn_commit_info`プロセスを最適化してトランザクションのコミットを高速化する[＃5062](https://github.com/tikv/tikv/pull/5062)
-   Raft関連のログを簡素化する[＃5425](https://github.com/tikv/tikv/pull/5425)
-   TiKVが異常終了する場合がある問題を解決[＃5441](https://github.com/tikv/tikv/pull/5441)

## PD {#pd}

-   PDに`config-check`オプションを追加して、PD構成項目が有効かどうかを確認します[＃1725](https://github.com/pingcap/pd/pull/1725)
-   pd-ctl に`remove-tombstone`コマンドを追加して、トゥームストーン ストア レコードのクリアをサポートする[＃1705](https://github.com/pingcap/pd/pull/1705)
-   オペレーターに積極的にスケジュールのスピードアップを促すサポート[＃1686](https://github.com/pingcap/pd/pull/1686)

## ツール {#tools}

-   TiDBBinlog
    -   Reparoに`worker-count`と`txn-batch`設定項目を追加して回復速度を制御する[＃746](https://github.com/pingcap/tidb-binlog/pull/746)
    -   Drainerのメモリ使用量を最適化して並列実行効率を向上させる[＃735](https://github.com/pingcap/tidb-binlog/pull/735)
    -   Pumpが正常に終了できないことがあるバグを修正[＃739](https://github.com/pingcap/tidb-binlog/pull/739)
    -   Pumpの`LevelDB`の処理ロジックを最適化し、GC [＃720](https://github.com/pingcap/tidb-binlog/pull/720)の実行効率を向上
-   TiDB Lightning
    -   チェックポイント[＃239](https://github.com/pingcap/tidb-lightning/pull/239)からデータを再インポートすると tidb-lightning がクラッシュする可能性があるバグを修正しました。

## TiDB アンシブル {#tidb-ansible}

-   Sparkバージョンを2.4.3にアップデートし、TiSparkバージョンをSpark 2.4.3 [＃914](https://github.com/pingcap/tidb-ansible/pull/914) 、 [＃919](https://github.com/pingcap/tidb-ansible/pull/927)と互換性のある2.2.0にアップデートします。
-   リモートマシンのパスワードの有効期限が切れたときに長い待ち時間が発生する問題を修正[＃937](https://github.com/pingcap/tidb-ansible/pull/937) 、 [＃948](https://github.com/pingcap/tidb-ansible/pull/948)
