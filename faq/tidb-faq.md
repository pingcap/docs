---
title: TiDB Architecture FAQs
summary: TiDB に関するよくある質問 (FAQ) について説明します。
---

# TiDBアーキテクチャFAQ {#tidb-architecture-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントには、TiDB に関するよくある質問が記載されています。

## TiDB の紹介とアーキテクチャ {#tidb-introduction-and-architecture}

### TiDB とは何ですか? {#what-is-tidb}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

[ティビ](https://github.com/pingcap/tidb)は、ハイブリッド トランザクションおよび分析処理 (HTAP) ワークロードをサポートするオープンソースの分散 SQL データベースです。MySQL と互換性があり、水平スケーラビリティ、強力な一貫性、高可用性を備えています。TiDB の目標は、OLTP (オンライン トランザクション処理)、OLAP (オンライン分析処理)、および HTAP サービスをカバーするワンストップ データベース ソリューションをユーザーに提供することです。TiDB は、大規模データで高可用性と強力な一貫性を必要とするさまざまなユース ケースに適しています。

### TiDB のアーキテクチャは何ですか? {#what-is-tidb-s-architecture}

TiDB クラスターには、TiDBサーバー、PD (配置Driver)サーバー、および TiKVサーバーの3 つのコンポーネントがあります。詳細については、 [TiDBアーキテクチャ](/tidb-architecture.md) 、 [TiDBstorage](/tidb-storage.md) 、 [TiDBコンピューティング](/tidb-computing.md) 、および[TiDB スケジューリング](/tidb-scheduling.md)を参照してください。

### TiDB は MySQL に基づいていますか? {#is-tidb-based-on-mysql}

いいえ。TiDB は MySQL の構文とプロトコルをサポートしていますが、PingCAP, Inc. によって開発および保守されている新しいオープン ソース データベースです。

### TiDB、TiKV、PD (Placement Driver) のそれぞれの責任は何ですか? {#what-is-the-respective-responsibility-of-tidb-tikv-and-pd-placement-driver}

-   TiDB は SQL コンピューティングレイヤーとして機能し、主に SQL の解析、クエリ プランの指定、エグゼキュータの生成を担当します。
-   TiKV は、実際のデータを保存するために使用される分散型キー値storageエンジンとして機能します。つまり、TiKV は TiDB のstorageエンジンです。
-   PD は TiDB のクラスター マネージャーとして機能し、TiKV メタデータを管理し、タイムスタンプを割り当て、データの配置と負荷分散の決定を行います。

### TiDB は使いやすいですか? {#is-it-easy-to-use-tidb}

はい、そうです。必要なサービスがすべて起動すると、MySQLサーバーと同じくらい簡単に TiDB を使用できます。ほとんどの場合、コードを 1 行も変更せずに、MySQL を TiDB に置き換えてアプリケーションを強化できます。また、一般的な MySQL 管理ツールを使用して TiDB を管理することもできます。

### TiDB は MySQL とどのように互換性がありますか? {#how-is-tidb-compatible-with-mysql}

現在、TiDB は MySQL 8.0 構文の大部分をサポートしていますが、トリガー、ストアド プロシージャ、およびユーザー定義関数はサポートしていません。詳細については、 [MySQLとの互換性](/mysql-compatibility.md)参照してください。

### TiDB は分散トランザクションをサポートしていますか? {#does-tidb-support-distributed-transactions}

はい。TiDB は、単一の場所にある少数のノードであっても、多数の[複数のデータセンターにわたるノード](/multi-data-centers-in-one-city-deployment.md)であっても、クラスター全体にトランザクションを分散します。

Google の Percolator にヒントを得た TiDB のトランザクション モデルは、主に 2 フェーズ コミット プロトコルで、実用的な最適化がいくつか施されています。このモデルは、タイムスタンプ アロケータを使用して各トランザクションに単調に増加するタイムスタンプを割り当てるため、競合を検出できます。1 [PD](/tidb-architecture.md#placement-driver-pd-server) 、TiDB クラスターのタイムスタンプ アロケータとして機能します。

### TiDB を操作するために使用できるプログラミング言語は何ですか? {#what-programming-language-can-i-use-to-work-with-tidb}

MySQL クライアントまたはドライバーでサポートされている任意の言語。

### TiDB で他のキー値storageエンジンを使用できますか? {#can-i-use-other-key-value-storage-engines-with-tidb}

はい。TiKV に加えて、TiDB は UniStore や MockTiKV などのスタンドアロンstorageエンジンをサポートしています。今後の TiDB リリースでは、MockTiKV がサポートされなくなる可能性があることに注意してください。

TiDB でサポートされているすべてのstorageエンジンを確認するには、次のコマンドを使用します。

```shell
./bin/tidb-server -h
```

出力は次のようになります。

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

### TiDB ドキュメントの他に、TiDB の知識を習得する方法はありますか? {#in-addition-to-the-tidb-documentation-are-there-any-other-ways-to-acquire-tidb-knowledge}

-   [TiDB ドキュメント](https://docs.pingcap.com/) : TiDB 関連の知識を得るための最も重要かつタイムリーな方法。
-   [TiDB ブログ](https://www.pingcap.com/blog/) : 技術記事、製品の洞察、ケーススタディを学びます。
-   [PingCAP教育](https://www.pingcap.com/education/?from=en) : オンラインコースや認定プログラムを受講します。

### TiDB ユーザー名の長さ制限は何ですか? {#what-is-the-length-limit-for-the-tidb-user-name}

最大32文字。

### TiDB の列数と行サイズの制限は何ですか? {#what-are-the-limits-on-the-number-of-columns-and-row-size-in-tidb}

-   TiDB の列の最大数はデフォルトで 1017 です。この数は最大 4096 まで調整できます。
-   1 行の最大サイズはデフォルトで 6 MB です。この数値は最大 120 MB まで増やすことができます。

詳細については[TiDB の制限](/tidb-limitations.md)参照してください。

### TiDB は XA をサポートしていますか? {#does-tidb-support-xa}

いいえ。TiDB の JDBC ドライバーは MySQL Connector/J です。Atomikos を使用する場合は、データ ソースを`type="com.mysql.jdbc.jdbc2.optional.MysqlXADataSource"`に設定してください。TiDB は、MySQL JDBC XADataSource との接続をサポートしていません。MySQL JDBC XADataSource は、MySQL でのみ機能します (たとえば、DML を使用して`redo`ログを変更する場合)。

Atomikos の 2 つのデータ ソースを設定したら、JDBC ドライブを XA に設定します。Atomikos が TM と RM (DB) を操作する場合、Atomikos は XA を含むコマンドを JDBCレイヤーに送信します。MySQL を例にとると、JDBCレイヤーで XA が有効になっている場合、JDBC は DML を使用して`redo`ログを変更することを含む一連の XA ロジック操作を InnoDB に送信します。これが 2 フェーズ コミットの操作です。現在の TiDB バージョンは、上位アプリケーションレイヤーのJTA/XA をサポートしておらず、Atomikos が送信した XA 操作を解析しません。

スタンドアロン データベースとして、MySQL は XA を使用してデータベース間トランザクションのみを実装できます。一方、TiDB は Google Percolator トランザクション モデルを使用して分散トランザクションをサポートし、パフォーマンスの安定性は XA よりも高いため、TiDB は JTA/XA をサポートしておらず、TiDB が XA をサポートする必要もありません。

### TiDB は、パフォーマンスを損なうことなく、列指向storageエンジン (TiFlash) への大量の同時<code>INSERT</code>または<code>UPDATE</code>操作をどのようにサポートできるでしょうか? {#how-could-tidb-support-high-concurrent-code-insert-code-or-code-update-code-operations-to-the-columnar-storage-engine-tiflash-without-hurting-performance}

-   [TiFlash](/tiflash/tiflash-overview.md)列指向エンジンの変更を処理するために DeltaTree という特別な構造が導入されています。
-   TiFlash はRaftグループ内で学習者の役割として機能するため、ログのコミットや書き込みには投票しません。つまり、DML 操作はTiFlashの確認応答を待つ必要がないため、 TiFlashOLTP のパフォーマンスが低下することはありません。さらに、 TiFlashと TiKV は別々のインスタンスで動作するため、互いに影響を及ぼしません。

### TiFlash はどのような一貫性を提供しますか? {#what-kind-of-consistency-does-tiflash-provide}

TiFlash はデフォルトで強力なデータ一貫性を維持します。ラフト学習プロセスがデータを更新します。クエリ内のデータがトランザクションと完全に一致していることを確認するための TSO チェックもあります。詳細については、 [非同期レプリケーション](/tiflash/tiflash-overview.md#asynchronous-replication)および[一貫性](/tiflash/tiflash-overview.md#consistency)参照してください。

## TiDB テクニック {#tidb-techniques}

### データstorage用のTiKV {#tikv-for-data-storage}

[TiDB 内部 (I) - データ ストレージ](https://www.pingcap.com/blog/tidb-internal-data-storage/?from=en)参照。

### データコンピューティングのための TiDB {#tidb-for-data-computing}

[TiDB 内部 (II) - コンピューティング](https://www.pingcap.com/blog/tidb-internal-computing/?from=en)参照。

### スケジュールのPD {#pd-for-scheduling}

[TiDB 内部 (III) - スケジュール](https://www.pingcap.com/blog/tidb-internal-scheduling/?from=en)参照。
