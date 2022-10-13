---
title: Deploy and Use BR
summary: Learn how to deploy and use BR.
---

# BR をデプロイして使用する {#deploy-and-use-br}

このドキュメントでは、バックアップと復元 (BR) の推奨される展開と、BR を使用してデータをバックアップおよび復元する方法について説明します。

## デプロイを導入する {#deploy-br}

BR を導入する際の推奨プラクティス:

-   本番環境では、少なくとも 8 コアの CPU と 16 GB のメモリを搭載したノードに BR をデプロイします。次の[Linux OS のバージョン要件](/hardware-and-software-requirements.md#linux-os-version-requirements)に従って、適切な OS バージョンを選択します。
-   バックアップ データを Amazon S3、GCS、または Azure Blob Storage に保存します。
-   バックアップと復元に十分なリソースを割り当てます。

    -   BR、TiKV ノード、およびバックアップ ストレージ システムは、バックアップ速度よりも高いネットワーク帯域幅を提供する必要があります。ターゲット クラスタが特に大きい場合、バックアップと復元の速度のしきい値は、バックアップ ネットワークの帯域幅によって制限されます。
    -   バックアップ ストレージ システムは、十分な書き込み/読み取りパフォーマンス (IOPS) も提供する必要があります。そうしないと、バックアップまたは復元中に IOPS がパフォーマンスのボトルネックになる可能性があります。
    -   TiKV ノードには、少なくとも 2 つの追加の CPU コアと、バックアップ用の高性能ディスクが必要です。そうしないと、バックアップがクラスターで実行されているサービスに影響を与える可能性があります。

> **ノート：**
>
> -   ネットワーク ファイル システム (NFS) が BR または TiKV ノードにマウントされていない場合、または Amazon S3、GCS、または Azure Blob Storage プロトコルをサポートする外部ストレージを使用している場合、BR によってバックアップされたデータは各 TiKV ノードで生成されます。 BR はリーダー レプリカのみをバックアップするため、リーダーのサイズに基づいて各ノードで予約されるスペースを見積もる必要があります。 TiDB はデフォルトでロード バランシングにリーダー カウントを使用するため、リーダーのサイズは大きく異なる場合があります。これにより、バックアップ データが各ノードに不均等に分散されるという問題が発生する可能性があります。
> -   バックアップ データは各ノードのローカル ファイル システムに分散しているため、**これは BR を展開するための推奨される方法ではないことに注意してください**。バックアップデータを採取すると、データの冗長性や運用・保守上の問題が発生する可能性があります。一方、バックアップ データを収集する前に直接データを復元すると、エラー`SST file not found`が発生します。

## BRを使用 {#use-br}

現在、BR ツールを実行するために次の方法がサポートされています。

### SQL ステートメントを使用する {#use-sql-statements}

TiDB は、 [`BACKUP`](/sql-statements/sql-statement-backup.md)つと[`RESTORE`](/sql-statements/sql-statement-restore.md)の SQL ステートメントの両方をサポートします。ステートメント[`SHOW BACKUPS|RESTORES`](/sql-statements/sql-statement-show-backups.md)を使用して、これらの操作の進行状況を監視できます。

### コマンドライン ツールを使用する {#use-the-command-line-tool}

詳細については、 [バックアップと復元に BR コマンドラインを使用する](/br/use-br-command-line-tool.md)を参照してください。

### Kubernetes 環境で BR を使用する {#use-br-in-the-kubernetes-environment}

Kubernetes 環境では、 TiDB Operatorを使用して TiDB クラスター データを Amazon S3、GCS、または永続ボリュームにバックアップし、そのようなシステムのバックアップ データからデータを復元できます。詳細については、 [TiDB Operatorを使用したデータのバックアップと復元](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-restore-overview)を参照してください。
