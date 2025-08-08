---
title: TiDB 1.0.6 Release Notes
summary: TiDB 1.0.6は2018年1月8日にリリースされました。更新内容には、Alter Table Auto_Increment構文のサポート、コストベース計算のバグ修正、Null JSON問題の修正、シャーディング暗黙行IDの拡張構文のサポートが含まれます。その他の更新内容には、潜在的なDDL問題の修正、特定の関数におけるタイムゾーン設定の考慮、GROUP_CONCAT関数におけるSEPARATOR構文のサポートが含まれます。PDでは、ホットリージョンスケジューラのストア選択の問題を修正しました。1.0.5から1.0.6にアップグレードするには、PD、TiKV、TiDBのローリングアップグレードの順序に従ってください。
---

# TiDB 1.0.6 リリースノート {#tidb-1-0-6-release-notes}

2018 年 1 月 8 日に、次の更新を含む TiDB 1.0.6 がリリースされました。

## TiDB {#tidb}

-   [`Alter Table Auto_Increment`構文をサポートする](https://github.com/pingcap/tidb/pull/5511)
-   [コストベースの計算のバグと統計の`Null Json`問題を修正しました](https://github.com/pingcap/tidb/pull/5556)
-   [単一テーブルの書き込みホットスポットを回避するために、暗黙の行IDを分割する拡張構文をサポートします。](https://github.com/pingcap/tidb/pull/5559)
-   [潜在的なDDLの問題を修正](https://github.com/pingcap/tidb/pull/5562)
-   [`curtime` 、 `sysdate` 、 `curdate`関数のタイムゾーン設定を考慮する](https://github.com/pingcap/tidb/pull/5564)
-   [`GROUP_CONCAT`関数で`SEPARATOR`構文をサポートする](https://github.com/pingcap/tidb/pull/5569)
-   [`GROUP_CONCAT`関数の間違った戻り値の型の問題を修正しました。](https://github.com/pingcap/tidb/pull/5582)

## PD {#pd}

-   [ホットリージョンスケジューラのストア選択問題を修正](https://github.com/pingcap/pd/pull/898)

## TiKV {#tikv}

なし。

1.0.5 から 1.0.6 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレード順序に従います。
