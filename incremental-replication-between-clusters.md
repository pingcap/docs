---
title: Replicate Incremental Data between TiDB Clusters in Real Time
summary: Learns how to replicate incremental data from one TiDB cluster to another cluster in real time
---

# TiDBクラスター間でインクリメンタルデータをリアルタイムで複製する {#replicate-incremental-data-between-tidb-clusters-in-real-time}

このドキュメントでは、TiDBクラスタとそのセカンダリMySQLまたはTiDBクラスタを構成する方法、およびプライマリクラスタからセカンダリクラスタに増分データをリアルタイムで複製する方法について説明します。

増分データをリアルタイムで複製するために実行中のTiDBクラスタとそのセカンダリクラスタを構成する必要がある場合は、 [バックアップと復元（BR）](/br/backup-and-restore-tool.md) 、および[Dumpling](/dumpling-overview.md)を使用し[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) 。

## 実装の原則 {#implementation-principles}

TiDBに書き込まれる各トランザクションには、一意のコミットタイムスタンプ（コミットTS）が割り当てられます。このTSを介して、TiDBクラスタのグローバル整合性ステータスを取得できます。

クラスタデータは、グローバルに一貫した時点でBRまたはDumplingを使用してエクスポートされます。次に、この時点から、TiDBBinlogを使用して増分データを複製します。つまり、レプリケーションプロセスは、完全レプリケーションと増分レプリケーションの2つの段階に分けられます。

1.  フルバックアップを実行し、バックアップデータのコミットTSを取得します。
2.  インクリメンタルレプリケーションを実行します。インクリメンタルレプリケーションの開始時刻がバックアップデータのコミットTSであることを確認してください。

> **ノート：**
>
> バックアップデータのエクスポート後に取得されるコミットTSは、閉じた間隔です。 TiDB Binlogを使用してレプリケーションプロセスを開始した後に取得されるinitial-commit-tsは、オープンインターバルです。

## レプリケーションプロセス {#replication-process}

既存のクラスタAが正しく機能するとします。まず、クラスタAのセカンダリクラスタとして新しいクラスタBを作成してから、クラスタAの増分データをクラスタBにリアルタイムで複製する必要があります。手順については、次の手順を参照してください。

### 手順1.TiDBBinlogを有効にする {#step-1-enable-tidb-binlog}

TiDB BinlogがクラスタAにデプロイされ、有効になっていることを確認してください。

### ステップ2.すべてのクラスタデータをエクスポートする {#step-2-export-all-cluster-data}

1.  次のツールのいずれかを使用して、クラスタAのデータを（グローバル整合性が確保された状態で）指定されたパスにエクスポートします。

    -   使用[フルバックアップ用のBR](/br/use-br-command-line-tool.md#back-up-all-the-cluster-data)

    -   使用[完全なデータをインポートするためのDumpling](/dumpling-overview.md)

2.  グローバルに一貫したタイムスタンプを取得する`COMMIT_TS` ：

    -   BR `validate`コマンドを使用して、バックアップタイムスタンプを取得します。例えば：

        {{< copyable "" >}}

        ```shell
        COMMIT_TS=`br validate decode --field="end-version" -s local:///home/tidb/backupdata | tail -n1`
        ```

    -   または、 Dumplingメタデータを確認して、Pos（ `COMMIT_TS` ）を取得します。

        {{< copyable "" >}}

        ```shell
        cat metadata
        ```

        ```shell
        Started dump at: 2020-11-10 10:40:19
        SHOW MASTER STATUS:
                Log: tidb-binlog
                Pos: 420747102018863124

        Finished dump at: 2020-11-10 10:40:20
        ```

3.  クラスタAのデータをクラスタBにエクスポートします。

### ステップ3.増分データを複製する {#step-3-replicate-incremental-data}

次の構成を追加して、TiDB Binlogの`drainer.toml`の構成ファイルを変更し、TiDBBinlogがクラスタBへのデータの複製を開始する`COMMIT_TS`を指定します。

{{< copyable "" >}}

```toml
initial-commit-ts = COMMIT_TS
[syncer.to]
host = {the IP address of cluster B}
port = 3306
```
