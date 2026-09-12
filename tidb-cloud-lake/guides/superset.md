---
title: 使用 Apache Superset 连接到 TiDB Cloud Lake
summary: 了解如何在 Apache Superset 中安装 TiDB Cloud Lake 的 SQLAlchemy 方言，并将 Superset 连接到 TiDB Cloud Lake 计算集群。
---

# 使用 Apache Superset 连接到 TiDB Cloud Lake

[Apache Superset](https://superset.apache.org/) 是一个开源的数据探索和可视化平台。Superset 通过 [TiDB Cloud Lake dialect for SQLAlchemy](https://github.com/tidbcloud/lake-sqlalchemy) 连接到 {{{ .lake }}}。

## 前提条件 {#prerequisites}

开始之前，请确保你已具备以下条件：

- Docker
- 一个 {{{ .lake }}} 账户、数据库和计算集群
- 用于连接的主机、用户名、密码、数据库名称和计算集群名称

如需了解如何获取连接信息，请参见[连接到计算集群](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse)。

## 构建 Superset 镜像 {#build-a-superset-image}

官方 Superset 镜像不包含 {{{ .lake }}} SQLAlchemy 方言。请创建一个名为 `Dockerfile` 的文件，并写入以下内容：

```dockerfile
FROM apache/superset

USER root
RUN pip install --no-cache-dir tidbcloudlake-sqlalchemy
USER superset
```

`tidbcloudlake-sqlalchemy` 包会安装所需的 {{{ .lake }}} Python 驱动作为依赖关系。

构建镜像：

```shell
docker build -t superset-lake .
```

基于该镜像启动一个容器：

```shell
docker run -d \
    -p 8080:8088 \
    -e "SUPERSET_SECRET_KEY=<your-secret-key>" \
    --name superset \
    superset-lake
```

## 初始化 Superset {#initialize-superset}

创建管理员账户：

```shell
docker exec -it superset superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@example.com \
    --password <admin-password>
```

应用数据库迁移：

```shell
docker exec -it superset superset db upgrade
```

初始化 Superset：

```shell
docker exec -it superset superset init
```

打开 `http://localhost:8080`，并使用管理员账户登录。

## 将 Superset 连接到 TiDB Cloud Lake {#connect-superset-to-tidb-cloud-lake}

1. 在 Superset 中，选择 **Settings** > **Data** > **Connect Database**。
2. 选择 **Other** 作为数据库类型。
3. 输入一个显示名称，例如 `TiDB Cloud Lake`。
4. 按以下格式输入 SQLAlchemy URI：

    ```text
    lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
    ```

5. 点击 **Test Connection**。
6. 连接测试成功后，点击 **Connect**。

现在，你可以在 Superset 中基于 {{{ .lake }}} 表创建数据集，并将其用于图表和仪表板。

## 相关资源 {#related-resources}

- [PyPI 上的 `tidbcloudlake-sqlalchemy`](https://pypi.org/project/tidbcloudlake-sqlalchemy/)
- [Apache Superset 文档](https://superset.apache.org/docs/intro)