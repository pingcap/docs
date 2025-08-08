---
title: IMPORT INTO vs. TiDB Lightning
summary: IMPORT INTO` とTiDB Lightningの違いについて説明します。
---

# IMPORT INTO とTiDB Lightning の比較 {#import-into-vs-tidb-lightning}

多くのユーザーから、 [TiDB Lightning](/tidb-lightning/tidb-lightning-configuration.md)の展開、構成、メンテナンスは、特に[並行輸入](/tidb-lightning/tidb-lightning-distributed-import.md)の大規模なデータセットが関係するシナリオでは複雑であるというフィードバックが寄せられています。

皆様からのフィードバックに基づき、TiDBはTiDB Lightningの一部の機能を[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) SQL文に段階的に統合してきました。3 `IMPORT INTO`実行することでデータを直接インポートできるため、データインポートの効率が向上します。さらに、 `IMPORT INTO`自動分散タスクスケジューリングや[TiDB グローバルソート](/tidb-global-sort.md)といった、 TiDB Lightningにはない機能もサポートされています。

`IMPORT INTO`はv7.2.0で導入され、v7.5.0で一般提供（GA）されます。今後のバージョンでも引き続き改良と最適化が行われます。2 `IMPORT INTO`機能がTiDB Lightningを完全に置き換えることが可能になった時点で、 TiDB Lightningは廃止されます。その際には、TiDBのリリースノートおよびドキュメントで事前にお知らせいたします。

## <code>IMPORT INTO</code>とTiDB Lightningの比較 {#comparison-between-code-import-into-code-and-tidb-lightning}

次のセクションでは、 `IMPORT INTO`とTiDB Lightningの違いをさまざまな側面から説明します。

### 導入コスト {#deployment-cost}

#### <code>IMPORT INTO</code> {#code-import-into-code}

`IMPORT INTO`個別のデプロイメントを必要としません。TiDB ノード上で直接実行できるため、追加のデプロイメント作業が不要になります。

#### TiDB Lightning {#tidb-lightning}

対照的に、 TiDB Lightning[個別のサーバー展開](/tidb-lightning/deploy-tidb-lightning.md)必要です。

### リソースの活用 {#resource-utilization}

#### <code>IMPORT INTO</code> {#code-import-into-code}

`IMPORT INTO`タスクと他のビジネスワークロードは、TiDB リソースを共有したり、異なるタイミングで利用したりすることで、TiDB リソースを最大限に活用できます。3 タスクのパフォーマンスと安定性を維持しながら、ビジネスワークロードの安定した運用を確保するために、 `IMPORT INTO`タスクにデータインポート専用の[特定のTiDBノード](/system-variables.md#tidb_service_scope-new-in-v740)を指定することができ`IMPORT INTO` 。

[TiDB グローバルソート](/tidb-global-sort.md)使用する場合、大容量のローカルディスクをマウントする必要はありません。TiDB Global Sort は Amazon S3 をstorageとして使用できます。インポートタスクが完了すると、グローバルソート用に Amazon S3 に保存された一時データは自動的に削除され、storageコストを節約できます。

#### TiDB Lightning {#tidb-lightning}

TiDB Lightning をデプロイして実行するには、別々のサーバーが必要です。インポートタスクが実行されていない場合、これらのリソースはアイドル状態のままになります。インポートタスクが定期的に実行されるシナリオでは、合計アイドル時間はさらに長くなり、リソースの無駄が発生します。

インポートするデータセットが大きい場合は、インポートするデータをソートするための大容量のローカル ディスクも準備する必要があります。

### タスクの構成と統合 {#task-configuration-and-integration}

#### <code>IMPORT INTO</code> {#code-import-into-code}

You can directly write SQL statements to submit import tasks, which are easy to call and integrate.

#### TiDB Lightning {#tidb-lightning}

対照的に、 TiDB Lightning[タスク設定ファイル](/tidb-lightning/tidb-lightning-configuration.md)記述する必要があります。これらの構成ファイルは複雑であり、サードパーティが簡単に呼び出すことはできません。

### タスクのスケジュール {#task-scheduling}

#### <code>IMPORT INTO</code> {#code-import-into-code}

`IMPORT INTO`分散実行をサポートします。例えば、40TiBのソースデータファイルを1つのターゲットテーブルにインポートする場合、SQL文の送信後、TiDBはインポートタスクを複数のサブタスクに自動的に分割し、各サブタスクを実行するために異なるTiDBノードをスケジュールします。

#### TiDB Lightning {#tidb-lightning}

対照的に、 TiDB Lightningの構成は複雑で非効率であり、エラーが発生しやすくなります。

10 個のTiDB Lightningインスタンスを起動してデータを並列インポートする場合、10 個のTiDB Lightning設定ファイルを作成する必要があります。各ファイルでは、対応するTiDB Lightningインスタンスが読み取るソースファイルの範囲を設定する必要があります。例えば、 TiDB Lightningインスタンス 1 は最初の 100 ファイルを読み取り、インスタンス 2 は次の 100 ファイルを読み取り、というように続きます。

さらに、これら 10 個のTiDB Lightningインスタンスの共有メタデータ テーブルやその他の構成情報を構成する必要があり、これは複雑です。

### グローバルソートとローカルソート {#global-sort-vs-local-sort}

#### <code>IMPORT INTO</code> {#code-import-into-code}

TiDB Global Sort を使用すると、 `IMPORT INTO`十 TiB のソースデータを複数の TiDB ノードに送信し、データ KV ペアとインデックス KV ペアをエンコードしてから、これらのペアを Amazon S3 に転送してグローバルソートしてから、TiKV に書き込むことができます。

これらのKVペアはグローバルにソートされているため、複数のTiDBノードからTiKVにインポートされたデータは重複せず、RocksDBに直接書き込むことができます。これにより、TiKVによる圧縮操作が不要になり、TiKVの書き込みパフォーマンスと安定性が大幅に向上します。

インポートが完了すると、Amazon S3 上のグローバルソートに使用されたデータは自動的に削除され、storageコストを節約できます。

#### TiDB Lightning {#tidb-lightning}

TiDB Lightningはローカルソートのみをサポートします。例えば、数十TiB規模のソースデータの場合、 TiDB Lightningに大容量のローカルディスクが設定されていない場合、または複数のTiDB Lightningインスタンスを並列インポートに使用している場合、各TiDB Lightningインスタンスはローカルディスクを使用してのみインポートデータをソートできます。グローバルソートを実行できないため、複数のTiDB LightningインスタンスからTiKVにインポートされたデータに重複が生じ、特にインデックスデータが多いシナリオでは、TiKVは圧縮操作を実行します。圧縮操作はリソースを大量に消費するため、TiKVの書き込みパフォーマンスと安定性が低下します。

後日データのインポートを継続する場合は、次回のインポートのためにTiDB Lightningサーバーとサーバー上のディスクを保持しておく必要があります。事前割り当てディスクを使用する場合のコストは、Amazon S3を従量課金制で使用した`IMPORT INTO`と比較して比較的高くなります。

### パフォーマンス {#performance}

現在、 `IMPORT INTO`とTiDB Lightningの間で同等のテスト環境下でのパフォーマンステスト比較結果はありません。

グローバルソートのstorageとして Amazon S3 を使用した場合、 `IMPORT INTO`のパフォーマンステスト結果は次のとおりです。

| ソースデータセット                              | ノード構成                                   | TiDBノードあたりの平均インポート速度 |
| -------------------------------------- | --------------------------------------- | -------------------- |
| 40 TiB のデータ (22.6 億行、行あたり 19 KiB)      | 10個のTiDB（16C32G）ノードと20個のTiKV（16C27G）ノード | 222 GiB/時            |
| 10 TiB のデータ (5 億 6,500 万行、行あたり 19 KiB) | 5つのTiDB（16C32G）ノードと10つのTiKV（16C27G）ノード  | 307 GiB/時            |

### 高可用性 {#high-availability}

#### <code>IMPORT INTO</code> {#code-import-into-code}

TiDB ノードに障害が発生すると、そのノード上のタスクは残りの TiDB ノードに自動的に転送され、実行が継続されます。

#### TiDB Lightning {#tidb-lightning}

TiDB Lightningインスタンス ノードに障害が発生した場合、以前に記録されたチェックポイントに基づいて、新しいノードでタスクの手動リカバリを実行する必要があります。

### スケーラビリティ {#scalability}

#### <code>IMPORT INTO</code> {#code-import-into-code}

Due to the use of Global Sort, data imported into TiKV does not overlap, resulting in better scalability compared with TiDB Lightning.

#### TiDB Lightning {#tidb-lightning}

ローカルソートのみをサポートしているため、新しいTiDB Lightningインスタンスが追加されたときに TiKV にインポートされたデータが重複する可能性があり、その結果 TiKV の圧縮操作が増え、 `IMPORT INTO`に対するスケーラビリティが制限されます。

## <code>IMPORT INTO</code>でサポートされていない機能 {#functionalities-not-supported-by-code-import-into-code}

現在、 `IMPORT INTO`はまだいくつかの機能が欠けており、次のようなシナリオではTiDB Lightning を完全に置き換えることはできません。

-   論理インポート

    `IMPORT INTO`でデータをインポートする前に、ターゲットテーブルは空である必要があります。既にデータが含まれているテーブルにデータをインポートする必要がある場合は、 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)や直接挿入などの方法を使用することをお勧めします。TiDB v8.0以降、大規模トランザクションの実行には[バルクDML](/system-variables.md#tidb_dml_type-new-in-v800)サポートされます。

-   競合データの処理

    `IMPORT INTO`現在、競合データの処理をサポートしていません。データのインポート前に、インポートするデータが主キー（PK）または一意キー（UK）と競合しないように、テーブルスキーマを適切に定義する必要があります。そうしないと、タスクが失敗する可能性があります。

-   複数のターゲットテーブルへのデータのインポート

    現在、 `IMPORT INTO` SQL文で指定できるターゲットテーブルは1つだけです。複数のターゲットテーブルにデータをインポートする場合は、 `IMPORT INTO`のSQL文を発行する必要があります。

将来のバージョンでは、これらの機能は`IMPORT INTO`でサポートされる予定です。また、タスク実行中の同時実行性の変更やTiKVへの書き込みスループットの調整といった機能強化も行われます。これにより、タスク管理がより便利になります。

## まとめ {#summary}

TiDB Lightningと比較すると、 `IMPORT INTO` TiDBノード上で直接実行でき、自動化された分散タスクスケジューリングと[TiDB グローバルソート](/tidb-global-sort.md)サポートし、デプロイメント、リソース利用率、タスク設定の利便性、呼び出しと統合の容易さ、高可用性、スケーラビリティにおいて大幅な改善をもたらします。適切なシナリオでは、 TiDB Lightningではなく`IMPORT INTO`使用を検討することをお勧めします。
