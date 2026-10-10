---
title: stage の概要
summary: stage は、データファイルが存在する仮想的な場所です。stage 内のファイルは直接クエリすることも、テーブルにロードすることもできます。あるいは、テーブルからデータをファイルとして stage にアンロードすることもできます。
---

# stage の概要

{{{ .lake }}} では、stage はデータファイルが存在する仮想的な場所です。stage 内のファイルは直接クエリすることも、テーブルにロード (load) することもできます。あるいは、テーブルからデータをファイルとして stage にアンロード (unload) することもできます。stage を使用する利点は、コンピュータ上のフォルダと同じような手軽さで、データのロードやアンロードのためにアクセスできることです。フォルダにファイルを置くときと同様に、ハードディスク上の正確な保存場所を必ずしも知っている必要はありません。stage 内のファイルにアクセスする際は、オブジェクトストレージのバケット内での場所を指定する代わりに、`@mystage/mydatafile.csv` のように、stage 名とファイル名だけを指定すれば十分です。コンピュータ上のフォルダと同様に、{{{ .lake }}} では必要な数だけ stage を作成できます。ただし、stage の中に別の stage を含めることはできない点に注意してください。各 stage は独立して動作し、他の stage を内包しません。

データのロードに stage を利用すると、データファイルのアップロード、管理、フィルタリングの効率も向上します。[LakeSQL](/tidb-cloud-lake/guides/connect-using-lakesql.md) を使用すると、1 つのコマンドで stage へのファイルのアップロードや、stage からのファイルのダウンロードを簡単に行えます。{{{ .lake }}} にデータをロードする際は、COPY INTO コマンドで stage を直接指定でき、その stage からデータファイルを読み取り、さらにフィルタリングすることも可能です。同様に、{{{ .lake }}} からデータをエクスポートする際は、データファイルを stage にダンプできます。

## stage の種類 {#stage-types}

実際の保存場所とアクセス性に基づいて、stage は Internal Stage、External Stage、User Stage の 3 種類に分類できます。次の表は、{{{ .lake }}} における各 stage 種類の特徴を、保存場所、アクセス性、推奨される利用シナリオの観点からまとめたものです。

|                      | ユーザー stage                         | 内部 stage                                   | 外部 stage                                                                                                |
|----------------------|------------------------------------|--------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| **保存場所** | 内部オブジェクトストレージ ({{{ .lake }}}) | 内部オブジェクトストレージ ({{{ .lake }}})               | 外部オブジェクトストレージ (例: S3, Azure)                                                                     |
| **作成方法**  | 自動的に作成される              | 手動で作成: `CREATE STAGE stage_name;` | 手動で作成: `CREATE STAGE stage_name` `'s3://bucket/prefix/'` `CONNECTION=(endpoint_url='x', ...);` |
| **アクセス制御**   | ユーザー本人のみアクセス可能        | 他のユーザーまたはロールと共有可能          | 他のユーザーまたはロールと共有可能                                                                       |
| **stage の削除**       | 不可                        | stage を削除し、その中のファイルも消去する         | stage のみを削除し、外部ロケーション内のファイルは保持される                                           |
| **ファイルのアップロード**      | ファイルを {{{ .lake }}} にアップロードする必要がある      | ファイルを {{{ .lake }}} にアップロードする必要がある                    | アップロード不要。外部ストレージとの間でデータの読み取りまたはアンロードに使用する                                        |
| **利用シナリオ**   | 個人用 / 非公開データ              | チーム用 / 共有データ                                 | 外部データ統合またはアンロード                                                                        |
| **パス形式**      | `@~/`                              | `@stage_name/`                                   | `@stage_name/`                                                                                                |

### Internal Stage {#internal-stage}

Internal Stage 内のファイルは、実際には {{{ .lake }}} が存在するオブジェクトストレージに保存されます。Internal Stage は組織内のすべてのユーザーが利用でき、各ユーザーは自分のデータロードやエクスポート作業にその stage を使用できます。フォルダを作成するのと同様に、stage を作成する際には名前の指定が必要です。以下は、[CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) コマンドを使用して Internal Stage を作成する例です。

```sql
-- Create an internal stage named my_internal_stage
CREATE STAGE my_internal_stage;
```

### External Stage {#external-stage}

External Stage を使用すると、{{{ .lake }}} が存在する場所の外部にあるオブジェクトストレージの場所を指定できます。たとえば、Google Cloud Storage コンテナにデータセットがある場合、そのコンテナを使って External Stage を作成できます。External Stage を作成する際には、{{{ .lake }}} がその外部ロケーションに接続するための接続情報を指定する必要があります。

以下は External Stage を作成する例です。ここでは、`lake-doc` という名前の Amazon S3 バケットにデータセットがあるとします。

[CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) コマンドを使用して、{{{ .lake }}} をそのバケットに接続する External Stage を作成できます。

```sql
-- Create an external stage named my_external_stage
CREATE STAGE my_external_stage
    URL = 's3://lake-doc'
    CONNECTION = (
        ACCESS_KEY_ID = '<YOUR-KEY-ID>',
        SECRET_ACCESS_KEY = '<YOUR-SECRET-KEY>'
    );
```

External Stage を作成すると、{{{ .lake }}} からそのデータセットにアクセスできます。たとえば、ファイルを一覧表示するには次のようにします。

```sql
LIST @my_external_stage;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│      name     │  size  │                 md5                │         last_modified         │      creator     │
├───────────────┼────────┼────────────────────────────────────┼───────────────────────────────┼──────────────────┤
│ Inventory.csv │  57585 │ "0cd02fb636a22ba9f4ae4d24555a7d68" │ 2024-03-17 21:22:38.000 +0000 │ NULL             │
│ Products.csv  │  42987 │ "570e5cbf6a4b6e7e9a258094192f4784" │ 2024-03-17 21:22:38.000 +0000 │ NULL             │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

外部ストレージは、{{{ .lake }}} がサポートするオブジェクトストレージソリューションのいずれかである必要がある点に注意してください。[CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) コマンドのページには、一般的によく使われるオブジェクトストレージソリューション向けの接続情報の指定例が記載されています。

### User Stage {#user-stage}

User Stage は、特殊な種類の Internal Stage と考えることができます。User Stage 内のファイルは {{{ .lake }}} が存在するオブジェクトストレージに保存されますが、他のユーザーからアクセスすることはできません。各ユーザーには最初から専用の User Stage が用意されており、使用前に作成したり名前を付けたりする必要はありません。また、User Stage を削除することもできません。

User Stage は、他のユーザーと共有する必要のないデータファイルを保存するための便利な保管場所として利用できます。User Stage にアクセスするには、`@~` を使用します。たとえば、自分の stage 内のすべてのファイルを一覧表示するには次のようにします。

```sql
LIST @~;
```

## PATTERN を使用した stage ファイルのフィルタリング {#filtering-staged-files-with-pattern}

stage 内のファイルを読み取り、一覧表示し、削除し、または調査するコマンドや関数では、`PATTERN` を使用して正規表現でファイルをフィルタリングできます。stage のロケーションに対しては、`PATTERN` は完全な stage URI ではなく、`@<stage_name>[/<path>]` の後ろに続くファイルパス部分に対してマッチします。

> **Note:**
>
> ファイルパス内の glob パターン（例: `ontime_200{6,7,8}.csv` や `ontime_200[6-8].csv`）は、HTTP ベースの外部ロケーションでのみサポートされます。S3 やその他のオブジェクトストレージのロケーションでは、ファイルパス内の glob 展開はサポートされません。代わりに、正規表現を使った `PATTERN` を使用してください。

たとえば、`@sales_stage/raw/` に対して、stage ファイル `@sales_stage/raw/year=2025/month=01/sales_20250101.parquet` は `year=2025/month=01/sales_20250101.parquet` としてマッチされます。

```sql
LIST @sales_stage/raw/ PATTERN = 'year=2025/month=01/.*[.]parquet';
```

stage パス配下のすべての `.log` ファイルにマッチさせるには、次のような正規表現を使用します。

```sql
LIST @my_stage PATTERN = '.*[.]log';
```

## stage の管理 {#managing-stages}

{{{ .lake }}} には、stage およびその中に stage されたファイルを管理するためのさまざまなコマンドが用意されています。

| コマンド                                                      | 説明                                                                                                                                                                                                                          | User Stage に適用 | Internal Stage に適用 | External Stage に適用 |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------- | ------------------------- | ------------------------- |
| [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) | Internal Stage または External Stage を作成します。                                                                                                                                                                                               | No                    | Yes                       | Yes                       |
| [DROP STAGE](/tidb-cloud-lake/sql/drop-stage.md)     | Internal Stage または External Stage を削除します。                                                                                                                                                                                               | No                    | Yes                       | Yes                       |
| [DESC STAGE](/tidb-cloud-lake/sql/desc-stage.md)     | Internal Stage または External Stage のプロパティを表示します。                                                                                                                                                                               | No                    | Yes                       | Yes                       |
| [LIST](/tidb-cloud-lake/sql/list-stage-files.md)           | stage 内のファイルの一覧を返します。あるいは、テーブル関数 [LIST_STAGE](/tidb-cloud-lake/sql/list-stage.md) を使用すると、特定のファイル情報を取得するための柔軟性が追加された同様の機能を利用できます | Yes                   | Yes                       | Yes                       |
| [REMOVE](/tidb-cloud-lake/sql/remove-stage-files.md)       | stage からファイルを削除します。                                                                                                                                                                                                   | Yes                   | Yes                       | Yes                       |
| [SHOW STAGES](/tidb-cloud-lake/sql/show-stages.md)   | 作成済みの Internal Stage および External Stage の一覧を返します。                                                                                                                                                                          | No                    | Yes                       | Yes                       |