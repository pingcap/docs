---
title: Use TiDB Lightning to Import Data in Parallel
summary: TiDB Lightningを使用する際のデータの並列インポートの概念、ユーザー シナリオ、使用法、および制限について学習します。
---

# TiDB Lightningを使用してデータを並列インポートする {#use-tidb-lightning-to-import-data-in-parallel}

TiDB Lightning v5.3.0以降、 [物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)は単一テーブルまたは複数テーブルの並列インポートをサポートしています。複数のTiDB Lightningインスタンスを同時に実行することで、単一または複数のテーブルからデータを並列インポートできます。これにより、 TiDB Lightningは水平スケーリングが可能になり、大量のデータのインポートにかかる時間を大幅に短縮できます。

技術的な実装では、 TiDB Lightning は各インスタンスのメタデータと各インポートされたテーブルのデータをターゲット TiDB に記録し、異なるインスタンスの Row ID 割り当て範囲、グローバル チェックサムの記録、TiKV と PD の構成変更と回復を調整します。

TiDB Lightning を使用すると、次のシナリオでデータを並列にインポートできます。

-   シャード化されたスキーマとシャード化されたテーブルをインポートします。このシナリオでは、複数の上流データベースインスタンスからの複数のテーブルが、異なるTiDB Lightningインスタンスによって下流 TiDB データベースに並行してインポートされます。
-   単一テーブルの並列インポート。このシナリオでは、特定のディレクトリまたはクラウドstorage（Amazon S3など）に保存された単一テーブルが、複数のTiDB Lightningインスタンスによって下流のTiDBクラスタに並列インポートされます。これはTiDB 5.3.0で導入された新機能です。

> **注記：**
>
> -   並列インポートは、TiDB 内の初期化された空のテーブルのみをサポートし、既存のサービスによって書き込まれたデータを含むテーブルへのデータ移行はサポートしません。そうしないと、データの不整合が発生する可能性があります。
>
> -   並行インポートは通常、物理インポートモードで使用されます。1 `parallel-import = true`設定する必要があります。
>
> -   複数のTiDB Lightningインスタンスを使用して同じターゲットにデータをインポートする場合は、一度に1つのバックエンドのみを適用してください。例えば、同じTiDBクラスターに物理インポートモードと論理インポートモードの両方で同時にデータをインポートすることはできません。

## 考慮事項 {#considerations}

並列インポートを使用するには、 `parallel-import = true`設定する必要があります。TiDB TiDB Lightning を起動すると、下流の TiDB クラスタにメタデータが登録され、同時にターゲットクラスタにデータを移行している他のインスタンスが存在するかどうかが自動的に検出されます。存在する場合、自動的に並列インポートモードに移行します。

ただし、データを並行して移行する場合は、次の点を考慮する必要があります。

-   複数のシャードテーブル間の主キーまたは一意のインデックス間の競合を処理する
-   インポートパフォーマンスの最適化

### 主キーまたは一意のインデックス間の競合を処理する {#handle-conflicts-between-primary-keys-or-unique-indexes}

[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)使用してデータを並列インポートする場合は、データソース間およびターゲット TiDB クラスター内のテーブル間で主キーまたは一意のインデックスの競合がないこと、またインポート中にターゲットテーブルにデータの書き込みが行われないことを確認してください。そうでない場合、 TiDB Lightning はインポートされたデータの正確性を保証できず、インポート完了後にターゲットテーブルに不整合なインデックスが含まれることになります。

### インポートパフォーマンスの最適化 {#optimize-import-performance}

TiDB Lightningは、生成されたキーバリューデータを、対応するリージョンの各コピーが配置されているTiKVノードにアップロードする必要があるため、インポート速度はターゲットクラスタのサイズによって制限されます。ターゲットTiDBクラスタ内のTiKVインスタンスの数とTiDB Lightningインスタンスの数がn:1（nはリージョンのコピー数）より大きくすることを推奨します。同時に、最適なインポートパフォーマンスを実現するには、以下の要件を満たす必要があります。

-   各TiDB Lightningインスタンスを専用マシンにデプロイ。1つのTiDB LightningインスタンスはデフォルトですべてのCPUリソースを消費するため、1台のマシンに複数のインスタンスをデプロイしてもパフォーマンスは向上しません。
-   並列インポートを実行する各TiDB Lightningインスタンスのソースファイルの合計サイズは 5 TiB 未満である必要があります。
-   TiDB Lightningインスタンスの合計数は 10 未満である必要があります。

TiDB Lightningを使用して共有データベースとテーブルを並列にインポートする場合は、データの量に応じて適切な数のTiDB Lightningインスタンスを選択します。

-   MySQL のデータ量が 2 TiB 未満の場合、1 つのTiDB Lightningインスタンスを並列インポートに使用できます。
-   MySQL データ量が 2 TiB を超え、MySQL インスタンスの合計数が 10 未満の場合、MySQL インスタンスごとに 1 つのTiDB Lightningインスタンスを使用することをお勧めします。また、並列TiDB Lightningインスタンスの数は 10 を超えないようにしてください。
-   MySQL データ量が 2 TiB を超え、MySQL インスタンスの合計数が 10 を超える場合は、これらの MySQL インスタンスによってエクスポートされたデータをインポートするために 5 ～ 10 個のTiDB Lightningインスタンスを割り当てることをお勧めします。

次に、このドキュメントでは、2 つの例を使用して、さまざまなシナリオでの並行インポートの操作手順を詳しく説明します。

-   例1: Dumpling + TiDB Lightningを使用して、シャードデータベースとテーブルをTiDBに並列にインポートする
-   例2: 単一のテーブルを並列にインポートする

### 制限 {#restrictions}

TiDB Lightning は実行時に一部のリソースを排他的に使用します。単一のマシン（本番環境では推奨されません）または複数のマシンで共有されるディスクに複数のTiDB Lightningインスタンスを展開する必要がある場合は、以下の使用制限にご注意ください。

-   各TiDB Lightningインスタンスの一意のパスを`tikv-importer.sorted-kv-dir`に設定してください。複数のインスタンスが同じパスを共有すると、意図しない動作が発生し、インポートの失敗やデータエラーが発生する可能性があります。
-   各TiDB Lightningチェックポイントは個別に保存してください。チェックポイントの設定の詳細については、 [TiDB Lightningチェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)参照してください。
    -   checkpoint.driver = &quot;file&quot; (デフォルト) を設定する場合は、チェックポイントへのパスがインスタンスごとに一意であることを確認してください。
    -   checkpoint.driver = &quot;mysql&quot; を設定する場合は、インスタンスごとに一意のスキーマを設定する必要があります。
-   各TiDB Lightningのログファイルは、それぞれ異なるパスに設定する必要があります。同じログファイルを共有すると、ログのクエリやトラブルシューティングに影響します。
-   [ウェブインターフェース](/tidb-lightning/tidb-lightning-web-interface.md)または Debug API を使用する場合は、インスタンスごとに`lightning.status-addr`一意のアドレスに設定する必要があります。そうしないと、ポートの競合によりTiDB Lightningプロセスが起動に失敗します。

## 例 1: Dumpling + TiDB Lightningを使用して、シャードデータベースとテーブルを TiDB に並列インポートする {#example-1-use-dumpling-tidb-lightning-to-import-sharded-databases-and-tables-into-tidb-in-parallel}

この例では、アップストリームが10個のシャードテーブルを持つMySQLクラスタで、合計サイズが10TiBであると仮定します。5つのTiDB Lightningインスタンスを使用して並列インポートを実行し、各インスタンスが2TiBをインポートします。合計インポート時間（ Dumplingエクスポートに必要な時間を除く）は、約40時間から約10時間に短縮されると推定されます。

上流ライブラリの名前が`my_db` 、各シャードテーブルの名前が`my_table_01` ～ `my_table_10`であると仮定します。これらを下流のテーブル`my_db.my_table`にマージしてインポートします。具体的な手順については、以下のセクションで説明します。

### ステップ1: Dumplingを使用してデータをエクスポートする {#step-1-use-dumpling-to-export-data}

TiDB Lightningがデプロイされている 5 つのノード上の 2 つのシャード テーブルをエクスポートします。

-   2つのシャードテーブルが同じMySQLインスタンス内にある場合、 Dumplingのパラメータ`--filter`使用して直接エクスポートできます。TiDB TiDB Lightningを使用してインポートする場合は、 Dumplingがデータをエクスポートするディレクトリとして`data-source-dir`指定できます。
-   2つのシャードテーブルのデータが異なるMySQLノードに分散されている場合は、 Dumplingを使用して個別にエクスポートする必要があります。エクスポートしたデータは、同じ親ディレクトリ内<b>、かつ異なるサブディレクトリに</b>配置する必要があります。TiDB TiDB Lightningを使用して並列インポートを実行する場合は、親ディレクトリとして`data-source-dir`指定する必要があります。

Dumpling を使用してデータをエクスポートする方法の詳細については、 [Dumpling](/dumpling-overview.md)参照してください。

### ステップ2: TiDB Lightningデータソースを構成する {#step-2-configure-tidb-lightning-data-sources}

構成ファイル`tidb-lightning.toml`を作成し、次のコンテンツを追加します。

    [lightning]
    status-addr = ":8289"

    [mydumper]
    # Specify the path for Dumpling to export data. If Dumpling performs several times and the data belongs to different directories, you can place all the exported data in the same parent directory and specify this parent directory here.
    data-source-dir = "/path/to/source-dir"

    [tikv-importer]
    # Whether to allow importing data into tables that already have data. The default value is `false`.
    # When using parallel import, because multiple TiDB Lightning instances import a table at the same time, this configuration item must be set to `true`.
    parallel-import = true
    # "local": The default mode. It applies to large dataset import, for example, greater than 1 TiB. However, during the import, downstream TiDB is not available to provide services.
    # "tidb": You can use this mode for small dataset import, for example, smaller than 1 TiB. During the import, downstream TiDB is available to provide services.
    backend = "local"

    # Specify the path for local sorting data.
    sorted-kv-dir = "/path/to/sorted-dir"

データソースがAmazon S3やGCSなどの外部storageに保存されている場合は、接続用の追加パラメータを設定する必要があります。このような設定にはパラメータを指定できます。例えば、次の例では、データがAmazon S3に保存されていると仮定しています。

    tiup tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup'

詳細なパラメータの説明については、 [外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

### ステップ3: TiDB Lightningを起動してデータをインポートする {#step-3-start-tidb-lightning-to-import-data}

並列インポート中、各TiDB Lightningノードのサーバー構成要件は、非並列インポートモードの場合と同じです。各TiDB Lightningノードは同じリソースを使用する必要があります。各ノードは異なるサーバーにデプロイすることをお勧めします。詳細なデプロイ手順については、 [TiDB Lightningをデプロイ](/tidb-lightning/deploy-tidb-lightning.md)参照してください。

各サーバーで順番にTiDB Lightningを起動します。コマンドラインから`nohup`指定して直接起動すると、SIGHUPシグナルによって終了する可能性があります。そのため、スクリプトに`nohup`指定することをお勧めします。例：

```shell
# !/bin/bash
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
```

並列インポート中、 TiDB Lightning はタスクの開始後に次のチェックを自動的に実行します。

-   ローカルディスク（構成`sort-kv-dir`で制御）とTiKVクラスターに、データのインポートに必要な空き容量があるかどうかを確認してください。必要なディスク容量については、 [下流のstorageスペース要件](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database)と[リソース要件](/tidb-lightning/tidb-lightning-physical-import-mode.md#environment-requirements)参照してください。TiDB TiDB Lightningはデータソースをサンプリングし、サンプル結果からインデックスサイズの割合を推定します。推定にはインデックスも含まれるため、ソースデータのサイズがローカルディスクの空き容量よりも小さい場合でも、チェックが失敗する場合があります。
-   TiKVクラスタ内のリージョンが均等に分散されているか、また空きリージョンが多すぎないかを確認してください。空きリージョンの数がmax(1000, テーブル数 * 3)を超える場合、つまり「1000」または「テーブル数の3倍」のいずれか大きい方を超える場合、インポートは実行できません。
-   データソースからデータが順番にインポートされているか確認します。確認結果に基づいて`mydumper.batch-size`のサイズが自動的に調整されます。そのため、 `mydumper.batch-size`構成は利用できなくなります。

チェックをオフにして、 `lightning.check-requirements`設定で強制インポートを実行することもできます。詳細なチェックについては、 [TiDB Lightning事前チェック](/tidb-lightning/tidb-lightning-prechecks.md)参照してください。

### ステップ4: インポートの進行状況を確認する {#step-4-check-the-import-progress}

インポートを開始した後、次のいずれかの方法で進行状況を確認できます。

-   `grep` log キーワード`progress`で進捗状況を確認します。デフォルトでは5分ごとに更新されます。
-   監視コンソールで進行状況を確認してください。詳細は[TiDB Lightning監視](/tidb-lightning/monitor-tidb-lightning.md)参照してください。

すべてのTiDB Lightningインスタンスが終了するまで待機すると、インポート全体が完了します。

## 例2: 単一のテーブルを並列にインポートする {#example-2-import-single-tables-in-parallel}

TiDB Lightningは、単一テーブルの並列インポートもサポートしています。例えば、Amazon S3に保存されている複数の単一テーブルを、異なるTiDB Lightningインスタンスで下流のTiDBクラスターに並列インポートできます。この方法により、インポート全体の速度が向上します。Amazon S3などのリモートストレージを使用する場合、 TiDB Lightningの設定パラメータはBRと同じです。詳細については、 [外部ストレージサービスのURI形式](/external-storage-uri.md)参照してください。

> **注記：**
>
> ローカル環境では、 Dumplingの`--filesize`または`--where`のパラメータを使用して、単一テーブルのデータを複数の部分に分割し、複数のサーバーのローカルディスクに事前にエクスポートすることができます。これにより、並列インポートが可能になります。設定は例1と同じです。

ソースファイルがAmazon S3に保存されており、テーブルファイルが`my_db.my_table.00001.sql` ～ `my_db.my_table.10000.sql` 、合計10,000個のSQLファイルがあると仮定します。インポートを高速化するために2つのTiDB Lightningインスタンスを使用する場合は、設定ファイルに以下の設定を追加する必要があります。

    [[mydumper.files]]
    # the db schema file
    pattern = '(?i)^(?:[^/]*/)*my_db-schema-create\.sql'
    schema = "my_db"
    type = "schema-schema"

    [[mydumper.files]]
    # the table schema file
    pattern = '(?i)^(?:[^/]*/)*my_db\.my_table-schema\.sql'
    schema = "my_db"
    table = "my_table"
    type = "table-schema"

    [[mydumper.files]]
    # Only import 00001~05000 and ignore other files
    pattern = '(?i)^(?:[^/]*/)*my_db\.my_table\.(0[0-4][0-9][0-9][0-9]|05000)\.sql'
    schema = "my_db"
    table = "my_table"
    type = "sql"

    [tikv-importer]
    # Whether to allow importing data into tables that already have data. The default value is `false`.
    # When using parallel import, because multiple TiDB Lightning instances import a table at the same time, this configuration item must be set to `true`.
    parallel-import = true

他のインスタンスの構成を変更して、 `05001 ~ 10000`データ ファイルのみをインポートすることができます。

その他の手順については、例 1 の関連する手順を参照してください。

## エラーを処理する {#handle-errors}

### 一部のTiDB Lightningノードが異常終了する {#some-tidb-lightning-nodes-exit-abnormally}

並列インポート中に 1 つ以上のTiDB Lightningノードが異常終了した場合は、ログに記録されたエラーに基づいて原因を特定し、エラーの種類に応じてエラーを処理します。

-   エラーが通常の終了 (たとえば、kill コマンドに応答して終了) または OOM によるオペレーティング システムによる終了を示している場合は、構成を調整してから、 TiDB Lightningノードを再起動します。

-   ネットワーク タイムアウトなどのエラーがデータの精度に影響を与えない場合は、次の手順を実行します。

    1.  チェックポイント ソース データのエラーを消去するには、失敗したすべてのノードで設定`--checkpoint-error-ignore=all`で[`checkpoint-error-ignore`](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-ignore)コマンドを実行します。

    2.  チェックポイントからのデータのインポートを続行するには、これらのノードを再起動します。

-   ソース ファイル内の無効なデータを示すチェックサムの不一致など、データの不正確さにつながるエラーがログに記録されている場合は、次の手順を実行してこの問題を解決できます。

    1.  成功したノードを含むすべてのLightningノードで[`checkpoint-error-destroy`](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy)コマンドを実行します。このコマンドは、失敗したテーブルからインポートされたデータを削除し、これらのテーブルのチェックポイントステータスを「未開始」にリセットします。

    2.  正常に終了するノードを含むすべてのTiDB Lightningノードで[`filter`](/table-filter.md)パラメータを使用して、失敗したテーブルのデータを再構成してインポートします。

        Lightning の並列インポートタスクを再設定する際は、各 Lightning ノードの起動スクリプトに`checkpoint-error-destroy`コマンドを含めないでください。このコマンドを実行すると、複数の並列インポートタスクで使用されている共有メタデータが削除され、データインポート時に問題が発生する可能性があります。例えば、2つ目の Lightning インポートタスクを開始すると、最初のタスクによって書き込まれたメタデータが削除され、データインポートが正常に行われなくなります。

### インポート中に、「ターゲットテーブルがチェックサムを計算中です。チェックサムが完了するまで待ってから再試行してください」というエラーが報告されます。 {#during-an-import-an-error-target-table-is-calculating-checksum-please-wait-until-the-checksum-is-finished-and-try-again-is-reported}

並列インポートには、多数のテーブルや少量のデータを含むテーブルが含まれる場合があります。このような場合、1つ以上のタスクがテーブルの処理を開始する前に、そのテーブルの他のタスクが終了し、データのチェックサムが進行中である可能性があります。このとき、エラー`Target table is calculating checksum. Please wait until the checksum is finished and try again`が報告されます。この場合、チェックサムの完了を待ってから、失敗したタスクを再開できます。エラーは消え、データの精度に影響はありません。
