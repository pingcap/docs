---
title: TiDB 6.1.3 Release Notes
---

# TiDB 6.1.3 リリースノート {#tidb-6-1-3-release-notes}

発売日：2022年12月5日

TiDB バージョン: 6.1.3

クイックアクセス: [<a href="https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb">クイックスタート</a>](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [<a href="https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup">本番展開</a>](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [<a href="https://www.pingcap.com/download/?version=v6.1.3#version-list">インストールパッケージ</a>](https://www.pingcap.com/download/?version=v6.1.3#version-list)

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiCDC

        -   デフォルト値[<a href="/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb">`transaction-atomicity`</a>](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb) `table`から`none`に変更します。これにより、レプリケーションのレイテンシーが短縮され、OOM リスクが軽減され、すべてのトランザクションではなく少数のトランザクション (単一トランザクションのサイズが 1024 行を超える) のみが分割されるようになります[<a href="https://github.com/pingcap/tiflow/issues/7505">#7505</a>](https://github.com/pingcap/tiflow/issues/7505) [<a href="https://github.com/pingcap/tiflow/issues/5231">#5231</a>](https://github.com/pingcap/tiflow/issues/5231) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)

## 改善点 {#improvements}

-   PD

    -   ロックの粒度を最適化してロックの競合を軽減し、高同時実行[<a href="https://github.com/tikv/pd/issues/5586">#5586</a>](https://github.com/tikv/pd/issues/5586) @ [<a href="https://github.com/rleungx">ルルンクス</a>](https://github.com/rleungx)でのハートビートの処理能力を向上させます。

-   ツール

    -   TiCDC

        -   パフォーマンスを向上させるために、デフォルトで TiCDC のトランザクション分割を有効にし、チェンジフィードのセーフ モードを無効にします[<a href="https://github.com/pingcap/tiflow/issues/7505">#7505</a>](https://github.com/pingcap/tiflow/issues/7505) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)
        -   Kafka プロトコル エンコーダ[<a href="https://github.com/pingcap/tiflow/issues/7540">#7540</a>](https://github.com/pingcap/tiflow/issues/7540) 、 [<a href="https://github.com/pingcap/tiflow/issues/7532">#7532</a>](https://github.com/pingcap/tiflow/issues/7532) 、 [<a href="https://github.com/pingcap/tiflow/issues/7543">#7543</a>](https://github.com/pingcap/tiflow/issues/7543) @ [<a href="https://github.com/sdojjy">スドジ</a>](https://github.com/sdojjy) @ [<a href="https://github.com/3AceShowHand">3エースショーハンド</a>](https://github.com/3AceShowHand)のパフォーマンスを向上させます。

-   その他

    -   TiDB の Go コンパイラー バージョンを go1.18 から[<a href="https://go.dev/doc/go1.19">go1.19</a>](https://go.dev/doc/go1.19)にアップグレードすると、TiDB の安定性が向上します。具体的には、TiDB のメモリ使用量を一定のしきい値以下に保つために、Go 環境変数[<a href="https://pkg.go.dev/runtime@go1.19#hdr-Environment_Variables">`GOMEMLIMIT`</a>](https://pkg.go.dev/runtime@go1.19#hdr-Environment_Variables)が導入されています。これは、ほとんどの OOM 問題を軽減するのに役立ちます。詳細については、 [<a href="/configure-memory-usage.md#mitigate-oom-issues-by-configuring-gomemlimit">`GOMEMLIMIT`を構成することで OOM の問題を軽減する</a>](/configure-memory-usage.md#mitigate-oom-issues-by-configuring-gomemlimit)を参照してください。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `mysql.tables_priv`テーブル[<a href="https://github.com/pingcap/tidb/issues/38293">#38293</a>](https://github.com/pingcap/tidb/issues/38293) @ [<a href="https://github.com/CbcWestwolf">Cbcウェストウルフ</a>](https://github.com/CbcWestwolf)で`grantor`フィールドが欠落している問題を修正
    -   結合したテーブルの再配置 [<a href="https://github.com/pingcap/tidb/issues/38736">#38736</a>](https://github.com/pingcap/tidb/issues/38736) @ [<a href="https://github.com/winoros">ウィノロス</a>](https://github.com/winoros)で誤ってプッシュダウンされた条件が破棄された場合に、間違ったクエリ結果が発生する問題を修正しました。
    -   `get_lock()`で取得したロックが 10 分以上保持できない問題を修正[<a href="https://github.com/pingcap/tidb/issues/38706">#38706</a>](https://github.com/pingcap/tidb/issues/38706) @ [<a href="https://github.com/tangenta">タンジェンタ</a>](https://github.com/tangenta)
    -   検査制約[<a href="https://github.com/pingcap/tidb/issues/38894">#38894</a>](https://github.com/pingcap/tidb/issues/38894) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)で自動インクリメントカラムが使用できない問題を修正
    -   gPRCログが間違ったファイルに出力される問題を修正[<a href="https://github.com/pingcap/tidb/issues/38941">#38941</a>](https://github.com/pingcap/tidb/issues/38941) @ [<a href="https://github.com/xhebox">ゼボックス</a>](https://github.com/xhebox)
    -   テーブルが切り捨てられるか削除されると、テーブルのTiFlash同期ステータスが etcd から削除されない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/37168">#37168</a>](https://github.com/pingcap/tidb/issues/37168) @ [<a href="https://github.com/CalvinNeo">カルビンネオ</a>](https://github.com/CalvinNeo)
    -   データ ソース名インジェクションを介してデータ ファイルに無制限にアクセスできる問題を修正します (CVE-2022-3023) [<a href="https://github.com/pingcap/tidb/issues/38541">#38541</a>](https://github.com/pingcap/tidb/issues/38541) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)
    -   `NO_ZERO_DATE` SQL モード[<a href="https://github.com/pingcap/tidb/issues/39146">#39146</a>](https://github.com/pingcap/tidb/issues/39146) @ [<a href="https://github.com/mengxin9014">孟新9014</a>](https://github.com/mengxin9014)で関数`str_to_date`間違った結果を返す問題を修正
    -   バックグラウンドでの統計収集タスクがpanic[<a href="https://github.com/pingcap/tidb/issues/35421">#35421</a>](https://github.com/pingcap/tidb/issues/35421) @ [<a href="https://github.com/lilinghai">リリンハイ</a>](https://github.com/lilinghai)になる可能性がある問題を修正
    -   一部のシナリオで、悲観的ロックが非一意のセカンダリ インデックス[<a href="https://github.com/pingcap/tidb/issues/36235">#36235</a>](https://github.com/pingcap/tidb/issues/36235) @ [<a href="https://github.com/ekexium">エキシウム</a>](https://github.com/ekexium)に誤って追加される問題を修正します。

<!---->

-   PD

    -   不正確なストリーム タイムアウトを修正し、リーダーの切り替え[<a href="https://github.com/tikv/pd/issues/5207">#5207</a>](https://github.com/tikv/pd/issues/5207) @ [<a href="https://github.com/CabinfeverB">キャビンフィーバーB</a>](https://github.com/CabinfeverB)を高速化します。

<!---->

-   TiKV

    -   スナップショット取得中のリース期限切れによって引き起こされる異常なリージョン競合を修正[<a href="https://github.com/tikv/tikv/issues/13553">#13553</a>](https://github.com/tikv/tikv/issues/13553) @ [<a href="https://github.com/SpadeA-Tang">SpadeA-Tang</a>](https://github.com/SpadeA-Tang)

-   TiFlash

    -   引数の型が`UInt8` [<a href="https://github.com/pingcap/tiflash/issues/6127">#6127</a>](https://github.com/pingcap/tiflash/issues/6127) @ [<a href="https://github.com/xzhangxian1008">xzhangxian1008</a>](https://github.com/xzhangxian1008)の場合、論理演算子が間違った結果を返す問題を修正
    -   `CAST(value AS DATETIME)`の間違ったデータ入力によりTiFlash sys CPU [<a href="https://github.com/pingcap/tiflash/issues/5097">#5097</a>](https://github.com/pingcap/tiflash/issues/5097) @ [<a href="https://github.com/xzhangxian1008">xzhangxian1008</a>](https://github.com/xzhangxian1008)のパフォーマンスが高くなる問題を修正
    -   書き込み圧力が高いと、デルタレイヤー[<a href="https://github.com/pingcap/tiflash/issues/6361">#6361</a>](https://github.com/pingcap/tiflash/issues/6361) @ [<a href="https://github.com/lidezhu">リデジュ</a>](https://github.com/lidezhu)で多すぎる列ファイルが生成される可能性がある問題を修正します。
    -   TiFlash [<a href="https://github.com/pingcap/tiflash/issues/6159">#6159</a>](https://github.com/pingcap/tiflash/issues/6159) @ [<a href="https://github.com/lidezhu">リデジュ</a>](https://github.com/lidezhu)の再起動後にデルタレイヤーのカラムファイルが圧縮できない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   データベースまたはテーブル[<a href="https://github.com/pingcap/tidb/issues/39150">#39150</a>](https://github.com/pingcap/tidb/issues/39150) @ [<a href="https://github.com/MoCuishle28">モクイシュル28</a>](https://github.com/MoCuishle28)の照合順序に古いフレームワークを使用すると、復元タスクが失敗する問題を修正します。

    -   TiCDC

        -   最初に DDL ステートメントを実行し、次に変更フィード[<a href="https://github.com/pingcap/tiflow/issues/7682">#7682</a>](https://github.com/pingcap/tiflow/issues/7682) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)を一時停止して再開するシナリオで発生したデータ損失を修正しました。
        -   ダウンストリーム ネットワークが利用できない場合にシンクコンポーネントがスタックする問題を修正[<a href="https://github.com/pingcap/tiflow/issues/7706">#7706</a>](https://github.com/pingcap/tiflow/issues/7706) @ [<a href="https://github.com/hicqu">ひっくり返る</a>](https://github.com/hicqu)

    -   TiDB データ移行 (DM)

        -   `collation_compatible`を`"strict"`に設定すると、DM が重複した照合順序[<a href="https://github.com/pingcap/tiflow/issues/6832">#6832</a>](https://github.com/pingcap/tiflow/issues/6832) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)を含む SQL を生成する可能性がある問題を修正します。
        -   DM タスクが`Unknown placement policy`エラー[<a href="https://github.com/pingcap/tiflow/issues/7493">#7493</a>](https://github.com/pingcap/tiflow/issues/7493) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)で停止することがある問題を修正
        -   場合によってはリレーログが上流から再度取得される場合がある問題を修正[<a href="https://github.com/pingcap/tiflow/issues/7525">#7525</a>](https://github.com/pingcap/tiflow/issues/7525) @ [<a href="https://github.com/liumengya94">リウメンギャ94</a>](https://github.com/liumengya94)
        -   既存のワーカーが終了する前に新しい DM ワーカーがスケジュールされている場合、データが複数回レプリケートされる問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/7658">#7658</a>](https://github.com/pingcap/tiflow/issues/7658) @ [<a href="https://github.com/GMHDBJD">GMHDBJD</a>](https://github.com/GMHDBJD)
