---
title: Use TiDB Lightning to Import Data in Parallel
summary: Learn the concept, user scenarios, usages, and limitations of importing data in parallel when using TiDB Lightning.
---

# TiDB Lightning を使用してデータを並行してインポートする {#use-tidb-lightning-to-import-data-in-parallel}

v5.3.0 以降、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md) 、単一テーブルまたは複数テーブルの並列インポートをサポートしています。複数のTiDB Lightningインスタンスを同時に実行することにより、異なる単一テーブルまたは複数のテーブルから並行してデータをインポートできます。このように、 TiDB Lightning は水平方向に拡張する機能を提供し、大量のデータのインポートに必要な時間を大幅に短縮します。

技術的な実装では、 TiDB Lightning は、各インスタンスのメタデータとインポートされた各テーブルのデータをターゲット TiDB に記録し、さまざまなインスタンスの Row ID 割り当て範囲、グローバル チェックサムの記録、TiKV の構成変更とリカバリを調整します。そしてPD。

TiDB Lightning を使用すると、次のシナリオでデータを並行してインポートできます。

-   シャード化されたスキーマとシャード化されたテーブルをインポートします。このシナリオでは、複数の上流データベース インスタンスからの複数のテーブルが、異なるTiDB Lightningインスタンスによって並行してダウンストリーム TiDB データベースにインポートされます。
-   単一のテーブルを並行してインポートします。このシナリオでは、特定のディレクトリまたはクラウドstorage(Amazon S3 など) に保存されている単一のテーブルが、異なるTiDB Lightningインスタンスによって並行してダウンストリーム TiDB クラスターにインポートされます。これは、TiDB 5.3.0 で導入された新機能です。

> **注記：**
>
> -   並列インポートでは、TiDB 内の初期化された空のテーブルのみがサポートされ、既存のサービスによって書き込まれたデータを含むテーブルへのデータの移行はサポートされません。そうしないと、データの不整合が発生する可能性があります。
>
> -   平行輸入は通常、物理輸入モードで使用されます。 `parallel-import = true`を設定する必要があります。
>
> -   複数のTiDB Lightningインスタンスを使用して同じターゲットにデータをインポートする場合は、一度に 1 つのバックエンドのみを適用します。たとえば、物理インポート モードと論理インポート モードの両方で同時に同じ TiDB クラスターにデータをインポートすることはできません。

## 考慮事項 {#considerations}

平行輸入を使用するには、 `parallel-import = true`を設定する必要があります。 TiDB Lightningが開始されると、ダウンストリーム TiDB クラスターにメタデータが登録され、同時にターゲット クラスターにデータを移行している他のインスタンスがあるかどうかが自動的に検出されます。存在する場合は、自動的に平行輸入モードに入ります。

ただし、データを並行して移行する場合は、次の点を考慮する必要があります。

-   複数のシャードテーブルにわたる主キーまたは一意のインデックス間の競合を処理する
-   インポートのパフォーマンスを最適化する

### 主キーまたは一意のインデックス間の競合を処理する {#handle-conflicts-between-primary-keys-or-unique-indexes}

[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)を使用してデータを並行してインポートする場合は、データ ソース間およびターゲット TiDB クラスター内のテーブル間で主キーまたは一意のインデックスの競合がないこと、およびインポート中にターゲット テーブルにデータが書き込まれないことを確認してください。そうしないと、 TiDB Lightning はインポートされたデータの正確性を保証できなくなり、インポート完了後にターゲット テーブルに一貫性のないインデックスが含まれることになります。

### インポートのパフォーマンスを最適化する {#optimize-import-performance}

TiDB Lightning は、生成された Key-Value データを、対応するリージョンの各コピーが配置されている TiKV ノードにアップロードする必要があるため、インポート速度はターゲット クラスターのサイズによって制限されます。ターゲット TiDB クラスター内の TiKV インスタンスの数とTiDB Lightningインスタンスの数が n:1 (n はリージョンのコピーの数) より大きいことを確認することをお勧めします。同時に、最適なインポート パフォーマンスを達成するには、次の要件を満たす必要があります。

-   各TiDB Lightningインスタンスを専用マシンにデプロイ。デフォルトでは 1 つのTiDB Lightningインスタンスがすべての CPU リソースを消費するため、1 台のマシンに複数のインスタンスをデプロイしてもパフォーマンスを向上させることはできません。
-   並列インポートを実行する各TiDB Lightningインスタンスのソース ファイルの合計サイズは 5 TiB 未満である必要があります。
-   TiDB Lightningインスタンスの合計数は 10 未満である必要があります。

TiDB Lightningを使用して共有データベースと共有テーブルを並行してインポートする場合は、データ量に応じて適切な数のTiDB Lightningインスタンスを選択します。

-   MySQL データ ボリュームが 2 TiB 未満の場合は、並列インポートに 1 つのTiDB Lightningインスタンスを使用できます。
-   MySQL データ ボリュームが 2 TiB を超え、MySQL インスタンスの合計数が 10 未満の場合は、MySQL インスタンスごとに 1 つのTiDB Lightningインスタンスを使用し、並列TiDB Lightningインスタンスの数が 10 を超えないようにすることをお勧めします。
-   MySQL データ ボリュームが 2 TiB を超え、MySQL インスタンスの合計数が 10 を超える場合は、これらの MySQL インスタンスによってエクスポートされたデータをインポートするために 5 ～ 10 個のTiDB Lightningインスタンスを割り当てることをお勧めします。

次に、このドキュメントでは 2 つの例を使用して、さまざまなシナリオでの並行インポートの操作手順を詳しく説明します。

-   例 1: Dumpling + TiDB Lightningを使用して、シャード化されたデータベースとテーブルを TiDB に並行してインポートする
-   例 2: 単一テーブルを並行してインポートする

### 制限 {#restrictions}

TiDB Lightning は、実行中に一部のリソースを排他的に使用します。複数のTiDB Lightningインスタンスを 1 台のマシン (本番環境には推奨されません) または複数のマシンで共有されるディスクにデプロイする必要がある場合は、次の使用制限に注意してください。

-   各TiDB Lightningインスタンスの一意のパスに`tikv-importer.sorted-kv-dir`を設定します。複数のインスタンスが同じパスを共有すると、意図しない動作が発生し、インポートの失敗やデータ エラーが発生する可能性があります。
-   各TiDB Lightningチェックポイントを個別に保存します。チェックポイント構成の詳細については、 [TiDB Lightningチェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)を参照してください。
    -   Checkpoint.driver = &quot;file&quot; (デフォルト) を設定する場合は、チェックポイントへのパスがインスタンスごとに一意であることを確認してください。
    -   Checkpoint.driver = &quot;mysql&quot; を設定する場合は、インスタンスごとに一意のスキーマを設定する必要があります。
-   各TiDB Lightningのログ ファイルは一意のパスに設定する必要があります。同じログ ファイルを共有すると、ログのクエリとトラブルシューティングに影響します。
-   [ウェブインターフェース](/tidb-lightning/tidb-lightning-web-interface.md)または Debug API を使用する場合は、 `lightning.status-addr`各インスタンスの一意のアドレスに設定する必要があります。そうしないと、ポートの競合によりTiDB Lightningプロセスの開始に失敗します。

## 例 1: Dumpling + TiDB Lightningを使用して、シャード化されたデータベースとテーブルを TiDB に並行してインポートする {#example-1-use-dumpling-tidb-lightning-to-import-sharded-databases-and-tables-into-tidb-in-parallel}

この例では、アップストリームが 10 個のシャード テーブルを持ち、合計サイズが 10 TiB の MySQL クラスターであると仮定します。 5 つのTiDB Lightningインスタンスを使用して並行インポートを実行でき、各インスタンスは 2 TiB をインポートします。総輸入時間（Dumplingの輸出時間を除く）は約40時間から約10時間に短縮できる見込みです。

上流ライブラリの名前が`my_db` 、各シャードテーブルの名前が`my_table_01` ~ `my_table_10`であると仮定します。これらをマージしてダウンストリーム`my_db.my_table`テーブルにインポートしたいと考えています。具体的な手順については、次のセクションで説明します。

### ステップ 1: Dumpling を使用してデータをエクスポートする {#step-1-use-dumpling-to-export-data}

TiDB Lightningがデプロイされている 5 つのノード上で 2 つのシャード テーブルをエクスポートします。

-   2 つのシャード テーブルが同じ MySQL インスタンス内にある場合は、 Dumplingの`--filter`パラメータを使用してそれらを直接エクスポートできます。 TiDB Lightningを使用してインポートする場合、 Dumpling がデータをエクスポートするディレクトリとして`data-source-dir`指定できます。
-   2 つのシャード テーブルのデータが異なる MySQL ノードに分散されている場合は、 Dumpling を使用してそれらを個別にエクスポートする必要があります。エクスポートされたデータは、同じ親ディレクトリに<b>、異なるサブディレクトリに</b>配置する必要があります。 TiDB Lightningを使用して並行インポートを実行する場合、親ディレクトリとして`data-source-dir`を指定する必要があります。

Dumpling を使用してデータをエクスポートする方法の詳細については、 [Dumpling](/dumpling-overview.md)を参照してください。

### ステップ 2: TiDB Lightningデータソースを構成する {#step-2-configure-tidb-lightning-data-sources}

構成ファイル`tidb-lightning.toml`を作成し、次の内容を追加します。

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

データ ソースが Amazon S3 や GCS などの外部storageに保存されている場合は、接続用の追加パラメータを設定する必要があります。このような構成にはパラメータを指定できます。たとえば、次の例では、データが Amazon S3 に保存されていることを前提としています。

    ./tidb-lightning --tidb-port=4000 --pd-urls=127.0.0.1:2379 --backend=local --sorted-kv-dir=/tmp/sorted-kvs \
        -d 's3://my-bucket/sql-backup'

パラメーターの詳細については、 [外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。

### ステップ 3: TiDB Lightning を開始してデータをインポートする {#step-3-start-tidb-lightning-to-import-data}

並行インポート中の各TiDB Lightningノードのサーバー構成要件は、非並行インポート モードと同じです。各TiDB Lightningノードは同じリソースを消費する必要があります。それらを別のサーバーにデプロイすることをお勧めします。詳細な展開手順については、 [TiDB Lightningのデプロイ](/tidb-lightning/deploy-tidb-lightning.md)を参照してください。

各サーバーでTiDB Lightning を順番に起動します。 `nohup`を使用してコマンド ラインから直接開始すると、SIGHUP シグナルにより終了する可能性があります。したがって、スクリプトに`nohup`入れることをお勧めします。例:

```shell
# !/bin/bash
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
```

並行インポート中、 TiDB Lightning はタスクの開始後に次のチェックを自動的に実行します。

-   ローカル ディスク ( `sort-kv-dir`構成によって制御される) と TiKV クラスターにデータをインポートするための十分なスペースがあるかどうかを確認します。必要なディスク容量については、 [ダウンストリームのstorageスペース要件](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database)および[リソース要件](/tidb-lightning/tidb-lightning-physical-import-mode.md#environment-requirements)を参照してください。 TiDB Lightning はデータ ソースをサンプリングし、サンプル結果からインデックス サイズのパーセンテージを推定します。推定にはインデックスが含まれるため、ソース データのサイズがローカル ディスク上の利用可能な領域より小さい場合でも、チェックは失敗する場合があります。
-   TiKV クラスター内のリージョンが均等に分散されているかどうか、および空のリージョンが多すぎるかどうかを確認します。空領域の数が max(1000, テーブル数 * 3) を超える場合、つまり「1000」または「テーブル数の 3 倍」の大きい方を超える場合、インポートは実行できません。
-   データがデータソースから順番にインポートされているかどうかを確認します。 `mydumper.batch-size`のサイズはチェックの結果に基づいて自動的に調整されます。したがって、 `mydumper.batch-size`構成は使用できなくなりました。

チェックをオフにして、 `lightning.check-requirements`構成で強制インポートを実行することもできます。より詳細なチェックについては、 [TiDB Lightning の事前チェック](/tidb-lightning/tidb-lightning-prechecks.md)を参照してください。

### ステップ 4: インポートの進行状況を確認する {#step-4-check-the-import-progress}

インポートを開始した後、次のいずれかの方法で進行状況を確認できます。

-   `grep`ログキーワード`progress`で進行状況を確認します。デフォルトでは 5 分ごとに更新されます。
-   監視コンソールで進捗状況を確認します。詳細は[TiDB Lightning監視](/tidb-lightning/monitor-tidb-lightning.md)を参照してください。

すべてのTiDB Lightningインスタンスが完了するまで待ってから、インポート全体が完了します。

## 例 2: 単一テーブルを並行してインポートする {#example-2-import-single-tables-in-parallel}

TiDB Lightning は、単一テーブルの並行インポートもサポートしています。たとえば、異なるTiDB Lightningインスタンスによって Amazon S3 に保存されている複数の単一テーブルをダウンストリーム TiDB クラスターに並行してインポートします。この方法により、全体的なインポート速度が向上します。 Amazon S3 などのリモート ストレージを使用する場合、 TiDB Lightningの設定パラメータはBRの設定パラメータと同じです。詳細については、 [外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。

> **注記：**
>
> ローカル環境では、 Dumplingの`--filesize`または`--where`パラメータを使用して、1 つのテーブルのデータを複数の部分に分割し、複数のサーバーのローカル ディスクに事前にエクスポートできます。この方法でも並行輸入を行うことができます。構成は例1と同じです。

ソースファイルが Amazon S3 に保存されているとすると、テーブルファイルは`my_db.my_table.00001.sql` ～ `my_db.my_table.10000.sql` 、合計 10,000 個の SQL ファイルになります。 2 つのTiDB Lightningインスタンスを使用してインポートを高速化する場合は、構成ファイルに次の設定を追加する必要があります。

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

`05001 ~ 10000`データ ファイルのみをインポートするように他のインスタンスの構成を変更できます。

他の手順については、例 1 の関連する手順を参照してください。

## エラーを処理する {#handle-errors}

### 一部のTiDB Lightningノードが異常終了します {#some-tidb-lightning-nodes-exit-abnormally}

並行インポート中に 1 つ以上のTiDB Lightningノードが異常終了した場合は、ログに記録されたエラーに基づいて原因を特定し、エラー タイプに応じてエラーを処理します。

-   エラーが通常の終了 (たとえば、kill コマンドに応答した終了) または OOM によるオペレーティング システムによる終了を示している場合は、構成を調整してからTiDB Lightningノードを再起動します。

-   ネットワーク タイムアウトなど、エラーがデータの精度に影響を与えない場合は、次の手順を実行します。

    1.  失敗したすべてのノードで設定`--checkpoint-error-ignore=all`指定して[`checkpoint-error-ignore`](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-ignore)コマンドを実行し、チェックポイント ソース データのエラーを消去します。

    2.  チェックポイントからのデータのインポートを続行するには、これらのノードを再起動します。

-   ソース ファイル内の無効なデータを示すチェックサムの不一致など、データの不正確さを引き起こすエラーがログに表示された場合は、次の手順を実行してこの問題を解決できます。

    1.  成功したノードを含むすべての Lightning ノードで[`checkpoint-error-destroy`](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy)コマンドを実行します。このコマンドは、失敗したテーブルからインポートされたデータを削除し、これらのテーブルのチェックポイント ステータスを「未開始」にリセットします。

    2.  正常に終了しているノードを含むすべてのTiDB Lightningノードで[`filter`](/table-filter.md)パラメータを使用して、失敗したテーブルのデータを再構成してインポートします。

        Lightning 並列インポートタスクを再設定する場合は、各 Lightning ノードの起動スクリプトに`checkpoint-error-destroy`コマンドを含めないでください。それ以外の場合、このコマンドは複数の並列インポート タスクで使用される共有メタデータを削除するため、データ インポート中に問題が発生する可能性があります。たとえば、2 番目の Lightning インポートタスクが開始されると、最初のタスクによって書き込まれたメタデータが削除され、異常なデータインポートが発生します。

### インポート中に、「ターゲット テーブルはチェックサムを計算しています。チェックサムが完了するまで待ってからもう一度お試しください」というエラーが報告されます。 {#during-an-import-an-error-target-table-is-calculating-checksum-please-wait-until-the-checksum-is-finished-and-try-again-is-reported}

一部の並行インポートには、多数のテーブル、または少量のデータを含むテーブルが含まれます。この場合、1 つ以上のタスクがテーブルの処理を開始する前に、このテーブルの他のタスクが終了し、データのチェックサムが進行中である可能性があります。このとき、エラー`Target table is calculating checksum. Please wait until the checksum is finished and try again`が報告されます。この場合、チェックサムの完了を待ってから、失敗したタスクを再開できます。エラーは消え、データの精度は影響を受けません。
