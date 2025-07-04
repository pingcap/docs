---
title: Integrate TiDB Vector Search with Django ORM
summary: Learn how to integrate TiDB Vector Search with Django ORM to store embeddings and perform semantic search.
---

# Integrate TiDB Vector Search with Django ORM

This tutorial walks you through how to use [Django](https://www.djangoproject.com/) ORM to interact with the [TiDB Vector Search](/vector-search/vector-search-overview.md), store embeddings, and perform vector search queries.

<CustomContent platform="tidb">

> **Warning:**
>
> The vector search feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> The vector search feature is only available for TiDB Self-Managed clusters and [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

## Prerequisites

To complete this tutorial, you need:

- [Python 3.8 or higher](https://www.python.org/downloads/) installed.
- [Git](https://git-scm.com/downloads) installed.
- A TiDB cluster.

<CustomContent platform="tidb">

**If you don't have a TiDB cluster, you can create one as follows:**

- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.
- Follow [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster of v8.4.0 or a later version.

</CustomContent>

## Run the sample app

You can quickly learn about how to integrate TiDB Vector Search with Django ORM by following the steps below.

### Step 1. Clone the repository

Clone the `tidb-vector-python` repository to your local machine:

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### Step 2. Create a virtual environment

Create a virtual environment for your project:

```bash
cd tidb-vector-python/examples/orm-django-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3. Install required dependencies

Install the required dependencies for the demo project:

```bash
pip install -r requirements.txt
```

Alternatively, you can install the following packages for your project:

```bash
pip install Django django-tidb mysqlclient numpy python-dotenv
```

If you encounter installation issues with mysqlclient, refer to the mysqlclient official documentation.

#### What is `django-tidb`

`django-tidb` is a TiDB dialect for Django, which enhances the Django ORM to support TiDB-specific features (for example, Vector Search) and resolves compatibility issues between TiDB and Django.

To install `django-tidb`, choose a version that matches your Django version. For example, if you are using `django==4.2.*`, install `django-tidb==4.2.*`. The minor version does not need to be the same. It is recommended to use the latest minor version.

For more information, refer to [django-tidb repository](https://github.com/pingcap/django-tidb).

### Step 4. Configure the environment variables

Configure the environment variables depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="{{{ .starter }}}">

For a {{{ .starter }}} cluster, take the following steps to obtain the cluster connection string and configure environment variables:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Connection Type** is set to `Public`
    - **Branch** is set to `main`
    - **Connect With** is set to `General`
    - **Operating System** matches your environment.

    > **Tip:**
    >
    > If your program is running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.

4. Copy the connection parameters from the connection dialog.

    > **Tip:**
    >
    > If you have not set a password yet, click **Generate Password** to generate a random password.

5. In the root directory of your Python project, create a `.env` file and paste the connection parameters to the corresponding environment variables.

    - `TIDB_HOST`: The host of the TiDB cluster.
    - `TIDB_PORT`: The port of the TiDB cluster.
    - `TIDB_USERNAME`: The username to connect to the TiDB cluster.
    - `TIDB_PASSWORD`: The password to connect to the TiDB cluster.
    - `TIDB_DATABASE`: The database name to connect to.
    - `TIDB_CA_PATH`: The path to the root certificate file.

    The following is an example for macOS:

    ```dotenv
    TIDB_HOST=gateway01.****.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME=********.root
    TIDB_PASSWORD=********
    TIDB_DATABASE=test
    TIDB_CA_PATH=/etc/ssl/cert.pem
    ```

</div>
<div label="TiDB Self-Managed">

For a TiDB Self-Managed cluster, create a `.env` file in the root directory of your Python project. Copy the following content into the `.env` file, and modify the environment variable values according to the connection parameters of your TiDB cluster:

```dotenv
TIDB_HOST=127.0.0.1
TIDB_PORT=4000
TIDB_USERNAME=root
TIDB_PASSWORD=
TIDB_DATABASE=test
```

If you are running TiDB on your local machine, `TIDB_HOST` is `127.0.0.1` by default. The initial `TIDB_PASSWORD` is empty, so if you are starting the cluster for the first time, you can omit this field.

The following are descriptions for each parameter:

- `TIDB_HOST`: The host of the TiDB cluster.
- `TIDB_PORT`: The port of the TiDB cluster.
- `TIDB_USERNAME`: The username to connect to the TiDB cluster.
- `TIDB_PASSWORD`: The password to connect to the TiDB cluster.
- `TIDB_DATABASE`: The name of the database you want to connect to.

</div>

</SimpleTab>

### Step 5. Run the demo

Migrate the database schema:

```bash
python manage.py migrate
```

Run the Django development server:

```bash
python manage.py runserver
```

Open your browser and visit `http://127.0.0.1:8000` to try the demo application. Here are the available API paths:

| API Path                                | Description                              |
| --------------------------------------- | ---------------------------------------- |
| `POST: /insert_documents`               | Insert documents with embeddings.        |
| `GET: /get_nearest_neighbors_documents` | Get the 3-nearest neighbor documents.    |
| `GET: /get_documents_within_distance`   | Get documents within a certain distance. |

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

### Connect to the TiDB cluster

In the file `sample_project/settings.py`, add the following configurations:

```python
dotenv.load_dotenv()

DATABASES = {
    "default": {
        # https://github.com/pingcap/django-tidb
        "ENGINE": "django_tidb",
        "HOST": os.environ.get("TIDB_HOST", "127.0.0.1"),
        "PORT": int(os.environ.get("TIDB_PORT", 4000)),
        "USER": os.environ.get("TIDB_USERNAME", "root"),
        "PASSWORD": os.environ.get("TIDB_PASSWORD", ""),
        "NAME": os.environ.get("TIDB_DATABASE", "test"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

TIDB_CA_PATH = os.environ.get("TIDB_CA_PATH", "")
if TIDB_CA_PATH:
    DATABASES["default"]["OPTIONS"]["ssl_mode"] = "VERIFY_IDENTITY"
    DATABASES["default"]["OPTIONS"]["ssl"] = {
        "ca": TIDB_CA_PATH,
    }
```

You can create a `.env` file in the root directory of your project and set up the environment variables `TIDB_HOST`, `TIDB_PORT`, `TIDB_USERNAME`, `TIDB_PASSWORD`, `TIDB_DATABASE`, and `TIDB_CA_PATH` with the actual values of your TiDB cluster.

### Create vector tables

#### Define a vector column

`tidb-django` provides a `VectorField` to store vector embeddings in a table.

Create a table with a column named `embedding` that stores a 3-dimensional vector.

```python
class Document(models.Model):
   content = models.TextField()
   embedding = VectorField(dimensions=3)
```

### Store documents with embeddings

```python
Document.objects.create(content="dog", embedding=[1, 2, 1])
Document.objects.create(content="fish", embedding=[1, 2, 4])
Document.objects.create(content="tree", embedding=[1, 0, 0])
```

### Search the nearest neighbor documents

TiDB Vector support the following distance functions:

- `L1Distance`
- `L2Distance`
- `CosineDistance`
- `NegativeInnerProduct`

Search for the top-3 documents that are semantically closest to the query vector `[1, 2, 3]` based on the cosine distance function.

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).order_by('distance')[:3]
```

### Search documents within a certain distance

Search for the documents whose cosine distance from the query vector `[1, 2, 3]` is less than 0.2.

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).filter(distance__lt=0.2).order_by('distance')[:3]
```

## See also

- [Vector Data Types](/vector-search/vector-search-data-types.md)
- [Vector Search Index](/vector-search/vector-search-index.md)
