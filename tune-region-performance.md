---
title: Tune Region Performance
summary: リージョンサイズを調整してリージョンのパフォーマンスを調整する方法と、リージョンサイズが大きい場合にバケットを使用して同時クエリを最適化する方法を学習します。
---

# リージョンパフォーマンスの調整 {#tune-region-performance}

このドキュメントでは、リージョンサイズを調整してリージョンのパフォーマンスを調整する方法と、リージョンサイズが大きい場合にバケットを使用して同時クエリを最適化する方法について説明します。さらに、このドキュメントでは、Active PD Follower機能を有効にして、PD が TiDB ノードにリージョン情報を提供する機能を強化する方法についても説明します。

## 概要 {#overview}

TiKV は自動的に[最下層のデータを分割する](/best-practices/tidb-best-practices.md#data-sharding) 。データはキー範囲に基づいて複数のリージョンに分割されます。リージョンのサイズがしきい値を超えると、TiKV はそれを 2 つ以上のリージョンに分割します。

大規模なデータセットが関係するシナリオでは、リージョンサイズが比較的小さい場合、TiKV のリージョンが多すぎる可能性があり、リソースの消費量が増加し、 [パフォーマンスの低下](/best-practices/massive-regions-best-practices.md#performance-problem)なります。v6.1.0 以降、TiDB はリージョンサイズのカスタマイズをサポートしています。リージョンのデフォルト サイズは 96 MiB です。リージョンの数を減らすには、リージョンをより大きなサイズに調整できます。

多くのリージョンのパフォーマンスオーバーヘッドを削減するには、 [休止状態リージョン](/best-practices/massive-regions-best-practices.md#method-4-increase-the-number-of-tikv-instances)または[`Region Merge`](/best-practices/massive-regions-best-practices.md#method-5-adjust-raft-base-tick-interval)有効にすることもできます。

## リージョンサイズを調整するには、 <code>region-split-size</code>を使用します。 {#use-code-region-split-size-code-to-adjust-region-size}

> **注記：**
>
> リージョンサイズの推奨範囲は [48MiB、258MiB] です。一般的に使用されるサイズは、96 MiB、128 MiB、256 MiB です。リージョンサイズを 1 GiB を超えて設定することはお勧めしません。サイズを 10 GiB 以上に設定しないでください。リージョンサイズが大きすぎると、次のような副作用が発生する可能性があります。
>
> -   パフォーマンスのジッター
> -   クエリのパフォーマンスが低下する（特に、広範囲のデータを扱うクエリの場合）
> -   遅いリージョンスケジュール

リージョンサイズを調整するには、 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size)構成項目を使用できます。TiFlashを使用する場合、リージョンサイズは 256 MiB を超えないようにしてください。

Dumplingツールを使用する場合、リージョンサイズは 1 GiB を超えないようにしてください。この場合、リージョンサイズを増やした後に同時実行性を減らす必要があります。そうしないと、TiDB のメモリが不足する可能性があります。

## バケットを使用して同時実行性を高める {#use-bucket-to-increase-concurrency}

> **警告：**
>
> 現在、これは TiDB v6.1.0 で導入された実験的機能です。本番環境での使用はお勧めしません。

リージョンをより大きなサイズに設定した後、クエリの同時実行性をさらに向上させたい場合は、 [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610)から`true`に設定できます。この設定を使用すると、リージョンはバケットに分割されます。バケットはリージョン内のより小さな範囲であり、スキャンの同時実行性を向上させるための同時クエリの単位として使用されます。 [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)を使用してバケット サイズを制御できます。

## アクティブPDFollower機能を使用して、PDのリージョン情報クエリサービスのスケーラビリティを強化します。 {#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pd-s-region-information-query-service}

> **警告：**
>
> Active PD Follower機能は実験的です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

多数のリージョンを持つ TiDB クラスターでは、ハートビートの処理とタスクのスケジュール設定のオーバーヘッドが増加するため、PD リーダーの CPU 負荷が高くなる可能性があります。クラスターに多数の TiDB インスタンスがあり、リージョン情報に対する要求の同時実行性が高い場合、PD リーダーの CPU 負荷がさらに増加し​​、PD サービスが利用できなくなる可能性があります。

高可用性を確保するために、PD リーダーはリージョン情報をフォロワーとリアルタイムで同期します。PD フォロワーはリージョン情報をメモリに保持して保存し、リージョン情報要求を処理できるようにします。システム変数[`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)を`ON`に設定することで、アクティブ PDFollower機能を有効にすることができます。この機能を有効にすると、TiDB はリージョン情報要求をすべての PD サーバーに均等に分散し、PD フォロワーもリージョン要求を直接処理できるため、PD リーダーの CPU 負荷が軽減されます。

PD は、リージョン同期ストリームのステータスを維持し、TiKV client-go のフォールバック メカニズムを使用することで、TiDB 内のリージョン情報が常に最新であることを保証します。

-   PD リーダーとフォロワー間のネットワークが不安定な場合、またはフォロワーが利用できない場合は、リージョン同期ストリームが切断され、PD フォロワーはリージョン情報要求を拒否します。この場合、TiDB は PD リーダーへの要求を自動的に再試行し、フォロワーを一時的に利用不可としてマークします。
-   ネットワークが安定している場合、リーダーとフォロワー間の同期に遅延が発生する可能性があるため、フォロワーから取得した一部のリージョン情報が古くなっている可能性があります。この場合、リージョンに対応する KV 要求が失敗すると、TiDB は PD リーダーに最新のリージョン情報を自動的に再要求し、KV 要求を再度 TiKV に送信します。
