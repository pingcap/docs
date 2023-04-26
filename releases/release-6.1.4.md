---
title: TiDB 6.1.4 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.1.4.
---

# TiDB 6.1.4 リリースノート {#tidb-6-1-4-release-notes}

発売日：2023年2月8日

TiDB バージョン: 6.1.4

クイック アクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [インストール パッケージ](https://www.pingcap.com/download/?version=v6.1.4#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   正確性の問題が発生する可能性があるため、分割されたテーブルの列の型の変更はサポートされなくなりました[#40620](https://github.com/pingcap/tidb/issues/40620) @ [ミヨンス](https://github.com/mjonss)

## 改良点 {#improvements}

-   TiFlash

    -   高い更新スループット ワークロードの下で、 TiFlashインスタンスの IOPS を最大 95% 削減し、書き込み増幅を最大 65% 削減します[#6460](https://github.com/pingcap/tiflash/issues/6460) @ [フロービーハッピー](https://github.com/flowbehappy)

-   ツール

    -   TiCDC

        -   DML バッチ操作モードを追加して、SQL ステートメントがバッチで生成される場合のスループットを向上させます[#7653](https://github.com/pingcap/tiflow/issues/7653) @ [アスドンメン](https://github.com/asddongmen)
        -   GCS または Azure 互換のオブジェクトstorageへの REDO ログの保存をサポート[#7987](https://github.com/pingcap/tiflow/issues/7987) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)

    -   TiDB Lightning

        -   事前チェック項目`clusterResourceCheckItem`と`emptyRegionCheckItem`の重大度を`Critical`から`Warning` [#37654](https://github.com/pingcap/tidb/issues/37654) @ [ニューベル](https://github.com/niubell)に変更します

## バグの修正 {#bug-fixes}

-   TiDB

    -   テーブルを作成するときに、デフォルト値と列のタイプが一致せず、自動的に修正されない問題を修正します[#34881](https://github.com/pingcap/tidb/issues/34881) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger) @ [ミヨンス](https://github.com/mjonss)
    -   `LazyTxn.LockKeys`関数[#40355](https://github.com/pingcap/tidb/issues/40355) @ [ヒューシャープ](https://github.com/HuSharp)のデータ競合の問題を修正
    -   `INSERT`つまたは`REPLACE`のステートメントが長いセッション接続でpanicになる可能性がある問題を修正します[#40351](https://github.com/pingcap/tidb/issues/40351) @ [ファンレンホー](https://github.com/fanrenhoo)
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC [#39447](https://github.com/pingcap/tidb/issues/39447) @ [ジグアン](https://github.com/zyguan)が原因でエラーが返される可能性がある問題を修正します。
    -   ポイント取得クエリ[#39928](https://github.com/pingcap/tidb/issues/39928) @ [ジグアン](https://github.com/zyguan)で[`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)構成アイテムが有効にならない問題を修正
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`テーブルをクエリすると間違った結果[#37436](https://github.com/pingcap/tidb/issues/37436) @ [ジムラーラ](https://github.com/zimulala)が返される問題を修正します。
    -   一部のパターンで`IN`および`NOT IN`サブクエリが`Can't find column`エラー[#37032](https://github.com/pingcap/tidb/issues/37032) @ [アイリンキッド](https://github.com/AilinKid) @ [ランス6716](https://github.com/lance6716)を報告する問題を修正します。

<!---->

-   PD

    -   PD がリージョン[#5786](https://github.com/tikv/pd/issues/5786) @ [フンドゥンDM](https://github.com/HunDunDM)に複数の学習者を予期せず追加する可能性がある問題を修正します

<!---->

-   TiKV

    -   `cgroup`と`mountinfo`レコードが複数ある場合に Gitpod で TiDB の起動に失敗する問題を修正[#13660](https://github.com/tikv/tikv/issues/13660) @ [タボキー](https://github.com/tabokie)
    -   `reset-to-version`コマンド[#13829](https://github.com/tikv/tikv/issues/13829) @ [タボキー](https://github.com/tabokie)を実行すると tikv-ctl が予期せず終了する問題を修正
    -   TiKV が誤って`PessimisticLockNotFound`エラー[#13425](https://github.com/tikv/tikv/issues/13425) @ [スティックナーフ](https://github.com/sticnarf)を報告する問題を修正
    -   1 回の書き込みのサイズが 2 GiB [#13848](https://github.com/tikv/tikv/issues/13848) @ [ユジュンセン](https://github.com/YuJuncen)を超えると、TiKV がpanicことがある問題を修正します。
    -   悲観的DML [#14038](https://github.com/tikv/tikv/issues/14038) @ [みょんけみんた](https://github.com/MyonKeminta)が失敗した後の DML の実行中に、TiDB と TiKV 間のネットワーク障害によって引き起こされたデータの不整合の問題を修正します。
    -   新しい照合順序が有効になっていない場合、 `LIKE`演算子の`_`非 ASCII 文字と一致しないという問題を修正します[#13769](https://github.com/tikv/tikv/issues/13769) @ [ヤンケアオ](https://github.com/YangKeao) @ [tonyxuqqi](https://github.com/tonyxuqqi)

-   TiFlash

    -   TiFlashグローバル ロックが長時間ブロックされることがある問題を修正[#6418](https://github.com/pingcap/tiflash/issues/6418) @ [シーライズ](https://github.com/SeaRise)
    -   高スループットの書き込みで OOM [#6407](https://github.com/pingcap/tiflash/issues/6407) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)が発生する問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンサイズ[#36053](https://github.com/pingcap/tidb/issues/36053) @ [ユジュンセン](https://github.com/YuJuncen)の取得に失敗して復元が中断される問題を修正
        -   BR が`backupmeta`ファイル[#40878](https://github.com/pingcap/tidb/issues/40878) @ [MoCuishle28](https://github.com/MoCuishle28)をデバッグするときにpanicを引き起こす問題を修正します。

    -   TiCDC

        -   TiCDC が過度に多数のテーブル[#8004](https://github.com/pingcap/tiflow/issues/8004) @ [アスドンメン](https://github.com/asddongmen)をレプリケートすると、チェックポイントが進められない問題を修正します
        -   `transaction_atomicity`と`protocol`構成ファイル[#7935](https://github.com/pingcap/tiflow/issues/7935) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)経由で更新できない問題を修正
        -   TiFlashのバージョンがTiCDC [#7744](https://github.com/pingcap/tiflow/issues/7744) @ [大静脈](https://github.com/overvenus)よりも新しい場合、TiCDCが誤ってエラーを報告する問題を修正
        -   TiCDC が大規模なトランザクション[#7913](https://github.com/pingcap/tiflow/issues/7913) @ [大静脈](https://github.com/overvenus)をレプリケートするときに OOM が発生する問題を修正します。
        -   TiCDC が大規模なトランザクション[#7982](https://github.com/pingcap/tiflow/issues/7982) @ [ハイラスチン](https://github.com/hi-rustin)を分割せずにデータを複製すると、コンテキストのデッドラインを超過するバグを修正
        -   `changefeed query`結果の`sasl-password`が[#7182](https://github.com/pingcap/tiflow/issues/7182) @ [ドヴィーデン](https://github.com/dveeden)でマスクされない問題を修正
        -   ユーザーがレプリケーション タスクをすばやく削除してから、同じタスク名で別のタスクを作成すると、データが失われる問題を修正します[#7657](https://github.com/pingcap/tiflow/issues/7657) @ [大静脈](https://github.com/overvenus)

    -   TiDB データ移行 (DM)

        -   `SHOW GRANTS`のダウンストリーム データベース名にワイルドカード (&quot;*&quot;) が含まれている場合、事前チェック中に DM がエラーを発生させる可能性があるバグを修正します[#7645](https://github.com/pingcap/tiflow/issues/7645) @ [ランス6716](https://github.com/lance6716)
        -   binlogクエリ イベント[#7525](https://github.com/pingcap/tiflow/issues/7525) @ [リウメンギャ94](https://github.com/liumengya94)の「COMMIT」が原因で DM が出力ログが多すぎる問題を修正します。
        -   SSL [#7941](https://github.com/pingcap/tiflow/issues/7941) @ [リウメンギャ94](https://github.com/liumengya94)に`ssl-ca`しか設定されていない場合、DM タスクの開始に失敗する問題を修正します。
        -   1つのテーブルに「更新」タイプと「非更新」タイプの両方の式フィルターを指定すると、 `UPDATE`ステートメントがすべてスキップされるバグを修正[#7831](https://github.com/pingcap/tiflow/issues/7831) @ [ランス6716](https://github.com/lance6716)
        -   テーブルに`update-old-value-expr`または`update-new-value-expr`のいずれか 1 つしか設定されていない場合、フィルター ルールが有効にならないか、DM が[#7774](https://github.com/pingcap/tiflow/issues/7774) @ [ランス6716](https://github.com/lance6716)でパニックになるバグを修正します。

    -   TiDB Lightning

        -   TiDB Lightning が巨大なソース データ ファイルをインポートするときのメモリリークの問題を修正します[#39331](https://github.com/pingcap/tidb/issues/39331) @ [dsdashun](https://github.com/dsdashun)
        -   以前に失敗したインポート[#39477](https://github.com/pingcap/tidb/issues/39477) @ [dsdashun](https://github.com/dsdashun)によって残されたダーティ データをTiDB Lightningプリチェックが見つけられないという問題を修正します。
