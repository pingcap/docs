---
title: TiDB 6.5.5 Release Notes
summary: TiDB 6.5.5 の改善点とバグ修正について説明します。
---

# TiDB 6.5.5 リリースノート {#tidb-6-5-5-release-notes}

発売日：2023年9月21日

TiDB バージョン: 6.5.5

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 改善点 {#improvements}

-   TiDB

    -   [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-)、[`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-)、[`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-)、[`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-)、[`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-)を含む新しいオプティマイザヒントを追加 [＃45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990)
    -   コプロセッサに関連する要求元情報を追加します [＃46514](https://github.com/pingcap/tidb/issues/46514) @ [you06](https://github.com/you06)

-   TiKV

    -   接続再試行のプロセスでPDクライアントのバックオフメカニズムを追加し、エラー再試行中に再試行間隔を徐々に増やしてPD圧力を軽減します。 [＃15428](https://github.com/tikv/tikv/issues/15428) @ [nolouch](https://github.com/nolouch)
    -   スナップショットの監視メトリックを追加します [＃15401](https://github.com/tikv/tikv/issues/15401) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   リーダー転送中の PITR チェックポイント ラグの安定性を向上[＃13638](https://github.com/tikv/tikv/issues/13638) @ [YuJuncen](https://github.com/YuJuncen)
    -   `safe-ts` に関連するログと監視メトリックを追加します [＃15082](https://github.com/tikv/tikv/issues/15082) @ [ekexium](https://github.com/ekexium)
    -   `resolved-ts` のログと監視メトリックをさらに提供 [＃15082](https://github.com/tikv/tikv/issues/15082) @ [ekexium](https://github.com/ekexium)

-   ツール

    -   Backup & Restore (BR)

        -   ログバックアップのCPUオーバーヘッドを削減`resolve lock` [＃40759](https://github.com/pingcap/tidb/issues/40759) @ [3pointer](https://github.com/3pointer)

## バグ修正 {#bug-fixes}

-   TiDB

    -   ステイル読み取り が利用できないレプリカを選択する可能性がある問題を修正しました [＃46198](https://github.com/pingcap/tidb/issues/46198) @ [zyguan](https://github.com/zyguan)
    -   ステイル読み取りとSchema Cache の非互換性により追加のオーバーヘッドが発生する問題を修正しました [＃43481](https://github.com/pingcap/tidb/issues/43481) @ [crazycs520](https://github.com/crazycs520)

-   TiKV

    -   Titanが有効になっているときにTiKVが起動に失敗し、 `Blob file deleted twice`エラーが発生する問題を修正しました [＃15454](https://github.com/tikv/tikv/issues/15454) @ [Connor1996](https://github.com/Connor1996)
    -   オンラインアンセーフリカバリがマージ中止を処理できない問題を修正 [＃15580](https://github.com/tikv/tikv/issues/15580) @ [v01dstar](https://github.com/v01dstar)

-   PD

    -   スケジューラの起動に時間がかかる問題を修正[＃6920](https://github.com/tikv/pd/issues/6920) @ [HuSharp](https://github.com/HuSharp)
    -   スキャッターリージョンにおけるリーダーとピアの処理ロジックが矛盾している問題を修正しました [＃6962](https://github.com/tikv/pd/issues/6962) @ [bufferflies](https://github.com/bufferflies)
    -   クラスタが再起動されたとき、またはPDLeaderが切り替えられたときに、 `empty-region-count`監視メトリックが異常になる問題を修正しました。 [＃7008](https://github.com/tikv/pd/issues/7008) @ [CabinfeverB](https://github.com/CabinfeverB)

-   ツール

    -   Backup & Restore (BR)

        -   PITRによる暗黙の主キーの復元が競合を引き起こす可能性がある問題を修正 [＃46520](https://github.com/pingcap/tidb/issues/46520) @ [3pointer](https://github.com/3pointer)
        -   PITRがメタkv を回復するときにエラーが発生する問題を修正しました [＃46578](https://github.com/pingcap/tidb/issues/46578) @ [Leavrth](https://github.com/Leavrth)
        -   BR統合テストケースのエラーを修正 [＃46561](https://github.com/pingcap/tidb/issues/46561) @ [purelind](https://github.com/purelind)
        -   PITRがGCS からデータを復元できない問題を修正 [＃47022](https://github.com/pingcap/tidb/issues/47022) @ [Leavrth](https://github.com/Leavrth)

    -   TiCDC

        -   PDノードのネットワーク分離によって発生するTiCDCレプリケーションのレイテンシーが大きくなる問題を修正 [＃9565](https://github.com/pingcap/tiflow/issues/9565) @ [asddongmen](https://github.com/asddongmen)
        -   CSV形式を使用するとTiCDCが誤って`UPDATE`演算を`INSERT`に変更する問題を修正 [＃9658](https://github.com/pingcap/tiflow/issues/9658) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   一部のログにユーザーパスワードが記録される問題を修正[＃9690](https://github.com/pingcap/tiflow/issues/9690) @ [sdojjy](https://github.com/sdojjy)
        -   SASL認証を使用するとTiCDCがpanicする可能性がある問題を修正[＃9669](https://github.com/pingcap/tiflow/issues/9669) @ [sdojjy](https://github.com/sdojjy)
        -   一部のコーナーケースで TiCDC レプリケーションタスクが失敗する可能性がある問題を修正[＃9685](https://github.com/pingcap/tiflow/issues/9685) [＃9697](https://github.com/pingcap/tiflow/issues/9697) [＃9695](https://github.com/pingcap/tiflow/issues/9695) [＃9736](https://github.com/pingcap/tiflow/issues/9736) @ [hicqu](https://github.com/hicqu) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   上流にリージョンが多数ある場合、TiCDC が TiKV ノード障害から迅速に回復できない問題を修正しました。 [＃9741](https://github.com/pingcap/tiflow/issues/9741) @ [sdojjy](https://github.com/sdojjy)

    -   TiDB Lightning

        -   ターゲットサーバーにTiCDCがデプロイされているときにTiDB Lightningが起動に失敗する問題を修正 [＃41040](https://github.com/pingcap/tidb/issues/41040) @ [lance6716](https://github.com/lance6716)
        -   PDトポロジが変更されるとTiDB Lightningが起動に失敗する問題を修正[＃46688](https://github.com/pingcap/tidb/issues/46688) @ [lance6716](https://github.com/lance6716)
        -   PD のリーダーを@ [lance6716](https://github.com/lance6716)切り替えた後にTiDB Lightning がデータのインポートを続行できない問題を修正しました [＃46540](https://github.com/pingcap/tidb/issues/46540)
        -   事前チェックがターゲット クラスターで実行中の TiCDC の存在を正確に検出できない問題を修正しました。 [＃41040](https://github.com/pingcap/tidb/issues/41040) @ [lance6716](https://github.com/lance6716)
