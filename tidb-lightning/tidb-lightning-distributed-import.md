---
title: Use TiDB Lightning to Import Data in Parallel
summary: Learn the concept, user scenarios, usages, and limitations of importing data in parallel when using TiDB Lightning.
---

# TiDB Lightning を使用してデータを並行してインポートする {#use-tidb-lightning-to-import-data-in-parallel}

v5.3.0 以降、 TiDB Lightningの[ローカル バックエンド モード](/tidb-lightning/tidb-lightning-backends.md#tidb-lightning-local-backend)単一テーブルまたは複数テーブルの並列インポートをサポートしています。複数のTiDB Lightningインスタンスを同時に実行することで、異なる単一のテーブルまたは複数のテーブルからデータを並行してインポートできます。このように、 TiDB Lightning は水平方向にスケーリングする機能を提供し、大量のデータのインポートに必要な時間を大幅に短縮できます。

技術的な実装では、 TiDB Lightning は各インスタンスのメタデータとインポートされた各テーブルのデータをターゲット TiDB に記録し、異なるインスタンスの Row ID 割り当て範囲、グローバル チェックサムの記録、および TiKV の構成変更と回復を調整します。とPD。

次のシナリオでは、 TiDB Lightning を使用してデータを並行してインポートできます。

-   シャード スキーマとシャード テーブルをインポートします。このシナリオでは、複数のアップストリーム データベース インスタンスからの複数のテーブルが、異なるTiDB Lightningインスタンスによって並行してダウンストリーム TiDB データベースにインポートされます。
-   単一のテーブルを並行してインポートします。このシナリオでは、特定のディレクトリまたはクラウドstorage(Amazon S3 など) に保存されている単一のテーブルが、異なるTiDB Lightningインスタンスによって並行して下流の TiDB クラスターにインポートされます。これは TiDB 5.3.0 で導入された新機能です。

> **ノート：**
>
> -   並列インポートは、TiDB で初期化された空のテーブルのみをサポートし、既存のサービスによって書き込まれたデータを含むテーブルへのデータの移行はサポートしていません。そうしないと、データの不整合が発生する可能性があります。
>
> -   並列インポートは通常、ローカル バックエンド モードで使用されます。
>
> -   複数のTiDB Lightningインスタンスを使用して同じターゲットにデータをインポートする場合は、一度に 1 つのバックエンドのみを適用します。たとえば、ローカル バックエンド モードと TiDB バックエンド モードの両方で同時に同じ TiDB クラスターにデータをインポートすることはできません。

## 考慮事項 {#considerations}

TiDB Lightningを使用したパラレル インポートでは、追加の構成は必要ありません。 TiDB Lightningを起動すると、下流の TiDB クラスターにメタデータを登録し、同時にターゲット クラスターにデータを移行している他のインスタンスが存在するかどうかを自動的に検出します。あれば自動的に並行輸入モードに入る。

ただし、データを並行して移行する場合は、次の点を考慮する必要があります。

-   複数のシャード テーブル間で主キーまたは一意のインデックス間の競合を処理する
-   インポートのパフォーマンスを最適化する

### 主キーまたは一意のインデックス間の競合を処理する {#handle-conflicts-between-primary-keys-or-unique-indexes}

[ローカル バックエンド モード](/tidb-lightning/tidb-lightning-backends.md#tidb-lightning-local-backend)を使用して並行してインポートする場合、データ ソース間、およびターゲット TiDB クラスター内のテーブル間で主キーまたは一意のインデックスの競合がないことを確認する必要があります。インポート中にターゲット テーブルにデータ書き込みがないことを確認します。そうしないと、 TiDB Lightning はインポートされたデータの正確性を保証できず、インポートの完了後にターゲット テーブルに一貫性のないインデックスが含まれます。

### インポートのパフォーマンスを最適化する {#optimize-import-performance}

TiDB Lightning は、生成された Key-Value データを、対応するリージョンの各コピーが配置されている TiKV ノードにアップロードする必要があるため、インポート速度はターゲット クラスターのサイズによって制限されます。ターゲット TiDB クラスター内の TiKV インスタンスの数とTiDB Lightningインスタンスの数が n:1 より大きいことを確認することをお勧めします (n はリージョンのコピーの数です)。同時に、最適なインポート パフォーマンスを実現するには、次の要件を満たす必要があります。

-   各TiDB Lightningインスタンスを専用マシンにデプロイ。デフォルトでは、1 つのTiDB Lightningインスタンスがすべての CPU リソースを消費するため、1 台のマシンに複数のインスタンスをデプロイしてもパフォーマンスは向上しません。
-   並列インポートを実行する各TiDB Lightningインスタンスのソース ファイルの合計サイズは、5 TiB 未満にする必要があります。
-   TiDB Lightningインスタンスの総数は 10 未満にする必要があります。

TiDB Lightningを使用して共有データベースとテーブルを並行してインポートする場合は、データ量に応じて適切な数のTiDB Lightningインスタンスを選択してください。

-   MySQL データ ボリュームが 2 TiB 未満の場合は、1 つのTiDB Lightningインスタンスを並列インポートに使用できます。
-   MySQL データ ボリュームが 2 TiB を超え、MySQL インスタンスの総数が 10 未満の場合、各 MySQL インスタンスに 1 つのTiDB Lightningインスタンスを使用し、並列TiDB Lightningインスタンスの数が 10 を超えないようにすることをお勧めします。
-   MySQL データ ボリュームが 2 TiB を超え、MySQL インスタンスの総数が 10 を超える場合、これらの MySQL インスタンスによってエクスポートされたデータをインポートするために、5 ～ 10 のTiDB Lightningインスタンスを割り当てることをお勧めします。

次に、このドキュメントでは 2 つの例を使用して、さまざまなシナリオでの並行輸入の操作手順を詳しく説明します。

-   例 1: Dumpling + TiDB Lightningを使用して、シャードされたデータベースとテーブルを TiDB に並行してインポートする
-   例 2: 単一のテーブルを並行してインポートする

### 制限 {#restrictions}

TiDB Lightning は、実行中に一部のリソースを排他的に使用します。複数のTiDB Lightningインスタンスを単一のマシン (本番環境には推奨されません) または複数のマシンで共有されるディスクにデプロイする必要がある場合は、次の使用制限に注意してください。

-   TiDB Lightningインスタンスごとに一意のパスに`tikv-importer.sorted-kv-dir`を設定します。複数のインスタンスが同じパスを共有すると、意図しない動作が発生する可能性があり、インポートの失敗やデータ エラーが発生する可能性があります。
-   各TiDB Lightningチェックポイントを個別に保存します。チェックポイント構成の詳細については、 [TiDB Lightningチェックポイント](/tidb-lightning/tidb-lightning-checkpoints.md)を参照してください。
    -   checkpoint.driver = &quot;file&quot; (デフォルト) を設定する場合は、チェックポイントへのパスがインスタンスごとに一意であることを確認してください。
    -   checkpoint.driver = &quot;mysql&quot; を設定する場合、インスタンスごとに一意のスキーマを設定する必要があります。
-   各TiDB Lightningのログ ファイルは、一意のパスに設定する必要があります。同じログ ファイルを共有すると、ログのクエリとトラブルシューティングに影響します。
-   [ウェブインターフェース](/tidb-lightning/tidb-lightning-web-interface.md)または Debug API を使用する場合は、インスタンスごとに一意のアドレスに`lightning.status-addr`を設定する必要があります。そうしないと、ポートの競合が原因でTiDB Lightningプロセスの開始に失敗します。

## 例 1: Dumpling + TiDB Lightningを使用して、シャードされたデータベースとテーブルを並列で TiDB にインポートする {#example-1-use-dumpling-tidb-lightning-to-import-sharded-databases-and-tables-into-tidb-in-parallel}

この例では、アップストリームが 10 個のシャード テーブルを持つ MySQL クラスターであり、合計サイズが 10 TiB であると想定しています。 5 つのTiDB Lightningインスタンスを使用して並列インポートを実行でき、各インスタンスは 2 TiB をインポートします。合計のインポート時間 (Dumplingのエクスポートに必要な時間を除く) は、約 40 時間から約 10 時間に短縮できると推定されます。

アップストリーム ライブラリの名前が`my_db`で、各シャード テーブルの名前が`my_table_01` ~ `my_table_10`であるとします。それらをマージして下流の`my_db.my_table`テーブルにインポートします。具体的な手順については、次のセクションで説明します。

### ステップ 1: Dumpling を使用してデータをエクスポートする {#step-1-use-dumpling-to-export-data}

TiDB Lightningがデプロイされている 5 つのノードで 2 つのシャード テーブルをエクスポートします。

-   2 つのシャード テーブルが同じ MySQL インスタンスにある場合は、 Dumplingの`--filter`パラメータを使用してそれらを直接エクスポートできます。 TiDB Lightningを使用してインポートする場合、 Dumpling がデータをエクスポートするディレクトリとして`data-source-dir`指定できます。
-   2 つのシャード テーブルのデータが異なる MySQL ノードに分散されている場合は、 Dumpling を使用してそれらを個別にエクスポートする必要があります。エクスポートされたデータは、同じ親ディレクトリに配置する必要があります<b>が、異なるサブディレクトリに</b>配置する必要があります。 TiDB Lightningを使用して並列インポートを実行する場合、親ディレクトリとして`data-source-dir`を指定する必要があります。

Dumpling を使用してデータをエクスポートする方法の詳細については、 [Dumpling](/dumpling-overview.md)を参照してください。

### ステップ 2: TiDB Lightningデータソースを構成する {#step-2-configure-tidb-lightning-data-sources}

構成ファイル`tidb-lightning.toml`を作成し、次の内容を追加します。

```
[lightning]
status-addr = ":8289"

[mydumper]
# Specify the path for Dumpling to export data. If Dumpling performs several times and the data belongs to different directories, you can place all the exported data in the same parent directory and specify this parent directory here.
data-source-dir = "/path/to/source-dir"

[tikv-importer]
# Whether to allow importing data to tables with data. The default value is `false`.
# When you use parallel import mode, you must set it to `true`, because multiple TiDB Lightning instances are importing the same table at the same time.
incremental-import = true
# "local": The default mode. It applies to large dataset import, for example, greater than 1 TiB. However, during the import, downstream TiDB is not available to provide services.
# "tidb": You can use this mode for small dataset import, for example, smaller than 1 TiB. During the import, downstream TiDB is available to provide services.
backend = "local"

# Specify the path for local sorting data.
sorted-kv-dir = "/path/to/sorted-dir"

# Specify the routes for shard schemas and tables.
[[routes]]
schema-pattern = "my_db"
table-pattern = "my_table_*"
target-schema = "my_db"
target-table = "my_table"
```

データ ソースが Amazon S3 や GCS などの外部storageに保存されている場合は、 [外部ストレージ](/br/backup-and-restore-storages.md)を参照してください。

### ステップ 3: TiDB Lightning を起動してデータをインポートする {#step-3-start-tidb-lightning-to-import-data}

並行インポート中、各TiDB Lightningノードのサーバー構成要件は、非並行インポート モードと同じです。各TiDB Lightningノードは同じリソースを消費する必要があります。それらを異なるサーバーにデプロイすることをお勧めします。詳細な導入手順については、 [TiDB Lightningをデプロイ](/tidb-lightning/deploy-tidb-lightning.md)を参照してください。

各サーバーで順番にTiDB Lightningを開始します。 `nohup`を使用してコマンド ラインから直接起動すると、SIGHUP シグナルが原因で終了する場合があります。したがって、スクリプトに`nohup`入れることをお勧めします。たとえば、次のようになります。

```shell
# !/bin/bash
nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
```

並行インポート中、 TiDB Lightning はタスクの開始後に次のチェックを自動的に実行します。

-   ローカル ディスク ( `sort-kv-dir`構成で制御) と TiKV クラスターに、データをインポートするための十分なスペースがあるかどうかを確認します。 TiDB Lightning はデータ ソースをサンプリングし、サンプル結果からインデックス サイズのパーセンテージを推定します。推定にはインデックスが含まれているため、ソース データのサイズがローカル ディスクの使用可能な領域よりも小さい場合がありますが、それでもチェックは失敗します。
-   TiKV クラスター内のリージョンが均等に分散されているかどうか、および空のリージョンが多すぎるかどうかを確認します。空の領域の数が max(1000, テーブル数 * 3) を超える場合、つまり、「1000」または「テーブル数の 3 倍」のいずれか大きい方より大きい場合、インポートは実行できません。
-   データソースから順番にデータがインポートされているか確認してください。 `mydumper.batch-size`のサイズは、チェックの結果に基づいて自動的に調整されます。したがって、 `mydumper.batch-size`構成は使用できなくなりました。

チェックをオフにして、 `lightning.check-requirements`構成で強制インポートを実行することもできます。詳細なチェックについては、 [TiDB Lightningの事前チェック](/tidb-lightning/tidb-lightning-prechecks.md)を参照してください。

### ステップ 4: インポートの進行状況を確認する {#step-4-check-the-import-progress}

インポートを開始したら、次のいずれかの方法で進行状況を確認できます。

-   `grep`ログ キーワード`progress`で進行状況を確認します。デフォルトでは 5 分ごとに更新されます。
-   監視コンソールで進行状況を確認します。詳細については、 [TiDB Lightningモニタリング](/tidb-lightning/monitor-tidb-lightning.md)を参照してください。

すべてのTiDB Lightningインスタンスが完了するまで待ってから、インポート全体が完了します。

## 例 2: 単一のテーブルを並行してインポートする {#example-2-import-single-tables-in-parallel}

TiDB Lightning は、単一テーブルの並列インポートもサポートしています。たとえば、異なるTiDB Lightningインスタンスによって Amazon S3 に格納された複数の単一テーブルを、下流の TiDB クラスターに並行してインポートします。この方法により、全体的なインポート速度を高速化できます。外部ストレージの詳細については、 [外部ストレージ](/br/backup-and-restore-storages.md) ) を参照してください。

> **ノート：**
>
> ローカル環境では、 Dumplingの`--filesize`または`--where`パラメータを使用して、1 つのテーブルのデータを複数のパーツに分割し、複数のサーバーのローカル ディスクに事前にエクスポートできます。このようにして、並行インポートを引き続き実行できます。構成は例 1 と同じです。

ソースファイルが Amazon S3 に保存されていると仮定すると、テーブルファイルは`my_db.my_table.00001.sql` ~ `my_db.my_table.10000.sql`で、合計 10,000 個の SQL ファイルです。インポートを高速化するために 2 つのTiDB Lightningインスタンスを使用する場合は、構成ファイルに次の設定を追加する必要があります。

```
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
```

`05001 ~ 10000`データ ファイルのみをインポートするように、他のインスタンスの構成を変更できます。

その他の手順については、例 1 の関連する手順を参照してください。

## エラー処理 {#handle-errors}

### 一部のTiDB Lightningノードが異常終了する {#some-tidb-lightning-nodes-exit-abnormally}

並列インポート中に 1 つ以上のTiDB Lightningノードが異常終了した場合は、ログに記録されたエラーに基づいて原因を特定し、エラーの種類に従ってエラーを処理します。

-   エラーが通常の終了 (たとえば、kill コマンドに応じた終了) または OOM によるオペレーティング システムによる終了を示している場合は、構成を調整してからTiDB Lightningノードを再起動します。

-   ネットワーク タイムアウトなど、エラーがデータの精度に影響を与えない場合は、次の手順を実行します。

    1.  障害が発生したすべてのノードで設定`--checkpoint-error-ignore=all`指定して[`checkpoint-error-ignore`](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-ignore)コマンドを実行し、チェックポイント ソース データのエラーを消去します。

    2.  これらのノードを再起動して、チェックポイントからのデータのインポートを続行します。

-   ソース ファイル内の無効なデータを示すチェックサムの不一致など、データが不正確になるエラーがログに表示される場合は、次の手順を実行してこの問題を解決できます。

    1.  成功したノードを含むすべての Lightning ノードで[`checkpoint-error-destroy`](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy)コマンドを実行します。このコマンドは、失敗したテーブルからインポートされたデータを削除し、これらのテーブルのチェックポイント ステータスを「未開始」にリセットします。

    2.  正常に終了しているノードを含むすべてのTiDB Lightningノードで[`filter`](/table-filter.md)パラメータを使用して、失敗したテーブルのデータを再構成してインポートします。

        Lightning 並列インポート タスクを再設定するときは、各 Lightning ノードの起動スクリプトに`checkpoint-error-destroy`コマンドを含めないでください。それ以外の場合、このコマンドは複数の並列インポート タスクで使用される共有メタデータを削除するため、データ インポート中に問題が発生する可能性があります。たとえば、2 番目の Lightning インポート タスクが開始されると、最初のタスクによって書き込まれたメタデータが削除され、異常なデータ インポートが発生します。

### インポート中に、「ターゲット テーブルはチェックサムを計算しています。チェックサムが完了するまで待ってから、もう一度やり直してください」というエラーが報告される {#during-an-import-an-error-target-table-is-calculating-checksum-please-wait-until-the-checksum-is-finished-and-try-again-is-reported}

一部の並行インポートには、多数のテーブルまたは少量のデータを含むテーブルが含まれます。この場合、1 つ以上のタスクがテーブルの処理を開始する前に、このテーブルの他のタスクが終了し、データ チェックサムが進行中である可能性があります。このとき、エラー`Target table is calculating checksum. Please wait until the checksum is finished and try again`が報告されます。この場合、チェックサムの完了を待ってから、失敗したタスクを再開できます。エラーはなくなり、データの精度は影響を受けません。
