---
title: BR Tool Overview
summary: Learn what is BR and how to use the tool.
---

# BRツールの概要 {#br-tool-overview}

[BR](http://github.com/pingcap/br) （バックアップと復元）は、TiDBクラスタデータの分散バックアップと復元のためのコマンドラインツールです。

[Dumpling](/dumpling-overview.md)と比較して、BRは大量のデータを含むシナリオに適しています。

定期的なバックアップと復元に加えて、互換性が確保されている限り、BRを使用して大規模なデータ移行を行うこともできます。

このドキュメントでは、BRの実装原則、推奨される展開構成、使用制限、およびBRを使用するためのいくつかの方法について説明します。

## 実装の原則 {#implementation-principles}

BRは、バックアップまたは復元コマンドを各TiKVノードに送信します。これらのコマンドを受信した後、TiKVは対応するバックアップまたは復元操作を実行します。

各TiKVノードには、バックアップ操作で生成されたバックアップファイルが保存され、復元中に保存されたバックアップファイルが読み取られるパスがあります。

![br-arch](/media/br-arch.png)

<details>

<summary>バックアップの原則</summary>

BRがバックアップ操作を実行すると、最初にPDから次の情報を取得します。

-   バックアップスナップショットの時刻としての現在のTS（タイムスタンプ）
-   現在のクラスタのTiKVノード情報

これらの情報に従って、BRは内部で`mysql`インスタンスを起動して、TSに対応するデータベースまたはテーブル情報を取得し、同時にシステムデータベース（ `information_schema` ）を除外し`performance_schema` 。

backupサブコマンドによると、BRは次の2種類のバックアップロジックを採用しています。

-   完全バックアップ：BRはすべてのテーブルをトラバースし、各テーブルに従ってバックアップされるKV範囲を構築します。
-   単一テーブルのバックアップ：BRは、単一のテーブルに従ってバックアップされるKV範囲を構築します。

最後に、BRはバックアップするKV範囲を収集し、完全なバックアップ要求をクラスタのTiKVノードに送信します。

リクエストの構造：

```
BackupRequest{
    ClusterId,      // The cluster ID.
    StartKey,       // The starting key of the backup (backed up).
    EndKey,         // The ending key of the backup (not backed up).
    StartVersion,   // The version of the last backup snapshot, used for the incremental backup.
    EndVersion,     // The backup snapshot time.
    StorageBackend, // The path where backup files are stored.
    RateLimit,      // Backup speed (MB/s).
}
```

バックアップ要求を受信した後、TiKVノードはノード上のすべてのリージョンリーダーをトラバースして、この要求のKV範囲と重複するリージョンを見つけます。 TiKVノードは、範囲内のデータの一部またはすべてをバックアップし、対応するSSTファイルを生成します。

対応するリージョンのデータのバックアップが終了すると、TiKVノードはメタデータをBRに返します。 BRはメタデータを収集し、復元に使用される`backupmeta`のファイルに保存します。

`StartVersion`が`0`でない場合、バックアップは増分バックアップと見なされます。 KVに加えて、BRは`[StartVersion, EndVersion)`の間のDDLも収集します。データの復元中に、これらのDDLが最初に復元されます。

バックアップコマンドの実行時にチェックサムが有効になっている場合、BRはデータチェックのためにバックアップされた各テーブルのチェックサムを計算します。

### バックアップファイルの種類 {#types-of-backup-files}

バックアップファイルが保存されるパスには、次の2種類のバックアップファイルが生成されます。

-   **SSTファイル**：TiKVノードがバックアップしたデータを保存します。
-   **`backupmeta`ファイル**：バックアップファイルの数、キー範囲、サイズ、ハッシュ（sha256）値など、このバックアップ操作のメタデータを格納します。
-   **`backup.lock`ファイル**：複数のバックアップ操作が同じディレクトリにデータを保存するのを防ぎます。

### SSTファイル名の形式 {#the-format-of-the-sst-file-name}

SSTファイルは`storeID_regionID_regionEpoch_keyHash_cf`の形式で名前が付けられます。ここで

-   `storeID`はTiKVノードIDです。
-   `regionID`はリージョンIDです。
-   `regionEpoch`はリージョンのバージョン番号です。
-   `keyHash`は、範囲のstartKeyのハッシュ（sha256）値であり、キーの一意性を保証します。
-   `cf`はRocksDBの[カラムファミリー](/tune-tikv-memory-performance.md)を示します（デフォルトでは`default`または`write` ）。

</details>

<details>

<summary>修復の原則</summary>

データ復元プロセス中に、BRは次のタスクを順番に実行します。

1.  バックアップパス内の`backupmeta`のファイルを解析し、内部でTiDBインスタンスを起動して、解析された情報に基づいて対応するデータベースとテーブルを作成します。

2.  解析されたSSTファイルをテーブルに従って集約します。

3.  SSTファイルのキー範囲に従ってリージョンを事前に分割し、すべてのリージョンが少なくとも1つのSSTファイルに対応するようにします。

4.  復元する各テーブルと、各テーブルに対応するSSTファイルをトラバースします。

5.  SSTファイルに対応するリージョンを見つけ、ファイルをダウンロードするために対応するTiKVノードにリクエストを送信します。次に、ファイルが正常にダウンロードされた後、ファイルのロード要求を送信します。

TiKVがSSTファイルをロードする要求を受信した後、TiKVはRaftメカニズムを使用して、SSTデータの強力な整合性を確保します。ダウンロードしたSSTファイルが正常に読み込まれると、ファイルは非同期で削除されます。

復元操作が完了すると、BRは復元されたデータに対してチェックサム計算を実行して、保存されたデータとバックアップされたデータを比較します。

</details>

## デプロイを導入して使用する {#deploy-and-use-br}

### 推奨される展開構成 {#recommended-deployment-configuration}

-   PDノードにBRを展開することをお勧めします。
-   高性能SSDをBRノードとすべてのTiKVノードにマウントすることをお勧めします。 10ギガビットのネットワークカードをお勧めします。そうしないと、バックアップおよび復元プロセス中に帯域幅がパフォーマンスのボトルネックになる可能性があります。

> **ノート：**
>
> -   ネットワークディスクをマウントしない場合、または他の共有ストレージを使用する場合、BRによってバックアップされたデータは各TiKVノードで生成されます。 BRはリーダーのレプリカのみをバックアップするため、リーダーのサイズに基づいて各ノードに予約されているスペースを見積もる必要があります。
>
> -   TiDBはデフォルトで負荷分散にリーダー数を使用するため、リーダーのサイズは大きく異なる可能性があります。これにより、各ノードでバックアップデータが不均一に分散される可能性があります。

### 使用制限 {#usage-restrictions}

バックアップと復元にBRを使用する場合の制限は次のとおりです。

-   BRがTiCDC/ Drainerのアップストリームクラスタにデータを復元する場合、TiCDC/ Drainerは復元されたデータをダウンストリームに複製できません。
-   BRはKVデータのみをバックアップするため、BRは同じ[`new_collations_enabled_on_first_bootstrap`](/character-set-and-collation.md#collation-support-framework)の値を持つクラスター間の操作のみをサポートします。バックアップするクラスタと復元するクラスタが異なる照合を使用する場合、データ検証は失敗します。したがって、クラスタを復元する前に、 `select VARIABLE_VALUE from mysql.tidb where VARIABLE_NAME='new_collation_enabled';`ステートメントのクエリ結果からのスイッチ値がバックアッププロセス中のスイッチ値と一致していることを確認してください。

### 互換性 {#compatibility}

BRとTiDBクラスタの互換性の問題は、次のカテゴリに分類されます。

-   BRの一部のバージョンは、TiDBクラスタのインターフェースと互換性がありません。

    -   v5.4.0より前のBRバージョンは、 `charset=GBK`のテーブルのリカバリーをサポートしていません。 v5.4.0より前のバージョンのBRは、 `charset=GBK`のテーブルをTiDBクラスターにリカバリーすることをサポートしていません。

-   一部の機能が有効または無効になると、KV形式が変更される場合があります。これらの機能がバックアップおよび復元中に一貫して有効または無効にされていない場合、互換性の問題が発生する可能性があります。

これらの機能は次のとおりです。

| 特徴                    | 関連する問題                                                                  | ソリューション                                                                                                                                    |
| --------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| クラスター化されたインデックス       | [＃565](https://github.com/pingcap/br/issues/565)                        | 復元中の`tidb_enable_clustered_index`のグローバル変数の値が、バックアップ中の値と一致していることを確認してください。そうしないと、 `default not found`やデータインデックスの不整合など、データの不整合が発生する可能性があります。 |
| 新しい照合順序               | [＃352](https://github.com/pingcap/br/issues/352)                        | `new_collations_enabled_on_first_bootstrap`変数の値がバックアップ中の値と一致していることを確認してください。そうしないと、一貫性のないデータインデックスが発生し、チェックサムが渡されない可能性があります。               |
| 復元クラスタでTiCDCが有効になっている | [＃364](https://github.com/pingcap/br/issues/364#issuecomment-646813965) | 現在、TiKVはBRを取り込んだSSTファイルをTiCDCにプッシュダウンできません。したがって、BRを使用してデータを復元する場合は、TiCDCを無効にする必要があります。                                                    |
| グローバル一時テーブル           |                                                                         | データのバックアップと復元には、BRv5.3.0以降のバージョンを使用していることを確認してください。そうしないと、バックアップされたグローバル一時テーブルの定義でエラーが発生します。                                               |

ただし、バックアップと復元中に上記の機能が一貫して有効または無効になっていることを確認した後でも、BRとTiKV / TiDB / PD間の内部バージョンまたはインターフェイスの一貫性がないため、互換性の問題が発生する可能性があります。このようなケースを回避するために、BRにはバージョンチェックが組み込まれています。

#### バージョンチェック {#version-check}

バックアップと復元を実行する前に、BRはTiDBクラスタのバージョンとBRのバージョンを比較して確認します。メジャーバージョンの不一致（たとえば、BRv4.xとTiDBv5.x）がある場合、BRは終了するようにリマインダーを表示します。バージョンチェックを強制的にスキップするには、 `--check-requirements=false`を設定します。

バージョンチェックをスキップすると、非互換性が生じる可能性があることに注意してください。 BRバージョンとTiDBバージョン間のバージョン互換性情報は次のとおりです。

| バックアップバージョン（垂直）\復元バージョン（水平）             | 毎晩BRを使用して、毎晩TiDBを復元します                                                                       | BRv5.0を使用してTiDBv5.0を復元します                                                                    | BRv4.0を使用してTiDBv4.0を復元します                                                                                                                                                       |
| --------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 毎晩BRを使用してTiDBを毎晩バックアップします               | ✅                                                                                            | ✅                                                                                            | ❌（非整数のクラスター化インデックスタイプの主キーを持つテーブルがTiDB v4.0クラスタに復元された場合、BRは警告なしにデータエラーを引き起こします。）                                                                                                 |
| BRv5.0を使用してTiDBv5.0をバックアップします           | ✅                                                                                            | ✅                                                                                            | ❌（非整数のクラスター化インデックスタイプの主キーを持つテーブルがTiDB v4.0クラスタに復元された場合、BRは警告なしにデータエラーを引き起こします。）                                                                                                 |
| BRv4.0を使用してTiDBv4.0をバックアップします           | ✅                                                                                            | ✅                                                                                            | ✅（TiKV&gt; = v4.0.0-rc.1で、BRに[＃233](https://github.com/pingcap/br/pull/233)のバグ修正が含まれ、TiKVに[＃7241](https://github.com/tikv/tikv/pull/7241)のバグ修正が含まれていない場合、BRによってTiKVノードが再起動します。） |
| BRnightlyまたはv5.0を使用してTiDBv4.0をバックアップします | ❌（TiDBバージョンがv4.0.9より前の場合、 [＃609](https://github.com/pingcap/br/issues/609)の問題が発生する可能性があります。） | ❌（TiDBバージョンがv4.0.9より前の場合、 [＃609](https://github.com/pingcap/br/issues/609)の問題が発生する可能性があります。） | ❌（TiDBバージョンがv4.0.9より前の場合、 [＃609](https://github.com/pingcap/br/issues/609)の問題が発生する可能性があります。）                                                                                    |

### <code>mysql</code>システムスキーマのテーブルデータをバックアップおよび復元します（実験的機能） {#back-up-and-restore-table-data-in-the-code-mysql-code-system-schema-experimental-feature}

> **警告：**
>
> この機能は実験的であり、徹底的にテストされていません。この機能を実稼働環境で使用することは強く**お勧め**しません。

v5.1.0より前では、BRはバックアップ中にシステムスキーマ`mysql`からデータを除外していました。 v5.1.0以降、BRは、システムスキーマ`mysql.*`を含むすべてのデータをデフォルトで**バックアップ**します。ただし、 `mysql.*`でシステムテーブルを復元する技術的な実装はまだ完了していないため、システムスキーマ`mysql`のテーブルはデフォルトでは復元され<strong>ません</strong>。

システムテーブルのデータ（たとえば、 `mysql.usertable1` ）をシステムスキーマ`mysql`に復元する場合は、 [`filter`パラメータ](/br/use-br-command-line-tool.md#back-up-with-table-filter)を設定してテーブル名（ `-f "mysql.usertable1"` ）をフィルタリングできます。設定後、システムテーブルは最初に一時スキーマに復元され、次に名前を変更してシステムスキーマに復元されます。

以下のシステムテーブルは、技術的な理由により正しく復元できないことに注意してください。 `-f "mysql.*"`を指定しても、次のテーブルは復元されません。

-   統計に関連するテーブル： &quot;stats_buckets&quot;、 &quot;stats_extended&quot;、 &quot;stats_feedback&quot;、 &quot;stats_fm_sketch&quot;、 &quot;stats_histograms&quot;、 &quot;stats_meta&quot;、 &quot;stats_top_n&quot;
-   特権またはシステムに関連するテーブル： &quot;tidb&quot;、 &quot;global_variables&quot;、 &quot;columns_priv&quot;、 &quot;db&quot;、 &quot;default_roles&quot;、 &quot;global_grants&quot;、 &quot;global_priv&quot;、 &quot;role_edges&quot;、 &quot;tables_priv&quot;、 &quot;user&quot;、 &quot;gc_delete_range &quot;、&quot; Gc_delete_range_done &quot;、&quot; schema_index_usage &quot;

### BRの実行に必要な最小マシン構成 {#minimum-machine-configuration-required-for-running-br}

BRの実行に必要な最小マシン構成は次のとおりです。

| CPU | メモリー   | ハードディスクの種類 | 通信網            |
| --- | ------ | ---------- | -------------- |
| 1コア | 4ギガバイト | HDD        | ギガビットネットワークカード |

一般的なシナリオ（バックアップと復元用に1000テーブル未満）では、実行時のBRのCPU消費量は200％を超えず、メモリ消費量は4GBを超えません。ただし、多数のテーブルをバックアップおよび復元する場合、BRは4GBを超えるメモリを消費する可能性があります。 24000テーブルをバックアップするテストでは、BRは約2.7 GBのメモリを消費し、CPU消費量は100％未満のままです。

### ベストプラクティス {#best-practices}

以下は、BRを使用するためのいくつかの推奨操作です。

-   アプリケーションへの影響を最小限に抑えるために、オフピーク時にバックアップ操作を実行することをお勧めします。
-   データを復元するとき、BRはターゲットクラスタのリソースを可能な限り消費します。したがって、データを新しいクラスターまたはオフラインクラスターに復元することをお勧めします。稼働中の本番クラスタにデータを復元しないでください。そうしないと、サービスが影響を受ける可能性があります。
-   複数のバックアップまたは復元操作を1つずつ実行することをお勧めします。バックアップまたは復元操作を並行して実行すると、パフォーマンスが低下し、オンラインアプリケーションにも影響します。さらに悪いことに、複数のタスク間のコラボレーションが不足していると、タスクが失敗し、クラスタのパフォーマンスに影響を与える可能性があります。
-   バックアップデータの保存には、Amazon S3、Google Cloud Storage、AzureBlobStorageをお勧めします。
-   BRノードとTiKVノード、およびバックアップストレージバックエンドに、読み取りと書き込みのパフォーマンスを確保するのに十分なネットワーク帯域幅があることを確認してください。不十分なストレージ容量は、バックアップまたは復元操作のボトルネックになる可能性があります。

### BRの使い方 {#how-to-use-br}

現在、BRツールを実行するために次のメソッドがサポートされています。

-   SQLステートメントを使用する
-   コマンドラインツールを使用する
-   Kubernetes環境でBRを使用する

#### SQLステートメントを使用する {#use-sql-statements}

TiDBは、 [`BACKUP`](/sql-statements/sql-statement-backup.md#backup)つと[`RESTORE`](/sql-statements/sql-statement-restore.md#restore)のSQLステートメントの両方をサポートします。これらの操作の進行状況は、ステートメント[`SHOW BACKUPS|RESTORES`](/sql-statements/sql-statement-show-backups.md)で監視できます。

#### コマンドラインツールを使用する {#use-the-command-line-tool}

`br`コマンドラインユーティリティは[別ダウンロード](/download-ecosystem-tools.md#br-backup-and-restore)として使用できます。詳細については、 [バックアップと復元にBRコマンドラインを使用する](/br/use-br-command-line-tool.md)を参照してください。

#### Kubernetes環境で {#in-the-kubernetes-environment}

Kubernetes環境では、BRツールを使用してTiDBクラスタデータをS3互換ストレージ、Google Cloud Storage（GCS）、永続ボリューム（PV）にバックアップし、それらを復元できます。

> **ノート：**
>
> AmazonS3およびGoogleCloudStorageのパラメーターの説明については、 [外部ストレージ](/br/backup-and-restore-storages.md#url-parameters)のドキュメントを参照してください。

-   [BRを使用してS3互換ストレージにデータをバックアップする](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br)
-   [BRを使用してS3互換ストレージからデータを復元する](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br)
-   [BRを使用してデータをGCSにバックアップする](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-gcs-using-br)
-   [BRを使用してGCSからデータを復元する](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-gcs-using-br)
-   [BRを使用してデータをPVにバックアップする](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-pv-using-br)
-   [BRを使用してPVからデータを復元する](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-pv-using-br)

## BRに関するその他のドキュメント {#other-documents-about-br}

-   [BRコマンドラインを使用する](/br/use-br-command-line-tool.md)
-   [BRのユースケース](/br/backup-and-restore-use-cases.md)
-   [BR FAQ](/br/backup-and-restore-faq.md)
-   [外部ストレージ](/br/backup-and-restore-storages.md)
