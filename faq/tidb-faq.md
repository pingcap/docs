---
title: TiDB FAQ
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB.
---

# TiDB FAQ {#tidb-faq}

<!-- markdownlint-disable MD026 -->

このドキュメントには、TiDBに関して最もよく寄せられる質問がリストされています。

## TiDBについて {#about-tidb}

### TiDBの紹介とアーキテクチャ {#tidb-introduction-and-architecture}

#### TiDBとは何ですか？ {#what-is-tidb}

TiDBは、水平方向のスケーラビリティ、高可用性、および一貫性のある分散トランザクションを特徴とする分散SQLデータベースです。また、MySQLのSQL構文とプロトコルを使用してデータを管理および取得することもできます。

#### TiDBのアーキテクチャは何ですか？ {#what-is-tidb-s-architecture}

TiDBクラスタには、TiDBサーバー、PD（配置Driver）サーバー、およびTiKVサーバーの3つのコンポーネントがあります。詳細については、 [TiDBアーキテクチャ](/tidb-architecture.md)を参照してください。

#### TiDBはMySQLに基づいていますか？ {#is-tidb-based-on-mysql}

いいえ。TiDBはMySQLの構文とプロトコルをサポートしていますが、PingCAP、Incによって開発および保守されている新しいオープンソースデータベースです。

#### TiDB、TiKV、PD（プレースメントDriver）のそれぞれの責任は何ですか？ {#what-is-the-respective-responsibility-of-tidb-tikv-and-pd-placement-driver}

-   TiDBはSQLコンピューティング層として機能し、主にSQLの解析、クエリプランの指定、およびエグゼキュータの生成を担当します。
-   TiKVは、実際のデータを格納するために使用される分散型Key-Valueストレージエンジンとして機能します。つまり、TiKVはTiDBのストレージエンジンです。
-   PDは、TiKVメタデータを管理し、タイムスタンプを割り当て、データの配置と負荷分散を決定するTiDBのクラスタマネージャーとして機能します。

#### TiDBは使いやすいですか？ {#is-it-easy-to-use-tidb}

はい、そうです。必要なすべてのサービスが開始されると、MySQLサーバーと同じくらい簡単にTiDBを使用できます。ほとんどの場合、コードを1行も変更せずに、MySQLをTiDBに置き換えて、アプリケーションを強化できます。人気のあるMySQL管理ツールを使用してTiDBを管理することもできます。

#### TiDBはMySQLとどのように互換性がありますか？ {#how-is-tidb-compatible-with-mysql}

現在、TiDBはMySQL 5.7構文の大部分をサポートしていますが、トリガー、ストアドプロシージャ、ユーザー定義関数、および外部キーはサポートしていません。詳細については、 [MySQLとの互換性](/mysql-compatibility.md)を参照してください。

#### TiDBは分散トランザクションをサポートしていますか？ {#does-tidb-support-distributed-transactions}

はい。 TiDBは、単一の場所にある少数のノードであろうと多数の[複数のデータセンターにまたがるノード](/multi-data-centers-in-one-city-deployment.md)であろうと、クラスタ全体にトランザクションを分散します。

Googleのパーコレーターに触発されたTiDBのトランザクションモデルは、主に2フェーズコミットプロトコルであり、いくつかの実用的な最適化が施されています。このモデルは、タイムスタンプアロケータに依存して、トランザクションごとに単調に増加するタイムスタンプを割り当てるため、競合を検出できます。 [PD](/tidb-architecture.md#placement-driver-pd-server)は、TiDBクラスタのタイムスタンプアロケータとして機能します。

#### TiDBを操作するために使用できるプログラミング言語は何ですか？ {#what-programming-language-can-i-use-to-work-with-tidb}

MySQLクライアントまたはドライバーでサポートされている任意の言語。

#### TiDBで他のKey-Valueストレージエンジンを使用できますか？ {#can-i-use-other-key-value-storage-engines-with-tidb}

はい。 TiKVに加えて、TiDBはUniStoreやMockTiKVなどのスタンドアロンストレージエンジンをサポートします。それ以降のTiDBリリースでは、MockTiKVはサポートされなくなる可能性があることに注意してください。

TiDBがサポートするすべてのストレージエンジンを確認するには、次のコマンドを使用します。

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

#### TiDBのドキュメントに加えて、TiDBの知識を習得する方法は他にありますか？ {#in-addition-to-the-tidb-documentation-are-there-any-other-ways-to-acquire-tidb-knowledge}

現在、 [TiDBドキュメント](/overview.md#tidb-introduction)は、TiDB関連の知識を取得するための最も重要でタイムリーな方法です。さらに、いくつかのテクニカルコミュニケーショングループもあります。必要な場合は、 [info@pingcap.com](mailto:info@pingcap.com)にお問い合わせください。

#### TiDBユーザー名の長さの制限は何ですか？ {#what-is-the-length-limit-for-the-tidb-user-name}

最大32文字。

#### TiDBはXAをサポートしていますか？ {#does-tidb-support-xa}

いいえ。TiDBのJDBCドライバーはMySQLJDBC（Connector / J）です。 Atomikosを使用する場合は、データソースを`type="com.mysql.jdbc.jdbc2.optional.MysqlXADataSource"`に設定します。 TiDBは、MySQLJDBCXADataSourceとの接続をサポートしていません。 MySQL JDBC XADataSourceはMySQLでのみ機能します（たとえば、DMLを使用して`redo`のログを変更します）。

Atomikosの2つのデータソースを構成した後、JDBCドライブをXAに設定します。 AtomikosがTMおよびRM（DB）を操作すると、AtomikosはXAを含むコマンドをJDBCレイヤーに送信します。 MySQLを例にとると、JDBCレイヤーでXAが有効になっている場合、JDBCはDMLを使用して`redo`のログを変更するなど、一連のXAロジック操作をInnoDBに送信します。これは、2フェーズコミットの操作です。現在のTiDBバージョンは、上位アプリケーション層のJTA / XAをサポートしておらず、Atomikosによって送信されたXA操作を解析しません。

スタンドアロンデータベースとして、MySQLはXAを使用してデータベース間トランザクションのみを実装できます。 TiDBはGooglePercolatorトランザクションモデルを使用した分散トランザクションをサポートし、そのパフォーマンスの安定性はXAよりも高いため、TiDBはXAをサポートせず、TiDBがXAをサポートする必要はありません。

### TiDBテクニック {#tidb-techniques}

#### データストレージ用のTiKV {#tikv-for-data-storage}

[TiDB内部（I）-データストレージ](https://en.pingcap.com/blog/tidb-internal-data-storage/)を参照してください。

#### データコンピューティング用のTiDB {#tidb-for-data-computing}

[TiDB内部（II）-コンピューティング](https://en.pingcap.com/blog/tidb-internal-computing/)を参照してください。

#### スケジューリングのためのPD {#pd-for-scheduling}

[TiDB内部（III）-スケジューリング](https://en.pingcap.com/blog/tidb-internal-scheduling/)を参照してください。

## クラウドへの展開 {#deployment-on-the-cloud}

### パブリッククラウド {#public-cloud}

#### 現在TiDBでサポートされているクラウドベンダーは何ですか？ {#what-cloud-vendors-are-currently-supported-by-tidb}

TiDBは、 [Google GKE](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-gcp-gke) 、および[AWS EKS](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-aws-eks)での展開をサポートし[アリババクラウドACK](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-on-alibaba-cloud) 。

さらに、TiDBは現在JD CloudとUCloudで利用可能であり、それらに第1レベルのデータベースエントリがあります。

## トラブルシューティング {#troubleshoot}

### TiDBカスタムエラーメッセージ {#tidb-custom-error-messages}

#### エラー8005（HY000）：書き込みの競合、txnStartTSが古くなっています {#error-8005-hy000-write-conflict-txnstartts-is-stale}

`tidb_disable_txn_auto_retry`が`on`に設定されているかどうかを確認します。その場合は、 `off`に設定します。すでに`off`の場合は、エラーが発生しなくなるまで`tidb_retry_limit`の値を増やします。

#### エラー9001（HY000）：PDサーバーのタイムアウト {#error-9001-hy000-pd-server-timeout}

PD要求のタイムアウト。 PDサーバーのステータス、監視データ、ログ、およびTiDBサーバーとPDサーバー間のネットワークを確認してください。

#### エラー9002（HY000）：TiKVサーバーのタイムアウト {#error-9002-hy000-tikv-server-timeout}

TiKV要求のタイムアウト。 TiKVサーバーのステータス、監視データ、ログ、およびTiDBサーバーとTiKVサーバー間のネットワークを確認してください。

#### エラー9003（HY000）：TiKVサーバーがビジーです {#error-9003-hy000-tikv-server-is-busy}

TiKVサーバーがビジーです。これは通常、データベースの負荷が非常に高い場合に発生します。 TiKVサーバーのステータス、監視データ、ログを確認してください。

#### エラー9004（HY000）：ロックタイムアウトを解決 {#error-9004-hy000-resolve-lock-timeout}

ロック解決タイムアウト。これは通常、トランザクションの競合が多数存在する場合に発生します。アプリケーションコードをチェックして、データベースにロックの競合が存在するかどうかを確認します。

#### エラー9005（HY000）：リージョンは利用できません {#error-9005-hy000-region-is-unavailable}

アクセスされたリージョンは利用できません。レプリカの数が不十分であるなどの理由により、Raftグループは利用できません。これは通常、TiKVサーバーがビジーであるか、TiKVノードがシャットダウンされている場合に発生します。 TiKVサーバーのステータス、監視データ、ログを確認してください。

#### エラー9006（HY000）：GCの寿命がトランザクション期間よりも短い {#error-9006-hy000-gc-life-time-is-shorter-than-transaction-duration}

`GC Life Time`の間隔が短すぎます。長いトランザクションで読み取られるはずだったデータが削除される可能性があります。次のコマンドを使用して[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)を調整できます。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_gc_life_time = '30m';
```

> **ノート：**
>
> 「30m」は、30分前に生成されたデータのみをクリーンアップすることを意味し、余分なストレージスペースを消費する可能性があります。

#### エラー9007（HY000）：書き込みの競合 {#error-9007-hy000-write-conflict}

`tidb_disable_txn_auto_retry`が`on`に設定されているかどうかを確認します。その場合は、 `off`に設定します。すでに`off`の場合は、エラーが発生しなくなるまで`tidb_retry_limit`の値を増やします。

#### エラー8130（HY000）：クライアントでマルチステートメント機能が無効になっています {#error-8130-hy000-client-has-multi-statement-capability-disabled}

このエラーは、以前のバージョンのTiDBからアップグレードした後に発生する可能性があります。 SQLインジェクション攻撃の影響を減らすために、TiDBは、デフォルトで同じ`COM_QUERY`の呼び出しで複数のクエリが実行されないようにしました。

システム変数[`tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-new-in-v4011)を使用して、この動作を制御できます。

### MySQLネイティブエラーメッセージ {#mysql-native-error-messages}

#### エラー2013（HY000）：クエリ中にMySQLサーバーへの接続が失われました {#error-2013-hy000-lost-connection-to-mysql-server-during-query}

-   panicがログにあるかどうかを確認します。
-   `dmesg -T | grep -i oom`を使用して、OOMがdmesgに存在するかどうかを確認します。
-   長時間アクセスできない場合も、このエラーが発生する可能性があります。これは通常、TCPタイムアウトが原因で発生します。 TCPが長期間使用されない場合、オペレーティングシステムはTCPを強制終了します。

#### エラー1105（HY000）：その他のエラー：不明なエラーワイヤーエラー（InvalidEnumValue（4004）） {#error-1105-hy000-other-error-unknown-error-wire-error-invalidenumvalue-4004}

このエラーは通常、TiDBのバージョンがTiKVのバージョンと一致しない場合に発生します。バージョンの不一致を回避するには、バージョンをアップグレードするときにすべてのコンポーネントをアップグレードします。

#### エラー1148（42000）：使用されているコマンドはこのTiDBバージョンでは許可されていません {#error-1148-42000-the-used-command-is-not-allowed-with-this-tidb-version}

`LOAD DATA LOCAL`ステートメントを実行したが、MySQLクライアントがこのステートメントの実行を許可していない場合（ `local_infile`オプションの値は0）、このエラーが発生します。

解決策は、MySQLクライアントを起動するときに`--local-infile=1`オプションを使用することです。たとえば、 `mysql --local-infile=1 -u root -h 127.0.0.1 -P 4000`のようなコマンドを使用します。デフォルト値の`local-infile`は、MySQLクライアントのバージョンによって異なるため、一部のMySQLクライアントで構成する必要があり、他のクライアントで構成する必要はありません。

#### エラー9001（HY000）：PDサーバーのタイムアウト開始タイムスタンプが安全ポイントより遅れる可能性があります {#error-9001-hy000-pd-server-timeout-start-timestamp-may-fall-behind-safe-point}

このエラーは、TiDBがPDにアクセスできない場合に発生します。 TiDBバックグラウンドのワーカーは、PDからセーフポイントを継続的にクエリします。このエラーは、100秒以内にクエリに失敗した場合に発生します。一般に、PDのディスクが低速でビジーであるか、TiDBとPDの間のネットワークに障害が発生したことが原因です。一般的なエラーの詳細については、 [エラー番号と障害診断](/error-codes.md)を参照してください。

### TiDBログエラーメッセージ {#tidb-log-error-messages}

#### EOFエラー {#eof-error}

クライアントまたはプロキシがTiDBから切断しても、TiDBは接続が切断されたことをすぐには認識しません。代わりに、TiDBは、接続にデータを返し始めたときにのみ切断に気付くことができます。このとき、ログにはEOFエラーが出力れます。
