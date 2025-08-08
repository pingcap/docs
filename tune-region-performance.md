---
title: Tune Region Performance
summary: リージョンサイズを調整してリージョンのパフォーマンスを調整する方法と、リージョンサイズが大きい場合にバケットを使用して同時クエリを最適化する方法を学習します。
---

# リージョンパフォーマンスの調整 {#tune-region-performance}

このドキュメントでは、リージョンサイズを調整することでリージョンパフォーマンスをチューニングする方法と、リージョンサイズが大きい場合にバケットを使用して同時クエリを最適化する方法について説明します。さらに、Active PD Follower機能を有効にすることで、PDがTiDBノードにリージョン情報を提供する能力を強化する方法についても説明します。

## 概要 {#overview}

TiKVは自動的に[最下層のデータを分割する](/best-practices/tidb-best-practices.md#data-sharding)データをキー範囲に基づいて複数のリージョンに分割します。リージョンのサイズがしきい値を超えると、TiKVはそれを2つ以上のリージョンに分割します。

大規模なデータセットが関係するシナリオでは、リージョンサイズが比較的小さい場合、TiKV のリージョンが多すぎる可能性があり、リソースの消費量が増加し、 [パフォーマンスの回帰](/best-practices/massive-regions-best-practices.md#performance-problem)発生します。

> **注記：**
>
> -   v6.1.0 では、TiDB は実験的機能としてリージョンサイズのカスタマイズをサポートしています。
> -   v6.5.0 以降、この機能は一般提供 (GA) されます。
> -   v8.4.0以降、リージョンのデフォルトサイズが96MiBから256MiBに変更されました。リージョンサイズを増やすと、リージョンの数を減らすことができます。

多くのリージョンのパフォーマンスオーバーヘッドを削減するには、 [休止状態リージョン](/best-practices/massive-regions-best-practices.md#method-4-increase-the-number-of-tikv-instances)または[`Region Merge`](/best-practices/massive-regions-best-practices.md#method-5-adjust-raft-base-tick-interval)有効にすることもできます。

## リージョンサイズを調整するには、 <code>region-split-size</code>を使用します。 {#use-code-region-split-size-code-to-adjust-region-size}

> **注記：**
>
> リージョンサイズの推奨範囲は[48 MiB、256 MiB]です。一般的に使用されるサイズは96 MiB、128 MiB、256 MiBです。リージョンサイズを1 GiBを超える値に設定することは推奨されません。10 GiBを超えるサイズの設定は避けてください。リージョンサイズが大きすぎると、以下の副作用が発生する可能性があります。
>
> -   パフォーマンスのジッター
> -   クエリパフォーマンスの低下（特に広範囲のデータを扱うクエリの場合）
> -   遅いリージョンスケジュール

リージョンサイズを調整するには、 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size)設定項目を使用します。TiFlashまたはTiFlashツールを使用する場合、リージョンサイズは1GiBを超えないようにしてください。リージョンサイズを増やした後、 Dumplingツールを使用する場合は同時実行性を下げる必要があります。そうしないと、TiDBのメモリが発生する可能性があります。

## バケットを使用して同時実行性を高める {#use-bucket-to-increase-concurrency}

> **警告：**
>
> 現在、これはTiDB v6.1.0で導入された実験的機能です。本番環境での使用は推奨されません。

リージョンのサイズを大きくした後、クエリの同時実行性をさらに向上させたい場合は、 [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610)から`true`に設定できます。この設定では、リージョンがバケットに分割されます。バケットはリージョン内の小さな範囲であり、スキャンの同時実行性を向上させるための同時クエリの単位として使用されます。バケットサイズは[`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)で制御できます。

## アクティブPDFollower機能を使用して、PDのリージョン情報クエリサービスのスケーラビリティを強化します。 {#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pd-s-region-information-query-service}

多数のリージョンを持つTiDBクラスターでは、ハートビート処理とタスクのスケジューリングによるオーバーヘッドの増加により、PDリーダーのCPU負荷が高くなる可能性があります。クラスターに多数のTiDBインスタンスがあり、リージョン情報へのリクエストが同時に発生すると、PDリーダーのCPU負荷がさらに高まり、PDサービスが利用できなくなる可能性があります。

高可用性を確保するため、PDリーダーはリージョン情報をフォロワーとリアルタイムで同期します。PDフォロワーはリージョン情報をメモリに保持・保存し、リージョン情報要求を処理できるようにします。システム変数[`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760)を`ON`に設定することで、アクティブPDFollower機能を有効にすることができます。この機能を有効にすると、TiDBはリージョン情報要求をすべてのPDサーバーに均等に分散し、PDフォロワーもリージョン要求を直接処理できるようになるため、PDリーダーのCPU負荷が軽減されます。

PD は、リージョン同期ストリームのステータスを維持し、TiKV client-go のフォールバック メカニズムを使用することで、TiDB 内のリージョン情報が常に最新であることを保証します。

-   PDリーダーとフォロワー間のネットワークが不安定な場合、またはフォロワーが利用できない場合、リージョン同期ストリームは切断され、PDフォロワーはリージョン情報要求を拒否します。この場合、TiDBはPDリーダーへの要求を自動的に再試行し、フォロワーを一時的に利用不可としてマークします。
-   ネットワークが安定している場合でも、リーダーとフォロワー間の同期に遅延が生じる可能性があり、フォロワーから取得したリージョン情報の一部が古くなっている可能性があります。この場合、当該リージョンに対応するKV要求が失敗すると、TiDBはPDリーダーに最新のリージョン情報を自動的に再要求し、TiKVに再度KV要求を送信します。
