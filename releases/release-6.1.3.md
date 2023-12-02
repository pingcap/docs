---
title: TiDB 6.1.3 Release Notes
---

# TiDB 6.1.3 リリースノート {#tidb-6-1-3-release-notes}

発売日：2022年12月5日

TiDB バージョン: 6.1.3

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.1.3#version-list)

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiCDC

        -   デフォルト値[`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb) `table`から`none`に変更します。これにより、レプリケーションのレイテンシーが短縮され、OOM リスクが軽減され、すべてのトランザクションではなく少数のトランザクション (単一トランザクションのサイズが 1024 行を超える) のみが分割されるようになります[#7505](https://github.com/pingcap/tiflow/issues/7505) [#5231](https://github.com/pingcap/tiflow/issues/5231) @ [東門](https://github.com/asddongmen)

## 改善点 {#improvements}

-   PD

    -   ロックの粒度を最適化してロックの競合を軽減し、高同時実行[#5586](https://github.com/tikv/pd/issues/5586) @ [ルルンクス](https://github.com/rleungx)でのハートビートの処理能力を向上させます。

-   ツール

    -   TiCDC

        -   パフォーマンスを向上させるために、デフォルトで TiCDC のトランザクション分割を有効にし、チェンジフィードのセーフ モードを無効にします[#7505](https://github.com/pingcap/tiflow/issues/7505) @ [東門](https://github.com/asddongmen)
        -   Kafka プロトコル エンコーダ[#7540](https://github.com/pingcap/tiflow/issues/7540) 、 [#7532](https://github.com/pingcap/tiflow/issues/7532) 、 [#7543](https://github.com/pingcap/tiflow/issues/7543) @ [スドジ](https://github.com/sdojjy) @ [3エースショーハンド](https://github.com/3AceShowHand)のパフォーマンスを向上させます。

-   その他

    -   TiDB の Go コンパイラー バージョンを go1.18 から[go1.19](https://go.dev/doc/go1.19)にアップグレードすると、TiDB の安定性が向上します。具体的には、TiDB のメモリ使用量を一定のしきい値以下に保つために、Go 環境変数[`GOMEMLIMIT`](https://pkg.go.dev/runtime@go1.19#hdr-Environment_Variables)が導入されています。これは、ほとんどの OOM 問題を軽減するのに役立ちます。詳細については、 [`GOMEMLIMIT`を構成することで OOM の問題を軽減する](/configure-memory-usage.md#mitigate-oom-issues-by-configuring-gomemlimit)を参照してください。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `mysql.tables_priv`テーブル[#38293](https://github.com/pingcap/tidb/issues/38293) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)で`grantor`フィールドが欠落している問題を修正
    -   結合したテーブルの再配置 [#38736](https://github.com/pingcap/tidb/issues/38736) @ [ウィノロス](https://github.com/winoros)で誤ってプッシュダウンされた条件が破棄された場合に、間違ったクエリ結果が発生する問題を修正しました。
    -   `get_lock()`で取得したロックが 10 分以上保持できない問題を修正[#38706](https://github.com/pingcap/tidb/issues/38706) @ [タンジェンタ](https://github.com/tangenta)
    -   検査制約[#38894](https://github.com/pingcap/tidb/issues/38894) @ [ヤンケオ](https://github.com/YangKeao)で自動インクリメントカラムが使用できない問題を修正
    -   gPRCログが間違ったファイルに出力される問題を修正[#38941](https://github.com/pingcap/tidb/issues/38941) @ [ゼボックス](https://github.com/xhebox)
    -   テーブルが切り捨てられるか削除されると、テーブルのTiFlash同期ステータスが etcd から削除されない問題を修正します[#37168](https://github.com/pingcap/tidb/issues/37168) @ [カルビンネオ](https://github.com/CalvinNeo)
    -   データ ソース名インジェクションを介してデータ ファイルに無制限にアクセスできる問題を修正します (CVE-2022-3023) [#38541](https://github.com/pingcap/tidb/issues/38541) @ [ランス6716](https://github.com/lance6716)
    -   `NO_ZERO_DATE` SQL モード[#39146](https://github.com/pingcap/tidb/issues/39146) @ [孟新9014](https://github.com/mengxin9014)で関数`str_to_date`間違った結果を返す問題を修正
    -   バックグラウンドでの統計収集タスクがpanic[#35421](https://github.com/pingcap/tidb/issues/35421) @ [リリンハイ](https://github.com/lilinghai)になる可能性がある問題を修正
    -   一部のシナリオで、悲観的ロックが非一意のセカンダリ インデックス[#36235](https://github.com/pingcap/tidb/issues/36235) @ [エキシウム](https://github.com/ekexium)に誤って追加される問題を修正します。

<!---->

-   PD

    -   不正確なストリーム タイムアウトを修正し、リーダーの切り替え[#5207](https://github.com/tikv/pd/issues/5207) @ [キャビンフィーバーB](https://github.com/CabinfeverB)を高速化します。

<!---->

-   TiKV

    -   スナップショット取得中のリース期限切れによって引き起こされる異常なリージョン競合を修正[#13553](https://github.com/tikv/tikv/issues/13553) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)

-   TiFlash

    -   引数の型が`UInt8` [#6127](https://github.com/pingcap/tiflash/issues/6127) @ [xzhangxian1008](https://github.com/xzhangxian1008)の場合、論理演算子が間違った結果を返す問題を修正
    -   `CAST(value AS DATETIME)`の間違ったデータ入力によりTiFlash sys CPU [#5097](https://github.com/pingcap/tiflash/issues/5097) @ [xzhangxian1008](https://github.com/xzhangxian1008)のパフォーマンスが高くなる問題を修正
    -   書き込み圧力が高いと、デルタレイヤー[#6361](https://github.com/pingcap/tiflash/issues/6361) @ [リデズ](https://github.com/lidezhu)で多すぎる列ファイルが生成される可能性がある問題を修正します。
    -   TiFlash [#6159](https://github.com/pingcap/tiflash/issues/6159) @ [リデズ](https://github.com/lidezhu)の再起動後にデルタレイヤーのカラムファイルが圧縮できない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   データベースまたはテーブル[#39150](https://github.com/pingcap/tidb/issues/39150) @ [モクイシュル28](https://github.com/MoCuishle28)の照合順序に古いフレームワークを使用すると、復元タスクが失敗する問題を修正します。

    -   TiCDC

        -   最初に DDL ステートメントを実行し、次に変更フィード[#7682](https://github.com/pingcap/tiflow/issues/7682) @ [東門](https://github.com/asddongmen)を一時停止して再開するシナリオで発生したデータ損失を修正しました。
        -   ダウンストリーム ネットワークが利用できない場合にシンクコンポーネントがスタックする問題を修正[#7706](https://github.com/pingcap/tiflow/issues/7706) @ [ひっくり返る](https://github.com/hicqu)

    -   TiDB データ移行 (DM)

        -   `collation_compatible`を`"strict"`に設定すると、DM が重複した照合順序[#6832](https://github.com/pingcap/tiflow/issues/6832) @ [ランス6716](https://github.com/lance6716)を含む SQL を生成する可能性がある問題を修正します。
        -   DM タスクが`Unknown placement policy`エラー[#7493](https://github.com/pingcap/tiflow/issues/7493) @ [ランス6716](https://github.com/lance6716)で停止することがある問題を修正
        -   場合によってはリレーログが上流から再度取得される場合がある問題を修正[#7525](https://github.com/pingcap/tiflow/issues/7525) @ [リウメンギャ94](https://github.com/liumengya94)
        -   既存のワーカーが終了する前に新しい DM ワーカーがスケジュールされている場合、データが複数回レプリケートされる問題を修正します[#7658](https://github.com/pingcap/tiflow/issues/7658) @ [GMHDBJD](https://github.com/GMHDBJD)
