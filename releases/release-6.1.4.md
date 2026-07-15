---
title: TiDB 6.1.4 Release Notes
summary: TiDB 6.1.4 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 6.1.4 リリースノート {#tidb-6-1-4-release-notes}

発売日：2023年2月8日

TiDB バージョン: 6.1.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   潜在的な正確性の問題のため、パーティション化されたテーブルでの列タイプの変更はサポートされなくなりました[＃40620](https://github.com/pingcap/tidb/issues/40620) @ [mjonss](https://github.com/mjonss)

## 改善点 {#improvements}

-   TiFlash

    -   Reduce the IOPS by up to 95% and the write amplification by up to 65% for TiFlash instances under high update throughput workloads [＃6460](https://github.com/pingcap/tiflash/issues/6460) @ [flowbehappy](https://github.com/flowbehappy)

-   ツール

    -   TiCDC

        -   SQL文がバッチで生成される際のスループットを向上させるために、DMLバッチ操作モードを追加します。 [＃7653](https://github.com/pingcap/tiflow/issues/7653) @ [asddongmen](https://github.com/asddongmen)
        -   GCS または Azure 互換のオブジェクトストレージへの REDO ログの保存をサポート [＃7987](https://github.com/pingcap/tiflow/issues/7987) @ [CharlesCheung96](https://github.com/CharlesCheung96)

    -   TiDB Lightning

        -   事前チェック項目`clusterResourceCheckItem`と`emptyRegionCheckItem`の重大度を`Critical`から`Warning`に変更します[＃37654](https://github.com/pingcap/tidb/issues/37654) @ [niubell](https://github.com/niubell)

## Bug fixes {#bug-fixes}

-   TiDB

    -   テーブルを作成するときに、列のデフォルト値とタイプが一致せず、自動的に修正されない問題を修正しました[＃34881](https://github.com/pingcap/tidb/issues/34881) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) @ [mjonss](https://github.com/mjonss)
    -   `LazyTxn.LockKeys`関数のデータ競合問題を修正 [＃40355](https://github.com/pingcap/tidb/issues/40355) @ [HuSharp](https://github.com/HuSharp)
    -   長いセッション接続で`INSERT`または`REPLACE`ステートメントがpanic可能性がある問題を修正しました [＃40351](https://github.com/pingcap/tidb/issues/40351) @ [fanrenhoo](https://github.com/fanrenhoo)
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC のためにエラーが返される可能性がある問題を修正しました。 [＃39447](https://github.com/pingcap/tidb/issues/39447) @ [zyguan](https://github.com/zyguan)
    -   [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)構成項目がPointGetクエリで有効にならない問題を修正しました [＃39928](https://github.com/pingcap/tidb/issues/39928) @ [zyguan](https://github.com/zyguan)
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`テーブルをクエリすると誤った結果が返される問題を修正[＃37436](https://github.com/pingcap/tidb/issues/37436) @ [zimulala](https://github.com/zimulala)
    -   一部のパターンの`IN`と`NOT IN`サブクエリが`Can't find column`エラーを報告する問題を修正しました [＃37032](https://github.com/pingcap/tidb/issues/37032) @ [AilinKid](https://github.com/AilinKid) @ [lance6716](https://github.com/lance6716)

<!---->

-   PD

    -   PD が予期せず複数のラーナーをリージョンに追加する可能性がある問題を修正しました。 [＃5786](https://github.com/tikv/pd/issues/5786) @ [HunDunDM](https://github.com/HunDunDM)

<!---->

-   TiKV

    -   `cgroup`と`mountinfo`レコードが複数ある場合、TiDBがGitpodで起動に失敗する問題を修正しました[＃13660](https://github.com/tikv/tikv/issues/13660) @ [tabokie](https://github.com/tabokie)
    -   `reset-to-version`コマンドを実行すると tikv-ctl が予期せず終了する問題を修正しました [＃13829](https://github.com/tikv/tikv/issues/13829) @ [tabokie](https://github.com/tabokie)
    -   TiKVが誤って`PessimisticLockNotFound`エラーを報告する問題を修正 [＃13425](https://github.com/tikv/tikv/issues/13425) @ [sticnarf](https://github.com/sticnarf)
    -   1回の書き込みサイズが2 GiB を超えるとTiKVがpanicになる問題を修正 [＃13848](https://github.com/tikv/tikv/issues/13848) @ [YuJuncen](https://github.com/YuJuncen)
    -   Fix the data inconsistency issue caused by network failure between TiDB and TiKV during the execution of a DML after a failed pessimistic DML [＃14038](https://github.com/tikv/tikv/issues/14038) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   新しい照合順序が有効になっていない場合、 `LIKE`演算子の`_`非 ASCII 文字と一致しない問題を修正[＃13769](https://github.com/tikv/tikv/issues/13769) @ [YangKeao](https://github.com/YangKeao) @ [tonyxuqqi](https://github.com/tonyxuqqi)

-   TiFlash

    -   TiFlashグローバルロックが時々長時間ブロックされる問題を修正[＃6418](https://github.com/pingcap/tiflash/issues/6418) @ [SeaRise](https://github.com/SeaRise)
    -   高スループット書き込みがOOM を引き起こす問題を修正 [＃6407](https://github.com/pingcap/tiflash/issues/6407) @ [JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   Backup & Restore (BR)

        -   リージョンサイズの取得に失敗したために復元が中断される問題を修正しました [#36053](https://github.com/pingcap/tidb/issues/36053) @ [YuJuncen](https://github.com/YuJuncen)
        -   BRが`backupmeta`ファイルをデバッグするときにpanicを引き起こす問題を修正しました [＃40878](https://github.com/pingcap/tidb/issues/40878) @ [MoCuishle28](https://github.com/MoCuishle28)

    -   TiCDC

        -   TiCDC が過度に多数のテーブルを複製するとチェックポイントが進めなくなる問題を修正しました [＃8004](https://github.com/pingcap/tiflow/issues/8004) @ [asddongmen](https://github.com/asddongmen)
        -   `transaction-atomicity`と`protocol`構成ファイル経由で更新できない問題を修正 [＃7935](https://github.com/pingcap/tiflow/issues/7935) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   Fix the issue that TiCDC mistakenly reports an error when the version of TiFlash is later than that of TiCDC [＃7744](https://github.com/pingcap/tiflow/issues/7744) @ [overvenus](https://github.com/overvenus)
        -   TiCDCが大規模なトランザクションを複製するときにOOMが発生する問題を修正 [＃7913](https://github.com/pingcap/tiflow/issues/7913) @ [overvenus](https://github.com/overvenus)
        -   TiCDCが大きなトランザクションを@ [Rustin170506](https://github.com/Rustin170506)に分割せずにデータを複製するとコンテキスト期限が超過するバグを修正 [＃7982](https://github.com/pingcap/tiflow/issues/7982)
        -   `changefeed query`結果のうち`sasl-password`がマスクされない問題を修正しました [＃7182](https://github.com/pingcap/tiflow/issues/7182) @ [dveeden](https://github.com/dveeden)
        -   Fix the issue that data is lost when a user quickly deletes a replication task and then creates another one with the same task name [＃7657](https://github.com/pingcap/tiflow/issues/7657) @ [overvenus](https://github.com/overvenus)

    -   TiDB Data Migration (DM)

        -   `SHOW GRANTS`下流データベース名にワイルドカード (&quot;*&quot;) が含まれている場合に、DM が事前チェック中にエラーを発生させる可能性があるバグを修正しました[＃7645](https://github.com/pingcap/tiflow/issues/7645) @ [lance6716](https://github.com/lance6716)
        -   binlogログクエリイベントの「COMMIT」によって DM がログを過剰に出力問題を修正しました [＃7525](https://github.com/pingcap/tiflow/issues/7525) @ [liumengya94](https://github.com/liumengya94)
        -   SSL が`ssl-ca`しか設定されていない場合に DM タスクが起動に失敗する問題を修正しました [＃7941](https://github.com/pingcap/tiflow/issues/7941) @ [liumengya94](https://github.com/liumengya94)
        -   1つのテーブルに「更新」と「非更新」の両方の式フィルタが指定されている場合、すべての`UPDATE`文がスキップされるバグを修正しました[＃7831](https://github.com/pingcap/tiflow/issues/7831) @ [lance6716](https://github.com/lance6716)
        -   テーブルに`update-old-value-expr`または`update-new-value-expr`のいずれか一方のみが設定されている場合に、フィルタルールが有効にならないか、DM がパニックになるバグを修正しました。 [＃7774](https://github.com/pingcap/tiflow/issues/7774) @ [lance6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightning が巨大なソースデータファイルをインポートする際のメモリリークの問題を修正しました [＃39331](https://github.com/pingcap/tidb/issues/39331) @ [dsdashun](https://github.com/dsdashun)
        -   TiDB Lightningの事前チェックで、以前に失敗したインポートによって残されたダーティデータを見つけられない問題を修正[＃39477](https://github.com/pingcap/tidb/issues/39477) @ [dsdashun](https://github.com/dsdashun)
