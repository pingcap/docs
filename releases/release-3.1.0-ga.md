---
title: TiDB 3.1.0 GA Release Notes
---

# TiDB3.1.0GAリリースノート {#tidb-3-1-0-ga-release-notes}

発売日：2020年4月16日

TiDBバージョン：3.1.0 GA

TiDB Ansibleバージョン：3.1.0 GA

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `report-status`構成項目が有効になっているときにHTTPリスニングポートが使用できない場合、TiDBの起動を直接停止することをサポートします[＃16291](https://github.com/pingcap/tidb/pull/16291)

-   ツール

    -   バックアップと復元（BR）

        -   BRは、3.1GA1より前の[＃233](https://github.com/pingcap/br/pull/233)クラスタからのデータの復元をサポートしていません。

## 新機能 {#new-features}

-   TiDB

    -   [＃16125](https://github.com/pingcap/tidb/pull/16125)でのコプロセッサータスクの情報の表示をサポートし`explain format = "dot"` 。
    -   `disable-error-stack`構成項目[＃16182](https://github.com/pingcap/tidb/pull/16182)を使用して、ログの冗長スタック情報を削減します。

-   配置Driver（PD）

    -   ホットリージョンのスケジューリングを最適化する[＃2342](https://github.com/pingcap/pd/pull/2342)

-   TiFlash

    -   DeltaTreeエンジンの読み取りおよび書き込みワークロードに関連するメトリックレポートを追加します
    -   `fromUnixTime`と`dateFormat`の関数のプッシュダウンをサポート
    -   ラフ集合フィルターをデフォルトで無効にします

-   TiDB Ansible

    -   [＃1257](https://github.com/pingcap/tidb-ansible/pull/1257)モニターを追加[＃1253](https://github.com/pingcap/tidb-ansible/pull/1253)
    -   [＃1262](https://github.com/pingcap/tidb-ansible/pull/1262)の構成[＃1271](https://github.com/pingcap/tidb-ansible/pull/1271)を最適化する[＃1265](https://github.com/pingcap/tidb-ansible/pull/1265)
    -   TiDB開始スクリプトを最適化する[＃1268](https://github.com/pingcap/tidb-ansible/pull/1268)

## バグの修正 {#bug-fixes}

-   TiDB

    -   一部のシナリオでのマージ結合操作によって引き起こされるpanicの問題を修正します[＃15920](https://github.com/pingcap/tidb/pull/15920)
    -   選択性の計算で一部の式が繰り返しカウントされる問題を修正[＃16052](https://github.com/pingcap/tidb/pull/16052)
    -   極端な場合に統計情報をロードするときに発生したpanicの問題を修正します[＃15710](https://github.com/pingcap/tidb/pull/15710)
    -   SQLクエリ[＃16015](https://github.com/pingcap/tidb/pull/16015)で同等の式を認識できない場合にエラーが返される問題を修正しました
    -   あるデータベースの`view`つを別のデータベースからクエリするとエラーが返される問題を修正します[＃15867](https://github.com/pingcap/tidb/pull/15867)
    -   列が[＃16080](https://github.com/pingcap/tidb/pull/16080)を使用して処理されるときに発生するpanicの問題を修正し`fast analyze`
    -   `current_role`印刷結果[＃16084](https://github.com/pingcap/tidb/pull/16084)の誤った文字セットを修正します
    -   MySQL接続ハンドシェイクエラー[＃15799](https://github.com/pingcap/tidb/pull/15799)のログを調整します
    -   監査プラグインがロードされた後のポートプロービングによって引き起こされるpanicの問題を修正します[＃16065](https://github.com/pingcap/tidb/pull/16065)
    -   `TypeNull`クラスが可変長タイプ[＃15739](https://github.com/pingcap/tidb/pull/15739)と間違えられるため、左結合の`sort`演算子のpanicの問題を修正します。
    -   監視セッションの再試行エラーのカウントが不正確になる問題を修正します[＃16120](https://github.com/pingcap/tidb/pull/16120)
    -   `ALLOW_INVALID_DATES`モード[＃16171](https://github.com/pingcap/tidb/pull/16171)で`weekday`の間違った結果の問題を修正します
    -   クラスタにTiFlashノードがある場合にガベージコレクション（GC）が正常に機能しない可能性がある問題を修正します[＃15761](https://github.com/pingcap/tidb/pull/15761)
    -   ユーザーがハッシュパーティションテーブル[＃16219](https://github.com/pingcap/tidb/pull/16219)を作成するときに大きなパーティションカウントを設定すると、TiDBがメモリ（OOM）を使い果たす問題を修正します。
    -   警告がエラーと間違われる問題を修正し、 `UNION`ステートメントが`SELECT`ステートメントと同じ動作をするようにします[＃16138](https://github.com/pingcap/tidb/pull/16138)
    -   `TopN`が[＃16200](https://github.com/pingcap/tidb/pull/16200)にプッシュダウンされたときの実行エラーを修正しました
    -   `runtime.growslice` [＃16142](https://github.com/pingcap/tidb/pull/16142)の不要なオーバーヘッドを回避するために、初期長を`chunk.column.nullBitMap`に増やします。

-   TiKV

    -   レプリカ読み取りによって引き起こされるpanicの問題を修正し[＃7369](https://github.com/tikv/tikv/pull/7369) [＃7418](https://github.com/tikv/tikv/pull/7418)
    -   復元プロセスで空のリージョンが作成される問題を修正します[＃7419](https://github.com/tikv/tikv/pull/7419)
    -   ロック要求の解決を繰り返すと、悲観的なトランザクションの原子性が損なわれる可能性があるという問題を修正します[＃7389](https://github.com/tikv/tikv/pull/7389)

-   TiFlash

    -   TiDBからスキーマを複製するときの`rename table`の操作の潜在的な問題を修正します
    -   複数のデータパス構成での`rename table`の操作によって引き起こされるデータ損失の問題を修正します
    -   一部のシナリオでTiFlashが誤ったストレージスペースを報告する問題を修正します
    -   リージョンマージが有効になっているときにTiFlashから読み取ることによって引き起こされる潜在的な問題を修正します

-   ツール

    -   TiDB Binlog

        -   [＃942](https://github.com/pingcap/tidb-binlog/pull/942)関連のDDLジョブがDrainerのレプリケーションを中断する可能性がある問題を修正し[＃948](https://github.com/pingcap/tidb-binlog/pull/948)

    -   バックアップと復元（BR）

        -   `checksum`操作が無効になっても実行される問題を修正します[＃223](https://github.com/pingcap/br/pull/223)
        -   `alter-pk`が`auto-random`または[＃231](https://github.com/pingcap/br/pull/231)を有効にすると、増分バックアップが失敗する問題を修正し[＃230](https://github.com/pingcap/br/pull/230) 。
