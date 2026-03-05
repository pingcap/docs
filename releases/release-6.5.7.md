---
title: TiDB 6.5.7 Release Notes
summary: TiDB 6.5.7 の改善点とバグ修正について説明します。
---

# TiDB 6.5.7 リリースノート {#tidb-6-5-7-release-notes}

発売日：2024年1月8日

TiDB バージョン: 6.5.7

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiDB 構成項目[`performance.force-init-stats`](https://docs.pingcap.com/tidb/v6.5/tidb-configuration-file#force-init-stats-new-in-v657)導入して、TiDB の起動時にサービスを提供する前に統計の初期化が完了するまで TiDB が待機する必要があるかどうかを制御します[＃43385](https://github.com/pingcap/tidb/issues/43385) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
-   ログ印刷のオーバーヘッドを減らすために、 TiFlashはデフォルト値の`logger.level`を`"debug"`から`"info"` [＃8568](https://github.com/pingcap/tiflash/issues/8568) @ [xzhangxian1008](https://github.com/xzhangxian1008)に変更します。

## 改善点 {#improvements}

-   TiDB

    -   パーティションテーブル[＃47071](https://github.com/pingcap/tidb/issues/47071) [＃47104](https://github.com/pingcap/tidb/issues/47104) [＃46804](https://github.com/pingcap/tidb/issues/46804) @ [ホーキングレイ](https://github.com/hawkingrei)での`ANALYZE`操作のメモリ使用量とパフォーマンスを最適化します
    -   プランキャッシュをサポートして、オプティマイザ修正コントロール[＃44830](https://github.com/pingcap/tidb/issues/44830) @ [qw4990](https://github.com/qw4990)を使用して物理的な最適化中に生成された`PointGet`演算子を含む実行プランをキャッシュします。
    -   特定のシナリオで`OUTER JOIN`を`INNER JOIN`に変換する能力を強化する[＃49616](https://github.com/pingcap/tidb/issues/49616) @ [qw4990](https://github.com/qw4990)

-   TiFlash

    -   ディスクパフォーマンスジッタによる読み取りレイテンシーへの影響を軽減[＃8583](https://github.com/pingcap/tiflash/issues/8583) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   大規模なデータセット[＃48301](https://github.com/pingcap/tidb/issues/48301) @ [リーヴルス](https://github.com/Leavrth)シナリオで`RESTORE`ステートメントのテーブル作成パフォーマンスを向上
        -   EBS ベースのスナップショット バックアップとTiDB Lightningインポート間の互換性の問題を解決[＃46850](https://github.com/pingcap/tidb/issues/46850) @ [ユジュンセン](https://github.com/YuJuncen)
        -   リージョンリーダーシップの移行が発生すると、PITR ログバックアップの進行のレイテンシーが長くなるという問題を軽減します[＃13638](https://github.com/tikv/tikv/issues/13638) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   ダウンストリームがKafkaの場合、トピック式では`schema`オプションとして指定でき、トピック名を直接指定できます[＃9763](https://github.com/pingcap/tiflow/issues/9763) @ [3エースショーハンド](https://github.com/3AceShowHand)

## バグ修正 {#bug-fixes}

-   TiDB

    -   短時間に多数の`CREATE TABLE`文が実行されると、TiDB が同時に新しい統計メタデータを作成しない可能性があり、後続のクエリ推定で正確な行数情報を取得できない問題を修正しました[＃36004](https://github.com/pingcap/tidb/issues/36004) [＃38189](https://github.com/pingcap/tidb/issues/38189) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   監査ログ用のエンタープライズプラグインを使用すると、TiDBサーバーが大量のリソースを消費する可能性がある問題を修正[＃49273](https://github.com/pingcap/tidb/issues/49273) @ [lcwangchao](https://github.com/lcwangchao)
    -   `ErrLoadDataInvalidURI`の誤ったエラーメッセージを修正 (無効な S3 URI エラー) [＃48164](https://github.com/pingcap/tidb/issues/48164) @ [ランス6716](https://github.com/lance6716)
    -   `tidb_server_memory_limit` [＃48741](https://github.com/pingcap/tidb/issues/48741) @ [徐淮嶼](https://github.com/XuHuaiyu)による長期メモリ圧迫により TiDB の CPU 使用率が上昇する問題を修正
    -   共通テーブル式 (CTE) を含むクエリがメモリ制限を超えたときに予期せず停止する問題を修正[＃49096](https://github.com/pingcap/tidb/issues/49096) @ [アイリンキッド](https://github.com/AilinKid)
    -   同じクエリプランで、場合によっては[＃47634](https://github.com/pingcap/tidb/issues/47634) @ [キング・ディラン](https://github.com/King-Dylan)の異なる`PLAN_DIGEST`値が発生する問題を修正しました
    -   CTE を含むクエリが、 `tidb_max_chunk_size`小さい値[＃48808](https://github.com/pingcap/tidb/issues/48808) @ [グオシャオゲ](https://github.com/guo-shaoge)に設定されている場合に`runtime error: index out of range [32] with length 32`報告する問題を修正しました。
    -   正常なシャットダウン中に TiDBサーバーがpanic可能性がある問題を修正[＃36793](https://github.com/pingcap/tidb/issues/36793) @ [bb7133](https://github.com/bb7133)
    -   TiDB [＃42931](https://github.com/pingcap/tidb/issues/42931) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)の初期バージョンからエクスポートされた統計をインポートするときに統計データエラーが発生する可能性がある問題を修正しました。
    -   Golang の暗黙的な変換アルゴリズム[＃49801](https://github.com/pingcap/tidb/issues/49801) @ [qw4990](https://github.com/qw4990)によって発生する統計情報の構築における過剰な統計エラーの問題を修正しました
    -   特定のシナリオでオプティマイザがTiFlash選択パスを DUAL テーブルに誤って変換する問題を修正[＃49285](https://github.com/pingcap/tidb/issues/49285) @ [アイリンキッド](https://github.com/AilinKid)
    -   `ENUM`または`SET`種類の無効な値を解析すると、SQL ステートメント エラー[＃49487](https://github.com/pingcap/tidb/issues/49487) @ [ウィノロス](https://github.com/winoros)が直接発生する問題を修正しました。
    -   `WITH RECURSIVE` CTE を含む`UPDATE`または`DELETE`ステートメントで誤った結果が生成される可能性がある問題を修正しました[＃48969](https://github.com/pingcap/tidb/issues/48969) @ [ウィノロス](https://github.com/winoros)
    -   データの末尾にスペースが含まれている場合に`LIKE`で`_`ワイルドカードを使用すると、クエリ結果が不正確になる可能性がある問題を修正しました[＃48983](https://github.com/pingcap/tidb/issues/48983) @ [時間と運命](https://github.com/time-and-fate)
    -   IndexHashJoin 演算子を含むクエリがメモリが`tidb_mem_quota_query` [＃49033](https://github.com/pingcap/tidb/issues/49033) @ [徐淮嶼](https://github.com/XuHuaiyu)を超えると停止する問題を修正しました
    -   ネストされた`UNION`クエリ[＃49377](https://github.com/pingcap/tidb/issues/49377) @ [アイリンキッド](https://github.com/AilinKid)で`LIMIT`と`OPRDERBY`無効になる可能性がある問題を修正しました
    -   非厳密モード（ `sql_mode = ''` ）で、 `INSERT`実行中に切り捨てが行われても、 [天菜まお](https://github.com/tiancaiamao)でエラー[＃49369](https://github.com/pingcap/tidb/issues/49369)が報告される問題を修正しました。
    -   TiDBがパニックを起こしてエラーを報告する問題を修正`invalid memory address or nil pointer dereference` [＃42739](https://github.com/pingcap/tidb/issues/42739) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   CTEクエリが再試行プロセス[＃46522](https://github.com/pingcap/tidb/issues/46522) @ [天菜まお](https://github.com/tiancaiamao)中にエラー`type assertion for CTEStorageMap failed`を報告する可能性がある問題を修正しました
    -   一部のタイムゾーン[＃49586](https://github.com/pingcap/tidb/issues/49586) @ [金星の上](https://github.com/overvenus)で夏時間が正しく表示されない問題を修正
    -   依存関係のある 2 つの DDL タスクの完了時間が[＃49498](https://github.com/pingcap/tidb/issues/49498) @ [接線](https://github.com/tangenta)と誤って順序付けられる問題を修正しました。

-   TiKV

    -   破損したSSTファイルが他のTiKVノード[＃15986](https://github.com/tikv/tikv/issues/15986) @ [コナー1996](https://github.com/Connor1996)に広がる可能性がある問題を修正
    -   大規模なトランザクション[＃14864](https://github.com/tikv/tikv/issues/14864) @ [金星の上](https://github.com/overvenus)を追跡するときに、古い読み取りの解決済み TS が TiKV OOM 問題を引き起こす可能性がある問題を修正しました
    -   TiKVがraft log [＃15800](https://github.com/tikv/tikv/issues/15800) @ [トニー・シュッキ](https://github.com/tonyxuqqi)を追加できないため`ServerIsBusy`エラーを報告する問題を修正しました。

-   PD

    -   SQLの配置ルールで設定された`location-labels`特定の条件下で期待どおりにスケジュールされない問題を修正[＃6637](https://github.com/tikv/pd/issues/6637) @ [rleungx](https://github.com/rleungx)
    -   レプリカ数が[＃7584](https://github.com/tikv/pd/issues/7584) @ [バッファフライ](https://github.com/bufferflies)要件を満たしていない場合に孤立ピアが削除される問題を修正しました

-   TiFlash

    -   `FLASHBACK DATABASE` [＃8450](https://github.com/pingcap/tiflash/issues/8450) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を実行した後もTiFlashレプリカのデータがガベージコレクションされる問題を修正しました
    -   クエリ[＃8447](https://github.com/pingcap/tiflash/issues/8447) @ [ジンヘリン](https://github.com/JinheLin)中にTiFlash がメモリ制限に遭遇するとメモリリークが発生する問題を修正しました。
    -   Grafana [＃8076](https://github.com/pingcap/tiflash/issues/8076) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)の一部のパネルの最大パーセンタイル時間の表示が誤っていた問題を修正
    -   クエリ[＃8564](https://github.com/pingcap/tiflash/issues/8564) @ [ジンヘリン](https://github.com/JinheLin)の低速化によりメモリ使用量が大幅に増加する問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   タスク初期化中にPDへの接続に失敗すると、ログバックアップタスクは開始できるが正常に動作しない問題を修正[＃16056](https://github.com/tikv/tikv/issues/16056) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   TiCDC が下流の MySQL [＃10334](https://github.com/pingcap/tiflow/issues/10334) @ [張金鵬87](https://github.com/zhangjinpeng87)にデータを複製するときに`checkpoint-ts`スタックする可能性がある問題を修正しました
        -   `kv-client`初期化[＃10095](https://github.com/pingcap/tiflow/issues/10095) @ [3エースショーハンド](https://github.com/3AceShowHand)中に発生する可能性のあるデータ競合問題を修正
