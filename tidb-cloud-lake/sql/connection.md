---
title: Connection
summary: "{{{ .lake }}} における接続とは、外部ストレージサービスとやり取りするために必要な詳細をまとめた、指定済みの設定を指します。これは、アクセス認証情報、エンドポイント URL、ストレージタイプなどのパラメータを一元化して再利用できるセットとして機能し、{{{ .lake }}} とさまざまなストレージサービスとの統合を容易にします。"
---

# Connection

## Connection とは何ですか？ {#what-is-connection}

{{{ .lake }}} における接続とは、外部ストレージサービスとやり取りするために必要な詳細をまとめた、指定済みの設定を指します。これは、アクセス認証情報、エンドポイント URL、ストレージタイプなどのパラメータを一元化して再利用できるセットとして機能し、{{{ .lake }}} とさまざまなストレージサービスとの統合を容易にします。

Connection は、外部 stage や外部テーブルの作成、およびテーブルのアタッチに利用でき、{{{ .lake }}} を通じて外部ストレージサービスに保存されたデータを管理およびアクセスするための、簡潔でモジュール化された方法を提供します。

## Connection の管理 {#connection-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md) | 外部ストレージサービスへの新しい接続を作成します |
| [DROP CONNECTION](/tidb-cloud-lake/sql/drop-connection.md) | 既存の接続を削除します |

## Connection 情報 {#connection-information}

| コマンド | 説明 |
|---------|-------------|
| [DESCRIBE CONNECTION](/tidb-cloud-lake/sql/desc-connection.md) | 特定の接続の詳細を表示します |
| [SHOW CONNECTIONS](/tidb-cloud-lake/sql/show-connections.md) | 現在のデータベース内のすべての接続を一覧表示します |

### 使用例 {#usage-examples}

このセクションの例では、まず Amazon S3 に接続するために必要な認証情報を含む接続を作成します。続いて、この作成済みの接続を使用して外部 stage を作成し、既存のテーブルをアタッチします。

次のステートメントは、必須の接続パラメータを指定して Amazon S3 への接続を開始します。

```sql
CREATE CONNECTION toronto
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

```

#### 例 1: Connection を使用した外部 stage の作成 {#example-1-creating-external-stage-with-connection}

次の例では、前に定義した 'toronto' という名前の接続を使用して外部 stage を作成します。

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

#### 例 2: Connection を使用したテーブルのアタッチ {#example-2-attaching-table-with-connection}

[ATTACH TABLE](/tidb-cloud-lake/sql/attach-table.md) ページには、{{{ .lake }}} 内の新しいテーブルを {{{ .lake }}} 内の既存のテーブルに接続する方法を示す [例](/tidb-cloud-lake/sql/attach-table.md#examples) があります。データは "lake-toronto" という名前の Amazon S3 バケットに保存されています。各例では、ステップ 3 を、前に定義した 'toronto' という名前の接続を使用して簡略化できます。

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

#### 例 3: Connection を使用した外部テーブルの作成 {#example-3-creating-external-table-with-connection}

この例では、前に定義した 'toronto' という名前の接続を使用して、'BOOKS' という名前の外部テーブルを作成する方法を示します。

```sql
CREATE TABLE BOOKS (
    id BIGINT UNSIGNED,
    title VARCHAR,
    genre VARCHAR DEFAULT 'General'
)
's3://lake-toronto'
CONNECTION = (CONNECTION_NAME = 'toronto');

```