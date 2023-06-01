---
title: TiDB 6.1.4 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.1.4.
---

# TiDB 6.1.4 リリースノート {#tidb-6-1-4-release-notes}

発売日：2023年2月8日

TiDB バージョン: 6.1.4

クイックアクセス: [<a href="https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb">クイックスタート</a>](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [<a href="https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup">本番展開</a>](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [<a href="https://www.pingcap.com/download/?version=v6.1.4#version-list">インストールパッケージ</a>](https://www.pingcap.com/download/?version=v6.1.4#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   潜在的な正確性の問題のため、パーティション化されたテーブルの列タイプの変更はサポートされなくなりました[<a href="https://github.com/pingcap/tidb/issues/40620">#40620</a>](https://github.com/pingcap/tidb/issues/40620) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)

## 改善点 {#improvements}

-   TiFlash

    -   高更新スループットのワークロード[<a href="https://github.com/pingcap/tiflash/issues/6460">#6460</a>](https://github.com/pingcap/tiflash/issues/6460) @ [<a href="https://github.com/flowbehappy">フロービハッピー</a>](https://github.com/flowbehappy)の下で、 TiFlashインスタンスの IOPS を最大 95% 削減し、書き込み増幅を最大 65% 削減します。

-   ツール

    -   TiCDC

        -   DML バッチ操作モードを追加して、SQL ステートメントがバッチ[<a href="https://github.com/pingcap/tiflow/issues/7653">#7653</a>](https://github.com/pingcap/tiflow/issues/7653) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)で生成される場合のスループットを向上させます。
        -   GCS または Azure 互換のオブジェクトstorage[<a href="https://github.com/pingcap/tiflow/issues/7987">#7987</a>](https://github.com/pingcap/tiflow/issues/7987) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)への REDO ログの保存のサポート

    -   TiDB Lightning

        -   事前チェック項目`clusterResourceCheckItem`と`emptyRegionCheckItem`の重大度を`Critical`から`Warning` [<a href="https://github.com/pingcap/tidb/issues/37654">#37654</a>](https://github.com/pingcap/tidb/issues/37654) @ [<a href="https://github.com/niubell">ニューベル</a>](https://github.com/niubell)に変更します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   テーブルを作成するときに、デフォルト値と列の型が一致せず、自動的に修正されない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/34881">#34881</a>](https://github.com/pingcap/tidb/issues/34881) @ [<a href="https://github.com/Lloyd-Pottiger">ロイド・ポティガー</a>](https://github.com/Lloyd-Pottiger) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)
    -   `LazyTxn.LockKeys`関数[<a href="https://github.com/pingcap/tidb/issues/40355">#40355</a>](https://github.com/pingcap/tidb/issues/40355) @ [<a href="https://github.com/HuSharp">ヒューシャープ</a>](https://github.com/HuSharp)のデータ競合の問題を修正
    -   長いセッション接続[<a href="https://github.com/pingcap/tidb/issues/40351">#40351</a>](https://github.com/pingcap/tidb/issues/40351) @ [<a href="https://github.com/fanrenhoo">ファンレンフー</a>](https://github.com/fanrenhoo)で`INSERT`または`REPLACE`ステートメントがpanic可能性がある問題を修正
    -   「カーソル読み取り」メソッドを使用してデータを読み取ると、GC [<a href="https://github.com/pingcap/tidb/issues/39447">#39447</a>](https://github.com/pingcap/tidb/issues/39447) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)が原因でエラーが返される場合がある問題を修正
    -   ポイント取得クエリ[<a href="https://github.com/pingcap/tidb/issues/39928">#39928</a>](https://github.com/pingcap/tidb/issues/39928) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)で設定項目[<a href="/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600">`pessimistic-auto-commit`</a>](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)が有効にならない問題を修正
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`テーブルをクエリすると間違った結果[<a href="https://github.com/pingcap/tidb/issues/37436">#37436</a>](https://github.com/pingcap/tidb/issues/37436) @ [<a href="https://github.com/zimulala">ジムララ</a>](https://github.com/zimulala)が返される問題を修正します。
    -   一部のパターンの`IN`および`NOT IN`サブクエリで`Can't find column`エラー[<a href="https://github.com/pingcap/tidb/issues/37032">#37032</a>](https://github.com/pingcap/tidb/issues/37032) @ [<a href="https://github.com/AilinKid">アイリンキッド</a>](https://github.com/AilinKid) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)が報告される問題を修正します。

<!---->

-   PD

    -   PD が予期せず複数の学習者をリージョン[<a href="https://github.com/tikv/pd/issues/5786">#5786</a>](https://github.com/tikv/pd/issues/5786) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)に追加する可能性がある問題を修正

<!---->

-   TiKV

    -   複数の`cgroup`および`mountinfo`レコード[<a href="https://github.com/tikv/tikv/issues/13660">#13660</a>](https://github.com/tikv/tikv/issues/13660) @ [<a href="https://github.com/tabokie">タボキー</a>](https://github.com/tabokie)がある場合、Gitpod で TiDB が起動できない問題を修正
    -   `reset-to-version`コマンド[<a href="https://github.com/tikv/tikv/issues/13829">#13829</a>](https://github.com/tikv/tikv/issues/13829) @ [<a href="https://github.com/tabokie">タボキー</a>](https://github.com/tabokie)を実行すると tikv-ctl が予期せず終了する問題を修正
    -   TiKV が誤って`PessimisticLockNotFound`エラー[<a href="https://github.com/tikv/tikv/issues/13425">#13425</a>](https://github.com/tikv/tikv/issues/13425) @ [<a href="https://github.com/sticnarf">スティックナーフ</a>](https://github.com/sticnarf)を報告する問題を修正
    -   1 回の書き込みサイズが 2 GiB [<a href="https://github.com/tikv/tikv/issues/13848">#13848</a>](https://github.com/tikv/tikv/issues/13848) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)を超えると TiKV がpanicになる可能性がある問題を修正
    -   悲観的DML [<a href="https://github.com/tikv/tikv/issues/14038">#14038</a>](https://github.com/tikv/tikv/issues/14038) @ [<a href="https://github.com/MyonKeminta">ミョンケミンタ</a>](https://github.com/MyonKeminta)が失敗した後の DML の実行中に、TiDB と TiKV の間のネットワーク障害によって引き起こされるデータの不整合の問題を修正しました。
    -   新しい照合順序が有効になっていない場合、 `LIKE`演算子の`_`非 ASCII 文字と一致できない問題を修正[<a href="https://github.com/tikv/tikv/issues/13769">#13769</a>](https://github.com/tikv/tikv/issues/13769) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao) @ [<a href="https://github.com/tonyxuqqi">トニーシュクキ</a>](https://github.com/tonyxuqqi)

-   TiFlash

    -   TiFlashグローバル ロックが時折長時間ブロックされる問題を修正[<a href="https://github.com/pingcap/tiflash/issues/6418">#6418</a>](https://github.com/pingcap/tiflash/issues/6418) @ [<a href="https://github.com/SeaRise">シーライズ</a>](https://github.com/SeaRise)
    -   高スループットの書き込みにより OOM [<a href="https://github.com/pingcap/tiflash/issues/6407">#6407</a>](https://github.com/pingcap/tiflash/issues/6407) @ [<a href="https://github.com/JaySon-Huang">ジェイ・ソン・ファン</a>](https://github.com/JaySon-Huang)が発生する問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンサイズ[<a href="https://github.com/pingcap/tidb/issues/36053">#36053</a>](https://github.com/pingcap/tidb/issues/36053) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)の取得に失敗して復元が中断される問題を修正
        -   BR が`backupmeta` file [<a href="https://github.com/pingcap/tidb/issues/40878">#40878</a>](https://github.com/pingcap/tidb/issues/40878) @ [<a href="https://github.com/MoCuishle28">モクイシュル28</a>](https://github.com/MoCuishle28)をデバッグするときにpanicを引き起こす問題を修正

    -   TiCDC

        -   TiCDC が過度に多数のテーブル[<a href="https://github.com/pingcap/tiflow/issues/8004">#8004</a>](https://github.com/pingcap/tiflow/issues/8004) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)をレプリケートするとチェックポイントが進められない問題を修正
        -   設定ファイル[<a href="https://github.com/pingcap/tiflow/issues/7935">#7935</a>](https://github.com/pingcap/tiflow/issues/7935) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)から`transaction_atomicity`と`protocol`を更新できない問題を修正
        -   TiFlashのバージョンが TiCDC [<a href="https://github.com/pingcap/tiflow/issues/7744">#7744</a>](https://github.com/pingcap/tiflow/issues/7744) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)のバージョンより新しい場合、TiCDC が誤ってエラーを報告する問題を修正
        -   TiCDC が大規模なトランザクション[<a href="https://github.com/pingcap/tiflow/issues/7913">#7913</a>](https://github.com/pingcap/tiflow/issues/7913) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)をレプリケートするときに OOM が発生する問題を修正
        -   TiCDC が大規模なトランザクション[<a href="https://github.com/pingcap/tiflow/issues/7982">#7982</a>](https://github.com/pingcap/tiflow/issues/7982) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)を分割せずにデータをレプリケートするとコンテキスト期限を超過するバグを修正
        -   `changefeed query`結果のうち`sasl-password`マスクされない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/7182">#7182</a>](https://github.com/pingcap/tiflow/issues/7182) @ [<a href="https://github.com/dveeden">ドヴィーデン</a>](https://github.com/dveeden)
        -   ユーザーがレプリケーション タスクをすぐに削除し、同じタスク名[<a href="https://github.com/pingcap/tiflow/issues/7657">#7657</a>](https://github.com/pingcap/tiflow/issues/7657) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)で別のタスクを作成するとデータが失われる問題を修正します。

    -   TiDB データ移行 (DM)

        -   `SHOW GRANTS`の下流データベース名にワイルドカード (&quot;*&quot;) [<a href="https://github.com/pingcap/tiflow/issues/7645">#7645</a>](https://github.com/pingcap/tiflow/issues/7645) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)が含まれている場合、DM が事前チェック中にエラーを引き起こす可能性があるバグを修正
        -   binlogクエリ イベント[<a href="https://github.com/pingcap/tiflow/issues/7525">#7525</a>](https://github.com/pingcap/tiflow/issues/7525) @ [<a href="https://github.com/liumengya94">リウメンギャ94</a>](https://github.com/liumengya94)の「COMMIT」が原因で DM が大量のログを出力問題を修正します。
        -   SSL [<a href="https://github.com/pingcap/tiflow/issues/7941">#7941</a>](https://github.com/pingcap/tiflow/issues/7941) @ [<a href="https://github.com/liumengya94">リウメンギャ94</a>](https://github.com/liumengya94)に`ssl-ca`つだけが構成されている場合に DM タスクの開始に失敗する問題を修正
        -   1つのテーブルに「更新」タイプと「非更新」タイプの両方の式フィルタを指定した場合、 `UPDATE`ステートメントがすべてスキップされるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/7831">#7831</a>](https://github.com/pingcap/tiflow/issues/7831) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)
        -   テーブルに`update-old-value-expr`または`update-new-value-expr`のいずれか 1 つだけが設定されている場合、フィルター ルールが有効にならない、または DM パニック[<a href="https://github.com/pingcap/tiflow/issues/7774">#7774</a>](https://github.com/pingcap/tiflow/issues/7774) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)が発生するバグを修正

    -   TiDB Lightning

        -   TiDB Lightning が巨大なソース データ ファイル[<a href="https://github.com/pingcap/tidb/issues/39331">#39331</a>](https://github.com/pingcap/tidb/issues/39331) @ [<a href="https://github.com/dsdashun">dsダシュン</a>](https://github.com/dsdashun)をインポートするときのメモリリークの問題を修正
        -   TiDB Lightning事前チェックが、以前に失敗したインポート[<a href="https://github.com/pingcap/tidb/issues/39477">#39477</a>](https://github.com/pingcap/tidb/issues/39477) @ [<a href="https://github.com/dsdashun">dsダシュン</a>](https://github.com/dsdashun)によって残されたダーティ データを見つけられない問題を修正
