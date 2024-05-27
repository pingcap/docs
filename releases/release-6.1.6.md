---
title: TiDB 6.1.6 Release Notes
summary: TiDB 6.1.6 の互換性の変更、改善、バグ修正について説明します。
---

# TiDB 6.1.6 リリースノート {#tidb-6-1-6-release-notes}

発売日: 2023年4月12日

TiDB バージョン: 6.1.6

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiCDC は、Avro [＃8490](https://github.com/pingcap/tiflow/issues/8490) @ [3エースショーハンド](https://github.com/3AceShowHand)での FLOAT データの不正なエンコードの問題を修正しました。

    TiCDC クラスターを v6.1.6 またはそれ以降の v6.1.x バージョンにアップグレードする場合、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレード前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整して、changefeed がスキーマを正常に更新できるようにする必要があります。そうしないと、アップグレード後に changefeed がスキーマを更新できず、エラー状態になります。

## 改善点 {#improvements}

-   ティビ

    -   プリペアドプランキャッシュ[＃42125](https://github.com/pingcap/tidb/issues/42125) @ [qw4990](https://github.com/qw4990)で`BatchPointGet`の実行プランのキャッシュをサポートします。
    -   インデックス結合[#40505](https://github.com/pingcap/tidb/issues/40505) @ [イサール](https://github.com/Yisaer)のより多くの SQL 形式をサポート

-   ティクヴ

    -   1コア未満のCPUでのTiKVの起動をサポート[＃13586](https://github.com/tikv/tikv/issues/13586) [＃13752](https://github.com/tikv/tikv/issues/13752) [＃14017](https://github.com/tikv/tikv/issues/14017) @ [アンドレイドDB](https://github.com/andreid-db) @ [アンドレイドDB](https://github.com/andreid-db)

## バグの修正 {#bug-fixes}

-   ティビ

    -   `ignore_plan_cache`ヒントが`INSERT`ステートメント[＃40079](https://github.com/pingcap/tidb/issues/40079) [＃39717](https://github.com/pingcap/tidb/issues/39717) @ [qw4990](https://github.com/qw4990)で機能しない可能性がある問題を修正しました
    -   `indexMerge`でエラーが発生した後に TiDB がpanicになる可能性がある問題を修正[＃41047](https://github.com/pingcap/tidb/issues/41047) [＃40877](https://github.com/pingcap/tidb/issues/40877) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [風の話し手](https://github.com/windtalker)
    -   仮想列を持つ TopN 演算子が誤って TiKV またはTiFlash [＃41355](https://github.com/pingcap/tidb/issues/41355) @ [ドゥージール9](https://github.com/Dousir9)にプッシュダウンすると、誤った結果が返される可能性がある問題を修正しました。
    -   多数のリージョンがあるが、 `Prepare`または`Execute` [＃39605](https://github.com/pingcap/tidb/issues/39605) @ [翻訳者](https://github.com/djshow832)を使用して一部の仮想テーブルをクエリするときにテーブル ID をプッシュダウンできない PD OOM 問題を修正しました。
    -   `int_col in (decimal...)`条件[#40224](https://github.com/pingcap/tidb/issues/40224) @ [qw4990](https://github.com/qw4990)を処理するときにプラン キャッシュが FullScan プランをキャッシュする可能性がある問題を修正しました
    -   IndexMerge プランが SET 型列[＃41273](https://github.com/pingcap/tidb/issues/41273) [＃41293](https://github.com/pingcap/tidb/issues/41293) @ [時間と運命](https://github.com/time-and-fate)に誤った範囲を生成する可能性がある問題を修正しました
    -   符号なし`TINYINT` / `SMALLINT` / `INT`値を`0` [＃41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)より小さい`DECIMAL` / `FLOAT` / `DOUBLE`の値と比較するときに誤った結果になる可能性がある問題を修正しました。
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルをクエリすると TiDBサーバーのメモリが不足する問題を修正しました。この問題は、Grafana ダッシュボード[＃33893](https://github.com/pingcap/tidb/issues/33893) @ [クレイジーcs520](https://github.com/crazycs520)で遅いクエリをチェックすると発生する可能性があります。
    -   範囲パーティションで複数の`MAXVALUE`パーティション[＃36329](https://github.com/pingcap/tidb/issues/36329) @ [ユー5サーフ](https://github.com/u5surf)が許可される問題を修正
    -   プラン キャッシュがシャッフル演算子をキャッシュし、誤った結果を返す可能性がある問題を修正[＃38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990)
    -   タイムゾーンでのデータ競合によりデータインデックスの不整合が発生する可能性がある問題を修正[＃40710](https://github.com/pingcap/tidb/issues/40710) @ [翻訳:](https://github.com/wjhuang2016)
    -   `indexMerge` [＃41545](https://github.com/pingcap/tidb/issues/41545) [＃41605](https://github.com/pingcap/tidb/issues/41605) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [グオシャオゲ](https://github.com/guo-shaoge)で goroutine リークが発生する可能性がある問題を修正しました
    -   カーソルフェッチを使用し、実行、フェッチ、クローズの間で他のステートメントを実行すると、フェッチコマンドとクローズコマンドが誤った結果を返したり、TiDB がpanicを起こしたりする可能性がある問題を修正しました[＃40094](https://github.com/pingcap/tidb/issues/40094) @ [ヤンケオ](https://github.com/YangKeao)
    -   DDL を使用して浮動小数点型を変更し、長さを変更せずに小数点以下の桁数を減らしても、古いデータは同じままになる問題を修正しました[＃41281](https://github.com/pingcap/tidb/issues/41281) @ [ジムララ](https://github.com/zimulala)
    -   `information_schema.columns`テーブルを結合すると TiDB がpanicになる問題を修正[＃32459](https://github.com/pingcap/tidb/issues/32459) @ [タンジェンタ](https://github.com/tangenta)
    -   実行プラン[＃41622](https://github.com/pingcap/tidb/issues/41622) @ [天菜まお](https://github.com/tiancaiamao)を生成する際に不整合な InfoSchema が取得され、TiDBpanicが発生する問題を修正しました。
    -   実行中にTiFlash が生成された列のエラーを報告する問題を修正[＃40663](https://github.com/pingcap/tidb/issues/40663) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   単一の SQL ステートメントに異なるパーティション テーブルが出現すると、TiDB が誤った結果を生成する可能性がある問題を修正しました[＃42135](https://github.com/pingcap/tidb/issues/42135) @ [ミョンス](https://github.com/mjonss)
    -   プラン キャッシュがシャッフル演算子をキャッシュし、誤った結果を返す可能性がある問題を修正[＃38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990) @ [ふーふー](https://github.com/fzzf678)
    -   インデックスマージを使用して`SET`型の列を含むテーブルを読み取ると、誤った結果[＃41293](https://github.com/pingcap/tidb/issues/41293) @ [時間と運命](https://github.com/time-and-fate)が発生する可能性がある問題を修正しました
    -   準備済みプランキャッシュが有効になっている場合にフルインデックススキャンでエラーが発生する可能性がある問題を修正[＃42150](https://github.com/pingcap/tidb/issues/42150) @ [ふーふー](https://github.com/fzzf678)
    -   DDL 文の実行中に`PointGet`使用してテーブルを読み込む SQL 文がpanic[＃41622](https://github.com/pingcap/tidb/issues/41622) @ [天菜まお](https://github.com/tiancaiamao)をスローする可能性がある問題を修正しました。
    -   トランザクション内で`PointUpdate`実行した後、TiDB が`SELECT`ステートメント[＃28011](https://github.com/pingcap/tidb/issues/28011) @ [ジグアン](https://github.com/zyguan)に対して誤った結果を返す問題を修正しました。
    -   メモリリークとパフォーマンスの低下を防ぐために、期限切れの領域キャッシュを定期的にクリアします[＃40461](https://github.com/pingcap/tidb/issues/40461) @ [スティクナーフ](https://github.com/sticnarf) @ [ジグアン](https://github.com/zyguan)
    -   `INSERT IGNORE`と`REPLACE`ステートメントが値[＃42121](https://github.com/pingcap/tidb/issues/42121) @ [ジグアン](https://github.com/zyguan)を変更しないキーをロックしない問題を修正しました

-   ティクヴ

    -   `const Enum`型を他の型[＃14156](https://github.com/tikv/tikv/issues/14156) @ [うわー](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正
    -   CPU クォータ制限[＃13084](https://github.com/tikv/tikv/issues/13084) @ [ボーンチェンジャー](https://github.com/BornChanger)の問題を修正
    -   スナップショットの最後のインデックス[＃12618](https://github.com/tikv/tikv/issues/12618) @ [リンティアンシー](https://github.com/LintianShi)が間違っている問題を修正しました

-   PD

    -   リージョン散布によりリーダー[＃6017](https://github.com/tikv/pd/issues/6017) @ [ハンダンDM](https://github.com/HunDunDM)の分布が不均一になる可能性がある問題を修正しました。
    -   オンラインアンセーフリカバリのタイムアウトメカニズムが機能しない問題を修正[＃6107](https://github.com/tikv/pd/issues/6107) @ [v01dスター](https://github.com/v01dstar)

-   TiFlash

    -   直交積[＃6730](https://github.com/pingcap/tiflash/issues/6730) @ [ゲンリキ](https://github.com/gengliqi)を計算するときにセミ結合が過剰なメモリを使用する問題を修正しました
    -   TiFlashログ検索が遅すぎる問題を修正[＃6829](https://github.com/pingcap/tiflash/issues/6829) @ [ヘヘチェン](https://github.com/hehechen)
    -   新しい照合順序[＃6807](https://github.com/pingcap/tiflash/issues/6807) @ [翻訳者](https://github.com/xzhangxian1008)を有効にした後に TopN/Sort 演算子が誤った結果を生成する問題を修正しました。
    -   特定のケースで[＃6994](https://github.com/pingcap/tiflash/issues/6994) @ [風の話し手](https://github.com/windtalker)の Decimal キャストが誤って切り上げられる問題を修正しました
    -   TiFlashが生成された列[＃6801](https://github.com/pingcap/tiflash/issues/6801) @ [グオシャオゲ](https://github.com/guo-shaoge)を認識できない問題を修正
    -   特定のケースで小数点以下の桁が切り上げられない問題を修正[＃7022](https://github.com/pingcap/tiflash/issues/7022) @ [リトルフォール](https://github.com/LittleFall)

-   ツール

    -   ティCDC

        -   データ複製中に`UPDATE`と`INSERT`のステートメントが混在すると`Duplicate entry`エラー[＃8597](https://github.com/pingcap/tiflow/issues/8597) @ [スドジ](https://github.com/sdojjy)が発生する可能性がある問題を修正しました。
        -   PD と TiCDC [＃8562](https://github.com/pingcap/tiflow/issues/8562) @ [金星の上](https://github.com/overvenus)間のネットワーク分離によって発生する TiCDC サービスの異常終了問題を修正
        -   TiDB または MySQL シンクにデータを複製するとき、および主キー[＃8420](https://github.com/pingcap/tiflow/issues/8420) @ [趙新宇](https://github.com/zhaoxinyu)のない非 NULL ユニーク インデックスを持つ列に`CHARACTER SET`指定されたときに発生するデータの不整合を修正します。
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [＃8588](https://github.com/pingcap/tiflow/issues/8588) @ [アミヤンフェイ](https://github.com/amyangfei)で制御されない問題を修正
        -   無効な入力[＃7903](https://github.com/pingcap/tiflow/issues/7903) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に対する`cdc cli`のエラーメッセージを最適化します
        -   S3storage障害[＃8089](https://github.com/pingcap/tiflow/issues/8089) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に対して REDO ログが許容できる期間が不十分である問題を修正
        -   PD が異常なときにチェンジフィードを一時停止すると、誤ったステータス[＃8330](https://github.com/pingcap/tiflow/issues/8330) @ [スドジ](https://github.com/sdojjy)になる問題を修正しました。

    -   TiDB Lightning

        -   競合解決ロジック（ `duplicate-resolution` ）によりチェックサム[＃40657](https://github.com/pingcap/tidb/issues/40657) @ [ゴズスキー](https://github.com/gozssky)の不一致が発生する可能性がある問題を修正
        -   TiDB Lightningが分割領域フェーズ[＃40934](https://github.com/pingcap/tidb/issues/40934) @ [ランス6716](https://github.com/lance6716)でパニックになる問題を修正
        -   ローカル バックエンド モードでデータをインポートするときに、インポートされたターゲット テーブルの複合プライマリ キーに`auto_random`列があり、ソース データ[＃41454](https://github.com/pingcap/tidb/issues/41454) @ [D3ハンター](https://github.com/D3Hunter)でその列の値が指定されていない場合、ターゲット列が自動的にデータを生成しない問題を修正しました。
        -   並列インポート中に最後のTiDB Lightningインスタンスを除くすべてのインスタンスでローカル重複レコードが検出された場合、 TiDB Lightning が競合解決を誤ってスキップする可能性がある問題を修正[＃40923](https://github.com/pingcap/tidb/issues/40923) @ [リチュンジュ](https://github.com/lichunzhu)
