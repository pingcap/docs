---
title: Apache Superset で TiDB Cloud Lake に接続する
summary: Apache Superset に TiDB Cloud Lake SQLAlchemy dialect をインストールし、Superset を TiDB Cloud Lake の Warehouse に接続する方法を学びます。
---

# Apache Superset で TiDB Cloud Lake に接続する

[Apache Superset](https://superset.apache.org/) は、オープンソースのデータ探索および可視化プラットフォームです。Superset は、[TiDB Cloud Lake dialect for SQLAlchemy](https://github.com/tidbcloud/lake-sqlalchemy) を介して {{{ .lake }}} に接続します。

## 前提条件 {#prerequisites}

開始する前に、以下を用意してください。

- Docker
- {{{ .lake }}} のアカウント、データベース、および Warehouse
- 接続に使用する host、username、password、database、および warehouse 名

接続情報の取得方法については、[Warehouse に接続する](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse) を参照してください。

## Superset イメージをビルドする {#build-a-superset-image}

公式の Superset イメージには、{{{ .lake }}} SQLAlchemy dialect は含まれていません。`Dockerfile` という名前のファイルを作成し、以下の内容を記述します。

```dockerfile
FROM apache/superset

USER root
RUN pip install --no-cache-dir tidbcloudlake-sqlalchemy
USER superset
```

`tidbcloudlake-sqlalchemy` パッケージは、必要な {{{ .lake }}} Python driver を依存関係としてインストールします。

イメージをビルドします。

```shell
docker build -t superset-lake .
```

イメージからコンテナを起動します。

```shell
docker run -d \
    -p 8080:8088 \
    -e "SUPERSET_SECRET_KEY=<your-secret-key>" \
    --name superset \
    superset-lake
```

## Superset を初期化する {#initialize-superset}

管理者アカウントを作成します。

```shell
docker exec -it superset superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@example.com \
    --password <admin-password>
```

データベースマイグレーションを適用します。

```shell
docker exec -it superset superset db upgrade
```

Superset を初期化します。

```shell
docker exec -it superset superset init
```

`http://localhost:8080` を開き、管理者アカウントでサインインします。

## Superset を TiDB Cloud Lake に接続する {#connect-superset-to-tidb-cloud-lake}

1. Superset で、**Settings** > **Data** > **Connect Database** を選択します。
2. データベースタイプとして **Other** を選択します。
3. `TiDB Cloud Lake` などの表示名を入力します。
4. 以下の形式で SQLAlchemy URI を入力します。

    ```text
    lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
    ```

5. **Test Connection** をクリックします。
6. 接続テストが成功したら、**Connect** をクリックします。

これで、Superset で {{{ .lake }}} テーブルからデータセットを作成し、それらをチャートやダッシュボードで使用できるようになります。

## 関連リソース {#related-resources}

- [PyPI の `tidbcloudlake-sqlalchemy`](https://pypi.org/project/tidbcloudlake-sqlalchemy/)
- [Apache Superset documentation](https://superset.apache.org/docs/intro)