---
title: TiDB 7.5.2 Release Notes
summary: TiDB 7.5.2 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.5.2 リリースノート {#tidb-7-5-2-release-notes}

発売日：2024年6月13日

TiDB バージョン: 7.5.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   RocksDB の TiKV 構成項目[`track-and-verify-wals-in-manifest`](https://docs.pingcap.com/tidb/v7.5/tikv-configuration-file#track-and-verify-wals-in-manifest-new-in-v659-v715-and-v752)追加します。これは、Write Ahead Log (WAL) の破損の可能性を調査するのに役立ちます。 [＃16549](https://github.com/tikv/tikv/issues/16549) @ [v01dstar](https://github.com/v01dstar)
-   TiDB Lightning `strict-format`または`SPLIT_FILE`を使用して CSV ファイルをインポートする場合は、行末文字を設定する必要があります[＃37338](https://github.com/pingcap/tidb/issues/37338) @ [lance6716](https://github.com/lance6716)
-   TiCDCオープンプロトコルの`sink.open.output-old-value`設定項目を追加して、更新前の値を下流に出力するかどうかを制御します。 [＃10916](https://github.com/pingcap/tiflow/issues/10916) @ [sdojjy](https://github.com/sdojjy)
-   以前のバージョンでは、 `UPDATE`変更を含むトランザクションを処理する際に、 `UPDATE`目のイベントで主キーまたは非NULLの一意インデックス値が変更されると、TiCDCはこのイベントを`DELETE`目と`INSERT`目のイベントに分割していました。v7.5.2以降では、MySQLシンクを使用する場合、 `UPDATE`の変更のトランザクション`commitTS` TiCDC `thresholdTS` （TiCDCが対応するテーブルをダウンストリームに複製し始める際にPDから取得する現在のタイムスタンプ）より小さい場合、TiCDCは`UPDATE`目のイベントを`DELETE` `INSERT`と13件目のイベントに分割します。この動作変更は、TiCDCが受信した`UPDATE`目のイベントの順序が誤っている可能性があり、分割された`DELETE`と`INSERT`目のイベントの順序が誤っている可能性があるため、ダウンストリームデータの不整合が発生する問題に対処しています。詳細については、 [ドキュメント](https://docs.pingcap.com/tidb/v7.5/ticdc-split-update-behavior#split-update-events-for-mysql-sinks) してください@ [lidezhu](https://github.com/lidezhu) [＃10918](https://github.com/pingcap/tiflow/issues/10918)

## 改善点 {#improvements}

-   TiDB

    -   `ANALYZE`文がメタデータロックをブロックする問題を最適化します [＃47475](https://github.com/pingcap/tidb/issues/47475) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `SHOW CREATE TABLE` の出力に表示される式のデフォルト値のMySQL互換性を改善しました [＃52939](https://github.com/pingcap/tidb/issues/52939) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   常に`false`である DNF 項目の処理を強化し、そのようなフィルタ条件を直接無視することで、不要なテーブル全体のスキャンを回避します[＃40997](https://github.com/pingcap/tidb/issues/40997) @ [Rustin170506](https://github.com/Rustin170506)
    -   `EXPLAIN ANALYZE` のTiFlash `TableScan`オペレータの実行プロセスの統計を最適化します [＃51727](https://github.com/pingcap/tidb/issues/51727) @ [JinheLin](https://github.com/JinheLin)
    -   MPP ロード バランシング中にリージョンのないストアを削除する [＃52313](https://github.com/pingcap/tidb/issues/52313) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   PD からリージョンを一括ロードすることをサポートし、大規模なテーブルをクエリするときに KV 範囲からリージョンへの変換プロセスを高速化します。 [＃51326](https://github.com/pingcap/tidb/issues/51326) @ [SeaRise](https://github.com/SeaRise)
    -   `Resource Control`監視ページで、各リソース グループの最大 RU 消費率を表示する新しいパネル`RU(Max)`を追加します。 [＃49318](https://github.com/pingcap/tidb/issues/49318) @ [nolouch](https://github.com/nolouch)
    -   同期ロードパフォーマンスを改善し、統計情報のロードのレイテンシーを削減します[＃52994](https://github.com/pingcap/tidb/issues/52294) @ [hawkingrei](https://github.com/hawkingrei)
    -   統計初期化の同時実行性を高めて起動を高速化します[＃52466](https://github.com/pingcap/tidb/issues/52466) [＃52102](https://github.com/pingcap/tidb/issues/52102) [＃52553](https://github.com/pingcap/tidb/issues/52553) @ [hawkingrei](https://github.com/hawkingrei)

-   TiKV

    -   コプロセッサエラーのログレベルを`warn`から`debug`に調整して、クラスタの不要なログを削減します。 [＃15881](https://github.com/tikv/tikv/issues/15881) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   CDC イベント処理のキュー時間の監視メトリックを追加して、下流の CDC イベントレイテンシー問題のトラブルシューティングを容易にします[＃16282](https://github.com/tikv/tikv/issues/16282) @ [hicqu](https://github.com/hicqu)
    -   TiKV の安定性を向上させるために、raftstore スレッドでスナップショット ファイルに対する IO 操作を実行しないようにします[＃16564](https://github.com/tikv/tikv/issues/16564) @ [Connor1996](https://github.com/Connor1996)
    -   ピアのスローログを追加し、メッセージを保存します [＃16600](https://github.com/tikv/tikv/issues/16600) @ [Connor1996](https://github.com/Connor1996)
    -   TiKVは破損したSSTファイルの存在を検出すると、破損の具体的な理由をログに記録します[＃16308](https://github.com/tikv/tikv/issues/16308) @ [overvenus](https://github.com/overvenus)
    -   不要な非同期ブロックを削除してメモリ使用量を削減する[＃16540](https://github.com/tikv/tikv/issues/16540) @ [overvenus](https://github.com/overvenus)
    -   TiKV のシャットダウン速度を加速 [＃16680](https://github.com/tikv/tikv/issues/16680) @ [LykxSassinator](https://github.com/LykxSassinator)

-   PD

    -   etcdのバージョンをv3.4.30 にアップグレードします [＃7904](https://github.com/tikv/pd/issues/7904) @ [JmPotato](https://github.com/JmPotato)
    -   1秒あたりの最大リクエストユニット（RU）の監視メトリックを追加します。 [＃7908](https://github.com/tikv/pd/issues/7908) @ [nolouch](https://github.com/nolouch)

-   TiFlash

    -   TLS を有効にした後に証明書を更新することでTiFlash がpanicする可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [windtalker](https://github.com/windtalker)

-   ツール

    -   Backup & Restore (BR)

        -   BRはデータ復旧中に空のSSTファイルをクリーンアップします[＃16005](https://github.com/tikv/tikv/issues/16005) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップの互換性テストとインデックスアクセラレーションをカバーするPITR統合テストケースを追加します。 [＃51987](https://github.com/pingcap/tidb/issues/51987) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップのマージ操作に対する許容度を向上します。比較的長いマージ操作が発生した場合、ログバックアップタスクがエラー状態に陥る可能性が低くなります。 [＃16554](https://github.com/tikv/tikv/issues/16554) @ [YuJuncen](https://github.com/YuJuncen)
        -   大規模なデータセットシナリオで`RESTORE`ステートメントのテーブル作成パフォーマンスを向上 [＃48301](https://github.com/pingcap/tidb/issues/48301) @ [Leavrth](https://github.com/Leavrth)
        -   リストアプロセス中にテーブルIDを事前割り当てすることで、テーブルIDの再利用を最大化し、リストアパフォーマンスを向上します[＃51736](https://github.com/pingcap/tidb/issues/51736) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップの開始時にアクティブなDDLジョブの無効な検証を削除します[＃52733](https://github.com/pingcap/tidb/issues/52733) @ [Leavrth](https://github.com/Leavrth)
        -   Google Cloud Storage（GCS）を外部ストレージとして使用する場合の古い互換性チェックを削除します[＃50533](https://github.com/pingcap/tidb/issues/50533) @ [lance6716](https://github.com/lance6716)
        -   DNSエラーによる失敗の再試行回数をから@ [YuJuncen](https://github.com/YuJuncen)増やす [＃53029](https://github.com/pingcap/tidb/issues/53029)

    -   TiCDC

        -   REDOログを使用してデータリカバリ中のメモリの安定性を向上させ、OOM の確率を低減します。 [＃10900](https://github.com/pingcap/tiflow/issues/10900) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   トランザクション競合シナリオにおけるデータレプリケーションの安定性が大幅に向上し、パフォーマンスが最大10倍向上します[＃10896](https://github.com/pingcap/tiflow/issues/10896) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   PDクライアント転送機能を有効にして、TiCDCとPDリーダー間のネットワーク分離中にTiCDCをより安定させます[＃10849](https://github.com/pingcap/tiflow/issues/10849) @ [asddongmen](https://github.com/asddongmen)
        -   レプリケーションタスクの初期化速度を向上 [＃11124](https://github.com/pingcap/tiflow/issues/11124) @ [asddongmen](https://github.com/asddongmen)
        -   レプリケーションタスクを非同期に初期化して、プロセッサと所有者の初期化時間を短縮します。 [＃10845](https://github.com/pingcap/tiflow/issues/10845) @ [sdojjy](https://github.com/sdojjy)
        -   Kafka クラスターのバージョンを自動的に検出し、Kafka との互換性を向上します [＃10852](https://github.com/pingcap/tiflow/issues/10852) @ [wk989898](https://github.com/wk989898)

## バグ修正 {#bug-fixes}

-   TiDB

    -   一意インデックスを追加するときに同時 DML 操作によって発生するデータ インデックスの不整合の問題を修正しました。 [＃52914](https://github.com/pingcap/tidb/issues/52914) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   パーティションテーブルに複数のスキーマ変更を含むインデックスを追加することで発生するデータインデックスの不整合の問題を修正しました。 [＃52080](https://github.com/pingcap/tidb/issues/52080) @ [tangenta](https://github.com/tangenta)
    -   複数値インデックスを追加することによって発生するデータ インデックスの不整合の問題を修正しました [＃51162](https://github.com/pingcap/tidb/issues/51162) @ [ywqzzy](https://github.com/ywqzzy)
    -   ネットワークの問題によりDDL操作が停止する問題を修正[＃47060](https://github.com/pingcap/tidb/issues/47060) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   起動時に統計情報をロードするときにTiDBがGCによるエラーを報告する可能性がある問題を修正[＃53592](https://github.com/pingcap/tidb/issues/53592) @ [you06](https://github.com/you06)
    -   TiDBが準備完了していないTiKVノードにリクエストを送信する可能性がある問題を修正 [＃50758](https://github.com/pingcap/tidb/issues/50758) @ [zyguan](https://github.com/zyguan)
    -   TiKVローリング再起動後にステイル読み取りが失われる可能性がある問題を修正 [＃52193](https://github.com/pingcap/tidb/issues/52193) @ [zyguan](https://github.com/zyguan)
    -   KV リクエストの再試行中にデータ競合が発生し、TiDB パニックが発生する可能性がある問題を修正しました。 [＃51921](https://github.com/pingcap/tidb/issues/51921) @ [zyguan](https://github.com/zyguan)
    -   インデックスデータを解析するときに TiDB がpanicする可能性がある問題を修正しました [＃47115](https://github.com/pingcap/tidb/issues/47115) @ [zyguan](https://github.com/zyguan)
    -   JOIN条件に暗黙的な型変換が含まれている場合にTiDBがpanicする可能性がある問題を修正しました [＃46556](https://github.com/pingcap/tidb/issues/46556) @ [qw4990](https://github.com/qw4990)
    -   `YEAR`型の列を範囲外の符号なし整数と比較すると誤った結果が発生する問題を修正[＃50235](https://github.com/pingcap/tidb/issues/50235) @ [qw4990](https://github.com/qw4990)
    -   `UPDATE`リスト内のサブクエリによって TiDB がpanicする可能性がある問題を修正[＃52687](https://github.com/pingcap/tidb/issues/52687) @ [winoros](https://github.com/winoros)
    -   述語の`Longlong`型のオーバーフローの問題を修正 [＃45783](https://github.com/pingcap/tidb/issues/45783) @ [hawkingrei](https://github.com/hawkingrei)
    -   クラスター化インデックスを述語として使用すると`SELECT INTO OUTFILE`が機能しない問題を修正[＃42093](https://github.com/pingcap/tidb/issues/42093) @ [qw4990](https://github.com/qw4990)
    -   TopN演算子が誤ってプッシュダウンされる可能性がある問題を修正しました [＃37986](https://github.com/pingcap/tidb/issues/37986) @ [qw4990](https://github.com/qw4990)
    -   空の投影により TiDB がpanicを引き起こす問題を修正しました [＃49109](https://github.com/pingcap/tidb/issues/49109) @ [winoros](https://github.com/winoros)
    -   インデックス プランが順序に保たれている場合に、インデックス マージによって部分的な制限が誤ってプッシュダウンされる問題を修正しました。 [＃52947](https://github.com/pingcap/tidb/issues/52947) @ [AilinKid](https://github.com/AilinKid)
    -   再帰CTE でビューの使用が機能しない問題を修正 [＃49721](https://github.com/pingcap/tidb/issues/49721) @ [hawkingrei](https://github.com/hawkingrei)
    -   列の不安定な一意のIDにより、 `UPDATE`文がエラーを返す可能性がある問題を修正しました。 [＃53236](https://github.com/pingcap/tidb/issues/53236) @ [winoros](https://github.com/winoros)
    -   常に`true` となる述語を持つ`SHOW ERRORS`文を実行すると TiDB がパニックを起こす問題を修正しました。 [＃46962](https://github.com/pingcap/tidb/issues/46962) @ [elsa0520](https://github.com/elsa0520)
    -   大規模並列処理 (MPP) で`final` AggMode と`non-final` AggMode が共存できない問題を修正しました [＃51362](https://github.com/pingcap/tidb/issues/51362) @ [AilinKid](https://github.com/AilinKid)
    -   間違った TableDual プランにより空のクエリ結果が発生する問題を修正しました [＃50051](https://github.com/pingcap/tidb/issues/50051) @ [onlyacat](https://github.com/onlyacat)
    -   `lite-init-stats`と`concurrently-init-stats`両方のを有効にした後に統計を初期化するとTiDBがpanicを起こす可能性がある問題を修正しました [＃52223](https://github.com/pingcap/tidb/issues/52223) @ [hawkingrei](https://github.com/hawkingrei)
    -   `NO_JOIN`ヒントが`CREATE BINDING` で機能しない問題を修正しました [＃52813](https://github.com/pingcap/tidb/issues/52813) @ [qw4990](https://github.com/qw4990)
    -   `ALL`関数に含まれるサブクエリが誤った結果を引き起こす可能性がある問題を修正[＃52755](https://github.com/pingcap/tidb/issues/52755) @ [hawkingrei](https://github.com/hawkingrei)
    -   `VAR_SAMP()`ウィンドウ関数として使用できない問題を修正 [＃52933](https://github.com/pingcap/tidb/issues/52933) @ [Rustin170506](https://github.com/Rustin170506)
    -   スライスの浅いコピーを使用せずに列プルーニングを行うと、TiDB がpanicする可能性がある問題を修正しました[＃52768](https://github.com/pingcap/tidb/issues/52768) @ [winoros](https://github.com/winoros)
    -   一意インデックスを追加するとTiDBがpanicする可能性がある問題を修正[＃52312](https://github.com/pingcap/tidb/issues/52312) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   初期化が完了する前に TiDBサーバーが正常とマークされる問題を修正[＃51596](https://github.com/pingcap/tidb/issues/51596) @ [shenqidebaozi](https://github.com/shenqidebaozi)
    -   `IFNULL`関数によって返される型が MySQL と一致しない問題を修正しました [＃51765](https://github.com/pingcap/tidb/issues/51765) @ [YangKeao](https://github.com/YangKeao)
    -   テーブルにクラスター化インデックスがある場合に並列`Apply`で誤った結果が生成される可能性がある問題を修正しました。 [＃51372](https://github.com/pingcap/tidb/issues/51372) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   サブクエリの`HAVING`句に相関列が含まれている場合にクエリ結果が正しくない可能性がある問題を修正しました。 [＃51107](https://github.com/pingcap/tidb/issues/51107) @ [hawkingrei](https://github.com/hawkingrei)
    -   `TIDB_HOT_REGIONS`テーブルをクエリすると、誤って`INFORMATION_SCHEMA`テーブルが返される可能性がある問題を修正しました。 [＃50810](https://github.com/pingcap/tidb/issues/50810) @ [Defined2014](https://github.com/Defined2014)
    -   統計の初期化が完了する前に自動統計収集がトリガーされる問題を修正[＃52346](https://github.com/pingcap/tidb/issues/52346) @ [Rustin170506](https://github.com/Rustin170506)
    -   AutoIDLeaderの変更により、 `AUTO_ID_CACHE=1` の場合にAUTO_INCREMENT列の値が減少する可能性がある問題を修正しました。 [＃52600](https://github.com/pingcap/tidb/issues/52600) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   共通テーブル式 (CTE) を使用して、統計情報が欠落しているパーティション テーブルにアクセスすると、クエリ結果が正しくなくなる可能性がある問題を修正しました[＃51873](https://github.com/pingcap/tidb/issues/51873) @ [qw4990](https://github.com/qw4990)
    -   TiDB Dashboardのモニタリングページにおける接続数（接続数）の計算と表示が誤っていた問題を修正しました。 [＃51889](https://github.com/pingcap/tidb/issues/51889) @ [YangKeao](https://github.com/YangKeao)
    -   外部キーを持つテーブルを復元するときに DDL 操作が停止する問題を修正しました [＃51838](https://github.com/pingcap/tidb/issues/51838) @ [YangKeao](https://github.com/YangKeao)
    -   列のデフォルト値が削除されている場合、列のデフォルト値を取得するとエラーが返される問題を修正[＃50043](https://github.com/pingcap/tidb/issues/50043) [＃51324](https://github.com/pingcap/tidb/issues/51324) @ [crazycs520](https://github.com/crazycs520)
    -   `force-init-stats` に設定されている場合に TiDB が対応するポートを listen しない問題を修正しました [＃51473](https://github.com/pingcap/tidb/issues/51473) @ [hawkingrei](https://github.com/hawkingrei)
    -   `IN()`述語に`NULL` が含まれている場合にクエリ結果が正しくない問題を修正しました [＃51560](https://github.com/pingcap/tidb/issues/51560) @ [winoros](https://github.com/winoros)
    -   TiDBの同期的な統計読み込みメカニズムが空の統計の読み込みを無期限に再試行し、 `fail to get stats version for this histogram` log を出力問題を修正しました。 [＃52657](https://github.com/pingcap/tidb/issues/52657) @ [hawkingrei](https://github.com/hawkingrei)
    -   `EXCHANGE PARTITION`外部キーを誤って処理する問題を修正 [＃51807](https://github.com/pingcap/tidb/issues/51807) @ [YangKeao](https://github.com/YangKeao)
    -   `LIMIT` `OR`型`Index Merge` にプッシュダウンされない可能性がある問題を修正しました [＃48588](https://github.com/pingcap/tidb/issues/48588) @ [AilinKid](https://github.com/AilinKid)
    -   相関サブクエリにおける TopN 演算子の誤った結果を修正 [＃52777](https://github.com/pingcap/tidb/issues/52777) @ [yibin87](https://github.com/yibin87)
    -   `CPS by type`メトリックに誤った値が表示される問題を修正しました [＃52605](https://github.com/pingcap/tidb/issues/52605) @ [nolouch](https://github.com/nolouch)
    -   特定の列の統計情報が完全にロードされていない場合に、 `EXPLAIN`ステートメントの結果に誤った列 ID が表示される可能性がある問題を修正しました[＃52207](https://github.com/pingcap/tidb/issues/52207) @ [time-and-fate](https://github.com/time-and-fate)
    -   照合の新しいフレームワークが無効になっているときに、異なる照合を含む式によってクエリがpanicになる可能性がある問題を修正しました[＃52772](https://github.com/pingcap/tidb/issues/52772) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   複数値インデックスを持つテーブルを含むSQL文を実行すると、 `Can't find a proper physical plan for this query`エラーが返される可能性がある問題を修正しました。 [＃49438](https://github.com/pingcap/tidb/issues/49438) @ [qw4990](https://github.com/qw4990)
    -   TiDBが式内のシステム変数の型を正しく変換できない問題を修正 [＃43527](https://github.com/pingcap/tidb/issues/43527) @ [Rustin170506](https://github.com/Rustin170506)
    -   `INSERT IGNORE`を実行すると、一意インデックスとデータの間に不整合が発生する可能性がある問題を修正しました。 [＃51784](https://github.com/pingcap/tidb/issues/51784) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   OOMエラー発生後に自動統計収集が停止する問題を修正[＃51993](https://github.com/pingcap/tidb/issues/51993) @ [Rustin170506](https://github.com/Rustin170506)
    -   `tidb_mem_quota_analyze`が有効になっていて、統計の更新に使用されるメモリが制限を超えると TiDB がクラッシュする可能性がある問題を修正しました。 [＃52601](https://github.com/pingcap/tidb/issues/52601) @ [hawkingrei](https://github.com/hawkingrei)
    -   複数のレベルの`max_execute_time`設定が互いに干渉する問題を修正[＃50914](https://github.com/pingcap/tidb/issues/50914) @ [jiyfhust](https://github.com/jiyfhust)
    -   単一のSQL文を使用して複数のインデックスを追加することによって発生するインデックスの不整合の問題を修正[＃51746](https://github.com/pingcap/tidb/issues/51746) @ [tangenta](https://github.com/tangenta)
    -   相関サブクエリがある場合にウィンドウ関数がpanicする可能性がある問題を修正[＃42734](https://github.com/pingcap/tidb/issues/42734) @ [Rustin170506](https://github.com/Rustin170506)
    -   `shuffleExec`予期せず終了すると TiDB がクラッシュする問題を修正[＃48230](https://github.com/pingcap/tidb/issues/48230) @ [wshwsh12](https://github.com/wshwsh12)
    -   パーティションDDLタスクをロールバックするときにステータスが停止する問題を修正しました [＃51090](https://github.com/pingcap/tidb/issues/51090) @ [jiyfhust](https://github.com/jiyfhust)
    -   `BINARY`タイプの JSON をクエリすると、場合によってはエラーが発生する可能性がある問題を修正しました[＃51547](https://github.com/pingcap/tidb/issues/51547) @ [YangKeao](https://github.com/YangKeao)
    -   分散実行フレームワーク (DXF) を有効にした後に、大きなテーブルにインデックスを追加できない問題を修正しました。 [＃52640](https://github.com/pingcap/tidb/issues/52640) @ [tangenta](https://github.com/tangenta)
    -   TTL 機能により、データ範囲の分割が不正確になり、場合によってはでデータ ホットスポットが発生する問題を修正しました。 [＃51527](https://github.com/pingcap/tidb/issues/51527) @ [lcwangchao](https://github.com/lcwangchao)
    -   主キーの型が`VARCHAR` の場合に`ALTER TABLE ... COMPACT TIFLASH REPLICA`誤って終了する可能性がある問題を修正しました [＃51810](https://github.com/pingcap/tidb/issues/51810) @ [breezewish](https://github.com/breezewish)
    -   インデックス追加中にクラスターのアップグレードによって発生するデータ インデックスの不整合の問題を修正しました。 [＃52411](https://github.com/pingcap/tidb/issues/52411) @ [tangenta](https://github.com/tangenta)
    -   TableDual で述語プッシュダウンを無効にすることで発生するパフォーマンス低下の問題を修正しました [＃50614](https://github.com/pingcap/tidb/issues/50614) @ [time-and-fate](https://github.com/time-and-fate)
    -   TiDBサーバーがHTTPインターフェース経由でラベルを追加し成功を返すが、それが有効にならない問題を修正[＃51427](https://github.com/pingcap/tidb/issues/51427) @ [you06](https://github.com/you06)
    -   取り込みモードでインデックスを追加すると、一部のコーナーケースでデータインデックスの不整合が発生する可能性がある問題を修正[＃51954](https://github.com/pingcap/tidb/issues/51954) @ [lance6716](https://github.com/lance6716)
    -   `init-stats`プロセスが TiDB をpanicに陥らせ、 `load stats`プロセスが終了する可能性がある問題を修正しました。 [＃51581](https://github.com/pingcap/tidb/issues/51581) @ [hawkingrei](https://github.com/hawkingrei)
    -   無効な設定項目が含まれている場合、設定ファイルが有効にならない問題を修正しました [＃51399](https://github.com/pingcap/tidb/issues/51399) @ [Defined2014](https://github.com/Defined2014)
    -   SQL 文に`JOIN`が含まれ、文内の`SELECT`リストに定数のみが含まれる場合に、MPP を使用してクエリを実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました。 [＃50358](https://github.com/pingcap/tidb/issues/50358) @ [yibin87](https://github.com/yibin87)
    -   `determinate`モード（ `tidb_opt_objective='determinate'` ）でクエリに述語が含まれていない場合、統計がロードされない可能性がある問題を修正しました[＃48257](https://github.com/pingcap/tidb/issues/48257) @ [time-and-fate](https://github.com/time-and-fate)
    -   特定の条件下で`SURVIVAL_PREFERENCES`属性が`SHOW CREATE PLACEMENT POLICY`ステートメントの出力に表示されない可能性がある問題を修正[＃51699](https://github.com/pingcap/tidb/issues/51699) @ [lcwangchao](https://github.com/lcwangchao)
    -   IndexJoin が Left Outer Anti Semi type のハッシュ値を計算するときに重複行を生成する問題を修正しました。 [＃52902](https://github.com/pingcap/tidb/issues/52902) @ [yibin87](https://github.com/yibin87)
    -   `TIMESTAMPADD()`関数が誤った結果を返す問題を修正[＃41052](https://github.com/pingcap/tidb/issues/41052) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `FLOAT`型から`UNSIGNED`型へのデータ変換で誤った結果が返される問題を修正[＃41736](https://github.com/pingcap/tidb/issues/41736) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `TRUNCATE()`関数の 2 番目の引数が大きな負の数の場合に誤った結果を返す問題を修正しました。 [＃52978](https://github.com/pingcap/tidb/issues/52978) @ [yibin87](https://github.com/yibin87)
    -   Grafana で重複したパネル ID により表示が異常になる可能性がある問題を修正しました [＃51556](https://github.com/pingcap/tidb/issues/51556) @ [D3Hunter](https://github.com/D3Hunter)
    -   gRPC エラーをログに記録するときに TiDB が予期せず再起動する問題を修正しました [＃51301](https://github.com/pingcap/tidb/issues/51301) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   起動時にTiDBの統計情報を読み込むとOOM が発生する可能性がある問題を修正しました。 [＃52219](https://github.com/pingcap/tidb/issues/52219) @ [hawkingrei](https://github.com/hawkingrei)
    -   テーブルが削除された後もテーブルの TTL ジョブが停止しない問題を修正[＃51540](https://github.com/pingcap/tidb/issues/51540) @ [YangKeao](https://github.com/YangKeao)

-   TiKV

    -   TiKV ログで`thread_id`値が`0x5`として誤って表示される問題を修正しました [＃16398](https://github.com/tikv/tikv/issues/16398) @ [overvenus](https://github.com/overvenus)
    -   不安定なテストケースの問題を修正し、各テストが独立した一時ディレクトリを使用するようにして、オンライン構成の変更が他のテストケースに影響しないようにします。 [＃16871](https://github.com/tikv/tikv/issues/16871) @ [glorv](https://github.com/glorv)
    -   バイナリからJSON への変換中にTiKVがpanicする可能性がある問題を修正しました [＃16616](https://github.com/tikv/tikv/issues/16616) @ [YangKeao](https://github.com/YangKeao)
    -   tikv-ctlの`raft region`コマンドの出力にリージョンステータス情報が含まれていない問題を修正しました [＃17037](https://github.com/tikv/tikv/issues/17037) @ [glorv](https://github.com/glorv)
    -   1 つの TiKV ノードで遅い`check-leader`操作により、他の TiKV ノードの`resolved-ts`正常に進まなくなる問題を修正しました。 [＃15999](https://github.com/tikv/tikv/issues/15999) @ [crazycs520](https://github.com/crazycs520)
    -   スナップショットの適用によってピアの破棄処理が中断された後、スナップショットの適用が完了しても再開されない問題を修正[＃16561](https://github.com/tikv/tikv/issues/16561) @ [tonyxuqqi](https://github.com/tonyxuqqi)
    -   `DECIMAL`型の小数点部分が場合に正しくない問題を修正しました [＃16913](https://github.com/tikv/tikv/issues/16913) @ [gengliqi](https://github.com/gengliqi)
    -   クエリ内の`CONV()`関数が数値システム変換中にオーバーフローし、TiKV panicが発生する問題を修正しました。 [＃16969](https://github.com/tikv/tikv/issues/16969) @ [gengliqi](https://github.com/gengliqi)
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [overvenus](https://github.com/overvenus)
    -   監視メトリック`tikv_unified_read_pool_thread_count`データがない場合がある問題を修正[＃16629](https://github.com/tikv/tikv/issues/16629) @ [YuJuncen](https://github.com/YuJuncen)
    -   RocksDB の非アクティブな Write Ahead Logs (WAL) によってデータが破損する可能性がある問題を修正しました[＃16705](https://github.com/tikv/tikv/issues/16705) @ [Connor1996](https://github.com/Connor1996)
    -   古いリージョンピアがGCメッセージを無視するとresolve-tsがブロックされる問題を修正しました [＃16504](https://github.com/tikv/tikv/issues/16504) @ [crazycs520](https://github.com/crazycs520)
    -   楽観的トランザクションの実行中に、他のトランザクションがそのトランザクションのロック解決操作を開始すると、トランザクションの主キーに非同期コミットまたは 1PC モードで以前にコミットされたデータがある場合、トランザクションの原子性が壊れる可能性がわずかにあるという問題を修正しました。 [＃16620](https://github.com/tikv/tikv/issues/16620) @ [MyonKeminta](https://github.com/MyonKeminta)

-   PD

    -   TiDBネットワークパーティションの障害回復後の接続panicの問題を修正しました [＃7926](https://github.com/tikv/pd/issues/7926) @ [CabinfeverB](https://github.com/CabinfeverB)
    -   オンラインデータ復旧後にスケジュールが誤って一時停止される可能性がある問題を修正 [＃8095](https://github.com/tikv/pd/issues/8095) @ [JmPotato](https://github.com/JmPotato)
    -   リソース グループを有効にした後に、CPS By Type 監視タイプが正しく表示されない問題を修正しました。 [＃52605](https://github.com/pingcap/tidb/issues/52605) @ [nolouch](https://github.com/nolouch)
    -   設定ファイル経由でログレベルを変更しても反映されない問題を修正[＃8117](https://github.com/tikv/pd/issues/8117) @ [rleungx](https://github.com/rleungx)
    -   リソースグループクエリをキャンセルするときに再試行回数が多すぎる問題を修正 [＃8217](https://github.com/tikv/pd/issues/8217) @ [nolouch](https://github.com/nolouch)
    -   `ALTER PLACEMENT POLICY`配置ポリシー を変更できない問題を修正 [＃51712](https://github.com/pingcap/tidb/issues/51712) @ [jiyfhust](https://github.com/jiyfhust) [＃52257](https://github.com/pingcap/tidb/issues/52257)
    -   配置ルールを使用しているときに、ダウンしたピアが回復しない可能性がある問題を修正しました。 [＃7808](https://github.com/tikv/pd/issues/7808) @ [rleungx](https://github.com/rleungx)
    -   PDリーダーを手動で転送すると失敗する可能性がある問題を修正しました [＃8225](https://github.com/tikv/pd/issues/8225) @ [HuSharp](https://github.com/HuSharp)
    -   書き込みホットスポットのスケジュール設定により配置ポリシーの制約が破られる可能性がある問題を修正[＃7848](https://github.com/tikv/pd/issues/7848) @ [lhy1024](https://github.com/lhy1024)
    -   リソース グループ クライアントでスロットが完全に削除されず、割り当てられたトークンの数が指定された値より少なくなる問題を修正しました。 [＃7346](https://github.com/tikv/pd/issues/7346) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   スケーリングの進行状況が正しく表示されない問題を修正[＃7726](https://github.com/tikv/pd/issues/7726) @ [CabinfeverB](https://github.com/CabinfeverB)
    -   展開された2つのデータセンター間でリーダーを切り替えるとLeaderが失敗する問題を修正[＃7992](https://github.com/tikv/pd/issues/7992) @ [TonsnakeLin](https://github.com/TonsnakeLin)
    -   PDの`Filter target`監視メトリックが散布範囲情報を提供しない問題を修正[＃8125](https://github.com/tikv/pd/issues/8125) @ [HuSharp](https://github.com/HuSharp)
    -   クエリ結果`SHOW CONFIG`に非推奨の構成項目`trace-region-flow` が含まれる問題を修正しました [＃7917](https://github.com/tikv/pd/issues/7917) @ [rleungx](https://github.com/rleungx)

-   TiFlash

    -   分散ストレージおよびコンピューティングアーキテクチャで、DDL操作で非NULL列を追加した後にクエリでNULL値が誤って返される可能性がある問題を修正しました。 [＃9084](https://github.com/pingcap/tiflash/issues/9084) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   空のパーティションを含むパーティション テーブルでクエリを実行するときに発生するクエリ タイムアウトの問題を修正しました。 [＃9024](https://github.com/pingcap/tiflash/issues/9024) @ [JinheLin](https://github.com/JinheLin)
    -   分散ストレージとコンピューティングアーキテクチャで、コンピューティングノードのプロセスが停止するとTiFlash がpanicする可能性がある問題を修正しました[＃8860](https://github.com/pingcap/tiflash/issues/8860) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   生成された列をクエリするとエラーが返される問題を修正しました [＃8787](https://github.com/pingcap/tiflash/issues/8787) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   クラスタをv6.5.0より前のバージョンからv6.5.0以降にアップグレードするときに、 TiFlashメタデータが破損してプロセスがpanicになる可能性がある問題を修正しました[＃9039](https://github.com/pingcap/tiflash/issues/9039) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   チャンクエンコード中に`ENUM`列がTiFlashを引き起こす可能性がある問題を修正しました [＃8674](https://github.com/pingcap/tiflash/issues/8674) @ [yibin87](https://github.com/yibin87)
    -   ログの誤った`local_region_num`値を修正 [＃8895](https://github.com/pingcap/tiflash/issues/8895) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   分散ストレージとコンピューティングアーキテクチャで、シャットダウン中にTiFlash がpanicになる可能性がある問題を修正しました。 [＃8837](https://github.com/pingcap/tiflash/issues/8837) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlash が高同時読み取りシナリオで一時的に誤った結果を返す可能性がある問題を修正[＃8845](https://github.com/pingcap/tiflash/issues/8845) @ [JinheLin](https://github.com/JinheLin)
    -   分散ストレージおよびコンピューティングアーキテクチャで、 TiFlashコンピューティングノードの`storage.remote.cache.capacity`構成項目の値を変更した後、Grafanaに表示されるディスク`used_size`メトリックが正しくないという問題を修正しました。 [＃8920](https://github.com/pingcap/tiflash/issues/8920) @ [JinheLin](https://github.com/JinheLin)
    -   分散ストレージおよびコンピューティングアーキテクチャで、ネットワーク分離後にクエリが永続的にブロックされる可能性がある問題を修正しました [＃8806](https://github.com/pingcap/tiflash/issues/8806) @ [JinheLin](https://github.com/JinheLin)
    -   非厳密モードの`sql_mode` で無効なデフォルト値を持つ列にデータを挿入するとTiFlash がpanicする可能性がある問題を修正しました [＃8803](https://github.com/pingcap/tiflash/issues/8803) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)

-   ツール

    -   Backup & Restore (BR)

        -   特別なイベントタイミングにより、ログバックアップでデータ損失が発生する可能性があるという稀な問題を修正しました。 [＃16739](https://github.com/tikv/tikv/issues/16739) @ [YuJuncen](https://github.com/YuJuncen)
        -   フルバックアップが失敗したときにログが多すぎる問題を修正[＃51572](https://github.com/pingcap/tidb/issues/51572) @ [Leavrth](https://github.com/Leavrth)
        -   PD接続障害により、ログバックアップアドバンサ所有者が配置されているTiDBインスタンスがpanicになる可能性がある問題を修正しました。 [＃52597](https://github.com/pingcap/tidb/issues/52597) @ [YuJuncen](https://github.com/YuJuncen)
        -   TiKV の再起動により、ログ バックアップのグローバル チェックポイントが実際のバックアップ ファイルの書き込みポイントよりも先に進められ、少量のバックアップ データが失われる可能性がある問題を修正しました[＃16809](https://github.com/tikv/tikv/issues/16809) @ [YuJuncen](https://github.com/YuJuncen)
        -   PD へのネットワーク接続が不安定な状態で一時停止中のログバックアップタスクを再開すると TiKV がpanicする可能性がある問題を修正しました [＃17020](https://github.com/tikv/tikv/issues/17020) @ [YuJuncen](https://github.com/YuJuncen)
        -   不安定なテストケース[＃52547](https://github.com/pingcap/tidb/issues/52547) @ [Leavrth](https://github.com/Leavrth)で修正する
        -   BRを使用してデータを復元する場合、または物理インポート モードでTiDB Lightningを使用してデータをインポートする場合に、PD から取得されたリージョンにLeaderがない問題を修正しました[＃51124](https://github.com/pingcap/tidb/issues/51124) [＃50501](https://github.com/pingcap/tidb/issues/50501) @ [Leavrth](https://github.com/Leavrth)
        -   フルバックアップでピアが見つからない場合に TiKV がパニックを起こす問題を修正[＃16394](https://github.com/tikv/tikv/issues/16394) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップタスクを一時停止後に削除しても、GCセーフポイントがすぐに復元されない問題を修正しました。 [＃52082](https://github.com/pingcap/tidb/issues/52082) @ [3pointer](https://github.com/3pointer)
        -   不安定なテストケース`TestClearCache` を修正 [＃50743](https://github.com/pingcap/tidb/issues/50743) @ [3pointer](https://github.com/3pointer)
        -   空の`EndKey` が原因でBR がトランザクション KV クラスターの復元に失敗する問題を修正しました [＃52574](https://github.com/pingcap/tidb/issues/52574) @ [3pointer](https://github.com/3pointer)
        -   PDリーダーの転送により、データ復元時にBRがpanicになる可能性がある問題を修正しました。 [＃53724](https://github.com/pingcap/tidb/issues/53724) @ [Leavrth](https://github.com/Leavrth)
        -   BRが`AUTO_RANDOM`列を含むユニオンクラスター化インデックスの`AUTO_RANDOM` ID割り当ての進行状況をバックアップできなかった問題を修正しました。 [＃52255](https://github.com/pingcap/tidb/issues/52255) @ [Leavrth](https://github.com/Leavrth)

    -   TiCDC

        -   PDディスクI/Oの高レイテンシーによりデータレプリケーションで深刻なレイテンシーが発生する問題を修正 [＃9054](https://github.com/pingcap/tiflow/issues/9054) @ [asddongmen](https://github.com/asddongmen)
        -   TiCDC所有者ノードを退去させるAPI（ `/api/v2/owner/resign` ）を呼び出すと、TiCDCタスクが予期せず再起動する問題を修正しました[＃10781](https://github.com/pingcap/tiflow/issues/10781) @ [sdojjy](https://github.com/sdojjy)
        -   DDL文が頻繁に実行されるシナリオで、間違ったBarrierTSが原因でデータが間違ったCSVファイルに書き込まれる問題を修正[＃10668](https://github.com/pingcap/tiflow/issues/10668) @ [lidezhu](https://github.com/lidezhu)
        -   単一行データのデータ整合性検証が有効にされた後、タイムゾーンの不一致により TiCDC が`TIMESTAMP`種類のチェックサムの検証に失敗する問題を修正[＃10573](https://github.com/pingcap/tiflow/issues/10573) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   オブジェクトストレージシンクに一時的な障害が発生した場合に、結果整合性が有効になっている変更フィードが失敗する可能性がある問題を修正しました[＃10710](https://github.com/pingcap/tiflow/issues/10710) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   `DROP PRIMARY KEY`と`DROP UNIQUE KEY`ステートメントが正しく複製されない問題を修正[＃10890](https://github.com/pingcap/tiflow/issues/10890) @ [asddongmen](https://github.com/asddongmen)
        -   テーブルレプリケーションタスクをスケジュールするときに TiCDC がパニックになる問題を修正しました [＃10613](https://github.com/pingcap/tiflow/issues/10613) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   下流の Pulsar が停止しているときに、changefeed を削除すると通常の TiCDC プロセスが停止し、他の changefeed プロセスも停止するという問題を修正しました[＃10629](https://github.com/pingcap/tiflow/issues/10629) @ [asddongmen](https://github.com/asddongmen)
        -   PDを再起動するとTiCDCノードがエラーで再起動する可能性がある問題を修正しました [＃10799](https://github.com/pingcap/tiflow/issues/10799) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   `open-protocol`の古い値部分が、実際のタイプではなく、タイプ`STRING`に応じて誤ってデフォルト値を出力する問題を修正しました。 [＃10803](https://github.com/pingcap/tiflow/issues/10803) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   `TIMEZONE`種類のデフォルト値が正しいタイムゾーンに従って設定されない問題を修正 [＃10931](https://github.com/pingcap/tiflow/issues/10931) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   TiCDC が上流に書き込まれた後に下流の`Exchange Partition ... With Validation` DDL の実行に失敗し、変更フィードが停止する問題を修正しました。 [＃10859](https://github.com/pingcap/tiflow/issues/10859) @ [hongyunyan](https://github.com/hongyunyan)
        -   KVクライアントのデータ競合によりTiCDCがpanicになる問題を修正 [＃10718](https://github.com/pingcap/tiflow/issues/10718) @ [asddongmen](https://github.com/asddongmen)
        -   アップストリームの主キーまたは一意キーを更新すると、アップストリームとダウンストリーム間でデータの不整合が発生する可能性がある問題を修正[＃10918](https://github.com/pingcap/tiflow/issues/10918) @ [lidezhu](https://github.com/lidezhu)

    -   TiDB Data Migration (DM)

        -   `go-mysql` にアップグレードして接続ブロックの問題を修正しました [＃11041](https://github.com/pingcap/tiflow/issues/11041) @ [D3Hunter](https://github.com/D3Hunter)
        -   アップストリーム主キーがバイナリ型の場合にデータが失われる問題を修正しました [＃10672](https://github.com/pingcap/tiflow/issues/10672) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   EBS BRが実行されているときにTiDB Lightningがデータのインポートに失敗する可能性がある問題を修正しました [＃49517](https://github.com/pingcap/tidb/issues/49517) @ [mittalrishabh](https://github.com/mittalrishabh)
        -   ソースファイル内の互換性のない SQL ステートメントが原因で、 TiDB Lightning がデータインポート中に`no database selected`報告する問題を修正しました。 [＃51800](https://github.com/pingcap/tidb/issues/51800) @ [lance6716](https://github.com/lance6716)
        -   PDLeaderを強制終了すると、 TiDB Lightningがデータインポート中に`invalid store ID 0`エラーを報告する問題を修正しました。 [＃50501](https://github.com/pingcap/tidb/issues/50501) @ [Leavrth](https://github.com/Leavrth)
        -   Parquet 形式の空のテーブルをインポートするときにTiDB Lightning がパニックになる問題を修正しました [＃52518](https://github.com/pingcap/tidb/issues/52518) @ [kennytm](https://github.com/kennytm)
