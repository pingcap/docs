---
title: App Development for Django
summary: Learn how to build a simple Python application using TiDB and Django.
aliases: ['/appdev/dev/for-django']
---

# Djangoのアプリ開発 {#app-development-for-django}

> **ノート：**
>
> このドキュメントはアーカイブされています。これは、このドキュメントがその後更新されないことを示しています。詳細については、 [開発者ガイドの概要](/develop/dev-guide-overview.md)を参照してください。

このチュートリアルでは、TiDBとDjangoに基づいて簡単なPythonアプリケーションを構築する方法を示します。ここで構築するサンプルアプリケーションは、顧客および注文情報を追加、照会、および更新できる単純なCRMツールです。

## 手順1.TiDBクラスタを開始します {#step-1-start-a-tidb-cluster}

ローカルストレージで疑似TiDBクラスタを開始します。

{{< copyable "" >}}

```bash
docker run -p 127.0.0.1:$LOCAL_PORT:4000 pingcap/tidb:v5.1.0
```

上記のコマンドは、モックTiKVを使用して一時的な単一ノードクラスタを開始します。クラスタはポート`$LOCAL_PORT`でリッスンします。クラスタが停止した後、データベースにすでに加えられた変更は保持されません。

> **ノート：**
>
> 「実際の」TiDBクラスタを実稼働環境にデプロイするには、次のガイドを参照してください。
>
> -   [オンプレミスのTiUPを使用してTiDBをデプロイ](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup)
> -   [KubernetesにTiDBをデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable)
>
> また、無料トライアルを提供するフルマネージドのDatabase-as- [TiDB Cloudを使用する](https://pingcap.com/products/tidbcloud/) -Service（DBaaS）も可能です。

## ステップ2.データベースを作成します {#step-2-create-a-database}

1.  SQLシェルで、アプリケーションが使用する`django`のデータベースを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE django;
    ```

2.  アプリケーションのSQLユーザーを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE USER <username> IDENTIFIED BY <password>;
    ```

    ユーザー名とパスワードをメモします。プロジェクトを初期化するときに、アプリケーションコードでそれらを使用します。

3.  作成したSQLユーザーに必要な権限を付与します。

    {{< copyable "" >}}

    ```sql
    GRANT ALL ON django.* TO <username>;
    ```

## ステップ3.仮想環境を設定し、プロジェクトを初期化します {#step-3-set-virtual-environments-and-initialize-the-project}

1.  Pythonの依存関係およびパッケージマネージャーである[詩](https://python-poetry.org/docs/)を使用して、仮想環境を設定し、プロジェクトを初期化します。

    詩は、システムの依存関係を他の依存関係から分離し、依存関係の汚染を回避できます。次のコマンドを使用して、Poetryをインストールします。

    {{< copyable "" >}}

    ```bash
    pip install --user poetry
    ```

2.  Poetryを使用して開発環境を初期化します。

    {{< copyable "" >}}

    ```bash
    poetry init --no-interaction --dependency django
    poetry run django-admin startproject tidb_example

    mv pyproject.toml ./tidb_example
    cd tidb_example

    poetry add django-tidb

    poetry shell
    ```

3.  構成ファイルを変更します。 `tidb_example/settings.py`の構成は次のとおりです。

    {{< copyable "" >}}

    ```python
    USE_TZ = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    ```

    上記の構成を次のように変更します。これは、TiDBへの接続に使用されます。

    {{< copyable "" >}}

    ```python
    USE_TZ = False

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

## ステップ4.アプリケーションロジックを記述します {#step-4-write-the-application-logic}

アプリケーションのデータベース接続を構成した後、アプリケーションの構築を開始できます。アプリケーションロジックを作成するには、モデルを構築し、コントローラーを構築し、URLルートを定義する必要があります。

1.  `models.py`というファイルで定義されているモデルをビルドします。以下のサンプルコードをコピーして、新しいファイルに貼り付けることができます。

    {{< copyable "" >}}

    ```python
    from django.db import models

    class Orders(models.Model):
        id = models.AutoField(primary_key=True)
        username = models.CharField(max_length=250)
        price = models.FloatField()
    ```

2.  `views.py`というファイルにクラスベースのビューを作成します。以下のサンプルコードをコピーして、新しいファイルに貼り付けることができます。

    {{< copyable "" >}}

    ```python
    from django.http import JsonResponse, HttpResponse
    from django.utils.decorators import method_decorator
    from django.views.generic import View
    from django.views.decorators.csrf import csrf_exempt
    from django.db import Error, OperationalError
    from django.db.transaction import atomic
    from functools import wraps
    import json
    import sys
    import time

    from .models import *

    def retry_on_exception(view, num_retries=3, on_failure=HttpResponse(status=500), delay_=0.5, backoff_=1.5):
        @wraps(view)
        def retry(*args, **kwargs):
            delay = delay_
            for i in range(num_retries):
                try:
                    return view(*args, **kwargs)
                except Exception as e:
                    return on_failure
        return retry


    class PingView(View):
        def get(self, request, *args, **kwargs):
            return HttpResponse("python/django", status=200)


    @method_decorator(csrf_exempt, name='dispatch')
    class OrderView(View):
        def get(self, request, id=None, *args, **kwargs):
            if id is None:
                orders = list(Orders.objects.values())
            else:
                orders = list(Orders.objects.filter(id=id).values())
            return JsonResponse(orders, safe=False)


        @retry_on_exception
        @atomic
        def post(self, request, *args, **kwargs):
            form_data = json.loads(request.body.decode())
            username = form_data['username']
            price = form_data['price']
            c = Orders(username=username, price=price)
            c.save()
            return HttpResponse(status=200)

        @retry_on_exception
        @atomic
        def delete(self, request, id=None, *args, **kwargs):
            if id is None:
                return HttpResponse(status=404)
            Orders.objects.filter(id=id).delete()
            return HttpResponse(status=200)
    ```

3.  `urls.py`というファイルでURLルートを定義します。 `django-admin`コマンドラインツールはDjangoプロジェクトの作成時にこのファイルを生成したため、ファイルはすでに`tidb_example/tidb_example`に存在しているはずです。以下のサンプルコードをコピーして、既存の`urls.py`ファイルに貼り付けることができます。

    {{< copyable "" >}}

    ```python
    from django.contrib import admin
    from django.urls import path
    from django.conf.urls import url

    from .views import OrderView, PingView

    urlpatterns = [
        path('admin/', admin.site.urls),

        url('ping/', PingView.as_view()),

        url('order/', OrderView.as_view(), name='order'),
        url('order/<int:id>/', OrderView.as_view(), name='order'),
    ]
    ```

## ステップ5.Djangoアプリケーションをセットアップして実行します {#step-5-set-up-and-run-the-django-application}

最上位の`tidb_example`ディレクトリで、 [`manage.py`](https://docs.djangoproject.com/en/3.1/ref/django-admin/)スクリプトを使用して、アプリケーションのデータベースを初期化する[Djangoの移行](https://docs.djangoproject.com/en/3.1/topics/migrations/)を作成します。

{{< copyable "" >}}

```bash
python manage.py makemigrations tidb_example
python manage.py migrate tidb_example
python manage.py migrate
```

次に、アプリケーションを起動します。

{{< copyable "" >}}

```python
python3 manage.py runserver 0.0.0.0:8000
```

いくつかのサンプルデータを挿入してアプリケーションをテストするには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
curl --request POST '127.0.0.1:8000/order/' \
--data-raw '{
    "uid": 1,
    "price": 3.12
}'

curl --request PATCH '127.0.0.1:8000/order/' --data-raw '{ "oid": 1, "price": 312 }'

curl --request GET '127.0.0.1:8000/order/' --data-raw '{ "oid": 1 }'
```

データの挿入が成功したかどうかを確認するには、SQLシェルでターミナルを開いて以下を確認します。

{{< copyable "" >}}

```sql
MySQL root@127.0.0.1:(none)> select * from django.tidb_example_orders;
+-----+-----+-------+
| oid | uid | price |
+-----+-----+-------+
| 1   | 1   | 312.0 |
+-----+-----+-------+
1 row in set
Time: 0.008s
```

上記の結果は、データ挿入が成功したことを示しています。次に、挿入されたデータを削除できます。

{{< copyable "" >}}

```bash
curl --request DELETE '127.0.0.1:8000/order/' --data-raw '{ "oid": 1 }'
```
