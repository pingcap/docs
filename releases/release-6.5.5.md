---
title: TiDB 6.5.5 Release Notes
summary: TiDB 6.5.5 の改善点とバグ修正について説明します。
---

# TiDB 6.5.5 リリースノート {#tidb-6-5-5-release-notes}

発売日: 2023年9月21日

TiDB バージョン: 6.5.5

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 改善点 {#improvements}

-   ティビ

    -   [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-) [`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-) [`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-) [`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) [qw4990](https://github.com/qw4990)含む新しいオプティマイザヒントを追加し[＃45520](https://github.com/pingcap/tidb/issues/45520) [`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-)
    -   コプロセッサ[＃46514](https://github.com/pingcap/tidb/issues/46514) @ [あなた06](https://github.com/you06)に関連するリクエストソース情報を追加します

-   ティクヴ

    -   接続再試行のプロセスで PD クライアントのバックオフ メカニズムを追加します。これにより、エラー再試行中に再試行間隔が徐々に長くなり、PD の負荷が軽減されます[＃15428](https://github.com/tikv/tikv/issues/15428) @ [ノルーシュ](https://github.com/nolouch)
    -   スナップショット[＃15401](https://github.com/tikv/tikv/issues/15401) @ [スペードA-タン](https://github.com/SpadeA-Tang)の監視メトリックを追加します
    -   リーダー転送中の PITR チェックポイント ラグの安定性を向上[＃13638](https://github.com/tikv/tikv/issues/13638) @ [ユジュンセン](https://github.com/YuJuncen)
    -   `safe-ts` [＃15082](https://github.com/tikv/tikv/issues/15082) @ [エキシウム](https://github.com/ekexium)に関連するログと監視メトリックを追加します
    -   `resolved-ts` [＃15082](https://github.com/tikv/tikv/issues/15082) @ [エキシウム](https://github.com/ekexium)のログと監視メトリックをさらに提供

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップのCPUオーバーヘッドを削減`resolve lock` [＃40759](https://github.com/pingcap/tidb/issues/40759) @ [3ポインター](https://github.com/3pointer)

## バグ修正 {#bug-fixes}

-   ティビ

    -   ステイル読み取りで使用できないレプリカ[＃46198](https://github.com/pingcap/tidb/issues/46198) @ [ジグアン](https://github.com/zyguan)が選択される可能性がある問題を修正しました
    -   ステイル読み取りとSchema Cache [＃43481](https://github.com/pingcap/tidb/issues/43481) @ [クレイジーcs520](https://github.com/crazycs520)の非互換性により追加のオーバーヘッドが発生する問題を修正

-   ティクヴ

    -   Titan が有効になっているときに TiKV が起動に失敗し、 `Blob file deleted twice`エラーが発生する問題を修正しました[＃15454](https://github.com/tikv/tikv/issues/15454) @ [コナー1996](https://github.com/Connor1996)
    -   オンラインの安全でないリカバリがマージ中止[＃15580](https://github.com/tikv/tikv/issues/15580) @ [v01dスター](https://github.com/v01dstar)処理できない問題を修正

-   PD

    -   スケジューラの起動に時間がかかる問題を修正[＃6920](https://github.com/tikv/pd/issues/6920) @ [ヒューシャープ](https://github.com/HuSharp)
    -   スキャッターリージョンにおけるリーダーとピアの処理ロジックが一貫していない問題を修正[＃6962](https://github.com/tikv/pd/issues/6962) @ [バッファフライ](https://github.com/bufferflies)
    -   クラスタが再起動されたとき、またはPDLeaderが[＃7008](https://github.com/tikv/pd/issues/7008) @ [キャビンフィーバーB](https://github.com/CabinfeverB)に切り替えられたときに`empty-region-count`監視メトリックが異常になる問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   PITR による暗黙の主キーの復元が競合[＃46520](https://github.com/pingcap/tidb/issues/46520) @ [3ポインター](https://github.com/3pointer)を引き起こす可能性がある問題を修正
        -   PITRがメタkv [＃46578](https://github.com/pingcap/tidb/issues/46578) @ [リーヴルス](https://github.com/Leavrth)を回復するときにエラーが発生する問題を修正
        -   BR統合テストケース[＃46561](https://github.com/pingcap/tidb/issues/46561) @ [ピュアリンド](https://github.com/purelind)のエラーを修正
        -   PITRがGCS [＃47022](https://github.com/pingcap/tidb/issues/47022) @ [リーヴルス](https://github.com/Leavrth)からデータを復元できない問題を修正

    -   ティCDC

        -   PDノード[＃9565](https://github.com/pingcap/tiflow/issues/9565) @ [アズドンメン](https://github.com/asddongmen)のネットワーク分離によって発生するTiCDCレプリケーションレイテンシーの問題を修正
        -   CSV形式[＃9658](https://github.com/pingcap/tiflow/issues/9658) @ [3エースショーハンド](https://github.com/3AceShowHand)使用するとTiCDCが`UPDATE`演算を誤って`INSERT`に変更する問題を修正
        -   一部のログにユーザーパスワードが記録される問題を修正[＃9690](https://github.com/pingcap/tiflow/issues/9690) @ [スドジ](https://github.com/sdojjy)
        -   SASL認証を使用するとTiCDCがpanicを起こす可能性がある問題を修正[＃9669](https://github.com/pingcap/tiflow/issues/9669) @ [スドジ](https://github.com/sdojjy)
        -   一部の特殊なケースで TiCDC レプリケーション タスクが失敗する可能性がある問題を修正[＃9685](https://github.com/pingcap/tiflow/issues/9685) [＃9697](https://github.com/pingcap/tiflow/issues/9697) [＃9695](https://github.com/pingcap/tiflow/issues/9695) [＃9736](https://github.com/pingcap/tiflow/issues/9736) @ [ヒック](https://github.com/hicqu) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   上流にリージョン[＃9741](https://github.com/pingcap/tiflow/issues/9741) @ [スドジ](https://github.com/sdojjy)が多数ある場合に TiCDC が TiKV ノード障害から迅速に回復できない問題を修正しました。

    -   TiDB Lightning

        -   ターゲットサーバー[＃41040](https://github.com/pingcap/tidb/issues/41040) @ [ランス6716](https://github.com/lance6716)に TiCDC がデプロイされているときにTiDB Lightning が起動に失敗する問題を修正
        -   PDトポロジが変更されるとTiDB Lightningが起動に失敗する問題を修正[＃46688](https://github.com/pingcap/tidb/issues/46688) @ [ランス6716](https://github.com/lance6716)
        -   PD リーダー[＃46540](https://github.com/pingcap/tidb/issues/46540) @ [ランス6716](https://github.com/lance6716)の切り替え後にTiDB Lightning がデータのインポートを続行できない問題を修正しました。
        -   事前チェックがターゲット クラスター[＃41040](https://github.com/pingcap/tidb/issues/41040) @ [ランス6716](https://github.com/lance6716)で実行中の TiCDC の存在を正確に検出できない問題を修正しました。
