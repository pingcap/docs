---
title: Tune Region Performance
summary: リージョンサイズを調整してリージョンのパフォーマンスを調整する方法と、リージョンサイズが大きい場合にバケットを使用して同時クエリを最適化する方法を学習します。
---

# リージョンパフォーマンスの調整 {#tune-region-performance}

このドキュメントでは、リージョンサイズを調整してリージョンのパフォーマンスを調整する方法と、リージョンサイズが大きい場合にバケットを使用して同時クエリを最適化する方法について説明します。

## 概要 {#overview}

TiKV は自動的に[最下層のデータを分割する](/best-practices/tidb-best-practices.md#data-sharding) 。データはキー範囲に基づいて複数のリージョンに分割されます。リージョンのサイズがしきい値を超えると、TiKV はそれを 2 つ以上のリージョンに分割します。

大規模なデータセットが関係するシナリオでは、リージョンサイズが比較的小さい場合、TiKV のリージョンが多すぎる可能性があり、リソースの消費量が増加し、 [パフォーマンスの低下](/best-practices/massive-regions-best-practices.md#performance-problem)なります。v6.1.0 以降、TiDB はリージョンサイズのカスタマイズをサポートしています。リージョンのデフォルト サイズは 96 MiB です。リージョンの数を減らすには、リージョンをより大きなサイズに調整できます。

多くのリージョンのパフォーマンスオーバーヘッドを削減するには、 [休止状態リージョン](/best-practices/massive-regions-best-practices.md#method-4-increase-the-number-of-tikv-instances)または[`Region Merge`](/best-practices/massive-regions-best-practices.md#method-5-adjust-raft-base-tick-interval)有効にすることもできます。

## リージョンサイズを調整するには、 <code>region-split-size</code>を使用します。 {#use-code-region-split-size-code-to-adjust-region-size}

> **注記：**
>
> リージョンサイズの推奨範囲は [48 MiB、256 MiB] です。一般的に使用されるサイズは、96 MiB、128 MiB、256 MiB です。リージョンサイズを 1 GiB を超えて設定することはお勧めしません。サイズを 10 GiB 以上に設定しないでください。リージョンサイズが大きすぎると、次のような副作用が発生する可能性があります。
>
> -   パフォーマンスのジッター
> -   クエリのパフォーマンスが低下する（特に、広範囲のデータを扱うクエリの場合）
> -   遅いリージョンスケジュール

リージョンサイズを調整するには、 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size)構成項目を使用できます。TiFlash またはTiFlashツールを使用する場合、リージョンサイズは 1 GiB を超えてはなりません。リージョンサイズを増やした後、 Dumplingツールを使用する場合は同時実行性を減らす必要があります。そうしないと、TiDB のメモリが不足する可能性があります。

## バケットを使用して同時実行性を高める {#use-bucket-to-increase-concurrency}

> **警告：**
>
> 現在、これは TiDB v6.1.0 で導入された実験的機能です。本番環境での使用はお勧めしません。

リージョンをより大きなサイズに設定した後、クエリの同時実行性をさらに向上させたい場合は、 [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610)から`true`に設定できます。この設定を使用すると、リージョンはバケットに分割されます。バケットはリージョン内のより小さな範囲であり、スキャンの同時実行性を向上させるための同時クエリの単位として使用されます。 [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)を使用してバケット サイズを制御できます。
