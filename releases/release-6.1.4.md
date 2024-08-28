---
title: TiDB 6.1.4 Release Notes
summary: TiDB 6.1.4 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 6.1.4 リリースノート {#tidb-6-1-4-release-notes}

発売日: 2023年2月8日

TiDB バージョン: 6.1.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   ティビ

    -   潜在的な正確性の問題のため、パーティション化されたテーブルでの列タイプの変更はサポートされなくなりました[＃40620](https://github.com/pingcap/tidb/issues/40620) @ [ミョンス](https://github.com/mjonss)

## 改善点 {#improvements}

-   TiFlash

    -   高い更新スループットのワークロード[＃6460](https://github.com/pingcap/tiflash/issues/6460) @ [フロービーハッピー](https://github.com/flowbehappy)で、 TiFlashインスタンスのIOPSを最大95％削減し、書き込み増幅を最大65％削減します。

-   ツール

    -   ティCDC

        -   SQL文がバッチ[＃7653](https://github.com/pingcap/tiflow/issues/7653) @ [アズドンメン](https://github.com/asddongmen)で生成される場合のスループットを向上させるためにDMLバッチ操作モードを追加します。
        -   GCS または Azure 互換のオブジェクトstorageへの REDO ログの保存をサポート[＃7987](https://github.com/pingcap/tiflow/issues/7987) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

    -   TiDB Lightning

        -   事前チェック項目`clusterResourceCheckItem`と`emptyRegionCheckItem`の重大度を`Critical`から`Warning` [＃37654](https://github.com/pingcap/tidb/issues/37654) @ [ニューベル](https://github.com/niubell)に変更します

## バグ修正 {#bug-fixes}

-   ティビ

    -   テーブルを作成するときに、列のデフォルト値とタイプが一致せず、自動的に修正されない問題を修正[＃34881](https://github.com/pingcap/tidb/issues/34881) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger) @ [ミョンス](https://github.com/mjonss)
    -   `LazyTxn.LockKeys`関数[＃40355](https://github.com/pingcap/tidb/issues/40355) @ [ヒューシャープ](https://github.com/HuSharp)のデータ競合問題を修正
    -   長いセッション接続[＃40351](https://github.com/pingcap/tidb/issues/40351) @ [ファンレンフー](https://github.com/fanrenhoo)で`INSERT`または`REPLACE`ステートメントがpanicになる可能性がある問題を修正しました
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC [＃39447](https://github.com/pingcap/tidb/issues/39447) @ [ジグアン](https://github.com/zyguan)が原因でエラーが返される可能性がある問題を修正しました。
    -   [`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)構成項目がポイント取得クエリ[＃39928](https://github.com/pingcap/tidb/issues/39928) @ [ジグアン](https://github.com/zyguan)で有効にならない問題を修正しました
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`テーブルをクエリすると誤った結果が返される問題を修正[＃37436](https://github.com/pingcap/tidb/issues/37436) @ [ジムララ](https://github.com/zimulala)
    -   一部のパターンの`IN`と`NOT IN`のサブクエリが`Can't find column`エラー[＃37032](https://github.com/pingcap/tidb/issues/37032) @ [アイリンキッド](https://github.com/AilinKid) @ [ランス6716](https://github.com/lance6716)を報告する問題を修正しました

<!---->

-   PD

    -   PD が予期せず複数の学習者をリージョン[＃5786](https://github.com/tikv/pd/issues/5786) @ [ハンダンDM](https://github.com/HunDunDM)に追加する可能性がある問題を修正しました。

<!---->

-   ティクヴ

    -   `cgroup`と`mountinfo`レコードが複数ある場合に Gitpod で TiDB が起動に失敗する問題を修正[＃13660](https://github.com/tikv/tikv/issues/13660) @ [タボキ](https://github.com/tabokie)
    -   `reset-to-version`コマンド[＃13829](https://github.com/tikv/tikv/issues/13829) @ [タボキ](https://github.com/tabokie)を実行すると tikv-ctl が予期せず終了する問題を修正
    -   TiKVが誤って`PessimisticLockNotFound`エラー[＃13425](https://github.com/tikv/tikv/issues/13425) @ [スティクナーフ](https://github.com/sticnarf)を報告する問題を修正
    -   1回の書き込みサイズが2 GiBを超えるとTiKVがpanicになる可能性がある問題を修正[＃13848](https://github.com/tikv/tikv/issues/13848) @ [ユジュンセン](https://github.com/YuJuncen)
    -   悲観的DML [＃14038](https://github.com/tikv/tikv/issues/14038) @ [ミョンケミンタ](https://github.com/MyonKeminta)が失敗した後の DML 実行中に TiDB と TiKV 間のネットワーク障害によって発生するデータ不整合の問題を修正しました。
    -   新しい照合順序が有効になっていない場合、 `LIKE`演算子の`_`非 ASCII 文字と一致しない問題を修正[＃13769](https://github.com/tikv/tikv/issues/13769) @ [ヤンケオ](https://github.com/YangKeao) @ [トニー](https://github.com/tonyxuqqi)

-   TiFlash

    -   TiFlashグローバル ロックが時々長時間ブロックされる問題を修正[＃6418](https://github.com/pingcap/tiflash/issues/6418) @ [シーライズ](https://github.com/SeaRise)
    -   高スループット書き込みがOOM [＃6407](https://github.com/pingcap/tiflash/issues/6407) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を引き起こす問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンサイズ[＃36053](https://github.com/pingcap/tidb/issues/36053) @ [ユジュンセン](https://github.com/YuJuncen)の取得に失敗したために復元が中断される問題を修正しました
        -   BRが`backupmeta`ファイル[＃40878](https://github.com/pingcap/tidb/issues/40878) @ [モクイシュル28](https://github.com/MoCuishle28)をデバッグするときにpanicを引き起こす問題を修正

    -   ティCDC

        -   TiCDC が過度に多くのテーブル[＃8004](https://github.com/pingcap/tiflow/issues/8004) @ [アズドンメン](https://github.com/asddongmen)を複製するとチェックポイントが進まない問題を修正しました。
        -   `transaction_atomicity`と`protocol`構成ファイル[＃7935](https://github.com/pingcap/tiflow/issues/7935) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)経由で更新できない問題を修正
        -   TiFlashのバージョンがTiCDC [＃7744](https://github.com/pingcap/tiflow/issues/7744) @ [金星の上](https://github.com/overvenus)より新しい場合にTiCDCが誤ってエラーを報告する問題を修正しました
        -   TiCDC が大規模なトランザクション[＃7913](https://github.com/pingcap/tiflow/issues/7913) @ [金星の上](https://github.com/overvenus)を複製するときに OOM が発生する問題を修正しました
        -   TiCDC が大規模なトランザクションを分割せずにデータを複製するとコンテキスト期限が超過するバグを修正[＃7982](https://github.com/pingcap/tiflow/issues/7982) @ [ハイラスティン](https://github.com/Rustin170506)
        -   `changefeed query`の結果のうち`sasl-password`がマスクされていない問題を修正[＃7182](https://github.com/pingcap/tiflow/issues/7182) @ [ドヴェーデン](https://github.com/dveeden)
        -   ユーザーがレプリケーションタスクをすばやく削除し、同じタスク名で別のタスクを作成するとデータが失われる問題を修正[＃7657](https://github.com/pingcap/tiflow/issues/7657) @ [金星の上](https://github.com/overvenus)

    -   TiDB データ移行 (DM)

        -   `SHOW GRANTS`のダウンストリーム データベース名にワイルドカード (&quot;*&quot;) が含まれている場合に、DM が事前チェック中にエラーを発生させる可能性があるバグを修正しました[＃7645](https://github.com/pingcap/tiflow/issues/7645) @ [ランス6716](https://github.com/lance6716)
        -   binlogログクエリイベント[＃7525](https://github.com/pingcap/tiflow/issues/7525) @ [りゅうめんぎゃ](https://github.com/liumengya94)の「COMMIT」によって DM がログを過剰に出力問題を修正しました。
        -   SSL [＃7941](https://github.com/pingcap/tiflow/issues/7941) @ [りゅうめんぎゃ](https://github.com/liumengya94)に`ssl-ca`しか設定されていない場合に DM タスクが起動しない問題を修正しました。
        -   1 つのテーブルに「更新」と「非更新」の両方のタイプの式フィルターが指定されている場合、すべての`UPDATE`ステートメントがスキップされるバグを修正しました[＃7831](https://github.com/pingcap/tiflow/issues/7831) @ [ランス6716](https://github.com/lance6716)
        -   テーブルに`update-old-value-expr`または`update-new-value-expr`のいずれか一方のみが設定されている場合に、フィルタ ルールが有効にならないか、DM が[＃7774](https://github.com/pingcap/tiflow/issues/7774) @ [ランス6716](https://github.com/lance6716)でパニックになるというバグを修正しました。

    -   TiDB Lightning

        -   TiDB Lightning が巨大なソース データ ファイル[＃39331](https://github.com/pingcap/tidb/issues/39331) @ [ダシュン](https://github.com/dsdashun)をインポートするときに発生するメモリリークの問題を修正しました
        -   TiDB Lightning の事前チェックで、以前に失敗したインポートによって残されたダーティ データを見つけられない問題を修正[＃39477](https://github.com/pingcap/tidb/issues/39477) @ [ダシュン](https://github.com/dsdashun)
