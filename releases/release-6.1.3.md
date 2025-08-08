---
title: TiDB 6.1.3 Release Notes
summary: TiDB 6.1.3は2022年12月5日にリリースされました。このリリースには、互換性の変更、改善、バグ修正、そしてTiCDC、PD、TiKV、 TiFlash、バックアップとリストア、TiCDC、TiDBデータ移行などの各種ツールのアップデートが含まれています。主な変更点としては、TiCDCのデフォルト値の変更、PDのロック粒度の最適化、TiDB、PD、TiKV、 TiFlash、および各種ツールのバグ修正などが挙げられます。また、このリリースにはTiDBのGoコンパイラバージョンがgo1.18からgo1.19にアップグレードされ、安定性が向上しています。
---

# TiDB 6.1.3 リリースノート {#tidb-6-1-3-release-notes}

発売日：2022年12月5日

TiDB バージョン: 6.1.3

Quick access: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiCDC

        -   デフォルト値の[`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)を`table`から`none`に変更します。これにより、レプリケーションのレイテンシーが短縮され、OOM のリスクが軽減され、すべてのトランザクションではなく、少数のトランザクション (単一トランザクションのサイズが 1024 行を超える) のみが分割されるようになります[＃7505](https://github.com/pingcap/tiflow/issues/7505) [＃5231](https://github.com/pingcap/tiflow/issues/5231) @ [アズドンメン](https://github.com/asddongmen)

## Improvements {#improvements}

-   PD

    -   ロックの粒度を最適化してロック競合を減らし、高並行性[＃5586](https://github.com/tikv/pd/issues/5586) @ [rleungx](https://github.com/rleungx)でハートビートを処理する能力を向上させる

-   ツール

    -   TiCDC

        -   Enable transaction split and disable the safe mode of a changefeed in TiCDC by default to improve performance [＃7505](https://github.com/pingcap/tiflow/issues/7505) @[asddongmen](https://github.com/asddongmen)
        -   Kafka プロトコル エンコーダー[#7540](https://github.com/pingcap/tiflow/issues/7540) @ [＃7543](https://github.com/pingcap/tiflow/issues/7543) @ [3エースショーハンド](https://github.com/3AceShowHand) [＃7532](https://github.com/pingcap/tiflow/issues/7532)パフォーマンス[スドジ](https://github.com/sdojjy)向上

-   その他

    -   TiDBのGoコンパイラバージョンをgo1.18から[go1.19](https://go.dev/doc/go1.19)にアップグレードすることで、TiDBの安定性が向上します。具体的には、TiDBのメモリ使用量を一定のしきい値未満に保つためのGo環境変数[`GOMEMLIMIT`](https://pkg.go.dev/runtime@go1.19#hdr-Environment_Variables)導入されました。これにより、ほとんどのOOM問題を軽減できます。詳細については、 [`GOMEMLIMIT`を設定してOOMの問題を軽減する](/configure-memory-usage.md#mitigate-oom-issues-by-configuring-gomemlimit)ご覧ください。

## バグ修正 {#bug-fixes}

-   TiDB

    -   Fix the issue that the `grantor` field is missing in the `mysql.tables_priv` table [＃38293](https://github.com/pingcap/tidb/issues/38293) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   結合したテーブルの再配置 [＃38736](https://github.com/pingcap/tidb/issues/38736) @ [ウィノロス](https://github.com/winoros)によって誤ってプッシュダウンされた条件が破棄されたときに発生する間違ったクエリ結果の問題を修正しました。
    -   `get_lock()`で取得したロックが10分以上保持できない問題を修正[＃38706](https://github.com/pingcap/tidb/issues/38706) @ [接線](https://github.com/tangenta)
    -   自動インクリメント列がチェック制約[＃38894](https://github.com/pingcap/tidb/issues/38894) @ [ヤンケオ](https://github.com/YangKeao)で使用できない問題を修正しました
    -   gPRCログが間違ったファイルに出力される問題を修正[#38941](https://github.com/pingcap/tidb/issues/38941) @ [xhebox](https://github.com/xhebox)
    -   テーブルが切り捨てられたり削除されたりしても、テーブルのTiFlash同期ステータスが etcd から削除されない問題を修正[#37168](https://github.com/pingcap/tidb/issues/37168) @ [カルビンネオ](https://github.com/CalvinNeo)
    -   データソース名インジェクションによりデータファイルに無制限にアクセスできる問題を修正 (CVE-2022-3023) [＃38541](https://github.com/pingcap/tidb/issues/38541) @ [ランス6716](https://github.com/lance6716)
    -   関数`str_to_date` `NO_ZERO_DATE`モード[#39146](https://github.com/pingcap/tidb/issues/39146) @ [mengxin9014](https://github.com/mengxin9014)で間違った結果を返す問題を修正
    -   バックグラウンドでの統計収集タスクがpanic可能性がある問題を修正[＃35421](https://github.com/pingcap/tidb/issues/35421) @ [リーリンハイ](https://github.com/lilinghai)
    -   Fix the issue that in some scenarios the pessimistic lock is incorrectly added to the non-unique secondary index [＃36235](https://github.com/pingcap/tidb/issues/36235) @[ekexium](https://github.com/ekexium)

<!---->

-   PD

    -   不正確なストリームタイムアウトを修正し、リーダーのスイッチオーバーを高速化[＃5207](https://github.com/tikv/pd/issues/5207) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

<!---->

-   TiKV

    -   Fix abnormal Region competition caused by expired lease during snapshot acquisition [＃13553](https://github.com/tikv/tikv/issues/13553) @[スペードA-タン](https://github.com/SpadeA-Tang)

-   TiFlash

    -   Fix the issue that logical operators return wrong results when the argument type is `UInt8` [＃6127](https://github.com/pingcap/tiflash/issues/6127) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   `CAST(value AS DATETIME)`間違ったデータ入力によりTiFlash sys CPU [#5097](https://github.com/pingcap/tiflash/issues/5097) @ [xzhangxian1008](https://github.com/xzhangxian1008)の負荷が高くなる問題を修正
    -   書き込み圧力が高すぎるとデルタレイヤー[＃6361](https://github.com/pingcap/tiflash/issues/6361) @ [リデズ](https://github.com/lidezhu)に過剰な列ファイルが生成される可能性がある問題を修正しました。
    -   TiFlash [＃6159](https://github.com/pingcap/tiflash/issues/6159) @ [リデズ](https://github.com/lidezhu)を再起動した後、デルタレイヤーの列ファイルを圧縮できない問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   データベースまたはテーブル[#39150](https://github.com/pingcap/tidb/issues/39150) @ [MoCuishle28](https://github.com/MoCuishle28)照合に古いフレームワークを使用すると復元タスクが失敗する問題を修正しました

    -   TiCDC

        -   最初にDDLステートメントを実行し、次に変更フィード[＃7682](https://github.com/pingcap/tiflow/issues/7682) @ [アズドンメン](https://github.com/asddongmen)を一時停止して再開するシナリオで発生したデータ損失を修正しました
        -   Fix the issue that the sink component gets stuck if the downstream network is unavailable [#7706](https://github.com/pingcap/tiflow/issues/7706) @[ヒック](https://github.com/hicqu)

    -   TiDB データ移行 (DM)

        -   `collation_compatible` `"strict"`に設定すると、DM が重複した照合順序[#6832](https://github.com/pingcap/tiflow/issues/6832) @ [ランス6716](https://github.com/lance6716)を持つ SQL を生成する可能性がある問題を修正しました。
        -   DMタスクが`Unknown placement policy`エラー[＃7493](https://github.com/pingcap/tiflow/issues/7493) @ [ランス6716](https://github.com/lance6716)で停止する可能性がある問題を修正
        -   場合によってはリレーログがアップストリームから再度取得される可能性がある問題を修正[＃7525](https://github.com/pingcap/tiflow/issues/7525) @ [liumengya94](https://github.com/liumengya94)
        -   既存のワーカーが終了する前に新しい DM ワーカーがスケジュールされると、データが複数回複製される問題を修正しました[#7658](https://github.com/pingcap/tiflow/issues/7658) @ [GMHDBJD](https://github.com/GMHDBJD)
