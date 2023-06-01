---
title: TiDB 1.0.5 Release Notes
---

# TiDB 1.0.5 リリースノート {#tidb-1-0-5-release-notes}

2017 年 12 月 26 日に、次の更新を含む TiDB 1.0.5 がリリースされました。

## TiDB {#tidb}

-   [<a href="https://github.com/pingcap/tidb/pull/5489">`Show Create Table`ステートメントに現在の Auto_Increment ID の最大値を追加します。</a>](https://github.com/pingcap/tidb/pull/5489)
-   [<a href="https://github.com/pingcap/tidb/pull/5486">潜在的な goroutine リークを修正します。</a>](https://github.com/pingcap/tidb/pull/5486)
-   [<a href="https://github.com/pingcap/tidb/pull/5484">遅いクエリの別ファイルへの出力をサポートします。</a>](https://github.com/pingcap/tidb/pull/5484)
-   [<a href="https://github.com/pingcap/tidb/pull/5479">新しいセッションを作成するときに、TiKV から`TimeZone`変数をロードします。</a>](https://github.com/pingcap/tidb/pull/5479)
-   [<a href="https://github.com/pingcap/tidb/pull/5474">`Show Create Table`および`Analyze`ステートメントがパブリック テーブル/インデックスのみを処理できるように、スキーマ状態チェックをサポートします。</a>](https://github.com/pingcap/tidb/pull/5474)
-   [<a href="https://github.com/pingcap/tidb/pull/5491">`set transaction read only` `tx_read_only`変数に影響を与える必要があります。</a>](https://github.com/pingcap/tidb/pull/5491)
-   [<a href="https://github.com/pingcap/tidb/pull/5391">ロールバック時に増分統計データをクリーンアップします。</a>](https://github.com/pingcap/tidb/pull/5391)
-   [<a href="https://github.com/pingcap/tidb/pull/5421">`Show Create Table`ステートメントでインデックスの長さが欠落している問題を修正します。</a>](https://github.com/pingcap/tidb/pull/5421)

## PD {#pd}

-   特定の状況下でリーダーのバランスが取れなくなる問題を修正します。
    -   [<a href="https://github.com/pingcap/pd/pull/869">869</a>](https://github.com/pingcap/pd/pull/869)
    -   [<a href="https://github.com/pingcap/pd/pull/874">874</a>](https://github.com/pingcap/pd/pull/874)
-   [<a href="https://github.com/pingcap/pd/pull/889">ブートストラップ中の潜在的なpanicを修正します。</a>](https://github.com/pingcap/pd/pull/889)

## TiKV {#tikv}

-   [<a href="https://github.com/pingcap/tikv/pull/2611">`get_cpuid`</a>](https://github.com/pingcap/tikv/pull/2611)関数を使用したCPU IDの取得が遅い問題を修正しました。
-   スペース収集の状況を改善するために[<a href="https://github.com/pingcap/tikv/pull/2605">`dynamic-level-bytes`</a>](https://github.com/pingcap/tikv/pull/2605)パラメーターをサポートします。

1.0.4 から 1.0.5 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。
