---
title: TiDB 1.0.5 Release Notes
---

# TiDB 1.0.5 リリースノート {#tidb-1-0-5-release-notes}

2017 年 12 月 26 日に、次の更新を含む TiDB 1.0.5 がリリースされました。

## TiDB {#tidb}

-   [`Show Create Table`ステートメントに現在の Auto_Increment ID の最大値を追加します。](https://github.com/pingcap/tidb/pull/5489)
-   [潜在的な goroutine リークを修正します。](https://github.com/pingcap/tidb/pull/5486)
-   [遅いクエリの別ファイルへの出力をサポートします。](https://github.com/pingcap/tidb/pull/5484)
-   [新しいセッションを作成するときに、TiKV から`TimeZone`変数をロードします。](https://github.com/pingcap/tidb/pull/5479)
-   [`Show Create Table`および`Analyze`ステートメントがパブリック テーブル/インデックスのみを処理できるように、スキーマ状態チェックをサポートします。](https://github.com/pingcap/tidb/pull/5474)
-   [`set transaction read only` `tx_read_only`変数に影響を与える必要があります。](https://github.com/pingcap/tidb/pull/5491)
-   [ロールバック時に増分統計データをクリーンアップします。](https://github.com/pingcap/tidb/pull/5391)
-   [`Show Create Table`ステートメントでインデックスの長さが欠落している問題を修正します。](https://github.com/pingcap/tidb/pull/5421)

## PD {#pd}

-   特定の状況下でリーダーのバランスが取れなくなる問題を修正します。
    -   [869](https://github.com/pingcap/pd/pull/869)
    -   [874](https://github.com/pingcap/pd/pull/874)
-   [ブートストラップ中の潜在的なpanicを修正します。](https://github.com/pingcap/pd/pull/889)

## TiKV {#tikv}

-   [`get_cpuid`](https://github.com/pingcap/tikv/pull/2611)関数を使用したCPU IDの取得が遅い問題を修正しました。
-   スペース収集の状況を改善するために[`dynamic-level-bytes`](https://github.com/pingcap/tikv/pull/2605)パラメーターをサポートします。

1.0.4 から 1.0.5 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。
