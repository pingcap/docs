---
title: Known Incompatibility Issues with Third-Party Tools
summary: テスト中に発見されたサードパーティ ツールとの TiDB 互換性の問題について説明します。
aliases: ['/ja/tidb/stable/dev-guide-third-party-tools-compatibility/','/ja/tidbcloud/dev-guide-third-party-tools-compatibility/']
---

# サードパーティ製ツールとの既知の非互換性の問題 {#known-incompatibility-issues-with-third-party-tools}

> **注記：**
>
> [サポートされていない機能](/mysql-compatibility.md#unsupported-features)セクションには、次のものを含む、TiDB でサポートされていない機能がリストされています。
>
> -   ストアドプロシージャと関数
> -   トリガー
> -   イベント
> -   ユーザー定義関数
> -   `SPATIAL`関数、データ型、インデックス
> -   `XA`構文
>
> 上記のサポートされていない機能は想定される動作であり、このドキュメントには記載されていません。詳細については、 [MySQLの互換性](/mysql-compatibility.md)参照してください。

このドキュメントに記載されている非互換性の問題は、いくつかの[TiDBでサポートされているサードパーティツール](/develop/dev-guide-third-party-tools-compatibility.md)に見られます。

## 一般的な非互換性 {#general-incompatibility}

### <code>SELECT CONNECTION_ID()</code>はTiDBで64ビット整数を返します。 {#code-select-connection-id-code-returns-a-64-bit-integer-in-tidb}

**説明**

`SELECT CONNECTION_ID()`関数は、TiDB では`2199023260887`などの 64 ビット整数を返しますが、MySQL では`391650`などの 32 ビット整数を返します。

**回避方法**

TiDBアプリケーションでは、データオーバーフローを回避するために、 `SELECT CONNECTION_ID()`の結果を格納する際に64ビット整数型または文字列型を使用する必要があります。例えば、 Javaでは`Long`または`String`を使用し、JavaScriptまたはTypeScriptでは`string`使用できます。

### TiDBは<code>Com_*</code>カウンタを維持しません {#tidb-does-not-maintain-code-com-code-counters}

**説明**

MySQLは、データベースに対して実行された操作の合計数を追跡するために、 [`Com_`で始まるサーバーステータス変数](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Com_xxx)という一連の変数を保持しています。例えば、 `Com_select` MySQLが最後に起動されてから開始された`SELECT`のステートメントの合計数を記録します（ステートメントが正常に実行されなかった場合でも記録されます）。TiDBはこれらの変数を保持していません。TiDBとMySQLの違いを確認するには、 [`SHOW GLOBAL STATUS LIKE 'Com_%'`](/sql-statements/sql-statement-show-status.md)ステートメントを使用してください。

**回避方法**

これらの変数は使用しないでください。よくあるシナリオの一つは監視です。TiDBは監視性に優れているため、サーバーステータス変数からのクエリは必要ありません。監視サービスの詳細については、以下のドキュメントを参照してください。

-   TiDB Cloudドキュメント: [TiDBクラスタを監視する](/tidb-cloud/monitor-tidb-cluster.md) .
-   TiDB セルフマネージド ドキュメント: [TiDB 監視フレームワークの概要](/tidb-monitoring-framework.md) .

### TiDBはエラーメッセージで<code>TIMESTAMP</code>と<code>DATETIME</code>を区別します {#tidb-distinguishes-between-code-timestamp-code-and-code-datetime-code-in-error-messages}

**説明**

TiDBのエラーメッセージは`TIMESTAMP`と`DATETIME`を区別しますが、MySQLは区別せず、すべて`DATETIME`として返します。つまり、MySQLは`TIMESTAMP`タイプのエラーメッセージを誤って`DATETIME`タイプに変換します。

**回避方法**

文字列の照合にはエラーメッセージを使用しないでください。代わりに、トラブルシューティングには[エラーコード](/error-codes.md)使用してください。

### TiDBは<code>CHECK TABLE</code>文をサポートしていません {#tidb-does-not-support-the-code-check-table-code-statement}

**説明**

`CHECK TABLE`ステートメントは TiDB ではサポートされていません。

**回避方法**

データと対応するインデックスの一貫性をチェックするには、TiDB の[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを使用できます。

## MySQL JDBCとの互換性 {#compatibility-with-mysql-jdbc}

テストバージョンは MySQL Connector/J 8.0.29 です。

### デフォルトの照合順序が一貫していない {#the-default-collation-is-inconsistent}

**説明**

MySQL Connector/J の照合順序はクライアント側に保存され、サーバーバージョンによって区別されます。

次の表は、文字セットにおけるクライアント側とサーバー側の既知の照合順序の不一致を示しています。

| キャラクター    | クライアント側の照合順序         | サーバー側のデフォルトの照合順序 |
| --------- | -------------------- | ---------------- |
| `ascii`   | `ascii_general_ci`   | `ascii_bin`      |
| `latin1`  | `latin1_swedish_ci`  | `latin1_bin`     |
| `utf8mb4` | `utf8mb4_0900_ai_ci` | `utf8mb4_bin`    |

**回避方法**

照合順序は手動で設定し、クライアント側の照合順序に依存しないでください。クライアント側のデフォルトの照合順序は、MySQL Connector/J 構成ファイルに保存されます。

### <code>NO_BACKSLASH_ESCAPES</code>パラメータは効果がありません {#the-code-no-backslash-escapes-code-parameter-does-not-take-effect}

**説明**

TiDBでは、 `\`番目の文字をエスケープせずに`NO_BACKSLASH_ESCAPES`パラメータを使用することはできません。詳細については、 [問題](https://github.com/pingcap/tidb/issues/35302)を参照してください。

**回避方法**

TiDB では`NO_BACKSLASH_ESCAPES`と`\`を使用しないでください。SQL ステートメントでは`\\`使用してください。

### <code>INDEX_USED</code>関連のパラメータはサポートされていません {#the-code-index-used-code-related-parameters-are-not-supported}

**説明**

TiDBはプロトコルのパラメータ`SERVER_QUERY_NO_GOOD_INDEX_USED`と`SERVER_QUERY_NO_INDEX_USED`を設定しません。そのため、以下のパラメータが実際の状況と矛盾した値として返されます。

-   `com.mysql.cj.protocol.ServerSession.noIndexUsed()`
-   `com.mysql.cj.protocol.ServerSession.noGoodIndexUsed()`

**回避方法**

TiDB では`noIndexUsed()`および`noGoodIndexUsed()`関数を使用しないでください。

### <code>enablePacketDebug</code>パラメータはサポートされていません {#the-code-enablepacketdebug-code-parameter-is-not-supported}

**説明**

TiDBはパラメータ[パケットデバッグを有効にする](https://dev.mysql.com/doc/connector-j/en/connector-j-connp-props-debugging-profiling.html)をサポートしていません。これはMySQL Connector/Jのデバッグ用パラメータであり、データパケットのバッファを保持します。これにより、接続が予期せず切断される可能性があります。このパラメータを有効に**しないでください**。

**回避方法**

TiDB に`enablePacketDebug`パラメータを設定しないでください。

### UpdatableResultSetはサポートされていません {#the-updatableresultset-is-not-supported}

**説明**

TiDB は`UpdatableResultSet`サポートしていません。5 パラメータ`ResultSet.CONCUR_UPDATABLE`指定**しないでください**。また、 `ResultSet`内のデータを更新**しないでください**。

**回避方法**

トランザクションによるデータの一貫性を確保するには、 `UPDATE`ステートメントを使用してデータを更新できます。

## MySQL JDBC のバグ {#mysql-jdbc-bugs}

### <code>useLocalTransactionState</code>と<code>rewriteBatchedStatements</code>が同時にtrueの場合、トランザクションはコミットまたはロールバックに失敗します。 {#code-uselocaltransactionstate-code-and-code-rewritebatchedstatements-code-are-true-at-the-same-time-will-cause-the-transaction-to-fail-to-commit-or-roll-back}

**説明**

MySQL Connector/J 8.0.32 以前のバージョンを使用している場合、パラメータ`useLocalTransactionState`と`rewriteBatchedStatements`を同時に`true`に設定すると、トランザクションのコミットに失敗する可能性があります。 [このコード](https://github.com/Icemap/tidb-java-gitpod/tree/reproduction-local-transaction-state-txn-error)に設定すると再現します。

**回避方法**

> **注記：**
>
> `useConfigs=maxPerformance`は一連の設定が含まれています。MySQL Connector/J 8.0 および MySQL Connector/J 5.1 の詳細な設定については、それぞれ[mysql-コネクタ-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties)および[mysql-コネクタ-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)参照してください。 `maxPerformance`使用する場合は`useLocalTransactionState`無効にする必要があります。つまり、 `useConfigs=maxPerformance&useLocalTransactionState=false`使用してください。

このバグはMySQL Connector/J 8.0.33で修正されました。8.0.xシリーズのアップデートは終了しているため、安定性とパフォーマンスを向上させるためにMySQL Connector/Jを[最新の一般提供（GA）バージョン](https://dev.mysql.com/downloads/connector/j/)にアップグレードすることを強くお勧めします。

### コネクタは 5.7.5 より前のサーバーバージョンとは互換性がありません {#connector-is-incompatible-with-the-server-version-earlier-than-5-7-5}

**説明**

MySQL Connector/J 8.0.31 以前のバージョンを、MySQL サーバー 5.7.5 未満、または MySQL サーバー 5.7.5 未満のプロトコルを使用するデータベース（TiDB v6.3.0 未満など）で使用すると、特定の条件下でデータベース接続がハングすることがあります。詳細については、 [バグレポート](https://bugs.mysql.com/bug.php?id=106252)を参照してください。

**回避方法**

このバグはMySQL Connector/J 8.0.32で修正されました。8.0.xシリーズのアップデートは終了しているため、安定性とパフォーマンスを向上させるためにMySQL Connector/Jを[最新の一般提供（GA）バージョン](https://dev.mysql.com/downloads/connector/j/)にアップグレードすることを強くお勧めします。

TiDB では、次の方法でもこれを修正します。

-   クライアント側: このバグは**pingcap/mysql-connector-j**で修正されており、公式の MySQL Connector/J の代わりに[pingcap/mysql-connector-j](https://github.com/pingcap/mysql-connector-j)使用できます。
-   サーバー側: この互換性の問題は TiDB v6.3.0 以降で修正されており、サーバーをv6.3.0 以降のバージョンにアップグレードできます。

## Sequelizeとの互換性 {#compatibility-with-sequelize}

このセクションで説明する互換性情報は[シークエライズ v6.32.1](https://www.npmjs.com/package/sequelize/v/6.32.1)に基づいています。

テスト結果によると、TiDBはSequelizeのほとんどの機能をサポートしています（ [`MySQL`方言として使用する](https://sequelize.org/docs/v6/other-topics/dialect-specific-things/#mysql) ）。

サポートされていない機能は次のとおりです。

-   [`GEOMETRY`](https://github.com/pingcap/tidb/issues/6347)はサポートされていません。
-   整数主キーの変更はサポートされていません。
-   `PROCEDURE`はサポートされていません。
-   `READ-UNCOMMITTED`と`SERIALIZABLE` [分離レベル](/system-variables.md#transaction_isolation)はサポートされていません。
-   列の`AUTO_INCREMENT`属性の変更はデフォルトでは許可されません。
-   `FULLTEXT` 、 `HASH` 、 `SPATIAL`インデックスはサポートされていません。
-   `sequelize.queryInterface.showIndex(Model.tableName);`はサポートされていません。
-   `sequelize.options.databaseVersion`はサポートされていません。
-   [`queryInterface.addColumn`](https://sequelize.org/api/v6/class/src/dialects/abstract/query-interface.js~queryinterface#instance-method-addColumn)を使用した外部キ​​ー参照の追加はサポートされていません。

### 整数主キーの変更はサポートされていません {#modification-of-integer-primary-key-is-not-supported}

**説明**

整数型の主キーの変更はサポートされていません。TiDBは、主キーが整数型の場合、データ編成のインデックスとして主キーを使用します。詳細は[問題 #18090](https://github.com/pingcap/tidb/issues/18090)と[クラスター化インデックス](/clustered-indexes.md)を参照してください。

### <code>READ-UNCOMMITTED</code>および<code>SERIALIZABLE</code>分離レベルはサポートされていません {#the-code-read-uncommitted-code-and-code-serializable-code-isolation-levels-are-not-supported}

**説明**

TiDBは分離レベル`READ-UNCOMMITTED`と`SERIALIZABLE`をサポートしていません。分離レベルが`READ-UNCOMMITTED`または`SERIALIZABLE`に設定されている場合、TiDBはエラーをスローします。

**回避方法**

TiDB がサポートする分離レベル`REPEATABLE-READ`または`READ-COMMITTED`のみを使用します。

分離レベル`SERIALIZABLE`を設定し、分離レベル`SERIALIZABLE`に依存しない他のアプリケーションと TiDB の互換性を確保したい場合は、分離レベル[`tidb_skip_isolation_level_check`](/system-variables.md#tidb_skip_isolation_level_check)を`1`に設定してください。この場合、TiDB はサポートされていない分離レベルエラーを無視します。

### 列の<code>AUTO_INCREMENT</code>属性の変更はデフォルトでは許可されていません {#modification-of-a-column-s-code-auto-increment-code-attribute-is-not-allowed-by-default}

**説明**

デフォルトでは、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`コマンドを使用して列の`AUTO_INCREMENT`の属性を追加または削除することはできません。

**回避方法**

[`AUTO_INCREMENT`の制限](/auto-increment.md#restrictions)を参照してください。

`AUTO_INCREMENT`属性の削除を許可するには、 `@@tidb_allow_remove_auto_inc`を`true`に設定します。

### <code>FULLTEXT</code> 、 <code>HASH</code> 、 <code>SPATIAL</code>インデックスはサポートされていません {#code-fulltext-code-code-hash-code-and-code-spatial-code-indexes-are-not-supported}

**説明**

`FULLTEXT` 、 `HASH` 、 `SPATIAL`インデックスはサポートされていません。

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
