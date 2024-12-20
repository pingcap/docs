---
title: TiDB 1.0.5 Release Notes
summary: TiDB 1.0.5 は、2017 年 12 月 26 日にリリースされました。更新内容には、Auto_Increment ID の最大値の追加、goroutine リークの修正、低速クエリの別ファイルへの出力のサポート、TiKV からの TimeZone 変数の読み込みなどが含まれています。PD の修正には、リーダーのバランス調整とブートストラップ中の潜在的なpanicが含まれます。TiKV は、低速な CPU ID の取得を修正し、dynamic-level-bytes パラメータをサポートします。アップグレードの順序は、PD -> TiKV -> TiDB です。
---

# TiDB 1.0.5 リリースノート {#tidb-1-0-5-release-notes}

2017 年 12 月 26 日に、次の更新を含む TiDB 1.0.5 がリリースされました。

## ティビ {#tidb}

-   [`Show Create Table`ステートメントに現在の Auto_Increment ID の最大値を追加します。](https://github.com/pingcap/tidb/pull/5489)
-   [潜在的な goroutine リークを修正します。](https://github.com/pingcap/tidb/pull/5486)
-   [遅いクエリを別のファイルに出力することをサポートします。](https://github.com/pingcap/tidb/pull/5484)
-   [新しいセッションを作成するときに、TiKV から`TimeZone`変数を読み込みます。](https://github.com/pingcap/tidb/pull/5479)
-   [`Show Create Table`および`Analyze`ステートメントがパブリック テーブル/インデックスのみを処理するように、スキーマ状態チェックをサポートします。](https://github.com/pingcap/tidb/pull/5474)
-   [`set transaction read only` `tx_read_only`変数に影響します。](https://github.com/pingcap/tidb/pull/5491)
-   [ロールバック時に増分統計データをクリーンアップします。](https://github.com/pingcap/tidb/pull/5391)
-   [`Show Create Table`ステートメントでインデックスの長さが欠落する問題を修正しました。](https://github.com/pingcap/tidb/pull/5421)

## PD {#pd}

-   特定の状況下でリーダーのバランスが取れなくなる問題を修正しました。
    -   [869](https://github.com/pingcap/pd/pull/869)
    -   [874](https://github.com/pingcap/pd/pull/874)
-   [ブートストラップ中に発生する可能性のあるpanicを修正しました。](https://github.com/pingcap/pd/pull/889)

## ティクヴ {#tikv}

-   [`get_cpuid`](https://github.com/pingcap/tikv/pull/2611)関数を使用して CPU ID を取得するのが遅い問題を修正しました。
-   スペース収集状況を改善するために[`dynamic-level-bytes`](https://github.com/pingcap/tikv/pull/2605)パラメータをサポートします。

1.0.4 から 1.0.5 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。
