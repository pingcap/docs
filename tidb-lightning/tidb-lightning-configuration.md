---
title: TiDB Lightning Configuration
summary: TiDB Lightningの CLI の使用方法とサンプル構成について学習します。
---

# TiDB Lightningコンフィグレーション {#tidb-lightning-configuration}

このドキュメントでは、グローバル設定とタスク設定のサンプルを提供し、コマンドラインパラメータの使用方法を説明します。サンプル設定ファイルは[`lightning/tidb-lightning.toml`](https://github.com/pingcap/tidb/blob/master/lightning/tidb-lightning.toml)にあります。

TiDB Lightningには「グローバル」と「タスク」という2つの設定クラスがあり、構造は互換性があります。これらの違いは、 [サーバーモード](/tidb-lightning/tidb-lightning-web-interface.md)が有効な場合にのみ発生します。サーバーモードが無効（デフォルト）の場合、 TiDB Lightningは1つのタスクのみを実行し、グローバル設定とタスク設定の両方に同じ設定ファイルが使用されます。

## TiDB Lightning （グローバル） {#tidb-lightning-global}

### 稲妻 {#lightning}

#### <code>status-addr</code> {#code-status-addr-code}

-   Web インターフェースでタスクの進行状況を表示し、Prometheus メトリックを取得し、デバッグ データを公開し、インポート タスクを送信 (サーバーモード) するための HTTP ポート。
-   `0`に設定するとポートが無効になります。

<!-- Example: `:8289` -->

#### <code>server-mode</code> {#code-server-mode-code}

-   サーバーモードを設定します。
-   デフォルト値: `false`
-   値のオプション:
    -   `false` : コマンドを実行するとすぐにインポート タスクが開始されます。
    -   `true` : コマンド実行後、 TiDB LightningはWebインターフェースでインポートタスクを送信するまで待機します。詳細については、 [TiDB Lightning Webインターフェース](/tidb-lightning/tidb-lightning-web-interface.md)参照してください。

#### <code>level</code> {#code-level-code}

-   例: `"info"`

#### <code>file</code> {#code-file-code}

-   例: `"tidb-lightning.log"`

#### <code>max-size</code> {#code-max-size-code}

-   例: `128`<!-- MB -->

#### <code>max-days</code> {#code-max-days-code}

-   例: `28`

#### <code>max-backups</code> {#code-max-backups-code}

-   例: `14`

#### <code>enable-diagnose-logs</code> <span class="version-mark">v7.3.0 の新機能</span> {#code-enable-diagnose-logs-code-span-class-version-mark-new-in-v7-3-0-span}

-   診断ログを有効にするかどうかを制御します。
-   デフォルト値: `false`
-   値のオプション:
    -   `false` : インポートに関連するログのみが出力され、他の依存コンポーネントのログは出力されません。
    -   `true` : インポート プロセスとその他の依存コンポーネントの両方からのログが出力され、診断に使用できる GRPC デバッグが有効になります。

## TiDB Lightning （タスク） {#tidb-lightning-task}

### 稲妻 {#lightning}

#### <code>check-requirements</code> {#code-check-requirements-code}

-   タスクを開始する前にクラスターが最小要件を満たしているかどうかを確認し、実行中に TiKV に 10% を超える空き領域が残っているかどうかを確認します。

<!-- Example: `true` -->

#### <code>index-concurrency</code> {#code-index-concurrency-code}

-   同時に開くインデックスエンジンの最大数。各テーブルは、インデックスを格納する1つの「インデックスエンジン」と、行データを格納する複数の「データエンジン」に分割されます。1と`table-concurrency` `index-concurrency`は、各エンジンタイプの最大同時実行数を制御します。通常はデフォルト値を使用してください。

<!-- Example: `2` -->

#### <code>table-concurrency</code> {#code-table-concurrency-code}

-   同時に開くことができるデータエンジンの最大数です。各テーブルは、インデックスを格納する1つの「インデックスエンジン」と、行データを格納する複数の「データエンジン」に分割されます。1と`table-concurrency` `index-concurrency`は、各エンジンタイプの最大同時接続数を制御します。通常はデフォルト値を使用してください。

<!-- Example: `6` -->

#### <code>region-concurrency</code> {#code-region-concurrency-code}

-   データの同時実行数。他のコンポーネントと一緒にデプロイする場合、CPU使用率を制限するために、論理CPUコアサイズの75%に設定できます。
-   デフォルト値: 論理CPUコアの数

#### <code>io-concurrency</code> {#code-io-concurrency-code}

-   最大I/O同時実行数。I/O同時実行数が多すぎると、ディスクの内部バッファが頻繁に更新されるため、I/Oレイテンシーが増加し、キャッシュミスが発生し、読み取り速度が低下します。storageメディアによっては、最適なパフォーマンスを得るためにこの値を調整する必要があるかもしれません。

<!-- Example: `5` -->

#### <code>max-error</code> {#code-max-error-code}

-   TiDB Lightning を停止する前に許容される致命的ではないエラーの最大数。
-   致命的ではないエラーはいくつかの行に限定されており、それらの行を無視するとインポート プロセスを続行できます。
-   これを N に設定すると、(N+1) 番目のエラーが発生すると、 TiDB Lightning はできるだけ早く停止します。
-   スキップされた行は、ターゲット TiDB の`task info`スキーマ内のテーブルに挿入されます。
-   デフォルト値: `MaxInt64`バイト、つまり`9223372036854775807`バイト。

#### <code>task-info-schema-name</code> {#code-task-info-schema-name-code}

-   TiDB Lightning実行結果を保存するスキーマまたはデータベースの名前を指定します。
-   エラー記録を無効にするには、これを空の文字列に設定します。

<!-- Example: `'lightning_task_info'` -->

#### <code>meta-schema-name</code> {#code-meta-schema-name-code}

-   [並行輸入モード](/tidb-lightning/tidb-lightning-distributed-import.md)では、ターゲットクラスタ内の各TiDB Lightningインスタンスのメタ情報を格納するスキーマ名です。このパラメータは、並列インポートが有効な場合にのみ設定してください。
-   このパラメータに設定する値は、同じ並列インポートに参加する各TiDB Lightningインスタンスで同じである必要があります。そうでない場合、インポートされたデータの正確性は保証されません。
-   並列インポート モードが有効になっている場合は、インポートに使用されるユーザー (構成`tidb.user` ) に、この構成に対応するデータベースを作成してアクセスする権限があることを確認します。
-   TiDB Lightningはインポート完了後にこのスキーマを削除します。そのため、このパラメータを設定する際に既存のスキーマ名を使用しないでください。
-   デフォルト値: `"lightning_metadata"`

### 安全 {#security}

`security`セクションでは、クラスター内の TLS 接続の証明書とキーを指定します。

#### <code>ca-path</code> {#code-ca-path-code}

-   CAの公開証明書を指定します。TLSを無効にする場合は空白のままにしてください。

<!-- Example: `"/path/to/ca.pem"` -->

#### <code>cert-path</code> {#code-cert-path-code}

-   このサービスの公開証明書を指定します。

<!-- Example: `"/path/to/lightning.pem"` -->

#### <code>key-path</code> {#code-key-path-code}

-   このサービスの秘密鍵を指定します。

<!-- Example: `"/path/to/lightning.key"` -->

### チェックポイント {#checkpoint}

#### <code>enable</code> {#code-enable-code}

-   チェックポイントを有効にするかどうかを制御します。
-   データのインポート中に、 TiDB Lightning はどのテーブルがインポートされたかを記録するため、 TiDB Lightningまたは別のコンポーネントがクラッシュした場合でも、最初から再起動するのではなく、既知の正常な状態から開始できます。

<!-- Example: `true` -->

#### <code>schema</code> {#code-schema-code}

-   チェックポイントを保存するスキーマ名 (データベース名) を指定します。

<!-- Example: `"tidb_lightning_checkpoint"` -->

#### <code>driver</code> {#code-driver-code}

-   チェックポイントを保存する場所。
-   値のオプション:
    -   `"file"` : ローカルファイルとして保存します。
    -   `"mysql"` : リモートの MySQL 互換データベースに保存します。

#### <code>dsn</code> {#code-dsn-code}

-   チェックポイントstorageの場所を示すデータ ソース名 (DSN)。
-   `file`ドライバの場合、DSNはパスです。パスが指定されていない場合、 TiDB Lightningはデフォルト値の`/tmp/CHECKPOINT_SCHEMA.pb`使用します。
-   `mysql`ドライバーの場合、 DSN は`USER:PASS@tcp(HOST:PORT)/`形式の URL です。
-   URL が指定されていない場合は、 `[tidb]`セクションの TiDBサーバーがチェックポイントの保存に使用されます。
-   ターゲット TiDB クラスターの負荷を軽減するには、別の MySQL 互換データベースサーバーを指定することをお勧めします。

<!-- Example: `"/tmp/tidb_lightning_checkpoint.pb"` -->

#### <code>keep-after-success</code> {#code-keep-after-success-code}

-   すべてのデータのインポート後もチェックポイントを保持するかどうかを制御します。1 `false`場合、チェックポイントは削除されます。
-   チェックポイントを保持するとデバッグが容易になりますが、データ ソースに関するメタデータが漏洩します。

<!-- Example: `false` -->

### 対立 {#conflict}

#### <code>strategy</code> {#code-strategy-code}

-   v7.3.0以降、競合データを処理するための新しい戦略が導入されました。v8.0.0以降、 TiDB Lightningは物理インポートモードと論理インポートモードの両方で競合戦略を最適化します。
-   デフォルト値: `""`
-   値のオプション:
    -   `""` :
        -   物理インポートモードでは、 TiDB Lightning は競合するデータを検出または処理しません。ソースファイルに競合する主キーまたは一意キーのレコードが含まれている場合、後続のステップでエラーが報告されます。
        -   論理インポート モードでは、 TiDB Lightning は処理のために`""`戦略を`"error"`戦略に変換します。
    -   `"error"` : インポートされたデータ内で競合する主キー レコードまたは一意のキー レコードが検出されると、 TiDB Lightning はインポートを終了し、エラーを報告します。
    -   `"replace"` : 競合する主キー レコードまたは一意のキー レコードが発生した場合、 TiDB Lightning は最新のデータを保持し、古いデータを上書きします。
        -   物理インポート モードを使用すると、競合するデータはターゲット TiDB クラスターの`lightning_task_info.conflict_view`ビューに記録されます。
        -   `lightning_task_info.conflict_view`ビューにおいて、行の`is_precheck_conflict`フィールドが`0`場合、その行に記録された競合データは後処理の競合検出によって検出されたことを意味します。行の`is_precheck_conflict`フィールドが`1`の場合、その行に記録された競合データはインポート前の競合検出によって検出されたことを意味します。アプリケーション要件に基づいて、適切なレコードをターゲットテーブルに手動で挿入できます。
        -   ターゲット TiKV は v5.2.0 以降のバージョンである必要があることに注意してください。
    -   `"ignore"` : 主キーまたは一意キーのレコードの競合が発生した場合、 TiDB Lightning は古いデータを保持し、新しいデータを無視します。このオプションは論理インポートモードでのみ使用できます。

#### <code>precheck-conflict-before-import</code> {#code-precheck-conflict-before-import-code}

-   インポート前の競合検出を有効にするかどうかを制御します。これは、TiDBにインポートする前にデータの競合をチェックします。このパラメータは、物理インポートモードでのみ使用できます。
-   競合レコードの数が 1,000,000 を超えるシナリオでは、競合検出のパフォーマンスを向上させるために`precheck-conflict-before-import = true`設定することをお勧めします。
-   その他のシナリオでは、無効にすることをお勧めします。
-   デフォルト値: `false`
-   値のオプション:
    -   `false` : TiDB Lightning はインポート後にのみ競合をチェックします。
    -   `true` : TiDB Lightning はインポートの前後の両方で競合をチェックします。

#### <code>threshold</code> {#code-threshold-code}

-   [`strategy`](#strategy)が`"replace"`または`"ignore"`の場合に処理できる競合エラーの最大数を制御します。7 `strategy` `"replace"`または`"ignore"`場合のみ設定できます。
-   `10000`より大きい値を設定すると、インポート プロセスのパフォーマンスが低下する可能性があります。
-   デフォルト値: `10000`

#### <code>max-record-rows</code> {#code-max-record-rows-code}

-   `conflict_records`テーブル内のレコードの最大数を制御します。
-   v8.1.0 以降では、ユーザー入力に関係なく、 TiDB Lightning が`max-record-rows`の値に[`threshold`](#threshold)の値を自動的に割り当てるため、 `max-record-rows`手動で構成する必要はありません。
-   `max-record-rows`将来のリリースでは非推奨になります。
-   物理インポートモードでは、戦略が`"replace"`場合、上書きされる競合レコードが記録されます。
-   論理インポート モードでは、戦略が`"ignore"`場合、無視される競合レコードが記録され、戦略が`"replace"`場合、競合レコードは記録されません。
-   デフォルト値: `10000`

### tikvインポーター {#tikv-importer}

#### <code>backend</code> {#code-backend-code}

-   TiDB Lightningのインポート モードを指定します。
-   デフォルト値: `"local"`
-   値のオプション:
    -   `"local"` : [物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md) （デフォルト）です。これは、例えば1 TiBを超えるような大規模なデータセットのインポートに適用されます。ただし、インポート中は下流のTiDBはサービスを提供できません。
    -   `"tidb"` : [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md) 。このモードは、例えば1 TiB未満の小さなデータセットのインポートに使用できます。インポート中は、下流のTiDBがサービスを提供できます。

#### <code>parallel-import</code> {#code-parallel-import-code}

-   複数のTiDB Lightningインスタンス（物理インポートモード）が1つ以上のターゲットテーブル[並行して](/tidb-lightning/tidb-lightning-distributed-import.md)にデータをインポートできるようにするかどうかを制御します。このパラメータは、ターゲットテーブルが空の場合にのみ使用されることに注意してください。
-   デフォルト値: `false`
-   値`false`オプション: `true`
-   並列インポート モードを使用する場合は、パラメータを`true`に設定する必要がありますが、ターゲット テーブルにデータが存在しないことが前提となります。つまり、すべてのデータはTiDB Lightningによってのみインポートできます。

#### <code>duplicate-resolution</code> {#code-duplicate-resolution-code}

> **警告：**
>
> バージョン8.0.0以降、 `duplicate-resolution`パラメータは非推奨となり、将来のリリースで削除される予定です。詳細については、 [競合検出の旧バージョン](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800)参照してください。

-   物理インポート モードで重複レコード (一意キーの競合) を検出して解決するかどうかを制御します。
-   デフォルト値: `'none'`
-   値のオプション:
    -   `'none'` : 重複レコードを検出しません。データソースに重複レコードがある場合、ターゲットTiDBでデータの不整合が発生する可能性があります。2 `duplicate-resolution = 'none'`設定し、 `conflict.strategy`設定していない場合、 TiDB Lightningは自動的に`""`から`conflict.strategy`割り当てます。
    -   `'remove'` : `duplicate-resolution = 'remove'`設定し、 `conflict.strategy`設定しない場合、 TiDB Lightning は自動的に`conflict.strategy`に「置換」を割り当て、新しいバージョンの競合検出を有効にします。

#### <code>send-kv-pairs</code> {#code-send-kv-pairs-code}

> **警告：**
>
> バージョン7.2.0以降、このパラメータは非推奨となり、設定後は無効になります。1回のリクエストでTiKVに送信されるデータ量を調整したい場合は、代わりに[`send-kv-size`](#send-kv-size-new-in-v720)パラメータを使用してください。

-   物理インポート モードで TiKV にデータを送信するときに、1 つの要求内の KV ペアの最大数を指定します。

<!-- Example: 32768 -->

#### <code>send-kv-size</code> <span class="version-mark">v7.2.0 の新機能</span> {#code-send-kv-size-code-span-class-version-mark-new-in-v7-2-0-span}

-   物理インポート モードで TiKV にデータを送信するときの 1 つのリクエストの最大サイズを指定します。
-   デフォルト値: `"16K"`

#### <code>compress-kv-pairs</code> {#code-compress-kv-pairs-code}

-   物理インポート モードで KV ペアを TiKV に送信するときに圧縮を有効にするかどうかを制御します。
-   現在、Gzip圧縮アルゴリズムのみがサポートされています。このアルゴリズムを使用するには、このパラメータに`"gzip"`または`"gz"`を入力してください。
-   デフォルト値: `""` 。圧縮が有効になっていないことを意味します。
-   `"gz"` `"gzip"`オプション: `""`

#### <code>sorted-kv-dir</code> {#code-sorted-kv-dir-code}

-   物理インポートモードにおけるローカルKVソートのディレクトリを指定します。ディスクパフォ​​ーマンスが低い場合（HDDなど）は、インポート速度を向上させるために、 `data-source-dir`とは異なるディスク上のディレクトリを設定することをお勧めします。

#### <code>range-concurrency</code> {#code-range-concurrency-code}

-   TiKV が物理インポート モードで KV データを書き込む同時実行性を指​​定します。
-   TiDB Lightningと TiKV 間のネットワーク伝送速度が 10 ギガビットを超える場合は、この値を適宜増やすことができます。
-   デフォルト値: `16`

#### <code>store-write-bwlimit</code> {#code-store-write-bwlimit-code}

-   物理インポート モードでTiDB Lightning が各 TiKV ノードにデータを書き込む帯域幅を制限します。
-   デフォルト値: `0` 、制限がないことを意味します。

#### <code>disk-quota</code> {#code-disk-quota-code}

-   物理インポート モードを使用する場合のローカル一時ファイルのディスク クォータを指定します。
-   ディスククォータが不足している場合、 TiDB Lightningはソースデータの読み取りと一時ファイルの書き込みを停止しますが、ソート済みのキーと値のペアをTiKVに書き込むことを優先します。TiDB TiDB Lightningがローカルの一時ファイルを削除した後、インポートプロセスは続行されます。
-   このオプションは、 [`backend`](#backend)オプションを`local`に設定した場合にのみ有効になります。
-   デフォルト値: `MaxInt64`バイト、つまり 9223372036854775807 バイト。

#### <code>add-index-by-sql</code> {#code-add-index-by-sql-code}

-   物理インポート モードで SQL 経由でインデックスを追加するかどうかを指定します。
-   このメカニズムは、過去のバージョンと一貫性があります。SQLを使用してインデックスを追加する利点は、データのインポートとインデックスのインポートを個別に実行できるため、データのインポートが高速化されることです。データのインポート後、インデックスの追加に失敗しても、インポートされたデータの整合性には影響しません。
-   デフォルト値: `false`
-   値のオプション:
    -   `false` : TiDB Lightningデータとインデックス データの両方を KV ペアにエンコードし、一緒に TiKV にインポートします。
    -   `true` : TiDB Lightning は、行データをインポートした後、 `ADD INDEX` SQL ステートメントを介してインデックスを追加します。

#### <code>keyspace-name</code> {#code-keyspace-name-code}

-   TiDB Lightningを使用してマルチテナント TiDB クラスターをインポートする場合は、このパラメータを使用して対応するキースペース名を指定します。
-   デフォルト値: `""` 。これは、 TiDB Lightning がデータをインポートするために、対応するテナントのキー スペース名を自動的に取得することを意味します。
-   値を指定すると、指定されたキースペース名がデータのインポートに使用されます。

#### <code>pause-pd-scheduler-scope</code><span class="version-mark">バージョン7.1.0の新機能</span> {#code-pause-pd-scheduler-scope-code-span-class-version-mark-new-in-v7-1-0-span}

-   物理インポート モードでは、このパラメータはTiDB Lightning がPD スケジュールを停止する範囲を制御します。
-   デフォルト値: `"table"`
-   値のオプション:
    -   `"table"` : ターゲット テーブル データを格納するリージョンのみのスケジュールを一時停止します。
    -   `"global"` : グローバルスケジューリングを一時停止します。ビジネストラフィックのないクラスターにデータをインポートする場合は、他のスケジューリングからの干渉を避けるため、このパラメータを`"global"`に設定することをお勧めします。

#### <code>region-split-batch-size</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-region-split-batch-size-code-span-class-version-mark-new-in-v7-1-0-span}

-   物理インポート モードでは、このパラメータはバッチで領域を分割するときの領域の数を制御します。
-   TiDB Lightningインスタンスごとに同時に分割できるリージョンの最大数は次のとおりです: `region-split-batch-size * region-split-concurrency * table-concurrency`
-   デフォルト値: `4096`

#### <code>region-split-concurrency</code> <span class="version-mark">v7.1.0 の新機能</span> {#code-region-split-concurrency-code-span-class-version-mark-new-in-v7-1-0-span}

-   物理インポート モードでは、このパラメーターはリージョンを分割する際の同時実行性を制御します。
-   デフォルト値: CPUコアの数

#### <code>region-check-backoff-limit</code><span class="version-mark">バージョン7.1.0の新機能</span> {#code-region-check-backoff-limit-code-span-class-version-mark-new-in-v7-1-0-span}

-   物理インポート モードでは、このパラメータは、分割および分散操作後にリージョンがオンラインになるまで待機する再試行回数を制御します。
-   再試行間隔は最大2秒です。再試行の間にいずれかのリージョンがオンラインになった場合でも、再試行回数は増加しません。
-   デフォルト値: `1800`

#### <code>block-size</code> <span class="version-mark">v7.6.0 の新機能</span> {#code-block-size-code-span-class-version-mark-new-in-v7-6-0-span}

-   物理インポートモードでは、このパラメータはローカルファイルのソートに使用するI/Oブロックサイズを制御します。ディスクIOPSがボトルネックになっている場合は、この値を増やすことでデータインポートのパフォーマンスを向上させることができます。
-   値は`1B`以上である必要があります。数値のみ（例： `16` ）を指定した場合、単位は KiB ではなくバイトになります。
-   デフォルト値: `"16KiB"`

#### <code>logical-import-batch-size</code> <span class="version-mark">v8.0.0 の新機能</span> {#code-logical-import-batch-size-code-span-class-version-mark-new-in-v8-0-0-span}

-   論理インポート モードでは、このパラメータはダウンストリーム TiDBサーバーで実行される各 SQL ステートメントのサイズを制御します。
-   単一のトランザクション内の`INSERT`または`REPLACE`ステートメントの`VALUES`部分の予想サイズを指定します。
-   このパラメータは厳密な制限ではありません。実際に実行されるSQLは、インポートされるコンテンツに応じて、これより長くなったり短くなったりする場合があります。
-   デフォルト値: `"96KiB"` 。これは、 TiDB Lightning がクラスターの唯一のクライアントである場合に、インポート速度が最適化されます。
-   TiDB Lightningの実装上の理由により、この値は96 KiBに制限されています。これより大きな値を設定しても効果はありません。この値を下げることで、大規模なトランザクションによるクラスターへの負荷を軽減できます。

#### <code>logical-import-batch-rows</code> <span class="version-mark">v8.0.0 の新機能</span> {#code-logical-import-batch-rows-code-span-class-version-mark-new-in-v8-0-0-span}

-   論理インポート モードでは、このパラメータはトランザクションごとに挿入される行の最大数を制御します。
-   [`logical-import-batch-size`](#logical-import-batch-size-new-in-v800)と`logical-import-batch-rows`両方を指定した場合、最初にしきい値に達したパラメータが有効になります。
-   この値を減らすと、大規模なトランザクションによるクラスターのストレスを軽減できます。
-   デフォルト値: `65536`

#### <code>logical-import-prep-stmt</code> {#code-logical-import-prep-stmt-code}

-   論理インポート モードでは、このパラメータは、パフォーマンスを向上させるために[準備された文](/sql-statements/sql-statement-prepare.md)およびステートメント キャッシュを使用するかどうかを制御します。
-   デフォルト値: `false`

### マイダンパー {#mydumper}

#### <code>read-block-size</code> {#code-read-block-size-code}

-   ファイル読み取り時のブロックサイズを指定します。データソースの最長文字列よりも長く設定してください。
-   デフォルト値: `"64KiB"`

#### <code>batch-import-ratio</code> {#code-batch-import-ratio-code}

-   エンジンファイルは順番にインポートする必要があります。並列処理のため、複数のデータエンジンがほぼ同時にインポートされ、キューが生成されてリソースが浪費されます。そのため、 TiDB Lightning、リソースを適切に配分するために、最初の数バッチのサイズをわずかに大きくしています。
-   スケールアップ係数はこのパラメータによって制御されます。このパラメータは、完全な同時実行における「インポート」ステップと「書き込み」ステップの所要時間の比率を表します。これは、約1GiBの単一テーブルにおける比率（インポート所要時間/書き込み所要時間）を使用して計算できます。正確な時間はログで確認できます。
-   「インポート」の方が高速であれば、バッチ サイズの分散は小さくなり、比率が 0 であればバッチ サイズは均一になります。
-   範囲: `[0, 1)`

<!-- Example: `0.75` -->

#### <code>data-source-dir</code> {#code-data-source-dir-code}

-   ローカルソースデータディレクトリまたは外部storageのURIを指定します。外部storageのURIの詳細については、 [URI形式](/br/backup-and-restore-storages.md#uri-format)参照してください。

<!-- Example: `"/data/my_database"` -->

#### <code>character-set</code> {#code-character-set-code}

-   `CREATE TABLE`ステートメントを含むスキーマ ファイルの文字セットを指定します。
-   デフォルト値: `"auto"`
-   値のオプション:
    -   `"auto"` : スキーマがUTF-8かGB-18030かを自動的に検出します。エンコードがどちらでもない場合はエラーが報告されます。
    -   `"utf8mb4"` : スキーマ ファイルは UTF-8 としてエンコードする必要があります。それ以外の場合はエラーが報告されます。
    -   `"gb18030"` : スキーマファイルは GB-18030 としてエンコードされている必要があります。そうでない場合はエラーが報告されます。
    -   `"latin1"` : スキーマ ファイルは、コード ページ 1252 とも呼ばれる MySQL latin1 エンコードを使用します。
    -   `"binary"` : スキーマファイルのデコードを試みない

#### <code>data-character-set</code> {#code-data-character-set-code}

-   ソースデータファイルの文字セットを指定します。TiDB TiDB Lightning は、インポート時にソースファイルを指定された文字セットから UTF-8 エンコードに変換します。
-   現在、この設定ではCSVファイルの文字セットのみを指定し、以下のオプションがサポートされています。空白のままにすると、デフォルト値の`"binary"`が使用され、Lightningはエンコーディングを変換しません。
-   TiDB Lightning はソース データ ファイルの文字セットを予測せず、この構成に基づいてソース ファイルを変換し、データをインポートするだけです。
-   この構成の値がソース データ ファイルの実際のエンコードと同じでない場合、インポートの失敗、データの損失、またはデータの乱れが発生する可能性があります。
-   デフォルト値: `"binary"`
-   値のオプション:
    -   `"binary"` : TiDB Lightning がエンコーディングを変換しないことを示します (デフォルト)。
    -   `"utf8mb4"` : ソース データ ファイルが UTF-8 エンコードを使用していることを示します。
    -   `"GB18030"` : ソース データ ファイルで GB-18030 エンコードが使用されていることを示します。
    -   `"GBK"` : ソース データ ファイルは GBK エンコードを使用します (GBK エンコードは GB-2312 文字セットの拡張であり、コード ページ 936 とも呼ばれます)。
    -   `"latin1"` : ソース データ ファイルは、コード ページ 1252 とも呼ばれる MySQL latin1 エンコードを使用します。

#### <code>data-invalid-char-replace</code> {#code-data-invalid-char-replace-code}

-   ソース データ ファイルの文字セット変換中に互換性のない文字があった場合に置換する文字を指定します。
-   この設定は、フィールドセパレーター、引用符定義子、改行と重複してはいけません。デフォルト値を変更すると、ソースデータファイルの解析パフォーマンスが低下する可能性があります。
-   デフォルト値: `"\uFFFD"` 。これは、UTF-8 エンコードにおける「エラー」の Rune または Unicode 置換文字です。

#### <code>strict-format</code> {#code-strict-format-code}

-   処理速度を上げるには、入力データを[厳格な形式](/tidb-lightning/tidb-lightning-data-source.md#strict-format)で指定します。デフォルト値は、速度ではなく安全性を優先した`false`です。
-   デフォルト値: `false`
-   値`false`オプション: `true`
-   `strict-format = true`次のことが求められます:
    -   CSV では、引用符で囲まれている場合でも、すべての値にリテラルの改行 ( `U+000A`と`U+000D` 、または`\r`と`\n` ) を含めることはできません。つまり、改行は行を区切るために厳密に使用されます。
    -   厳密なフォーマットにより、 TiDB Lightningは並列処理において大きなファイルの分割位置を迅速に特定できます。ただし、入力データが「厳密」でない場合、有効なデータが半分に分割され、結果が破損する可能性があります。

#### <code>max-region-size</code> {#code-max-region-size-code}

-   [`strict-format`](#strict-format)が`true`の場合、 TiDB Lightning は大きな CSV ファイルを複数のチャンクに分割して並列処理します。5 `max-region-size`分割後の各チャンクの最大サイズです。
-   デフォルト値: `"256MiB"`

#### <code>filter</code> {#code-filter-code}

-   これらのワイルドカード ルールに一致するテーブルのみをインポートします。

<!-- Example: `['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']` -->

### マイダンパー.csv {#mydumper-csv}

CSV ファイルの解析方法を構成します。

#### <code>separator</code> {#code-separator-code}

-   フィールド間の区切り文字を指定します。1文字以上の文字をサポートします。
-   デフォルト値: `','`

#### <code>delimiter</code> {#code-delimiter-code}

-   引用符の区切り文字を指定します。値が空の場合、引用符は使用されません。
-   デフォルト値: `'"'`

#### <code>terminator</code> {#code-terminator-code}

-   行末記号を指定します。
-   デフォルト値: `""` 。これは、 `"\n"` (LF) と`"\r\n"` (CRLF) の両方が行末文字であることを意味します。

#### <code>header</code> {#code-header-code}

-   CSV ファイルにヘッダーが含まれているかどうかを制御します。
-   値のオプション:
    -   `true` : TiDB Lightning は最初の行をテーブル ヘッダーとして扱い、データとしてインポートしません。
    -   `false` : 最初の行も CSV データとしてインポートされます。

#### <code>header-schema-match</code> {#code-header-schema-match-code}

-   CSV ファイル ヘッダー内の列名が、ターゲット テーブルで定義されている列名と一致するかどうかを制御します。
-   デフォルト値は`true`です。これは、CSV ヘッダーの列名がターゲット テーブルの列名と一致していることが確認されたことを意味します。そのため、2 つの列の順序が異なっていても、 TiDB Lightning は列名をマッピングすることでデータを正常にインポートできます。
-   CSVテーブルヘッダーとターゲットテーブルの列名が一致しない（例えば、CSVテーブルヘッダーの一部の列名がターゲットテーブルに見つからない）ものの、列の順序が同じ場合は、この設定を`false`に設定してください。この場合、 TiDB Lightningはエラーを回避するためにCSVヘッダーを無視し、ターゲットテーブルの列の順序でデータを直接インポートします。したがって、列の順序が同じでない場合は、インポート前にCSVファイル内の列の順序をターゲットテーブルの順序と一致するように手動で調整する必要があります。そうしないと、データの不一致が発生する可能性があります。
-   デフォルト値: `true`
-   値`false`オプション: `true`

> **注記：**
>
> このパラメータは、 `header`パラメータが`true`に設定されている場合にのみ適用されます。 `header` `false`に設定されている場合は、CSVファイルにヘッダーが含まれていないため、このパラメータは適用されません。

#### <code>not-null</code> {#code-not-null-code}

-   CSV に NULL 値が含まれているかどうかを制御します。
-   値のオプション:
    -   `true` : CSV のすべての列を NULL にすることはできません。
    -   `false` : CSV には NULL 値を含めることができます。

#### <code>null</code> {#code-null-code}

-   `not-null`が`false`の場合 (つまり、CSV に NULL を含めることができる場合)、この値に等しいフィールドは NULL として扱われます。

<!-- Example: `'\N'` -->

#### <code>backslash-escape</code> {#code-backslash-escape-code}

-   フィールド内のバックスラッシュエスケープを解釈するかどうかを制御します。

<!-- Example: `true` -->

#### <code>trim-last-separator</code> {#code-trim-last-separator-code}

-   行がセパレーターで終わる場合にそれを削除するかどうかを制御します。

<!-- Example: `false` -->

### mydumper.files {#mydumper-files}

#### <code>pattern</code> {#code-pattern-code}

-   AWS Aurora parquet ファイルを解析するために使用される式。
-   例: `'(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'`

#### <code>schema</code> {#code-schema-code}

-   例: `'$1'`

#### <code>table</code> {#code-table-code}

-   例: `'$2'`

#### <code>type</code> {#code-type-code}

-   例: `'$3'`

### ティッド {#tidb}

#### <code>host</code> {#code-host-code}

-   クラスターからの任意の TiDBサーバーのコンフィグレーション。

<!-- Example: `"172.16.31.1"` -->

#### <code>port</code> {#code-port-code}

-   例: `4000`

#### <code>user</code> {#code-user-code}

-   例: `"root"`

#### <code>password</code> {#code-password-code}

-   TiDBに接続するためのパスワードを設定します。パスワードはプレーンテキストまたはBase64エンコードのいずれかで使用できます。

#### <code>status-port</code> {#code-status-port-code}

-   TiDB からテーブル スキーマ情報を取得します。

<!-- Example: `10080` -->

#### <code>pd-addr</code> {#code-pd-addr-code}

-   クラスター内の任意のPDサーバーのアドレスを指定します。v7.6.0以降、TiDBは複数のPDアドレスの設定をサポートします。

<!-- Example: `"172.16.31.4:2379,56.78.90.12:3456"` -->

#### <code>log-level</code> {#code-log-level-code}

-   TiDB ライブラリのログレベルを制御します。TiDB TiDB Lightning はTiDB をライブラリとしてインポートし、いくつかのログを自ら生成します。

<!-- Example: `"error"` -->

#### <code>build-stats-concurrency</code> {#code-build-stats-concurrency-code}

-   チェックサムおよび分析処理を高速化するために、TiDBセッション変数を設定します。詳細については、 [`ANALYZE`同時実行を制御する](/statistics.md#control-analyze-concurrency)参照してください。

<!-- Example: `20` -->

#### <code>distsql-scan-concurrency</code> {#code-distsql-scan-concurrency-code}

-   チェックサムおよび分析処理を高速化するために、TiDBセッション変数を設定します。詳細については、 [`ANALYZE`同時実行を制御する](/statistics.md#control-analyze-concurrency)参照してください。
-   [`checksum-via-sql`](#checksum-via-sql) `"true"`に設定した場合、 TiDB Lightning は`ADMIN CHECKSUM TABLE <table>` SQL 文を実行して TiDB のチェックサム演算を実行します。この場合、以下のパラメータ`distsql-scan-concurrency`と`checksum-table-concurrency`無効になります。

<!-- Example: `15` -->

#### <code>index-serial-scan-concurrency</code> {#code-index-serial-scan-concurrency-code}

-   チェックサムおよび分析処理を高速化するために、TiDBセッション変数を設定します。詳細については、 [`ANALYZE`同時実行を制御する](/statistics.md#control-analyze-concurrency)参照してください。

<!-- Example: `20` -->

#### <code>checksum-table-concurrency</code> {#code-checksum-table-concurrency-code}

-   チェックサムと`ANALYZE`操作を高速化するために、TiDBセッション変数を設定します。詳細については、 [`ANALYZE`同時実行を制御する](/statistics.md#control-analyze-concurrency)参照してください。
-   [`checksum-via-sql`](#checksum-via-sql) `"true"`に設定した場合、 TiDB Lightning は`ADMIN CHECKSUM TABLE <table>` SQL 文を実行して TiDB のチェックサム演算を実行します。この場合、以下のパラメータ`distsql-scan-concurrency`と`checksum-table-concurrency`無効になります。

<!-- Example: `2` -->

#### <code>sql-mode</code> {#code-sql-mode-code}

-   SQL ステートメントを解析および実行するために使用するデフォルトの SQL モードを指定します。

<!-- Example: `"ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER"` -->

#### <code>max-allowed-packet</code> {#code-max-allowed-packet-code}

-   SQL 接続に許可される最大パケット サイズを設定します。
-   これを`0`に設定すると、接続ごとにサーバーから`max_allowed_packet`変数が自動的に取得されます。

<!-- Example: `67_108_864` -->

#### <code>tls</code> {#code-tls-code}

-   SQL 接続に TLS を使用するかどうかを制御します。
-   値のオプション:
    -   `""` : [`[tidb.security]`](#tidbsecurity)セクションが設定されている場合、TLS を強制します（「cluster」と同じ）。それ以外の場合は`"false"`と同じです。
    -   `"false"` : TLS を無効にします。
    -   `"cluster"` : TLS を強制し、 [`[tidb.security]`](#tidbsecurity)セクションで指定された CA を使用してサーバーの証明書を検証します。
    -   `"skip-verify"` : TLSを強制しますが、サーバーの証明書を検証しません。この設定は安全ではないことに注意してください。
    -   `"preferred"` : `"skip-verify"`と同じですが、サーバーがTLS をサポートしていない場合は、暗号化されていない接続にフォールバックします。

### tidb.セキュリティ {#tidb-security}

-   TLS 対応の MySQL 接続の証明書とキーを指定します。
-   デフォルト値: [`security`](#security)セクションのコピー。

#### <code>ca-path</code> {#code-ca-path-code}

-   CA の公開証明書を指定します。SQL の TLS を無効にする場合は、空の文字列に設定します。

<!-- Example: `"/path/to/ca.pem"` -->

#### <code>cert-path</code> {#code-cert-path-code}

-   このサービスの公開証明書を指定します。
-   デフォルト値: [`security.cert-path`](#cert-path)のコピー。

<!-- Example: `"/path/to/lightning.pem"` -->

#### <code>key-path</code> {#code-key-path-code}

-   このサービスの秘密鍵を指定します。
-   デフォルト値: [`security.key-path`](#key-path)のコピー。

<!-- Example: `"/path/to/lightning.key"` -->

### tidb.セッション変数 {#tidb-session-vars}

その他の TiDB セッション変数を指定します。

<!-- tidb_enable_clustered_index = "OFF" -->

### 復元後 {#post-restore}

-   物理インポート モードでは、データのインポートが完了すると、 TiDB Lightning はチェックサムと`ANALYZE`操作を自動的に実行できます。
-   実本番環境ではこれらを true のままにしておくことをお勧めします。
-   実行順序: チェックサム -&gt; `ANALYZE` 。
-   論理インポート モードでは、チェックサムと`ANALYZE`操作は必要なく、実際の操作では常にスキップされることに注意してください。

#### <code>checksum</code> {#code-checksum-code}

-   インポート後にデータの整合性を検証するために、テーブルごとに`ADMIN CHECKSUM TABLE <table>`を実行するかどうかを指定します。
-   デフォルト値: `"required"` 。v4.0.8 以降では、デフォルト値が`"true"`から`"required"`に変更されます。
-   値のオプション:
    -   `"required"` : 管理者チェックサムを実行します。チェックサムが失敗した場合、 TiDB Lightning は失敗して終了します。
    -   `"optional"` : 管理者チェックサムを実行します。チェックサムに失敗した場合、 TiDB Lightning はWARN ログを報告しますが、エラーは無視されます。
    -   `"off"` : チェックサムを実行しません。
-   チェックサムの失敗は通常、インポート例外（データの損失または不整合）を意味します。チェックサムは常に有効にすることをお勧めします。
-   下位互換性のため、このフィールドでは bool 値`true`と`false`も許可されます。5 `true` `required`に相当し、 `false` `off`に相当します。

#### <code>checksum-via-sql</code> {#code-checksum-via-sql-code}

-   `ADMIN CHECKSUM TABLE <table>`操作が TiDB 経由で実行されるかどうかを指定します。
-   デフォルト値: `"false"`
-   値のオプション:
    -   `"false"` : `ADMIN CHECKSUM TABLE <table>`コマンドは、 TiDB Lightning経由で実行するために TiKV に送信されます。
    -   `"true"` : この値が`"true"`場合に同時実行性を調整するには、TiDB で[`tidb_checksum_table_concurrency`](/system-variables.md#tidb_checksum_table_concurrency)変数を設定する必要があります。
-   チェックサムが失敗した場合に問題を特定しやすくするために、この値を`"true"`に設定することをお勧めします。

#### <code>analyze</code> {#code-analyze-code}

-   チェックサムが完了した後に各テーブルに対して`ANALYZE TABLE <table>`実行するかどうかを指定します。
-   デフォルト値: `"optional"`
-   `"off"` `"optional"`オプション: `"required"`

### クローン {#cron}

-   バックグラウンドでの定期的なアクションを設定します。
-   サポートされる単位: h (時間)、m (分)、s (秒)。

#### <code>switch-mode</code> {#code-switch-mode-code}

-   TiDB Lightningがインポートモードのステータスを自動的に更新する間隔を指定します。対応するTiKV設定よりも短くする必要があります。

<!-- Example: `"5m"` -->

#### <code>log-progress</code> {#code-log-progress-code}

-   インポートの進行状況をログに出力する間隔を指定します。

<!-- Example: `"5m"` -->

#### <code>check-disk-quota</code> {#code-check-disk-quota-code}

-   物理インポート モードを使用するときに、ローカル ディスク クォータをチェックする時間間隔を指定します。
-   デフォルト値: `"60s"` 、これは 60 秒を意味します。
