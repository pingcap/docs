---
title: TiDB 6.1.3 Release Notes
summary: TiDB 6.1.3 は 2022 年 12 月 5 日にリリースされました。このリリースには、互換性の変更、改善、バグ修正、および TiCDC、PD、TiKV、 TiFlash、バックアップと復元、TiCDC、TiDB データ移行などのさまざまなツールの更新が含まれています。注目すべき変更点としては、TiCDC のデフォルト値の変更、PD のロック粒度の最適化、TiDB、PD、TiKV、 TiFlash、およびさまざまなツールのバグ修正などがあります。このリリースには、TiDB の Go コンパイラ バージョンが go1.18 から go1.19 にアップグレードされ、安定性が向上していることも含まれています。
---

# TiDB 6.1.3 リリースノート {#tidb-6-1-3-release-notes}

発売日: 2022年12月5日

TiDB バージョン: 6.1.3

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   ティCDC

        -   デフォルト値[`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)を`table`から`none`に変更します。これにより、レプリケーションのレイテンシーが短縮され、OOM のリスクが軽減され、すべてのトランザクションではなく、少数のトランザクション (1 つのトランザクションのサイズが 1024 行を超える) のみが分割されるようになります[＃7505](https://github.com/pingcap/tiflow/issues/7505) [＃5231](https://github.com/pingcap/tiflow/issues/5231) @ [アズドンメン](https://github.com/asddongmen)

## 改善点 {#improvements}

-   PD

    -   ロックの粒度を最適化してロック競合を減らし、高同時実行でのハートビート処理能力を向上させる[＃5586](https://github.com/tikv/pd/issues/5586) @ [rleungx](https://github.com/rleungx)

-   ツール

    -   ティCDC

        -   パフォーマンスを向上させるために、TiCDC でトランザクション分割を有効にし、変更フィードのセーフ モードをデフォルトで無効にします[＃7505](https://github.com/pingcap/tiflow/issues/7505) @ [アズドンメン](https://github.com/asddongmen)
        -   Kafka プロトコル エンコーダー[＃7540](https://github.com/pingcap/tiflow/issues/7540) [スドジ](https://github.com/sdojjy) [＃7543](https://github.com/pingcap/tiflow/issues/7543) [3エースショーハンド](https://github.com/3AceShowHand)のパフォーマンス[＃7532](https://github.com/pingcap/tiflow/issues/7532)向上

-   その他

    -   TiDB の Go コンパイラー バージョンを go1.18 から[1.19 へ](https://go.dev/doc/go1.19)にアップグレードすると、TiDB の安定性が向上します。具体的には、TiDB のメモリ使用量を一定のしきい値未満に保つために、Go 環境変数[`GOMEMLIMIT`](https://pkg.go.dev/runtime@go1.19#hdr-Environment_Variables)が導入されました。これにより、ほとんどの OOM の問題が軽減されます。詳細については、 [`GOMEMLIMIT`を設定してOOMの問題を軽減する](/configure-memory-usage.md#mitigate-oom-issues-by-configuring-gomemlimit)参照してください。

## バグ修正 {#bug-fixes}

-   ティビ

    -   `mysql.tables_priv`テーブル[＃38293](https://github.com/pingcap/tidb/issues/38293) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)で`grantor`フィールドが欠落している問題を修正
    -   結合したテーブルの再配置 [＃38736](https://github.com/pingcap/tidb/issues/38736) @ [ウィノロス](https://github.com/winoros)によって誤ってプッシュダウンされた条件が破棄されたときに発生する間違ったクエリ結果の問題を修正しました。
    -   `get_lock()`で取得したロックが 10 分以上保持できない問題を修正[＃38706](https://github.com/pingcap/tidb/issues/38706) @ [タンジェンタ](https://github.com/tangenta)
    -   自動インクリメント列がチェック制約[＃38894](https://github.com/pingcap/tidb/issues/38894) @ [ヤンケオ](https://github.com/YangKeao)で使用できない問題を修正
    -   gPRCログが間違ったファイルに出力される問題を修正[＃38941](https://github.com/pingcap/tidb/issues/38941) @ [xhebox](https://github.com/xhebox)
    -   テーブルが切り捨てられたり削除されたりしても、テーブルのTiFlash同期ステータスが etcd から削除されない問題を修正[＃37168](https://github.com/pingcap/tidb/issues/37168) @ [カルビンネオ](https://github.com/CalvinNeo)
    -   データソース名インジェクションによりデータファイルに無制限にアクセスできる問題を修正 (CVE-2022-3023) [＃38541](https://github.com/pingcap/tidb/issues/38541) @ [ランス6716](https://github.com/lance6716)
    -   関数`str_to_date`が`NO_ZERO_DATE`モード[＃39146](https://github.com/pingcap/tidb/issues/39146) @ [メンシン9014](https://github.com/mengxin9014)で間違った結果を返す問題を修正
    -   バックグラウンドでの統計収集タスクがpanicになる可能性がある問題を修正[＃35421](https://github.com/pingcap/tidb/issues/35421) @ [リリンハイ](https://github.com/lilinghai)
    -   いくつかのシナリオで、悲観的ロックが非一意のセカンダリインデックス[＃36235](https://github.com/pingcap/tidb/issues/36235) @ [エキシウム](https://github.com/ekexium)に誤って追加される問題を修正しました。

<!---->

-   PD

    -   不正確なストリームタイムアウトを修正し、リーダーの切り替えを高速化[＃5207](https://github.com/tikv/pd/issues/5207) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

<!---->

-   ティクヴ

    -   スナップショット取得中に期限切れのリースが原因で発生する異常なリージョン競合を修正[＃13553](https://github.com/tikv/tikv/issues/13553) @ [スペードA-タン](https://github.com/SpadeA-Tang)

-   TiFlash

    -   引数の型が`UInt8` [＃6127](https://github.com/pingcap/tiflash/issues/6127) @ [翻訳者](https://github.com/xzhangxian1008)の場合に論理演算子が間違った結果を返す問題を修正しました
    -   `CAST(value AS DATETIME)`の誤ったデータ入力によりTiFlash sys CPU [＃5097](https://github.com/pingcap/tiflash/issues/5097) @ [翻訳者](https://github.com/xzhangxian1008)の負荷が高くなる問題を修正
    -   書き込み圧力が高すぎるとデルタレイヤー[＃6361](https://github.com/pingcap/tiflash/issues/6361) @ [リデズ](https://github.com/lidezhu)に列ファイルが大量に生成される問題を修正しました。
    -   TiFlash [＃6159](https://github.com/pingcap/tiflash/issues/6159) @ [リデズ](https://github.com/lidezhu)を再起動した後、デルタレイヤーの列ファイルを圧縮できない問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   データベースまたはテーブル[＃39150](https://github.com/pingcap/tidb/issues/39150) @ [モクイシュル28](https://github.com/MoCuishle28)の照合に古いフレームワークを使用すると復元タスクが失敗する問題を修正しました

    -   ティCDC

        -   最初に DDL ステートメントを実行し、次に変更フィード[＃7682](https://github.com/pingcap/tiflow/issues/7682) @ [アズドンメン](https://github.com/asddongmen)を一時停止して再開するシナリオで発生したデータ損失を修正しました。
        -   ダウンストリームネットワークが利用できない場合にシンクコンポーネントが停止する問題を修正[＃7706](https://github.com/pingcap/tiflow/issues/7706) @ [ヒック](https://github.com/hicqu)

    -   TiDB データ移行 (DM)

        -   `collation_compatible` `"strict"`に設定すると、DM が重複した照合順序[＃6832](https://github.com/pingcap/tiflow/issues/6832) @ [ランス6716](https://github.com/lance6716)を持つ SQL を生成する可能性がある問題を修正しました。
        -   DMタスクが`Unknown placement policy`エラー[＃7493](https://github.com/pingcap/tiflow/issues/7493) @ [ランス6716](https://github.com/lance6716)で停止する可能性がある問題を修正
        -   場合によってはリレーログがアップストリームから再度プルされる可能性がある問題を修正[＃7525](https://github.com/pingcap/tiflow/issues/7525) @ [りゅうめんぎゃ](https://github.com/liumengya94)
        -   既存のワーカーが終了する前に新しい DM ワーカーがスケジュールされると、データが複数回複製される問題を修正[＃7658](https://github.com/pingcap/tiflow/issues/7658) @ [GMHDBJD](https://github.com/GMHDBJD)
