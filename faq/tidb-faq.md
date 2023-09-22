---
title: TiDB Architecture FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB.
---

# TiDBアーキテクチャよくある質問 {#tidb-architecture-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントには、TiDB に関するよくある質問がリストされています。

## TiDB の概要とアーキテクチャ {#tidb-introduction-and-architecture}

### TiDBとは何ですか？ {#what-is-tidb}

<!-- Localization note for TiDB:

- English: use distributed SQL, and start to emphasize HTAP
- Chinese: can keep "NewSQL" and emphasize one-stop real-time HTAP ("一栈式实时 HTAP")
- Japanese: use NewSQL because it is well-recognized

-->

[TiDB](https://github.com/pingcap/tidb)は、ハイブリッド トランザクションおよび分析処理 (HTAP) ワークロードをサポートするオープンソースの分散 SQL データベースです。 MySQL と互換性があり、水平スケーラビリティ、強力な一貫性、高可用性を備えています。 TiDB の目標は、OLTP (オンライン トランザクション処理)、OLAP (オンライン分析処理)、および HTAP サービスをカバーするワンストップ データベース ソリューションをユーザーに提供することです。 TiDB は、高可用性と大規模データの強力な一貫性を必要とするさまざまなユースケースに適しています。

### TiDB のアーキテクチャとは何ですか? {#what-is-tidb-s-architecture}

TiDB クラスターには、TiDBサーバー、PD (配置Driver)サーバー、および TiKVサーバー の3 つのコンポーネントがあります。詳細については、 [TiDBアーキテクチャ](/tidb-architecture.md) 、 [TiDBstorage](/tidb-storage.md) 、 [TiDB コンピューティング](/tidb-computing.md) 、および[TiDB スケジューリング](/tidb-scheduling.md)を参照してください。

### TiDB は MySQL に基づいていますか? {#is-tidb-based-on-mysql}

いいえ。TiDB は MySQL 構文とプロトコルをサポートしていますが、PingCAP, Inc. によって開発および保守されている新しいオープン ソース データベースです。

### TiDB、TiKV、PD (配置Driver) のそれぞれの責任は何ですか? {#what-is-the-respective-responsibility-of-tidb-tikv-and-pd-placement-driver}

-   TiDB は SQL コンピューティングレイヤーとして機能し、主に SQL の解析、クエリ プランの指定、実行プログラムの生成を担当します。
-   TiKV は、実際のデータを保存するために使用される分散 Key-Valuestorageエンジンとして機能します。つまり、TiKV は TiDB のstorageエンジンです。
-   PD は TiDB のクラスター マネージャーとして機能し、TiKV メタデータを管理し、タイムスタンプを割り当て、データの配置と負荷分散に関する決定を行います。

### TiDBの使い方は簡単ですか？ {#is-it-easy-to-use-tidb}

はい、そうです。必要なサービスがすべて開始されると、MySQLサーバーと同じように簡単に TiDB を使用できるようになります。 MySQL を TiDB に置き換えることで、ほとんどの場合、コードを 1 行も変更することなくアプリケーションを強化できます。一般的な MySQL 管理ツールを使用して TiDB を管理することもできます。

### TiDB は MySQL とどのように互換性がありますか? {#how-is-tidb-compatible-with-mysql}

現在、TiDB はMySQL 5.7構文の大部分をサポートしていますが、トリガー、ストアド プロシージャ、およびユーザー定義関数はサポートしていません。詳細については、 [MySQLとの互換性](/mysql-compatibility.md)を参照してください。

### TiDB は分散トランザクションをサポートしていますか? {#does-tidb-support-distributed-transactions}

はい。 TiDB は、単一の場所にある少数のノードであっても、 [複数のデータセンターにわたるノード](/multi-data-centers-in-one-city-deployment.md)のノードであっても、クラスター全体にトランザクションを分散します。

Google の Percolator からインスピレーションを得た TiDB のトランザクション モデルは、主に 2 フェーズ コミット プロトコルであり、いくつかの実用的な最適化が施されています。このモデルは、タイムスタンプ アロケータに依存して各トランザクションに単調増加タイムスタンプを割り当てるため、競合を検出できます。 [PD](/tidb-architecture.md#placement-driver-pd-server) TiDB クラスター内のタイムスタンプ アロケーターとして機能します。

### TiDB を操作するにはどのようなプログラミング言語を使用できますか? {#what-programming-language-can-i-use-to-work-with-tidb}

MySQL クライアントまたはドライバーでサポートされている任意の言語。

### TiDB で他の Key-Valuestorageエンジンを使用できますか? {#can-i-use-other-key-value-storage-engines-with-tidb}

はい。 TiKV に加えて、TiDB は UniStore や MockTiKV などのスタンドアロンstorageエンジンをサポートします。今後の TiDB リリースでは、MockTiKV はサポートされなくなる可能性があることに注意してください。

TiDB がサポートするすべてのstorageエンジンを確認するには、次のコマンドを使用します。

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

### TiDB ドキュメント以外に、TiDB の知識を取得する方法はありますか? {#in-addition-to-the-tidb-documentation-are-there-any-other-ways-to-acquire-tidb-knowledge}

-   [TiDB ドキュメント](https://docs.pingcap.com/) : TiDB 関連の知識を得る最も重要かつタイムリーな方法。
-   [TiDB ブログ](https://www.pingcap.com/blog/) : 技術記事、製品に関する洞察、ケーススタディを学びます。
-   [PingCAP 教育](https://www.pingcap.com/education/?from=en) : オンラインコースと認定プログラムを受講します。

### TiDB ユーザー名の長さの制限は何ですか? {#what-is-the-length-limit-for-the-tidb-user-name}

最大 32 文字。

### TiDB の列数と行サイズの制限は何ですか? {#what-are-the-limits-on-the-number-of-columns-and-row-size-in-tidb}

-   TiDB の最大列数のデフォルトは 1017 です。この数は最大 4096 まで調整できます。
-   単一行の最大サイズのデフォルトは 6 MB です。最大 120 MB まで数値を増やすことができます。

詳細については、 [TiDB の制限事項](/tidb-limitations.md)を参照してください。

### TiDB は XA をサポートしていますか? {#does-tidb-support-xa}

いいえ。TiDB の JDBC ドライバーは MySQL Connector/J です。 Amitikos を使用する場合は、データ ソースを`type="com.mysql.jdbc.jdbc2.optional.MysqlXADataSource"`に設定します。 TiDB は、MySQL JDBC XADataSource との接続をサポートしていません。 MySQL JDBC XADataSource は MySQL でのみ機能します (たとえば、DML を使用して`redo`ログを変更する)。

Atomikos の 2 つのデータ ソースを構成したら、JDBC ドライブを XA に設定します。 Amitikos が TM と RM (DB) を操作する場合、Amitikos は XA を含むコマンドを JDBCレイヤーに送信します。 MySQL を例にとると、JDBCレイヤーで XA が有効になっている場合、JDBC は、DML を使用して`redo`ログを変更するなど、一連の XA ロジック操作を InnoDB に送信します。これが２相コミットの動作である。現在の TiDB バージョンは、上位アプリケーションレイヤーJTA/XA をサポートしておらず、Amitikos によって送信された XA オペレーションを解析しません。

スタンドアロン データベースとして、MySQL は XA を使用したデータベース間のトランザクションのみを実装できます。一方、TiDB は Google Percolator トランザクション モデルを使用した分散トランザクションをサポートしており、そのパフォーマンスの安定性は XA よりも高いため、TiDB は JTA/XA をサポートしておらず、TiDB が XA をサポートする必要はありません。

### TiDB は、パフォーマンスを損なうことなく、カラムナstorageエンジン (TiFlash) への大量の同時<code>INSERT</code>または<code>UPDATE</code>操作をどのようにサポートできるのでしょうか? {#how-could-tidb-support-high-concurrent-code-insert-code-or-code-update-code-operations-to-the-columnar-storage-engine-tiflash-without-hurting-performance}

-   [TiFlash](/tiflash/tiflash-overview.md)柱状エンジンの変更を処理するために、DeltaTree という特別な構造が導入されています。
-   TiFlash はRaftグループの学習者ロールとして機能するため、ログのコミットや書き込みに投票しません。これは、DML 操作がTiFlashの確認応答を待つ必要がないことを意味します。そのため、 TiFlashが OLTP のパフォーマンスを低下させません。さらに、 TiFlashと TiKV は別のインスタンスで動作するため、相互に影響しません。

### TiFlash はどのような一貫性を提供しますか? {#what-kind-of-consistency-does-tiflash-provide}

TiFlash はデフォルトで強力なデータ一貫性を維持します。 Raft 学習プロセスはデータを更新します。クエリ内のデータがトランザクションと完全に一致していることを確認するための TSO チェックもあります。詳細については、 [非同期レプリケーション](/tiflash/tiflash-overview.md#asynchronous-replication)および[一貫性](/tiflash/tiflash-overview.md#consistency)を参照してください。

## TiDB テクニック {#tidb-techniques}

### データstorage用の TiKV {#tikv-for-data-storage}

[TiDB 内部 (I) - データ ストレージ](https://www.pingcap.com/blog/tidb-internal-data-storage/?from=en)を参照してください。

### データコンピューティング用の TiDB {#tidb-for-data-computing}

[TiDB 内部 (II) - コンピューティング](https://www.pingcap.com/blog/tidb-internal-computing/?from=en)を参照してください。

### スケジューリング用PD {#pd-for-scheduling}

[TiDB 内部 (III) - スケジュール設定](https://www.pingcap.com/blog/tidb-internal-scheduling/?from=en)を参照してください。
