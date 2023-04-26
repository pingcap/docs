---
title: TiDB 6.1.6 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.1.6.
---

# TiDB 6.1.6 リリースノート {#tidb-6-1-6-release-notes}

発売日：2023年4月12日

TiDB バージョン: 6.1.6

クイック アクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [インストール パッケージ](https://www.pingcap.com/download/?version=v6.1.6#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiCDC は、Avro [#8490](https://github.com/pingcap/tiflow/issues/8490) @ [3AceShowHand](https://github.com/3AceShowHand)での FLOAT データの不適切なエンコードの問題を修正します。

    TiCDC クラスターを v6.1.6 以降の v6.1.x バージョンにアップグレードするときに、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合、アップグレードする前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整する必要があります。 changefeed はスキーマを正常に更新できます。そうしないと、アップグレード後に変更フィードがスキーマを更新できず、エラー状態になります。

## 改良点 {#improvements}

-   TiDB

    -   プリペアドプランキャッシュ[#42125](https://github.com/pingcap/tidb/issues/42125) @ [qw4990](https://github.com/qw4990)で`BatchPointGet`の実行プランのキャッシュをサポート
    -   Index Join [#40505](https://github.com/pingcap/tidb/issues/40505) @ [イサール](https://github.com/Yisaer)でより多くの SQL 形式をサポート

-   TiKV

    -   コア数が 1 未満の CPU での TiKV の起動をサポート[#13586](https://github.com/tikv/tikv/issues/13586) [#13752](https://github.com/tikv/tikv/issues/13752) [#14017](https://github.com/tikv/tikv/issues/14017) @ [アンドレイドデータベース](https://github.com/andreid-db) @ [アンドレイドデータベース](https://github.com/andreid-db)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `INSERT`ステートメント[#40079](https://github.com/pingcap/tidb/issues/40079) [#39717](https://github.com/pingcap/tidb/issues/39717) @ [qw4990](https://github.com/qw4990)に対して`ignore_plan_cache`ヒントが機能しない可能性がある問題を修正します。
    -   `indexMerge`エラー[#41047](https://github.com/pingcap/tidb/issues/41047) [#40877](https://github.com/pingcap/tidb/issues/40877) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [風の語り手](https://github.com/windtalker)に遭遇した後、TiDB がpanicになる可能性がある問題を修正します。
    -   仮想列を持つ TopN オペレーターが誤って TiKV またはTiFlash [#41355](https://github.com/pingcap/tidb/issues/41355) @ [ドゥジール9](https://github.com/Dousir9)にプッシュ ダウンすると、誤った結果が返されることがある問題を修正します。
    -   多数のリージョンがあるが、 `Prepare`または`Execute` [#39605](https://github.com/pingcap/tidb/issues/39605) @ [DJshow832](https://github.com/djshow832)を使用して一部の仮想テーブルをクエリするときにテーブル ID をプッシュダウンできない場合の PD OOM の問題を修正します
    -   `int_col in (decimal...)`条件[#40224](https://github.com/pingcap/tidb/issues/40224) @ [qw4990](https://github.com/qw4990)を処理するときに、Plan Cache が FullScan プランをキャッシュする可能性がある問題を修正します。
    -   IndexMerge プランが SET タイプ列[#41273](https://github.com/pingcap/tidb/issues/41273) [#41293](https://github.com/pingcap/tidb/issues/41293) @ [時間と運命](https://github.com/time-and-fate)で誤った範囲を生成する可能性があるという問題を修正します
    -   符号なしの`TINYINT` / `SMALLINT` / `INT`値を`0` [#41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)より小さい`DECIMAL` / `FLOAT` / `DOUBLE`値と比較すると、間違った結果になる可能性がある問題を修正
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルをクエリすると、TiDBサーバーがメモリ不足になることがある問題を修正します。この問題は、Grafana ダッシュボード[#33893](https://github.com/pingcap/tidb/issues/33893) @ [クレイジーcs520](https://github.com/crazycs520)でスロー クエリを確認すると発生する可能性があります
    -   範囲パーティションが複数の`MAXVALUE`パーティション[#36329](https://github.com/pingcap/tidb/issues/36329) @ [u5surf](https://github.com/u5surf)を許可する問題を修正します
    -   Plan Cache が Shuffle 演算子をキャッシュし、誤った結果[#38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990)を返す可能性がある問題を修正します。
    -   タイム ゾーンでのデータ競合がデータ インデックスの不整合を引き起こす可能性がある問題を修正します[#40710](https://github.com/pingcap/tidb/issues/40710) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `indexMerge` [#41545](https://github.com/pingcap/tidb/issues/41545) [#41605](https://github.com/pingcap/tidb/issues/41605) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [グオシャオゲ](https://github.com/guo-shaoge)でゴルーチンリークが発生する可能性がある問題を修正
    -   Cursor Fetch を使用して Execute、Fetch、および Close の他のステートメントを実行すると、Fetch および Close コマンドが誤った結果を返したり、TiDB がpanicを引き起こしたりする可能性があるという問題を修正します[#40094](https://github.com/pingcap/tidb/issues/40094) [@ヤンケアオ](https://github.com/YangKeao)
    -   DDL を使用して浮動小数点型を変更して長さを変更せずに小数点以下の桁数を減らすと、古いデータが同じままになるという問題を修正します[#41281](https://github.com/pingcap/tidb/issues/41281) [@zimulala](https://github.com/zimulala)
    -   `information_schema.columns`テーブルを結合すると TiDB がpanicになる問題を修正[#32459](https://github.com/pingcap/tidb/issues/32459) [@接線](https://github.com/tangenta)
    -   実行計画生成時に得られる InfoSchema の不整合により TiDBpanicが発生する問題を修正[#41622](https://github.com/pingcap/tidb/issues/41622) [@tiancaiamao](https://github.com/tiancaiamao)
    -   [#40663](https://github.com/pingcap/tidb/issues/40663) @ [グオシャオゲ](https://github.com/guo-shaoge)の実行中に、 TiFlash が生成された列のエラーを報告する問題を修正します。
    -   単一の SQL ステートメント[#42135](https://github.com/pingcap/tidb/issues/42135) @ [ミヨンス](https://github.com/mjonss)に異なるパーティション テーブルが表示されると、TiDB が誤った結果を生成する可能性があるという問題を修正します。
    -   Plan Cache が Shuffle 演算子をキャッシュし、誤った結果[#38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990) @ [fzzf678](https://github.com/fzzf678)を返す可能性がある問題を修正します
    -   インデックス マージを使用して`SET`型の列を含むテーブルを読み取ると、誤った結果[#41293](https://github.com/pingcap/tidb/issues/41293) @ [時間と運命](https://github.com/time-and-fate)が発生する可能性があるという問題を修正します
    -   準備済みプラン キャッシュが有効になっている場合に、フル インデックス スキャンでエラーが発生する可能性がある問題を修正します[#42150](https://github.com/pingcap/tidb/issues/42150) @ [fzzf678](https://github.com/fzzf678)
    -   DDL ステートメントの実行中に`PointGet`使用してテーブルを読み取る SQL ステートメントがpanic[#41622](https://github.com/pingcap/tidb/issues/41622) @ [ティアンカイマオ](https://github.com/tiancaiamao)をスローする可能性がある問題を修正します。
    -   トランザクション内で`PointUpdate`実行した後、TiDB が`SELECT`ステートメント[#28011](https://github.com/pingcap/tidb/issues/28011) @ [ジグアン](https://github.com/zyguan)に対して誤った結果を返す問題を修正します。
    -   期限切れの領域キャッシュを定期的にクリアして、メモリリークとパフォーマンスの低下を回避する[#40461](https://github.com/pingcap/tidb/issues/40461) @ [スティックナーフ](https://github.com/sticnarf) @ [ジグアン](https://github.com/zyguan)
    -   `INSERT IGNORE`および`REPLACE`ステートメントが値[#42121](https://github.com/pingcap/tidb/issues/42121) @ [ジグアン](https://github.com/zyguan)を変更しないキーをロックしないという問題を修正します。

-   TiKV

    -   `const Enum`型を他の型[#14156](https://github.com/tikv/tikv/issues/14156) @ [wshwsh12](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正
    -   CPU クォータ制限[13084](https://github.com/tikv/tikv/issues/13084) @ [ボーンチェンジャー](https://github.com/BornChanger)の問題を修正
    -   誤ったスナップショットの最後のインデックス[12618](https://github.com/tikv/tikv/issues/12618) @ [臨田市](https://github.com/LintianShi)の問題を修正

-   PD

    -   リージョン Scatter がリーダー[#6017](https://github.com/tikv/pd/issues/6017) @ [フンドゥンDM](https://github.com/HunDunDM)の不均一な分布を引き起こす可能性がある問題を修正します。
    -   Online Unsafe Recovery のタイムアウト メカニズムが機能しない問題を修正[#6107](https://github.com/tikv/pd/issues/6107) @ [v01dstar](https://github.com/v01dstar)

-   TiFlash

    -   デカルト積[#6730](https://github.com/pingcap/tiflash/issues/6730) @ [ゲンリキ](https://github.com/gengliqi)を計算するときに準結合が過剰なメモリを使用する問題を修正します。
    -   TiFlash のログ検索が遅すぎる問題を修正[#6829](https://github.com/pingcap/tiflash/issues/6829) @ [へへへん](https://github.com/hehechen)
    -   新しい照合順序[#6807](https://github.com/pingcap/tiflash/issues/6807) @ [xzhangxian1008](https://github.com/xzhangxian1008)を有効にした後、TopN/Sort 演算子が誤った結果を生成する問題を修正します。
    -   Decimal キャストが特定の場合に[#6994](https://github.com/pingcap/tiflash/issues/6994) @ [風の語り手](https://github.com/windtalker)で誤って切り上げられる問題を修正します。
    -   TiFlash が生成された列[#6801](https://github.com/pingcap/tiflash/issues/6801) @ [グオシャオゲ](https://github.com/guo-shaoge)を認識できない問題を修正
    -   特定の場合に 10 進数の除算で最後の桁が切り上げられない問題を修正します[#7022](https://github.com/pingcap/tiflash/issues/7022) @ [リトルフォール](https://github.com/LittleFall)

-   ツール

    -   TiCDC

        -   データのレプリケーション中に`UPDATE`と`INSERT`ステートメントが乱れると、 `Duplicate entry`エラー[#8597](https://github.com/pingcap/tiflow/issues/8597) @ [スドジ](https://github.com/sojjy)が発生する可能性がある問題を修正します。
        -   PD と TiCDC [#8562](https://github.com/pingcap/tiflow/issues/8562) @ [大静脈](https://github.com/overvenus)の間のネットワーク分離によって発生する TiCDC サービスの異常終了の問題を修正します。
        -   TiDB または MySQL シンクにデータをレプリケートするときに、主キー[#8420](https://github.com/pingcap/tiflow/issues/8420) @ [照信雨](https://github.com/zhaoxinyu)なしで null 以外の一意のインデックスを持つ列に`CHARACTER SET`が指定されたときに発生するデータの不整合を修正します。
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [#8588](https://github.com/pingcap/tiflow/issues/8588) @ [アミヤンフェイ](https://github.com/amyangfei)によって制御されない問題を修正
        -   無効な入力[#7903](https://github.com/pingcap/tiflow/issues/7903) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)に対する`cdc cli`のエラー メッセージを最適化する
        -   S3storage障害[#8089](https://github.com/pingcap/tiflow/issues/8089) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)に対して REDO ログが許容できる期間が不十分であるという問題を修正します。
        -   PDが異常な状態でチェンジフィードを一時停止すると、ステータスが正しくない[#8330](https://github.com/pingcap/tiflow/issues/8330) @ [スドジ](https://github.com/sdojjy)になる問題を修正

    -   TiDB Lightning

        -   競合解決ロジック ( `duplicate-resolution` ) が不整合なチェックサム[#40657](https://github.com/pingcap/tidb/issues/40657) @ [ゴズスキー](https://github.com/gozssky)を引き起こす可能性があるという問題を修正します。
        -   分割領域フェーズ[#40934](https://github.com/pingcap/tidb/issues/40934) @ [ランス6716](https://github.com/lance6716)でTiDB Lightning がパニックになる問題を修正
        -   ローカル バックエンド モードでデータをインポートするときに、インポートされたターゲット テーブルの複合主キーに`auto_random`列があり、その列の値がソース データで指定されていない場合、ターゲット列が自動的にデータを生成しないという問題を修正します[#41454](https://github.com/pingcap/tidb/issues/41454) @ [D3ハンター](https://github.com/D3Hunter)
        -   並列インポート[#40923](https://github.com/pingcap/tidb/issues/40923) @ [リチュンジュ](https://github.com/lichunzhu)中に、最後のTiDB Lightningインスタンス以外のすべてのインスタンスがローカルの重複レコードに遭遇した場合、 TiDB Lightning が競合解決を誤ってスキップする可能性があるという問題を修正します。
