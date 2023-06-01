---
title: TiDB 3.1.0 GA Release Notes
---

# TiDB 3.1.0 GA リリースノート {#tidb-3-1-0-ga-release-notes}

発売日：2020年4月16日

TiDB バージョン: 3.1.0 GA

TiDB Ansible バージョン: 3.1.0 GA

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `report-status`構成項目が有効になっているときに HTTP リスニング ポートが使用できない場合、TiDB の起動を直接停止するサポート[<a href="https://github.com/pingcap/tidb/pull/16291">#16291</a>](https://github.com/pingcap/tidb/pull/16291)

-   ツール

    -   バックアップと復元 (BR)

        -   BR は、 3.1 GA [<a href="https://github.com/pingcap/br/pull/233">#233</a>](https://github.com/pingcap/br/pull/233)より前の TiKV クラスターからのデータの復元をサポートしていません。

## 新機能 {#new-features}

-   TiDB

    -   `explain format = "dot"` [<a href="https://github.com/pingcap/tidb/pull/16125">#16125</a>](https://github.com/pingcap/tidb/pull/16125)でのコプロセッサータスクの情報の表示をサポート
    -   `disable-error-stack`設定項目[<a href="https://github.com/pingcap/tidb/pull/16182">#16182</a>](https://github.com/pingcap/tidb/pull/16182)を使用してログの冗長なスタック情報を削減する

-   配置Driver(PD)

    -   ホットリージョンのスケジュールを最適化する[<a href="https://github.com/pingcap/pd/pull/2342">#2342</a>](https://github.com/pingcap/pd/pull/2342)

-   TiFlash

    -   DeltaTree エンジンの読み取りおよび書き込みワークロードに関連するメトリクス レポートを追加します。
    -   `fromUnixTime`と`dateFormat`関数の押し下げをサポート
    -   ラフセットフィルターをデフォルトで無効にする

-   TiDB Ansible

    -   TiFlashモニターを追加[<a href="https://github.com/pingcap/tidb-ansible/pull/1253">#1253</a>](https://github.com/pingcap/tidb-ansible/pull/1253) [<a href="https://github.com/pingcap/tidb-ansible/pull/1257">#1257</a>](https://github.com/pingcap/tidb-ansible/pull/1257)
    -   TiFlash [<a href="https://github.com/pingcap/tidb-ansible/pull/1262">#1262</a>](https://github.com/pingcap/tidb-ansible/pull/1262) [<a href="https://github.com/pingcap/tidb-ansible/pull/1265">#1265</a>](https://github.com/pingcap/tidb-ansible/pull/1265) [<a href="https://github.com/pingcap/tidb-ansible/pull/1271">#1271</a>](https://github.com/pingcap/tidb-ansible/pull/1271)の設定パラメータを最適化します。
    -   TiDB 起動スクリプト[<a href="https://github.com/pingcap/tidb-ansible/pull/1268">#1268</a>](https://github.com/pingcap/tidb-ansible/pull/1268)を最適化する

## バグの修正 {#bug-fixes}

-   TiDB

    -   一部のシナリオでマージ結合操作によって引き起こされるpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/15920">#15920</a>](https://github.com/pingcap/tidb/pull/15920)
    -   選択性計算[<a href="https://github.com/pingcap/tidb/pull/16052">#16052</a>](https://github.com/pingcap/tidb/pull/16052)で一部の式が繰り返しカウントされる問題を修正
    -   極端な場合に統計情報をロードする際に発生するpanic問題を修正[<a href="https://github.com/pingcap/tidb/pull/15710">#15710</a>](https://github.com/pingcap/tidb/pull/15710)
    -   SQLクエリ[<a href="https://github.com/pingcap/tidb/pull/16015">#16015</a>](https://github.com/pingcap/tidb/pull/16015)で同等の式が認識できない場合にエラーが返される場合がある問題を修正
    -   あるデータベースの`view`を別のデータベース[<a href="https://github.com/pingcap/tidb/pull/15867">#15867</a>](https://github.com/pingcap/tidb/pull/15867)からクエリするとエラーが返される問題を修正します。
    -   列が`fast analyze` [<a href="https://github.com/pingcap/tidb/pull/16080">#16080</a>](https://github.com/pingcap/tidb/pull/16080)を使用して処理されるときに発生するpanicの問題を修正します。
    -   `current_role`印刷結果の不正な文字セットを修正[<a href="https://github.com/pingcap/tidb/pull/16084">#16084</a>](https://github.com/pingcap/tidb/pull/16084)
    -   MySQL 接続ハンドシェイク エラー[<a href="https://github.com/pingcap/tidb/pull/15799">#15799</a>](https://github.com/pingcap/tidb/pull/15799)のログを詳細化する
    -   監査プラグインがロードされた後のポートプローブによって引き起こされるpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/16065">#16065</a>](https://github.com/pingcap/tidb/pull/16065)
    -   `TypeNull`クラスが可変長型[<a href="https://github.com/pingcap/tidb/pull/15739">#15739</a>](https://github.com/pingcap/tidb/pull/15739)と誤認されるため、左結合の`sort`演算子がパニックになるpanicを修正しました。
    -   モニタリングセッションのリトライエラー数が不正確になる問題を修正[<a href="https://github.com/pingcap/tidb/pull/16120">#16120</a>](https://github.com/pingcap/tidb/pull/16120)
    -   `ALLOW_INVALID_DATES`モード[<a href="https://github.com/pingcap/tidb/pull/16171">#16171</a>](https://github.com/pingcap/tidb/pull/16171)の`weekday`の結果が間違っている問題を修正
    -   クラスターにTiFlashノード[<a href="https://github.com/pingcap/tidb/pull/15761">#15761</a>](https://github.com/pingcap/tidb/pull/15761)がある場合、ガベージ コレクション (GC) が正常に動作しない可能性がある問題を修正します。
    -   ハッシュパーティションテーブル[<a href="https://github.com/pingcap/tidb/pull/16219">#16219</a>](https://github.com/pingcap/tidb/pull/16219)の作成時にユーザーが大きなパーティション数を設定すると、TiDB がメモリ不足 (OOM) になる問題を修正します。
    -   警告がエラーと誤認される問題を修正し、 `UNION`ステートメントを`SELECT`ステートメントと同じ動作にする[<a href="https://github.com/pingcap/tidb/pull/16138">#16138</a>](https://github.com/pingcap/tidb/pull/16138)
    -   `TopN`をmocktikv [<a href="https://github.com/pingcap/tidb/pull/16200">#16200</a>](https://github.com/pingcap/tidb/pull/16200)にプッシュダウンしたときの実行エラーを修正
    -   `runtime.growslice` [<a href="https://github.com/pingcap/tidb/pull/16142">#16142</a>](https://github.com/pingcap/tidb/pull/16142)の不要なオーバーヘッドを避けるために、初期の長さ`chunk.column.nullBitMap`増やします。

-   TiKV

    -   レプリカ読み取りによるpanic問題を修正[<a href="https://github.com/tikv/tikv/pull/7418">#7418</a>](https://github.com/tikv/tikv/pull/7418) [<a href="https://github.com/tikv/tikv/pull/7369">#7369</a>](https://github.com/tikv/tikv/pull/7369)
    -   復元プロセスで空のリージョン[<a href="https://github.com/tikv/tikv/pull/7419">#7419</a>](https://github.com/tikv/tikv/pull/7419)が作成される問題を修正
    -   ロック解決リクエストを繰り返すと、悲観的トランザクションのアトミック性が損なわれる可能性がある問題を修正します[<a href="https://github.com/tikv/tikv/pull/7389">#7389</a>](https://github.com/tikv/tikv/pull/7389)

-   TiFlash

    -   TiDB からスキーマをレプリケートするときの`rename table`操作の潜在的な問題を修正します。
    -   複数のデータ パス構成での`rename table`操作によって発生するデータ損失の問題を修正
    -   一部のシナリオでTiFlash が誤ったstorage容量を報告する問題を修正
    -   リージョンマージが有効な場合にTiFlashからの読み取りによって引き起こされる潜在的な問題を修正

-   ツール

    -   TiDBBinlog

        -   TiFlash関連の DDL ジョブがDrainer [<a href="https://github.com/pingcap/tidb-binlog/pull/948">#948</a>](https://github.com/pingcap/tidb-binlog/pull/948) [<a href="https://github.com/pingcap/tidb-binlog/pull/942">#942</a>](https://github.com/pingcap/tidb-binlog/pull/942)のレプリケーションを中断する可能性がある問題を修正

    -   バックアップと復元 (BR)

        -   `checksum`操作が無効になっている場合でも実行される問題を修正[<a href="https://github.com/pingcap/br/pull/223">#223</a>](https://github.com/pingcap/br/pull/223)
        -   TiDB が`auto-random`または`alter-pk`を有効にすると増分バックアップが失敗する問題[<a href="https://github.com/pingcap/br/pull/230">#230</a>](https://github.com/pingcap/br/pull/230)修正[<a href="https://github.com/pingcap/br/pull/231">#231</a>](https://github.com/pingcap/br/pull/231)
