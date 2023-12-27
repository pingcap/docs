---
title: Tune Region Performance
summary: Learn how to tune Region performance by adjusting the Region size and how to use buckets to optimize concurrent queries when the Region size is large.
---

# リージョンのパフォーマンスを調整する {#tune-region-performance}

このドキュメントでは、リージョンサイズを調整してリージョンのパフォーマンスを調整する方法と、リージョンサイズが大きい場合にバケットを使用して同時クエリを最適化する方法を紹介します。

## 概要 {#overview}

TiKV は自動的に[最下位層のデータをシャード化する](/best-practices/tidb-best-practices.md#data-sharding) 。データはキー範囲に基づいて複数のリージョンに分割されます。リージョンのサイズがしきい値を超えると、TiKV はリージョンを 2 つ以上のリージョンに分割します。

大規模なデータセットを含むシナリオでは、リージョンサイズが比較的小さい場合、TiKV のリージョンが多すぎる可能性があり、リソースの消費量が増加し、 [パフォーマンスの回帰](/best-practices/massive-regions-best-practices.md#performance-problem)発生します。 v6.1.0 以降、TiDB はリージョンサイズのカスタマイズをサポートしています。リージョンのデフォルトのサイズは 96 MiB です。リージョンの数を減らすには、リージョンをより大きなサイズに調整します。

多くのリージョンのパフォーマンスのオーバーヘッドを軽減するために、 [ハイバネートリージョン](/best-practices/massive-regions-best-practices.md#method-4-increase-the-number-of-tikv-instances)または[`Region Merge`](/best-practices/massive-regions-best-practices.md#method-5-adjust-raft-base-tick-interval)を有効にすることもできます。

## リージョンサイズを調整するには、 <code>region-split-size</code>を使用します {#use-code-region-split-size-code-to-adjust-region-size}

> **注記：**
>
> リージョンサイズの推奨範囲は [48MiB、258MiB] です。一般的に使用されるサイズには、96 MiB、128 MiB、256 MiB などがあります。リージョンサイズを 1 GiB を超えるように設定することはお勧めできません。サイズを 10 GiB を超えるように設定しないでください。リージョンサイズが大きすぎると、次の副作用が発生する可能性があります。
>
> -   パフォーマンスのジッター
> -   クエリのパフォーマンスの低下、特に広範囲のデータを処理するクエリの場合
> -   低速なリージョンのスケジューリング

リージョンサイズを調整するには、 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size)設定項目を使用できます。 TiFlashを使用する場合、リージョンサイズは 256 MiB を超えてはなりません。

Dumplingツールを使用する場合、リージョンサイズは 1 GiB を超えてはなりません。この場合、リージョンサイズを増やした後で同時実行性を減らす必要があります。そうしないと、TiDB がメモリ不足になる可能性があります。

## バケットを使用して同時実行性を向上させる {#use-bucket-to-increase-concurrency}

> **警告：**
>
> 現在、これは TiDB v6.1.0 で導入された実験的機能です。本番環境で使用することはお勧めできません。

リージョンをより大きなサイズに設定した後、クエリの同時実行性をさらに向上させたい場合は、 [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610)から`true`に設定してクエリの同時実行性を高めることができます。この構成を使用すると、リージョンはバケットに分割されます。バケットはリージョン内のより小さな範囲であり、スキャンの同時実行性を向上させるための同時クエリの単位として使用されます。 [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)を使用してバケット サイズを制御できます。デフォルト値は`96MiB`です。
