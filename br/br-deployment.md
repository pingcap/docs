---
title: Deploy and Use BR
summary: Learn how to deploy and use BR.
---

# デプロイを導入して使用する {#deploy-and-use-br}

このドキュメントでは、バックアップと復元（BR）の推奨される展開と、BRを使用してデータをバックアップおよび復元する方法について説明します。

## BRをデプロイ {#deploy-br}

BRを展開する際の推奨プラクティス：

-   実稼働環境では、少なくとも8コアのCPUと16GBのメモリを備えたノードにBRをデプロイします。 [LinuxOSのバージョン要件](/hardware-and-software-requirements.md#linux-os-version-requirements)に従って、適切なOSバージョンを選択します。
-   バックアップデータをAmazonS3、GCS、またはAzureBlobStorageに保存します。
-   バックアップと復元に十分なリソースを割り当てます。

    -   BR、TiKVノード、およびバックアップストレージシステムは、バックアップ速度よりも速いネットワーク帯域幅を提供する必要があります。ターゲットクラスタが特に大きい場合、バックアップと復元の速度のしきい値は、バックアップネットワークの帯域幅によって制限されます。
    -   バックアップストレージシステムは、十分な書き込み/読み取りパフォーマンス（IOPS）も提供する必要があります。そうしないと、バックアップまたは復元中にIOPSがパフォーマンスのボトルネックになる可能性があります。
    -   TiKVノードには、バックアップ用に少なくとも2つの追加のCPUコアと高性能ディスクが必要です。そうしないと、バックアップがクラスタで実行されているサービスに影響を与える可能性があります。

> **注**：
>
> -   ネットワークファイルシステム（NFS）がBRまたはTiKVノードにマウントされていない場合、またはAmazon S3、GCS、またはAzure Blob Storageプロトコルをサポートする外部ストレージを使用している場合、BRによってバックアップされるデータは各TiKVノードで生成されます。 BRはリーダーレプリカのみをバックアップするため、リーダーのサイズに基づいて各ノードで予約されているスペースを見積もる必要があります。 TiDBはデフォルトで負荷分散にリーダー数を使用するため、リーダーのサイズは大きく異なる可能性があります。これにより、バックアップデータが各ノードに不均一に分散されるという問題が発生する可能性があります。
> -   バックアップデータは各ノードのローカルファイルシステムに分散しているため、**これはBRを展開するための推奨される方法ではないことに注意してください**。バックアップデータを収集すると、データの冗長性と運用および保守の問題が発生する可能性があります。一方、バックアップデータを収集する直前にデータを復元すると、 `SST file not found`エラーが発生します。

## BRを使用する {#use-br}

現在、BRツールを実行するために次のメソッドがサポートされています。

### SQLステートメントを使用する {#use-sql-statements}

TiDBは、 [`BACKUP`](/sql-statements/sql-statement-backup.md)つと[`RESTORE`](/sql-statements/sql-statement-restore.md)のSQLステートメントの両方をサポートします。ステートメント[`SHOW BACKUPS| RESTORE`](/sql-statements/sql-statement-show-backups.md)を使用して、これらの操作の進行状況を監視できます。

### コマンドラインツールを使用する {#use-the-command-line-tool}

詳細については、 [バックアップと復元にBRコマンドラインを使用する](/br/use-br-command-line-tool.md)を参照してください。

### Kubernetes環境でBRを使用する {#use-br-in-the-kubernetes-environment}

Kubernetes環境では、 TiDB Operatorを使用してTiDBクラスタデータをAmazonS3、GCS、または永続ボリュームにバックアップし、そのようなシステムのバックアップデータからデータを復元できます。詳細については、 [TiDB Operatorを使用したデータのバックアップと復元](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-restore-overview)を参照してください。
