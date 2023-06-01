---
title: Known Incompatibility Issues with Third-Party Tools
summary: Describes TiDB compatibility issues with third-party tools found during testing.
---

# サードパーティツールとの既知の非互換性の問題 {#known-incompatibility-issues-with-third-party-tools}

> **ノート：**
>
> [<a href="/mysql-compatibility.md#unsupported-features">サポートされていない機能</a>](/mysql-compatibility.md#unsupported-features)セクションには、TiDB でサポートされていない次の機能がリストされています。
>
> -   ストアド プロシージャと関数
> -   トリガー
> -   イベント
> -   ユーザー定義関数
> -   `SPATIAL`関数、データ型、インデックス
> -   `XA`の構文
>
> 上記のサポートされていない機能は予期された動作であるため、このドキュメントには記載されていません。詳細については、 [<a href="/mysql-compatibility.md">MySQL の互換性</a>](/mysql-compatibility.md)を参照してください。

このドキュメントに記載されている非互換性の問題は、一部の[<a href="/develop/dev-guide-third-party-tools-compatibility.md">TiDB によってサポートされるサードパーティ ツール</a>](/develop/dev-guide-third-party-tools-compatibility.md)で発生します。

## 一般的な非互換性 {#general-incompatibility}

### <code>SELECT CONNECTION_ID()</code> TiDB の 64 ビット整数を返します {#code-select-connection-id-code-returns-a-64-bit-integer-in-tidb}

**説明**

`SELECT CONNECTION_ID()`関数は、TiDB では`2199023260887`などの 64 ビット整数を返しますが、MySQL では`391650`などの 32 ビット整数を返します。

**回避方法**

TiDB アプリケーションでは、データのオーバーフローを避けるために、 `SELECT CONNECTION_ID()`の結果を格納するために 64 ビットの整数または文字列型を使用する必要があります。たとえば、 Javaでは`Long`または`String`使用し、JavaScript または TypeScript では`string`を使用できます。

### TiDB は<code>Com_*</code>カウンターを維持しません {#tidb-does-not-maintain-code-com-code-counters}

**説明**

MySQL は、データベースに対して実行された操作の合計数を追跡するために、一連の[<a href="https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Com_xxx">`Com_`で始まるサーバーステータス変数</a>](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Com_xxx)維持します。たとえば、 `Com_select` 、(ステートメントが正常にクエリされなかった場合でも) MySQL が最後に起動されてから開始された`SELECT`のステートメントの合計数を記録します。 TiDB はこれらの変数を維持しません。ステートメント[<a href="/sql-statements/sql-statement-show-status.md">`SHOW GLOBAL STATUS LIKE 'Com_%'`</a>](/sql-statements/sql-statement-show-status.md)を使用すると、TiDB と MySQL の違いを確認できます。

**回避方法**

<CustomContent platform="tidb">

これらの変数は使用しないでください。一般的なシナリオの 1 つはモニタリングです。 TiDB は十分に観察可能であり、サーバーのステータス変数からクエリを実行する必要はありません。カスタム監視ツールについては、 [<a href="/tidb-monitoring-framework.md">TiDB モニタリング フレームワークの概要</a>](/tidb-monitoring-framework.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

これらの変数は使用しないでください。一般的なシナリオの 1 つはモニタリングです。 TiDB Cloudは十分に観察可能であり、サーバーのステータス変数からクエリを実行する必要はありません。 TiDB Cloud監視サービスの詳細については、 [<a href="/tidb-cloud/monitor-tidb-cluster.md">TiDBクラスタを監視する</a>](/tidb-cloud/monitor-tidb-cluster.md)を参照してください。

</CustomContent>

### TiDB はエラー メッセージで<code>TIMESTAMP</code>と<code>DATETIME</code>を区別します {#tidb-distinguishes-between-code-timestamp-code-and-code-datetime-code-in-error-messages}

**説明**

TiDB エラー メッセージは`TIMESTAMP`と`DATETIME`を区別しますが、MySQL は区別せず、すべて`DATETIME`として返します。つまり、MySQL は`TIMESTAMP`タイプのエラー メッセージを誤って`DATETIME`タイプに変換します。

**回避方法**

<CustomContent platform="tidb">

文字列の照合にエラー メッセージを使用しないでください。代わりに、トラブルシューティングには[<a href="/error-codes.md">エラーコード</a>](/error-codes.md)を使用してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

文字列の照合にエラー メッセージを使用しないでください。代わりに、トラブルシューティングには[<a href="https://docs.pingcap.com/tidb/stable/error-codes">エラーコード</a>](https://docs.pingcap.com/tidb/stable/error-codes)を使用してください。

</CustomContent>

### TiDB は<code>CHECK TABLE</code>ステートメントをサポートしていません {#tidb-does-not-support-the-code-check-table-code-statement}

**説明**

`CHECK TABLE`ステートメントは TiDB ではサポートされていません。

**回避方法**

データと対応するインデックスの一貫性をチェックするには、TiDB の[<a href="/sql-statements/sql-statement-admin-check-table-index.md">`ADMIN CHECK [TABLE|INDEX]`</a>](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを使用できます。

## MySQL JDBC との互換性 {#compatibility-with-mysql-jdbc}

テスト バージョンは MySQL Connector/J 8.0.29 です。

### デフォルトの照合順序が矛盾しています {#the-default-collation-is-inconsistent}

**説明**

MySQL Connector/J の照合順序はクライアント側に保存され、サーバーのバージョンによって区別されます。

次の表は、文字セットにおけるクライアント側とサーバー側の既知の照合順序順序の不一致を示しています。

| キャラクター    | クライアント側のデフォルトの照合順序   | サーバー側のデフォルトの照合順序 |
| --------- | -------------------- | ---------------- |
| `ascii`   | `ascii_general_ci`   | `ascii_bin`      |
| `latin1`  | `latin1_swedish_ci`  | `latin1_bin`     |
| `utf8mb4` | `utf8mb4_0900_ai_ci` | `utf8mb4_bin`    |

**回避方法**

照合順序を手動で設定し、クライアント側のデフォルトの照合照合順序に依存しないでください。クライアント側のデフォルトの照合順序は、 MySQL Connector/J 構成ファイルによって保存されます。

### <code>NO_BACKSLASH_ESCAPES</code>パラメータは有効になりません {#the-code-no-backslash-escapes-code-parameter-does-not-take-effect}

**説明**

TiDB では、 `\`文字をエスケープせずに`NO_BACKSLASH_ESCAPES`パラメータを使用することはできません。詳細については、この[<a href="https://github.com/pingcap/tidb/issues/35302">問題</a>](https://github.com/pingcap/tidb/issues/35302)を参照してください。

**回避方法**

TiDB では`NO_BACKSLASH_ESCAPES`と`\`使用せず、SQL ステートメントでは`\\`を使用してください。

### <code>INDEX_USED</code>関連パラメータはサポートされていません {#the-code-index-used-code-related-parameters-are-not-supported}

**説明**

TiDB はプロトコルの`SERVER_QUERY_NO_GOOD_INDEX_USED`および`SERVER_QUERY_NO_INDEX_USED`パラメータを設定しません。これにより、実際の状況と一致しない以下のパラメータが返されます。

-   `com.mysql.cj.protocol.ServerSession.noIndexUsed()`
-   `com.mysql.cj.protocol.ServerSession.noGoodIndexUsed()`

**回避方法**

TiDB では`noIndexUsed()`および`noGoodIndexUsed()`関数を使用しないでください。

### <code>enablePacketDebug</code>パラメータはサポートされていません {#the-code-enablepacketdebug-code-parameter-is-not-supported}

**説明**

TiDB は[<a href="https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-connp-props-debugging-profiling.html">パケットデバッグを有効にする</a>](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-connp-props-debugging-profiling.html)パラメータをサポートしていません。これは、データ パケットのバッファを保持するデバッグに使用される MySQL Connector/J パラメータです。これにより、接続が予期せず終了する可能性があります。電源を入れ**ないでください**。

**回避方法**

TiDB では`enablePacketDebug`パラメータを設定しないでください。

### UpdatableResultSet はサポートされていません {#the-updatableresultset-is-not-supported}

**説明**

TiDB は`UpdatableResultSet`をサポートしていません。 `ResultSet.CONCUR_UPDATABLE`パラメータを指定したり、 `ResultSet`内のデータを更新し**たりしないで****ください**。

**回避方法**

トランザクションごとにデータの一貫性を確保するには、 `UPDATE`ステートメントを使用してデータを更新します。

## MySQL JDBC のバグ {#mysql-jdbc-bugs}

### <code>useLocalTransactionState</code>と<code>rewriteBatchedStatements</code>同時に true の場合、トランザクションはコミットまたはロールバックに失敗します。 {#code-uselocaltransactionstate-code-and-code-rewritebatchedstatements-code-are-true-at-the-same-time-will-cause-the-transaction-to-fail-to-commit-or-roll-back}

**説明**

`useLocalTransactionState`と`rewriteBatchedStatements`パラメータを同時に`true`に設定すると、トランザクションのコミットに失敗する可能性があります。 [<a href="https://github.com/Icemap/tidb-java-gitpod/tree/reproduction-local-transaction-state-txn-error">このコード</a>](https://github.com/Icemap/tidb-java-gitpod/tree/reproduction-local-transaction-state-txn-error)で再現できます。

**回避方法**

> **ノート：**
>
> このバグは MySQL JDBC に報告されています。プロセスを追跡するには、この[<a href="https://bugs.mysql.com/bug.php?id=108643">バグレポート</a>](https://bugs.mysql.com/bug.php?id=108643)に従ってください。

`useLocalTransactionState`をオンにし**ないでください**。これにより、トランザクションのコミットまたはロールバックが妨げられる可能性があります。

### コネクタは 5.7.5 より前のサーバーバージョンと互換性がありません {#connector-is-incompatible-with-the-server-version-earlier-than-5-7-5}

**説明**

MySQLサーバー&lt; 5.7.5 プロトコルを使用するデータベース (v6.3.0 より前の TiDB など) を使用する場合、特定の条件下でデータベース接続がハングする場合があります。詳細については、 [<a href="https://bugs.mysql.com/bug.php?id=106252">バグレポート</a>](https://bugs.mysql.com/bug.php?id=106252)参照してください。

**回避方法**

これは既知の問題です。 2022 年 10 月 12 日の時点で、MySQL Connector/J はこの問題を修正していません。

TiDB は次の方法でこの問題を修正します。

-   クライアント側: このバグは**pingcap/mysql-connector-j**で修正されており、公式の MySQL Connector/J の代わりに[<a href="https://github.com/pingcap/mysql-connector-j">pingcap/mysql-connector-j</a>](https://github.com/pingcap/mysql-connector-j)使用できます。
-   サーバー側: この互換性の問題は TiDB v6.3.0 以降修正されており、サーバーをv6.3.0 以降のバージョンにアップグレードできます。

## Sequelizeとの互換性 {#compatibility-with-sequelize}

このセクションで説明する互換性情報は[<a href="https://www.npmjs.com/package/sequelize/v/6.21.4">シークライズ v6.21.4</a>](https://www.npmjs.com/package/sequelize/v/6.21.4)に基づいています。

テスト結果によると、TiDB は Sequelize 機能のほとんどをサポートしています ( [<a href="https://sequelize.org/docs/v6/other-topics/dialect-specific-things/#mysql">`MySQL`方言として使用する</a>](https://sequelize.org/docs/v6/other-topics/dialect-specific-things/#mysql) )。

サポートされていない機能は次のとおりです。

-   [<a href="https://github.com/pingcap/tidb/issues/6347">`GEOMETRY`</a>](https://github.com/pingcap/tidb/issues/6347)はサポートされていません。
-   整数の主キーの変更はサポートされていません。
-   `PROCEDURE`はサポートされていません。
-   `READ-UNCOMMITTED`と`SERIALIZABLE` [<a href="/system-variables.md#transaction_isolation">分離レベル</a>](/system-variables.md#transaction_isolation)はサポートされていません。
-   デフォルトでは、列の`AUTO_INCREMENT`属性の変更は許可されていません。
-   `FULLTEXT` 、 `HASH` 、および`SPATIAL`インデックスはサポートされていません。

### 整数の主キーの変更はサポートされていません {#modification-of-integer-primary-key-is-not-supported}

**説明**

整数の主キーの変更はサポートされていません。 TiDB は、主キーが整数型の場合、主キーをデータ編成のインデックスとして使用します。詳細については、 [<a href="https://github.com/pingcap/tidb/issues/18090">問題 #18090</a>](https://github.com/pingcap/tidb/issues/18090)と[<a href="/clustered-indexes.md">クラスター化インデックス</a>](/clustered-indexes.md)を参照してください。

### <code>READ-UNCOMMITTED</code>および<code>SERIALIZABLE</code>分離レベルはサポートされていません {#the-code-read-uncommitted-code-and-code-serializable-code-isolation-levels-are-not-supported}

**説明**

TiDB は、 `READ-UNCOMMITTED`および`SERIALIZABLE`分離レベルをサポートしていません。分離レベルが`READ-UNCOMMITTED`または`SERIALIZABLE`に設定されている場合、TiDB はエラーをスローします。

**回避方法**

TiDB がサポートする分離レベル ( `REPEATABLE-READ`または`READ-COMMITTED`のみを使用します。

分離レベル`SERIALIZABLE`を設定するが`SERIALIZABLE`に依存しない他のアプリケーションと TiDB に互換性を持たせたい場合は、 [<a href="/system-variables.md#tidb_skip_isolation_level_check">`tidb_skip_isolation_level_check`</a>](/system-variables.md#tidb_skip_isolation_level_check)から`1`に設定できます。このような場合、TiDB はサポートされていない分離レベルのエラーを無視します。

### デフォルトでは、列の<code>AUTO_INCREMENT</code>属性の変更は許可されていません {#modification-of-a-column-s-code-auto-increment-code-attribute-is-not-allowed-by-default}

**説明**

デフォルトでは、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`コマンドを使用して列の`AUTO_INCREMENT`属性を追加または削除することはできません。

**回避方法**

[<a href="/auto-increment.md#restrictions">`AUTO_INCREMENT`の制限事項</a>](/auto-increment.md#restrictions)を参照してください。

`AUTO_INCREMENT`属性の削除を許可するには、 `@@tidb_allow_remove_auto_inc`を`true`に設定します。

### <code>FULLTEXT</code> 、 <code>HASH</code> 、および<code>SPATIAL</code>インデックスはサポートされていません {#code-fulltext-code-code-hash-code-and-code-spatial-code-indexes-are-not-supported}

**説明**

`FULLTEXT` 、 `HASH` 、および`SPATIAL`インデックスはサポートされていません。
