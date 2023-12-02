---
title: TiDB 6.1.6 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.1.6.
---

# TiDB 6.1.6 リリースノート {#tidb-6-1-6-release-notes}

発売日：2023年4月12日

TiDB バージョン: 6.1.6

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.1.6#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiCDC は、Avro [#8490](https://github.com/pingcap/tiflow/issues/8490) @ [3エースショーハンド](https://github.com/3AceShowHand)での FLOAT データの誤ったエンコードの問題を修正しました

    TiCDC クラスターを v6.1.6 以降の v6.1.x バージョンにアップグレードするときに、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレードする前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整する必要があります。 Changefeed はスキーマを正常に更新できます。そうしないと、アップグレード後に変更フィードがスキーマを更新できなくなり、エラー状態になります。

## 改善点 {#improvements}

-   TiDB

    -   プリペアドプランキャッシュ [#42125](https://github.com/pingcap/tidb/issues/42125) @ [qw4990](https://github.com/qw4990)の`BatchPointGet`の実行プランのキャッシュをサポートします。
    -   インデックス結合[#40505](https://github.com/pingcap/tidb/issues/40505) @ [イーサール](https://github.com/Yisaer)でより多くの SQL 形式をサポート

-   TiKV

    -   1 コア未満の CPU での TiKV の起動をサポート[#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @ [アンドロイドデータベース](https://github.com/andreid-db) @ [アンドロイドデータベース](https://github.com/andreid-db)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `ignore_plan_cache`ヒントが`INSERT`ステートメント[#40079](https://github.com/pingcap/tidb/issues/40079) [#39717](https://github.com/pingcap/tidb/issues/39717) @ [qw4990](https://github.com/qw4990)に対して機能しない可能性がある問題を修正
    -   `indexMerge`エラー[#41047](https://github.com/pingcap/tidb/issues/41047) [#40877](https://github.com/pingcap/tidb/issues/40877) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [ウィンドトーカー](https://github.com/windtalker)が発生した後に TiDB がpanicになる可能性がある問題を修正
    -   仮想列を持つ TopN オペレーターが誤って TiKV またはTiFlash [#41355](https://github.com/pingcap/tidb/issues/41355) @ [ドゥーシール9](https://github.com/Dousir9)にプッシュダウンすると、誤った結果が返される可能性がある問題を修正
    -   多数のリージョンがあるにもかかわらず、 `Prepare`または`Execute` [#39605](https://github.com/pingcap/tidb/issues/39605) @ [djshow832](https://github.com/djshow832)を使用して一部の仮想テーブルをクエリするときにテーブル ID をプッシュダウンできない場合の PD OOM の問題を修正します。
    -   `int_col in (decimal...)`条件[#40224](https://github.com/pingcap/tidb/issues/40224) @ [qw4990](https://github.com/qw4990)を処理するときにプラン キャッシュがフルスキャン プランをキャッシュする可能性がある問題を修正
    -   IndexMerge プランが SET タイプの列[#41273](https://github.com/pingcap/tidb/issues/41273) [#41293](https://github.com/pingcap/tidb/issues/41293) @ [時間と運命](https://github.com/time-and-fate)に不正な範囲を生成する可能性がある問題を修正します。
    -   符号なし`TINYINT` / `SMALLINT` / `INT`の値を`0` [#41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)より小さい`DECIMAL` / `FLOAT` / `DOUBLE`の値と比較するときに誤った結果が生じる可能性がある問題を修正
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルがクエリされるときに TiDBサーバーがメモリ不足になる可能性がある問題を修正します。この問題は、Grafana ダッシュボード[#33893](https://github.com/pingcap/tidb/issues/33893) @ [クレイジークス520](https://github.com/crazycs520)で遅いクエリをチェックすると発生する可能性があります。
    -   範囲パーティションで複数の`MAXVALUE`パーティション[#36329](https://github.com/pingcap/tidb/issues/36329) @ [u5サーフィン](https://github.com/u5surf)が許可される問題を修正
    -   プラン キャッシュがシャッフル演算子をキャッシュし、誤った結果[#38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990)を返す可能性がある問題を修正します。
    -   タイムゾーン内のデータ競合によりデータインデックスの不整合が発生する可能性がある問題を修正[#40710](https://github.com/pingcap/tidb/issues/40710) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `indexMerge` [#41545](https://github.com/pingcap/tidb/issues/41545) [#41605](https://github.com/pingcap/tidb/issues/41605) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [グオシャオゲ](https://github.com/guo-shaoge)で goroutine リークが発生する可能性がある問題を修正
    -   Cursor Fetch を使用し、Execute、Fetch、Close の他のステートメントを実行すると、Fetch および Close コマンドが誤った結果を返したり、TiDB がpanicを起こしたりする可能性がある問題を修正します[#40094](https://github.com/pingcap/tidb/issues/40094) @ [ヤンケオ](https://github.com/YangKeao)
    -   DDL を使用して浮動小数点型を変更して長さを変更せずに小数点以下の桁数を減らすと、古いデータが同じままになる問題を修正します[#41281](https://github.com/pingcap/tidb/issues/41281) @ [ジムララ](https://github.com/zimulala)
    -   `information_schema.columns`テーブルに参加すると TiDB がpanic[#32459](https://github.com/pingcap/tidb/issues/32459) @ [タンジェンタ](https://github.com/tangenta)になる問題を修正
    -   実行プラン[#41622](https://github.com/pingcap/tidb/issues/41622) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)の生成時に取得される InfoSchema の不整合により TiDBpanicが発生する問題を修正
    -   TiFlash が実行中に生成された列のエラーを報告する問題を修正[#40663](https://github.com/pingcap/tidb/issues/40663) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   単一の SQL ステートメント[#42135](https://github.com/pingcap/tidb/issues/42135) @ [むじょん](https://github.com/mjonss)に異なるパーティション分割テーブルが含まれる場合に、TiDB が誤った結果を生成する可能性がある問題を修正します。
    -   プラン キャッシュがシャッフル演算子をキャッシュし、誤った結果[#38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990) @ [fzzf678](https://github.com/fzzf678)を返す可能性がある問題を修正します。
    -   インデックス マージを使用して`SET` type 列を含むテーブルを読み取ると、誤った結果が得られる可能性がある問題を修正します[#41293](https://github.com/pingcap/tidb/issues/41293) @ [時間と運命](https://github.com/time-and-fate)
    -   準備されたプラン キャッシュが有効になっている場合にフル インデックス スキャンでエラーが発生する可能性がある問題を修正します[#42150](https://github.com/pingcap/tidb/issues/42150) @ [fzzf678](https://github.com/fzzf678)
    -   DDL ステートメントの実行中に`PointGet`使用してテーブルを読み取る SQL ステートメントがpanic[#41622](https://github.com/pingcap/tidb/issues/41622) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)をスローする可能性がある問題を修正します。
    -   トランザクション内で`PointUpdate`実行した後、TiDB が`SELECT`ステートメント[#28011](https://github.com/pingcap/tidb/issues/28011) @ [ジグアン](https://github.com/zyguan)に対して誤った結果を返す問題を修正します。
    -   メモリリークやパフォーマンスの低下を避けるために、期限切れの領域キャッシュを定期的にクリアします[#40461](https://github.com/pingcap/tidb/issues/40461) @ [スティックナーフ](https://github.com/sticnarf) @ [ジグアン](https://github.com/zyguan)
    -   `INSERT IGNORE`および`REPLACE`ステートメントが、値[#42121](https://github.com/pingcap/tidb/issues/42121) @ [ジグアン](https://github.com/zyguan)を変更しないキーをロックしない問題を修正します。

-   TiKV

    -   `const Enum`型を他の型[#14156](https://github.com/tikv/tikv/issues/14156) @ [wshwsh12](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正
    -   CPU クォータ制限[#13084](https://github.com/tikv/tikv/issues/13084) @ [ボーンチェンジャー](https://github.com/BornChanger)の問題を修正
    -   不正なスナップショットの最後のインデックス[#12618](https://github.com/tikv/tikv/issues/12618) @ [林田市](https://github.com/LintianShi)の問題を修正

-   PD

    -   リージョン分散によりリーダー[#6017](https://github.com/tikv/pd/issues/6017) @ [フンドゥンDM](https://github.com/HunDunDM)が不均一に分布する可能性がある問題を修正
    -   Online Unsafe Recovery のタイムアウト メカニズムが機能しない問題を修正[#6107](https://github.com/tikv/pd/issues/6107) @ [v01dstar](https://github.com/v01dstar)

-   TiFlash

    -   デカルト積[#6730](https://github.com/pingcap/tiflash/issues/6730) @ [ゲンリキ](https://github.com/gengliqi)を計算するときにセミ結合が過剰なメモリを使用する問題を修正
    -   TiFlashログ検索が遅すぎる問題を修正[#6829](https://github.com/pingcap/tiflash/issues/6829) @ [へへへん](https://github.com/hehechen)
    -   新しい照合順序[#6807](https://github.com/pingcap/tiflash/issues/6807) @ [xzhangxian1008](https://github.com/xzhangxian1008)を有効にした後、TopN/Sort 演算子が誤った結果を生成する問題を修正します。
    -   特定の場合に Decimal キャストが誤って切り上げられる問題を修正[#6994](https://github.com/pingcap/tiflash/issues/6994) @ [ウィンドトーカー](https://github.com/windtalker)
    -   TiFlash が生成された列[#6801](https://github.com/pingcap/tiflash/issues/6801) @ [グオシャオゲ](https://github.com/guo-shaoge)を認識できない問題を修正
    -   特定の場合に 10 進数の除算で最後の桁が切り上げられない問題を修正[#7022](https://github.com/pingcap/tiflash/issues/7022) @ [リトルフォール](https://github.com/LittleFall)

-   ツール

    -   TiCDC

        -   データ レプリケーション中の`UPDATE`と`INSERT`ステートメントの不規則性により、 `Duplicate entry`エラー[#8597](https://github.com/pingcap/tiflow/issues/8597) @ [スドジ](https://github.com/sdojjy)が発生する可能性がある問題を修正します。
        -   PD と TiCDC [#8562](https://github.com/pingcap/tiflow/issues/8562) @ [オーバーヴィーナス](https://github.com/overvenus)の間のネットワーク分離によって引き起こされる TiCDC サービスの異常終了の問題を修正します。
        -   TiDB または MySQL シンクにデータをレプリケートするとき、および主キー[#8420](https://github.com/pingcap/tiflow/issues/8420) @ [ジャオシンユ](https://github.com/zhaoxinyu)のない非 null の一意のインデックスを持つ列に`CHARACTER SET`が指定されているときに発生するデータの不整合を修正します。
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [#8588](https://github.com/pingcap/tiflow/issues/8588) @ [咸陽飛](https://github.com/amyangfei)によって制御されない問題を修正
        -   無効な入力[#7903](https://github.com/pingcap/tiflow/issues/7903) @ [CharlesCheung96](https://github.com/CharlesCheung96)に対するエラー メッセージ`cdc cli`を最適化します。
        -   S3storage障害[#8089](https://github.com/pingcap/tiflow/issues/8089) @ [CharlesCheung96](https://github.com/CharlesCheung96)に対して REDO ログが許容できる期間が不十分である問題を修正
        -   PD が異常なときにチェンジフィードを一時停止すると、不正なステータス[#8330](https://github.com/pingcap/tiflow/issues/8330) @ [スドジ](https://github.com/sdojjy)が発生する問題を修正

    -   TiDB Lightning

        -   競合解決ロジック ( `duplicate-resolution` ) によってチェックサムの不一致が生じる可能性がある問題を修正します[#40657](https://github.com/pingcap/tidb/issues/40657) @ [ゴズスキー](https://github.com/gozssky)
        -   TiDB Lightning が分割リージョン フェーズ[#40934](https://github.com/pingcap/tidb/issues/40934) @ [ランス6716](https://github.com/lance6716)でパニックになる問題を修正
        -   ローカル バックエンド モードでデータをインポートするときに、インポートされたターゲット テーブルの複合主キーに`auto_random`列があり、その列の値がソース データ[#41454](https://github.com/pingcap/tidb/issues/41454) @ [D3ハンター](https://github.com/D3Hunter)で指定されていない場合、ターゲット列でデータが自動的に生成されない問題を修正します。
        -   並列インポート[#40923](https://github.com/pingcap/tidb/issues/40923) @ [リチュンジュ](https://github.com/lichunzhu)中に、最後の TiDB Lightning インスタンスを除くすべてのTiDB Lightningインスタンスでローカルの重複レコードが検出された場合、 TiDB Lightning が誤って競合解決をスキップする可能性がある問題を修正します。
