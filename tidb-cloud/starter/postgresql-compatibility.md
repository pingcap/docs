---
title: PostgreSQL Compatibility
summary: PostgreSQL互換のTiDB Cloud StarterとPostgreSQLの互換性について、サポートされていない機能や動作の違いを含めて説明します。
---

# PostgreSQL Compatibility

PostgreSQL互換の{{{ .starter }}}インスタンスは、PostgreSQL wire protocol（pgwire v3）と、一般的なPostgreSQL SQL構文およびアプリケーションパターンをサポートします。ほとんどのPostgreSQLクライアント、ドライバー、ORMは、標準のPostgreSQL接続文字列を使用して接続できます。

ただし、この実装はPostgreSQLと同一ではありません。一部のPostgreSQL機能はサポートされていないか、動作が異なります。特に、PostgreSQL固有のストレージ、レプリケーション、拡張機能、またはトランザクションセマンティクスに依存する機能に違いがあります。

> **Note:**
>
> このページでは、PostgreSQL互換の{{{ .starter }}}インスタンスにおける一般的なPostgreSQL互換性について説明します。MySQL互換のTiDBクラスターには適用されません。
>
> パブリックプレビュー期間中は、互換性の対象範囲や動作が引き続き変わる可能性があります。本番ワークロードを移行する前に、アプリケーションが依存しているPostgreSQL機能を検証してください。

## サポートされる機能 {#supported-features}

PostgreSQL互換の{{{ .starter }}}インスタンスは、以下のPostgreSQL機能をサポートします。

+ **Wire protocol**: PostgreSQL wire protocol v3。Simple QueryおよびExtended Query（`Parse`/`Bind`/`Describe`/`Execute`）を含みます。
+ **DDL**: テーブル、B-tree、GIN、HNSWインデックス、ビュー、マテリアライズドビュー、スキーマ、シーケンス、関数、トリガー、型、照合順序に対する`CREATE`、`ALTER`、`DROP`。
+ **DML**: `RETURNING`付きの`INSERT`、`UPDATE`、`DELETE`、および`INSERT ... ON CONFLICT`（upsert）。
+ **Queries**: テーブル結合（inner、left、right、full outer、cross、lateral）、共通テーブル式（CTE）、再帰CTE、ウィンドウ関数、サブクエリ、集合演算（`UNION`、`INTERSECT`、`EXCEPT`）。
+ **Transactions**: `BEGIN`、`COMMIT`、`ROLLBACK`、savepoint、autocommit。
+ **Data types**: Boolean、integer、bigint、double precision、numeric、text、varchar、bytea、timestamp/timestamptz、date、time、interval、UUID、JSON/JSONB、配列、serial/bigserial、vector、tsvector、tsquery。
+ **PL/pgSQL**: 関数、プロシージャ、制御フロー、動的`EXECUTE`を、一部制限付きでサポートします。`WHILE`、`FOREACH`、カーソルはサポートされません。`EXCEPTION`およびネストされたブロックには`DO`ブロックが必要です。
+ **Triggers**: `INSERT`、`UPDATE`、`DELETE`に対する`BEFORE`および`AFTER`トリガーを、一部制限付きでサポートします。詳細は[Triggers](#triggers)を参照してください。
+ **Indexes**: B-tree（デフォルト）、GIN、部分インデックス、式インデックス、`CREATE INDEX CONCURRENTLY`、HNSWベクトルインデックス。GiST、Hash、SP-GiST、BRINインデックスはサポートされません。

## サポートされない機能 {#unsupported-features}

以下のPostgreSQL機能はサポートされていません。

+ `RANGE`、`LIST`、`HASH`パーティショニングを含むテーブルパーティショニング。
+ テーブル継承。
+ Foreign data wrapper（FDW）。
+ テーブルスペース。
+ `CREATE RULE`で作成されるルール。
+ 論理レプリケーション。
+ ストリーミングレプリケーション。
+ 真の`SERIALIZABLE`分離レベル。
+ `DEFERRABLE`トランザクション。
+ PostgreSQL large object（OIDベースのlarge objectストレージ）。代わりにバイナリデータには`BYTEA`を使用してください。
+ `XML`、`CIDR`、`MACADDR`データ型。
+ PostgreSQL range型（`INT4RANGE`の部分サポートを除く）。
+ PL/pgSQL以外の手続き言語（PL/Python、PL/Perl、PL/v8など）。
+ PL/pgSQLの`WHILE`ループ、`FOREACH`ループ、カーソル操作。
+ カスタムまたはサードパーティのPostgreSQL拡張機能。

## PostgreSQLとの違い {#differences-from-postgresql}

### トランザクション分離レベル {#transaction-isolation}

デフォルトのトランザクション分離レベルは`READ COMMITTED`です。`READ COMMITTED`と`REPEATABLE READ`がサポートされています。

`READ UNCOMMITTED`は、PostgreSQLの動作と同様に`READ COMMITTED`として動作します。

PostgreSQL Serializable Snapshot Isolation（SSI）はサポートされていません。PostgreSQL wire protocol経由で`SERIALIZABLE`を要求した場合、トランザクションは`REPEATABLE READ`にダウングレードされ、警告が返されます。

例:

```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;
SHOW transaction_isolation;
```

実際に有効な分離レベルは`REPEATABLE READ`です。

アプリケーションがPostgreSQLの`SERIALIZABLE`セマンティクスに依存している場合は、必要に応じてトランザクションロジックを見直し、再設計してください。明示的な行ロックやデータベース制約によって特定の不変条件を保護することはできますが、PostgreSQL Serializable Snapshot Isolation（SSI）のセマンティクスは提供されません。

### データ型 {#data-types}

一般的によく使われるPostgreSQLデータ型の多くはサポートされていますが、以下の型には互換性上の違いがあります。

| PostgreSQL型 | 動作 |
| --- | --- |
| `SMALLINT` / `INT2` | 受け付けられ、内部的には32ビット整数として保存されます。PostgreSQLの`SMALLINT`の範囲（-32768～32767）は強制されません。 |
| `REAL` / `FLOAT4` | 受け付けられ、内部的には`DOUBLE PRECISION`として保存されます。PostgreSQLの単精度浮動小数点のセマンティクスは保持されません。 |
| `CHAR(n)` / `CHARACTER(n)` | 受け付けられ、内部的には`VARCHAR`として保存されます。PostgreSQLのような空白埋めは行われないため、空白埋めされた文字列との比較で結果が異なる場合があります。 |
| `INET` | IPv4およびIPv6のホストまたはネットワークアドレスについて、等価比較と順序比較をサポートします。PostgreSQLのネットワーク固有の演算子や関数はサポートされません。 |
| `INT4RANGE` | 部分的にサポートされます。等価（`=`）および重なり（`&&`）演算子はサポートされます。包含演算子（`@>`および`<@`）はサポートされません。`upper()`や`isempty()`などのPostgreSQL rangeアクセサ関数は利用できないか、期待どおりに動作しません。 |
| Composite types | 宣言でき、テキストリテラルを使って書き込むこともできますが、値をフィールド単位で読み取ることはできません。 |
| `BIT` / `VARBIT` | 互換性上の違いを伴って受け付けられます。値は`BYTEA`のセマンティクスを使用し、宣言されたビット長は強制されません。長すぎる値は拒否または切り捨てされず、そのまま保持されます。`B'1010'`のようなPostgreSQLのビット文字列リテラルはサポートされません。 |
| Arrays | 1次元配列をサポートします。多次元配列はサポートされません。 |

以下のPostgreSQLデータ型はサポートされていません。

+ `XML`
+ `CIDR`
+ `MACADDR`
+ `MONEY`
+ `INT8RANGE`
+ `NUMRANGE`
+ `DATERANGE`
+ `TSRANGE`
+ `TSTZRANGE`

### DDLとスキーマの動作 {#ddl-and-schema-behavior}

一般的なPostgreSQL DDLの多くはサポートされていますが、一部の操作は異なります。

+ `CREATE TABLE AS`と`SELECT INTO`はサポートされていますが、作成されるテーブルには追加の`_rowid`主キー列が含まれ、`SELECT *`で表示されます。
+ `ALTER SEQUENCE`は、`OWNER TO`や`OWNED BY`などの所有権関連の操作のみをサポートします。`RESTART`、`INCREMENT BY`、`RENAME TO`を含むその他の句はサポートされません。シーケンスの現在値を変更するには、`setval()`を使用してください。
+ `TRUNCATE`は基本的な単一テーブル形式のみをサポートします。複数テーブルの`TRUNCATE`や、`CASCADE`、`RESTRICT`、`ONLY`、`RESTART IDENTITY`、`CONTINUE IDENTITY`などのオプション句はサポートされません。
+ 外部キーは、`CASCADE`、`SET NULL`、`SET DEFAULT`、`RESTRICT`、`NO ACTION`の参照アクションをサポートします。
+ 外部キー依存関係の扱いはPostgreSQLと異なります。参照先テーブルを、`CASCADE`または`RESTRICT`付きで削除した場合も含めて削除すると、孤立した外部キー制約が残ることがあります。これらの制約により、`pg_constraint`および`information_schema.referential_constraints`に対するクエリが失敗する可能性があります。この問題を避けるには、参照先テーブルを削除する前に、参照元の外部キー制約を削除してください。
+ 遅延外部キー検証はサポートされていません。`DEFERRABLE INITIALLY DEFERRED`で宣言された外部キー制約は受け付けられますが、トランザクションコミット時ではなく即時に検証されます。遅延外部キー検査に依存するアプリケーションでは、トランザクション失敗が発生する可能性があります。
+ enum型はサポートされますが、enum値は宣言順ではなくラベル文字列でソートされます。
+ PostgreSQLのテーブルパーティショニングとテーブル継承はサポートされていません。

> **Note:**
>
> すでに孤立した外部キー制約が存在する場合は、`ALTER TABLE ... DROP CONSTRAINT`を使用してその制約を削除するか、参照元テーブルを削除してください。同じ名前で参照先テーブルを再作成しても、元の外部キー依存関係は復元されません。

### インデックス {#indexes}

B-tree、GIN、HNSWインデックスアクセスメソッドがサポートされています。

一意インデックス、式インデックス、部分インデックス、`CREATE INDEX CONCURRENTLY`もサポートされています。

以下のPostgreSQLインデックスアクセスメソッドはサポートされていません。

+ GiST
+ Hash
+ SP-GiST
+ BRIN

HNSWは、ベクトルワークロード向けにサポートされる近似最近傍インデックス型です。追加の構造要件およびクエリ形状要件があります。

TiDB Cloudで提供されていないその他のpgvectorインデックス型（IVFFlatなど）は利用できません。

### `COPY` {#copy}

`COPY ... FROM STDIN`は、PostgreSQL wire protocol経由でtext形式およびCSV形式をサポートします。

以下のPostgreSQL `COPY`機能はサポートされていません。

+ バイナリ`COPY`
+ `COPY (SELECT ...) TO STDOUT`

### PL/pgSQL {#pl-pgsql}

PL/pgSQLは部分的にサポートされています。変数、代入、`SELECT INTO`、`IF`/`ELSIF`/`ELSE`、`FOR`ループ、`PERFORM`、`EXIT`、`CONTINUE`、`RAISE`、動的`EXECUTE`などの一般的な構文はサポートされています。

以下の制限があります。

+ `WHILE`ループはサポートされていません。
+ `FOREACH`ループはサポートされていません。
+ カーソルおよび`REFCURSOR`操作はサポートされていません。
+ `BEGIN ... EXCEPTION`による例外処理は、`DO`ブロック内でのみサポートされます。
+ ネストされた手続きブロックは、`DO`ブロック内でのみサポートされます。

> **Note:**
>
> 一部のPL/pgSQL文は、関数作成時ではなく、関数呼び出し時にのみ検証されます。そのため、関数にサポートされない構文が含まれていても、`CREATE FUNCTION`が成功する場合があります。
>
> 互換性を確認するには、作成後に関数を実行してテストしてください。

### Triggers {#triggers}

`INSERT`、`UPDATE`、`DELETE`に対する`BEFORE`および`AFTER`トリガーはサポートされていますが、以下の互換性上の違いがあります。

+ `BEFORE`トリガー関数では、ループ、PL/pgSQLの`CASE`文、動的`EXECUTE`、例外ハンドラー、ネストされたブロックを使用できません。
+ `FOR EACH STATEMENT`は受け付けられますが、PostgreSQLの文単位セマンティクスではなく、行単位セマンティクスで実行されます。
+ `AFTER`トリガーでは、単独の`RETURN NEW`または`RETURN OLD`は、その行の唯一の文として記述する必要があります。

### 拡張機能 {#extensions}

PostgreSQL互換の{{{ .starter }}}インスタンスは、事前定義された拡張機能セットと組み込み機能を提供します。

任意のカスタムまたはサードパーティのPostgreSQL拡張機能はインストールできません。TiDB Cloudが明示的にサポートする拡張機能のみ利用できます。

利用可能な拡張機能の一覧と、拡張機能固有の制限については、[PostgreSQL Extensions](/tidb-cloud/starter/pg-extensions-overview.md)を参照してください。

### レプリケーション {#replication}

PostgreSQLの論理レプリケーションおよびストリーミングレプリケーションはサポートされていません。

PostgreSQL互換性のために、一部のpublicationやreplication slotのカタログオブジェクトまたは関数が存在する場合がありますが、実際に動作するレプリケーションや変更データキャプチャ（CDC）は提供しません。`CREATE SUBSCRIPTION`はサポートされていません。

### システムカタログとツール {#system-catalogs-and-tooling}

PostgreSQL互換の{{{ .starter }}}インスタンスは、スキーマのイントロスペクションのために、一般的によく使われる`pg_catalog`および`information_schema`オブジェクトを実装しています。

カタログの表面仕様はPostgreSQLと同一ではありません。一部のカタログビュー、カラム、統計情報、およびPostgreSQL固有のサーバー関数は利用できないか、部分的にしか実装されていません。

PostgreSQL固有のカタログや統計情報の動作に依存するツールは、使用前に検証してください。

## 移行に関する考慮事項 {#migration-considerations}

既存の PostgreSQL アプリケーションを移行する前に、ワークロードが未サポートの機能、または動作が異なる機能に依存していないかを確認してください。該当するものには、以下が含まれます。

+ テーブルパーティショニングまたはテーブル継承。
+ Foreign Data Wrapper。
+ 論理レプリケーションまたはストリーミングレプリケーション。
+ `SERIALIZABLE` トランザクション分離レベル。
+ 未サポートの PostgreSQL データ型。
+ GiST、Hash、SP-GiST、BRIN を含む、未サポートのインデックスアクセスメソッド。
+ カスタムまたはサードパーティの PostgreSQL 拡張機能。
+ `WHILE` ループ、`FOREACH` ループ、カーソル、関数本体内の例外処理など、未サポートの PL/pgSQL 機能。

本番ワークロードを移行する前に、アプリケーションのスキーマとクエリを確認し、テストしてください。