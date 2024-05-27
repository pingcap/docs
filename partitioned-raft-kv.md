---
title: Partitioned Raft KV
summary: TiKV のパーティション化されたRaft KV 機能について学習します。
---

# 分割RaftKV {#partitioned-raft-kv}

> **警告：**
>
> Partitioned Raft KV は実験的機能です。本番環境での使用は推奨されません。この機能は予告なしに変更または削除される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)報告できます。

v6.6.0 より前では、TiKV の Raft ベースのstorageエンジンは、単一の RocksDB インスタンスを使用して、TiKV インスタンスのすべてのリージョンのデータを格納していました。

より大規模なクラスターをより安定的にサポートするために、TiDB v6.6.0 以降では、複数の RocksDBstorageを使用して TiKVリージョンデータを保存し、各リージョンのデータを個別の RocksDB インスタンスに独立して保存する新しい TiKV ストレージ エンジンが導入されました。

新しいエンジンは、各 RocksDB インスタンス内のファイルの数とレベルをより適切に制御し、リージョン間のデータ操作の物理的な分離を実現し、より多くのデータを安定して管理することをサポートします。これは、パーティション分割によって複数の RocksDB インスタンスを管理する TiKV と見なすことができます。そのため、この機能は Partitioned Raft KV と名付けられています。

## アプリケーションシナリオ {#application-scenarios}

TiKV クラスターに次の特性がある場合、この機能を使用できます。

-   単一の TiKV インスタンスでより多くのデータをサポートする必要があります。
-   書き込みリクエストが多数あります。
-   スケールインおよびスケールアウト操作が頻繁に行われます。
-   ワークロードには、重大な読み取りおよび書き込み増幅があります。
-   TiKV には十分なメモリがあります。

この機能の利点は、書き込みパフォーマンスの向上、スケーリング速度の高速化、同じハードウェアでサポートされるデータの量の増加です。また、より大きなクラスター スケールもサポートできます。

## 使用法 {#usage}

Partitioned Raft KV を有効にするには、クラスター作成時に設定項目[`storage.engine`](/tikv-configuration-file.md#engine-new-in-v660) ～ `"partitioned-raft-kv"`を設定します。同時に、設定項目[`rocksdb.write-buffer-flush-oldest-first`](/tikv-configuration-file.md#write-buffer-flush-oldest-first-new-in-v660)と[`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660)を使用して、 Raft KV 使用時の RocksDB のメモリ使用量を制御できます。

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
-   まだTiFlashと互換性がありません。
-   クラスターが初期化された後は、この機能を有効または無効にすることはできません。
