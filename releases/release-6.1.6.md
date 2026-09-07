---
title: TiDB 6.1.6 Release Notes
summary: TiDB 6.1.6 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.1.6 リリースノート {#tidb-6-1-6-release-notes}

発売日：2023年4月12日

TiDB バージョン: 6.1.6

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番環境へのデプロイ](https://docs-archive.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

- TiCDCは、AvroにおけるFLOATデータの不正なエンコードの問題を修正しました。 [#8490](https://github.com/pingcap/tiflow/issues/8490) @[3AceShowHand](https://github.com/3AceShowHand)

    TiCDCクラスターをv6.1.6またはそれ以降のv6.1.xバージョンにアップグレードする際、Avroを使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレード前にConfluent Schema Registryの互換性ポリシーを手動で`None`に調整し、changefeedがスキーマを正常に更新できるようにする必要があります。そうしないと、アップグレード後にchangefeedがスキーマを更新できず、エラー状態になります。

## 改善点 {#improvements}

- TiDB

    - プリペアドプランキャッシュで`BatchPointGet`実行計画のキャッシュをサポート [#42125](https://github.com/pingcap/tidb/issues/42125) @[qw4990](https://github.com/qw4990)
    - インデックス結合でより多くの SQL 形式をサポート [#40505](https://github.com/pingcap/tidb/issues/40505) @[Yisaer](https://github.com/Yisaer)

- TiKV

    - 1コア未満のCPUでTiKVの起動をサポート[`#13586`](https://github.com/tikv/tikv/issues/13586) [`#13752`](https://github.com/tikv/tikv/issues/13752) [`#14017`](https://github.com/tikv/tikv/issues/14017) @[andreid-db](https://github.com/andreid-db)

## バグ修正 {#bug-fixes}

- TiDB

    - `ignore_plan_cache`ヒントが`INSERT`文では機能しない可能性がある問題を修正しました [#40079](https://github.com/pingcap/tidb/issues/40079) [#39717](https://github.com/pingcap/tidb/issues/39717) @[qw4990](https://github.com/qw4990)
    - `indexMerge`エラーに遭遇した後に TiDB がpanicする可能性がある問題を修正[#41047](https://github.com/pingcap/tidb/issues/41047) [#40877](https://github.com/pingcap/tidb/issues/40877) @[guo-shaoge](https://github.com/guo-shaoge) @[windtalker](https://github.com/windtalker)
    - 仮想列を持つ TopN オペレーターが誤って TiKV またはTiFlashにプッシュダウンすると、誤った結果が返される可能性がある問題を修正しました。 [#41355](https://github.com/pingcap/tidb/issues/41355) @[Dousir9](https://github.com/Dousir9)
    - 多数のリージョンがあるが、 `Prepare`または`Execute`を使用して一部の仮想テーブルをクエリするときにテーブル ID をプッシュダウンできないという PD OOM 問題を修正しました。 [#39605](https://github.com/pingcap/tidb/issues/39605) @[djshow832](https://github.com/djshow832)
    - プランキャッシュが`int_col in (decimal...)`条件を処理するときにフルスキャン プランをキャッシュする可能性がある問題を修正しました [#40224](https://github.com/pingcap/tidb/issues/40224) @[qw4990](https://github.com/qw4990)
    - IndexMerge プランが SET 型の列に誤った範囲を生成する可能性がある問題を修正しました [#41273](https://github.com/pingcap/tidb/issues/41273) [#41293](https://github.com/pingcap/tidb/issues/41293) @[time-and-fate](https://github.com/time-and-fate)
    - 符号なしの`TINYINT` / `SMALLINT` / `INT`値を`0`より小さい`DECIMAL` / `FLOAT` / `DOUBLE`値と比較するときに誤った結果になる可能性がある問題を修正しました。 [#41736](https://github.com/pingcap/tidb/issues/41736) @[LittleFall](https://github.com/LittleFall)
    - `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルへのクエリ実行時に TiDBサーバーのメモリが発生する問題を修正しました。この問題は、Grafana ダッシュボードでスロークエリを確認した場合に発生する可能性があります。 [#33893](https://github.com/pingcap/tidb/issues/33893) @[crazycs520](https://github.com/crazycs520)
    - 範囲パーティションで複数の`MAXVALUE`パーティションが許可される問題を修正しました [#36329](https://github.com/pingcap/tidb/issues/36329) @[u5surf](https://github.com/u5surf)
    - プランキャッシュがシャッフル演算子をキャッシュし、誤った結果を返す可能性がある問題を修正[#38335](https://github.com/pingcap/tidb/issues/38335) @[qw4990](https://github.com/qw4990)
    - タイムゾーンでのデータ競合によりデータインデックスの不整合が発生する可能性がある問題を修正[#40710](https://github.com/pingcap/tidb/issues/40710) @[wjhuang2016](https://github.com/wjhuang2016)
    - `indexMerge`で goroutine リークが発生する可能性がある問題を修正しました [#41545](https://github.com/pingcap/tidb/issues/41545) [#41605](https://github.com/pingcap/tidb/issues/41605) @[guo-shaoge](https://github.com/guo-shaoge) @[guo-shaoge](https://github.com/guo-shaoge)
    - カーソルフェッチを使用し、実行、フェッチ、およびクローズの間に他のステートメントを実行すると、フェッチおよびクローズコマンドが誤った結果を返したり、TiDB がpanicたりする可能性がある問題を修正しました[#40094](https://github.com/pingcap/tidb/issues/40094) @[YangKeao](https://github.com/YangKeao)
    - DDLを使用して浮動小数点型を変更し、長さを変更せずに小数点以下の桁数を減らしても、古いデータが同じままになる問題を修正しました[#41281](https://github.com/pingcap/tidb/issues/41281) @[zimulala](https://github.com/zimulala)
    - `information_schema.columns`テーブルを結合すると TiDB がpanicを起こす問題を修正 [#32459](https://github.com/pingcap/tidb/issues/32459) @[tangenta](https://github.com/tangenta)
    - 実行計画を生成する際に不整合な InfoSchema が取得され、TiDB panicが発生する問題を修正しました。 [#41622](https://github.com/pingcap/tidb/issues/41622) @[tiancaiamao](https://github.com/tiancaiamao)
    - 実行中にTiFlash が生成列に対してエラーを報告する問題を修正[#40663](https://github.com/pingcap/tidb/issues/40663) @[guo-shaoge](https://github.com/guo-shaoge)
    - 単一のSQL文に異なるパーティションテーブルが出現した場合にTiDBが誤った結果を生成する可能性がある問題を修正[#42135](https://github.com/pingcap/tidb/issues/42135) @[mjonss](https://github.com/mjonss)
    - プランキャッシュがシャッフル演算子をキャッシュし、誤った結果を返す可能性がある問題を修正[#38335](https://github.com/pingcap/tidb/issues/38335) @[qw4990](https://github.com/qw4990) @[fzzf678](https://github.com/fzzf678)
    - インデックスマージを使用して`SET`型の列を含むテーブルを読み取ると、誤った結果が発生する可能性がある問題を修正しました [#41293](https://github.com/pingcap/tidb/issues/41293) @[time-and-fate](https://github.com/time-and-fate)
    - プリペアドプランキャッシュが有効な場合にフルインデックススキャンでエラーが発生する可能性がある問題を修正[#42150](https://github.com/pingcap/tidb/issues/42150) @[fzzf678](https://github.com/fzzf678)
    - DDL文の実行中に`PointGet`を使用してテーブルを読み込むSQL文がpanicをスローする可能性がある問題を修正しました。 [#41622](https://github.com/pingcap/tidb/issues/41622) @[tiancaiamao](https://github.com/tiancaiamao)
    - トランザクション内で`PointUpdate`を実行した後、TiDB が`SELECT`文に対して誤った結果を返す問題を修正しました。 [#28011](https://github.com/pingcap/tidb/issues/28011) @[zyguan](https://github.com/zyguan)
    - メモリリークとパフォーマンスの低下を防ぐため、期限切れのリージョンキャッシュを定期的にクリアします[#40461](https://github.com/pingcap/tidb/issues/40461) @[sticnarf](https://github.com/sticnarf) @[zyguan](https://github.com/zyguan)
    - `INSERT IGNORE` および `REPLACE`文が値を変更しないキーをロックしない問題を修正しました [#42121](https://github.com/pingcap/tidb/issues/42121) @[zyguan](https://github.com/zyguan)

- TiKV

    - `const Enum`型を他の型にキャストするときに発生するエラーを修正しました [#14156](https://github.com/tikv/tikv/issues/14156) @[wshwsh12](https://github.com/wshwsh12)
    - CPUクォータ制限の問題を修正 [#13084](https://github.com/tikv/tikv/issues/13084) @[BornChanger](https://github.com/BornChanger)
    - スナップショットの最後のインデックスが誤っている問題を修正しました [#12618](https://github.com/tikv/tikv/issues/12618) @[LintianShi](https://github.com/LintianShi)

- PD

    - リージョン散布により、リーダーの分布が不均一になる可能性がある問題を修正しました。 [#6017](https://github.com/tikv/pd/issues/6017) @[HunDunDM](https://github.com/HunDunDM)
    - オンラインアンセーフリカバリのタイムアウトメカニズムが機能しない問題を修正[#6107](https://github.com/tikv/pd/issues/6107) @[v01dstar](https://github.com/v01dstar)

- TiFlash

    - 直交積を計算するときにセミ結合が過剰なメモリを使用する問題を修正しました [#6730](https://github.com/pingcap/tiflash/issues/6730) @[gengliqi](https://github.com/gengliqi)
    - TiFlashログ検索が遅すぎる問題を修正[#6829](https://github.com/pingcap/tiflash/issues/6829) @[hehechen](https://github.com/hehechen)
    - 新しい照合順序を有効にした後に TopN/Sort オペレーターが誤った結果を生成する問題を修正しました [#6807](https://github.com/pingcap/tiflash/issues/6807) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 特定のケースで 10 進キャストが誤って切り上げられる問題を修正しました [#6994](https://github.com/pingcap/tiflash/issues/6994) @[windtalker](https://github.com/windtalker)
    - TiFlashが生成列を認識できない問題を修正 [#6801](https://github.com/pingcap/tiflash/issues/6801) @[guo-shaoge](https://github.com/guo-shaoge)
    - 特定のケースで小数点以下の桁が切り上げられない問題を修正[#7022](https://github.com/pingcap/tiflash/issues/7022) @[LittleFall](https://github.com/LittleFall)

- ツール

    - TiCDC

        - データレプリケーション中の`UPDATE`と`INSERT`文の順序が乱れると、 `Duplicate entry`エラーが発生する可能性がある問題を修正しました。 [#8597](https://github.com/pingcap/tiflow/issues/8597) @[sdojjy](https://github.com/sdojjy)
        - PDとTiCDC間のネットワーク分離によって発生するTiCDCサービスの異常終了問題を修正 [#8562](https://github.com/pingcap/tiflow/issues/8562) @[overvenus](https://github.com/overvenus)
        - TiDB または MySQL シンクにデータを複製するときに、主キーのない非 NULL ユニーク インデックスを持つ列に`CHARACTER SET`を指定した場合に発生するデータの不整合を修正しました。 [#8420](https://github.com/pingcap/tiflow/issues/8420) @[zhaoxinyu](https://github.com/zhaoxinyu)
        - `db sorter`のメモリ使用量が`cgroup memory limit`で制御されない問題を修正 [#8588](https://github.com/pingcap/tiflow/issues/8588) @[amyangfei](https://github.com/amyangfei)
        - 無効な入力に対する`cdc cli`のエラーメッセージを最適化します [#7903](https://github.com/pingcap/tiflow/issues/7903) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - S3ストレージ障害に対して、REDO ログが許容できる期間が不十分である問題を修正しました [#8089](https://github.com/pingcap/tiflow/issues/8089) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - PDが異常なときにチェンジフィードを一時停止すると、誤ったステータスになる問題を修正しました。 [#8330](https://github.com/pingcap/tiflow/issues/8330) @[sdojjy](https://github.com/sdojjy)

    - TiDB Lightning

        - 競合解決ロジック（ `duplicate-resolution` ）によってチェックサムの不一致が発生する可能性がある問題を修正しました。 [#40657](https://github.com/pingcap/tidb/issues/40657) @[sleepymole](https://github.com/sleepymole)
        - TiDB Lightningが分割領域フェーズでパニックになる問題を修正 [#40934](https://github.com/pingcap/tidb/issues/40934) @[lance6716](https://github.com/lance6716)
        - ローカルバックエンドモードでデータをインポートする際に、インポートされたターゲットテーブルの複合主キーに`auto_random`列があり、ソースデータでその列の値が指定されていない場合、ターゲット列が自動的にデータを生成しない問題を修正しました。 [#41454](https://github.com/pingcap/tidb/issues/41454) @[D3Hunter](https://github.com/D3Hunter)
        - 並列インポート中に、最後のTiDB Lightningインスタンスを除くすべてのインスタンスがローカル重複レコードに遭遇した場合に、 TiDB Lightning が競合解決を誤ってスキップする可能性がある問題を修正しました[#40923](https://github.com/pingcap/tidb/issues/40923) @[lichunzhu](https://github.com/lichunzhu)
