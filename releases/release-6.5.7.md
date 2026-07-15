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
-   ログ印刷のオーバーヘッドを減らすために、 TiFlashはデフォルト値の`logger.level`を`"debug"`から`"info"` に変更します。 [＃8568](https://github.com/pingcap/tiflash/issues/8568) @ [xzhangxian1008](https://github.com/xzhangxian1008)

## 改善点 {#improvements}

-   TiDB

    -   パーティションテーブル[＃47071](https://github.com/pingcap/tidb/issues/47071) での`ANALYZE`操作のメモリ使用量とパフォーマンスを最適化します [＃46804](https://github.com/pingcap/tidb/issues/46804) @ [hawkingrei](https://github.com/hawkingrei) [＃47104](https://github.com/pingcap/tidb/issues/47104)
    -   プランキャッシュをサポートして、オプティマイザ修正コントロールを使用して物理的な最適化中に生成された`PointGet`演算子を含む実行プランをキャッシュします。 [＃44830](https://github.com/pingcap/tidb/issues/44830) @ [qw4990](https://github.com/qw4990)
    -   特定のシナリオで`OUTER JOIN`を`INNER JOIN`に変換する能力を強化する[＃49616](https://github.com/pingcap/tidb/issues/49616) @ [qw4990](https://github.com/qw4990)

-   TiFlash

    -   ディスクパフォーマンスジッタによる読み取りレイテンシーへの影響を軽減[＃8583](https://github.com/pingcap/tiflash/issues/8583) @ [JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   Backup & Restore (BR)

        -   大規模なデータセットシナリオで`RESTORE`ステートメントのテーブル作成パフォーマンスを向上 [＃48301](https://github.com/pingcap/tidb/issues/48301) @ [Leavrth](https://github.com/Leavrth)
        -   EBS ベースのスナップショット バックアップとTiDB Lightningインポート間の互換性の問題を解決[＃46850](https://github.com/pingcap/tidb/issues/46850) @ [YuJuncen](https://github.com/YuJuncen)
        -   リージョンリーダーシップの移行が発生すると、PITR ログバックアップの進行のレイテンシーが長くなるという問題を軽減します[＃13638](https://github.com/tikv/tikv/issues/13638) @ [YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   ダウンストリームがKafkaの場合、トピック式では`schema`オプションとして指定でき、トピック名を直接指定できます[＃9763](https://github.com/pingcap/tiflow/issues/9763) @ [3AceShowHand](https://github.com/3AceShowHand)

## バグ修正 {#bug-fixes}

-   TiDB

    -   短時間に多数の`CREATE TABLE`文が実行されると、TiDB が同時に新しい統計メタデータを作成しない可能性があり、後続のクエリ推定で正確な行数情報を取得できない問題を修正しました[＃36004](https://github.com/pingcap/tidb/issues/36004) [＃38189](https://github.com/pingcap/tidb/issues/38189) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   監査ログ用のEnterpriseプラグインを使用すると、TiDBサーバーが大量のリソースを消費する可能性がある問題を修正[＃49273](https://github.com/pingcap/tidb/issues/49273) @ [lcwangchao](https://github.com/lcwangchao)
    -   `ErrLoadDataInvalidURI`の誤ったエラーメッセージを修正 (無効な S3 URI エラー) [＃48164](https://github.com/pingcap/tidb/issues/48164) @ [lance6716](https://github.com/lance6716)
    -   `tidb_server_memory_limit` による長期メモリ圧迫により TiDB の CPU 使用率が上昇する問題を修正 [＃48741](https://github.com/pingcap/tidb/issues/48741) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   共通テーブル式 (CTE) を含むクエリがメモリ制限を超えたときに予期せず停止する問題を修正[＃49096](https://github.com/pingcap/tidb/issues/49096) @ [AilinKid](https://github.com/AilinKid)
    -   同じクエリプランで、場合によってはの異なる`PLAN_DIGEST`値が発生する問題を修正しました [＃47634](https://github.com/pingcap/tidb/issues/47634) @ [King-Dylan](https://github.com/King-Dylan)
    -   CTE を含むクエリが、 `tidb_max_chunk_size`小さい値に設定されている場合に`runtime error: index out of range [32] with length 32`報告する問題を修正しました。 [＃48808](https://github.com/pingcap/tidb/issues/48808) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   正常なシャットダウン中に TiDBサーバーがpanic可能性がある問題を修正[＃36793](https://github.com/pingcap/tidb/issues/36793) @ [bb7133](https://github.com/bb7133)
    -   TiDB の初期バージョンからエクスポートされた統計をインポートするときに統計データエラーが発生する可能性がある問題を修正しました。 [＃42931](https://github.com/pingcap/tidb/issues/42931) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   Golang の暗黙的な変換アルゴリズムによって発生する統計情報の構築における過剰な統計エラーの問題を修正しました [＃49801](https://github.com/pingcap/tidb/issues/49801) @ [qw4990](https://github.com/qw4990)
    -   特定のシナリオでオプティマイザがTiFlash選択パスを DUAL テーブルに誤って変換する問題を修正[＃49285](https://github.com/pingcap/tidb/issues/49285) @ [AilinKid](https://github.com/AilinKid)
    -   `ENUM`または`SET`種類の無効な値を解析すると、SQL ステートメント エラーが直接発生する問題を修正しました。 [＃49487](https://github.com/pingcap/tidb/issues/49487) @ [winoros](https://github.com/winoros)
    -   `WITH RECURSIVE` CTE を含む`UPDATE`または`DELETE`ステートメントで誤った結果が生成される可能性がある問題を修正しました[＃48969](https://github.com/pingcap/tidb/issues/48969) @ [winoros](https://github.com/winoros)
    -   データの末尾にスペースが含まれている場合に`LIKE`で`_`ワイルドカードを使用すると、クエリ結果が不正確になる可能性がある問題を修正しました[＃48983](https://github.com/pingcap/tidb/issues/48983) @ [time-and-fate](https://github.com/time-and-fate)
    -   IndexHashJoin 演算子を含むクエリがメモリが`tidb_mem_quota_query` を超えると停止する問題を修正しました [＃49033](https://github.com/pingcap/tidb/issues/49033) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   ネストされた`UNION`クエリで`LIMIT`と`OPRDERBY`無効になる可能性がある問題を修正しました [＃49377](https://github.com/pingcap/tidb/issues/49377) @ [AilinKid](https://github.com/AilinKid)
    -   非厳密モード（ `sql_mode = ''` ）で、 `INSERT`実行中に切り捨てが行われても、 [天菜まお](https://github.com/tiancaiamao)でエラーが報告される問題を修正しました。 [＃49369](https://github.com/pingcap/tidb/issues/49369)
    -   TiDBがパニックを起こしてエラーを報告する問題を修正`invalid memory address or nil pointer dereference` [＃42739](https://github.com/pingcap/tidb/issues/42739) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   CTEクエリが再試行プロセス中にエラー`type assertion for CTEStorageMap failed`を報告する可能性がある問題を修正しました [＃46522](https://github.com/pingcap/tidb/issues/46522) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   一部のタイムゾーンで夏時間が正しく表示されない問題を修正 [＃49586](https://github.com/pingcap/tidb/issues/49586) @ [overvenus](https://github.com/overvenus)
    -   依存関係のある 2 つの DDL タスクの完了時間がと誤って順序付けられる問題を修正しました。 [＃49498](https://github.com/pingcap/tidb/issues/49498) @ [tangenta](https://github.com/tangenta)

-   TiKV

    -   破損したSSTファイルが他のTiKVノードに広がる可能性がある問題を修正 [＃15986](https://github.com/tikv/tikv/issues/15986) @ [Connor1996](https://github.com/Connor1996)
    -   大規模なトランザクションを追跡するときに、古い読み取りの解決済み TS が TiKV OOM 問題を引き起こす可能性がある問題を修正しました [＃14864](https://github.com/tikv/tikv/issues/14864) @ [overvenus](https://github.com/overvenus)
    -   TiKVがraft log を追加できないため`ServerIsBusy`エラーを報告する問題を修正しました。 [＃15800](https://github.com/tikv/tikv/issues/15800) @ [tonyxuqqi](https://github.com/tonyxuqqi)

-   PD

    -   SQLの配置ルールで設定された`location-labels`特定の条件下で期待どおりにスケジュールされない問題を修正[＃6637](https://github.com/tikv/pd/issues/6637) @ [rleungx](https://github.com/rleungx)
    -   レプリカ数が要件を満たしていない場合に孤立ピアが削除される問題を修正しました [＃7584](https://github.com/tikv/pd/issues/7584) @ [bufferflies](https://github.com/bufferflies)

-   TiFlash

    -   `FLASHBACK DATABASE` を実行した後もTiFlashレプリカのデータがガベージコレクションされる問題を修正しました [＃8450](https://github.com/pingcap/tiflash/issues/8450) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   クエリ中にTiFlash がメモリ制限に遭遇するとメモリリークが発生する問題を修正しました。 [＃8447](https://github.com/pingcap/tiflash/issues/8447) @ [JinheLin](https://github.com/JinheLin)
    -   Grafana の一部のパネルの最大パーセンタイル時間の表示が誤っていた問題を修正 [＃8076](https://github.com/pingcap/tiflash/issues/8076) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   クエリの低速化によりメモリ使用量が大幅に増加する問題を修正 [＃8564](https://github.com/pingcap/tiflash/issues/8564) @ [JinheLin](https://github.com/JinheLin)

-   ツール

    -   Backup & Restore (BR)

        -   タスク初期化中にPDへの接続に失敗すると、ログバックアップタスクは開始できるが正常に動作しない問題を修正[＃16056](https://github.com/tikv/tikv/issues/16056) @ [YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   TiCDC が下流の MySQL にデータを複製するときに`checkpoint-ts`スタックする可能性がある問題を修正しました [＃10334](https://github.com/pingcap/tiflow/issues/10334) @ [zhangjinpeng87](https://github.com/zhangjinpeng87)
        -   `kv-client`初期化中に発生する可能性のあるデータ競合問題を修正 [＃10095](https://github.com/pingcap/tiflow/issues/10095) @ [3AceShowHand](https://github.com/3AceShowHand)
