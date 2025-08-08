---
title: TiDB Architecture FAQs
summary: TiDB に関するよくある質問 (FAQ) について説明します。
---

# TiDBアーキテクチャに関するFAQ {#tidb-architecture-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントには、TiDB に関するよくある質問が記載されています。

## TiDB の紹介とアーキテクチャ {#tidb-introduction-and-architecture}

### TiDB とは何ですか? {#what-is-tidb}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

TiDB [TiDB](https://github.com/pingcap/tidb)は、ハイブリッドトランザクションおよび分析処理（HTAP）ワークロードをサポートするオープンソースの分散SQLデータベースです。MySQLと互換性があり、水平スケーラビリティ、強力な一貫性、高可用性を備えています。TiDBの目標は、OLTP（オンライントランザクション処理）、OLAP（オンライン分析処理）、そしてHTAPサービスをカバーするワンストップデータベースソリューションをユーザーに提供することです。TiDBは、大規模データで高可用性と強力な一貫性が求められる様々なユースケースに適しています。

### TiDB のアーキテクチャとは何ですか? {#what-is-tidb-s-architecture}

TiDBクラスタは、TiDBサーバー、PD（配置Driver）サーバー、TiKVサーバーの3つのコンポーネントで構成されています。詳細については、 [TiDBアーキテクチャ](/tidb-architecture.md) [TiDBstorage](/tidb-storage.md)参照して[TiDB スケジューリング](/tidb-scheduling.md) [TiDBコンピューティング](/tidb-computing.md)

### TiDB は MySQL に基づいていますか? {#is-tidb-based-on-mysql}

いいえ。TiDB は MySQL の構文とプロトコルをサポートしていますが、PingCAP, Inc. によって開発および保守されている新しいオープン ソース データベースです。

### TiDB、TiKV、PD (配置Driver) のそれぞれの責任は何ですか? {#what-is-the-respective-responsibility-of-tidb-tikv-and-pd-placement-driver}

-   TiDB は SQL コンピューティングレイヤーとして機能し、主に SQL の解析、クエリ プランの指定、エグゼキュータの生成を担当します。
-   TiKVは分散型のキーバリューstorageエンジンとして動作し、実データの保存に使用されます。つまり、TiKVはTiDBのstorageエンジンです。
-   PD は TiDB のクラスター マネージャーとして機能し、TiKV メタデータを管理し、タイムスタンプを割り当て、データの配置と負荷分散の決定を行います。

### TiDB は使いやすいですか? {#is-it-easy-to-use-tidb}

はい、可能です。必要なサービスがすべて起動していれば、TiDBはMySQLサーバーと同じくらい簡単に使用できます。MySQLをTiDBに置き換えれば、ほとんどの場合、コードを1行も変更することなくアプリケーションを強化できます。また、一般的なMySQL管理ツールを使用してTiDBを管理することも可能です。

### TiDB は MySQL とどのように互換性がありますか? {#how-is-tidb-compatible-with-mysql}

現在、TiDBはMySQL 8.0の構文の大部分をサポートしていますが、トリガー、ストアドプロシージャ、ユーザー定義関数はサポートしていません。詳細については、 [MySQLとの互換性](/mysql-compatibility.md)参照してください。

### TiDB は分散トランザクションをサポートしていますか? {#does-tidb-support-distributed-transactions}

はい。TiDB は、単一の場所に少数のノードがある場合でも、多数の[複数のデータセンターにまたがるノード](/multi-data-centers-in-one-city-deployment.md)がある場合でも、クラスター全体にトランザクションを分散します。

GoogleのPercolatorに着想を得たTiDBのトランザクションモデルは、主に2フェーズコミットプロトコルをベースに、実用的な最適化が施されています。このモデルは、タイムスタンプアロケータを利用して各トランザクションに単調増加するタイムスタンプを割り当てることで、競合を検出します。1 [PD](/tidb-architecture.md#placement-driver-pd-server) TiDBクラスタ内でタイムスタンプアロケータとして機能します。

### TiDB を操作するためにどのプログラミング言語を使用できますか? {#what-programming-language-can-i-use-to-work-with-tidb}

MySQL クライアントまたはドライバーでサポートされている任意の言語。

### TiDB で他のキー値storageエンジンを使用できますか? {#can-i-use-other-key-value-storage-engines-with-tidb}

はい。TiDBはTiKVに加えて、UniStoreやMockTiKVなどのスタンドアロンstorageエンジンをサポートしています。ただし、今後のTiDBリリースでは、MockTiKVはサポートされなくなる可能性がありますのでご注意ください。

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

-   [TiDBドキュメント](https://docs.pingcap.com/) : TiDB 関連の知識を得るための最も重要かつタイムリーな方法。
-   [TiDBブログ](https://www.pingcap.com/blog/) : 技術記事、製品の洞察、ケーススタディを学びます。
-   [PingCAP教育](https://www.pingcap.com/education/?from=en) : オンライン コースや認定プログラムを受講します。

### TiDB ユーザー名の長さ制限は何ですか? {#what-is-the-length-limit-for-the-tidb-user-name}

最大32文字。

### TiDB の列数と行サイズの制限は何ですか? {#what-are-the-limits-on-the-number-of-columns-and-row-size-in-tidb}

-   TiDB の列の最大数はデフォルトで 1017 に設定されています。この数は最大 4096 まで調整できます。
-   1行あたりの最大サイズはデフォルトで6MBです。最大120MBまで増やすことができます。

詳細については[TiDB の制限](/tidb-limitations.md)参照してください。

### TiDB は XA をサポートしていますか? {#does-tidb-support-xa}

いいえ。TiDBのJDBCドライバはMySQL Connector/Jです。Atomikosを使用する場合は、データソースを`type="com.mysql.jdbc.jdbc2.optional.MysqlXADataSource"`に設定してください。TiDBはMySQL JDBC XADataSourceとの接続をサポートしていません。MySQL JDBC XADataSourceはMySQLでのみ機能します（例：DMLを使用して`redo`ログを変更する場合）。

Atomikosの2つのデータソースを設定したら、JDBCドライブをXAに設定します。AtomikosがTMおよびRM（DB）を操作する際、AtomikosはXAを含むコマンドをJDBCレイヤーに送信します。MySQLを例に挙げると、JDBCレイヤーでXAが有効になっている場合、JDBCはDMLを使用して`redo`ログを変更するなど、一連のXAロジック操作をInnoDBに送信します。これは2相コミットの動作です。現在のTiDBバージョンは、上位アプリケーションレイヤーのJTA/XAをサポートしておらず、Atomikosから送信されたXA操作を解析しません。

スタンドアロン データベースとして、MySQL は XA を使用したデータベース間トランザクションのみを実装できます。一方、TiDB は Google Percolator トランザクション モデルを使用した分散トランザクションをサポートし、パフォーマンスの安定性は XA よりも高いため、TiDB は JTA/XA をサポートしておらず、TiDB が XA をサポートする必要もありません。

### TiDB は、パフォーマンスを損なうことなく、列指向storageエンジン (TiFlash) への大量の同時<code>INSERT</code>または<code>UPDATE</code>操作をどのようにサポートできるでしょうか? {#how-could-tidb-support-high-concurrent-code-insert-code-or-code-update-code-operations-to-the-columnar-storage-engine-tiflash-without-hurting-performance}

-   [TiFlash](/tiflash/tiflash-overview.md) 、列指向エンジンの変更を処理するために DeltaTree という特別な構造が導入されています。
-   TiFlash はRaftグループにおいて学習者として動作するため、ログコミットや書き込みの投票は行いません。つまり、DML 操作はTiFlashの確認応答を待つ必要がなく、そのためTiFlashによって OLTP パフォーマンスが低下することはありません。さらに、 TiFlashと TiKV は別々のインスタンスで動作するため、相互に影響を与えることはありません。

### TiFlash はどのような一貫性を提供しますか? {#what-kind-of-consistency-does-tiflash-provide}

TiFlashはデフォルトで強力なデータ整合性を維持します。ラフト学習プロセスがデータを更新します。また、クエリ内のデータがトランザクションと完全に整合していることを確認するためのTSOチェックも実行されます。詳細については、 [非同期レプリケーション](/tiflash/tiflash-overview.md#asynchronous-replication)と[一貫性](/tiflash/tiflash-overview.md#consistency)参照してください。

## TiDBテクニック {#tidb-techniques}

### データstorage用のTiKV {#tikv-for-data-storage}

[TiDB 内部 (I) - データストレージ](https://www.pingcap.com/blog/tidb-internal-data-storage/?from=en)参照。

### データコンピューティングのためのTiDB {#tidb-for-data-computing}

[TiDB 内部 (II) - コンピューティング](https://www.pingcap.com/blog/tidb-internal-computing/?from=en)参照。

### スケジュールのPD {#pd-for-scheduling}

[TiDB内部（III） - スケジューリング](https://www.pingcap.com/blog/tidb-internal-scheduling/?from=en)参照。
