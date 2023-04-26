---
title: TiDB Architecture FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB.
---

# TiDBアーキテクチャよくある質問 {#tidb-architecture-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントでは、TiDB に関する最もよくある質問を一覧表示します。

## TiDB の紹介とアーキテクチャ {#tidb-introduction-and-architecture}

### TiDBとは？ {#what-is-tidb}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

[TiDB](https://github.com/pingcap/tidb)は、Hybrid Transactional and Analytical Processing (HTAP) ワークロードをサポートするオープンソースの分散 SQL データベースです。 MySQL と互換性があり、水平方向のスケーラビリティ、強力な一貫性、および高可用性を備えています。 TiDB の目標は、OLTP (オンライン トランザクション処理)、OLAP (オンライン分析処理)、および HTAP サービスをカバーするワンストップ データベース ソリューションをユーザーに提供することです。 TiDB は、高可用性と大規模データとの強力な整合性を必要とするさまざまなユース ケースに適しています。

### TiDB のアーキテクチャとは? {#what-is-tidb-s-architecture}

TiDB クラスターには、TiDBサーバー、PD (Placement Driver)サーバー、および TiKVサーバー の3 つのコンポーネントがあります。詳細については、 [TiDBアーキテクチャ](/tidb-architecture.md) 、 [TiDBstorage](/tidb-storage.md) 、 [TiDB コンピューティング](/tidb-computing.md) 、および[TiDB スケジューリング](/tidb-scheduling.md)を参照してください。

### TiDB は MySQL をベースにしていますか? {#is-tidb-based-on-mysql}

いいえ。TiDB は MySQL の構文とプロトコルをサポートしていますが、これは PingCAP, Inc. によって開発および保守されている新しいオープン ソース データベースです。

### TiDB、TiKV、PD (Placement Driver) のそれぞれの責任は何ですか? {#what-is-the-respective-responsibility-of-tidb-tikv-and-pd-placement-driver}

-   TiDB は SQL コンピューティングレイヤーとして機能し、主に SQL の解析、クエリ プランの指定、エグゼキューターの生成を担当します。
-   TiKV は、実際のデータを格納するために使用される分散 Key-Valuestorageエンジンとして機能します。つまり、TiKV は TiDB のstorageエンジンです。
-   PD は、TiKV メタデータの管理、タイムスタンプの割り当て、データの配置と負荷分散の決定を行う TiDB のクラスター マネージャーとして機能します。

### TiDB は使いやすいですか？ {#is-it-easy-to-use-tidb}

はい、そうです。必要なサービスがすべて開始されると、MySQLサーバーと同じくらい簡単に TiDB を使用できます。ほとんどの場合、コードを 1 行も変更することなく、MySQL を TiDB に置き換えてアプリケーションを強化できます。また、人気のある MySQL 管理ツールを使用して TiDB を管理することもできます。

### TiDB は MySQL とどのように互換性がありますか? {#how-is-tidb-compatible-with-mysql}

現在、TiDB はMySQL 5.7構文の大部分をサポートしていますが、トリガー、ストアド プロシージャ、ユーザー定義関数、および外部キーはサポートしていません。詳細については、 [MySQL との互換性](/mysql-compatibility.md)を参照してください。

### TiDB は分散トランザクションをサポートしていますか? {#does-tidb-support-distributed-transactions}

はい。 TiDB は、単一の場所にある少数のノードであろうと、多数のノードであろうと、クラスター全体にトランザクションを分散します[複数のデータセンターにまたがるノード](/multi-data-centers-in-one-city-deployment.md) 。

Google の Percolator に触発された TiDB のトランザクション モデルは、主に 2 フェーズ コミット プロトコルであり、いくつかの実用的な最適化が行われています。このモデルは、タイムスタンプ アロケータに依存して、トランザクションごとに単調に増加するタイムスタンプを割り当てるため、競合を検出できます。 [PD](/tidb-architecture.md#placement-driver-pd-server) TiDB クラスターでタイムスタンプ アロケーターとして機能します。

### TiDB を操作するには、どのプログラミング言語を使用できますか? {#what-programming-language-can-i-use-to-work-with-tidb}

MySQL クライアントまたはドライバーがサポートする任意の言語。

### TiDB で他の Key-Valuestorageエンジンを使用できますか? {#can-i-use-other-key-value-storage-engines-with-tidb}

はい。 TiKV に加えて、TiDB は UniStore や MockTiKV などのスタンドアロンstorageエンジンをサポートします。今後の TiDB リリースでは、MockTiKV がサポートされなくなる可能性があることに注意してください。

TiDB がサポートするすべてのstorageエンジンを確認するには、次のコマンドを使用します。

{{< copyable "" >}}

```shell
./bin/tidb-server -h
```

出力は次のとおりです。

```shell
Usage of ./bin/tidb-server:
  -L string
        log level: info, debug, warn, error, fatal (default "info")
  -P string
        tidb server port (default "4000")
  -V    print version information and exit (default false)
.........
  -store string
        registered store name, [tikv, mocktikv, unistore] (default "unistore")
  ......
```

### TiDB のドキュメント以外に、TiDB の知識を得る方法はありますか? {#in-addition-to-the-tidb-documentation-are-there-any-other-ways-to-acquire-tidb-knowledge}

-   [TiDB ドキュメント](https://docs.pingcap.com/) : TiDB 関連の知識を得るための最も重要でタイムリーな方法。
-   [TiDB ブログ](https://www.pingcap.com/blog/) : 技術記事、製品の洞察、およびケース スタディを学習します。
-   [PingCAP教育](https://www.pingcap.com/education/?from=en) : オンライン コースと認定プログラムを受講します。

### TiDB ユーザー名の長さ制限は? {#what-is-the-length-limit-for-the-tidb-user-name}

最大 32 文字。

### TiDB の列数と行サイズの制限は何ですか? {#what-are-the-limits-on-the-number-of-columns-and-row-size-in-tidb}

-   TiDB の列の最大数のデフォルトは 1017 です。この数は最大 4096 まで調整できます。
-   1 行の最大サイズのデフォルトは 6 MB です。この数は最大 120 MB まで増やすことができます。

詳細については、 [TiDB の制限事項](/tidb-limitations.md)を参照してください。

### TiDB は XA をサポートしていますか? {#does-tidb-support-xa}

いいえ。TiDB の JDBC ドライバーは MySQL Connector/J です。 Atomikos を使用する場合は、データ ソースを`type="com.mysql.jdbc.jdbc2.optional.MysqlXADataSource"`に設定します。 TiDB は、MySQL JDBC XADataSource との接続をサポートしていません。 MySQL JDBC XADataSource は MySQL でのみ機能します (たとえば、DML を使用して`redo`ログを変更します)。

Atomikos の 2 つのデータ ソースを構成したら、JDBC ドライブを XA に設定します。 Atomikos が TM と RM (DB) を操作する場合、Atomikos は XA を含むコマンドを JDBCレイヤーに送信します。 MySQL を例にとると、JDBCレイヤーで XA が有効になっている場合、JDBC は、DML を使用して`redo`ログを変更するなど、一連の XA ロジック操作を InnoDB に送信します。これが 2 フェーズ コミットの動作です。現在の TiDB バージョンは、上位アプリケーションレイヤーのJTA/XA をサポートしておらず、Atomikos から送信された XA 操作を解析していません。

スタンドアロン データベースとして、MySQL は XA を使用したデータベース間トランザクションのみを実装できます。一方、TiDB は Google Percolator トランザクション モデルを使用した分散トランザクションをサポートし、そのパフォーマンスの安定性は XA よりも高いため、TiDB は JTA/XA をサポートせず、TiDB が XA をサポートする必要はありません。

### TiDB は、パフォーマンスを損なわずに、カラムナstorageエンジン (TiFlash) に対する多数の同時<code>INSERT</code>または<code>UPDATE</code>操作をサポートするにはどうすればよいでしょうか? {#how-could-tidb-support-high-concurrent-code-insert-code-or-code-update-code-operations-to-the-columnar-storage-engine-tiflash-without-hurting-performance}

-   [TiFlash](/tiflash/tiflash-overview.md)列エンジンの変更を処理するために DeltaTree という名前の特別な構造を導入します。
-   TiFlash はRaftグループの学習者の役割として機能するため、ログのコミットまたは書き込みには投票しません。これは、DML 操作がTiFlashの確認応答を待つ必要がないことを意味します。これが、 TiFlash がOLTP パフォーマンスを低下させない理由です。さらに、 TiFlashと TiKV は別々のインスタンスで動作するため、互いに影響しません。

### TiFlash は最終的に整合性がありますか? {#is-tiflash-eventually-consistent}

はい。 TiFlash は、デフォルトで強力なデータ整合性を維持します。

## TiDB テクニック {#tidb-techniques}

### データstorage用TiKV {#tikv-for-data-storage}

[TiDB 内部 (I) - データストレージ](https://www.pingcap.com/blog/tidb-internal-data-storage/?from=en)を参照してください。

### データ コンピューティング用の TiDB {#tidb-for-data-computing}

[TiDB 内部 (II) - コンピューティング](https://www.pingcap.com/blog/tidb-internal-computing/?from=en)を参照してください。

### スケジューリング用 PD {#pd-for-scheduling}

[TiDB 内部 (III) - スケジューリング](https://www.pingcap.com/blog/tidb-internal-scheduling/?from=en)を参照してください。
