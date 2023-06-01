---
title: TiDB 6.1.4 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.1.4.
---

# TiDB 6.1.4 リリースノート {#tidb-6-1-4-release-notes}

発売日：2023年2月8日

TiDB バージョン: 6.1.4

クイックアクセス: [インストールパッケージ](https://www.pingcap.com/download/?version=v6.1.4#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   潜在的な正確性の問題のため、パーティション化されたテーブルの列タイプの変更はサポートされなくなりました[むじょん](https://github.com/mjonss)

## 改善点 {#improvements}

-   TiFlash

    -   高更新スループットのワークロード[フロービハッピー](https://github.com/flowbehappy)の下で、 TiFlashインスタンスの IOPS を最大 95% 削減し、書き込み増幅を最大 65% 削減します。

-   ツール

    -   TiCDC

        -   DML バッチ操作モードを追加して、SQL ステートメントがバッチ[東門](https://github.com/asddongmen)で生成される場合のスループットを向上させます。
        -   GCS または Azure 互換のオブジェクトstorage[CharlesCheung96](https://github.com/CharlesCheung96)への REDO ログの保存のサポート

    -   TiDB Lightning

        -   事前チェック項目`clusterResourceCheckItem`と`emptyRegionCheckItem`の重大度を`Critical`から`Warning` [ニューベル](https://github.com/niubell)に変更します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   テーブルを作成するときに、デフォルト値と列の型が一致せず、自動的に修正されない問題を修正します[むじょん](https://github.com/mjonss)
    -   `LazyTxn.LockKeys`関数[ヒューシャープ](https://github.com/HuSharp)のデータ競合の問題を修正
    -   長いセッション接続[ファンレンフー](https://github.com/fanrenhoo)で`INSERT`または`REPLACE`ステートメントがpanic可能性がある問題を修正
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC [ジグアン](https://github.com/zyguan)が原因でエラーが返される場合がある問題を修正
    -   ポイント取得クエリ[`pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)が有効にならない問題を修正
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`テーブルをクエリすると間違った結果[ジムララ](https://github.com/zimulala)が返される問題を修正します。
    -   一部のパターンの`IN`および`NOT IN`サブクエリで`Can't find column`エラー[ランス6716](https://github.com/lance6716)が報告される問題を修正します。

<!---->

-   PD

    -   PD が予期せず複数の学習者をリージョン[フンドゥンDM](https://github.com/HunDunDM)に追加する可能性がある問題を修正

<!---->

-   TiKV

    -   複数の`cgroup`および`mountinfo`レコード[タボキー](https://github.com/tabokie)がある場合、Gitpod で TiDB が起動できない問題を修正
    -   `reset-to-version`コマンド[タボキー](https://github.com/tabokie)を実行すると tikv-ctl が予期せず終了する問題を修正
    -   TiKV が誤って`PessimisticLockNotFound`エラー[スティックナーフ](https://github.com/sticnarf)を報告する問題を修正
    -   1 回の書き込みサイズが 2 GiB [ユジュンセン](https://github.com/YuJuncen)を超えると TiKV がpanicになる可能性がある問題を修正
    -   悲観的DML [ミョンケミンタ](https://github.com/MyonKeminta)が失敗した後の DML の実行中に、TiDB と TiKV の間のネットワーク障害によって引き起こされるデータの不整合の問題を修正しました。
    -   新しい照合順序が有効になっていない場合、 `LIKE`演算子の`_`非 ASCII 文字と一致できない問題を修正[トニーシュクキ](https://github.com/tonyxuqqi)

-   TiFlash

    -   TiFlashグローバル ロックが時折長時間ブロックされる問題を修正[シーライズ](https://github.com/SeaRise)
    -   高スループットの書き込みにより OOM [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)が発生する問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンサイズ[ユジュンセン](https://github.com/YuJuncen)の取得に失敗して復元が中断される問題を修正
        -   BR が`backupmeta` file [モクイシュル28](https://github.com/MoCuishle28)をデバッグするときにpanicを引き起こす問題を修正

    -   TiCDC

        -   TiCDC が過度に多数のテーブル[東門](https://github.com/asddongmen)をレプリケートするとチェックポイントが進められない問題を修正
        -   設定ファイル[CharlesCheung96](https://github.com/CharlesCheung96)から`transaction_atomicity`と`protocol`を更新できない問題を修正
        -   TiFlashのバージョンが TiCDC [オーバーヴィーナス](https://github.com/overvenus)のバージョンより新しい場合、TiCDC が誤ってエラーを報告する問題を修正
        -   TiCDC が大規模なトランザクション[オーバーヴィーナス](https://github.com/overvenus)をレプリケートするときに OOM が発生する問題を修正
        -   TiCDC が大規模なトランザクション[こんにちはラスティン](https://github.com/hi-rustin)を分割せずにデータをレプリケートするとコンテキスト期限を超過するバグを修正
        -   `changefeed query`結果のうち`sasl-password`マスクされない問題を修正[ドヴィーデン](https://github.com/dveeden)
        -   ユーザーがレプリケーション タスクをすぐに削除し、同じタスク名[オーバーヴィーナス](https://github.com/overvenus)で別のタスクを作成するとデータが失われる問題を修正します。

    -   TiDB データ移行 (DM)

        -   `SHOW GRANTS`の下流データベース名にワイルドカード (&quot;*&quot;) [ランス6716](https://github.com/lance6716)が含まれている場合、DM が事前チェック中にエラーを引き起こす可能性があるバグを修正
        -   binlogクエリ イベント[リウメンギャ94](https://github.com/liumengya94)の「COMMIT」が原因で DM が大量のログを出力問題を修正します。
        -   SSL [リウメンギャ94](https://github.com/liumengya94)に`ssl-ca`つだけが構成されている場合に DM タスクの開始に失敗する問題を修正
        -   1つのテーブルに「更新」タイプと「非更新」タイプの両方の式フィルタを指定した場合、 `UPDATE`ステートメントがすべてスキップされるバグを修正[ランス6716](https://github.com/lance6716)
        -   テーブルに`update-old-value-expr`または`update-new-value-expr`のいずれか 1 つだけが設定されている場合、フィルター ルールが有効にならない、または DM パニック[ランス6716](https://github.com/lance6716)が発生するバグを修正

    -   TiDB Lightning

        -   TiDB Lightning が巨大なソース データ ファイル[dsダシュン](https://github.com/dsdashun)をインポートするときのメモリリークの問題を修正
        -   TiDB Lightning事前チェックが、以前に失敗したインポート[dsダシュン](https://github.com/dsdashun)によって残されたダーティ データを見つけられない問題を修正
