---
title: TiDB 6.1.3 Release Notes
---

# TiDB 6.1.3 リリースノート {#tidb-6-1-3-release-notes}

発売日：2022年12月5日

TiDB バージョン: 6.1.3

クイック アクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [インストール パッケージ](https://www.pingcap.com/download/?version=v6.1.3#version-list)

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiCDC

        -   デフォルト値の[`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb) `table`から`none`に変更します。これにより、レプリケーションのレイテンシーが短縮され、OOM のリスクが軽減され、すべてのトランザクションではなく少数のトランザクション (1 つのトランザクションのサイズが 1024 行を超える) のみが分割されるようになります[#7505](https://github.com/pingcap/tiflow/issues/7505) [#5231](https://github.com/pingcap/tiflow/issues/5231) @ [アスドンメン](https://github.com/asddongmen)

## 改良点 {#improvements}

-   PD

    -   ロックの粒度を最適化してロックの競合を減らし、ハートビートを高い並行性で処理する能力を向上させます[#5586](https://github.com/tikv/pd/issues/5586) @ [ルルング](https://github.com/rleungx)

-   ツール

    -   TiCDC

        -   パフォーマンスを向上させるために、デフォルトでトランザクション分割を有効にし、TiCDC の変更フィードのセーフ モードを無効にします[#7505](https://github.com/pingcap/tiflow/issues/7505) @ [アスドンメン](https://github.com/asddongmen)
        -   Kafka プロトコル エンコーダー[#7540](https://github.com/pingcap/tiflow/issues/7540) 、 [#7532](https://github.com/pingcap/tiflow/issues/7532) 、 [#7543](https://github.com/pingcap/tiflow/issues/7543) @ [スドジ](https://github.com/sdojjy) @ [3AceShowHand](https://github.com/3AceShowHand)のパフォーマンスを向上させる

-   その他

    -   TiDB の Go コンパイラ バージョンを go1.18 から[go1.19](https://go.dev/doc/go1.19)にアップグレードすると、TiDB の安定性が向上します。具体的には、Go 環境変数[`GOMEMLIMIT`](https://pkg.go.dev/runtime@go1.19#hdr-Environment_Variables)が導入され、TiDB のメモリ使用量を特定のしきい値未満に保ちます。これにより、ほとんどの OOM の問題を軽減できます。詳細については、 [`GOMEMLIMIT`を構成して OOM の問題を軽減する](/configure-memory-usage.md#mitigate-oom-issues-by-configuring-gomemlimit)を参照してください。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `mysql.tables_priv`テーブル[#38293](https://github.com/pingcap/tidb/issues/38293) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)で`grantor`フィールドが欠落している問題を修正
    -   結合したテーブルの再配置 [#38736](https://github.com/pingcap/tidb/issues/38736) @ [ウィノロス](https://github.com/winoros)で誤ってプッシュダウンされた条件が破棄されると、間違ったクエリ結果が発生する問題を修正
    -   `get_lock()`が取得したロックが 10 分以上保持できない問題を修正[#38706](https://github.com/pingcap/tidb/issues/38706) @ [接線](https://github.com/tangenta)
    -   自動インクリメント列がチェック制約[#38894](https://github.com/pingcap/tidb/issues/38894) @ [ヤンケアオ](https://github.com/YangKeao)で使用できない問題を修正
    -   gPRC ログが間違ったファイルに出力される問題を修正[#38941](https://github.com/pingcap/tidb/issues/38941) @ [xhebox](https://github.com/xhebox)
    -   テーブルがトランケートまたはドロップされた場合、テーブルのTiFlash同期ステータスが etcd から削除されない問題を修正します[#37168](https://github.com/pingcap/tidb/issues/37168) @ [カルバンネオ](https://github.com/CalvinNeo)
    -   データソース名インジェクションにより、データファイルに無制限にアクセスできる問題を修正 (CVE-2022-3023) [#38541](https://github.com/pingcap/tidb/issues/38541) @ [ランス6716](https://github.com/lance6716)
    -   関数`str_to_date`が`NO_ZERO_DATE` SQL モード[#39146](https://github.com/pingcap/tidb/issues/39146) @ [mengxin9014](https://github.com/mengxin9014)で間違った結果を返す問題を修正
    -   バックグラウンドでの統計収集タスクがpanic[#35421](https://github.com/pingcap/tidb/issues/35421) @ [リリンハイ](https://github.com/lilinghai)になる可能性がある問題を修正します。
    -   一部のシナリオで悲観的ロックが一意でないセカンダリ インデックス[#36235](https://github.com/pingcap/tidb/issues/36235) @ [エキキシウム](https://github.com/ekexium)に誤って追加される問題を修正します。

<!---->

-   PD

    -   不正確なストリーム タイムアウトを修正し、リーダーの切り替えを高速化します[#5207](https://github.com/tikv/pd/issues/5207) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

<!---->

-   TiKV

    -   スナップショット取得[#13553](https://github.com/tikv/tikv/issues/13553) @ [スペード・ア・タン](https://github.com/SpadeA-Tang)中のリース期限切れによる異常なリージョン競合を修正

-   TiFlash

    -   引数の型が`UInt8` [#6127](https://github.com/pingcap/tiflash/issues/6127) @ [xzhangxian1008](https://github.com/xzhangxian1008)のときに論理演算子が間違った結果を返す問題を修正
    -   `CAST(value AS DATETIME)`の間違ったデータ入力が原因でTiFlash sys CPU [#5097](https://github.com/pingcap/tiflash/issues/5097) @ [xzhangxian1008](https://github.com/xzhangxian1008)が高くなる問題を修正
    -   書き込み圧力が高いと、デルタレイヤー[#6361](https://github.com/pingcap/tiflash/issues/6361) @ [リデジュ](https://github.com/lidezhu)で列ファイルが過剰に生成される可能性があるという問題を修正します。
    -   TiFlash [#6159](https://github.com/pingcap/tiflash/issues/6159) @ [リデジュ](https://github.com/lidezhu)の再起動後、デルタレイヤーの列ファイルを圧縮できない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   データベースまたはテーブル[#39150](https://github.com/pingcap/tidb/issues/39150) @ [MoCuishle28](https://github.com/MoCuishle28)の照合に古いフレームワークを使用すると、復元タスクが失敗する問題を修正します

    -   TiCDC

        -   最初に DDL ステートメントを実行し、次に changefeed [#7682](https://github.com/pingcap/tiflow/issues/7682) @ [アスドンメン](https://github.com/asddongmen)を一時停止して再開するシナリオで発生したデータ損失を修正
        -   ダウンストリーム ネットワークが使用できない場合にシンクコンポーネントがスタックする問題を修正します[#7706](https://github.com/pingcap/tiflow/issues/7706) @ [ヒック](https://github.com/hicqu)

    -   TiDB データ移行 (DM)

        -   `collation_compatible`が`"strict"`に設定されている場合、DM が重複した照合順序[#6832](https://github.com/pingcap/tiflow/issues/6832) @ [ランス6716](https://github.com/lance6716)で SQL を生成する可能性があるという問題を修正します。
        -   DM タスクが`Unknown placement policy`エラー[#7493](https://github.com/pingcap/tiflow/issues/7493) @ [ランス6716](https://github.com/lance6716)で停止することがある問題を修正
        -   場合によっては、リレー ログが上流から再度プルされる可能性がある問題を修正します[#7525](https://github.com/pingcap/tiflow/issues/7525) @ [リウメンギャ94](https://github.com/liumengya94)
        -   既存のワーカーが[#7658](https://github.com/pingcap/tiflow/issues/7658) @ [GMHDBJD](https://github.com/GMHDBJD)を終了する前に新しい DM ワーカーがスケジュールされると、データが複数回レプリケートされる問題を修正します
