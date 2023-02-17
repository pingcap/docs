---
title: TiDB Lightning Log Message Explanation
summary: Provide detailed explanation of log messages generated during the importing process using TiDB Lightning.
---

# TiDB Lightningログ メッセージの説明 {#tidb-lightning-log-message-explanation}

このドキュメントでは、テスト データのインポートの成功に基づいて、**ローカル バックエンド モードを**使用した<strong>TiDB Lightning v5.4</strong>のログ メッセージについて説明し、ログがどこから来て、それが実際に何を表しているのかを深く掘り下げます。このドキュメントを参照して、 TiDB Lightningログをよりよく理解することができます。

このドキュメントを読むには、 TiDB Lightningに精通しており、 [TiDB Lightningの概要](/tidb-lightning/tidb-lightning-overview.md)で説明されているその高レベルのワークフローに関する予備知識があることが求められます。なじみのない用語に遭遇した場合は、 [用語集](/tidb-lightning/tidb-lightning-glossary.md)を参照できます。

このドキュメントを使用して、 TiDB Lightningソース コード内をすばやくナビゲートし、内部でどのように機能するか、およびログ メッセージが正確に何を意味するかをよりよく理解できます。

一部の些細なログは無視されることに注意してください。次のドキュメントには、重要なログのみが含まれています。

## ログメッセージの説明 {#log-message-explanation}

```
[INFO] [info.go:49] ["Welcome to TiDB-Lightning"] [release-version=v5.4.0] [git-hash=55f3b24c1c9f506bd652ef1d162283541e428872] [git-branch=HEAD] [go-version=go1.16.6] [utc-build-time="2022-04-21 02:07:55"] [race-enabled=false]
```

[info.go:49](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/build/info.go#L49) : TiDB Lightning のバージョン情報を出力します。

```
[INFO] [lightning.go:233] [cfg] [cfg="{\"id\":1650510440481957437,\"lightning\":{\"table-concurrency\":6,\"index-concurrency\":2,\"region-concurrency\":8,\"io-concurrency\":5,\"check-requirements\":true,\"meta-schema-name\":\"lightning_metadata\", ...
```

[lightning.go:233](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L233) : TiDB Lightning構成情報を出力します。

```
[INFO] [lightning.go:312] ["load data source start"] 
```

[lightning.go:312](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L312) : Lightning [mydumper data-source-dir 構成フィールド](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L447)で定義された[データ ソース ディレクトリまたは外部ストレージをスキャンします](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L205)から開始し、将来の使用のためにすべてのデータ ソース ファイルのメタ情報を[内部データ構造](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L82)に読み込みます。

```
[INFO] [loader.go:289] ["[loader] file is filtered by file router"] [path=metadata]
```

[loader.go:289](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L289) : [ファイル ルールが定義されていません](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L847)場合、Ligthning [mydumper ファイルの構成フィールド](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L452)または内部[デフォルトのファイル ルーター ルール](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/router.go#L105)で定義された[ファイル ルーター ルール](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L139)に基づいてスキップされたデータ ソース ファイルを印刷します。

```
[INFO] [lightning.go:315] ["load data source completed"] [takeTime=273.964µs] []
```

[lightning.go:315](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L315) : 後でインポートするためのデータ ソース ファイル情報の[Mydumper ファイルローダー](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L73)への読み込みが完了しました。

```
[INFO] [checkpoints.go:977] ["open checkpoint file failed, going to create a new one"] [path=/tmp/tidb_lightning_checkpoint.pb] [error="open /tmp/tidb_lightning_checkpoint.pb: no such file or directory"]
```

[checkpoints.go:977](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/checkpoints/checkpoints.go#L977) : Lightning がファイルを使用してチェックポイントを保存し、ローカル チェックポイント ファイルが見つからない場合、Lightning は新しいチェックポイントを作成します。

```
[INFO] [restore.go:444] ["the whole procedure start"]
```

[restore.go:444](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L444) : インポート手順を開始します。

```
[INFO] [restore.go:748] ["restore all schema start"]
```

[restore.go:748](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L748) : データ ソースのスキーマ情報に基づいて、データベースとテーブルの作成を開始します。

```
[INFO] [restore.go:767] ["restore all schema completed"] [takeTime=189.766729ms]  
```

[restore.go:767](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L767) : データベースとテーブルの作成が完了しました。

```
[INFO] [check_info.go:680] ["datafile to check"] [db=sysbench] [table=sbtest1] [path=sysbench.sbtest1.000000000.sql]
```

[check_info.go:680](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L680) : 事前チェックの一環として、Lightning は各テーブルの最初のデータ ファイルを使用して、ソース データ ファイルとターゲット クラスタ テーブル スキーマが一致しているかどうかをチェックします。

```
[INFO] [version.go:360] ["detect server version"] [type=TiDB] [version=5.4.0]
```

[version.go:360](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/version.go#L360) : 現在の TiDBサーバーのバージョンを検出して出力します。ローカル バックエンド モードでデータをインポートするには、4.0 以上のバージョンの TiDB が必要です。 [データ競合の検出](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/version.go#L224)のサーバーバージョンも確認する必要があります。

```
[INFO] [check_info.go:995] ["sample file start"] [table=sbtest1]
```

[check_info.go:995](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L995) : 事前チェックの一環として、ソース データのサイズを見積もり、以下を決定します。

-   [Lightning がローカル バックエンド モードの場合、ローカル ディスクには十分な容量があります](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L462) ;
-   [ターゲット クラスタには、変換された kv ペアを保存するのに十分なスペースがあります](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L102) .

各テーブルの最初のソース データ ファイルをサンプリングし、変換された kv ペアのサイズを見積もるためにソース データ ファイル サイズの比率を使用して、ファイル サイズと kv ペアのサイズの比率を計算します。

```
[INFO] [check_info.go:1080] ["Sample source data"] [table=sbtest1] [IndexRatio=1.3037832180660969] [IsSourceOrder=true]  
```

[check_info.go:1080](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L1080) : テーブル ソース ファイル サイズと kv ペアのサイズの比率が計算されました。

```
[INFO] [pd.go:415] ["pause scheduler successful at beginning"] [name="[balance-region-scheduler,balance-leader-scheduler,balance-hot-region-scheduler]"] 
[INFO] [pd.go:423] ["pause configs successful at beginning"] [cfg="{\"enable-location-replacement\":\"false\",\"leader-schedule-limit\":4,\"max-merge-region-keys\":0,\"max-merge-region-size\":0,\"max-pending-peer-count\":2147483647,\"max-snapshot-count\":40,\"region-schedule-limit\":40}"]
```

[pd.go:415](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L415) , [pd.go:423](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L423) : ローカル バックエンド モードでは、一部の[pdスケジューラー](https://docs.pingcap.com/tidb/stable/tidb-scheduling)が無効になり、一部の[構成設定が変更されました](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L417)が tikv リージョンを分割および分散し、sst を取り込みます。

```
[INFO] [restore.go:1683] ["switch to import mode"]
```

[restore.go:1683](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1683) : ローカル バックエンド モードでは、各 TiKV ノードをインポート モードにしてインポート プロセスを高速化しますが、そのストレージ スペースを犠牲にします。 tidb バックエンド モードを使用する場合、TiKV を[インポート モード](https://docs.pingcap.com/tidb/stable/tidb-lightning-glossary#import-mode)に切り替える必要はありません。

```
[INFO] [restore.go:1462] ["restore table start"] [table=`sysbench`.`sbtest1`]
```

[restore.go:1462](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1462) : テーブル`sysbench`の復元を開始します。 `sbtest1` . [インデックス同時実行](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1459)構成に基づいて複数のテーブルを同時に復元します。テーブルごとに、 [リージョン同時実行](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L157)構成に基づいてテーブル内のデータ ファイルを同時に復元します。

```
[INFO] [table_restore.go:91] ["load engines and files start"] [table=`sysbench`.`sbtest1`]  
```

[table_restore.go:91](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L91) : 論理的に[各テーブル ソース データ ファイルを分割します](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L145)を複数の[チャンク/テーブル領域](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L283)に開始します。各テーブル ソース データ ファイルは、異なるエンジンで並列にデータ ファイルを処理するために[エンジンに割り当てられた](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L246)になります。

```
[INFO] [region.go:241] [makeTableRegions] [filesCount=8] [MaxRegionSize=268435456] [RegionsCount=8] [BatchSize=107374182400] [cost=53.207µs]
```

[region.go:241](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L241) : 処理されたテーブル データ ファイルの量 ( `filesCount` )、CSV ファイルの最大チャンク サイズ ( `MaxRegionSize` )、生成されたテーブル リージョン/チャンクの数 ( `RegionsCount` )、および異なるエンジンを割り当てるために使用する batchSize を出力します。データファイルを処理します。

```
[INFO] [table_restore.go:129] ["load engines and files completed"] [table=`sysbench`.`sbtest1`] [enginesCnt=2] [ime=75.563µs] []
```

[table_restore.go:129](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L129) : 表データファイルの論理分割完了。

```
[INFO] [backend.go:346] ["open engine"] [engineTag=`sysbench`.`sbtest1`:-1] [engineUUID=3942bab1-bd60-52e2-bf53-e17aebf962c6]
```

[backend.go:346](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L346) : エンジン ID -1 はインデックス エンジンを表します。変換されたインデックス kv ペアを格納するために、 [エンジンの復元プロセス](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L199)の開始時にインデックス エンジンを開きます。

```
[INFO] [table_restore.go:270] ["import whole table start"] [table=`sysbench`.`sbtest1`]
```

[table_restore.go:270](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L270) : 同時に開始[特定のテーブルの異なるデータ エンジンを復元する](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L318) 。

```
[INFO] [table_restore.go:317] ["restore engine start"] [table=`sysbench`.`sbtest1`] [engineNumber=0]
```

[table_restore.go:317](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L317) : エンジン 0 の復元を開始します。-1 以外のエンジン ID はデータ エンジンを意味します。 「restore enigne」と「import enigne」（ログの後半に表示される）は異なるプロセスを指すことに注意してください。 「エンジンの復元」は、割り当てられたエンジンに KV ペアを送信してソートするプロセスを示し、「インポート エンジン」は、エンジン ファイル内のソートされた KV ペアを TiKV ノードに取り込むプロセスを表します。

```
[INFO] [table_restore.go:422] ["encode kv data and write start"] [table=`sysbench`.`sbtest1`] [engineNumber=0]
```

[table_restore.go:422](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L422) : [テーブル データをチャンク単位で復元する](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L386)から開始します。

```
[INFO] [backend.go:346] ["open engine"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]
```

[backend.go:346](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L346) : 変換されたデータ kv ペアを格納するためのオープン データ エンジン id = 0。

```
[INFO] [restore.go:2482] ["restore file start"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [fileIndex=0] [path=sysbench.sbtest1.000000000.sql:0] 
```

[restore.go:2482](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2482) : このログは、インポート テーブルのデータ サイズに基づいて複数回表示される場合があります。この形式の各ログは、チャンク/テーブル リージョンの復元の開始を示します。同時に[チャンクを復元します](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L386)によって定義された内部[地域労働者](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L532)に基づいて[リージョン同時実行](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L402) 。各チャンクの復元プロセスは次のとおりです。

1.  [SQL を kv ペアにエンコードします](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2389)
2.  [kv ペアをデータ エンジンとインデックス エンジンに書き込みます](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2179)

```
[INFO] [engine.go:777] ["write data to local DB"] [size=134256327] [kvs=621576] [files=1] [sstFileSize=108984502] [file=/home/centos/tidb-lightning-temp-data/sorted-kv-dir/d173bb2e-b753-5da9-b72e-13a49a46f5d7.sst/11e65bc1-04d0-4a39-9666-cae49cd013a9.sst] [firstKey=74800000000000003F5F728000000000144577] [lastKey=74800000000000003F5F7280000000001DC17E] 
```

[engine.go:777](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/engine.go#L777) : 生成された SST ファイルの埋め込みエンジンへの取り込みを開始します。それ[同時に SST ファイルを取り込みます](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L624) 。

```
[INFO] [restore.go:2492] ["restore file completed"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [fileIndex=1] [path=sysbench.sbtest1.000000001.sql:0] [readDur=3.123667511s] [encodeDur=5.627497136s] [deliverDur=6.653498837s] [checksum="{cksum=6610977918434119862,size=336040251,kvs=2646056}"] [takeTime=15.474211783s] []
```

[restore.go:2492](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2492) : 特定のテーブルのチャンク (fileIndex=1 で定義されたデータ ソース ファイル) がエンコードされ、エンジンに格納されています。

```
[INFO] [table_restore.go:584] ["encode kv data and write completed"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [read=16] [written=2539933993] [takeTime=23.598662501s] []
[source code]
```

[table_restore.go:584](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L584) : エンジン`engineNumber=0`に属するすべてのチャンク/テーブル領域がエンコードされ、エンジン`engineNumber=0`に格納されています。

```
[INFO] [backend.go:438] ["engine close start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]   
[INFO] [backend.go:440] ["engine close completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [takeTime=2.879906ms] []
```

[backend.go:438](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L438) : [エンジンレストアの最終段階](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L628)のように、データ エンジンは閉じられ、tikv ノードにインポートする準備ができています。

```
[INFO] [table_restore.go:319] ["restore engine completed"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [takeTime=27.031916498s] []
```

[table_restore.go:319](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L319) : KV ペアのエンコードとデータ エンジン 0 への書き込みが完了しました。

```
[INFO] [table_restore.go:927] ["import and cleanup engine start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]   
[INFO] [backend.go:452] ["import start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [retryCnt=0]
```

[table_restore.go:927](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L927) , [backend.go:452](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L452) : エンジンに保存されている[輸入](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1311) kv ペアからターゲットの TiKV ノードへ。

```
[INFO] [local.go:1023] ["split engine key ranges"] [engine=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [totalSize=2159933993] [totalCount=10000000] [firstKey=74800000000000003F5F728000000000000001] [lastKey=74800000000000003F5F728000000000989680] [ranges=22]
```

[local.go:1023](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1023) : [輸入エンジン](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1331)手順の前に、 [RegionSplitSize](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L927)構成に基づいてエンジン データをより小さな範囲に論理的に分割します。

```
[INFO] [local.go:1336] ["start import engine"] [uuid=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [ranges=22] [count=10000000] [size=2159933993]
```

[local.go:1336](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1336) : KV ペアのエンジンへの分割範囲によるインポートを開始します。

```
[INFO] [localhelper.go:89] ["split and scatter region"] [minKey=7480000000000000FF3F5F728000000000FF0000010000000000FA] [maxKey=7480000000000000FF3F5F728000000000FF9896810000000000FA] [retry=0]
```

[localhelper.go:89](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L89) : エンジン範囲の minKey と maxKey に基づいて[分裂して散る](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L65) tikv リージョンを開始します。

```
[INFO] [localhelper.go:108] ["paginate scan regions"] [count=1] [start=7480000000000000FF3F5F728000000000FF0000010000000000FA] [end=7480000000000000FF3F5F728000000000FF9896810000000000FA]   
[INFO] [localhelper.go:116] ["paginate scan region finished"] [minKey=7480000000000000FF3F5F728000000000FF0000010000000000FA] [maxKey=7480000000000000FF3F5F728000000000FF9896810000000000FA] [regions=1]
```

[localhelper.go:108](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L108) , [localhelper.go:116](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L108) : PD のページネーション[地域情報のバッチをスキャンします](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split.go#L413) 。

```
[INFO] [split_client.go:460] ["checking whether need to scatter"] [store=1] [max-replica=3]   
[INFO] [split_client.go:113] ["skipping scatter because the replica number isn't less than store count."]
```

[split_client.go:460](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split_client.go#L460) , [split_client.go:113](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split_client.go#L113) : max-replica &lt;= TiKV ストアの数であるため、分散領域フェーズをスキップします。リージョンのScatteringは、PD スケジューラがリージョンとそのレプリカを異なる TiKV ストアに分散するプロセスです。

```
[INFO] [localhelper.go:240] ["batch split region"] [region_id=2] [keys=23] [firstKey="dIAAAAAAAAA/X3KAAAAAAAAAAQ=="] [end="dIAAAAAAAAA/X3KAAAAAAJiWgQ=="]
```

[localhelper.go:240](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L240) : tikv リージョンのバッチ分割が完了しました。

```
[INFO] [localhelper.go:319] ["waiting for scattering regions done"] [skipped_keys=0] [regions=23] [take=6.505195ms]
```

[localhelper.go:319](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L319) : Tikv リージョンの分散が完了しました。

```
[INFO] [local.go:1371] ["import engine success"] [uuid=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [size=2159933993] [kvs=10000000] [importedSize=2159933993] [importedCount=10000000]   
[INFO] [backend.go:455] ["import completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [retryCnt=0] [takeTime=20.179184481s] []
```

[local.go:1371](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1371) , [backend.go:455](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L455) : 特定のエンジンの KV ペアを TiKV ストアにインポートすることが完了しました。

```
[INFO] [backend.go:467] ["cleanup start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]   
[INFO] [backend.go:469] ["cleanup completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [takeTime=209.800004ms] []
```

[backend.go:467](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L467) 、 [backend.go:469](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L469) : インポート フェーズ中に中間データをクリーンアップします。 [掃除](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/engine.go#L158)のエンジン関連のメタ情報と db ファイルになります。

```
[INFO] [table_restore.go:946] ["import and cleanup engine completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [takeTime=20.389269402s] []
```

[table_restore.go:946](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L946) : インポートとクリーンアップが完了しました。

```
[INFO] [table_restore.go:345] ["import whole table completed"] [table=`sysbench`.`sbtest1`] [takeTime=47.421324969s] []
```

[table_restore.go:345](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L345) : テーブル データのインポートが完了しました。 Lightning はすべてのテーブル データを KV ペアに変換し、それらを TiKV クラスターに取り込みました。

```
[INFO] [tidb.go:401] ["alter table auto_increment start"] [table=`sysbench`.`sbtest1`] [auto_increment=10000002]   
[INFO] [tidb.go:403] ["alter table auto_increment completed"] [table=`sysbench`.`sbtest1`] [auto_increment=10000002] [takeTime=82.225557ms] []
```

[tidb.go:401](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/tidb.go#L401) , [tidb.go:403](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/tidb.go#L403) : [後処理](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L680)フェーズの間、新しく追加されたデータから競合が発生しないよう[テーブルの自動インクリメントを調整する](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L703)します。

```
[INFO] [restore.go:1466] ["restore table completed"] [table=`sysbench`.`sbtest1`] [takeTime=53.280464651s] []
```

[restore.go:1466](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1466) : テーブルの復元が完了しました。

```
[INFO] [restore.go:1396] ["add back PD leader&region schedulers"]    
[INFO] [pd.go:462] ["resume scheduler"] [schedulers="[balance-region-scheduler,balance-leader-scheduler,balance-hot-region-scheduler]"]    
[INFO] [pd.go:448] ["exit pause scheduler and configs successful"]    
[INFO] [pd.go:482] ["resume scheduler successful"] [scheduler=balance-region-scheduler]   
[INFO] [pd.go:573] ["restoring config"] [config="{\"enable-location-replacement\":\"true\",\"leader-schedule-limit\":4,\"max-merge-region-keys\":200000,\"max-merge-region-size\":20,\"max-pending-peer-count\":64,\"max-snapshot-count\":64,\"region-schedule-limit\":2048}"]
```

[restore.go:1396](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1396) 、 [pd.go:462](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L462) 、 [pd.go:448](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L448) 、 [pd.go:482](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#482) 、 [pd.go:573](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#573) : インポート前に一時停止した PD スケジューラを再開し、PD 構成をリセットします。

```
[INFO] [restore.go:1244] ["cancel periodic actions"] [do=true]
```

[restore.go:1244](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1244) : インポートの進行状況を定期的に出力キャンセル[定期的なアクション](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1087)を開始し、TiKV がまだインポート モードであるかどうかを確認します。

```
[INFO] [restore.go:1688] ["switch to normal mode"]
```

[restore.go:1688](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1688) : TiKV をインポート モードから通常モードに切り替えます。

```
[INFO] [table_restore.go:736] ["local checksum"] [table=`sysbench`.`sbtest1`] [checksum="{cksum=9970490404295648092,size=2539933993,kvs=20000000}"]   
[INFO] [checksum.go:172] ["remote checksum start"] [table=sbtest1]   
[INFO] [checksum.go:175] ["remote checksum completed"] [table=sbtest1] [takeTime=2.817086758s] []   
[INFO] [table_restore.go:971] ["checksum pass"] [table=`sysbench`.`sbtest1`] [local="{cksum=9970490404295648092,size=2539933993,kvs=20000000}"]
```

[table_restore.go:736](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L736) 、 [checksum.go:172](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/checksum.go#L172) 、 [checksum.go:175](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/checksum.go#L175) 、 [table_restore.go:971](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L971) : [ローカルとリモートのチェックサムを比較する](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L736)は、インポートされたデータを検証します。

```
[INFO] [table_restore.go:976] ["analyze start"] [table=`sysbench`.`sbtest1`]   
[INFO] [table_restore.go:978] ["analyze completed"] [table=`sysbench`.`sbtest1`] [takeTime=26.410378251s] []
```

[table_restore.go:976](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L976) , [table_restore.go:978](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L978) : TiDB はテーブルを分析して、TiDB がテーブルとインデックスに基づいて構築する統計を更新します。大規模なバッチ更新またはレコードのインポートを実行した後、またはクエリ実行プランが最適ではないことに気付いた場合は、 `ANALYZE`実行することをお勧めします。

```
[INFO] [restore.go:1440] ["cleanup task metas"]
```

[restore.go:1440](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1440) : 必要に応じて、インポート タスク メタ、テーブル メタ、およびスキーマ データベースをクリーンアップします。

```
[INFO] [restore.go:1842] ["clean checkpoints start"] [keepAfterSuccess=remove] [taskID=1650516927467320997]   
[INFO] [restore.go:1850] ["clean checkpoints completed"] [keepAfterSuccess=remove] [taskID=1650516927467320997] [takeTime=18.543µs] []
```

[restore.go:1842](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1842) , [restore.go:1850](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1850) : チェックポイントをクリーンアップします。

```
[INFO] [restore.go:473] ["the whole procedure completed"] [takeTime=1m22.804337152s] []
```

[restore.go:473](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L473) : インポート手順全体が完了しました。

```
[INFO] [restore.go:1143] ["everything imported, stopping periodic actions"]
```

[restore.go:1143](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1143) : インポートが完了した後、 [定期的なアクション](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1087)すべてを停止します。
