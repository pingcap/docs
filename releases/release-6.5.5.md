---
title: TiDB 6.5.5 Release Notes
summary: Learn about the improvements and bug fixes in TiDB 6.5.5.
---

# TiDB 6.5.5 リリースノート {#tidb-6-5-5-release-notes}

発売日：2023年9月21日

TiDB バージョン: 6.5.5

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.5.5#version-list)

## 改善点 {#improvements}

-   TiDB

    -   新しいオプティマイザー ヒント ( [`NO_MERGE_JOIN()`](https://docs.pingcap.com/tidb/v6.5/optimizer-hints#no_merge_joint1_name--tl_name-) 、 [`NO_INDEX_JOIN()`](https://docs.pingcap.com/tidb/v6.5/optimizer-hints#no_index_joint1_name--tl_name-) 、 [`NO_INDEX_MERGE_JOIN()`](https://docs.pingcap.com/tidb/v6.5/optimizer-hints#no_index_merge_joint1_name--tl_name-) 、 [`NO_HASH_JOIN()`](https://docs.pingcap.com/tidb/v6.5/optimizer-hints#no_hash_joint1_name--tl_name-) 、 [`NO_INDEX_HASH_JOIN()`](https://docs.pingcap.com/tidb/v6.5/optimizer-hints#no_index_hash_joint1_name--tl_name-) [#45520](https://github.com/pingcap/tidb/issues/45520) @ [qw4990](https://github.com/qw4990)など) を追加します。
    -   コプロセッサ[#46514](https://github.com/pingcap/tidb/issues/46514) @ [あなた06](https://github.com/you06)に関するリクエスト元情報を追加

-   TiKV

    -   接続再試行のプロセスで PD クライアントのバックオフ メカニズムを追加します。これにより、エラー再試行中の再試行間隔が徐々に増加し、PD プレッシャー[#15428](https://github.com/tikv/tikv/issues/15428) @ [ノールーシュ](https://github.com/nolouch)が軽減されます。
    -   スナップショット[#15401](https://github.com/tikv/tikv/issues/15401) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)の監視メトリクスを追加
    -   リーダー転送中の PITR チェックポイント ラグの安定性を向上[#13638](https://github.com/tikv/tikv/issues/13638) @ [ユジュンセン](https://github.com/YuJuncen)
    -   `safe-ts` [#15082](https://github.com/tikv/tikv/issues/15082) @ [エキシウム](https://github.com/ekexium)に関連するログと監視メトリクスを追加します
    -   `resolved-ts` [#15082](https://github.com/tikv/tikv/issues/15082) @ [エキシウム](https://github.com/ekexium)のログと監視メトリクスをさらに提供します
    -   圧縮メカニズムを最適化します。リージョンが分割されるときに、分割するキーがない場合、過剰な MVCC バージョン[#15282](https://github.com/tikv/tikv/issues/15282) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)を排除するために圧縮がトリガーされます。

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップの CPU オーバーヘッドを削減`resolve lock` [#40759](https://github.com/pingcap/tidb/issues/40759) @ [3ポインター](https://github.com/3pointer)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ステイル読み取り が使用できないレプリカ[#46198](https://github.com/pingcap/tidb/issues/46198) @ [ジグアン](https://github.com/zyguan)を選択する可能性がある問題を修正
    -   ステイル読み取りと Schema Cache [#43481](https://github.com/pingcap/tidb/issues/43481) @ [クレイジークス520](https://github.com/crazycs520)の間の非互換性により追加のオーバーヘッドが発生する問題を修正

-   TiKV

    -   TiKV ノードに障害が発生したときに、対応するリージョンのピアが誤って休止状態になる問題を修正します[#14547](https://github.com/tikv/tikv/issues/14547) @ [ひっくり返る](https://github.com/hicqu)
    -   Titan が有効になっているときに TiKV が起動できず、 `Blob file deleted twice`エラーが発生する問題を修正します[#15454](https://github.com/tikv/tikv/issues/15454) @ [コナー1996](https://github.com/Connor1996)
    -   Online Unsafe Recovery がマージ中止[#15580](https://github.com/tikv/tikv/issues/15580) @ [v01dstar](https://github.com/v01dstar)を処理できない問題を修正
    -   PD と TiKV の間のネットワークの中断により PITR がスタックする可能性がある問題を修正します[#15279](https://github.com/tikv/tikv/issues/15279) @ [ユジュンセン](https://github.com/YuJuncen)

-   PD

    -   スケジューラーの起動に時間がかかる問題を修正[#6920](https://github.com/tikv/pd/issues/6920) @ [ヒューシャープ](https://github.com/HuSharp)
    -   散布リージョンのリーダーとピアを処理するロジックが矛盾している問題を修正[#6962](https://github.com/tikv/pd/issues/6962) @ [バッファフライ](https://github.com/bufferflies)
    -   クラスタ再起動時やPDLeader切り替え[#7008](https://github.com/tikv/pd/issues/7008) @ [キャビンフィーバーB](https://github.com/CabinfeverB)時に`empty-region-count`監視メトリクスが異常になる問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   PITR によって暗黙的な主キーを復元すると競合が発生する可能性がある問題を修正[#46520](https://github.com/pingcap/tidb/issues/46520) @ [3ポインター](https://github.com/3pointer)
        -   PITRがmeta-kv [#46578](https://github.com/pingcap/tidb/issues/46578) @ [レヴルス](https://github.com/Leavrth)を回復するときにエラーが発生する問題を修正
        -   BR統合テスト ケース[#45561](https://github.com/pingcap/tidb/issues/46561) @ [ピュアリンド](https://github.com/purelind)のエラーを修正
        -   リージョンリーダーの移行が発生したときに PITR ログ バックアップの進行状況のレイテンシーが増加する問題を緩和します[#13638](https://github.com/tikv/tikv/issues/13638) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   PD ノード[#9565](https://github.com/pingcap/tiflow/issues/9565) @ [東門](https://github.com/asddongmen)のネットワーク分離によって引き起こされる高い TiCDC レプリケーションレイテンシーの問題を修正します。
        -   CSV 形式[#9658](https://github.com/pingcap/tiflow/issues/9658) @ [3エースショーハンド](https://github.com/3AceShowHand)を使用すると、TiCDC が`UPDATE`操作を誤って`INSERT`に変更する問題を修正します。
        -   ユーザーのパスワードが一部のログ[#9690](https://github.com/pingcap/tiflow/issues/9690) @ [スドジ](https://github.com/sdojjy)に記録される問題を修正
        -   SASL 認証を使用すると TiCDC がpanic[#9669](https://github.com/pingcap/tiflow/issues/9669) @ [スドジ](https://github.com/sdojjy)を引き起こす可能性がある問題を修正
        -   TiCDC レプリケーション タスクが特殊なケースで失敗する可能性がある問題を修正します[#9685](https://github.com/pingcap/tiflow/issues/9685) [#9697](https://github.com/pingcap/tiflow/issues/9697) [#9695](https://github.com/pingcap/tiflow/issues/9695) [#9736](https://github.com/pingcap/tiflow/issues/9736) @ [ひっくり返る](https://github.com/hicqu) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   アップストリーム[#9741](https://github.com/pingcap/tiflow/issues/9741) @ [スドジ](https://github.com/sdojjy)に多数のリージョンがある場合、TiCDC が TiKV ノードの障害から迅速に回復できない問題を修正

    -   TiDB Lightning

        -   TiCDC がターゲットサーバー[#41040](https://github.com/pingcap/tidb/issues/41040) @ [ランス6716](https://github.com/lance6716)にデプロイされている場合にTiDB Lightning が起動できない問題を修正
        -   PD トポロジを変更するとTiDB Lightning が起動できない問題を修正[#46688](https://github.com/pingcap/tidb/issues/46688) @ [ランス6716](https://github.com/lance6716)
        -   PD がリーダー[#46540](https://github.com/pingcap/tidb/issues/46540) @ [ランス6716](https://github.com/lance6716)を切り替えた後、 TiDB Lightning がデータのインポートを続行できない問題を修正
        -   事前チェックがターゲット クラスター[#41040](https://github.com/pingcap/tidb/issues/41040) @ [ランス6716](https://github.com/lance6716)で実行中の TiCDC の存在を正確に検出できない問題を修正します。
