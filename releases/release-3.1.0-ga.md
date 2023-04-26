---
title: TiDB 3.1.0 GA Release Notes
---

# TiDB 3.1.0 GA リリースノート {#tidb-3-1-0-ga-release-notes}

発売日：2020年4月16日

TiDB バージョン: 3.1.0 GA

TiDB Ansible バージョン: 3.1.0 GA

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `report-status` [#16291](https://github.com/pingcap/tidb/pull/16291)構成項目が有効になっているときに HTTP リスニング ポートが使用できない場合、TiDB の開始を直接停止することをサポートします。

-   ツール

    -   バックアップと復元 (BR)

        -   BR は、 3.1 GA [#233](https://github.com/pingcap/br/pull/233)より前の TiKV クラスターからのデータの復元をサポートしていません

## 新機能 {#new-features}

-   TiDB

    -   `explain format = "dot"` [#16125](https://github.com/pingcap/tidb/pull/16125)のコプロセッサー・タスクの情報の表示をサポート
    -   `disable-error-stack`構成項目[#16182](https://github.com/pingcap/tidb/pull/16182)を使用して、ログの冗長なスタック情報を削減します。

-   プレースメントDriver(PD)

    -   ホットリージョンのスケジューリングを最適化する[#2342](https://github.com/pingcap/pd/pull/2342)

-   TiFlash

    -   DeltaTree エンジンの読み取りおよび書き込みワークロードに関連するメトリック レポートを追加します。
    -   `fromUnixTime`および`dateFormat`関数のプッシュ ダウンをサポート
    -   デフォルトでラフ セット フィルタを無効にする

-   TiDB アンシブル

    -   TiFlashモニターの追加[#1253](https://github.com/pingcap/tidb-ansible/pull/1253) [#1257](https://github.com/pingcap/tidb-ansible/pull/1257)
    -   TiFlashの設定パラメータを最適化する[#1262](https://github.com/pingcap/tidb-ansible/pull/1262) [#1265](https://github.com/pingcap/tidb-ansible/pull/1265) [#1271](https://github.com/pingcap/tidb-ansible/pull/1271)
    -   TiDB 開始スクリプトを最適化する[#1268](https://github.com/pingcap/tidb-ansible/pull/1268)

## バグの修正 {#bug-fixes}

-   TiDB

    -   一部のシナリオでマージ結合操作によって引き起こされるpanicの問題を修正します[#15920](https://github.com/pingcap/tidb/pull/15920)
    -   選択度計算[#16052](https://github.com/pingcap/tidb/pull/16052)で一部の式が繰り返しカウントされる問題を修正
    -   極端な場合に統計情報をロードするときに発生したpanicの問題を修正します[#15710](https://github.com/pingcap/tidb/pull/15710)
    -   SQL クエリ[#16015](https://github.com/pingcap/tidb/pull/16015)で同等の式を認識できない場合にエラーが返される問題を修正
    -   あるデータベースの`view`を別のデータベースからクエリするとエラーが返される問題を修正します[#15867](https://github.com/pingcap/tidb/pull/15867)
    -   列が`fast analyze` [#16080](https://github.com/pingcap/tidb/pull/16080)を使用して処理されるときに発生するpanicの問題を修正します。
    -   `current_role`印刷結果の間違った文字セットを修正[#16084](https://github.com/pingcap/tidb/pull/16084)
    -   MySQL 接続ハンドシェイク エラー[#15799](https://github.com/pingcap/tidb/pull/15799)のログを絞り込む
    -   監査プラグインがロードされた後のポートプローブによって引き起こされるpanicの問題を修正します[#16065](https://github.com/pingcap/tidb/pull/16065)
    -   `TypeNull`クラスが可変長型[#15739](https://github.com/pingcap/tidb/pull/15739)と間違えられるため、左結合の`sort`演算子のpanicの問題を修正します。
    -   監視セッションの再試行エラーの不正確なカウントの問題を修正します[#16120](https://github.com/pingcap/tidb/pull/16120)
    -   `ALLOW_INVALID_DATES`モード[#16171](https://github.com/pingcap/tidb/pull/16171)で`weekday`の結果が間違っていた問題を修正
    -   クラスターにTiFlashノードがある場合、ガベージ コレクション (GC) が正常に機能しない場合がある問題を修正します[#15761](https://github.com/pingcap/tidb/pull/15761)
    -   ユーザーがハッシュパーティションテーブルを作成するときに大きなパーティション数を設定すると、TiDB がメモリ不足 (OOM) になる問題を修正します[#16219](https://github.com/pingcap/tidb/pull/16219)
    -   警告がエラーと誤認される問題を修正し、 `UNION`ステートメントを`SELECT`ステートメントと同じ動作にする[#16138](https://github.com/pingcap/tidb/pull/16138)
    -   mocktikv [#16200](https://github.com/pingcap/tidb/pull/16200)に`TopN`をpushした時の実行エラーを修正
    -   `runtime.growslice` [#16142](https://github.com/pingcap/tidb/pull/16142)の不要なオーバーヘッドを回避するために、初期の長さ`chunk.column.nullBitMap`増やします。

-   TiKV

    -   レプリカの読み取りによって引き起こされるpanicの問題を修正します[#7418](https://github.com/tikv/tikv/pull/7418) [#7369](https://github.com/tikv/tikv/pull/7369)
    -   復元プロセスで空のリージョンが作成される問題を修正します[#7419](https://github.com/tikv/tikv/pull/7419)
    -   解決ロック要求を繰り返すと、悲観的トランザクションの原子性が損なわれる可能性があるという問題を修正します[#7389](https://github.com/tikv/tikv/pull/7389)

-   TiFlash

    -   TiDB からスキーマを複製する際の`rename table`操作の潜在的な問題を修正します。
    -   複数のデータ パス構成で`rename table`操作が原因で発生するデータ損失の問題を修正します。
    -   一部のシナリオでTiFlash が誤ったstorage容量を報告する問題を修正
    -   リージョンマージが有効な場合にTiFlashからの読み取りによって引き起こされる潜在的な問題を修正します。

-   ツール

    -   TiDBBinlog

        -   TiFlash関連の DDL ジョブがDrainer [#948](https://github.com/pingcap/tidb-binlog/pull/948) [#942](https://github.com/pingcap/tidb-binlog/pull/942)のレプリケーションを中断する可能性がある問題を修正します。

    -   バックアップと復元 (BR)

        -   `checksum`操作を無効にしても実行される問題を修正[#223](https://github.com/pingcap/br/pull/223)
        -   TiDB が`auto-random`または`alter-pk` [#230](https://github.com/pingcap/br/pull/230) [#231](https://github.com/pingcap/br/pull/231)を有効にすると、増分バックアップが失敗する問題を修正します。
