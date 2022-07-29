---
title: TiDB 1.0.5 Release Notes
---

# TiDB1.0.5リリースノート {#tidb-1-0-5-release-notes}

2017年12月26日に、TiDB 1.0.5がリリースされ、次の更新が行われました。

## TiDB {#tidb}

-   [`Show Create Table`ステートメントに現在のAuto_IncrementIDの最大値を追加します。](https://github.com/pingcap/tidb/pull/5489)
-   [潜在的なゴルーチンリークを修正します。](https://github.com/pingcap/tidb/pull/5486)
-   [遅いクエリを別のファイルに出力することをサポートします。](https://github.com/pingcap/tidb/pull/5484)
-   [新しいセッションを作成するときに、TiKVから`TimeZone`変数をロードします。](https://github.com/pingcap/tidb/pull/5479)
-   [`Show Create Table`ステートメントと<code>Analyze</code>ステートメントがパブリックテーブル/インデックスのみを処理するように、スキーマ状態チェックをサポートします。](https://github.com/pingcap/tidb/pull/5474)
-   [`set transaction read only`は、 <code>tx_read_only</code>変数に影響を与えるはずです。](https://github.com/pingcap/tidb/pull/5491)
-   [ロールバック時に増分統計データをクリーンアップします。](https://github.com/pingcap/tidb/pull/5391)
-   [`Show Create Table`ステートメントでインデックスの長さが欠落する問題を修正します。](https://github.com/pingcap/tidb/pull/5421)

## PD {#pd}

-   ある状況下でリーダーがバランスをとるのをやめる問題を修正します。
    -   [869](https://github.com/pingcap/pd/pull/869)
    -   [874](https://github.com/pingcap/pd/pull/874)
-   [ブートストラップ中の潜在的なpanicを修正します。](https://github.com/pingcap/pd/pull/889)

## TiKV {#tikv}

-   [`get_cpuid`](https://github.com/pingcap/tikv/pull/2611)関数を使用してCPUIDを取得するのが遅いという問題を修正します。
-   スペース収集状況を改善するために[`dynamic-level-bytes`](https://github.com/pingcap/tikv/pull/2605)パラメーターをサポートします。

1.0.4から1.0.5にアップグレードするには、PD-&gt;TiKV-&gt;TiDBのローリングアップグレード順序に従います。
