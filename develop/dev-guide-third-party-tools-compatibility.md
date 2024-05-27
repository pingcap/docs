---
title: Known Incompatibility Issues with Third-Party Tools
summary: テスト中に見つかったサードパーティ ツールとの TiDB 互換性の問題について説明します。
---

# サードパーティツールとの既知の非互換性の問題 {#known-incompatibility-issues-with-third-party-tools}

> **注記：**
>
> [サポートされていない機能](/mysql-compatibility.md#unsupported-features)セクションには、TiDB でサポートされていない機能がリストされています。これには以下が含まれます。
>
> -   ストアドプロシージャと関数
> -   トリガー
> -   イベント
> -   ユーザー定義関数
> -   `SPATIAL`関数、データ型、インデックス
> -   `XA`構文
>
> 上記のサポートされていない機能は想定される動作であり、このドキュメントには記載されていません。詳細については、 [MySQL 互換性](/mysql-compatibility.md)参照してください。

このドキュメントに記載されている非互換性の問題は、いくつかの[TiDB がサポートするサードパーティ ツール](/develop/dev-guide-third-party-tools-compatibility.md)で見つかります。

## 一般的な非互換性 {#general-incompatibility}

### <code>SELECT CONNECTION_ID()</code> TiDBで64ビット整数を返します。 {#code-select-connection-id-code-returns-a-64-bit-integer-in-tidb}

**説明**

`SELECT CONNECTION_ID()`関数は、TiDB では`2199023260887`などの 64 ビット整数を返しますが、MySQL では`391650`などの 32 ビット整数を返します。

**回避方法**

TiDB アプリケーションでは、データのオーバーフローを回避するために、 `SELECT CONNECTION_ID()`の結果を格納するために 64 ビットの整数型または文字列型を使用する必要があります。たとえば、 Javaでは`Long`または`String`を使用し、JavaScript または TypeScript では`string`使用できます。

### TiDBは<code>Com_*</code>カウンタを維持しません {#tidb-does-not-maintain-code-com-code-counters}

**説明**

MySQL は、データベースで実行した操作の合計数を追跡するために、一連の[`Com_`で始まるサーバーステータス変数](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Com_xxx)維持します。たとえば、 `Com_select` 、MySQL が最後に起動されてから開始された`SELECT`のステートメントの合計数を記録します (ステートメントが正常にクエリされなかった場合でも)。TiDB はこれらの変数を維持しません。ステートメント[`SHOW GLOBAL STATUS LIKE 'Com_%'`](/sql-statements/sql-statement-show-status.md)を使用して、TiDB と MySQL の違いを確認できます。

**回避方法**

<CustomContent platform="tidb">

これらの変数は使用しないでください。一般的なシナリオの 1 つは監視です。TiDB は十分に監視可能であり、サーバーステータス変数からのクエリを必要としません。カスタム監視ツールについては、 [TiDB 監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

これらの変数は使用しないでください。一般的なシナリオの 1 つは監視です。TiDB TiDB Cloudは十分に監視可能であり、サーバーステータス変数からのクエリは必要ありません。TiDB TiDB Cloud監視サービスの詳細については、 [TiDBクラスタを監視する](/tidb-cloud/monitor-tidb-cluster.md)を参照してください。

</CustomContent>

### TiDBはエラーメッセージで<code>TIMESTAMP</code>と<code>DATETIME</code>を区別します {#tidb-distinguishes-between-code-timestamp-code-and-code-datetime-code-in-error-messages}

**説明**

TiDB エラー メッセージは`TIMESTAMP`と`DATETIME`を区別しますが、MySQL は区別せず、すべて`DATETIME`として返します。つまり、MySQL は`TIMESTAMP`タイプのエラー メッセージを誤って`DATETIME`タイプに変換します。

**回避方法**

<CustomContent platform="tidb">

文字列の一致にはエラー メッセージを使用しないでください。代わりに、トラブルシューティングには[エラーコード](/error-codes.md)使用してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

文字列の一致にはエラー メッセージを使用しないでください。代わりに、トラブルシューティングには[エラーコード](https://docs.pingcap.com/tidb/stable/error-codes)使用してください。

</CustomContent>

### TiDBは<code>CHECK TABLE</code>文をサポートしていません {#tidb-does-not-support-the-code-check-table-code-statement}

**説明**

`CHECK TABLE`ステートメントは TiDB ではサポートされていません。

**回避方法**

データと対応するインデックスの一貫性をチェックするには、TiDB の[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを使用できます。

## MySQL JDBC との互換性 {#compatibility-with-mysql-jdbc}

テストバージョンはMySQL Connector/J 8.0.29です。

### デフォルトの照合順序が一貫していません {#the-default-collation-is-inconsistent}

**説明**

MySQL Connector/J の照合順序はクライアント側に保存され、サーバーバージョンによって区別されます。

次の表は、文字セットにおけるクライアント側とサーバー側の既知の照合順序の不一致を示しています。

| キャラクター    | クライアント側のデフォルトの照合順序   | サーバー側のデフォルト照合順序 |
| --------- | -------------------- | --------------- |
| `ascii`   | `ascii_general_ci`   | `ascii_bin`     |
| `latin1`  | `latin1_swedish_ci`  | `latin1_bin`    |
| `utf8mb4` | `utf8mb4_0900_ai_ci` | `utf8mb4_bin`   |

**回避方法**

照合順序を手動で設定し、クライアント側のデフォルトの照合順序に依存しないでください。クライアント側のデフォルトの照合順序は、MySQL Connector/J 構成ファイルによって保存されます。

### <code>NO_BACKSLASH_ESCAPES</code>パラメータは有効になりません {#the-code-no-backslash-escapes-code-parameter-does-not-take-effect}

**説明**

TiDB では、 `\`文字をエスケープせずに`NO_BACKSLASH_ESCAPES`パラメータを使用することはできません。詳細については、 [問題](https://github.com/pingcap/tidb/issues/35302)を参照してください。

**回避方法**

TiDB では`NO_BACKSLASH_ESCAPES`と`\`を使用せず、SQL ステートメントでは`\\`使用します。

### <code>INDEX_USED</code>関連のパラメータはサポートされていません {#the-code-index-used-code-related-parameters-are-not-supported}

**説明**

TiDB はプロトコルの`SERVER_QUERY_NO_GOOD_INDEX_USED`と`SERVER_QUERY_NO_INDEX_USED`パラメータを設定しません。これにより、実際の状況と矛盾する次のパラメータが返されます。

-   `com.mysql.cj.protocol.ServerSession.noIndexUsed()`
-   `com.mysql.cj.protocol.ServerSession.noGoodIndexUsed()`

**回避方法**

TiDB では`noIndexUsed()`および`noGoodIndexUsed()`関数を使用しないでください。

### <code>enablePacketDebug</code>パラメータはサポートされていません {#the-code-enablepacketdebug-code-parameter-is-not-supported}

**説明**

TiDB は[パケットデバッグを有効にする](https://dev.mysql.com/doc/connector-j/en/connector-j-connp-props-debugging-profiling.html)パラメータをサポートしていません。これは、データ パケットのバッファを保持するデバッグ用 MySQL Connector/J パラメータです。これにより、接続が予期せず終了する可能性があります。オンに**しないでください**。

**回避方法**

TiDB で`enablePacketDebug`パラメータを設定しないでください。

### UpdatableResultSet はサポートされていません {#the-updatableresultset-is-not-supported}

**説明**

TiDB は`UpdatableResultSet`サポートしていません。5 パラメータを指定**しないでください**`ResultSet.CONCUR_UPDATABLE`また、 `ResultSet`内のデータを更新**しないでください**。

**回避方法**

トランザクションによるデータの一貫性を確保するには、 `UPDATE`ステートメントを使用してデータを更新できます。

## MySQL JDBC のバグ {#mysql-jdbc-bugs}

### <code>useLocalTransactionState</code>と<code>rewriteBatchedStatements</code>が同時にtrueの場合、トランザクションはコミットまたはロールバックに失敗します。 {#code-uselocaltransactionstate-code-and-code-rewritebatchedstatements-code-are-true-at-the-same-time-will-cause-the-transaction-to-fail-to-commit-or-roll-back}

**説明**

MySQL Connector/J 8.0.32 以前のバージョンを使用している場合、 `useLocalTransactionState`と`rewriteBatchedStatements`パラメータを同時に`true`に設定すると、トランザクションのコミットに失敗する可能性があります。 [このコード](https://github.com/Icemap/tidb-java-gitpod/tree/reproduction-local-transaction-state-txn-error)で再現できます。

**回避方法**

> **注記：**
>
> `useConfigs=maxPerformance`には、一連の設定が含まれています。MySQL Connector/J 8.0 および MySQL Connector/J 5.1 の詳細な設定については、それぞれ[mysql-コネクタ-j 8.0](https://github.com/mysql/mysql-connector-j/blob/release/8.0/src/main/resources/com/mysql/cj/configurations/maxPerformance.properties)および[mysql-コネクタ-j 5.1](https://github.com/mysql/mysql-connector-j/blob/release/5.1/src/com/mysql/jdbc/configs/maxPerformance.properties)を参照してください。 `maxPerformance`を使用する場合は`useLocalTransactionState`無効にする必要があります。つまり、 `useConfigs=maxPerformance&useLocalTransactionState=false`使用します。

このバグは MySQL Connector/J 8.0.33 で修正されました。8.0.x シリーズの更新が停止していることを考慮すると、安定性とパフォーマンスを向上させるために、MySQL Connector/J を[最新の一般提供（GA）バージョン](https://dev.mysql.com/downloads/connector/j/)にアップグレードすることを強くお勧めします。

### コネクタは 5.7.5 より前のサーバーバージョンと互換性がありません {#connector-is-incompatible-with-the-server-version-earlier-than-5-7-5}

**説明**

MySQL Connector/J 8.0.31 またはそれ以前のバージョンを MySQLサーバー&lt; 5.7.5 または MySQLサーバー&lt; 5.7.5 プロトコルを使用するデータベース (v6.3.0 より前の TiDB など) で使用すると、特定の条件下でデータベース接続がハングすることがあります。詳細については、 [バグレポート](https://bugs.mysql.com/bug.php?id=106252)参照してください。

**回避方法**

このバグは MySQL Connector/J 8.0.32 で修正されました。8.0.x シリーズの更新が停止していることを考慮すると、安定性とパフォーマンスを向上させるために、MySQL Connector/J を[最新の一般提供（GA）バージョン](https://dev.mysql.com/downloads/connector/j/)にアップグレードすることを強くお勧めします。

TiDB では、次の方法でもこれを修正します。

-   クライアント側: このバグは**pingcap/mysql-connector-j**で修正されており、公式の MySQL Connector/J の代わりに[pingcap/mysql-コネクタ-j](https://github.com/pingcap/mysql-connector-j)を使用できます。
-   サーバー側: この互換性の問題は TiDB v6.3.0 以降で修正されており、サーバーをv6.3.0 以降のバージョンにアップグレードできます。

## Sequelizeとの互換性 {#compatibility-with-sequelize}

このセクションで説明する互換性情報は[シークエライズ v6.32.1](https://www.npmjs.com/package/sequelize/v/6.32.1)に基づいています。

テスト結果によると、TiDBはSequelizeのほとんどの機能をサポートしています（ [`MySQL`方言として使用する](https://sequelize.org/docs/v6/other-topics/dialect-specific-things/#mysql) ）。

サポートされていない機能は次のとおりです:

-   [`GEOMETRY`](https://github.com/pingcap/tidb/issues/6347)はサポートされていません。
-   整数主キーの変更はサポートされていません。
-   `PROCEDURE`はサポートされていません。
-   `READ-UNCOMMITTED`と`SERIALIZABLE` [分離レベル](/system-variables.md#transaction_isolation)はサポートされていません。
-   列の`AUTO_INCREMENT`の属性の変更はデフォルトでは許可されません。
-   `FULLTEXT` `HASH` `SPATIAL`はサポートされていません。
-   `sequelize.queryInterface.showIndex(Model.tableName);`はサポートされていません。
-   `sequelize.options.databaseVersion`はサポートされていません。
-   [`queryInterface.addColumn`](https://sequelize.org/api/v6/class/src/dialects/abstract/query-interface.js~queryinterface#instance-method-addColumn)を使用した外部キ​​ー参照の追加はサポートされていません。

### 整数主キーの変更はサポートされていません {#modification-of-integer-primary-key-is-not-supported}

**説明**

整数主キーの変更はサポートされていません。主キーが整数型の場合、TiDB は主キーをデータ編成のインデックスとして使用します。詳細については、 [問題 #18090](https://github.com/pingcap/tidb/issues/18090)および[クラスター化インデックス](/clustered-indexes.md)を参照してください。

### <code>READ-UNCOMMITTED</code>および<code>SERIALIZABLE</code>分離レベルはサポートされていません {#the-code-read-uncommitted-code-and-code-serializable-code-isolation-levels-are-not-supported}

**説明**

TiDB は分離レベル`READ-UNCOMMITTED`および`SERIALIZABLE`サポートしていません。分離レベルが`READ-UNCOMMITTED`または`SERIALIZABLE`に設定されている場合、TiDB はエラーをスローします。

**回避方法**

TiDB がサポートする分離レベル`REPEATABLE-READ`または`READ-COMMITTED`のみを使用してください。

`SERIALIZABLE`分離レベルを設定するが`SERIALIZABLE`に依存しない他のアプリケーションと TiDB との互換性を確保したい場合は、 [`tidb_skip_isolation_level_check`](/system-variables.md#tidb_skip_isolation_level_check)を`1`に設定できます。この場合、 TiDB はサポートされていない分離レベル エラーを無視します。

### 列の<code>AUTO_INCREMENT</code>属性の変更はデフォルトでは許可されていません {#modification-of-a-column-s-code-auto-increment-code-attribute-is-not-allowed-by-default}

**説明**

デフォルトでは、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`コマンドを使用して列の`AUTO_INCREMENT`属性を追加または削除することはできません。

**回避方法**

[`AUTO_INCREMENT`の制限](/auto-increment.md#restrictions)を参照してください。

`AUTO_INCREMENT`属性の削除を許可するには、 `@@tidb_allow_remove_auto_inc`を`true`に設定します。

### <code>FULLTEXT</code> 、 <code>HASH</code> 、 <code>SPATIAL</code>インデックスはサポートされていません {#code-fulltext-code-code-hash-code-and-code-spatial-code-indexes-are-not-supported}

**説明**

`FULLTEXT` `HASH` `SPATIAL`はサポートされていません。
