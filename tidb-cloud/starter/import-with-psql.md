---
title: PostgreSQL から PostgreSQL 互換の TiDB Cloud Starter へ移行する
summary: "`psql` と `\\copy` を使用して、PostgreSQL から PostgreSQL 互換の TiDB Cloud Starter インスタンスへスキーマとデータを移行する方法を説明します。"
---

# PostgreSQL から PostgreSQL 互換の TiDB Cloud Starter へ移行する

このドキュメントでは、既存の PostgreSQL データベースを PostgreSQL 互換の {{{ .starter }}} インスタンスに移行する方法について説明します。

> **Note:**
>
> PostgreSQL 互換の {{{ .starter }}} は現在パブリックプレビューです。このプレビューは開発および評価を目的としており、本番ワークロードには推奨されません。
>
> パブリックプレビュー期間中、PostgreSQL 互換の {{{ .starter }}} は `psql` と `\copy` を使用した移行をサポートします。このガイドでは、ソース PostgreSQL データベースから `pg_dump` を使用してスキーマとデータをエクスポートし、ターゲットインスタンスへ `psql` と `\copy` を使用してインポートします。

移行全体の手順は次のとおりです。

1. ソースデータベース、ターゲットインスタンス、および移行ツールを準備します。
2. ソース PostgreSQL データベースの互換性を確認します。
3. ソーススキーマをエクスポートして確認します。
4. PostgreSQL 互換の {{{ .starter }}} インスタンスにスキーマをインポートします。
5. `psql` と `\copy` を使用してデータを移行します。
6. 移行後のスキーマとデータを検証します。

## 前提条件 {#prerequisites}

移行前に、次の項目を満たしていることを確認してください。

- ソース PostgreSQL データベースにアクセスできること。
- PostgreSQL 互換の {{{ .starter }}} インスタンスがあること。
- ターゲットインスタンスの接続文字列を取得していること。接続文字列を取得するには、TiDB Cloud コンソールでターゲットインスタンスを開き、**Connect** をクリックして **PostgreSQL CLI** を選択します。
- 移行コマンドを実行するマシンから、ソース PostgreSQL データベースとターゲットインスタンスの両方にネットワークアクセスできること。

移行前に、[PostgreSQLとの互換性](/tidb-cloud/starter/postgresql-compatibility.md) と [PostgreSQL 拡張機能](/tidb-cloud/starter/pg-extensions-overview.md) を確認してください。

## ツールを準備する {#prepare-tools}

移行を実行するマシンに、次の PostgreSQL クライアントツールをインストールします。

- `pg_dump`: ソース PostgreSQL データベースからスキーマとデータをエクスポートします。
- `psql`: PostgreSQL 互換の {{{ .starter }}} インスタンスにスキーマとデータをインポートします。

`pg_dump` は、ソース PostgreSQL データベースと同じ PostgreSQL メジャーリリースのバージョンを使用することを推奨します。

## PostgreSQL 互換性を確認する {#check-postgresql-compatibility}

PostgreSQL 互換の {{{ .starter }}} は一般的な PostgreSQL ワークロードをサポートしますが、一部の PostgreSQL 機能はサポートされていないか、動作が異なります。移行前に、ソースデータベースがこれらの機能に依存していないか確認してください。

### データベースロールと権限を確認する {#check-database-roles-and-permissions}

アプリケーションで行レベルセキュリティ（RLS）を使用している場合は、ソース PostgreSQL データベースで次のクエリを実行し、RLS ポリシーで参照されているロールを特定します。

```sql
SELECT DISTINCT r AS policy_role
FROM pg_policies, unnest(roles) AS r
WHERE r <> 'public';
```

スキーマをインポートする前に、必要なアプリケーションロールがターゲットインスタンスに作成されていることを確認してください。

### サポートされていないスキーマ機能を確認する {#check-unsupported-schema-features}

ソース PostgreSQL データベースに対して次のクエリを実行します。

```sql
-- Table partitioning
SELECT count(*) AS partitioned_tables
FROM pg_partitioned_table;

-- Table inheritance
SELECT count(*) AS inherited_tables
FROM pg_inherits;

-- Foreign data wrappers
SELECT count(*) AS fdw_servers
FROM pg_foreign_server;

-- Logical replication publications
SELECT count(*) AS publications
FROM pg_publication;
```

これらのクエリのいずれかが 0 以外の件数を返した場合は、移行前に影響を受けるオブジェクトを確認してください。

PostgreSQL 互換の {{{ .starter }}} は、テーブルパーティショニング、テーブル継承、外部データラッパー、および論理レプリケーションをサポートしていません。

### 遅延外部キー制約を確認する {#check-deferred-foreign-key-constraints}

PostgreSQL 互換の {{{ .starter }}} は、遅延外部キー検証をサポートしていません。`DEFERRABLE` として宣言された外部キー制約は即時に検証されます。

移行前に、ソース PostgreSQL データベースに対して次のクエリを実行し、遅延可能な外部キー制約を特定します。

```sql
SELECT
    conrelid::regclass AS table_name,
    conname AS constraint_name
FROM pg_constraint
WHERE contype = 'f'
  AND condeferrable;
```

移行前に、遅延外部キー検証に依存するアプリケーションのトランザクションを確認してください。

### 拡張機能を確認する {#check-extensions}

次のクエリを実行して、ソースデータベースにインストールされている拡張機能を一覧表示します。

```sql
SELECT extname
FROM pg_extension
ORDER BY extname;
```

結果を [PostgreSQL 拡張機能](/tidb-cloud/starter/pg-extensions-overview.md) と比較してください。

カスタムまたはサードパーティの PostgreSQL 拡張機能は、PostgreSQL 互換の {{{ .starter }}} にはインストールできません。移行前に、サポートされていない拡張機能への依存を削除または置き換えてください。

### PL/pgSQL を確認する {#check-pl-pgsql}

PostgreSQL 互換の {{{ .starter }}} は一般的な PL/pgSQL 構文をサポートしますが、一部の構文はサポートされていません。

次のクエリは、変更が必要になる可能性がある PL/pgSQL ルーチンを特定するのに役立ちます。

```sql
SELECT proname, prosrc
FROM pg_proc
WHERE prolang = (SELECT oid FROM pg_language WHERE lanname = 'plpgsql')
  AND (
    prosrc ~* '\m(WHILE|FOREACH|CURSOR|REFCURSOR)\M'
    OR prosrc ~* '\mEXCEPTION\s+WHEN\M'
    OR prosrc ~* '\mBEGIN\M.*\mBEGIN\M'
  );
```

移行前に、一致したルーチンを確認してください。特に次の点に注意してください。

- `WHILE` および `FOREACH` ループはサポートされていません。
- カーソルおよび `REFCURSOR` 操作はサポートされていません。
- `BEGIN ... EXCEPTION` を使用した例外処理は、`DO` ブロック内でのみサポートされます。
- ネストされた手続きブロックは、`DO` ブロック内でのみサポートされます。

互換性の詳細については、[PostgreSQLとの互換性](/tidb-cloud/starter/postgresql-compatibility.md) を参照してください。

## データベース全体を移行する {#migrate-a-full-database}

PostgreSQL データベースの移行では、データをインポートする前にスキーマをインポートします。

> **Important:**
>
> 通常どおり全体をダンプした `pg_dump` ファイルを、PostgreSQL 互換の {{{ .starter }}} に一度にインポートしないでください。通常の PostgreSQL ダンプでは、テーブルデータのロード後に主キーやその他の制約が追加されることがありますが、PostgreSQL 互換の {{{ .starter }}} では、空でないテーブルに主キーを追加できない場合があります。
>
> テーブルが空の状態で先にスキーマをインポートし、その後でデータをインポートしてください。
>
> この移行方法は、ゼロダウンタイム移行や論理レプリケーションをサポートしていません。最終移行とアプリケーション切り替えのために、メンテナンス時間を計画してください。
>
> 最終移行では、ソースデータベースに対するすべての書き込みとスキーマ変更を停止し、進行中の操作が完了するのを待ってから、スキーマとデータをエクスポートしてください。移行の検証とアプリケーション切り替えが完了するまで、ソースデータベースを変更しないでください。
>
> ソースへの書き込みを停止せずに試行移行を実施することはできますが、エクスポート開始後に行われた変更はターゲットデータベースに含まれない可能性があります。

### ステップ 1: スキーマをエクスポートする {#step-1-export-the-schema}

ソーススキーマをプレーン SQL 形式でエクスポートします。

```shell
pg_dump \
  --schema-only \
  --no-owner \
  --no-privileges \
  "<SOURCE_DATABASE_URL>" \
  > schema.sql
```

デフォルトのプレーン SQL 形式を使用してください。このワークフローでは、カスタム (`-Fc`) 形式またはディレクトリ (`-Fd`) 形式は使用しないでください。

### ステップ 2: スキーマを確認して更新する {#step-2-review-and-update-the-schema}

インポート前に、`schema.sql` に PostgreSQL の未サポート機能が含まれていないか確認します。

例えば、次のとおりです。

```shell
# Extensions
grep -i "CREATE EXTENSION" schema.sql

# Table partitioning
grep -Ei "PARTITION BY|PARTITION OF" schema.sql

# Table inheritance
grep -i "INHERITS" schema.sql

# Foreign data wrappers
grep -Ei "CREATE SERVER|CREATE FOREIGN TABLE" schema.sql

# Replication
grep -Ei "CREATE PUBLICATION|CREATE SUBSCRIPTION" schema.sql

# Rules
grep -i "CREATE RULE" schema.sql
```

スキーマをインポートする前に、未サポートの文を削除するか、書き換えてください。

また、未サポートのデータ型、インデックスアクセスメソッド、PL/pgSQL 構文、拡張機能についてもスキーマを確認してください。詳細は、[PostgreSQLとの互換性](/tidb-cloud/starter/postgresql-compatibility.md) を参照してください。

#### 行レベルセキュリティ {#row-level-security}

エクスポートしたスキーマには、`ENABLE ROW LEVEL SECURITY`、`FORCE ROW LEVEL SECURITY`、`CREATE POLICY` を含む行レベルセキュリティ（RLS）の文をそのまま残してください。

データをインポートする前に、`<TARGET_DATABASE_URL>` 内のロールに必要なテーブル権限があることを確認してください。このロールに RLS ポリシーが適用される場合、インポートされる各行は対象テーブルのポリシーを満たしている必要があります。そうでない場合、`COPY FROM STDIN` は `new row violates row-level security policy` で失敗します。

これらのポリシーによって拒否される行をインポートする必要がある場合は、RLS をバイパスする権限を持つ別の移行用ロールを使用して、データベース管理者にインポートを実行してもらってください。移行のためにアプリケーションロールへ `BYPASSRLS` を付与しないでください。移行専用に付与した権限は、完了後に削除してください。

`pg_dump` ユーティリティはデータベースロールをエクスポートしません。RLS ポリシーが特定のロールを参照している場合は、スキーマをインポートする前に、そのロールをターゲットインスタンスに作成してください。

例えば、次のとおりです。

```shell
psql "<TARGET_DATABASE_URL>" \
  -c "CREATE ROLE app_user LOGIN PASSWORD '<PASSWORD>'"
```

`--no-owner` オプションはオブジェクト所有権に関する文を省略し、`--no-privileges` は `GRANT` および `REVOKE` 文を省略します。

スキーマとデータをインポートした後、アプリケーションロールに必要なスキーマ、テーブル、シーケンスの権限、およびロールメンバーシップを復元してください。詳細は、[PostgreSQL の認証とロール](/tidb-cloud/starter/pg-auth-roles.md) を参照してください。

#### SERIAL と identity カラム {#serial-and-identity-columns}

`pg_dump` によって生成されたスキーマには、インポート前に調整が必要な、`SERIAL` のデフォルト値や identity カラムに関する PostgreSQL 固有の形式が含まれることがあります。

`SERIAL` または `BIGSERIAL` のデフォルト値については、`nextval()` 式から `::regclass` キャストを削除してください。例えば、次のとおりです。

```sql
-- PostgreSQL dump output
DEFAULT nextval('public.users_id_seq'::regclass)

-- Compatible form
DEFAULT nextval('public.users_id_seq')
```

ダンプに `ALTER TABLE ... ALTER COLUMN ... ADD GENERATED ... AS IDENTITY` によって追加された identity カラムが含まれている場合は、スキーマをインポートする前に、シーケンスと `DEFAULT nextval(...)` 式を使う形式に書き換えてください。

### ステップ 3: スキーマをインポートする {#step-3-import-the-schema}

確認済みのスキーマを、`psql` を使用してターゲットの PostgreSQL 互換の {{{ .starter }}} インスタンスにインポートします。

```shell
psql \
  "<TARGET_DATABASE_URL>" \
  -v ON_ERROR_STOP=1 \
  -f schema.sql
```

`ON_ERROR_STOP=1` オプションを指定すると、インポートエラーが発生した時点で `psql` が停止するため、未サポートの文を特定して修正しやすくなります。

### ステップ 4: データを移行する {#step-4-migrate-the-data}

スキーマのインポートが正常に完了したら、ソース PostgreSQL データベースからターゲットインスタンスへデータをストリーミングします。

```shell
pg_dump \
  --data-only \
  --no-owner \
  --no-privileges \
  "<SOURCE_DATABASE_URL>" \
  | psql "<TARGET_DATABASE_URL>" -v ON_ERROR_STOP=1
```

デフォルトでは、プレーンな `pg_dump` のデータストリームは PostgreSQL の `COPY` 文を使用します。このストリームを `psql` にパイプすると、`COPY ... FROM stdin` 文によって、PostgreSQL wire protocol 経由で PostgreSQL 互換の {{{ .starter }}} にデータがインポートされます。

PostgreSQL 互換の {{{ .starter }}} は、text および CSV 形式の `COPY` データ転送をサポートします。バイナリ `COPY` はサポートされていません。

### `\copy` を使用して個別のテーブルを移行する {#migrate-individual-tables-using-copy}

`psql` と `\copy` を使用して、個別のテーブルを移行することもできます。

ソース PostgreSQL データベースからテーブルをエクスポートするには、次のようにします。

```shell
psql "<SOURCE_DATABASE_URL>" \
  -c "\copy public.users TO 'users.csv' WITH (FORMAT csv, HEADER)"
```

テーブルをターゲットインスタンスにインポートするには、次のようにします。

```shell
psql "<TARGET_DATABASE_URL>" \
  -c "\copy public.users FROM 'users.csv' WITH (FORMAT csv, HEADER)"
```

データをインポートする前に、ターゲットテーブルが存在することを確認してください。

#### シーケンス値を復元する {#restore-sequence-values}

`\copy` を使用して個別のテーブルを移行する場合、シーケンス値は自動では転送されません。

テーブルで `SERIAL`、`BIGSERIAL`、または明示的に作成したシーケンスを使用している場合は、その後の挿入時に重複キーエラーを防ぐため、データのインポート後にシーケンスの状態を復元してください。

ソースへの書き込みを停止している間に、次のクエリをソース PostgreSQL データベースに対して実行し、シーケンスの状態を取得します。

```sql
SELECT last_value, is_called
FROM public.users_id_seq;
```

テーブルデータをインポートした後、`setval()` を使用してターゲットインスタンス内のシーケンス状態を復元します。

例えば、ソースシーケンスの `last_value = 3` かつ `is_called = true` の場合は、次を実行します。

```sql
SELECT setval('public.users_id_seq', 3, true);
```

値は、ソースデータベースから取得した実際の `last_value` と `is_called` の値に置き換えてください。

移行したテーブルに関連付けられている各シーケンスについて、この手順を繰り返してください。

> **Note:**
>
> SQL レベルの `COPY (SELECT ...) TO STDOUT` 構文はサポートされていません。代わりに、テーブル形式の `\copy` を使用してください。

## 移行したデータを検証する {#verify-the-migrated-data}

移行が完了したら、アプリケーショントラフィックを切り替える前にターゲットデータベースを検証してください。

### スキーマを検証する {#verify-the-schema}

`psql` を使用して移行後のスキーマを確認し、必要なテーブル、インデックス、制約、シーケンス、関数、その他のオブジェクトが存在することを検証します。

例えば、次のとおりです。

```shell
psql "<TARGET_DATABASE_URL>" -c "\dt"
```

### 行数を検証する {#verify-row-counts}

ソースデータベースとターゲットデータベースの行数を比較します。

例えば、次のとおりです。

```sql
SELECT count(*) FROM users;
SELECT count(*) FROM orders;
```

### シーケンスを検証する {#verify-sequences}

アプリケーションでシーケンス、`SERIAL`、または `BIGSERIAL` を使用している場合は、シーケンス値がインポート済みデータと整合していることを確認してください。

例えば、次のとおりです。

```sql
SELECT last_value FROM users_id_seq;
SELECT max(id) FROM users;
```

### アプリケーションを検証する {#verify-your-application}

アプリケーションを PostgreSQL 互換の {{{ .starter }}} インスタンスに接続し、アプリケーションのテストスイートを実行してください。

特に、未サポートであるか、動作が異なる PostgreSQL 機能に依存するアプリケーションロジックに注意してください。詳細は、[PostgreSQLとの互換性](/tidb-cloud/starter/postgresql-compatibility.md) を参照してください。

## 制限事項 {#limitations}

移行を計画する際は、次の制限事項に注意してください。

- パブリックプレビュー期間中、PostgreSQL 互換の {{{ .starter }}} は、`pg_dump` の `COPY` データストリームおよびテーブル形式の `\copy` を使った `psql` による移行をサポートします。
- PostgreSQL の論理レプリケーションとストリーミングレプリケーションはサポートされていません。最終移行では、スキーマとデータをエクスポートする前にソースへの書き込みを停止し、移行の検証とアプリケーションの切り替えが完了するまで停止したままにしてください。
- `COPY` プロトコルは text および CSV 形式をサポートします。バイナリ `COPY` はサポートされていません。
- SQL レベルの `COPY (SELECT ...) TO STDOUT` 構文はサポートされていません。個別テーブルの移行では、テーブル形式の `\copy` を使用してください。
- 一部の PostgreSQL スキーマオブジェクト、データ型、インデックスアクセスメソッド、拡張機能、PL/pgSQL 構文はサポートされていないか、動作が異なります。移行前に [PostgreSQLとの互換性](/tidb-cloud/starter/postgresql-compatibility.md) を確認してください。
- 移行されるテキストデータは、有効な UTF-8 エンコーディングを使用している必要があります。