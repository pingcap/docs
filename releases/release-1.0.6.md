---
title: TiDB 1.0.6 Release Notes
---

# TiDB1.0.6リリースノート {#tidb-1-0-6-release-notes}

2018年1月8日に、TiDB 1.0.6がリリースされ、次の更新が行われました。

## TiDB {#tidb}

-   [`Alter Table Auto_Increment`構文をサポートする](https://github.com/pingcap/tidb/pull/5511)
-   [コストベースの計算のバグと統計の`Null Json`の問題を修正します](https://github.com/pingcap/tidb/pull/5556)
-   [単一のテーブルの書き込みホットスポットを回避するために、暗黙の行IDをシャーディングする拡張構文をサポートします](https://github.com/pingcap/tidb/pull/5559)
-   [潜在的なDDLの問題を修正する](https://github.com/pingcap/tidb/pull/5562)
-   [`curtime` 、 <code>sysdate</code> 、 <code>curdate</code>関数のタイムゾーン設定を検討してください](https://github.com/pingcap/tidb/pull/5564)
-   [`GROUP_CONCAT`関数で<code>SEPARATOR</code>構文をサポートする](https://github.com/pingcap/tidb/pull/5569)
-   [`GROUP_CONCAT`関数の誤った戻りタイプの問題を修正します。](https://github.com/pingcap/tidb/pull/5582)

## PD {#pd}

-   [ホットリージョンスケジューラのストア選択の問題を修正](https://github.com/pingcap/pd/pull/898)

## TiKV {#tikv}

なし。

1.0.5から1.0.6にアップグレードするには、PD-&gt;TiKV-&gt;TiDBのローリングアップグレードの順序に従います。
