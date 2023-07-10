---
title: TiDB Lightning Log Message Explanation
summary: Provide detailed explanation of log messages generated during the importing process using TiDB Lightning.
---

# TiDB Lightningログ メッセージの説明 {#tidb-lightning-log-message-explanation}

このドキュメントでは、成功したテスト データのインポートに基づいて、**ローカル バックエンド モード**の**TiDB Lightning v5.4**のログ メッセージについて説明します。各ログ メッセージの起源と意味を深く掘り下げます。 TiDB Lightningログをより深く理解するには、このドキュメントを参照してください。

このドキュメントを完全に理解するには、 TiDB Lightningに精通しており、 [<a href="/tidb-lightning/tidb-lightning-overview.md">TiDB Lightningの概要</a>](/tidb-lightning/tidb-lightning-overview.md)で説明されているその高レベルのワークフローについての事前知識がある必要があります。馴染みのない用語が出てきた場合は、 [<a href="/tidb-lightning/tidb-lightning-glossary.md">用語集</a>](/tidb-lightning/tidb-lightning-glossary.md)を参照してください。

このドキュメントを使用すると、 TiDB Lightningソース コードをすばやくナビゲートし、その内部動作を洞察し、各ログ メッセージの背後にある重要性を理解することができます。

このドキュメントには重要なログのみが含まれていることに注意してください。重要性の低いログは省略されています。

## ログメッセージの説明 {#log-message-explanation}

```
[INFO] [info.go:49] ["Welcome to TiDB-Lightning"] [release-version=v5.4.0] [git-hash=55f3b24c1c9f506bd652ef1d162283541e428872] [git-branch=HEAD] [go-version=go1.16.6] [utc-build-time="2022-04-21 02:07:55"] [race-enabled=false]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/build/info.go#L49">info.go:49</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/build/info.go#L49) : TiDB Lightning のバージョン情報を出力します。

```
[INFO] [lightning.go:233] [cfg] [cfg="{\"id\":1650510440481957437,\"lightning\":{\"table-concurrency\":6,\"index-concurrency\":2,\"region-concurrency\":8,\"io-concurrency\":5,\"check-requirements\":true,\"meta-schema-name\":\"lightning_metadata\", ...
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L233">ライトニングゴー:233</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L233) : TiDB Lightning構成情報を出力します。

```
[INFO] [lightning.go:312] ["load data source start"]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L312">ライトニングゴー:312</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L312) : TiDB Lightning [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L447">mydumper `data-source-dir`設定フィールド</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L447)で定義されている[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L205">データソースディレクトリまたは外部storageをスキャンします</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L205)から開始し、将来の使用に備えてすべてのデータ ソース ファイルのメタ情報を[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L82">内部データ構造</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L82)にロードします。

```
[INFO] [loader.go:289] ["[loader] file is filtered by file router"] [path=metadata]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L289">ローダー.go:289</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L289) : TiDB Lightning [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L452">mydumper ファイルの設定フィールド</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L452)で定義された[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L139">ファイルルーターのルール</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L139) 、または[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L847">ファイルルールが定義されていません</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L847)の場合は内部[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/router.go#L105">デフォルトのファイルルータールール</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/router.go#L105)に基づいてスキップされた印刷データ ソース ファイル。

```
[INFO] [lightning.go:315] ["load data source completed"] [takeTime=273.964µs] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L315">ライトニングゴー:315</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L315) : 後でインポートするために、データ ソース ファイル情報の[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L73">Mydumper ファイルローダー</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L73)へのロードが完了しました。

```
[INFO] [checkpoints.go:977] ["open checkpoint file failed, going to create a new one"] [path=/tmp/tidb_lightning_checkpoint.pb] [error="open /tmp/tidb_lightning_checkpoint.pb: no such file or directory"]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/checkpoints/checkpoints.go#L977">チェックポイント.go:977</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/checkpoints/checkpoints.go#L977) : TiDB Lightning がファイルを使用してチェックポイントを保存し、ローカル チェックポイント ファイルが見つからない場合、 TiDB Lightning は新しいチェックポイントを作成します。

```
[INFO] [restore.go:444] ["the whole procedure start"]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L444">復元.go:444</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L444) : インポート手順を開始します。

```
[INFO] [restore.go:748] ["restore all schema start"]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L748">復元.go:748</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L748) : データ ソース スキーマ情報に基づいて、データベースとテーブルの作成を開始します。

```
[INFO] [restore.go:767] ["restore all schema completed"] [takeTime=189.766729ms]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L767">復元.go:767</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L767) : データベースとテーブルの作成が完了しました。

```
[INFO] [check_info.go:680] ["datafile to check"] [db=sysbench] [table=sbtest1] [path=sysbench.sbtest1.000000000.sql]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L680">check_info.go:680</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L680) : 事前チェックの一環として、 TiDB Lightning は各テーブルの最初のデータ ファイルを使用して、ソース データ ファイルとターゲット クラスタ テーブルのスキーマが一致するかどうかをチェックします。

```
[INFO] [version.go:360] ["detect server version"] [type=TiDB] [version=5.4.0]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/version.go#L360">バージョン.go:360</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/version.go#L360) : 現在の TiDBサーバーのバージョンを検出して出力します。ローカル バックエンド モードでデータをインポートするには、TiDB v4.0 以降が必要です。同じバージョンチェックが[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/version.go#L224">データ競合の検出</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/version.go#L224)にも実装されています。

```
[INFO] [check_info.go:995] ["sample file start"] [table=sbtest1]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L995">check_info.go:995</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L995) : 事前チェックの一環として、 TiDB Lightning はソース データ サイズを推定して、以下を決定します。

-   [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L462">TiDB Lightning がローカル バックエンド モードの場合、ローカル ディスクに十分なスペースがあるかどうか</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L462) 。
-   [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L102">ターゲット クラスターに、変換された KV ペアを保存するのに十分なスペースがあるかどうか</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L102) 。

TiDB Lightning は、各テーブルの最初のソース データ ファイルをサンプリングし、そのサイズと KV ペアのサイズの比率を計算することにより、変換された KV ペアのサイズを推定します。次に、その比率にソース データ ファイルのサイズを乗算して、変換された KV ペアのサイズを推定します。

```
[INFO] [check_info.go:1080] ["Sample source data"] [table=sbtest1] [IndexRatio=1.3037832180660969] [IsSourceOrder=true]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L1080">check_info.go:1080</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L1080) : テーブルソースファイルのサイズと KV ペアのサイズの比率が計算されています。

```
[INFO] [pd.go:415] ["pause scheduler successful at beginning"] [name="[balance-region-scheduler,balance-leader-scheduler,balance-hot-region-scheduler]"]
[INFO] [pd.go:423] ["pause configs successful at beginning"] [cfg="{\"enable-location-replacement\":\"false\",\"leader-schedule-limit\":4,\"max-merge-region-keys\":0,\"max-merge-region-size\":0,\"max-pending-peer-count\":2147483647,\"max-snapshot-count\":40,\"region-schedule-limit\":40}"]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L415">PD.GO:415</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L415) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L423">PD.GO:423</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L423) : ローカル バックエンド モードでは、TiKV リージョンを分割および分散し、SST を取り込むために、一部の[<a href="https://docs.pingcap.com/tidb/stable/tidb-scheduling">PDスケジューラ</a>](https://docs.pingcap.com/tidb/stable/tidb-scheduling)が無効になり、一部の[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L417">設定項目が変更される</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L417)無効になります。

```
[INFO] [restore.go:1683] ["switch to import mode"]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1683">復元.go:1683</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1683) : ローカル バックエンド モードでは、 TiDB Lightning は各 TiKV ノードをインポート モードに切り替えてインポート プロセスを高速化しますが、そのstorageスペースが犠牲になります。 tidb バックエンド モードを使用する場合、 TiKV を[<a href="https://docs.pingcap.com/tidb/stable/tidb-lightning-glossary#import-mode">インポートモード</a>](https://docs.pingcap.com/tidb/stable/tidb-lightning-glossary#import-mode)に切り替える必要はありません。

```
[INFO] [restore.go:1462] ["restore table start"] [table=`sysbench`.`sbtest1`]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1462">復元.go:1462</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1462) : テーブル`sysbench`の復元を開始します。 `sbtest1` ． TiDB Lightning は、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1459">`index-concurrency`</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1459)構成に基づいて複数のテーブルを同時に復元します。テーブルごとに、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L157">`region-concurrency`</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L157)構成に基づいてテーブル内のデータ ファイルを同時に復元します。

```
[INFO] [table_restore.go:91] ["load engines and files start"] [table=`sysbench`.`sbtest1`]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L91">table_restore.go:91</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L91) : 論理的に[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L145">各テーブルのソース データ ファイルを分割する</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L145)倍数[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L283">チャンク/テーブル領域</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L283)に変換し始めます。各テーブルのソース データ ファイルは[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L246">エンジンに割り当てられる</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L246)になるため、ソース データ ファイルは異なるエンジン間で並行して処理できます。

```
[INFO] [region.go:241] [makeTableRegions] [filesCount=8] [MaxRegionSize=268435456] [RegionsCount=8] [BatchSize=107374182400] [cost=53.207µs]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L241">地域.go:241</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L241) : 処理されたテーブル データ ファイルの量 ( `filesCount` )、CSV ファイルの最大チャンク サイズ ( `MaxRegionSize` )、生成されたテーブル領域/チャンクの数 ( `RegionsCount` )、および割り当てに使用される`batchSize`を出力します。データファイルを処理するためのさまざまなエンジン。

```
[INFO] [table_restore.go:129] ["load engines and files completed"] [table=`sysbench`.`sbtest1`] [enginesCnt=2] [ime=75.563µs] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L129">table_restore.go:129</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L129) : テーブルデータファイルの論理分割が完了しました。

```
[INFO] [backend.go:346] ["open engine"] [engineTag=`sysbench`.`sbtest1`:-1] [engineUUID=3942bab1-bd60-52e2-bf53-e17aebf962c6]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L346">バックエンド.go:346</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L346) : ID `-1`のエンジンはインデックス エンジンです。変換されたインデックス KV ペアを保存するために、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L199">エンジンのプロセスを復元する</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L199)のインデックス エンジンが最初に開きます。

```
[INFO] [table_restore.go:270] ["import whole table start"] [table=`sysbench`.`sbtest1`]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L270">table_restore.go:270</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L270) : [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L318">特定のテーブルのさまざまなデータ エンジンを復元する</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L318)を同時に開始します。

```
[INFO] [table_restore.go:317] ["restore engine start"] [table=`sysbench`.`sbtest1`] [engineNumber=0]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L317">table_restore.go:317</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L317) : エンジン`0`の復元を開始します。 `-1`以外のエンジン ID はデータ エンジンを示します。 「復元エンジン」と「インポート エンジン」（ログの後半に表示されます）は異なるプロセスを指すことに注意してください。 「復元エンジン」は、割り当てられたエンジンに KV ペアを送信して並べ替えるプロセスを示し、「インポート エンジン」は、エンジン ファイル内の並べ替えられた KV ペアを TiKV ノードに取り込むプロセスを示します。

```
[INFO] [table_restore.go:422] ["encode kv data and write start"] [table=`sysbench`.`sbtest1`] [engineNumber=0]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L422">table_restore.go:422</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L422) : [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L386">テーブルデータをチャンク単位で復元する</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L386)まで開始します。

```
[INFO] [backend.go:346] ["open engine"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L346">バックエンド.go:346</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L346) : 変換されたデータ KV ペアを保存するために、ID = 0 でデータ エンジンを開きます。

```
[INFO] [restore.go:2482] ["restore file start"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [fileIndex=0] [path=sysbench.sbtest1.000000000.sql:0]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2482">復元.go:2482</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2482) : このログは、インポートされたテーブルのデータ サイズに基づいて複数回表示される場合があります。この形式の各ログは、チャンク/テーブル領域の復元の開始を示します。同時に[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L386">チャンクを復元します</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L386) [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L402">リージョン同時実行</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L402)によって定義された内部[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L532">地域労働者</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L532)に基づいています。各チャンクの復元プロセスは次のとおりです。

1.  [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2389">SQLをKVペアにエンコードします</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2389) 。
2.  [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2179">KV ペアをデータ エンジンとインデックス エンジンに書き込みます</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2179) 。

```
[INFO] [engine.go:777] ["write data to local DB"] [size=134256327] [kvs=621576] [files=1] [sstFileSize=108984502] [file=/home/centos/tidb-lightning-temp-data/sorted-kv-dir/d173bb2e-b753-5da9-b72e-13a49a46f5d7.sst/11e65bc1-04d0-4a39-9666-cae49cd013a9.sst] [firstKey=74800000000000003F5F728000000000144577] [lastKey=74800000000000003F5F7280000000001DC17E]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/engine.go#L777">エンジン.go:777</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/engine.go#L777) : 生成された SST ファイルの組み込みエンジンへの取り込みを開始します。それ[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L624">SST ファイルを同時に取り込む</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L624) ．

```
[INFO] [restore.go:2492] ["restore file completed"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [fileIndex=1] [path=sysbench.sbtest1.000000001.sql:0] [readDur=3.123667511s] [encodeDur=5.627497136s] [deliverDur=6.653498837s] [checksum="{cksum=6610977918434119862,size=336040251,kvs=2646056}"] [takeTime=15.474211783s] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2492">復元.go:2492</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2492) : 指定されたテーブルのチャンク ( `fileIndex=1`で定義されたデータ ソース ファイル) がエンコードされ、エンジンに格納されています。

```
[INFO] [table_restore.go:584] ["encode kv data and write completed"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [read=16] [written=2539933993] [takeTime=23.598662501s] []
[source code]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L584">table_restore.go:584</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L584) : エンジン`engineNumber=0`に属するすべてのチャンク/テーブル領域がエンコードされ、エンジン`engineNumber=0`に保存されています。

```
[INFO] [backend.go:438] ["engine close start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]
[INFO] [backend.go:440] ["engine close completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [takeTime=2.879906ms] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L438">バックエンド.go:438</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L438) : [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L628">エンジンレストアの最終段階</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L628)と同様に、データ エンジンが閉じられ、TiKV ノードへのインポートの準備が整います。

```
[INFO] [table_restore.go:319] ["restore engine completed"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [takeTime=27.031916498s] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L319">table_restore.go:319</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L319) : KV ペアのエンコードとデータ エンジン 0 への書き込みが完了しました。

```
[INFO] [table_restore.go:927] ["import and cleanup engine start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]
[INFO] [backend.go:452] ["import start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [retryCnt=0]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L927">table_restore.go:927</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L927) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L452">バックエンド.go:452</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L452) : エンジンに保存されている[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1311">輸入</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1311) KV ペアをターゲット TiKV ノードに開始します。

```
[INFO] [local.go:1023] ["split engine key ranges"] [engine=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [totalSize=2159933993] [totalCount=10000000] [firstKey=74800000000000003F5F728000000000000001] [lastKey=74800000000000003F5F728000000000989680] [ranges=22]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1023">ローカル.ゴー:1023</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1023) : [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1331">インポートエンジン</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1331)手順の前に、 TiDB Lightning は[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L927">`RegionSplitSize`</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L927)構成に基づいてエンジン データをより小さい範囲に論理的に分割します。

```
[INFO] [local.go:1336] ["start import engine"] [uuid=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [ranges=22] [count=10000000] [size=2159933993]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1336">local.go:1336</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1336) : 範囲を分割して KV ペアのエンジンへのインポートを開始します。

```
[INFO] [localhelper.go:89] ["split and scatter region"] [minKey=7480000000000000FF3F5F728000000000FF0000010000000000FA] [maxKey=7480000000000000FF3F5F728000000000FF9896810000000000FA] [retry=0]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L89">ローカルヘルパー.go:89</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L89) : エンジン範囲`minKey`および`maxKey`に基づいて[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L65">分裂して飛び散る</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L65) TiKV 領域に開始します。

```
[INFO] [localhelper.go:108] ["paginate scan regions"] [count=1] [start=7480000000000000FF3F5F728000000000FF0000010000000000FA] [end=7480000000000000FF3F5F728000000000FF9896810000000000FA]
[INFO] [localhelper.go:116] ["paginate scan region finished"] [minKey=7480000000000000FF3F5F728000000000FF0000010000000000FA] [maxKey=7480000000000000FF3F5F728000000000FF9896810000000000FA] [regions=1]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L108">ローカルヘルパー.go:108</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L108) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L108">ローカルヘルパー.go:116</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L108) : PD の[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split.go#L413">地域情報のバッチのスキャン</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split.go#L413)をページネーションします。

```
[INFO] [split_client.go:460] ["checking whether need to scatter"] [store=1] [max-replica=3]
[INFO] [split_client.go:113] ["skipping scatter because the replica number isn't less than store count."]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split_client.go#L460">分割クライアント.go:460</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split_client.go#L460) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split_client.go#L113">分割クライアント.go:113</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split_client.go#L113) : `max-replica` &gt;= TiKV ストアの数であるため、散乱領域フェーズをスキップします。Scatteringリージョンは、PD スケジューラがリージョンとそのレプリカを異なる TiKV ストアに分散するプロセスです。

```
[INFO] [localhelper.go:240] ["batch split region"] [region_id=2] [keys=23] [firstKey="dIAAAAAAAAA/X3KAAAAAAAAAAQ=="] [end="dIAAAAAAAAA/X3KAAAAAAJiWgQ=="]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L240">ローカルヘルパー.go:240</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L240) : TiKV リージョンのバッチ分割が完了しました。

```
[INFO] [localhelper.go:319] ["waiting for scattering regions done"] [skipped_keys=0] [regions=23] [take=6.505195ms]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L319">ローカルヘルパー.go:319</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L319) : TiKV 領域の分散が完了しました。

```
[INFO] [local.go:1371] ["import engine success"] [uuid=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [size=2159933993] [kvs=10000000] [importedSize=2159933993] [importedCount=10000000]
[INFO] [backend.go:455] ["import completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [retryCnt=0] [takeTime=20.179184481s] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1371">local.go:1371</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1371) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L455">バックエンド.go:455</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L455) : 特定のエンジンの KV ペアを TiKV ストアにインポートする作業が完了しました。

```
[INFO] [backend.go:467] ["cleanup start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]
[INFO] [backend.go:469] ["cleanup completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [takeTime=209.800004ms] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L467">バックエンド.go:467</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L467) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L469">バックエンド.go:469</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L469) : インポート段階で中間データをクリーンアップします。 TiDB Lightning は、エンジン関連のメタ情報と DB ファイルを[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/engine.go#L158">掃除</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/engine.go#L158)します。

```
[INFO] [table_restore.go:946] ["import and cleanup engine completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [takeTime=20.389269402s] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L946">table_restore.go:946</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L946) : インポートとクリーンアップが完了しました。

```
[INFO] [table_restore.go:345] ["import whole table completed"] [table=`sysbench`.`sbtest1`] [takeTime=47.421324969s] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L345">table_restore.go:345</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L345) : テーブルデータのインポートが完了しました。 TiDB Lightning は、すべてのテーブル データを KV ペアに変換し、TiKV クラスターに取り込みました。

```
[INFO] [tidb.go:401] ["alter table auto_increment start"] [table=`sysbench`.`sbtest1`] [auto_increment=10000002]
[INFO] [tidb.go:403] ["alter table auto_increment completed"] [table=`sysbench`.`sbtest1`] [auto_increment=10000002] [takeTime=82.225557ms] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/tidb.go#L401">tidb.go:401</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/tidb.go#L401) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/tidb.go#L403">tidb.go:403</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/tidb.go#L403) : [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L680">後処理</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L680)フェーズでは、新しく追加されたデータによる競合を避けるために[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L703">テーブルの自動インクリメントIDを調整する</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L703)になります。

```
[INFO] [restore.go:1466] ["restore table completed"] [table=`sysbench`.`sbtest1`] [takeTime=53.280464651s] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1466">復元.go:1466</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1466) : テーブルの復元が完了しました。

```
[INFO] [restore.go:1396] ["add back PD leader&region schedulers"]
[INFO] [pd.go:462] ["resume scheduler"] [schedulers="[balance-region-scheduler,balance-leader-scheduler,balance-hot-region-scheduler]"]
[INFO] [pd.go:448] ["exit pause scheduler and configs successful"]
[INFO] [pd.go:482] ["resume scheduler successful"] [scheduler=balance-region-scheduler]
[INFO] [pd.go:573] ["restoring config"] [config="{\"enable-location-replacement\":\"true\",\"leader-schedule-limit\":4,\"max-merge-region-keys\":200000,\"max-merge-region-size\":20,\"max-pending-peer-count\":64,\"max-snapshot-count\":64,\"region-schedule-limit\":2048}"]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1396">復元.go:1396</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1396) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L462">PD.GO:462</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L462) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L448">PD.GO:448</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L448) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#482">PD.GO:482</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#482) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#573">PD.GO:573</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#573) : インポート前に一時停止した PD スケジューラを再開し、PD 構成をリセットします。

```
[INFO] [restore.go:1244] ["cancel periodic actions"] [do=true]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1244">復元.go:1244</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1244) : インポートの進行状況を定期的に出力[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1087">定期的なアクション</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1087)キャンセルを開始し、TiKV がまだインポート モードであるかどうかを確認します。

```
[INFO] [restore.go:1688] ["switch to normal mode"]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1688">復元.go:1688</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1688) : TiKV をインポート モードから通常モードに切り替えます。

```
[INFO] [table_restore.go:736] ["local checksum"] [table=`sysbench`.`sbtest1`] [checksum="{cksum=9970490404295648092,size=2539933993,kvs=20000000}"]
[INFO] [checksum.go:172] ["remote checksum start"] [table=sbtest1]
[INFO] [checksum.go:175] ["remote checksum completed"] [table=sbtest1] [takeTime=2.817086758s] []
[INFO] [table_restore.go:971] ["checksum pass"] [table=`sysbench`.`sbtest1`] [local="{cksum=9970490404295648092,size=2539933993,kvs=20000000}"]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L736">table_restore.go:736</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L736) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/checksum.go#L172">チェックサム.go:172</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/checksum.go#L172) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/checksum.go#L175">チェックサム.go:175</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/checksum.go#L175) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L971">table_restore.go:971</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L971) : [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L736">ローカルとリモートのチェックサムを比較する</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L736)は、インポートされたデータを検証します。

```
[INFO] [table_restore.go:976] ["analyze start"] [table=`sysbench`.`sbtest1`]
[INFO] [table_restore.go:978] ["analyze completed"] [table=`sysbench`.`sbtest1`] [takeTime=26.410378251s] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L976">table_restore.go:976</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L976) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L978">table_restore.go:978</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L978) : TiDB はテーブルを分析して、TiDB がテーブルとインデックスに基づいて構築する統計を更新します。大規模なバッチ更新またはレコードのインポートを実行した後、またはクエリ実行プランが最適ではないことに気づいた場合は、 `ANALYZE`実行することをお勧めします。

```
[INFO] [restore.go:1440] ["cleanup task metas"]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1440">復元.go:1440</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1440) : 必要に応じて、インポート タスク メタ、テーブル メタ、およびスキーマ データベースをクリーンアップします。

```
[INFO] [restore.go:1842] ["clean checkpoints start"] [keepAfterSuccess=remove] [taskID=1650516927467320997]
[INFO] [restore.go:1850] ["clean checkpoints completed"] [keepAfterSuccess=remove] [taskID=1650516927467320997] [takeTime=18.543µs] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1842">復元.go:1842</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1842) 、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1850">復元.go:1850</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1850) : チェックポイントをクリーンアップします。

```
[INFO] [restore.go:473] ["the whole procedure completed"] [takeTime=1m22.804337152s] []
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L473">復元.go:473</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L473) : インポート手順がすべて完了しました。

```
[INFO] [restore.go:1143] ["everything imported, stopping periodic actions"]
```

[<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1143">復元.go:1143</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1143) : インポート完了後、 [<a href="https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1087">定期的なアクション</a>](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1087)をすべて停止します。
