---
title: IMPORT INTO vs. TiDB Lightning
summary: IMPORT INTO` とTiDB Lightningの違いについて学びます。
---

# IMPORT INTO とTiDB Lightningの比較 {#import-into-vs-tidb-lightning}

多くのユーザーから、 [TiDB Lightning](/tidb-lightning/tidb-lightning-configuration.md)の展開、構成、およびメンテナンスは、特に[並行輸入](/tidb-lightning/tidb-lightning-distributed-import.md)の大規模なデータセットが関係するシナリオでは複雑であるというフィードバックが寄せられています。

フィードバックに基づいて、TiDB はTiDB Lightningの一部の機能を[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) SQL ステートメントに徐々に統合してきました。 `IMPORT INTO`実行することでデータを直接インポートできるため、データ インポートの効率が向上します。 さらに、 `IMPORT INTO`では、自動分散タスク スケジューリングや[TiDB グローバルソート](/tidb-global-sort.md)など、 TiDB Lightningにはない一部の機能がサポートされています。

`IMPORT INTO` v7.2.0 で導入され、v7.5.0 で一般提供 (GA) されます。今後のバージョンでも引き続き改善および最適化されます。2 `IMPORT INTO`機能がTiDB Lightning を完全に置き換えることができるようになったら、 TiDB Lightning は廃止されます。その時点で、関連する通知が TiDB リリース ノートおよびドキュメントで事前に提供されます。

## <code>IMPORT INTO</code>とTiDB Lightningの比較 {#comparison-between-code-import-into-code-and-tidb-lightning}

次のセクションでは、 `IMPORT INTO`とTiDB Lightningの違いをさまざまな側面から説明します。

### 導入コスト {#deployment-cost}

#### <code>IMPORT INTO</code> {#code-import-into-code}

`IMPORT INTO`では、個別のデプロイメントは必要ありません。TiDB ノード上で直接実行できるため、追加のデプロイメント作業が不要になります。

#### TiDB Lightning {#tidb-lightning}

対照的に、 TiDB Lightning[個別のサーバー展開](/tidb-lightning/deploy-tidb-lightning.md)必要です。

### リソースの活用 {#resource-utilization}

#### <code>IMPORT INTO</code> {#code-import-into-code}

`IMPORT INTO`タスクと他のビジネス ワークロードは、TiDB リソースを共有したり、異なるタイミングで使用したりして、TiDB リソースを最大限に活用できます。3 `IMPORT INTO`のパフォーマンスと安定性を維持しながら、ビジネス ワークロードの安定した運用を確保するために、データ インポート用に`IMPORT INTO`専用の[特定のTiDBノード](/system-variables.md#tidb_service_scope-new-in-v740)指定できます。

[TiDB グローバルソート](/tidb-global-sort.md)使用する場合、大きなローカルディスクをマウントする必要はありません。TiDB Global Sort は Amazon S3 をstorageとして使用できます。インポートタスクが完了すると、グローバルソート用に Amazon S3 に保存された一時データは自動的に削除され、storageコストを節約します。

#### TiDB Lightning {#tidb-lightning}

TiDB Lightningを展開して実行するには、別のサーバーが必要です。インポート タスクが実行されない場合、これらのリソースはアイドル状態のままになります。インポート タスクが定期的に実行されるシナリオでは、合計アイドル時間はさらに長くなり、リソースの無駄になります。

インポートするデータセットが大きい場合は、インポートするデータをソートするための大容量のローカルディスクも準備する必要があります。

### タスクの構成と統合 {#task-configuration-and-integration}

#### <code>IMPORT INTO</code> {#code-import-into-code}

インポート タスクを送信する SQL ステートメントを直接記述することができ、簡単に呼び出して統合できます。

#### TiDB Lightning {#tidb-lightning}

対照的に、 TiDB Lightning[タスク設定ファイル](/tidb-lightning/tidb-lightning-configuration.md)記述する必要があります。これらの構成ファイルは複雑であり、サードパーティが簡単に呼び出すことはできません。

### タスクのスケジュール {#task-scheduling}

#### <code>IMPORT INTO</code> {#code-import-into-code}

`IMPORT INTO`分散実行をサポートします。たとえば、40 TiB のソース データ ファイルを 1 つのターゲット テーブルにインポートする場合、SQL ステートメントを送信した後、TiDB はインポート タスクを複数のサブタスクに自動的に分割し、異なる TiDB ノードがこれらのサブタスクを実行するようにスケジュールします。

#### TiDB Lightning {#tidb-lightning}

対照的に、 TiDB Lightningの構成は複雑で非効率であり、エラーが発生しやすくなります。

10 個のTiDB Lightningインスタンスを起動してデータを並行してインポートする場合、10 個のTiDB Lightning構成ファイルを作成する必要があります。各ファイルで、対応するTiDB Lightningインスタンスによって読み取られるソース ファイルの範囲を構成する必要があります。たとえば、 TiDB Lightningインスタンス 1 は最初の 100 個のファイルを読み取り、インスタンス 2 は次の 100 個のファイルを読み取ります。

さらに、これら 10 個のTiDB Lightningインスタンスの共有メタデータ テーブルやその他の構成情報を構成する必要があり、これは複雑です。

### グローバルソートとローカルソート {#global-sort-vs-local-sort}

#### <code>IMPORT INTO</code> {#code-import-into-code}

TiDB Global Sort を使用すると、 `IMPORT INTO`十 TiB のソースデータを複数の TiDB ノードに送信し、データ KV ペアとインデックス KV ペアをエンコードしてから、これらのペアを Amazon S3 に転送してグローバルソートしてから、TiKV に書き込むことができます。

これらの KV ペアはグローバルにソートされているため、さまざまな TiDB ノードから TiKV にインポートされたデータは重複せず、RocksDB に直接書き込むことができます。これにより、TiKV が圧縮操作を実行する必要がなくなり、TiKV の書き込みパフォーマンスと安定性の両方が大幅に向上します。

インポートが完了すると、Amazon S3 上のグローバルソートに使用されたデータは自動的に削除され、storageコストが節約されます。

#### TiDB Lightning {#tidb-lightning}

TiDB Lightning はローカル ソートのみをサポートします。たとえば、数十 TiB のソース データの場合、 TiDB Lightningに大規模なローカル ディスクが設定されていない場合、または複数のTiDB Lightningインスタンスが並列インポートに使用されている場合、各TiDB Lightningインスタンスはローカル ディスクのみを使用してインポートするデータをソートできます。グローバル ソートを実行できないため、特にインデックス データが多く存在するシナリオでは、複数のTiDB Lightningインスタンスによって TiKV にインポートされたデータに重複が生じ、TiKV が圧縮操作を実行するようになります。圧縮操作はリソースを大量に消費するため、TiKV の書き込みパフォーマンスと安定性が低下します。

後でデータのインポートを続行する場合は、次のインポートのためにTiDB Lightningサーバーとサーバー上のディスクを保持する必要があります。事前割り当てディスクを使用する場合のコストは、従量課金制で Amazon S3 を使用する`IMPORT INTO`と比較して比較的高くなります。

### パフォーマンス {#performance}

現在、 `IMPORT INTO`とTiDB Lightningの間で同等のテスト環境でのパフォーマンステスト比較結果はありません。

グローバルソートのstorageとして Amazon S3 を使用した場合、 `IMPORT INTO`のパフォーマンステスト結果は次のとおりです。

| ソースデータセット                             | ノード構成                                            | TiDBノードあたりの平均インポート速度 |
| ------------------------------------- | ------------------------------------------------ | -------------------- |
| 40 TiB データ (22.6 億行、行あたり 19 KiB)      | 10 個の TiDB (16C32G) ノードと 20 個の TiKV (16C27G) ノード | 222 GiB/時            |
| 10 TiB データ (5 億 6,500 万行、行あたり 19 KiB) | 5 つの TiDB (16C32G) ノードと 10 つの TiKV (16C27G) ノード  | 307 GiB/時            |

### 高可用性 {#high-availability}

#### <code>IMPORT INTO</code> {#code-import-into-code}

TiDB ノードに障害が発生すると、そのノード上のタスクは残りの TiDB ノードに自動的に転送され、実行が継続されます。

#### TiDB Lightning {#tidb-lightning}

TiDB Lightningインスタンス ノードに障害が発生した場合は、以前に記録されたチェックポイントに基づいて、新しいノードでタスクの手動リカバリを実行する必要があります。

### スケーラビリティ {#scalability}

#### <code>IMPORT INTO</code> {#code-import-into-code}

グローバルソートを使用しているため、TiKV にインポートされたデータは重複せず、 TiDB Lightningと比較してスケーラビリティが向上します。

#### TiDB Lightning {#tidb-lightning}

ローカルソートのみをサポートしているため、新しいTiDB Lightningインスタンスが追加されたときに TiKV にインポートされたデータが重複する可能性があり、その結果、 TiKV の圧縮操作が増え、 `IMPORT INTO`に比べてスケーラビリティが制限されます。

## <code>IMPORT INTO</code>でサポートされていない機能 {#functionalities-not-supported-by-code-import-into-code}

現在、 `IMPORT INTO`まだいくつかの機能が欠けており、次のようなシナリオではTiDB Lightning を完全に置き換えることはできません。

-   論理インポート

    `IMPORT INTO`でデータをインポートする前に、ターゲット テーブルは空である必要があります。すでにデータが含まれているテーブルにデータをインポートする必要がある場合は、 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)や直接挿入などの方法を使用することをお勧めします。v8.0 以降、TiDB は大規模なトランザクションを実行するために[バルクDML](/system-variables.md#tidb_dml_type-new-in-v800)サポートしています。

-   競合データの処理

    `IMPORT INTO`現在、競合データの処理をサポートしていません。データのインポート前に、インポートするデータが主キー (PK) または一意キー (UK) と競合しないように、テーブル スキーマを適切に定義する必要があります。そうしないと、タスクが失敗する可能性があります。

-   複数のターゲット テーブルにデータをインポートする

    現在、 `IMPORT INTO`つの SQL ステートメントに対して許可されるターゲット テーブルは 1 つだけです。複数のターゲット テーブルにデータをインポートする場合は、複数の`IMPORT INTO` SQL ステートメントを送信する必要があります。

将来のバージョンでは、これらの機能は`IMPORT INTO`でサポートされるほか、タスク実行中の同時実行の変更や TiKV への書き込みスループットの調整などの機能強化も行われます。これにより、タスクの管理がより便利になります。

## まとめ {#summary}

TiDB Lightningと比較すると、 `IMPORT INTO` TiDB ノード上で直接実行でき、自動化された分散タスク スケジューリングと[TiDB グローバルソート](/tidb-global-sort.md)サポートし、デプロイメント、リソース使用率、タスク構成の利便性、呼び出しと統合の容易さ、高可用性、スケーラビリティが大幅に向上しています。適切なシナリオでは、 TiDB Lightningではなく`IMPORT INTO`使用を検討することをお勧めします。
