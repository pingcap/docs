---
title: TiDB 3.1.0 GA Release Notes
summary: TiDB 3.1.0 GAは2020年4月16日にリリースされました。TiDB、 TiFlash、TiKV、そしてBackup & RestoreやTiDB Binlogなどのツールに対する互換性の変更、新機能、バグ修正、そして改善が含まれています。主な変更点としては、コプロセッサータスクの表示サポート、ホットリージョンスケジューリングの最適化、そして様々なpanicおよびデータ損失の問題の修正などが挙げられます。また、このリリースには、監視と設定パラメータの改善のためのTiDB Ansibleの改善も含まれています。
---

# TiDB 3.1.0 GA リリースノート {#tidb-3-1-0-ga-release-notes}

発売日：2020年4月16日

TiDB バージョン: 3.1.0 GA

TiDB Ansible バージョン: 3.1.0 GA

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   `report-status`構成項目が有効になっているときに HTTP リスニング ポートが利用できない場合に TiDB の起動を直接停止する機能をサポート[＃16291](https://github.com/pingcap/tidb/pull/16291)

-   ツール

    -   バックアップと復元 (BR)

        -   BRは3.1 GA [＃233](https://github.com/pingcap/br/pull/233)より前のTiKVクラスターからのデータの復元をサポートしていません。

## 新機能 {#new-features}

-   TiDB

    -   `explain format = "dot"` [＃16125](https://github.com/pingcap/tidb/pull/16125)のコプロセッサータスク情報の表示をサポート
    -   `disable-error-stack`設定項目[＃16182](https://github.com/pingcap/tidb/pull/16182)使用してログの冗長スタック情報を削減する

-   配置Driver（PD）

    -   ホットリージョンのスケジュールを最適化する[＃2342](https://github.com/pingcap/pd/pull/2342)

-   TiFlash

    -   DeltaTreeエンジンの読み取りおよび書き込みワークロードに関連するメトリックレポートを追加します
    -   `fromUnixTime`と`dateFormat`押し下げ関数をサポート
    -   デフォルトでラフセットフィルタを無効にする

-   TiDB アンシブル

    -   TiFlashモニター[＃1253](https://github.com/pingcap/tidb-ansible/pull/1253) [＃1257](https://github.com/pingcap/tidb-ansible/pull/1257)を追加
    -   TiFlash [＃1262](https://github.com/pingcap/tidb-ansible/pull/1262) [＃1265](https://github.com/pingcap/tidb-ansible/pull/1265) [＃1271](https://github.com/pingcap/tidb-ansible/pull/1271)の設定パラメータを最適化する
    -   TiDB 起動スクリプト[＃1268](https://github.com/pingcap/tidb-ansible/pull/1268)を最適化する

## バグ修正 {#bug-fixes}

-   TiDB

    -   一部のシナリオでマージ結合操作によって発生するpanic問題を修正[＃15920](https://github.com/pingcap/tidb/pull/15920)
    -   選択性計算[＃16052](https://github.com/pingcap/tidb/pull/16052)で一部の式が繰り返しカウントされる問題を修正
    -   極端なケースで統計情報をロードするときに発生するpanic問題を修正[＃15710](https://github.com/pingcap/tidb/pull/15710)
    -   SQLクエリ[＃16015](https://github.com/pingcap/tidb/pull/16015)で同等の式を認識できない場合にエラーが返される問題を修正
    -   あるデータベースの`view`を別のデータベース[＃15867](https://github.com/pingcap/tidb/pull/15867)からクエリするとエラーが返される問題を修正しました
    -   `fast analyze` [＃16080](https://github.com/pingcap/tidb/pull/16080)を使用して列を処理するときに発生するpanic問題を修正しました
    -   `current_role`印刷結果[＃16084](https://github.com/pingcap/tidb/pull/16084)の誤った文字セットを修正
    -   MySQL接続ハンドシェイクエラー[＃15799](https://github.com/pingcap/tidb/pull/15799)のログを精査する
    -   監査プラグインのロード後にポートプローブによって発生するpanic問題を修正[＃16065](https://github.com/pingcap/tidb/pull/16065)
    -   `TypeNull`クラスが可変長型[＃15739](https://github.com/pingcap/tidb/pull/15739)と誤認されるために左結合の`sort`演算子がpanic問題を修正
    -   監視セッション再試行エラーの数が不正確になる問題を修正[＃16120](https://github.com/pingcap/tidb/pull/16120)
    -   `ALLOW_INVALID_DATES`モード[＃16171](https://github.com/pingcap/tidb/pull/16171)で`weekday`の間違った結果の問題を修正
    -   クラスタにTiFlashノード[＃15761](https://github.com/pingcap/tidb/pull/15761)がある場合にガベージコレクション（GC）が正常に動作しない可能性がある問題を修正しました
    -   ハッシュパーティションテーブル[＃16219](https://github.com/pingcap/tidb/pull/16219)を作成する際にユーザーが大きなパーティション数を設定すると、TiDBがメモリ（OOM）になる問題を修正しました。
    -   警告がエラーと誤認される問題を修正し、 `UNION`文が`SELECT`文と同じ動作になるようにします[＃16138](https://github.com/pingcap/tidb/pull/16138)
    -   `TopN` mocktikv [＃16200](https://github.com/pingcap/tidb/pull/16200)にプッシュダウンしたときの実行エラーを修正しました
    -   不要なオーバーヘッド`runtime.growslice` [＃16142](https://github.com/pingcap/tidb/pull/16142)を避けるために、初期の長さを`chunk.column.nullBitMap`に増やします。

-   TiKV

    -   レプリカ読み取り[＃7418](https://github.com/tikv/tikv/pull/7418) [＃7369](https://github.com/tikv/tikv/pull/7369)によって発生するpanic問題を修正
    -   復元プロセスで空のリージョン[＃7419](https://github.com/tikv/tikv/pull/7419)が作成される問題を修正しました
    -   繰り返しのロック解決要求が悲観的トランザクションの原子性を損なう可能性がある問題を修正[＃7389](https://github.com/tikv/tikv/pull/7389)

-   TiFlash

    -   TiDBからスキーマを複製する際の`rename table`操作の潜在的な問題を修正
    -   複数のデータパス構成で`rename table`操作によって発生するデータ損失の問題を修正しました
    -   一部のシナリオでTiFlash が誤ったstorage容量を報告する問題を修正しました
    -   リージョン結合が有効なときにTiFlashから読み取ることによって発生する可能性のある問題を修正しました

-   ツール

    -   TiDBBinlog

        -   TiFlash関連のDDLジョブがDrainer [＃948](https://github.com/pingcap/tidb-binlog/pull/948) [＃942](https://github.com/pingcap/tidb-binlog/pull/942)のレプリケーションを中断する可能性がある問題を修正しました。

    -   バックアップと復元 (BR)

        -   `checksum`操作が無効になっているにもかかわらず[＃223](https://github.com/pingcap/br/pull/223)が実行される問題を修正しました
        -   TiDBが`auto-random`または`alter-pk` [＃230](https://github.com/pingcap/br/pull/230) [＃231](https://github.com/pingcap/br/pull/231)を有効にすると増分バックアップが失敗する問題を修正
