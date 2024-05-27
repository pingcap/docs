---
title: Use TiDB Lightning to Import Data in Parallel
summary: TiDB Lightningを使用する際のデータの並列インポートの概念、ユーザー シナリオ、使用方法、および制限について学習します。
---

# TiDB Lightning を使用してデータを並列インポートする {#use-tidb-lightning-to-import-data-in-parallel}

v5.3.0 以降、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md) 、単一テーブルまたは複数テーブルの並列インポートをサポートしています。複数のTiDB Lightningインスタンスを同時に実行することで、異なる単一テーブルまたは複数テーブルからデータを並列にインポートできます。このように、 TiDB Lightning は水平方向にスケーリングする機能を提供し、大量のデータのインポートに必要な時間を大幅に短縮します。

技術的な実装では、 TiDB Lightning は各インスタンスのメタデータとターゲット TiDB にインポートされた各テーブルのデータを記録し、異なるインスタンスの Row ID 割り当て範囲、グローバル チェックサムの記録、TiKV と PD の構成変更と回復を調整します。

TiDB Lightning を使用すると、次のシナリオでデータを並列にインポートできます。

-   シャードされたスキーマとシャードされたテーブルをインポートします。このシナリオでは、複数のアップストリーム データベース インスタンスからの複数のテーブルが、異なるTiDB Lightningインスタンスによって並行してダウンストリーム TiDB データベースにインポートされます。
-   単一テーブルを並列でインポートします。このシナリオでは、特定のディレクトリまたはクラウドstorage(Amazon S3 など) に保存されている単一テーブルが、異なるTiDB Lightningインスタンスによって下流の TiDB クラスターに並列でインポートされます。これは、TiDB 5.3.0 で導入された新機能です。

> **注記：**
>
> -   並列インポートでは、TiDB 内の初期化された空のテーブルのみがサポートされ、既存のサービスによって書き込まれたデータを含むテーブルへのデータの移行はサポートされません。そうしないと、データの不整合が発生する可能性があります。
>
> -   並行インポートは通常、物理インポート モードで使用されます。 `parallel-import = true`設定する必要があります。
>
> -   複数のTiDB Lightningインスタンスを使用して同じターゲットにデータをインポートする場合は、一度に適用するバックエンドは 1 つだけにしてください。たとえば、物理インポート モードと論理インポート モードの両方で同時に同じ TiDB クラスターにデータをインポートすることはできません。

## 考慮事項 {#considerations}

並列インポートを使用するには、 `parallel-import = true`設定する必要があります。TiDB TiDB Lightningが起動すると、下流の TiDB クラスターにメタデータを登録し、同時にターゲット クラスターにデータを移行している他のインスタンスがあるかどうかを自動的に検出します。ある場合は、自動的に並列インポート モードに入ります。

ただし、データを並行して移行する場合は、次の点を考慮する必要があります。

-   複数のシャードテーブル間の主キーまたは一意のインデックス間の競合を処理する
-   インポートパフォーマンスの最適化

### 主キーまたは一意のインデックス間の競合を処理する {#handle-conflicts-between-primary-keys-or-unique-indexes}

[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)を使用してデータを並列にインポートする場合は、データ ソース間およびターゲット TiDB クラスター内のテーブル間で主キーまたは一意のインデックスの競合がないこと、およびインポート中にターゲット テーブルにデータが書き込まれていないことを確認してください。そうでない場合、 TiDB Lightning はインポートされたデータの正確性を保証できず、インポートが完了した後にターゲット テーブルに不整合なインデックスが含まれることになります。

### インポートパフォーマンスの最適化 {#optimize-import-performance}

TiDB Lightning は、生成されたキー値データを、対応するリージョンの各コピーが配置されている TiKV ノードにアップロードする必要があるため、インポート速度はターゲット クラスターのサイズによって制限されます。ターゲット TiDB クラスター内の TiKV インスタンスの数とTiDB Lightningインスタンスの数が n:1 (n はリージョンのコピー数) より大きいことを確認することをお勧めします。同時に、最適なインポート パフォーマンスを実現するには、次の要件を満たす必要があります。

-   各TiDB Lightningインスタンスを専用のマシンにデプロイ。1 つのTiDB Lightningインスタンスはデフォルトですべての CPU リソースを消費するため、1 台のマシンに複数のインスタンスをデプロイしてもパフォーマンスは向上しません。
-   並列インポートを実行する各TiDB Lightningインスタンスのソース ファイルの合計サイズは 5 TiB 未満である必要があります。
-   TiDB Lightningインスタンスの合計数は 10 未満である必要があります。

TiDB Lightningを使用して共有データベースとテーブルを並列でインポートする場合は、データの量に応じて適切な数のTiDB Lightningインスタンスを選択します。

-   MySQL データ量が 2 TiB 未満の場合、並列インポートに 1 つのTiDB Lightningインスタンスを使用できます。
-   MySQL データ量が 2 TiB を超え、MySQL インスタンスの合計数が 10 未満の場合は、MySQL インスタンスごとに 1 つのTiDB Lightningインスタンスを使用することをお勧めします。また、並列TiDB Lightningインスタンスの数は 10 を超えないようにしてください。
-   MySQL データ量が 2 TiB を超え、MySQL インスタンスの合計数が 10 を超える場合は、これらの MySQL インスタンスによってエクスポートされたデータをインポートするために 5 ～ 10 個のTiDB Lightningインスタンスを割り当てることをお勧めします。

次に、このドキュメントでは、2 つの例を使用して、さまざまなシナリオでの並行インポートの操作手順を詳しく説明します。

-   例1: Dumpling + TiDB Lightningを使用して、シャードデータベースとテーブルをTiDBに並列でインポートする
-   例2: 単一のテーブルを並列でインポートする

### 制限 {#restrictions}

TiDB Lightning は実行時に一部のリソースを排他的に使用します。単一のマシン (本番環境では推奨されません) または複数のマシンで共有されるディスクに複数のTiDB Lightningインスタンスを展開する必要がある場合は、次の使用制限に注意してください。

-   各TiDB Lightningインスタンスの一意のパスを`tikv-importer.sorted-kv-dir`に設定します。複数のインスタンスが同じパスを共有すると、意図しない動作が発生し、インポートの失敗やデータ エラーが発生する可能性があります。
-   各TiDB Lightningチェックポイントを個別に保存します。チェックポイント構成の詳細については、 [TiDB Lightningチェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)参照してください。
    -   checkpoint.driver = &quot;file&quot; (デフォルト) を設定する場合は、チェックポイントへのパスがインスタンスごとに一意であることを確認してください。
    -   checkpoint.driver = &quot;mysql&quot; を設定する場合は、インスタンスごとに一意のスキーマを設定する必要があります。
-   各TiDB Lightningのログ ファイルは、一意のパスに設定する必要があります。同じログ ファイルを共有すると、ログのクエリとトラブルシューティングに影響します。
-   [ウェブインターフェース](/tidb-lightning/tidb-lightning-web-interface.md)または Debug API を使用する場合は、インスタンスごとに`lightning.status-addr`一意のアドレスに設定する必要があります。そうしないと、ポートの競合によりTiDB Lightningプロセスが起動しなくなります。

## 例 1: Dumpling + TiDB Lightningを使用して、シャードされたデータベースとテーブルを TiDB に並列でインポートする {#example-1-use-dumpling-tidb-lightning-to-import-sharded-databases-and-tables-into-tidb-in-parallel}

この例では、アップストリームが 10 個のシャード テーブルを持つ MySQL クラスターであり、合計サイズが 10 TiB であると想定します。5 つのTiDB Lightningインスタンスを使用して並列インポートを実行し、各インスタンスが 2 TiB をインポートします。合計インポート時間 ( Dumplingエクスポートに必要な時間を除く) は、約 40 時間から約 10 時間に短縮できると推定されます。

アップストリームライブラリの名前が`my_db`で、各シャードテーブルの名前が`my_table_01` ～ `my_table_10`であると仮定します。これらをダウンストリームの`my_db.my_table`テーブルにマージしてインポートします。具体的な手順については、次のセクションで説明します。

### ステップ1: Dumplingを使用してデータをエクスポートする {#step-1-use-dumpling-to-export-data}

TiDB Lightningがデプロイされている 5 つのノード上の 2 つのシャード テーブルをエクスポートします。

-   2 つのシャード テーブルが同じ MySQL インスタンスにある場合は、 Dumplingの`--filter`パラメータを使用して直接エクスポートできます。TiDB TiDB Lightningを使用してインポートする場合は、 Dumpling がデータをエクスポートするディレクトリとして`data-source-dir`指定できます。
-   2 つのシャード テーブルのデータが別の MySQL ノードに分散されている場合は、 Dumpling を使用して個別にエクスポートする必要があります。エクスポートされたデータは、同じ親ディレクトリ<b>内の異なるサブディレクトリ</b>に配置する必要があります。TiDB TiDB Lightning を使用して並列インポートを実行する場合は、親ディレクトリとして`data-source-dir`指定する必要があります。

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

データ ソースが Amazon S3 や GCS などの外部storageに保存されている場合は、接続用の追加パラメータを設定する必要があります。このような設定のパラメータを指定できます。たとえば、次の例では、データが Amazon S3 に保存されていると想定しています。

    tiup tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup'

詳細なパラメータの説明については、 [外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。

### ステップ3: TiDB Lightningを起動してデータをインポートする {#step-3-start-tidb-lightning-to-import-data}

並列インポート中、各TiDB Lightningノードのサーバー構成要件は、非並列インポート モードと同じです。各TiDB Lightningノードは同じリソースを消費する必要があります。異なるサーバーに展開することをお勧めします。詳細な展開手順については、 [TiDB Lightning をデプロイ](/tidb-lightning/deploy-tidb-lightning.md)参照してください。

各サーバーでTiDB Lightning を順番に起動します。コマンドラインから`nohup`使用して直接起動すると、SIGHUP シグナルにより終了する可能性があります。そのため、スクリプトに`nohup`入れることをお勧めします。例:

```shell
# !/bin/bash
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
```

並列インポート中、 TiDB Lightning はタスクの開始後に次のチェックを自動的に実行します。

-   ローカル ディスク ( `sort-kv-dir`構成によって制御) と TiKV クラスターに、データをインポートするのに十分なスペースがあるかどうかを確認します。必要なディスク スペースについては、 [下流のstorageスペース要件](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database)と[リソース要件](/tidb-lightning/tidb-lightning-physical-import-mode.md#environment-requirements)を参照してください。TiDB TiDB Lightning はデータ ソースをサンプリングし、サンプル結果からインデックス サイズのパーセンテージを推定します。推定にはインデックスが含まれるため、ソース データのサイズがローカル ディスクの使用可能なスペースよりも小さい場合でも、チェックが失敗する場合があります。
-   TiKV クラスター内の領域が均等に分散されているかどうか、および空の領域が多すぎないかどうかを確認します。空の領域の数が max(1000、テーブル数 * 3) を超える場合、つまり「1000」または「テーブル数の 3 倍」のいずれか大きい方を超える場合、インポートは実行できません。
-   データソースからデータが順番にインポートされているかを確認します。 `mydumper.batch-size`のサイズは、チェックの結果に基づいて自動的に調整されます。 そのため、 `mydumper.batch-size`構成は使用できなくなります。

チェックをオフにして、 `lightning.check-requirements`構成で強制インポートを実行することもできます。詳細なチェックについては、 [TiDB Lightning事前チェック](/tidb-lightning/tidb-lightning-prechecks.md)を参照してください。

### ステップ4: インポートの進行状況を確認する {#step-4-check-the-import-progress}

インポートを開始した後、次のいずれかの方法で進行状況を確認できます。

-   `grep` log キーワード`progress`で進行状況を確認します。デフォルトでは 5 分ごとに更新されます。
-   監視コンソールから進行状況を確認します。詳細については、 [TiDB Lightning監視](/tidb-lightning/monitor-tidb-lightning.md)参照してください。

すべてのTiDB Lightningインスタンスが終了するまで待機すると、インポート全体が完了します。

## 例2: 単一のテーブルを並列でインポートする {#example-2-import-single-tables-in-parallel}

TiDB Lightning は、単一テーブルの並列インポートもサポートしています。たとえば、異なるTiDB Lightningインスタンスによって Amazon S3 に保存された複数の単一テーブルを、下流の TiDB クラスターに並列でインポートします。この方法により、全体的なインポート速度が向上します。Amazon S3 などのリモートストレージを使用する場合、 TiDB Lightningの構成パラメータはBRと同じです。詳細については、 [外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。

> **注記：**
>
> ローカル環境では、 Dumplingの`--filesize`または`--where`パラメータを使用して、1 つのテーブルのデータを複数の部分に分割し、複数のサーバーのローカル ディスクに事前にエクスポートすることができます。この方法でも、並列インポートを実行できます。構成は例 1 と同じです。

ソースファイルが Amazon S3 に保存されていると仮定すると、テーブルファイルは`my_db.my_table.00001.sql` ~ `my_db.my_table.10000.sql` 、合計 10,000 個の SQL ファイルになります。インポートを高速化するために 2 つのTiDB Lightningインスタンスを使用する場合は、構成ファイルに次の設定を追加する必要があります。

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

-   ネットワーク タイムアウトなど、エラーがデータの精度に影響を与えない場合は、次の手順を実行します。

    1.  チェックポイント ソース データのエラーを消去するには、障害が発生したすべてのノードで設定`--checkpoint-error-ignore=all`で[`checkpoint-error-ignore`](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-ignore)コマンドを実行します。

    2.  チェックポイントからのデータのインポートを続行するには、これらのノードを再起動します。

-   ソース ファイル内の無効なデータを示すチェックサムの不一致など、データの不正確さにつながるエラーがログに表示される場合は、次の手順を実行してこの問題を解決できます。

    1.  成功したノードを含むすべての Lightning ノードで[`checkpoint-error-destroy`](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy)コマンドを実行します。このコマンドは、失敗したテーブルからインポートされたデータを削除し、これらのテーブルのチェックポイント ステータスを「まだ開始されていません」にリセットします。

    2.  正常に終了するノードを含むすべてのTiDB Lightningノードで[`filter`](/table-filter.md)パラメータを使用して、失敗したテーブルのデータを再構成してインポートします。

        Lightning 並列インポート タスクを再構成する場合、各 Lightning ノードの起動スクリプトに`checkpoint-error-destroy`コマンドを含めないでください。そうしないと、このコマンドによって複数の並列インポート タスクで使用される共有メタデータが削除され、データのインポート中に問題が発生する可能性があります。たとえば、2 番目の Lightning インポート タスクが開始されると、最初のタスクによって書き込まれたメタデータが削除され、異常なデータ インポートが発生します。

### インポート中に、「ターゲット テーブルがチェックサムを計算しています。チェックサムが完了するまで待ってから、もう一度お試しください」というエラーが報告されます。 {#during-an-import-an-error-target-table-is-calculating-checksum-please-wait-until-the-checksum-is-finished-and-try-again-is-reported}

一部の並列インポートには、多数のテーブルまたは少量のデータを含むテーブルが含まれます。この場合、1 つ以上のタスクがテーブルの処理を開始する前に、このテーブルの他のタスクが終了し、データのチェックサムが進行中である可能性があります。この時点で、エラー`Target table is calculating checksum. Please wait until the checksum is finished and try again`が報告されます。この場合、チェックサムの完了を待ってから、失敗したタスクを再開できます。エラーは消え、データの精度には影響しません。
