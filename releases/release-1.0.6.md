---
title: TiDB 1.0.6 Release Notes
---

# TiDB 1.0.6 リリースノート {#tidb-1-0-6-release-notes}

2018 年 1 月 8 日に、次の更新を含む TiDB 1.0.6 がリリースされました。

## TiDB {#tidb}

-   [`Alter Table Auto_Increment`構文のサポート](https://github.com/pingcap/tidb/pull/5511)
-   [コストベースの計算のバグと統計の`Null Json`の問題を修正](https://github.com/pingcap/tidb/pull/5556)
-   [単一テーブルの書き込みホットスポットを回避するために、暗黙的な行 ID をシャードするための拡張構文をサポートします。](https://github.com/pingcap/tidb/pull/5559)
-   [潜在的な DDL 問題を修正する](https://github.com/pingcap/tidb/pull/5562)
-   [`curtime` 、 `sysdate` 、および`curdate`関数のタイムゾーン設定を考慮してください。](https://github.com/pingcap/tidb/pull/5564)
-   [`GROUP_CONCAT`関数で`SEPARATOR`構文をサポートする](https://github.com/pingcap/tidb/pull/5569)
-   [`GROUP_CONCAT`関数の間違った戻り値の型の問題を修正します。](https://github.com/pingcap/tidb/pull/5582)

## PD {#pd}

-   [ホットリージョンスケジューラのストア選択の問題を修正](https://github.com/pingcap/pd/pull/898)

## TiKV {#tikv}

なし。

1.0.5 から 1.0.6 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。
