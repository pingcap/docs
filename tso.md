---
title: TimeStamp Oracle (TSO) in TiDB
summary: TiDB の TimeStamp Oracle (TSO) について学習します。
---

# TiDB のタイムスタンプ Oracle (TSO) {#timestamp-oracle-tso-in-tidb}

TiDB では、配置Driver(PD) が、クラスター内のさまざまなコンポーネントにタイムスタンプを割り当てる上で重要な役割を果たします。これらのタイムスタンプは、トランザクションとデータに時間マーカーを割り当てる際に重要な役割を果たします。これは、TiDB 内で[パーコレーター](https://research.google/pubs/large-scale-incremental-processing-using-distributed-transactions-and-notifications/)モデルを有効にするために不可欠なメカニズムです。Percolator モデルは、 [マルチバージョン同時実行制御 (MVCC)](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc)と[取引管理](/transaction-overview.md)サポートするために使用されます。

次の例は、TiDB で現在の TSO を取得する方法を示しています。

```sql
BEGIN; SET @ts := @@tidb_current_ts; ROLLBACK;
Query OK, 0 rows affected (0.0007 sec)
Query OK, 0 rows affected (0.0002 sec)
Query OK, 0 rows affected (0.0001 sec)

SELECT @ts;
+--------------------+
| @ts                |
+--------------------+
| 443852055297916932 |
+--------------------+
1 row in set (0.00 sec)
```

TSO タイムスタンプはトランザクションごとに割り当てられるため、これは`BEGIN; ...; ROLLBACK`のトランザクションで実行されることに注意してください。

前の例で取得した TSO タイムスタンプは 10 進数です。次の SQL関数を使用してタイムスタンプを解析できます。

-   [`TIDB_PARSE_TSO()`](/functions-and-operators/tidb-functions.md#tidb_parse_tso)
-   [`TIDB_PARSE_TSO_LOGICAL()`](/functions-and-operators/tidb-functions.md)

```sql
SELECT TIDB_PARSE_TSO(443852055297916932);
+------------------------------------+
| TIDB_PARSE_TSO(443852055297916932) |
+------------------------------------+
| 2023-08-27 20:33:41.687000         |
+------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT TIDB_PARSE_TSO_LOGICAL(443852055297916932);
+--------------------------------------------+
| TIDB_PARSE_TSO_LOGICAL(443852055297916932) |
+--------------------------------------------+
|                                          4 |
+--------------------------------------------+
1 row in set (0.00 sec)
```

次の例は、TSO タイムスタンプがバイナリでどのように見えるかを示しています。

```shell
0000011000101000111000010001011110111000110111000000000000000100  ← This is 443852055297916932 in binary
0000011000101000111000010001011110111000110111                    ← The first 46 bits are the physical timestamp
                                              000000000000000100  ← The last 18 bits are the logical timestamp
```

TSO タイムスタンプには 2 つの部分があります。

-   物理タイムスタンプ: 1970 年 1 月 1 日からのミリ秒単位の UNIX タイムスタンプ。
-   論理タイムスタンプ: 同じミリ秒内に複数のタイムスタンプが必要なシナリオや、特定のイベントによってクロックの進行が逆転する可能性があるシナリオで使用される増分カウンター。このような場合、物理タイムスタンプは変更されませんが、論理タイムスタンプは着実に進みます。このメカニズムにより、常に前進し、決して後退しない TSO タイムスタンプの整合性が確保されます。

この知識があれば、SQL で TSO タイムスタンプをもう少し詳しく調べることができます。

```sql
SELECT @ts, UNIX_TIMESTAMP(NOW(6)), (@ts >> 18)/1000, FROM_UNIXTIME((@ts >> 18)/1000), NOW(6), @ts & 0x3FFFF\G
*************************** 1. row ***************************
                            @ts: 443852055297916932
         UNIX_TIMESTAMP(NOW(6)): 1693161835.502954
               (@ts >> 18)/1000: 1693161221.6870
FROM_UNIXTIME((@ts >> 18)/1000): 2023-08-27 20:33:41.6870
                         NOW(6): 2023-08-27 20:43:55.502954
                  @ts & 0x3FFFF: 4
1 row in set (0.00 sec)
```

`>> 18`演算は、物理タイムスタンプの抽出に使用される[右シフト](/functions-and-operators/bit-functions-and-operators.md#-right-shift) x 18 ビットのビット単位を表します。物理タイムスタンプはミリ秒単位で表され、秒単位で測定される一般的な UNIX タイムスタンプ形式とは異なるため、これを 1000 で割って[`FROM_UNIXTIME()`](/functions-and-operators/date-and-time-functions.md)と互換性のある形式に変換する必要があります。このプロセスは、 `TIDB_PARSE_TSO()`の機能と一致します。

10 進数では`4`に相当する、2 進数では論理タイムスタンプ`000000000000000100`を抽出することもできます。

次のように CLI ツールを使用してタイムスタンプを解析することもできます。

```shell
$ tiup ctl:v7.1.0 pd tso 443852055297916932
```

    system:  2023-08-27 20:33:41.687 +0200 CEST
    logic:   4

ここでは、 `system:`で始まる行に物理タイムスタンプが表示され、 `logic:`で始まる行に論理タイムスタンプが表示されます。
