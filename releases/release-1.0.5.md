---
title: TiDB 1.0.5 Release Notes
summary: TiDB 1.0.5は2017年12月26日にリリースされました。アップデートには、Auto_Increment IDの最大値の追加、goroutineリークの修正、低速クエリの別ファイルへの出力のサポート、TiKVからのTimeZone変数の読み込みなどが含まれています。PDの修正には、リーダーのバランス調整とブートストラップ中の潜在的なpanicの修正が含まれています。TiKVはCPU IDの取得速度の遅さを修正し、dynamic-level-bytesパラメータをサポートします。アップグレードの順序はPD -> TiKV -> TiDBです。
---

# TiDB 1.0.5 リリースノート {#tidb-1-0-5-release-notes}

2017 年 12 月 26 日に、次の更新を含む TiDB 1.0.5 がリリースされました。

## TiDB {#tidb}

-   [`Show Create Table`ステートメントに現在の Auto_Increment ID の最大値を追加します。](https://github.com/pingcap/tidb/pull/5489)
-   [潜在的な goroutine リークを修正します。](https://github.com/pingcap/tidb/pull/5486)
-   [遅いクエリを別のファイルに出力することをサポートします。](https://github.com/pingcap/tidb/pull/5484)
-   [新しいセッションを作成するときに、TiKV から`TimeZone`変数を読み込みます。](https://github.com/pingcap/tidb/pull/5479)
-   [スキーマ状態チェックをサポートし、 `Show Create Table`および`Analyze`ステートメントがパブリック テーブル/インデックスのみを処理するようにします。](https://github.com/pingcap/tidb/pull/5474)
-   [`set transaction read only` `tx_read_only`変数に影響します。](https://github.com/pingcap/tidb/pull/5491)
-   [ロールバック時に増分統計データをクリーンアップします。](https://github.com/pingcap/tidb/pull/5391)
-   [`Show Create Table`ステートメントでインデックスの長さが欠落している問題を修正しました。](https://github.com/pingcap/tidb/pull/5421)

## PD {#pd}

-   特定の状況下でリーダーのバランスが取れなくなる問題を修正しました。
    -   [869](https://github.com/pingcap/pd/pull/869)
    -   [874](https://github.com/pingcap/pd/pull/874)
-   [ブートストラップ中に発生する可能性のあるpanicを修正しました。](https://github.com/pingcap/pd/pull/889)

## TiKV {#tikv}

-   [`get_cpuid`](https://github.com/pingcap/tikv/pull/2611)関数を使用して CPU ID を取得するのが遅い問題を修正しました。
-   スペース収集状況を改善するために[`dynamic-level-bytes`](https://github.com/pingcap/tikv/pull/2605)パラメータをサポートします。

1.0.4 から 1.0.5 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレード順序に従います。
