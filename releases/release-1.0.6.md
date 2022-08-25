---
title: TiDB 1.0.6 Release Notes
---

# TiDB 1.0.6 リリースノート {#tidb-1-0-6-release-notes}

2018 年 1 月 8 日に、TiDB 1.0.6 がリリースされ、次の更新が行われました。

## TiDB {#tidb}

-   [`Alter Table Auto_Increment`構文をサポート](https://github.com/pingcap/tidb/pull/5511)
-   [コストベースの計算のバグと統計の`Null Json`の問題を修正](https://github.com/pingcap/tidb/pull/5556)
-   [拡張構文をサポートして、暗黙的な行 ID をシャーディングし、単一テーブルの書き込みホット スポットを回避します](https://github.com/pingcap/tidb/pull/5559)
-   [潜在的な DDL の問題を修正する](https://github.com/pingcap/tidb/pull/5562)
-   [`curtime` 、 <code>sysdate</code> 、および<code>curdate</code>関数のタイムゾーン設定を検討してください](https://github.com/pingcap/tidb/pull/5564)
-   [`GROUP_CONCAT`関数で<code>SEPARATOR</code>構文をサポートする](https://github.com/pingcap/tidb/pull/5569)
-   [`GROUP_CONCAT`関数の戻り値の型が間違っている問題を修正しました。](https://github.com/pingcap/tidb/pull/5582)

## PD {#pd}

-   [ホットリージョンスケジューラーの店舗選択問題を修正](https://github.com/pingcap/pd/pull/898)

## TiKV {#tikv}

なし。

1.0.5 から 1.0.6 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。
