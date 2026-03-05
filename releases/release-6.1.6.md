---
title: TiDB 6.1.6 Release Notes
summary: TiDB 6.1.6 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.1.6 リリースノート {#tidb-6-1-6-release-notes}

発売日：2023年4月12日

TiDB バージョン: 6.1.6

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiCDCは、Avro [＃8490](https://github.com/pingcap/tiflow/issues/8490) @ [3エースショーハンド](https://github.com/3AceShowHand)におけるFLOATデータの不正なエンコードの問題を修正しました。

    TiCDCクラスターをv6.1.6またはそれ以降のv6.1.xバージョンにアップグレードする際、Avroを使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレード前にConfluent Schema Registryの互換性ポリシーを手動で`None`に調整し、changefeedがスキーマを正常に更新できるようにする必要があります。そうしないと、アップグレード後にchangefeedがスキーマを更新できず、エラー状態になります。

## 改善点 {#improvements}

-   TiDB

    -   プリペアドプランキャッシュ[＃42125](https://github.com/pingcap/tidb/issues/42125) @ [qw4990](https://github.com/qw4990)で`BatchPointGet`実行プランのキャッシュをサポート
    -   インデックス結合[＃40505](https://github.com/pingcap/tidb/issues/40505) @ [イーサール](https://github.com/Yisaer)より多くの SQL 形式をサポート

-   TiKV

    -   1コア未満のCPUでTiKVの起動をサポート[＃13586](https://github.com/tikv/tikv/issues/13586) [＃13752](https://github.com/tikv/tikv/issues/13752) [＃14017](https://github.com/tikv/tikv/issues/14017) @ [andreid-db](https://github.com/andreid-db) @ [andreid-db](https://github.com/andreid-db)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `ignore_plan_cache`ヒントが`INSERT`ステートメント[＃40079](https://github.com/pingcap/tidb/issues/40079) [＃39717](https://github.com/pingcap/tidb/issues/39717) @ [qw4990](https://github.com/qw4990)では機能しない可能性がある問題を修正しました
    -   `indexMerge`エラーに遭遇した後に TiDB がpanic可能性がある問題を修正[＃41047](https://github.com/pingcap/tidb/issues/41047) [＃40877](https://github.com/pingcap/tidb/issues/40877) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [ウィンドトーカー](https://github.com/windtalker)
    -   仮想列を持つ TopN 演算子が誤って TiKV またはTiFlash [＃41355](https://github.com/pingcap/tidb/issues/41355) @ [ドゥーシル9](https://github.com/Dousir9)にプッシュダウンすると、誤った結果が返される可能性がある問題を修正しました。
    -   多数のリージョンがあるが、 `Prepare`または`Execute` [＃39605](https://github.com/pingcap/tidb/issues/39605) @ [djshow832](https://github.com/djshow832)を使用して一部の仮想テーブルをクエリするときにテーブル ID をプッシュダウンできないという PD OOM 問題を修正しました。
    -   プランキャッシュが`int_col in (decimal...)`条件[＃40224](https://github.com/pingcap/tidb/issues/40224) @ [qw4990](https://github.com/qw4990)を処理するときにフルスキャン プランをキャッシュする可能性がある問題を修正しました
    -   IndexMerge プランが SET 型の列[＃41273](https://github.com/pingcap/tidb/issues/41273) [＃41293](https://github.com/pingcap/tidb/issues/41293) @ [時間と運命](https://github.com/time-and-fate)に誤った範囲を生成する可能性がある問題を修正しました
    -   符号なしの`TINYINT` / `SMALLINT` / `INT`値を`0` [＃41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)より小さい`DECIMAL` / `FLOAT` / `DOUBLE`値と比較するときに誤った結果になる可能性がある問題を修正しました。
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルへのクエリ実行時に TiDBサーバーのメモリが発生する問題を修正しました。この問題は、Grafana ダッシュボード[＃33893](https://github.com/pingcap/tidb/issues/33893) @ [crazycs520](https://github.com/crazycs520)でスロークエリを確認した場合に発生する可能性があります。
    -   範囲パーティションで複数の`MAXVALUE`パーティション[＃36329](https://github.com/pingcap/tidb/issues/36329) @ [u5サーフ](https://github.com/u5surf)が許可される問題を修正しました
    -   プランキャッシュがシャッフル演算子をキャッシュし、誤った結果を返す可能性がある問題を修正[＃38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990)
    -   タイムゾーンでのデータ競合によりデータインデックスの不整合が発生する可能性がある問題を修正[＃40710](https://github.com/pingcap/tidb/issues/40710) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `indexMerge` [＃41545](https://github.com/pingcap/tidb/issues/41545) [＃41605](https://github.com/pingcap/tidb/issues/41605) @ [グオシャオゲ](https://github.com/guo-shaoge) @ [グオシャオゲ](https://github.com/guo-shaoge)で goroutine リークが発生する可能性がある問題を修正しました
    -   カーソルフェッチを使用し、実行、フェッチ、およびクローズの間に他のステートメントを実行すると、フェッチおよびクローズコマンドが誤った結果を返したり、TiDB がpanicたりする可能性がある問題を修正しました[＃40094](https://github.com/pingcap/tidb/issues/40094) @ [ヤンケオ](https://github.com/YangKeao)
    -   DDLを使用して浮動小数点型を変更し、長さを変更せずに小数点以下の桁数を減らしても、古いデータが同じままになる問題を修正しました[＃41281](https://github.com/pingcap/tidb/issues/41281) @ [ジムララ](https://github.com/zimulala)
    -   `information_schema.columns`テーブルを結合すると TiDB がpanic[＃32459](https://github.com/pingcap/tidb/issues/32459) @ [接線](https://github.com/tangenta)を起こす問題を修正
    -   実行プラン[＃41622](https://github.com/pingcap/tidb/issues/41622) @ [天菜まお](https://github.com/tiancaiamao)を生成する際に不整合な InfoSchema が取得され、TiDBpanicが発生する問題を修正しました。
    -   実行中にTiFlash が生成された列に対してエラーを報告する問題を修正[＃40663](https://github.com/pingcap/tidb/issues/40663) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   単一のSQL文に異なるパーティションテーブルが出現した場合にTiDBが誤った結果を生成する可能性がある問題を修正[＃42135](https://github.com/pingcap/tidb/issues/42135) @ [ミョンス](https://github.com/mjonss)
    -   プランキャッシュがシャッフル演算子をキャッシュし、誤った結果を返す可能性がある問題を修正[＃38335](https://github.com/pingcap/tidb/issues/38335) @ [qw4990](https://github.com/qw4990) @ [fzzf678](https://github.com/fzzf678)
    -   インデックスマージを使用して`SET`型の列を含むテーブルを読み取ると、誤った結果[＃41293](https://github.com/pingcap/tidb/issues/41293) @ [時間と運命](https://github.com/time-and-fate)が発生する可能性がある問題を修正しました
    -   準備済みプランキャッシュが有効な場合にフルインデックススキャンでエラーが発生する可能性がある問題を修正[＃42150](https://github.com/pingcap/tidb/issues/42150) @ [fzzf678](https://github.com/fzzf678)
    -   DDL文の実行中に`PointGet`使用してテーブルを読み込むSQL文がpanic[＃41622](https://github.com/pingcap/tidb/issues/41622) @ [天菜まお](https://github.com/tiancaiamao)をスローする可能性がある問題を修正しました
    -   トランザクション内で`PointUpdate`実行した後、TiDB が`SELECT`文[＃28011](https://github.com/pingcap/tidb/issues/28011) @ [ジグアン](https://github.com/zyguan)に対して誤った結果を返す問題を修正しました。
    -   メモリリークとパフォーマンスの低下を防ぐため、期限切れのリージョンキャッシュを定期的にクリアします[＃40461](https://github.com/pingcap/tidb/issues/40461) @ [スティクナーフ](https://github.com/sticnarf) @ [ジグアン](https://github.com/zyguan)
    -   Fix the issue that `INSERT IGNORE` and `REPLACE` statements do not lock keys that do not modify values [＃42121](https://github.com/pingcap/tidb/issues/42121) @[ジグアン](https://github.com/zyguan)

-   TiKV

    -   `const Enum`型を他の型[＃14156](https://github.com/tikv/tikv/issues/14156) @ [wshwsh12](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正しました
    -   CPUクォータ制限[＃13084](https://github.com/tikv/tikv/issues/13084) @ [生まれ変わった人](https://github.com/BornChanger)の問題を修正
    -   スナップショットの最後のインデックス[＃12618](https://github.com/tikv/tikv/issues/12618) @ [林田市](https://github.com/LintianShi)と誤っている問題を修正しました

-   PD

    -   リージョン散布により、リーダー[＃6017](https://github.com/tikv/pd/issues/6017) @ [ハンダンDM](https://github.com/HunDunDM)の分布が不均一になる可能性がある問題を修正しました。
    -   オンラインアンセーフリカバリのタイムアウトメカニズムが機能しない問題を修正[＃6107](https://github.com/tikv/pd/issues/6107) @ [v01dstar](https://github.com/v01dstar)

-   TiFlash

    -   直交積[＃6730](https://github.com/pingcap/tiflash/issues/6730) @ [ゲンリキ](https://github.com/gengliqi)を計算するときにセミ結合が過剰なメモリを使用する問題を修正しました
    -   TiFlashログ検索が遅すぎる問題を修正[＃6829](https://github.com/pingcap/tiflash/issues/6829) @ [ヘヘチェン](https://github.com/hehechen)
    -   新しい照合順序[＃6807](https://github.com/pingcap/tiflash/issues/6807) @ [xzhangxian1008](https://github.com/xzhangxian1008)を有効にした後に TopN/Sort 演算子が誤った結果を生成する問題を修正しました
    -   特定のケースで[＃6994](https://github.com/pingcap/tiflash/issues/6994) @ [ウィンドトーカー](https://github.com/windtalker) 10 進キャストが誤って切り上げられる問題を修正しました
    -   TiFlashが生成された列[＃6801](https://github.com/pingcap/tiflash/issues/6801) @ [グオシャオゲ](https://github.com/guo-shaoge)を認識できない問題を修正
    -   特定のケースで小数点以下の桁が切り上げられない問題を修正[＃7022](https://github.com/pingcap/tiflash/issues/7022) @ [リトルフォール](https://github.com/LittleFall)

-   ツール

    -   TiCDC

        -   データレプリケーション中の`UPDATE`と`INSERT`ステートメントの順序が乱れると、 `Duplicate entry`エラー[＃8597](https://github.com/pingcap/tiflow/issues/8597) @ [スドジ](https://github.com/sdojjy)が発生する可能性がある問題を修正しました。
        -   PDとTiCDC [＃8562](https://github.com/pingcap/tiflow/issues/8562) @ [金星の上](https://github.com/overvenus)間のネットワーク分離によって発生するTiCDCサービスの異常終了問題を修正
        -   TiDB または MySQL シンクにデータを複製するときに、主キー[＃8420](https://github.com/pingcap/tiflow/issues/8420) @ [ジャオシンユ](https://github.com/zhaoxinyu)のない非 NULL ユニーク インデックスを持つ列に`CHARACTER SET`指定した場合に発生するデータの不整合を修正しました。
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [＃8588](https://github.com/pingcap/tiflow/issues/8588) @ [アミャンフェイ](https://github.com/amyangfei)で制御されない問題を修正
        -   無効な入力[＃7903](https://github.com/pingcap/tiflow/issues/7903)に対する`cdc cli`のエラーメッセージを[チャールズ・チュン96](https://github.com/CharlesCheung96)で最適化します
        -   S3storage障害[＃8089](https://github.com/pingcap/tiflow/issues/8089) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)に対して、REDO ログが許容できる期間が不十分である問題を修正しました
        -   PDが異常なときにチェンジフィードを一時停止すると、誤ったステータス[＃8330](https://github.com/pingcap/tiflow/issues/8330) @ [スドジ](https://github.com/sdojjy)になる問題を修正しました。

    -   TiDB Lightning

        -   競合解決ロジック（ `duplicate-resolution` ）によってチェックサム[＃40657](https://github.com/pingcap/tidb/issues/40657) @ [眠そうなモグラ](https://github.com/sleepymole)の不一致が発生する可能性がある問題を修正しました。
        -   TiDB Lightningが分割領域フェーズ[＃40934](https://github.com/pingcap/tidb/issues/40934) @ [ランス6716](https://github.com/lance6716)でパニックになる問題を修正
        -   ローカルバックエンドモードでデータをインポートする際に、インポートされたターゲットテーブルの複合主キーに`auto_random`列があり、ソースデータ[＃41454](https://github.com/pingcap/tidb/issues/41454) @ [D3ハンター](https://github.com/D3Hunter)でその列の値が指定されていない場合、ターゲット列が自動的にデータを生成しない問題を修正しました。
        -   並列インポート中に、最後のTiDB Lightningインスタンスを除くすべてのインスタンスがローカル重複レコードに遭遇した場合に、 TiDB Lightning が競合解決を誤ってスキップする可能性がある問題を修正しました[＃40923](https://github.com/pingcap/tidb/issues/40923) @ [リチュンジュ](https://github.com/lichunzhu)
