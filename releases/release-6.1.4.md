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

    -   潜在的な正確性の問題のため、パーティション化されたテーブルでの列タイプの変更はサポートされなくなりました[＃40620](https://github.com/pingcap/tidb/issues/40620) @ [ミョンス](https://github.com/mjonss)

## 改善点 {#improvements}

-   TiFlash

    -   Reduce the IOPS by up to 95% and the write amplification by up to 65% for TiFlash instances under high update throughput workloads [＃6460](https://github.com/pingcap/tiflash/issues/6460) @[フロービーハッピー](https://github.com/flowbehappy)

-   ツール

    -   TiCDC

        -   SQL文がバッチ[＃7653](https://github.com/pingcap/tiflow/issues/7653) @ [アズドンメン](https://github.com/asddongmen)で生成される際のスループットを向上させるために、DMLバッチ操作モードを追加します。
        -   GCS または Azure 互換のオブジェクトstorage[＃7987](https://github.com/pingcap/tiflow/issues/7987) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)への REDO ログの保存をサポート

    -   TiDB Lightning

        -   事前チェック項目`clusterResourceCheckItem`と`emptyRegionCheckItem`の重大度を`Critical`から`Warning`に変更します[＃37654](https://github.com/pingcap/tidb/issues/37654) @ [ニューベル](https://github.com/niubell)

## Bug fixes {#bug-fixes}

-   TiDB

    -   テーブルを作成するときに、列のデフォルト値とタイプが一致せず、自動的に修正されない問題を修正しました[＃34881](https://github.com/pingcap/tidb/issues/34881) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger) @ [mjonss](https://github.com/mjonss)
    -   `LazyTxn.LockKeys`関数[＃40355](https://github.com/pingcap/tidb/issues/40355) @ [HuSharp](https://github.com/HuSharp)のデータ競合問題を修正
    -   長いセッション接続[＃40351](https://github.com/pingcap/tidb/issues/40351) @ [ファンレンフー](https://github.com/fanrenhoo)で`INSERT`または`REPLACE`ステートメントがpanic可能性がある問題を修正しました
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC [＃39447](https://github.com/pingcap/tidb/issues/39447) @ [ジグアン](https://github.com/zyguan)のためにエラーが返される可能性がある問題を修正しました。
    -   [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)構成項目がポイント取得クエリ[＃39928](https://github.com/pingcap/tidb/issues/39928) @ [zyguan](https://github.com/zyguan)で有効にならない問題を修正しました
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`テーブルをクエリすると誤った結果が返される問題を修正[＃37436](https://github.com/pingcap/tidb/issues/37436) @ [ジムララ](https://github.com/zimulala)
    -   一部のパターンの`IN`と`NOT IN`サブクエリが`Can't find column`エラー[＃37032](https://github.com/pingcap/tidb/issues/37032) @ [アイリンキッド](https://github.com/AilinKid) @ [ランス6716](https://github.com/lance6716)を報告する問題を修正しました

<!---->

-   PD

    -   PD が予期せず複数の学習者をリージョン[＃5786](https://github.com/tikv/pd/issues/5786) @ [ハンドゥンDM](https://github.com/HunDunDM)に追加する可能性がある問題を修正しました。

<!---->

-   TiKV

    -   `cgroup`と`mountinfo`レコードが複数ある場合、TiDBがGitpodで起動に失敗する問題を修正しました[＃13660](https://github.com/tikv/tikv/issues/13660) @ [タボキ](https://github.com/tabokie)
    -   `reset-to-version`コマンド[＃13829](https://github.com/tikv/tikv/issues/13829) @ [tabokie](https://github.com/tabokie)を実行すると tikv-ctl が予期せず終了する問題を修正しました
    -   TiKVが誤って`PessimisticLockNotFound`エラー[＃13425](https://github.com/tikv/tikv/issues/13425) @ [スティクナーフ](https://github.com/sticnarf)を報告する問題を修正
    -   1回の書き込みサイズが2 GiB [＃13848](https://github.com/tikv/tikv/issues/13848) @ [ユジュンセン](https://github.com/YuJuncen)を超えるとTiKVがpanicになる問題を修正
    -   Fix the data inconsistency issue caused by network failure between TiDB and TiKV during the execution of a DML after a failed pessimistic DML [＃14038](https://github.com/tikv/tikv/issues/14038) @[ミョンケミンタ](https://github.com/MyonKeminta)
    -   新しい照合順序が有効になっていない場合、 `LIKE`演算子の`_`非 ASCII 文字と一致しない問題を修正[＃13769](https://github.com/tikv/tikv/issues/13769) @ [YangKeao](https://github.com/YangKeao) @ [トニー・シュッキ](https://github.com/tonyxuqqi)

-   TiFlash

    -   TiFlashグローバルロックが時々長時間ブロックされる問題を修正[＃6418](https://github.com/pingcap/tiflash/issues/6418) @ [シーライズ](https://github.com/SeaRise)
    -   高スループット書き込みがOOM [＃6407](https://github.com/pingcap/tiflash/issues/6407) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を引き起こす問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンサイズ[#36053](https://github.com/pingcap/tidb/issues/36053) @ [ユジュンセン](https://github.com/YuJuncen)取得に失敗したために復元が中断される問題を修正しました
        -   BRが`backupmeta`ファイル[＃40878](https://github.com/pingcap/tidb/issues/40878) @ [モクイシュル28](https://github.com/MoCuishle28)をデバッグするときにpanicを引き起こす問題を修正しました

    -   TiCDC

        -   TiCDC が過度に多数のテーブル[＃8004](https://github.com/pingcap/tiflow/issues/8004) @ [アズドンメン](https://github.com/asddongmen)を複製するとチェックポイントが進めなくなる問題を修正しました
        -   `transaction-atomicity`と`protocol`構成ファイル[＃7935](https://github.com/pingcap/tiflow/issues/7935) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)経由で更新できない問題を修正
        -   Fix the issue that TiCDC mistakenly reports an error when the version of TiFlash is later than that of TiCDC [＃7744](https://github.com/pingcap/tiflow/issues/7744) @[overvenus](https://github.com/overvenus)
        -   TiCDCが大規模なトランザクション[＃7913](https://github.com/pingcap/tiflow/issues/7913) @ [金星の上](https://github.com/overvenus)を複製するときにOOMが発生する問題を修正
        -   TiCDCが大きなトランザクション[＃7982](https://github.com/pingcap/tiflow/issues/7982)を[ハイラスティン](https://github.com/Rustin170506)に分割せずにデータを複製するとコンテキスト期限が超過するバグを修正
        -   `changefeed query`結果のうち`sasl-password`が[＃7182](https://github.com/pingcap/tiflow/issues/7182) @ [ドヴェーデン](https://github.com/dveeden)でマスクされない問題を修正しました
        -   Fix the issue that data is lost when a user quickly deletes a replication task and then creates another one with the same task name [＃7657](https://github.com/pingcap/tiflow/issues/7657) @[金星の上](https://github.com/overvenus)

    -   TiDB データ移行 (DM)

        -   `SHOW GRANTS`下流データベース名にワイルドカード (&quot;*&quot;) が含まれている場合に、DM が事前チェック中にエラーを発生させる可能性があるバグを修正しました[＃7645](https://github.com/pingcap/tiflow/issues/7645) @ [ランス6716](https://github.com/lance6716)
        -   binlogログクエリイベント[＃7525](https://github.com/pingcap/tiflow/issues/7525) @ [liumengya94](https://github.com/liumengya94)の「COMMIT」によって DM がログを過剰に出力問題を修正しました
        -   SSL [＃7941](https://github.com/pingcap/tiflow/issues/7941) @ [liumengya94](https://github.com/liumengya94)が`ssl-ca`しか設定されていない場合に DM タスクが起動に失敗する問題を修正しました
        -   1つのテーブルに「更新」と「非更新」の両方の式フィルタが指定されている場合、すべての`UPDATE`文がスキップされるバグを修正しました[＃7831](https://github.com/pingcap/tiflow/issues/7831) @ [ランス6716](https://github.com/lance6716)
        -   テーブルに`update-old-value-expr`または`update-new-value-expr`のいずれか一方のみが設定されている場合に、フィルタルールが有効にならないか、DM が[＃7774](https://github.com/pingcap/tiflow/issues/7774) @ [ランス6716](https://github.com/lance6716)でパニックになるバグを修正しました。

    -   TiDB Lightning

        -   TiDB Lightning が巨大なソースデータファイル[＃39331](https://github.com/pingcap/tidb/issues/39331) @ [dsdashun](https://github.com/dsdashun)をインポートする際のメモリリークの問題を修正しました
        -   TiDB Lightningの事前チェックで、以前に失敗したインポートによって残されたダーティデータを見つけられない問題を修正[＃39477](https://github.com/pingcap/tidb/issues/39477) @ [dsdashun](https://github.com/dsdashun)
