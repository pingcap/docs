---
title: Known Incompatibility Issues with Third-Party Tools
summary: Describes TiDB compatibility issues with third-party tools found during testing.
---

# サードパーティ製ツールとの既知の非互換性の問題 {#known-incompatibility-issues-with-third-party-tools}

> **ノート：**
>
> [サポートされていない機能](/mysql-compatibility.md#unsupported-features)番目のセクションには、次のような TiDB でサポートされていない機能がリストされています。
>
> -   ストアド プロシージャと関数
> -   トリガー
> -   イベント
> -   ユーザー定義関数
> -   `FOREIGN KEY`制約
> -   `SPATIAL`関数、データ型、インデックス
> -   `XA`構文
>
> 上記のサポートされていない機能は予想される動作であり、このドキュメントには記載されていません。詳細については、 [MySQL の互換性](/mysql-compatibility.md)を参照してください。

このドキュメントに記載されている非互換性の問題は、いくつかの[TiDB がサポートするサードパーティ ツール](/develop/dev-guide-third-party-tools-compatibility.md)に見られます。

## 一般的な非互換性 {#general-incompatibility}

### <code>SELECT CONNECTION_ID()</code> TiDB で 64 ビット整数を返します {#code-select-connection-id-code-returns-a-64-bit-integer-in-tidb}

**説明**

`SELECT CONNECTION_ID()`関数は、TiDB では`2199023260887`などの 64 ビット整数を返しますが、MySQL では`391650`などの 32 ビット整数を返します。

**回避方法**

TiDB アプリケーションでは、データのオーバーフローを回避するために、64 ビット整数型または文字列型を使用して`SELECT CONNECTION_ID()`の結果を格納する必要があります。たとえば、 Javaでは`Long`または`String`使用し、JavaScript または TypeScript では`string`を使用できます。

### TiDB は<code>Com_*</code>カウンターを維持しない {#tidb-does-not-maintain-code-com-code-counters}

**説明**

MySQL は一連の[`Com_`で始まるサーバーステータス変数](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Com_xxx)を維持して、データベースで実行した操作の総数を追跡します。たとえば、 `Com_select` 、MySQL が最後に開始されてから開始された`SELECT`のステートメントの合計数を記録します (ステートメントが正常にクエリされなかった場合でも)。 TiDB はこれらの変数を維持しません。ステートメント[`SHOW GLOBAL STATUS LIKE 'Com_%'`](/sql-statements/sql-statement-show-status.md)使用して、TiDB と MySQL の違いを確認できます。

**回避方法**

<CustomContent platform="tidb">

これらの変数は使用しないでください。一般的なシナリオの 1 つは監視です。 TiDB は十分に監視可能であり、サーバーステータス変数からクエリを実行する必要はありません。カスタム監視ツールについては、 [TiDB 監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

これらの変数は使用しないでください。一般的なシナリオの 1 つは監視です。 TiDB Cloudは十分に監視可能であり、サーバーステータス変数からクエリを実行する必要はありません。 TiDB Cloud監視サービスの詳細については、 [TiDBクラスタを監視する](/tidb-cloud/monitor-tidb-cluster.md)を参照してください。

</CustomContent>

### TiDB はエラー メッセージで<code>TIMESTAMP</code>と<code>DATETIME</code>を区別します {#tidb-distinguishes-between-code-timestamp-code-and-code-datetime-code-in-error-messages}

**説明**

TiDB のエラー メッセージでは`TIMESTAMP`と`DATETIME`が区別されますが、MySQL では区別されず、すべて`DATETIME`として返されます。つまり、MySQL は`TIMESTAMP`タイプのエラー メッセージを`DATETIME`タイプに誤って変換します。

**回避方法**

<CustomContent platform="tidb">

文字列の照合にエラー メッセージを使用しないでください。代わりに、トラブルシューティングには[エラーコード](/error-codes.md)を使用してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

文字列の照合にエラー メッセージを使用しないでください。代わりに、トラブルシューティングには[エラーコード](https://docs.pingcap.com/tidb/stable/error-codes)を使用してください。

</CustomContent>

### TiDB は<code>CHECK TABLE</code>ステートメントをサポートしていません {#tidb-does-not-support-the-code-check-table-code-statement}

**説明**

`CHECK TABLE`ステートメントは TiDB ではサポートされていません。

**回避方法**

データと対応するインデックスの整合性をチェックするには、TiDB で[`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md)ステートメントを使用できます。

## MySQL JDBC との互換性 {#compatibility-with-mysql-jdbc}

テスト バージョンは MySQL Connector/J 8.0.29 です。

### デフォルトの照合順序は矛盾しています {#the-default-collation-is-inconsistent}

**説明**

MySQL Connector/J の照合順序はクライアント側に保存され、サーバーのバージョンによって区別されます。

次の表に、文字セットにおける既知のクライアント側とサーバー側の照合順序順序の不一致を示します。

| キャラクター    | クライアント側のデフォルトの照合順序   | サーバー側のデフォルトの照合順序 |
| --------- | -------------------- | ---------------- |
| `ascii`   | `ascii_general_ci`   | `ascii_bin`      |
| `latin1`  | `latin1_swedish_ci`  | `latin1_bin`     |
| `utf8mb4` | `utf8mb4_0900_ai_ci` | `utf8mb4_bin`    |

**回避方法**

照合順序を手動で設定し、クライアント側のデフォルトの照合順序に依存しないでください。クライアント側のデフォルトの照合順序は、 MySQL Connector/J 構成ファイルによって保存されます。

### <code>NO_BACKSLASH_ESCAPES</code>パラメータが有効にならない {#the-code-no-backslash-escapes-code-parameter-does-not-take-effect}

**説明**

TiDB では、 `\`文字をエスケープせずに`NO_BACKSLASH_ESCAPES`パラメーターを使用することはできません。詳細については、この[問題](https://github.com/pingcap/tidb/issues/35302)を追跡してください。

**回避方法**

TiDB では`NO_BACKSLASH_ESCAPES`と`\`使用しないでください。ただし、SQL ステートメントでは`\\`使用してください。

### <code>INDEX_USED</code>関連のパラメーターはサポートされていません {#the-code-index-used-code-related-parameters-are-not-supported}

**説明**

TiDB は、プロトコルで`SERVER_QUERY_NO_GOOD_INDEX_USED`および`SERVER_QUERY_NO_INDEX_USED`パラメーターを設定しません。これにより、実際の状況と矛盾する以下のパラメーターが返されます。

-   `com.mysql.cj.protocol.ServerSession.noIndexUsed()`
-   `com.mysql.cj.protocol.ServerSession.noGoodIndexUsed()`

**回避方法**

TiDB で`noIndexUsed()`と`noGoodIndexUsed()`関数を使用しないでください。

### <code>enablePacketDebug</code>パラメータはサポートされていません {#the-code-enablepacketdebug-code-parameter-is-not-supported}

**説明**

TiDB は[enablePacketDebug](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-connp-props-debugging-profiling.html)パラメータをサポートしていません。これは、データ パケットのバッファを保持するデバッグに使用される MySQL Connector/J パラメータです。これにより、接続が予期せず閉じられる可能性があります。電源を入れ**ないでください**。

**回避方法**

TiDB で`enablePacketDebug`パラメータを設定しないでください。

### UpdatableResultSet はサポートされていません {#the-updatableresultset-is-not-supported}

**説明**

TiDB は`UpdatableResultSet`をサポートしていません。 `ResultSet.CONCUR_UPDATABLE`パラメータを指定したり、 `ResultSet`内のデータを更新し**たりしないで**<strong>ください</strong>。

**回避方法**

トランザクションごとのデータの整合性を確保するために、 `UPDATE`ステートメントを使用してデータを更新できます。

## MySQL JDBC のバグ {#mysql-jdbc-bugs}

### <code>useLocalTransactionState</code>と<code>rewriteBatchedStatements</code>が同時に true の場合、トランザクションのコミットまたはロールバックが失敗します。 {#code-uselocaltransactionstate-code-and-code-rewritebatchedstatements-code-are-true-at-the-same-time-will-cause-the-transaction-to-fail-to-commit-or-roll-back}

**説明**

`useLocalTransactionState`パラメーターと`rewriteBatchedStatements`パラメーターを同時に`true`に設定すると、トランザクションがコミットに失敗する可能性があります。 [このコード](https://github.com/Icemap/tidb-java-gitpod/tree/reproduction-local-transaction-state-txn-error)で再現できます。

**回避方法**

> **ノート：**
>
> このバグは MySQL JDBC に報告されています。プロセスを追跡するには、この[バグレポート](https://bugs.mysql.com/bug.php?id=108643)に従うことができます。

トランザクションがコミットまたはロールバックされなくなる可能性があるため、 `useLocalTransactionState`をオンに**しないでください**。

### コネクタは、5.7.5 より前のサーバーバージョンと互換性がありません {#connector-is-incompatible-with-the-server-version-earlier-than-5-7-5}

**説明**

MySQLサーバー&lt; 5.7.5 または MySQLサーバー&lt; 5.7.5 プロトコル (v6.3.0 より前の TiDB など) を使用するデータベースで MySQL Connector/J 8.0.29 を使用すると、特定の条件下でデータベース接続がハングすることがあります。詳細については、 [バグレポート](https://bugs.mysql.com/bug.php?id=106252)参照してください。

**回避方法**

これは既知の問題です。 2022 年 10 月 12 日現在、MySQL Connector/J はこの問題を修正していません。

TiDB は次の方法でこれを修正します。

-   クライアント側: このバグは**pingcap/mysql-connector-j**で修正されており、公式の MySQL Connector/J の代わりに[pingcap/mysql-connector-j](https://github.com/pingcap/mysql-connector-j)使用できます。
-   サーバー側: この互換性の問題は TiDB v6.3.0 以降で修正されており、サーバーをv6.3.0 以降のバージョンにアップグレードできます。

## Sequelize との互換性 {#compatibility-with-sequelize}

このセクションで説明する互換性情報は、 [Sequelize v6.21.4](https://www.npmjs.com/package/sequelize/v/6.21.4)に基づいています。

テスト結果によると、TiDB はほとんどの Sequelize 機能をサポートしています ( [`MySQL`方言として使用する](https://sequelize.org/docs/v6/other-topics/dialect-specific-things/#mysql) )。

サポートされていない機能は次のとおりです。

-   外部キー制約 (多対多の関係を含む) はサポートされていません。
-   [`GEOMETRY`](https://github.com/pingcap/tidb/issues/6347)はサポートされていません。
-   整数の主キーの変更はサポートされていません。
-   `PROCEDURE`はサポートされていません。
-   `READ-UNCOMMITTED`と`SERIALIZABLE` [分離レベル](/system-variables.md#transaction_isolation)はサポートされていません。
-   デフォルトでは、列の`AUTO_INCREMENT`属性の変更は許可されていません。
-   `FULLTEXT` 、 `HASH` 、および`SPATIAL`インデックスはサポートされていません。

### 整数の主キーの変更はサポートされていません {#modification-of-integer-primary-key-is-not-supported}

**説明**

整数の主キーの変更はサポートされていません。主キーが整数型の場合、TiDB は主キーをデータ編成のインデックスとして使用します。詳細については、 [問題 #18090](https://github.com/pingcap/tidb/issues/18090)と[クラスタ化インデックス](/clustered-indexes.md)を参照してください。

### <code>READ-UNCOMMITTED</code>および<code>SERIALIZABLE</code>分離レベルはサポートされていません {#the-code-read-uncommitted-code-and-code-serializable-code-isolation-levels-are-not-supported}

**説明**

TiDB は、 `READ-UNCOMMITTED`および`SERIALIZABLE`分離レベルをサポートしていません。分離レベルが`READ-UNCOMMITTED`または`SERIALIZABLE`に設定されている場合、TiDB はエラーをスローします。

**回避方法**

TiDB がサポートする分離レベル`REPEATABLE-READ`または`READ-COMMITTED`のみを使用してください。

TiDB を、分離レベル`SERIALIZABLE`を設定するが`SERIALIZABLE`に依存しない他のアプリケーションと互換性を持たせたい場合は、 [`tidb_skip_isolation_level_check`](/system-variables.md#tidb_skip_isolation_level_check)から`1`を設定できます。このような場合、TiDB はサポートされていない分離レベル エラーを無視します。

### デフォルトでは、列の<code>AUTO_INCREMENT</code>属性の変更は許可されていません {#modification-of-a-column-s-code-auto-increment-code-attribute-is-not-allowed-by-default}

**説明**

`ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`コマンドを使用して列の`AUTO_INCREMENT`属性を追加または削除することは、デフォルトでは許可されていません。

**回避方法**

[`AUTO_INCREMENT`の制限](/auto-increment.md#restrictions)を参照してください。

`AUTO_INCREMENT`属性の削除を許可するには、 `@@tidb_allow_remove_auto_inc`を`true`に設定します。

### <code>FULLTEXT</code> 、 <code>HASH</code> 、および<code>SPATIAL</code>インデックスはサポートされていません {#code-fulltext-code-code-hash-code-and-code-spatial-code-indexes-are-not-supported}

**説明**

`FULLTEXT` 、 `HASH` 、および`SPATIAL`インデックスはサポートされていません。
