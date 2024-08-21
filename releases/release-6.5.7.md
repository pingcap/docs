---
title: TiDB 6.5.7 Release Notes
summary: TiDB 6.5.7 の改善点とバグ修正について説明します。
---

# TiDB 6.5.7 リリースノート {#tidb-6-5-7-release-notes}

発売日: 2024年1月8日

TiDB バージョン: 6.5.7

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiDB 構成項目[`performance.force-init-stats`](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#force-init-stats-new-in-v657)を導入して、TiDB 起動時にサービスを提供する前に統計の初期化が完了するまで TiDB が待機する必要があるかどうかを制御します[＃43385](https://github.com/pingcap/tidb/issues/43385) @ [翻訳者](https://github.com/xuyifangreeneyes)
-   ログ印刷のオーバーヘッドを減らすために、 TiFlashはデフォルト値`logger.level`を`"debug"`から`"info"` [＃8568](https://github.com/pingcap/tiflash/issues/8568) @ [翻訳者](https://github.com/xzhangxian1008)に変更します。

## 改善点 {#improvements}

-   ティビ

    -   パーティションテーブル[＃47071](https://github.com/pingcap/tidb/issues/47071) [＃47104](https://github.com/pingcap/tidb/issues/47104) [＃46804](https://github.com/pingcap/tidb/issues/46804) @ [ホーキングレイ](https://github.com/hawkingrei)での`ANALYZE`操作のメモリ使用量とパフォーマンスを最適化します
    -   プランキャッシュをサポートし、オプティマイザ修正コントロール[＃44830](https://github.com/pingcap/tidb/issues/44830) @ [qw4990](https://github.com/qw4990)を使用して物理的な最適化中に生成された`PointGet`演算子を含む実行プランをキャッシュします。
    -   特定のシナリオで`OUTER JOIN` `INNER JOIN`に変換する能力を強化する[＃49616](https://github.com/pingcap/tidb/issues/49616) @ [qw4990](https://github.com/qw4990)

-   TiFlash

    -   ディスクパフォ​​ーマンスジッターによる読み取りレイテンシーへの影響を軽減[＃8583](https://github.com/pingcap/tiflash/issues/8583) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   大規模なデータセットのシナリオで`RESTORE`ステートメントのテーブル作成パフォーマンスを向上[＃48301](https://github.com/pingcap/tidb/issues/48301) @ [リーヴルス](https://github.com/Leavrth)
        -   EBS ベースのスナップショット バックアップとTiDB Lightningインポート間の互換性の問題を解決する[＃46850](https://github.com/pingcap/tidb/issues/46850) @ [ユジュンセン](https://github.com/YuJuncen)
        -   リージョンリーダーシップの移行が発生すると、PITR ログバックアップの進行のレイテンシーが長くなるという問題を緩和します[＃13638](https://github.com/tikv/tikv/issues/13638) @ [ユジュンセン](https://github.com/YuJuncen)

    -   ティCDC

        -   ダウンストリームがKafkaの場合、トピック式では`schema`をオプションとして指定でき、トピック名を直接指定できます[＃9763](https://github.com/pingcap/tiflow/issues/9763) @ [3エースショーハンド](https://github.com/3AceShowHand)

## バグ修正 {#bug-fixes}

-   ティビ

    -   短時間に多数の`CREATE TABLE`ステートメントが実行されると、TiDB が新しい統計メタデータを同時に作成しない可能性があり、後続のクエリ推定で正確な行数情報を取得できない問題を修正しました[＃36004](https://github.com/pingcap/tidb/issues/36004) [＃38189](https://github.com/pingcap/tidb/issues/38189) @ [翻訳者](https://github.com/xuyifangreeneyes)
    -   監査ログ用のエンタープライズプラグインが使用されている場合に TiDBサーバーが大量のリソースを消費する可能性がある問題を修正[＃49273](https://github.com/pingcap/tidb/issues/49273) @ [lcwangchao](https://github.com/lcwangchao)
    -   `ErrLoadDataInvalidURI`の誤ったエラー メッセージを修正 (無効な S3 URI エラー) [＃48164](https://github.com/pingcap/tidb/issues/48164) @ [ランス6716](https://github.com/lance6716)
    -   `tidb_server_memory_limit` [＃48741](https://github.com/pingcap/tidb/issues/48741) @ [徐淮宇](https://github.com/XuHuaiyu)による長期メモリ圧迫により TiDB の CPU 使用率が高くなる問題を修正
    -   メモリ制限を超えると、共通テーブル式 (CTE) を含むクエリが予期せず停止する問題を修正[＃49096](https://github.com/pingcap/tidb/issues/49096) @ [アイリンキッド](https://github.com/AilinKid)
    -   同じクエリプランで`PLAN_DIGEST`値が[＃47634](https://github.com/pingcap/tidb/issues/47634) @ [キング・ディラン](https://github.com/King-Dylan)場合に異なる問題を修正
    -   CTE を含むクエリで、 `tidb_max_chunk_size`が小さい値[＃48808](https://github.com/pingcap/tidb/issues/48808) @ [グオシャオゲ](https://github.com/guo-shaoge)に設定されている場合に`runtime error: index out of range [32] with length 32`報告される問題を修正しました。
    -   正常なシャットダウン中に TiDBサーバーがpanicになる可能性がある問題を修正[＃36793](https://github.com/pingcap/tidb/issues/36793) @ [bb7133](https://github.com/bb7133)
    -   TiDB [＃42931](https://github.com/pingcap/tidb/issues/42931) @ [翻訳者](https://github.com/xuyifangreeneyes)の初期バージョンからエクスポートされた統計をインポートするときに統計データエラーが発生する可能性がある問題を修正しました。
    -   Golang の暗黙的な変換アルゴリズム[＃49801](https://github.com/pingcap/tidb/issues/49801) @ [qw4990](https://github.com/qw4990)によって発生する統計の構築における過度の統計エラーの問題を修正
    -   特定のシナリオでオプティマイザがTiFlash選択パスを DUAL テーブルに誤って変換する問題を修正[＃49285](https://github.com/pingcap/tidb/issues/49285) @ [アイリンキッド](https://github.com/AilinKid)
    -   `ENUM`または`SET`型の無効な値を解析すると、SQL ステートメント エラー[＃49487](https://github.com/pingcap/tidb/issues/49487) @ [ウィノロス](https://github.com/winoros)が直接発生する問題を修正しました。
    -   `WITH RECURSIVE` CTE を含む`UPDATE`または`DELETE`ステートメントで誤った結果が生成される可能性がある問題を修正しました[＃48969](https://github.com/pingcap/tidb/issues/48969) @ [ウィノロス](https://github.com/winoros)
    -   データの末尾にスペースが含まれている場合に`LIKE`で`_`ワイルドカードを使用すると、クエリ結果が不正確になる可能性がある問題を修正しました[＃48983](https://github.com/pingcap/tidb/issues/48983) @ [時間と運命](https://github.com/time-and-fate)
    -   メモリが`tidb_mem_quota_query` [＃49033](https://github.com/pingcap/tidb/issues/49033) @ [徐淮宇](https://github.com/XuHuaiyu)を超えると IndexHashJoin 演算子を含むクエリが停止する問題を修正しました。
    -   ネストされた`UNION`のクエリ[＃49377](https://github.com/pingcap/tidb/issues/49377) @ [アイリンキッド](https://github.com/AilinKid)で`LIMIT`と`OPRDERBY`無効になる可能性がある問題を修正しました
    -   非厳密モード（ `sql_mode = ''` ）で、 `INSERT`実行中に切り捨てが行われても、 [天菜まお](https://github.com/tiancaiamao)でエラー[＃49369](https://github.com/pingcap/tidb/issues/49369)が報告される問題を修正しました。
    -   TiDBがパニックを起こしてエラーを報告する問題を修正`invalid memory address or nil pointer dereference` [＃42739](https://github.com/pingcap/tidb/issues/42739) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)
    -   CTEクエリが再試行プロセス[＃46522](https://github.com/pingcap/tidb/issues/46522) @ [天菜まお](https://github.com/tiancaiamao)中にエラー`type assertion for CTEStorageMap failed`を報告する可能性がある問題を修正
    -   一部のタイムゾーンで夏時間が正しく表示されない問題を修正[＃49586](https://github.com/pingcap/tidb/issues/49586) @ [金星の上](https://github.com/overvenus)
    -   依存関係のある 2 つの DDL タスクの完了時間が[＃49498](https://github.com/pingcap/tidb/issues/49498) @ [タンジェンタ](https://github.com/tangenta)と誤って順序付けられる問題を修正しました。

-   ティクヴ

    -   破損したSSTファイルが他のTiKVノード[＃15986](https://github.com/tikv/tikv/issues/15986) @ [コナー1996](https://github.com/Connor1996)に広がる可能性がある問題を修正
    -   大規模なトランザクションを追跡するときに、古い読み取りの解決済み TS によって TiKV OOM の問題が発生する可能性がある問題を修正[＃14864](https://github.com/tikv/tikv/issues/14864) @ [金星の上](https://github.com/overvenus)
    -   TiKV がラフトログ[＃15800](https://github.com/tikv/tikv/issues/15800) @ [トニー](https://github.com/tonyxuqqi)を追加できないため`ServerIsBusy`エラーを報告する問題を修正しました。

-   PD

    -   特定の条件下では、SQL の配置ルールによって設定された`location-labels`が期待どおりにスケジュールされない問題を修正[＃6637](https://github.com/tikv/pd/issues/6637) @ [rleungx](https://github.com/rleungx)
    -   レプリカ数が要件[＃7584](https://github.com/tikv/pd/issues/7584) @ [バッファフライ](https://github.com/bufferflies)を満たしていない場合に孤立ピアが削除される問題を修正

-   TiFlash

    -   `FLASHBACK DATABASE` [＃8450](https://github.com/pingcap/tiflash/issues/8450) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を実行した後もTiFlashレプリカのデータがガベージ コレクションされる問題を修正しました。
    -   クエリ[＃8447](https://github.com/pingcap/tiflash/issues/8447) @ [ジンヘリン](https://github.com/JinheLin)中にTiFlash がメモリ制限に遭遇した場合のメモリリークの問題を修正しました。
    -   Grafana [＃8076](https://github.com/pingcap/tiflash/issues/8076) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)の一部のパネルの最大パーセンタイル時間の誤った表示を修正
    -   クエリが遅いためにメモリ使用量が大幅に増加する問題を修正[＃8564](https://github.com/pingcap/tiflash/issues/8564) @ [ジンヘリン](https://github.com/JinheLin)

-   ツール

    -   バックアップと復元 (BR)

        -   タスク初期化中にPDへの接続に失敗すると、ログバックアップタスクは開始できるが正常に動作しない問題を修正[＃16056](https://github.com/tikv/tikv/issues/16056) @ [ユジュンセン](https://github.com/YuJuncen)

    -   ティCDC

        -   TiCDC がデータを下流の MySQL [＃10334](https://github.com/pingcap/tiflow/issues/10334) @ [張金鵬87](https://github.com/zhangjinpeng87)に複製するときに`checkpoint-ts`スタックする可能性がある問題を修正しました。
        -   `kv-client`初期化[＃10095](https://github.com/pingcap/tiflow/issues/10095) @ [3エースショーハンド](https://github.com/3AceShowHand)中に発生する可能性のあるデータ競合問題を修正
