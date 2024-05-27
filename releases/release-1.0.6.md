---
title: TiDB 1.0.6 Release Notes
summary: TiDB 1.0.6 は、2018 年 1 月 8 日にリリースされました。更新内容には、Alter Table Auto_Increment 構文のサポート、コスト ベース計算のバグと Null Json 問題の修正、および暗黙の行 ID をシャードするための拡張構文のサポートが含まれます。その他の更新内容には、潜在的な DDL 問題の修正、特定の関数でのタイムゾーン設定の考慮、および GROUP_CONCAT 関数での SEPARATOR 構文のサポートが含まれます。PD では、ホット リージョン スケジューラのストア選択問題が修正されました。1.0.5 から 1.0.6 にアップグレードするには、PD、TiKV、TiDB のローリング アップグレード順序に従ってください。
---

# TiDB 1.0.6 リリースノート {#tidb-1-0-6-release-notes}

2018 年 1 月 8 日に、次の更新を含む TiDB 1.0.6 がリリースされました。

## ティビ {#tidb}

-   [`Alter Table Auto_Increment`構文をサポートする](https://github.com/pingcap/tidb/pull/5511)
-   [コストベースの計算のバグと統計の`Null Json`の問題を修正しました](https://github.com/pingcap/tidb/pull/5556)
-   [単一テーブルの書き込みホットスポットを回避するために、暗黙の行IDを分割する拡張構文をサポートします。](https://github.com/pingcap/tidb/pull/5559)
-   [潜在的なDDLの問題を修正](https://github.com/pingcap/tidb/pull/5562)
-   [`curtime` 、 `sysdate` 、 `curdate`関数のタイムゾーン設定を考慮する](https://github.com/pingcap/tidb/pull/5564)
-   [`GROUP_CONCAT`関数で`SEPARATOR`構文をサポートする](https://github.com/pingcap/tidb/pull/5569)
-   [`GROUP_CONCAT`関数の戻り値の型の誤りの問題を修正しました。](https://github.com/pingcap/tidb/pull/5582)

## PD {#pd}

-   [ホットリージョンスケジューラのストア選択問題を修正](https://github.com/pingcap/pd/pull/898)

## ティクヴ {#tikv}

なし。

1.0.5 から 1.0.6 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。
