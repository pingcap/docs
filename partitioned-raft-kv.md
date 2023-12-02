---
title: Partitioned Raft KV
summary: Learn about the partitioned Raft KV feature of TiKV.
---

# 仕切られたRaftKV {#partitioned-raft-kv}

> **警告：**
>
> パーティション化されたRaft KV は実験的機能です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

v6.6.0 より前は、TiKV の Raft ベースのstorageエンジンは単一の RocksDB インスタンスを使用して、TiKV インスタンスのすべてのリージョンのデータを保存していました。

大規模なクラスターをより安定してサポートするために、TiDB v6.6.0 からは、複数の RocksDB インスタンスを使用して TiKVリージョンデータを保存する新しい TiKVstorageエンジンが導入され、各リージョンのデータは個別の RocksDB インスタンスに個別に保存されます。

新しいエンジンは、各 RocksDB インスタンス内のファイルの数とレベルをより適切に制御し、リージョン間のデータ操作の物理的な分離を実現し、より多くのデータの安定した管理をサポートします。これは、パーティショニングを通じて複数の RocksDB インスタンスを管理する TiKV として見ることができます。そのため、この機能は Partitioned Raft KV と呼ばれています。

## アプリケーションシナリオ {#application-scenarios}

TiKV クラスターに次の特性がある場合、この機能を使用できます。

-   単一の TiKV インスタンスは、より多くのデータをサポートする必要があります。
-   書き込みリクエストが多いです。
-   スケールインおよびスケールアウト操作は頻繁に行われます。
-   ワークロードの読み取りおよび書き込みが大幅に増加します。
-   TiKV には十分なメモリがあります。

この機能の利点は、書き込みパフォーマンスの向上、スケーリング速度の高速化、および同じハードウェアでサポートされるデータ量の増加です。より大きなクラスター規模もサポートできます。

## 使用法 {#usage}

Partitioned Raft KV を有効にするには、クラスター作成時に設定項目[`storage.engine`](/tikv-configuration-file.md#engine-new-in-v660) ～ `"partitioned-raft-kv"`を設定します。同時に、構成項目[`rocksdb.write-buffer-flush-oldest-first`](/tikv-configuration-file.md#write-buffer-flush-oldest-first-new-in-v660)と[`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660)を使用して、 Raft KV を使用するときに RocksDB のメモリ使用量を制御できます。

## 制限 {#restrictions}

パーティション化されたRaft KV には次の制限があります。

-   EBS ボリューム スナップショット バックアップはまだサポートされていません。
-   オンラインの安全でない復元や Titan はまだサポートされていません。
-   tikv-ctl コマンドライン ツールの次のサブコマンドはサポートされていません。
    -   `unsafe-recover`
    -   `raw-scan`
    -   `remove-fail-stores`
    -   `recreate-region`
    -   `reset-to-version`
-   TiFlashにはまだ対応していません。
-   クラスターの初期化後は、この機能を有効または無効にすることはできません。
