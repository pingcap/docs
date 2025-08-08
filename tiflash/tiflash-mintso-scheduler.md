---
title: TiFlash MinTSO Scheduler
summary: TiFlash MinTSO Scheduler の実装原則を学びます。
---

# TiFlash MinTSO スケジューラ {#tiflash-mintso-scheduler}

TiFlash MinTSOスケジューラは、 TiFlash内の[MPP](/glossary.md#massively-parallel-processing-mpp)タスク用の分散スケジューラです。このドキュメントでは、 TiFlash MinTSOスケジューラの実装原理について説明します。

## 背景 {#background}

MPPクエリを処理する際、TiDBはクエリを1つ以上のMPPタスクに分割し、これらのMPPタスクを対応するTiFlashノードに送信してコンパイルおよび実行します。TiFlashが[パイプライン実行モデル](/tiflash/tiflash-pipeline-model.md)使用する前に、各MPPタスクを実行するために複数のスレッドを使用する必要があります。具体的なスレッド数は、MPPタスクの複雑さとTiFlashに設定された同時実行パラメータによって異なります。

同時実行性の高いシナリオでは、 TiFlashノードは複数のMPPタスクを同時に受信します。MPPタスクの実行が制御されていない場合、 TiFlashがシステムに要求する必要があるスレッド数は、MPPタスク数の増加に伴って直線的に増加します。スレッド数が多すぎるとTiFlashの実行効率に影響を与える可能性があります。また、オペレーティングシステム自体がサポートするスレッド数には制限があるため、オペレーティングシステムが提供できる以上のスレッドをTiFlashが要求するとエラーが発生します。

高い同時実行性が必要なシナリオで TiFlash の処理能力を向上させるには、 TiFlashに MPP タスク スケジューラを導入する必要があります。

## 実施原則 {#implementation-principles}

[背景](#background)で述べたように、 TiFlashタスクスケジューラを導入する当初の目的は、MPP クエリ実行中に使用されるスレッド数を制御することです。シンプルなスケジューリング戦略は、 TiFlash が要求できる最大スレッド数を指定することです。スケジューラは、各 MPP タスクについて、システムで現在使用されているスレッド数と、MPP タスクが使用すると予想されるスレッド数に基づいて、その MPP タスクをスケジュールできるかどうかを判断します。

![TiFlash MinTSO Scheduler v1](/media/tiflash/tiflash_mintso_v1.png)

前述のスケジューリング戦略はシステム スレッドの数を効果的に制御できますが、MPP タスクは最小の独立した実行単位ではなく、異なる MPP タスク間に依存関係が存在します。

```sql
EXPLAIN SELECT count(*) FROM t0 a JOIN t0 b ON a.id = b.id;
```

    +--------------------------------------------+----------+--------------+---------------+----------------------------------------------------------+
    | id                                         | estRows  | task         | access object | operator info                                            |
    +--------------------------------------------+----------+--------------+---------------+----------------------------------------------------------+
    | HashAgg_44                                 | 1.00     | root         |               | funcs:count(Column#8)->Column#7                          |
    | └─TableReader_46                           | 1.00     | root         |               | MppVersion: 2, data:ExchangeSender_45                    |
    |   └─ExchangeSender_45                      | 1.00     | mpp[tiflash] |               | ExchangeType: PassThrough                                |
    |     └─HashAgg_13                           | 1.00     | mpp[tiflash] |               | funcs:count(1)->Column#8                                 |
    |       └─Projection_43                      | 12487.50 | mpp[tiflash] |               | test.t0.id                                               |
    |         └─HashJoin_42                      | 12487.50 | mpp[tiflash] |               | inner join, equal:[eq(test.t0.id, test.t0.id)]           |
    |           ├─ExchangeReceiver_22(Build)     | 9990.00  | mpp[tiflash] |               |                                                          |
    |           │ └─ExchangeSender_21            | 9990.00  | mpp[tiflash] |               | ExchangeType: Broadcast, Compression: FAST               |
    |           │   └─Selection_20               | 9990.00  | mpp[tiflash] |               | not(isnull(test.t0.id))                                  |
    |           │     └─TableFullScan_19         | 10000.00 | mpp[tiflash] | table:a       | pushed down filter:empty, keep order:false, stats:pseudo |
    |           └─Selection_24(Probe)            | 9990.00  | mpp[tiflash] |               | not(isnull(test.t0.id))                                  |
    |             └─TableFullScan_23             | 10000.00 | mpp[tiflash] | table:b       | pushed down filter:empty, keep order:false, stats:pseudo |
    +--------------------------------------------+----------+--------------+---------------+----------------------------------------------------------+

例えば、上記のクエリは各TiFlashノードに2つのMPPタスクを生成しますが、 `ExchangeSender_45`のエグゼキューターを含むMPPタスクは`ExchangeSender_21`エグゼキューターを含むMPPタスクに依存しています。同時実行性の高いシナリオでは、スケジューラーが各クエリに対して`ExchangeSender_45`のエグゼキューターを含むMPPタスクをスケジュールすると、システムはデッドロック状態になります。

デッドロックを回避するために、 TiFlash は次の 2 つのレベルのスレッド制限を導入します。

-   thread_soft_limit: システムで使用されるスレッド数を制限するために使用されます。特定のMPPタスクでは、デッドロックを回避するためにこの制限を超えることができます。
-   thread_hard_limit: システムを保護するために使用されます。システムで使用されるスレッド数がハードリミットを超えると、 TiFlashはデッドロックを回避するためにエラーを報告します。

ソフトリミットとハードリミットは、デッドロックを回避するために次のように連携して機能します。ソフトリミットは、すべてのクエリで使用されるスレッドの総数を制限し、スレッドリソースの枯渇を回避しながらリソースを最大限に活用できるようにします。ハードリミットは、いかなる状況においても、システム内の少なくとも1つのクエリがソフトリミットを破り、スレッドリソースを取得して実行を継続できるようにすることで、デッドロックを回避します。スレッド数がハードリミットを超えない限り、システム内には常に1つのクエリが存在し、そのクエリのすべてのMPPタスクが正常に実行され、デッドロックを回避します。

MinTSOスケジューラの目的は、システムスレッドの数を制御しながら、システム内に常に1つの特別なクエリが存在し、そのクエリですべてのMPPタスクをスケジュールできるようにすることです。MinTSOスケジューラは完全に分散されたスケジューラであり、各TiFlashノードは自身の情報のみに基づいてMPPタスクをスケジュールします。したがって、 TiFlashノード上のすべてのMinTSOスケジューラは同じ「特別な」クエリを識別する必要があります。TiDBでは、各クエリは読み取りタイムスタンプ（ `start_ts` ）を持ち、MinTSOスケジューラは現在のTiFlashノード上で最も小さい`start_ts`持つクエリを「特別な」クエリとして定義します。グローバル最小値はローカル最小値でもあるという原則に基づき、すべてのTiFlashノードによって選択される「特別な」クエリは、MinTSOクエリと呼ばれる同じである必要があります。

MinTSO スケジューラのスケジューリング プロセスは次のとおりです。

![TiFlash MinTSO Scheduler v2](/media/tiflash/tiflash_mintso_v2.png)

ソフト制限とハード制限を導入することで、MinTSO スケジューラはシステム スレッドの数を制御しながらシステム デッドロックを効果的に回避します。ただし、同時実行性の高いシナリオでは、ほとんどのクエリで MPP タスクの一部のみがスケジュールされている可能性があります。MPP タスクの一部のみがスケジュールされているクエリは正常に実行できず、システム実行効率が低下します。この状況を回避するために、 TiFlash は、active_set_soft_limit と呼ばれる MinTSO スケジューラのクエリ レベルの制限を導入しています。この制限により、active_set_soft_limit クエリまでの MPP タスクのみがスケジューリングに参加できます。その他のクエリの MPP タスクはスケジューリングに参加せず、現在のクエリが終了した後にのみ新しいクエリがスケジューリングに参加できます。MinTSO クエリの場合、システム スレッドの数がハード制限を超えない限り、すべての MPP タスクを直接スケジュールできるため、この制限は単なるソフト制限です。

## 参照 {#see-also}

-   [TiFlashを設定する](/tiflash/tiflash-configuration.md) : MinTSO スケジューラを構成する方法を学習します。
