---
title: TiDB 6.1.6 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.1.6.
---

# TiDB 6.1.6 リリースノート {#tidb-6-1-6-release-notes}

発売日：2023年4月12日

TiDB バージョン: 6.1.6

クイックアクセス: [<a href="https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb">クイックスタート</a>](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [<a href="https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup">本番展開</a>](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [<a href="https://www.pingcap.com/download/?version=v6.1.6#version-list">インストールパッケージ</a>](https://www.pingcap.com/download/?version=v6.1.6#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiCDC は、Avro [<a href="https://github.com/pingcap/tiflow/issues/8490">#8490</a>](https://github.com/pingcap/tiflow/issues/8490) @ [<a href="https://github.com/3AceShowHand">3エースショーハンド</a>](https://github.com/3AceShowHand)での FLOAT データの誤ったエンコードの問題を修正しました

    TiCDC クラスターを v6.1.6 以降の v6.1.x バージョンにアップグレードするときに、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレードする前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整する必要があります。 Changefeed はスキーマを正常に更新できます。そうしないと、アップグレード後に変更フィードがスキーマを更新できなくなり、エラー状態になります。

## 改善点 {#improvements}

-   TiDB

    -   プリペアドプランキャッシュ [<a href="https://github.com/pingcap/tidb/issues/42125">#42125</a>](https://github.com/pingcap/tidb/issues/42125) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)の`BatchPointGet`の実行プランのキャッシュをサポートします。
    -   インデックス結合[<a href="https://github.com/pingcap/tidb/issues/40505">#40505</a>](https://github.com/pingcap/tidb/issues/40505) @ [<a href="https://github.com/Yisaer">イーサール</a>](https://github.com/Yisaer)でより多くの SQL 形式をサポート

-   TiKV

    -   1 コア未満の CPU での TiKV の起動をサポート[<a href="https://github.com/tikv/tikv/issues/13586">#13586</a>](https://github.com/tikv/tikv/issues/13586) [<a href="https://github.com/tikv/tikv/issues/13752">#13752</a>](https://github.com/tikv/tikv/issues/13752) [<a href="https://github.com/tikv/tikv/issues/14017">#14017</a>](https://github.com/tikv/tikv/issues/14017) @ [<a href="https://github.com/andreid-db">アンドロイドデータベース</a>](https://github.com/andreid-db) @ [<a href="https://github.com/andreid-db">アンドロイドデータベース</a>](https://github.com/andreid-db)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `ignore_plan_cache`ヒントが`INSERT`ステートメント[<a href="https://github.com/pingcap/tidb/issues/40079">#40079</a>](https://github.com/pingcap/tidb/issues/40079) [<a href="https://github.com/pingcap/tidb/issues/39717">#39717</a>](https://github.com/pingcap/tidb/issues/39717) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)に対して機能しない可能性がある問題を修正
    -   `indexMerge`エラー[<a href="https://github.com/pingcap/tidb/issues/41047">#41047</a>](https://github.com/pingcap/tidb/issues/41047) [<a href="https://github.com/pingcap/tidb/issues/40877">#40877</a>](https://github.com/pingcap/tidb/issues/40877) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge) @ [<a href="https://github.com/windtalker">ウィンドトーカー</a>](https://github.com/windtalker)が発生した後に TiDB がpanicになる可能性がある問題を修正
    -   仮想列を持つ TopN オペレーターが誤って TiKV またはTiFlash [<a href="https://github.com/pingcap/tidb/issues/41355">#41355</a>](https://github.com/pingcap/tidb/issues/41355) @ [<a href="https://github.com/Dousir9">ドゥーシール9</a>](https://github.com/Dousir9)にプッシュダウンすると、誤った結果が返される可能性がある問題を修正
    -   多数のリージョンがあるにもかかわらず、 `Prepare`または`Execute` [<a href="https://github.com/pingcap/tidb/issues/39605">#39605</a>](https://github.com/pingcap/tidb/issues/39605) @ [<a href="https://github.com/djshow832">djshow832</a>](https://github.com/djshow832)を使用して一部の仮想テーブルをクエリするときにテーブル ID をプッシュダウンできない場合の PD OOM の問題を修正します。
    -   `int_col in (decimal...)`条件[<a href="https://github.com/pingcap/tidb/issues/40224">#40224</a>](https://github.com/pingcap/tidb/issues/40224) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)を処理するときにプラン キャッシュがフルスキャン プランをキャッシュする可能性がある問題を修正
    -   IndexMerge プランが SET タイプの列[<a href="https://github.com/pingcap/tidb/issues/41273">#41273</a>](https://github.com/pingcap/tidb/issues/41273) [<a href="https://github.com/pingcap/tidb/issues/41293">#41293</a>](https://github.com/pingcap/tidb/issues/41293) @ [<a href="https://github.com/time-and-fate">時間と運命</a>](https://github.com/time-and-fate)に不正な範囲を生成する可能性がある問題を修正します。
    -   符号なし`TINYINT` / `SMALLINT` / `INT`の値を`0` [<a href="https://github.com/pingcap/tidb/issues/41736">#41736</a>](https://github.com/pingcap/tidb/issues/41736) @ [<a href="https://github.com/LittleFall">リトルフォール</a>](https://github.com/LittleFall)より小さい`DECIMAL` / `FLOAT` / `DOUBLE`の値と比較するときに誤った結果が生じる可能性がある問題を修正
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルがクエリされるときに TiDBサーバーがメモリ不足になる可能性がある問題を修正します。この問題は、Grafana ダッシュボード[<a href="https://github.com/pingcap/tidb/issues/33893">#33893</a>](https://github.com/pingcap/tidb/issues/33893) @ [<a href="https://github.com/crazycs520">クレイジークス520</a>](https://github.com/crazycs520)で遅いクエリをチェックすると発生する可能性があります。
    -   範囲パーティションで複数の`MAXVALUE`パーティション[<a href="https://github.com/pingcap/tidb/issues/36329">#36329</a>](https://github.com/pingcap/tidb/issues/36329) @ [<a href="https://github.com/u5surf">u5サーフィン</a>](https://github.com/u5surf)が許可される問題を修正
    -   プラン キャッシュがシャッフル演算子をキャッシュし、誤った結果[<a href="https://github.com/pingcap/tidb/issues/38335">#38335</a>](https://github.com/pingcap/tidb/issues/38335) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990)を返す可能性がある問題を修正します。
    -   タイムゾーン内のデータ競合によりデータインデックスの不整合が発生する可能性がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/40710">#40710</a>](https://github.com/pingcap/tidb/issues/40710) @ [<a href="https://github.com/wjhuang2016">wjhuang2016</a>](https://github.com/wjhuang2016)
    -   `indexMerge` [<a href="https://github.com/pingcap/tidb/issues/41545">#41545</a>](https://github.com/pingcap/tidb/issues/41545) [<a href="https://github.com/pingcap/tidb/issues/41605">#41605</a>](https://github.com/pingcap/tidb/issues/41605) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge)で goroutine リークが発生する可能性がある問題を修正
    -   Cursor Fetch を使用し、Execute、Fetch、Close の他のステートメントを実行すると、Fetch および Close コマンドが誤った結果を返したり、TiDB がpanicを引き起こす可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/40094">#40094</a>](https://github.com/pingcap/tidb/issues/40094) [<a href="https://github.com/YangKeao">@YangKeao</a>](https://github.com/YangKeao)
    -   DDL を使用して浮動小数点型を変更し、長さを変更せずに小数点以下の桁数を減らすと、古いデータが同じままになる問題を修正します[<a href="https://github.com/pingcap/tidb/issues/41281">#41281</a>](https://github.com/pingcap/tidb/issues/41281) [<a href="https://github.com/zimulala">@zimulala</a>](https://github.com/zimulala)
    -   `information_schema.columns`テーブルに参加すると TiDB がpanicになる問題を修正[<a href="https://github.com/pingcap/tidb/issues/32459">#32459</a>](https://github.com/pingcap/tidb/issues/32459) [<a href="https://github.com/tangenta">@タンジェンタ</a>](https://github.com/tangenta)
    -   実行プラン生成時に取得した InfoSchema の不整合により TiDBpanicが発生する問題を修正[<a href="https://github.com/pingcap/tidb/issues/41622">#41622</a>](https://github.com/pingcap/tidb/issues/41622) [<a href="https://github.com/tiancaiamao">@tiancaiamao</a>](https://github.com/tiancaiamao)
    -   TiFlash が実行中に生成された列のエラーを報告する問題を修正[<a href="https://github.com/pingcap/tidb/issues/40663">#40663</a>](https://github.com/pingcap/tidb/issues/40663) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge)
    -   単一の SQL ステートメント[<a href="https://github.com/pingcap/tidb/issues/42135">#42135</a>](https://github.com/pingcap/tidb/issues/42135) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)に異なるパーティション分割テーブルが含まれる場合、TiDB が誤った結果を生成する可能性がある問題を修正します。
    -   プラン キャッシュがシャッフル演算子をキャッシュし、誤った結果[<a href="https://github.com/pingcap/tidb/issues/38335">#38335</a>](https://github.com/pingcap/tidb/issues/38335) @ [<a href="https://github.com/qw4990">qw4990</a>](https://github.com/qw4990) @ [<a href="https://github.com/fzzf678">fzzf678</a>](https://github.com/fzzf678)を返す可能性がある問題を修正します。
    -   インデックス マージを使用して`SET` type 列を含むテーブルを読み取ると、誤った結果が得られる可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/41293">#41293</a>](https://github.com/pingcap/tidb/issues/41293) @ [<a href="https://github.com/time-and-fate">時間と運命</a>](https://github.com/time-and-fate)
    -   準備されたプラン キャッシュが有効になっている場合にフル インデックス スキャンでエラーが発生する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/42150">#42150</a>](https://github.com/pingcap/tidb/issues/42150) @ [<a href="https://github.com/fzzf678">fzzf678</a>](https://github.com/fzzf678)
    -   DDL ステートメントの実行中に`PointGet`使用してテーブルを読み取る SQL ステートメントがpanic[<a href="https://github.com/pingcap/tidb/issues/41622">#41622</a>](https://github.com/pingcap/tidb/issues/41622) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)をスローする可能性がある問題を修正します。
    -   トランザクション内で`PointUpdate`実行した後、TiDB が`SELECT`ステートメント[<a href="https://github.com/pingcap/tidb/issues/28011">#28011</a>](https://github.com/pingcap/tidb/issues/28011) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)に対して誤った結果を返す問題を修正します。
    -   メモリリークやパフォーマンスの低下を避けるために、期限切れの領域キャッシュを定期的にクリアします[<a href="https://github.com/pingcap/tidb/issues/40461">#40461</a>](https://github.com/pingcap/tidb/issues/40461) @ [<a href="https://github.com/sticnarf">スティックナーフ</a>](https://github.com/sticnarf) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)
    -   `INSERT IGNORE`および`REPLACE`ステートメントが、値[<a href="https://github.com/pingcap/tidb/issues/42121">#42121</a>](https://github.com/pingcap/tidb/issues/42121) @ [<a href="https://github.com/zyguan">ジグアン</a>](https://github.com/zyguan)を変更しないキーをロックしない問題を修正します。

-   TiKV

    -   `const Enum`型を他の型[<a href="https://github.com/tikv/tikv/issues/14156">#14156</a>](https://github.com/tikv/tikv/issues/14156) @ [<a href="https://github.com/wshwsh12">wshwsh12</a>](https://github.com/wshwsh12)にキャストするときに発生するエラーを修正
    -   CPU クォータ制限[<a href="https://github.com/tikv/tikv/issues/13084">13084</a>](https://github.com/tikv/tikv/issues/13084) @ [<a href="https://github.com/BornChanger">ボーンチェンジャー</a>](https://github.com/BornChanger)の問題を修正
    -   不正なスナップショットの最後のインデックス[<a href="https://github.com/tikv/tikv/issues/12618">12618</a>](https://github.com/tikv/tikv/issues/12618) @ [<a href="https://github.com/LintianShi">林田市</a>](https://github.com/LintianShi)の問題を修正

-   PD

    -   リージョン分散によりリーダー[<a href="https://github.com/tikv/pd/issues/6017">#6017</a>](https://github.com/tikv/pd/issues/6017) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)が不均一に分布する可能性がある問題を修正
    -   Online Unsafe Recovery のタイムアウト メカニズムが機能しない問題を修正[<a href="https://github.com/tikv/pd/issues/6107">#6107</a>](https://github.com/tikv/pd/issues/6107) @ [<a href="https://github.com/v01dstar">v01dstar</a>](https://github.com/v01dstar)

-   TiFlash

    -   デカルト積[<a href="https://github.com/pingcap/tiflash/issues/6730">#6730</a>](https://github.com/pingcap/tiflash/issues/6730) @ [<a href="https://github.com/gengliqi">ゲンリチ</a>](https://github.com/gengliqi)を計算するときにセミ結合が過剰なメモリを使用する問題を修正
    -   TiFlashログ検索が遅すぎる問題を修正[<a href="https://github.com/pingcap/tiflash/issues/6829">#6829</a>](https://github.com/pingcap/tiflash/issues/6829) @ [<a href="https://github.com/hehechen">へへへん</a>](https://github.com/hehechen)
    -   新しい照合順序[<a href="https://github.com/pingcap/tiflash/issues/6807">#6807</a>](https://github.com/pingcap/tiflash/issues/6807) @ [<a href="https://github.com/xzhangxian1008">xzhangxian1008</a>](https://github.com/xzhangxian1008)を有効にした後、TopN/Sort 演算子が誤った結果を生成する問題を修正します。
    -   特定の場合に Decimal キャストが誤って切り上げられる問題を修正[<a href="https://github.com/pingcap/tiflash/issues/6994">#6994</a>](https://github.com/pingcap/tiflash/issues/6994) @ [<a href="https://github.com/windtalker">ウィンドトーカー</a>](https://github.com/windtalker)
    -   TiFlash が生成された列[<a href="https://github.com/pingcap/tiflash/issues/6801">#6801</a>](https://github.com/pingcap/tiflash/issues/6801) @ [<a href="https://github.com/guo-shaoge">グオシャオゲ</a>](https://github.com/guo-shaoge)を認識できない問題を修正
    -   特定の場合に 10 進数の除算で最後の桁が切り上げられない問題を修正[<a href="https://github.com/pingcap/tiflash/issues/7022">#7022</a>](https://github.com/pingcap/tiflash/issues/7022) @ [<a href="https://github.com/LittleFall">リトルフォール</a>](https://github.com/LittleFall)

-   ツール

    -   TiCDC

        -   データ レプリケーション中の`UPDATE`と`INSERT`ステートメントの不規則性により、 `Duplicate entry`エラー[<a href="https://github.com/pingcap/tiflow/issues/8597">#8597</a>](https://github.com/pingcap/tiflow/issues/8597) @ [<a href="https://github.com/sojjy">スドジ</a>](https://github.com/sojjy)が発生する可能性がある問題を修正します。
        -   PD と TiCDC [<a href="https://github.com/pingcap/tiflow/issues/8562">#8562</a>](https://github.com/pingcap/tiflow/issues/8562) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)の間のネットワーク分離によって引き起こされる TiCDC サービスの異常終了の問題を修正します。
        -   TiDB または MySQL シンクにデータをレプリケートするとき、および主キー[<a href="https://github.com/pingcap/tiflow/issues/8420">#8420</a>](https://github.com/pingcap/tiflow/issues/8420) @ [<a href="https://github.com/zhaoxinyu">ジャオシンユ</a>](https://github.com/zhaoxinyu)のない非 null の一意のインデックスを持つ列に`CHARACTER SET`が指定されているときに発生するデータの不整合を修正します。
        -   `db sorter`のメモリ使用量が`cgroup memory limit` [<a href="https://github.com/pingcap/tiflow/issues/8588">#8588</a>](https://github.com/pingcap/tiflow/issues/8588) @ [<a href="https://github.com/amyangfei">咸陽飛</a>](https://github.com/amyangfei)によって制御されない問題を修正
        -   無効な入力[<a href="https://github.com/pingcap/tiflow/issues/7903">#7903</a>](https://github.com/pingcap/tiflow/issues/7903) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)に対するエラー メッセージ`cdc cli`を最適化します。
        -   S3storage障害[<a href="https://github.com/pingcap/tiflow/issues/8089">#8089</a>](https://github.com/pingcap/tiflow/issues/8089) @ [<a href="https://github.com/CharlesCheung96">CharlesCheung96</a>](https://github.com/CharlesCheung96)に対して REDO ログが許容できる期間が不十分である問題を修正
        -   PD が異常なときにチェンジフィードを一時停止すると、不正なステータス[<a href="https://github.com/pingcap/tiflow/issues/8330">#8330</a>](https://github.com/pingcap/tiflow/issues/8330) @ [<a href="https://github.com/sdojjy">スドジ</a>](https://github.com/sdojjy)が発生する問題を修正

    -   TiDB Lightning

        -   競合解決ロジック ( `duplicate-resolution` ) によってチェックサムの不一致が生じる可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/40657">#40657</a>](https://github.com/pingcap/tidb/issues/40657) @ [<a href="https://github.com/gozssky">ゴズスキー</a>](https://github.com/gozssky)
        -   TiDB Lightning が分割リージョン フェーズ[<a href="https://github.com/pingcap/tidb/issues/40934">#40934</a>](https://github.com/pingcap/tidb/issues/40934) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)でパニックになる問題を修正
        -   ローカル バックエンド モードでデータをインポートするときに、インポートされたターゲット テーブルの複合主キーに`auto_random`列があり、その列の値がソース データ[<a href="https://github.com/pingcap/tidb/issues/41454">#41454</a>](https://github.com/pingcap/tidb/issues/41454) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)で指定されていない場合、ターゲット列でデータが自動的に生成されない問題を修正します。
        -   並列インポート[<a href="https://github.com/pingcap/tidb/issues/40923">#40923</a>](https://github.com/pingcap/tidb/issues/40923) @ [<a href="https://github.com/lichunzhu">リチュンジュ</a>](https://github.com/lichunzhu)中に、最後の TiDB Lightning インスタンスを除くすべてのTiDB Lightningインスタンスでローカルの重複レコードが検出された場合、 TiDB Lightning が誤って競合解決をスキップする可能性がある問題を修正します。
