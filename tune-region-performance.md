---
title: Tune Region Performance
summary: Learn how to tune Region performance by adjusting the Region size and how to use buckets to optimize concurrent queries when the Region size is large.
---

# リージョンパフォーマンスの調整 {#tune-region-performance}

このドキュメントでは、リージョンサイズを調整してリージョンのパフォーマンスを調整する方法と、リージョンサイズが大きい場合にバケットを使用して同時クエリを最適化する方法を紹介します。

## 概要 {#overview}

TiKVは自動的に[最下層のデータを断片化する](/best-practices/tidb-best-practices.md#data-sharding) 。データは、キー範囲に基づいて複数のリージョンに分割されます。リージョンのサイズがしきい値を超えると、TiKVはそれを2つ以上のリージョンに分割します。

大量のデータを処理する場合、TiKVは非常に多くのリージョンを分割する可能性があり、その結果、より多くのリソース消費と[パフォーマンスの低下](/best-practices/massive-regions-best-practices.md#performance-problem)が発生します。特定の量のデータの場合、リージョンサイズが大きいほど、リージョンは少なくなります。 v6.1.0以降、TiDBはリージョンサイズのカスタマイズの設定をサポートしています。リージョンのデフォルトサイズは96MiBです。リージョンの数を減らすために、リージョンをより大きなサイズに調整できます。

多くのリージョンのパフォーマンスオーバーヘッドを削減するために、 [Hibernateリージョン](/best-practices/massive-regions-best-practices.md#method-4-increase-the-number-of-tikv-instances)または[`Region Merge`](/best-practices/massive-regions-best-practices.md#method-5-adjust-raft-base-tick-interval)を有効にすることもできます。

## <code>region-split-size</code>を使用してリージョンサイズを調整します {#use-code-region-split-size-code-to-adjust-region-size}

> **警告：**
>
> 現在、カスタマイズされたリージョンサイズは、TiDBv6.1.0で導入された実験的機能です。実稼働環境で使用することはお勧めしません。リスクは次のとおりです。
>
> -   パフォーマンスジッターが発生する可能性があります。
> -   特に広範囲のデータを処理するクエリの場合、クエリのパフォーマンスが低下する可能性があります。
> -   リージョンのスケジューリングが遅くなります。

リージョンサイズを調整するには、 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size)の構成アイテムを使用できます。推奨サイズは、96 MiB、128 MiB、または256MiBです。 `region-split-size`の値が大きいほど、パフォーマンスが不安定になります。リージョンサイズを1GiB以上に設定することはお勧めしません。サイズを10GiB以上に設定することは避けてください。 TiFlashを使用する場合、リージョンサイズは256MiBを超えてはなりません。

Dumplingツールを使用する場合、リージョンサイズは1GiBを超えてはなりません。この場合、リージョンサイズを増やした後、同時実行性を減らす必要があります。そうしないと、TiDBのメモリが不足する可能性があります。

## バケットを使用して同時実行性を高める {#use-bucket-to-increase-concurrency}

> **警告：**
>
> 現在、これはTiDBv6.1.0で導入された実験的機能です。実稼働環境で使用することはお勧めしません。

リージョンがより大きなサイズに設定されている場合、クエリの同時実行性を高めるために[`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610)から`true`に設定する必要があります。この構成を使用すると、リージョンはバケットに分割されます。バケットはリージョン内のより小さな範囲であり、スキャンの同時実行性を向上させるための同時クエリの単位として使用されます。 [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)を使用してバケットサイズを制御できます。デフォルト値は`96MiB`です。
