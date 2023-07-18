---
title: Build a TiDB App Using Django
summary: Learn an example of how to build a TiDB application using Django.
---

<!-- markdownlint-disable MD029 -->

# Build a TiDB App Using Spring Boot

This tutorial shows you how to build a [Django](https://www.djangoproject.com/) web application using TiDB. The [django-tidb](https://github.com/pingcap/django-tidb) module is used as the framework for data access capabilities. You can download the code for this sample application from [[Github](https://github.com/pingcap-inc/tidb-example-python).

This is a sample application for building a RESTful API, which shows a generic **Django** backend service using **TiDB** as the database. The following process was designed to recreate a real-world scenario:

This is an example of a game where each player has two attributes: `coins` and `goods`. Each player is uniquely identified by an `id` field. Players can trade freely if they have sufficient coins and goods.

You can build your own application based on this example.

## Step 1: Launch your TiDB cluster

<CustomContent platform="tidb">

The following introduces how to start a TiDB cluster.

**Use a TiDB Serverless cluster**

For detailed steps, see [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster).

**Use a local cluster**

For detailed steps, see [Deploy a local test cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

See [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster).

</CustomContent>

## Step 2: Install  Python

Download and install the **Python** on your computer. It is a necessary tool for Python development. [Django 3.2.16](https://docs.djangoproject.com/en/3.2/) supports Python for 3.6 later versions. It is recommended that you use 3.10 and later versions.

## Step 3: Get the application code

Download or clone the [pingcap-inc/tidb-example-python](https://github.com/pingcap-inc/tidb-example-python) and navigate to the `django_example` directory.

## Step 4: Run the application

In this step, the application code is compiled and run, which produces a web application. Django creates a `player` table within the `django` database. If you make requests using the application's RESTful API, these requests run [database transactions](/develop/dev-guide-transaction-overview.md) on the TiDB cluster.

If you want to learn more about the code of this application, refer to [Implementation details](#implementation-details).

### Step 4.1 Change parameters

If you are using a TiDB Serverless cluster, you need to provide your CA root path and replace `<ca_path>` in the following examples with your CA path. To get the CA root path on your system, refer to [Where is the CA root path on my system?](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system).

Change the `DATABASES` parameter in the `settings.py` (located in `example_project`).

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_tidb',
        'NAME': 'django',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 4000,
    },
}
```

Suppose that the password you set is `123456`, and the connection parameters you get from the cluster details page are the following:

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

Accordingly, the parameters must be set as folows:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_tidb',
        'NAME': 'django',
        'USER': '2aEp24QWEDLqRFs.root',
        'PASSWORD': '123456',
        'HOST': 'xxx.tidbcloud.com',
        'PORT': 4000,
        'OPTIONS': {
            'ssl': {
                "ca": "<ca_path>"
            },
        },
    },
}
```

### Step 4.2 Run

1. Open a terminal session and make sure you are in the `tidb-example-python` directory. If you are not already in this directory, navigate to the directory with the following command.

    ```shell
    cd <path>/tidb-example-python
    ```

2. Install dependencies, and enter `django_example` directory.

    ```shell
    pip install -r requirement.txt
    cd django_example
    ```

3. Running Data Model Migration.

    > **Note:**
    >
    > - This step assumes that the `django` database already exists.
    > - If the `django` database has not been created, you can create it using the `CREATE DATABASE django` statement. For detailed information on creating a database, refer to [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md#create-database) document.
    > - The database name `NAME` can be changed in the `DATABASES` parameter of `example_project/settings.py`.

    This command will generate the necessary data tables required by Django within the connected database.

    ```bash
    python manage.py migrate
    ```

4. Run application.

    ```bash
    python manage.py runserver
    ```

### Step 4.3 Output

The final part of the output should look like the following:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 12, 2022 - 08:21:50
Django version 3.2.16, using settings 'example_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

If you want to learn more about the code of this application, refer to [implementation details](#implementation-details).

## Step 5: HTTP requests

After the service is up and running, you can send the HTTP requests to the backend application. <http://localhost:8080> is the base URL that provides services. This tutorial uses a series of HTTP requests to show how to use the service.

<SimpleTab groupId="request">

<div label="Use Postman requests (recommended)" value="postman">

1. You can download this [configuration file](https://raw.githubusercontent.com/pingcap-inc/tidb-example-python/main/django_example/Player.postman_collection.json) locally and import it into [Postman](https://www.postman.com/) as shown here:

    ![postman import](/media/develop/postman_player_import.png)

2. Send requests:

    - Create players

        Click on the **Create** tab and the **Send** button to send a POST request to `http://localhost:8080/player/`. The return value is the number of players added, which is expected to be 1.

    - Get player information by ID

        Click on the **GetByID** tab and the **Send** button to send a GET request to `http://localhost:8080/player/1`. The return value is the information of the player with ID `1`.

    - Get player information in bulk by limit

        Click on the **GetByLimit** tab and the **Send** button to send a GET request to `http://localhost:8080/player/limit/3`. The return value is a list of information for up to 3 players.

    - Count players

        Click the **Count** tab and the **Send** button to send a GET request to `http://localhost:8080/player/count`. The return value is the number of players.

    - Player trading

        Click on the **Trade** tab and the **Send** button to send a POST request to `http://localhost:8080/player/trade`. The request parameters are the seller's ID `sellID`, the buyer's ID `buyID`, the number of goods purchased `amount`, the number of coins consumed for the purchase `price`.

        The return value is whether the transaction is successful or not. When there are insufficient goods for the seller, insufficient coins for the buyer, or a database error, the [database transaction](/develop/dev-guide-transaction-overview.md) guarantees that the trade is not successful and no player's coins or goods are lost.

</div>

<div label="Using curl requests" value="curl">

You can also use curl to make requests directly.

- Create players

    To create players, you can send a **POST** request to the `/player` endpoint. For example:

    ```shell
    curl --location --request POST 'http://localhost:8000/player/' --header 'Content-Type: application/json' --data-raw '[{"coins":100,"goods":20}]'
    ```

    The request uses JSON as the payload. The example above indicates creating a player with 100 `coins` and 20 `goods`. The return value is the number of players created.

    ```
    create 1 players.
    ```

- Get player information by ID

    To get the player information, you can send a **GET** request to the `/player` endpoint. You need to specify the `id` of the player in the path parameter as follows: `/player/{id}`. The following example shows how to get the information of a player with `id` 1:

    ```shell
    curl --location --request GET 'http://localhost:8000/player/1'
    ```

    The return value is the player's information:

    ```json
    {
    "coins": 200,
    "goods": 10,
    "id": 1
    }
    ```

- Get player information in bulk by limit

    To get the player information in bulk, you can send a **GET** request to the `/player/limit` endpoint. You need to specify the total number of players in the path parameter as follows: `/player/limit/{limit}`. The following example shows how to get the information of up to 3 players:

    ```shell
    curl --location --request GET 'http://localhost:8000/player/limit/3'
    ```

    The return value is a list of player information:

    ```json
    [
    {
        "coins": 200,
        "goods": 10,
        "id": 1
    },
    {
        "coins": 0,
        "goods": 30,
        "id": 2
    },
    {
        "coins": 100,
        "goods": 20,
        "id": 3
    }
    ]
    ```

- Count players

    To get the number of players, you can send a **GET** request to the `/player/count` endpoint:

    ```shell
    curl --location --request GET 'http://localhost:8000/player/count'
    ```

    The return value is the number of players:

    ```
    4
    ```

- Player trading

    To initiate a transaction between players, you can send a **POST** request to the `/player/trade` endpoint. For example:

    ```shell
    curl --location --request POST 'http://localhost:8000/player/trade' \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'sellID=1' \
    --data-urlencode 'buyID=2' \
    --data-urlencode 'amount=10' \
    --data-urlencode 'price=100'
    ```

    The request uses **Form Data** as the payload. The example request indicates that the seller's ID (`sellID`) is 1, the buyer's ID (`buyID`) is 2, the number of goods purchased (`amount`) is 10, and the number of coins consumed for purchase (`price`) is 100.

    The return value is whether the transaction is successful or not. When there are insufficient goods for the seller, insufficient coins for the buyer, or a database error, the [database transaction](/develop/dev-guide-transaction-overview.md) guarantees that the trade is not successful and no player's coins or goods are lost.

    ```
    true
    ```

</div>

<div label="使用 Shell 脚本" value="shell">

You can download [this shell script](https://github.com/pingcap-inc/tidb-example-python/blob/main/django_example/request.sh) for testing purposes. The script performs the following operations:

1. Create 10 players in a loop.
2. Get the information of players with the `id` of 1.
3. Get a list of up to 3 players.
4. Get the total number of players.
5. Perform a transaction, where the player with the `id` of 1 is the seller and the player with the `id` of 2 is the buyer, and 10 `goods` are purchased at the cost of 100 `coins`.

You can run this script with `./request.sh`. The result should look like this:

```shell
> ./request.sh
loop to create 10 players:
create 1 players.create 1 players.create 1 players.create 1 players.create 1 players.create 1 players.create 1 players.create 1 players.create 1 players.create 1 players.

get player 1:
{"id": 1, "coins": 100, "goods": 20}

get players by limit 3:
[{"id": 1, "coins": 100, "goods": 20}, {"id": 2, "coins": 100, "goods": 20}, {"id": 3, "coins": 100, "goods": 20}]

get players count:
10

trade by two players:
trade successful
```

</div>

</SimpleTab>

## Implementation details

This subsection describes the components in the sample application project.

### Overview

The catalog tree for this example project is shown below (some incomprehensible parts are removed):

```
.
├── example_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── player
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── manage.py
```

- Each `__init__.py` file in every folder declares that the folder is a Python package.
- `manage.py` is a script automatically generated by Django for managing the project.
- `example_project` contains code at the project level:

    - `settings.py` declares the project's configuration, such as the database address, password, and the database dialect being used.
    - `urls.py` configures the project's root routes.

- `player` is a package in the project that provides management and data querying for the `Player` data model. In Django, this is referred to as an application. You can create an empty `player` application using the command `python manage.py startapp player`.

    - `models.py` defines the `Player` data model.
    - `migrations` is a set of data model migration scripts. You can automatically analyze the data objects defined in the `models.py` file and generate migration scripts using the command `python manage.py makemigrations player`.
    - `urls.py` defines the routes for the application.
    - `views.py` provides the logic code for the application.

> **Note:**
>
> Due to Django's pluggable model, you need to register the application within the project after creating it. In this example, the registration process involves adding the entry `'player.apps.PlayerConfig'` to the `INSTALLED_APPS` object in the `example_project/settings.py` file. You can refer to the sample code in [`settings.py`](https://github.com/pingcap-inc/tidb-example-python/blob/main/django_example/example_project/settings.py#L33-L41) for more information.

### Configuration

This section provides a brief introduction to the important configurations in the `settings.py` file within the `example_project` package. This file contains the configuration for the Django project, including the declared applications, middleware, and connected databases. You can refer to the section on [Create a blank application with the same dependency (optional)](#create-a-blank-application-with-the-same-dependency-optional) to understand the generation process of this configuration file or directly use the `settings.py` file in your project. For more information on Django configuration, refer to the [Django Configuration](https://docs.djangoproject.com/en/3.2/topics/settings/) documentation.

```python
...

# Application definition

INSTALLED_APPS = [
    'player.apps.PlayerConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

...

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tidb',
        'NAME': 'django',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 4000,
    },
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

...
```

- `INSTALLED_APPS`：启用的应用全限定名称列表。
- `MIDDLEWARE`：启用的中间件列表。由于本示例无需 `CsrfViewMiddleware` 中间件，因此其被注释。
- `DATABASES`：数据库配置。其中，`ENGINE` 一项被配置为 `django_tidb`，这遵循了 [django-tidb](https://github.com/pingcap/django-tidb) 的配置要求。

- `INSTALLED_APPS`: A list of fully qualified names of enabled applications.
- `MIDDLEWARE`: A list of enabled middleware. In this example, the `CsrfViewMiddleware` middleware is commented out, indicating that it is not used.
- `DATABASES`: The configuration for the database. Here, the `ENGINE` is configured as `django_tidb`, following the configuration requirements of [django-tidb](https://github.com/pingcap/django-tidb).

### Root router

The root router is written in the `urls.py` file within the `example_project` package:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('player/', include('player.urls')),
    path('admin/', admin.site.urls),
]
```

In the above example, the root router maps the `player/` path to `player.urls`. This means that the `urls.py` file in the `player` package is responsible for handling all URL requests starting with `player/`. For more information on the Django URL dispatcher, please refer to the [Django URL Dispatcher](https://docs.djangoproject.com/en/3.2/topics/http/urls/) documentation.

### player Application

The `player` application implements functionalities such as data model migration, object persistence, and interface implementation for the `Player` object.

#### Data Model

The `models.py` file contains the `Player` data model, which corresponds to a table in the database.

```python
from django.db import models

# Create your models here.


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    coins = models.IntegerField()
    goods = models.IntegerField()

    objects = models.Manager()

    class Meta:
        db_table = "player"

    def as_dict(self):
        return {
            "id": self.id,
            "coins": self.coins,
            "goods": self.goods,
        }
```

In the above example, the data model has a subclass `Meta`, which provides additional information to Django to specify the metadata of the data model. Among them, `db_table` declares the table name associated with this data model as `player`. For a complete list of options for model metadata, you can refer to the [Django Model Meta Options](https://docs.djangoproject.com/en/3.2/ref/models/options/) documentation.

In addition, the data model defines three attributes: `id`, `coins`, and `goods`:

- `id`: `models.AutoField(primary_key=True)` indicates that it is an automatically incrementing primary key.
- `coins`: `models.IntegerField()` indicates that it is a field of type Integer.
- `goods`: `models.IntegerField()` indicates that it is a field of type Integer.

For detailed information on data models, you can refer to the [Django Models](https://docs.djangoproject.com/en/3.2/topics/db/models/) documentation.

#### Data Model Migration

Django relies on Python code that defines data models to perform database model migration. It generates a series of database model migration scripts to handle the differences between the code and the database. After defining the `Player` data model in `models.py`, you can use `python manage.py makemigrations player` to generate migration scripts. In the example provided, `0001_initial.py` inside the `migrations` package is the automatically generated migration script.

```python
# Generated by Django 3.2.16 on 2022-11-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('coins', models.IntegerField()),
                ('goods', models.IntegerField()),
            ],
            options={
                'db_table': 'player',
            },
        ),
    ]
```

You can use `python manage.py sqlmigrate ...` to preview the SQL statements that will be executed by the migration script. This greatly reduces the possibility of unexpected SQL statements being executed during migration. After generating the migration script, it is recommended to use this command at least once to preview and carefully review the generated SQL statements. In this example, you can run `python manage.py sqlmigrate player 0001` to obtain readable SQL statements that facilitate the review of the statements by developers.

```sql
--
-- Create model Player
--
CREATE TABLE `player` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `coins` integer NOT NULL, `goods` integer NOT NULL);
```

生成迁移脚本后，你可以使用 `python manage.py migrate` 实施数据迁移。此命令拥有幂等性，其运行后将在数据库内保存一条运行记录以完成幂等保证。因此，你可以多次运行此命令，而无需担心重复运行 SQL 语句。

After generating the migration script, you can use `python manage.py migrate` to perform data migration. This command is idempotent, meaning that it creates a single record in the database to ensure idempotence. Therefore, you can run this command multiple times without worrying about executing SQL statements repeatedly.

#### Application Routing

In the [Root Router](#root-router) section, the example program maps the `player/` path to `player.urls`. This section will further describe the application routing in the `urls.py` file under the `player` package:

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.create, name='create'),
    path('count', views.count, name='count'),
    path('limit/<int:limit>', views.limit_list, name='limit_list'),
    path('<int:player_id>', views.get_by_id, name='get_by_id'),
    path('trade', views.trade, name='trade'),
]
```

The application routing registers 5 paths:

- `''`: Points to the `views.create` function.
- `'count'`: Points to the `views.count` function.
- `'limit/<int:limit>'`: Points to the `views.limit_list` function. This path includes a `<int:limit>` path variable, where:

    - `int` specifies that this parameter will be validated as an `int` type.
    - `limit` specifies that the value of this parameter will be mapped to a function argument named `limit`.

- `'<int:player_id>'`: Points to the `views.get_by_id` function. This path includes an `<int:player_id>` path variable.
- `'trade'`: Points to the `views.trade` function.

Additionally, the application routing inherits from the root router, so it includes the paths configured in the root router when matching URLs. As shown in the example above, the root router is configured to forward `player/` to this application routing. Therefore, in the application routing:

- `''` corresponds to the actual request `http(s)://<host>(:<port>)/player`.
- `'count'` corresponds to the actual request `http(s)://<host>(:<port>)/player/count`.
- `'limit/<int:limit>'` with an example value of `limit=3` corresponds to the actual request `http(s)://<host>(:<port>)/player/limit/3`.

#### Logic Implementation

The logic implementation code resides in the `views.py` file under the `player` package, which is known as views in Django. For more information on Django views, refer to the [Django Views](https://docs.djangoproject.com/en/3.2/topics/http/views/) documentation.

```python
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import *
from .models import Player
import json


@require_POST
def create(request):
    dict_players = json.loads(request.body.decode('utf-8'))
    players = list(map(
        lambda p: Player(
            coins=p['coins'],
            goods=p['goods']
        ), dict_players))
    result = Player.objects.bulk_create(objs=players)
    return HttpResponse(f'create {len(result)} players.')


@require_GET
def count(request):
    return HttpResponse(Player.objects.count())


@require_GET
def limit_list(request, limit: int = 0):
    if limit == 0:
        return HttpResponse("")
    players = set(Player.objects.all()[:limit])
    dict_players = list(map(lambda p: p.as_dict(), players))
    return JsonResponse(dict_players, safe=False)


@require_GET
def get_by_id(request, player_id: int):
    result = get_object_or_404(Player, pk=player_id).as_dict()
    return JsonResponse(result)


@require_POST
@transaction.atomic
def trade(request):
    sell_id, buy_id, amount, price = int(request.POST['sellID']), int(request.POST['buyID']), \
                                     int(request.POST['amount']), int(request.POST['price'])
    sell_player = Player.objects.select_for_update().get(id=sell_id)
    if sell_player.goods < amount:
        raise Exception(f'sell player {sell_player.id} goods not enough')

    buy_player = Player.objects.select_for_update().get(id=buy_id)
    if buy_player.coins < price:
        raise Exception(f'buy player {buy_player.id} coins not enough')

    Player.objects.filter(id=sell_id).update(goods=F('goods') - amount, coins=F('coins') + price)
    Player.objects.filter(id=buy_id).update(goods=F('goods') + amount, coins=F('coins') - price)

    return HttpResponse("trade successful")
```

The following will explain the key parts of the code:

- Decorators:

    - `@require_GET`: Indicates that this function only accepts `GET` HTTP requests.
    - `@require_POST`: Indicates that this function only accepts `POST` HTTP requests.
    - `@transaction.atomic`: Indicates that all database operations within this function will be executed within a single transaction. For more information on using transactions in Django, refer to the [Django Database Transactions](https://docs.djangoproject.com/en/3.2/topics/db/transactions/) documentation. For detailed information on transactions in TiDB, refer to the [TiDB Transaction Overview](/develop/dev-guide-transaction-overview.md) documentation.

- `create` function:

    - Retrieves the payload from the `body` of the `request` object and decodes it using `utf-8`:

        ```python
        dict_players = json.loads(request.body.decode('utf-8'))
        ```

    - Uses the `map` function within a lambda to transform the `dict_players` object of type `dict` into a list of `Player` data model instances:

        ```python
        players = list(map(
            lambda p: Player(
                coins=p['coins'],
                goods=p['goods']
            ), dict_players))
        ```

    - Calls the `bulk_create` function of the `Player` data model to add the `players` list in bulk and returns the number of items added:

        ```python
        result = Player.objects.bulk_create(objs=players)
        return HttpResponse(f'create {len(result)} players.')
        ```

- `count` function: Calls the `count` function of the `Player` data model and returns the total number of data entries.
- `limit_list` function:

    - Short-circuit logic: When `limit` is `0`, no database request is sent:

        ```python
        if limit == 0:
            return HttpResponse("")
        ```

    - Calls the `all` function of the `Player` data model and uses the slicing operator to retrieve the first `limit` items. It's important to note that Django does not retrieve all data and then slice the first `limit` items in memory. Instead, it requests the first `limit` items from the database when they are used. This is because Django overrides the slicing operator, and QuerySet objects are **lazy**. This means that slicing an unevaluated QuerySet will continue to return an unevaluated QuerySet until you actually request the data within the QuerySet for the first time. For example, here we use the `set` function to iterate over it and return the entire set. For more information on Django QuerySets, you can refer to the [Django QuerySet API](https://docs.djangoproject.com/en/3.2/ref/models/querysets/) documentation.

        ```python
        players = set(Player.objects.all()[:limit])
        ```

    - Converts the returned list of `Player` data model instances to a list of dictionaries and outputs it using `JsonResponse`.

        ```python
        dict_players = list(map(lambda p: p.as_dict(), players))
        return JsonResponse(dict_players, safe=False)
        ```

- `get_by_id` function:

    - Uses the `get_object_or_404` shortcut with the `player_id` to retrieve the `Player` object and converts it to a dictionary. If the data does not exist, this function returns a `404` status code:

        ```python
        result = get_object_or_404(Player, pk=player_id).as_dict()
        ```

    - Returns the data using `JsonResponse`:

        ```python
        return JsonResponse(result)
        ```

- `trade` function:

    - Receives form data from the `POST` payload:

        ```python
        sell_id, buy_id, amount, price = int(request.POST['sellID']), int(request.POST['buyID']), \
                                        int(request.POST['amount']), int(request.POST['price'])
        ```

    - Calls the `select_for_update` function of the `Player` data model to lock the data of the seller and the buyer, and checks if the seller has enough goods and the buyer has enough currency. This function uses the `@transaction.atomic` decorator, and any exception will cause a transaction rollback. This mechanism can be used to throw an exception when any check fails, and Django will handle the transaction rollback.

        ```python
        sell_player = Player.objects.select_for_update().get(id=sell_id)
        if sell_player.goods < amount:
            raise Exception(f'sell player {sell_player.id} goods not enough')

        buy_player = Player.objects.select_for_update().get(id=buy_id)
        if buy_player.coins < price:
            raise Exception(f'buy player {buy_player.id} coins not enough')
        ```

    - Updates the data of the seller and the buyer. Since the `@transaction.atomic` decorator is used here, any exceptions will be handled by Django and the transaction will be rolled back. Therefore, please do not use `try-except` statements for exception handling in this section. If you need to handle exceptions, continue to raise the exception in the `except` block to prevent Django from mistakenly assuming that the function is running normally and committing the transaction, which may lead to data errors.

        ```python
        Player.objects.filter(id=sell_id).update(goods=F('goods') - amount, coins=F('coins') + price)
        Player.objects.filter(id=buy_id).update(goods=F('goods') + amount, coins=F('coins') - price)
        ```

    - Returns a string indicating a successful trade, as any other situation will result in an exception being raised and returned:

        ```python
        return HttpResponse("trade successful")
        ```

## Create a blank application with the same dependency (optional)

This program is built using the Django Admin CLI [django-admin](https://django-admin-cli.readthedocs.io/en/stable/index.html). You can install and use `django-admin` to quickly set up a Django project. If you want to quickly obtain a runnable blank application similar to the example program `django_example`, you can follow these steps:

1. Initialize the Django project `copy_django_example`:

    ```bash
    pip install -r requirement.txt
    django-admin startproject copy_django_example
    cd copy_django_example
    ```

2. Change the `DATABASES` configuration:

    1. Open the `copy_django_example/settings.py` configuration file.
    2. Change the `DATABASES` section from pointing to the local SQLite configuration to the information of the TiDB cluster:

        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django_tidb',
                'NAME': 'django',
                'USER': 'root',
                'PASSWORD': '',
                'HOST': '127.0.0.1',
                'PORT': 4000,
            },
        }
        DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
        ```

    3. Since this example does not require cross-site request forgery (CSRF) protection, you need to comment out or remove `CsrfViewMiddleware` from the `MIDDLEWARE` section. The modified `MIDDLEWARE` should be as follows:

        ```python
        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            # 'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]
        ```

You have now completed a blank application that has the same dependencies as the example application. If you want to further explore the usage of Django, you can refer to:

- [Django Documentation](https://docs.djangoproject.com/en/3.2/)
- [Django Tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial01/)
