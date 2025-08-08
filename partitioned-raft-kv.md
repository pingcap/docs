---
title: Partitioned Raft KV
summary: TiKV のパーティション化されたRaft KV 機能について学習します。
---

# 分割RaftKV {#partitioned-raft-kv}

> **警告：**
>
> Partitioned Raft KVは実験的機能です。本番環境での使用は推奨されません。この機能は予告なく変更または削除される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

v6.6.0 より前では、TiKV の Raft ベースのstorageエンジンは、単一の RocksDB インスタンスを使用して、TiKV インスタンスのすべてのリージョンのデータを格納していました。

より大規模なクラスターをより安定的にサポートするために、TiDB v6.6.0 以降では、複数の RocksDBstorageを使用して TiKVリージョンデータを保存し、各リージョンのデータが個別の RocksDB インスタンスに独立して保存される新しい TiKV ストレージ エンジンが導入されました。

新しいエンジンは、各RocksDBインスタンス内のファイル数とレベルをより適切に制御し、リージョン間のデータ操作を物理的に分離し、より多くのデータを安定的に管理できるようにします。これは、TiKVがパーティショニングを通じて複数のRocksDBインスタンスを管理するのと似ています。そのため、この機能はPartitioned Raft KVと名付けられています。

## アプリケーションシナリオ {#application-scenarios}

TiKV クラスターに次の特性がある場合、この機能を使用できます。

-   単一の TiKV インスタンスでより多くのデータをサポートする必要があります。
-   書き込みリクエストが多数あります。
-   スケールインおよびスケールアウト操作が頻繁に行われます。
-   ワークロードには重大な読み取りおよび書き込み増幅があります。
-   TiKV には十分なメモリがあります。

この機能の利点は、書き込みパフォーマンスの向上、スケーリング速度の高速化、そして同じハードウェアでサポートできるデータ量の増大です。また、より大規模なクラスターにも対応できます。

## 使用法 {#usage}

Partitioned Raft KVを有効にするには、クラスター作成時に設定項目[`storage.engine`](/tikv-configuration-file.md#engine-new-in-v660) ～ `"partitioned-raft-kv"`を設定します。同時に、設定項目[`rocksdb.write-buffer-flush-oldest-first`](/tikv-configuration-file.md#write-buffer-flush-oldest-first-new-in-v660)と[`rocksdb.write-buffer-limit`](/tikv-configuration-file.md#write-buffer-limit-new-in-v660)使用して、 Raft KV使用時のRocksDBのメモリ使用量を制御できます。

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
