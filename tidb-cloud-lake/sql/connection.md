---
title: Connection
summary: "{{{ .lake }}} における connection とは、外部ストレージサービスとやり取りするために必要な詳細をまとめた、指定済みの設定を指します。これは、アクセス認証情報、エンドポイント URL、ストレージタイプなどのパラメータを一元化して再利用できるセットとして機能し、{{{ .lake }}} とさまざまなストレージサービスとの統合を容易にします。"
---

# Connection

## Connection とは何ですか？ {#what-is-connection}

{{{ .lake }}} における connection とは、外部ストレージサービスとやり取りするために必要な詳細をまとめた、指定済みの設定を指します。これは、アクセス認証情報、エンドポイント URL、ストレージタイプなどのパラメータを一元化して再利用できるセットとして機能し、{{{ .lake }}} とさまざまなストレージサービスとの統合を容易にします。

Connection は、external stage、external table、および table の attach を作成する際に利用でき、{{{ .lake }}} を通じて外部ストレージサービスに保存されたデータを管理およびアクセスするための、簡潔でモジュール化された方法を提供します。

## Connection の管理 {#connection-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md) | 外部ストレージサービスへの新しい connection を作成します |
| [DROP CONNECTION](/tidb-cloud-lake/sql/drop-connection.md) | 既存の connection を削除します |

## Connection 情報 {#connection-information}

| コマンド | 説明 |
|---------|-------------|
| [DESCRIBE CONNECTION](/tidb-cloud-lake/sql/desc-connection.md) | 特定の connection の詳細を表示します |
| [SHOW CONNECTIONS](/tidb-cloud-lake/sql/show-connections.md) | 現在のデータベース内のすべての connection を一覧表示します |

### 使用例 {#usage-examples}

このセクションの例では、まず Amazon S3 に接続するために必要な認証情報を含む connection を作成します。続いて、この作成済みの connection を使用して external stage を作成し、既存の table を attach します。

次のステートメントは、必須の接続パラメータを指定して Amazon S3 への connection を開始します。

```sql
CREATE CONNECTION toronto
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

```

#### 例 1: Connection を使用した External Stage の作成 {#example-1-creating-external-stage-with-connection}

次の例では、前に定義した 'toronto' という名前の connection を使用して external stage を作成します。

```sql
CREATE STAGE my_s3_stage
    URL = 's3://lake-toronto'
    CONNECTION = (CONNECTION_NAME = 'toronto');

-- Equivalent to the following statement without using a connection:

CREATE STAGE my_s3_stage
    URL = 's3://lake-toronto'
    CONNECTION = (
        ACCESS_KEY_ID = '<your-access-key-id>',
        SECRET_ACCESS_KEY = '<your-secret-access-key>'
    );

```

#### 例 2: Connection を使用した Table の Attach {#example-2-attaching-table-with-connection}

[ATTACH TABLE](/tidb-cloud-lake/sql/attach-table.md) ページには、{{{ .lake }}} 内の新しい table を {{{ .lake }}} 内の既存の table に接続する方法を示す [例](/tidb-cloud-lake/sql/attach-table.md#examples) があります。データは "lake-toronto" という名前の Amazon S3 バケットに保存されています。各例では、Step 3 を、前に定義した 'toronto' という名前の connection を使用して簡略化できます。

```sql title='In {{{ .lake }}}:'
ATTACH TABLE employees_backup
    's3://lake-toronto/1/216/'
    CONNECTION = (CONNECTION_NAME = 'toronto');

```

```sql title='In {{{ .lake }}}:'
ATTACH TABLE population_readonly
    's3://lake-toronto/1/556/'
    CONNECTION = (CONNECTION_NAME = 'toronto')
    READ_ONLY;

```

#### 例 3: Connection を使用した External Table の作成 {#example-3-creating-external-table-with-connection}

この例では、前に定義した 'toronto' という名前の connection を使用して、'BOOKS' という名前の external table を作成する方法を示します。

```sql
CREATE TABLE BOOKS (
    id BIGINT UNSIGNED,
    title VARCHAR,
    genre VARCHAR DEFAULT 'General'
)
's3://lake-toronto'
CONNECTION = (CONNECTION_NAME = 'toronto');

```