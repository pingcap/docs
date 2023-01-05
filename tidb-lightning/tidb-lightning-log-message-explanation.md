---
title: TiDB Lightning Log Message Explanation
summary: Provide detailed explanation of log messages generated during the importing process using TiDB Lightning.
---

# Introduction

Based on a successful test data import, this document explains log messages of **v5.4 TiDB Lightning** with **Local Backend mode**, and dive deep to understand where the log comes from and what it actually represents. Users of TiDB Lightning can refer to this doc to have a better understanding of TiDB Lightning logs. We will continue working on other TiDB versions and improving the log messages.

We expect you are already familiar with TiDB Lightning, and read through the high level Lightning workflow doc in the [previous section](https://docs.pingcap.com/tidb/v5.4/tidb-lightning-overview). You can also refer to [glossary](https://docs.pingcap.com/tidb/v5.4/tidb-lightning-glossary) when you encounter an unfamiliar concept later in this doc.

You could use this doc to quickly navigate within Lightning source code to better understand how it works internally and what exactly the log message means for.

Note that some trivial logs are ignored. Only important logs are included in the following doc.

## Log Message Explanation 
```
[INFO] [info.go:49] ["Welcome to TiDB-Lightning"] [release-version=v5.4.0] [git-hash=55f3b24c1c9f506bd652ef1d162283541e428872] [git-branch=HEAD] [go-version=go1.16.6] [utc-build-time="2022-04-21 02:07:55"] [race-enabled=false]
```
[info.go:49](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/build/info.go#L49):
Print TiDB Lightning version information.

```
[INFO] [lightning.go:233] [cfg] [cfg="{\"id\":1650510440481957437,\"lightning\":{\"table-concurrency\":6,\"index-concurrency\":2,\"region-concurrency\":8,\"io-concurrency\":5,\"check-requirements\":true,\"meta-schema-name\":\"lightning_metadata\", ...
```
[lightning.go:233](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L233):
Print TiDB Lightning config information.

```
[INFO] [lightning.go:312] ["load data source start"] 
```
[lightning.go:312](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L312): Start to [scan data source dir or external storage]((https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L205)) defined in Lightning [mydumper data-source-dir config field](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L447), and load all data source file meta info into [internal data structure](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L82) for future usage.

```
[INFO] [loader.go:289] ["[loader] file is filtered by file router"] [path=metadata]
```
[loader.go:289](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L289): 
Print data source files skipped based on [file router rules](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L139) defined in Ligthning [mydumper files config field](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L452) or internal [default file router rules](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/router.go#L105) if [file rules are not defined](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/config/config.go#L847).

```
[INFO] [lightning.go:315] ["load data source completed"] [takeTime=273.964µs] []
``` 
[lightning.go:315](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/lightning.go#L315): Completed loading data source file info into [Mydumper File Loader](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/loader.go#L73) for later import.

```
[INFO] [checkpoints.go:977] ["open checkpoint file failed, going to create a new one"] [path=/tmp/tidb_lightning_checkpoint.pb] [error="open /tmp/tidb_lightning_checkpoint.pb: no such file or directory"]
```
[checkpoints.go:977](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/checkpoints/checkpoints.go#L977):
If Lightning uses files to store checkpoints, and can't find any local checkpoint file, Lightning will create a new checkpoint.

```
[INFO] [restore.go:444] ["the whole procedure start"]
```
[restore.go:444](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L444):
Start to import procedure.

```
[INFO] [restore.go:748] ["restore all schema start"]
```
[restore.go:748](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L748): Based on data source schema info, start to create database and table.

```
[INFO] [restore.go:767] ["restore all schema completed"] [takeTime=189.766729ms]  
```
[restore.go:767](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L767): Completed to create database and table.

```
[INFO] [check_info.go:680] ["datafile to check"] [db=sysbench] [table=sbtest1] [path=sysbench.sbtest1.000000000.sql]
```
[check_info.go:680](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L680):
As part of precheck, Lightning uses the first data file of each table to check if source data file and target cluster table schema are matched.

```
[INFO] [version.go:360] ["detect server version"] [type=TiDB] [version=5.4.0]
```
[version.go:360](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/version.go#L360):
Detect and print the current TiDB server version. To import data in local backend mode, TiDB with version higher than 4.0 is required.

We also need to check server version for [detecting data confilcts](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/version/version.go#L224).

```
[INFO] [check_info.go:995] ["sample file start"] [table=sbtest1]
```
[check_info.go:995](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L995): As part of precheck, it estimates source data size to determine: 
- [the local disk has enough space if Lighting is in local backend mode](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L462); 
- [the target cluster has enough space to store transformed kv pairs](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L102). 

It calculates the file size vs. kv pairs size ratio by sampling the first source data file of each table, and using the ratio times source data file size to estimate the size of transformed kv pairs.

```
[INFO] [check_info.go:1080] ["Sample source data"] [table=sbtest1] [IndexRatio=1.3037832180660969] [IsSourceOrder=true]  
```
[check_info.go:1080](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/check_info.go#L1080): Table source file size vs. kv pairs size ratio has been calculated.

```
[INFO] [pd.go:415] ["pause scheduler successful at beginning"] [name="[balance-region-scheduler,balance-leader-scheduler,balance-hot-region-scheduler]"] 
[INFO] [pd.go:423] ["pause configs successful at beginning"] [cfg="{\"enable-location-replacement\":\"false\",\"leader-schedule-limit\":4,\"max-merge-region-keys\":0,\"max-merge-region-size\":0,\"max-pending-peer-count\":2147483647,\"max-snapshot-count\":40,\"region-schedule-limit\":40}"]
```

[pd.go:415](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L415), [pd.go:423](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L423): In local backend mode, some [pd schedulers](https://docs.pingcap.com/tidb/stable/tidb-scheduling) are disabled and some [config settings are changed](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L417) to split and scatter tikv regions and ingest ssts.

```
[INFO] [restore.go:1683] ["switch to import mode"]
```
[restore.go:1683](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1683):
In local backend mode, it turns each TiKV node into import mode to speed up import process, but sacrifices its storage space. If it uses tidb backend mode, it does not need to switch TiKV to import mode.

```
[INFO] [restore.go:1462] ["restore table start"] [table=`sysbench`.`sbtest1`]
```
[restore.go:1462](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1462):
Start to restore table `sysbench`.`sbtest1`.  it concurrently restores multiple tables based on [index-concurrency](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1459) config. For each table, it concurrently restores data files in the table based on [region-concurrency](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L157) config.

```
[INFO] [table_restore.go:91] ["load engines and files start"] [table=`sysbench`.`sbtest1`]  
```
[table_restore.go:91](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L91): Start to logically [splits each table source data files](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L145) into multiple [chunks/table regions](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L283). Each table source data file will be [assigned to an engine](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L246) to process data files parallel in different engines.

```
[INFO] [region.go:241] [makeTableRegions] [filesCount=8] [MaxRegionSize=268435456] [RegionsCount=8] [BatchSize=107374182400] [cost=53.207µs]
```
[region.go:241](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/mydump/region.go#L241): Prints how many table data files(`filesCount`) have been processed, and the largest chunk size(`MaxRegionSize`) of CSV file, the number of generated table regions/chunks (`RegionsCount`), and the batchSize that we use to assign different engines to process data files.

```
[INFO] [table_restore.go:129] ["load engines and files completed"] [table=`sysbench`.`sbtest1`] [enginesCnt=2] [ime=75.563µs] []
```
[table_restore.go:129](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L129): Completed to logically split table data files.

```
[INFO] [backend.go:346] ["open engine"] [engineTag=`sysbench`.`sbtest1`:-1] [engineUUID=3942bab1-bd60-52e2-bf53-e17aebf962c6]
```
[backend.go:346](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L346): Engine id -1 represents the index engine. It will open the index engine at the beginning of [restore engines process](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L199) for storing transformed index kv pairs.

```
[INFO] [table_restore.go:270] ["import whole table start"] [table=`sysbench`.`sbtest1`]
```
[table_restore.go:270](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L270): Start to concurrently [restore different data engines of a given table](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L318).

```
[INFO] [table_restore.go:317] ["restore engine start"] [table=`sysbench`.`sbtest1`] [engineNumber=0]
```
[table_restore.go:317](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L317): Start to restore engine 0, non -1 engine id means data engine. Note that "restore enigne" and "import enigne" (appears later in the logs) refer to different processes. "restore engine" indicates the process of sending KV pairs to the allocated engine and sorting them, while "import engine" represents the process of ingesting sorted KV pairs in the engine file to the TiKV nodes.

```
[INFO] [table_restore.go:422] ["encode kv data and write start"] [table=`sysbench`.`sbtest1`] [engineNumber=0]
```
[table_restore.go:422](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L422): Start to [restore table data by chunks](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L386).

```
[INFO] [backend.go:346] ["open engine"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]
```
[backend.go:346](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L346): Open data engine id = 0 for storing transformed data kv pairs.

```
[INFO] [restore.go:2482] ["restore file start"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [fileIndex=0] [path=sysbench.sbtest1.000000000.sql:0] 
```
[restore.go:2482](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2482): 
This log may appear multiple times based on the importing table data size. Each log in this form indicates the start of restoring a chunk/table region. It concurrently [restores chunks](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L386) based on internal [region workers](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L532) defined by [region concurrency](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L402). For each chunk, the restoring process is as follows:
1. [encodes sql into kv pairs](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2389)
2. [writes kv pairs into data engine and index engine](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2179)

```
[INFO] [engine.go:777] ["write data to local DB"] [size=134256327] [kvs=621576] [files=1] [sstFileSize=108984502] [file=/home/centos/tidb-lightning-temp-data/sorted-kv-dir/d173bb2e-b753-5da9-b72e-13a49a46f5d7.sst/11e65bc1-04d0-4a39-9666-cae49cd013a9.sst] [firstKey=74800000000000003F5F728000000000144577] [lastKey=74800000000000003F5F7280000000001DC17E] 
```
[engine.go:777](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/engine.go#L777): Start to ingest generated SST files into the embeded engine. It [concurrently ingests SST files](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L624).

```
[INFO] [restore.go:2492] ["restore file completed"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [fileIndex=1] [path=sysbench.sbtest1.000000001.sql:0] [readDur=3.123667511s] [encodeDur=5.627497136s] [deliverDur=6.653498837s] [checksum="{cksum=6610977918434119862,size=336040251,kvs=2646056}"] [takeTime=15.474211783s] []
```
[restore.go:2492](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L2492): A chunk(a data source file defined by fileIndex=1) of a given table has been encoded and stored in engine.

```
[INFO] [table_restore.go:584] ["encode kv data and write completed"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [read=16] [written=2539933993] [takeTime=23.598662501s] []
[source code]
```
[table_restore.go:584](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L584): All chunks/table regions belong to engine `engineNumber=0` has been encoded and stored in engine `engineNumber=0`.

```
[INFO] [backend.go:438] ["engine close start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]   
[INFO] [backend.go:440] ["engine close completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [takeTime=2.879906ms] []
```
[backend.go:438](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L438): As [the final stage of engine restore](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L628), the data engine is closed and prepared for importing to tikv nodes.

```
[INFO] [table_restore.go:319] ["restore engine completed"] [table=`sysbench`.`sbtest1`] [engineNumber=0] [takeTime=27.031916498s] []
```
[table_restore.go:319](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L319): Completed to encode and write KV pairs to data engine 0.

```
[INFO] [table_restore.go:927] ["import and cleanup engine start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]   
[INFO] [backend.go:452] ["import start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [retryCnt=0]
```
[table_restore.go:927](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L927), [backend.go:452](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L452): Start to [import](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1311) kv pairs stored in the engine into the target TiKV node.

```
[INFO] [local.go:1023] ["split engine key ranges"] [engine=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [totalSize=2159933993] [totalCount=10000000] [firstKey=74800000000000003F5F728000000000000001] [lastKey=74800000000000003F5F728000000000989680] [ranges=22]
```
[local.go:1023](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1023): Before [import engine](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1331) procedure, it logically splits engine data into many ranges based on [TikvImporter.RegionSplitSize](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L927) config.

```
[INFO] [local.go:1336] ["start import engine"] [uuid=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [ranges=22] [count=10000000] [size=2159933993]
```
[local.go:1336](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1336): Start to import KV pairs into the engine by split ranges.

```
[INFO] [localhelper.go:89] ["split and scatter region"] [minKey=7480000000000000FF3F5F728000000000FF0000010000000000FA] [maxKey=7480000000000000FF3F5F728000000000FF9896810000000000FA] [retry=0]
```
[localhelper.go:89](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L89): Start to [split and scatter](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L65) tikv regions based on engine ranges minKey and maxKey.

```
[INFO] [localhelper.go:108] ["paginate scan regions"] [count=1] [start=7480000000000000FF3F5F728000000000FF0000010000000000FA] [end=7480000000000000FF3F5F728000000000FF9896810000000000FA]   
[INFO] [localhelper.go:116] ["paginate scan region finished"] [minKey=7480000000000000FF3F5F728000000000FF0000010000000000FA] [maxKey=7480000000000000FF3F5F728000000000FF9896810000000000FA] [regions=1]
```
[localhelper.go:108](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L108), [localhelper.go:116](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L108): Paginate [scans a batch of regions info](https://github.com/pingcap/tidb/blob/55f3b24c1c9f506bd652ef1d162283541e428872/br/pkg/restore/split.go#L413) on PD.

```
[INFO] [split_client.go:460] ["checking whether need to scatter"] [store=1] [max-replica=3]   
[INFO] [split_client.go:113] ["skipping scatter because the replica number isn't less than store count."]
```
[split_client.go:460](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split_client.go#L460), [split_client.go:113](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/restore/split_client.go#L113): Skips the scatter regions phase because max-replica <= number of TiKV stores. Scattering regions is the process that PD schedulers distribute regions and their replicas to different TiKV stores.

```
[INFO] [localhelper.go:240] ["batch split region"] [region_id=2] [keys=23] [firstKey="dIAAAAAAAAA/X3KAAAAAAAAAAQ=="] [end="dIAAAAAAAAA/X3KAAAAAAJiWgQ=="]
```
[localhelper.go:240](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L240): Completed to batch split tikv regions.

```
[INFO] [localhelper.go:319] ["waiting for scattering regions done"] [skipped_keys=0] [regions=23] [take=6.505195ms]
```
[localhelper.go:319](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/localhelper.go#L319): Completed to scatter Tikv regions.

```
[INFO] [local.go:1371] ["import engine success"] [uuid=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [size=2159933993] [kvs=10000000] [importedSize=2159933993] [importedCount=10000000]   
[INFO] [backend.go:455] ["import completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [retryCnt=0] [takeTime=20.179184481s] []
```
[local.go:1371](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/local/local.go#L1371), [backend.go:455](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L455): Completed to import KV pairs in the specific engine to TiKV stores.

``` 
[INFO] [backend.go:467] ["cleanup start"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7]   
[INFO] [backend.go:469] ["cleanup completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [takeTime=209.800004ms] []
```
[backend.go:467](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L467), [backend.go:469](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/backend/backend.go#L469): Clean up intermediate data during import phase. It will [cleanup](https://github.com/pingcap/tidb/blob/55f3b24c1c9f506bd652ef1d162283541e428872/br/pkg/lightning/backend/local/engine.go#L158) engine related meta info and db files.

```
[INFO] [table_restore.go:946] ["import and cleanup engine completed"] [engineTag=`sysbench`.`sbtest1`:0] [engineUUID=d173bb2e-b753-5da9-b72e-13a49a46f5d7] [takeTime=20.389269402s] []
```
[table_restore.go:946](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L946): Completed to import and cleanup.

```
[INFO] [table_restore.go:345] ["import whole table completed"] [table=`sysbench`.`sbtest1`] [takeTime=47.421324969s] []
```
[table_restore.go:345](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L345): Completed to import table data. Lightning converted all table data into KV pairs and ingested them into the TiKV clusters.

```
[INFO] [tidb.go:401] ["alter table auto_increment start"] [table=`sysbench`.`sbtest1`] [auto_increment=10000002]   
[INFO] [tidb.go:403] ["alter table auto_increment completed"] [table=`sysbench`.`sbtest1`] [auto_increment=10000002] [takeTime=82.225557ms] []
```
[tidb.go:401](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/tidb.go#L401), [tidb.go:403](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/tidb.go#L403): During the [post process](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L680) phase, it will [adjust table auto increment](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L703) to avoid introducing conflicts from newly added data.

```
[INFO] [restore.go:1466] ["restore table completed"] [table=`sysbench`.`sbtest1`] [takeTime=53.280464651s] []
```
[restore.go:1466](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1466): Completed to restore table.

```
[INFO] [restore.go:1396] ["add back PD leader&region schedulers"]    
[INFO] [pd.go:462] ["resume scheduler"] [schedulers="[balance-region-scheduler,balance-leader-scheduler,balance-hot-region-scheduler]"]    
[INFO] [pd.go:448] ["exit pause scheduler and configs successful"]    
[INFO] [pd.go:482] ["resume scheduler successful"] [scheduler=balance-region-scheduler]   
[INFO] [pd.go:573] ["restoring config"] [config="{\"enable-location-replacement\":\"true\",\"leader-schedule-limit\":4,\"max-merge-region-keys\":200000,\"max-merge-region-size\":20,\"max-pending-peer-count\":64,\"max-snapshot-count\":64,\"region-schedule-limit\":2048}"]
```
[restore.go:1396](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1396), [pd.go:462](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L462), [pd.go:448](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#L448), [pd.go:482](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#482), [pd.go:573](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/pdutil/pd.go#573): Resume paused PD schedulers before import, and reset PD configs.

```
[INFO] [restore.go:1244] ["cancel periodic actions"] [do=true]
```
[restore.go:1244](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1244): Start to cancel [periodic actions](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1087), which periodically prints the importing progress, and check whether TiKV is still in import mode.

```
[INFO] [restore.go:1688] ["switch to normal mode"]
```
[restore.go:1688](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1688): Switch TiKV from import mode to normal mode.

```
[INFO] [table_restore.go:736] ["local checksum"] [table=`sysbench`.`sbtest1`] [checksum="{cksum=9970490404295648092,size=2539933993,kvs=20000000}"]   
[INFO] [checksum.go:172] ["remote checksum start"] [table=sbtest1]   
[INFO] [checksum.go:175] ["remote checksum completed"] [table=sbtest1] [takeTime=2.817086758s] []   
[INFO] [table_restore.go:971] ["checksum pass"] [table=`sysbench`.`sbtest1`] [local="{cksum=9970490404295648092,size=2539933993,kvs=20000000}"]
```
[table_restore.go:736](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L736), [checksum.go:172](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/checksum.go#L172), [checksum.go:175](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/checksum.go#L175), [table_restore.go:971](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L971): [Compare local and remote checksum](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L736) to validate the imported data.

```
[INFO] [table_restore.go:976] ["analyze start"] [table=`sysbench`.`sbtest1`]   
[INFO] [table_restore.go:978] ["analyze completed"] [table=`sysbench`.`sbtest1`] [takeTime=26.410378251s] []
```
[table_restore.go:976](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L976), [table_restore.go:978](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/table_restore.go#L978): TiDB analyzes table to update the statistics that TiDB builds on tables and indexes. It is recommended to run `ANALYZE` after performing a large batch update or import of records, or when you notice that query execution plans are sub-optimal.

```
[INFO] [restore.go:1440] ["cleanup task metas"]
```
[restore.go:1440](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1440): Clean up import task metas, table metas and schema db if needed.

```
[INFO] [restore.go:1842] ["clean checkpoints start"] [keepAfterSuccess=remove] [taskID=1650516927467320997]   
[INFO] [restore.go:1850] ["clean checkpoints completed"] [keepAfterSuccess=remove] [taskID=1650516927467320997] [takeTime=18.543µs] []
```
[restore.go:1842](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1842), [restore.go:1850](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1850): Clean up checkpoints.

```
[INFO] [restore.go:473] ["the whole procedure completed"] [takeTime=1m22.804337152s] []
```
[restore.go:473](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L473): Completed the whole import procedure.

```
[INFO] [restore.go:1143] ["everything imported, stopping periodic actions"]
```
[restore.go:1143](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1143): Stop all [periodic actions](https://github.com/pingcap/tidb/blob/v5.4.0/br/pkg/lightning/restore/restore.go#L1087) after importing completed.