---
title: TiDB 6.1.3 Release Notes
---

# TiDB 6.1.3 リリースノート {#tidb-6-1-3-release-notes}

発売日：2022年12月5日

TiDB バージョン: 6.1.3

クイックアクセス: [インストールパッケージ](https://www.pingcap.com/download/?version=v6.1.3#version-list)

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiCDC

        -   デフォルト値[東門](https://github.com/asddongmen)

## 改善点 {#improvements}

-   PD

    -   ロックの粒度を最適化してロックの競合を軽減し、高同時実行[ルルンクス](https://github.com/rleungx)でのハートビートの処理能力を向上させます。

-   ツール

    -   TiCDC

        -   パフォーマンスを向上させるために、デフォルトで TiCDC のトランザクション分割を有効にし、チェンジフィードのセーフ モードを無効にします[東門](https://github.com/asddongmen)
        -   Kafka プロトコル エンコーダ[3エースショーハンド](https://github.com/3AceShowHand)のパフォーマンスを向上させます。

-   その他

    -   TiDB の Go コンパイラー バージョンを go1.18 から[`GOMEMLIMIT`を構成することで OOM の問題を軽減する](/configure-memory-usage.md#mitigate-oom-issues-by-configuring-gomemlimit)を参照してください。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `mysql.tables_priv`テーブル[Cbcウェストウルフ](https://github.com/CbcWestwolf)で`grantor`フィールドが欠落している問題を修正
    -   結合したテーブルの再配置 [ウィノロス](https://github.com/winoros)で誤ってプッシュダウンされた条件が破棄された場合に、間違ったクエリ結果が発生する問題を修正しました。
    -   `get_lock()`で取得したロックが 10 分以上保持できない問題を修正[タンジェンタ](https://github.com/tangenta)
    -   検査制約[ヤンケオ](https://github.com/YangKeao)で自動インクリメントカラムが使用できない問題を修正
    -   gPRCログが間違ったファイルに出力される問題を修正[ゼボックス](https://github.com/xhebox)
    -   テーブルが切り捨てられるか削除されると、テーブルのTiFlash同期ステータスが etcd から削除されない問題を修正します[カルビンネオ](https://github.com/CalvinNeo)
    -   データ ソース名インジェクションを介してデータ ファイルに無制限にアクセスできる問題を修正します (CVE-2022-3023) [ランス6716](https://github.com/lance6716)
    -   `NO_ZERO_DATE` SQL モード[孟新9014](https://github.com/mengxin9014)で関数`str_to_date`間違った結果を返す問題を修正
    -   バックグラウンドでの統計収集タスクがpanic[リリンハイ](https://github.com/lilinghai)になる可能性がある問題を修正
    -   一部のシナリオで、悲観的ロックが非一意のセカンダリ インデックス[エキシウム](https://github.com/ekexium)に誤って追加される問題を修正します。

<!---->

-   PD

    -   不正確なストリーム タイムアウトを修正し、リーダーの切り替え[キャビンフィーバーB](https://github.com/CabinfeverB)を高速化します。

<!---->

-   TiKV

    -   スナップショット取得中のリース期限切れによって引き起こされる異常なリージョン競合を修正[SpadeA-Tang](https://github.com/SpadeA-Tang)

-   TiFlash

    -   引数の型が`UInt8` [xzhangxian1008](https://github.com/xzhangxian1008)の場合、論理演算子が間違った結果を返す問題を修正
    -   `CAST(value AS DATETIME)`の間違ったデータ入力によりTiFlash sys CPU [xzhangxian1008](https://github.com/xzhangxian1008)のパフォーマンスが高くなる問題を修正
    -   書き込み圧力が高いと、デルタレイヤー[リデジュ](https://github.com/lidezhu)で多すぎる列ファイルが生成される可能性がある問題を修正します。
    -   TiFlash [リデジュ](https://github.com/lidezhu)の再起動後にデルタレイヤーのカラムファイルが圧縮できない問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   データベースまたはテーブル[モクイシュル28](https://github.com/MoCuishle28)の照合順序に古いフレームワークを使用すると、復元タスクが失敗する問題を修正します。

    -   TiCDC

        -   最初に DDL ステートメントを実行し、次に変更フィード[東門](https://github.com/asddongmen)を一時停止して再開するシナリオで発生したデータ損失を修正しました。
        -   ダウンストリーム ネットワークが利用できない場合にシンクコンポーネントがスタックする問題を修正[ひっくり返る](https://github.com/hicqu)

    -   TiDB データ移行 (DM)

        -   `collation_compatible`を`"strict"`に設定すると、DM が重複した照合順序[ランス6716](https://github.com/lance6716)を含む SQL を生成する可能性がある問題を修正します。
        -   DM タスクが`Unknown placement policy`エラー[ランス6716](https://github.com/lance6716)で停止することがある問題を修正
        -   場合によってはリレーログが上流から再度取得される場合がある問題を修正[リウメンギャ94](https://github.com/liumengya94)
        -   既存のワーカーが終了する前に新しい DM ワーカーがスケジュールされている場合、データが複数回レプリケートされる問題を修正します[GMHDBJD](https://github.com/GMHDBJD)
