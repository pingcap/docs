---
title: Tune Region Performance
summary: Learn how to tune Region performance by adjusting the Region size and how to use buckets to optimize concurrent queries when the Region size is large.
---

# リージョンのパフォーマンスを調整する {#tune-region-performance}

このドキュメントでは、リージョンサイズを調整してリージョンのパフォーマンスを調整する方法と、リージョンサイズが大きい場合にバケットを使用して同時クエリを最適化する方法を紹介します。

## 概要 {#overview}

TiKV は自動的に[最下位層のデータをシャード化する](/best-practices/tidb-best-practices.md#data-sharding) 。データはキー範囲に基づいて複数のリージョンに分割されます。リージョンのサイズがしきい値を超えると、TiKV はリージョンを 2 つ以上のリージョンに分割します。

大量のデータを処理する場合、TiKV は多くのリージョンを分割しすぎる可能性があり、これによりリソースの消費量が増加し、 [パフォーマンスの回帰](/best-practices/massive-regions-best-practices.md#performance-problem) .一定量のデータの場合、リージョンサイズが大きくなるほど、リージョンの数は少なくなります。 v6.1.0 以降、TiDB はリージョンサイズのカスタマイズ設定をサポートしています。リージョンのデフォルトのサイズは 96 MiB です。リージョンの数を減らすには、リージョンをより大きなサイズに調整します。

多くのリージョンのパフォーマンスのオーバーヘッドを軽減するために、 [ハイバネートリージョン](/best-practices/massive-regions-best-practices.md#method-4-increase-the-number-of-tikv-instances)または[`Region Merge`](/best-practices/massive-regions-best-practices.md#method-5-adjust-raft-base-tick-interval)を有効にすることもできます。

## リージョンサイズを調整するには、 <code>region-split-size</code>を使用します {#use-code-region-split-size-code-to-adjust-region-size}

> **警告：**
>
> 現在、カスタマイズされたリージョンサイズは、TiDB v6.1.0 で導入された実験的機能です。本番環境で使用することはお勧めできません。リスクは次のとおりです。
>
> -   パフォーマンスのジッターが発生する可能性があります。
> -   クエリのパフォーマンス、特に広範囲のデータを処理するクエリのパフォーマンスが低下する可能性があります。
> -   リージョンのスケジュールが遅くなります。

リージョンサイズを調整するには、 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size)設定項目を使用できます。推奨されるサイズは 96 MiB、128 MiB、または 256 MiB です。 `region-split-size`値が大きいほど、パフォーマンスのジッターが大きくなります。リージョンサイズを 1 GiB を超えるように設定することはお勧めできません。サイズを 10 GiB を超えるように設定しないでください。 TiFlashを使用する場合、リージョンサイズは 256 MiB を超えてはなりません。

Dumplingツールを使用する場合、リージョンサイズは 1 GiB を超えてはなりません。この場合、リージョンサイズを増やした後で同時実行性を減らす必要があります。そうしないと、TiDB がメモリ不足になる可能性があります。

## バケットを使用して同時実行性を向上させる {#use-bucket-to-increase-concurrency}

> **警告：**
>
> 現在、これは TiDB v6.1.0 で導入された実験的機能です。本番環境で使用することはお勧めできません。

リージョンがより大きなサイズに設定されている場合、クエリの同時実行性を高めるために[`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610)から`true`に設定する必要があります。この構成を使用すると、リージョンはバケットに分割されます。バケットはリージョン内のより小さな範囲であり、スキャンの同時実行性を向上させるための同時クエリの単位として使用されます。 [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)を使用してバケット サイズを制御できます。
