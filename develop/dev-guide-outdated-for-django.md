---
title: App Development for Django
summary: Learn how to build a simple Python application using TiDB and Django.
---

# Django のアプリ開発 {#app-development-for-django}

> **ノート：**
>
> このレガシー ドキュメントは古く、その後更新されません。詳細は[開発者ガイドの概要](/develop/dev-guide-overview.md)を参照してください。

このチュートリアルでは、TiDB と Django に基づいて単純な Python アプリケーションを構築する方法を示します。ここで構築するサンプル アプリケーションは、顧客情報と注文情報を追加、クエリ、および更新できるシンプルな CRM ツールです。

## ステップ 1. TiDB クラスターを開始する {#step-1-start-a-tidb-cluster}

ローカルstorageで疑似 TiDB クラスターを開始します。

```bash
docker run -p 127.0.0.1:$LOCAL_PORT:4000 pingcap/tidb:v5.1.0
```

上記のコマンドは、モック TiKV を使用して一時的な単一ノード クラスターを開始します。クラスタはポート`$LOCAL_PORT`でリッスンします。クラスターが停止すると、データベースに対して既に行われた変更は保持されません。

> **ノート：**
>
> 本番用の「実際の」TiDB クラスターをデプロイするには、次のガイドを参照してください。
>
> -   [TiUP for On-Premises を使用して TiDBをデプロイ](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup)
> -   [TiDB を Kubernetes にデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable)
>
> [TiDB Cloudを使用する](https://pingcap.com/products/tidbcloud/) 、TiDB のフルマネージド Database-as-a-Service (DBaaS) も可能です。

## ステップ 2. データベースを作成する {#step-2-create-a-database}

1.  SQL シェルで、アプリケーションが使用する`django`データベースを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE django;
    ```

2.  アプリケーションの SQL ユーザーを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE USER <username> IDENTIFIED BY <password>;
    ```

    ユーザー名とパスワードをメモします。プロジェクトを初期化するときに、アプリケーション コードでそれらを使用します。

3.  作成した SQL ユーザーに必要な権限を付与します。

    {{< copyable "" >}}

    ```sql
    GRANT ALL ON django.* TO <username>;
    ```

## ステップ 3. 仮想環境を設定してプロジェクトを初期化する {#step-3-set-virtual-environments-and-initialize-the-project}

1.  Python の依存関係およびパッケージ マネージャーである[詩](https://python-poetry.org/docs/)使用して、仮想環境を設定し、プロジェクトを初期化します。

    詩は、システムの依存関係を他の依存関係から分離し、依存関係の汚染を回避できます。次のコマンドを使用して、Poetry をインストールします。

    {{< copyable "" >}}

    ```bash
    pip install --user poetry
    ```

2.  Poetry を使用して開発環境を初期化します。

    {{< copyable "" >}}

    ```bash
    poetry init --no-interaction --dependency django
    poetry run django-admin startproject tidb_example

    mv pyproject.toml ./tidb_example
    cd tidb_example

    poetry add django-tidb

    poetry shell
    ```

3.  構成ファイルを変更します。 `tidb_example/settings.py`の構成は以下の通りです。

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

    上記の構成を次のように変更します。これは TiDB への接続に使用されます。

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

## ステップ 4. アプリケーション ロジックを記述する {#step-4-write-the-application-logic}

アプリケーションのデータベース接続を構成したら、アプリケーションの構築を開始できます。アプリケーション ロジックを記述するには、モデルを構築し、コントローラーを構築し、URL ルートを定義する必要があります。

1.  `models.py`というファイルで定義されているモデルを構築します。以下のサンプル コードをコピーして、新しいファイルに貼り付けることができます。

    {{< copyable "" >}}

    ```python
    from django.db import models

    class Orders(models.Model):
        id = models.AutoField(primary_key=True)
        username = models.CharField(max_length=250)
        price = models.FloatField()
    ```

2.  `views.py`というファイルにクラスベースのビューを作成します。以下のサンプル コードをコピーして、新しいファイルに貼り付けることができます。

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

3.  `urls.py`というファイルで URL ルートを定義します。 Django プロジェクトの作成時に`django-admin`コマンドライン ツールがこのファイルを生成したため、このファイルは`tidb_example/tidb_example`に既に存在しているはずです。以下のサンプル コードをコピーして、既存の`urls.py`ファイルに貼り付けることができます。

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

## ステップ 5. Django アプリケーションをセットアップして実行する {#step-5-set-up-and-run-the-django-application}

`tidb_example`番上のディレクトリで、 [`manage.py`](https://docs.djangoproject.com/en/3.1/ref/django-admin/)スクリプトを使用して、アプリケーションのデータベースを初期化する[Django の移行](https://docs.djangoproject.com/en/3.1/topics/migrations/)を作成します。

```bash
python manage.py makemigrations tidb_example
python manage.py migrate tidb_example
python manage.py migrate
```

次に、アプリケーションを開始します。

```python
python3 manage.py runserver 0.0.0.0:8000
```

サンプル データを挿入してアプリケーションをテストするには、次のコマンドを実行します。

```bash
curl --request POST '127.0.0.1:8000/order/' \
--data-raw '{
    "uid": 1,
    "price": 3.12
}'

curl --request PATCH '127.0.0.1:8000/order/' --data-raw '{ "oid": 1, "price": 312 }'

curl --request GET '127.0.0.1:8000/order/' --data-raw '{ "oid": 1 }'
```

データの挿入が成功したかどうかを確認するには、SQL シェルでターミナルを開いて確認します。

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

上記の結果は、データの挿入が成功したことを示しています。次に、挿入されたデータを削除できます。

```bash
curl --request DELETE '127.0.0.1:8000/order/' --data-raw '{ "oid": 1 }'
```
