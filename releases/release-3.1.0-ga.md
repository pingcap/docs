---
title: TiDB 3.1.0 GA Release Notes
---

# TiDB 3.1.0 GA リリースノート {#tidb-3-1-0-ga-release-notes}

発売日：2020年4月16日

TiDB バージョン: 3.1.0 GA

TiDB Ansible バージョン: 3.1.0 GA

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `report-status`構成項目が有効になっているときに HTTP リスニング ポートが使用できない場合、TiDB の起動を直接停止するサポート[#16291](https://github.com/pingcap/tidb/pull/16291)

-   ツール

    -   バックアップと復元 (BR)

        -   BR は、 3.1 GA [#233](https://github.com/pingcap/br/pull/233)より前の TiKV クラスターからのデータの復元をサポートしていません。

## 新機能 {#new-features}

-   TiDB

    -   `explain format = "dot"` [#16125](https://github.com/pingcap/tidb/pull/16125)でのコプロセッサータスクの情報の表示をサポート
    -   `disable-error-stack`設定項目[#16182](https://github.com/pingcap/tidb/pull/16182)を使用してログの冗長なスタック情報を削減する

-   配置Driver(PD)

    -   ホットリージョンのスケジュールを最適化する[#2342](https://github.com/pingcap/pd/pull/2342)

-   TiFlash

    -   DeltaTree エンジンの読み取りおよび書き込みワークロードに関連するメトリクス レポートを追加します。
    -   `fromUnixTime`と`dateFormat`関数の押し下げをサポート
    -   ラフセットフィルターをデフォルトで無効にする

-   TiDB Ansible

    -   TiFlashモニターを追加[#1253](https://github.com/pingcap/tidb-ansible/pull/1253) [#1257](https://github.com/pingcap/tidb-ansible/pull/1257)
    -   TiFlash [#1262](https://github.com/pingcap/tidb-ansible/pull/1262) [#1265](https://github.com/pingcap/tidb-ansible/pull/1265) [#1271](https://github.com/pingcap/tidb-ansible/pull/1271)の設定パラメータを最適化します。
    -   TiDB 起動スクリプト[#1268](https://github.com/pingcap/tidb-ansible/pull/1268)を最適化する

## バグの修正 {#bug-fixes}

-   TiDB

    -   一部のシナリオでマージ結合操作によって引き起こされるpanicの問題を修正します[#15920](https://github.com/pingcap/tidb/pull/15920)
    -   選択性計算[#16052](https://github.com/pingcap/tidb/pull/16052)で一部の式が繰り返しカウントされる問題を修正
    -   極端な場合に統計情報をロードする際に発生するpanic問題を修正[#15710](https://github.com/pingcap/tidb/pull/15710)
    -   SQLクエリ[#16015](https://github.com/pingcap/tidb/pull/16015)で同等の式が認識できない場合にエラーが返される場合がある問題を修正
    -   あるデータベースの`view`を別のデータベース[#15867](https://github.com/pingcap/tidb/pull/15867)からクエリするとエラーが返される問題を修正します。
    -   列が`fast analyze` [#16080](https://github.com/pingcap/tidb/pull/16080)を使用して処理されるときに発生するpanicの問題を修正します。
    -   `current_role`印刷結果の不正な文字セットを修正[#16084](https://github.com/pingcap/tidb/pull/16084)
    -   MySQL 接続ハンドシェイク エラー[#15799](https://github.com/pingcap/tidb/pull/15799)のログを詳細化する
    -   監査プラグインがロードされた後のポートプローブによって引き起こされるpanicの問題を修正します[#16065](https://github.com/pingcap/tidb/pull/16065)
    -   `TypeNull`クラスが可変長型[#15739](https://github.com/pingcap/tidb/pull/15739)と誤認されるため、左結合の`sort`演算子がパニックになるpanicを修正しました。
    -   モニタリングセッションのリトライエラー数が不正確になる問題を修正[#16120](https://github.com/pingcap/tidb/pull/16120)
    -   `ALLOW_INVALID_DATES`モード[#16171](https://github.com/pingcap/tidb/pull/16171)の`weekday`の結果が間違っている問題を修正
    -   クラスターにTiFlashノード[#15761](https://github.com/pingcap/tidb/pull/15761)がある場合、ガベージ コレクション (GC) が正常に動作しない可能性がある問題を修正します。
    -   ハッシュパーティションテーブル[#16219](https://github.com/pingcap/tidb/pull/16219)の作成時にユーザーが大きなパーティション数を設定すると、TiDB がメモリ不足 (OOM) になる問題を修正します。
    -   警告がエラーと誤認される問題を修正し、 `UNION`ステートメントを`SELECT`ステートメントと同じ動作にする[#16138](https://github.com/pingcap/tidb/pull/16138)
    -   `TopN`をmocktikv [#16200](https://github.com/pingcap/tidb/pull/16200)にプッシュダウンしたときの実行エラーを修正
    -   `runtime.growslice` [#16142](https://github.com/pingcap/tidb/pull/16142)の不要なオーバーヘッドを避けるために、初期の長さ`chunk.column.nullBitMap`増やします。

-   TiKV

    -   レプリカ読み取りによるpanic問題を修正[#7418](https://github.com/tikv/tikv/pull/7418) [#7369](https://github.com/tikv/tikv/pull/7369)
    -   復元プロセスで空のリージョン[#7419](https://github.com/tikv/tikv/pull/7419)が作成される問題を修正
    -   ロック解決リクエストを繰り返すと、悲観的トランザクションのアトミック性が損なわれる可能性がある問題を修正します[#7389](https://github.com/tikv/tikv/pull/7389)

-   TiFlash

    -   TiDB からスキーマをレプリケートするときの`rename table`操作の潜在的な問題を修正します。
    -   複数のデータ パス構成での`rename table`操作によって発生するデータ損失の問題を修正
    -   一部のシナリオでTiFlash が誤ったstorage容量を報告する問題を修正
    -   リージョンマージが有効な場合にTiFlashからの読み取りによって引き起こされる潜在的な問題を修正

-   ツール

    -   TiDBBinlog

        -   TiFlash関連の DDL ジョブがDrainer [#948](https://github.com/pingcap/tidb-binlog/pull/948) [#942](https://github.com/pingcap/tidb-binlog/pull/942)のレプリケーションを中断する可能性がある問題を修正

    -   バックアップと復元 (BR)

        -   `checksum`操作が無効になっている場合でも実行される問題を修正[#223](https://github.com/pingcap/br/pull/223)
        -   TiDB が`auto-random`または`alter-pk`を有効にすると増分バックアップが失敗する問題を修正[#230](https://github.com/pingcap/br/pull/230) [#231](https://github.com/pingcap/br/pull/231)
