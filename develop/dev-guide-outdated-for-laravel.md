---
title: App Development for Laravel
summary: Learn how to build a simple PHP application based on TiDB and Laravel.
aliases: ['/appdev/dev/for-laravel']
---

# Laravelのアプリ開発 {#app-development-for-laravel}

> **ノート：**
>
> このドキュメントはアーカイブされています。これは、このドキュメントがその後更新されないことを示しています。詳細は[開発者ガイドの概要](/develop/dev-guide-overview.md)を参照してください。

このチュートリアルでは、Laravel を使用して TiDB に基づく単純な PHP アプリケーションを構築する方法を示します。ここで構築するサンプル アプリケーションは、顧客情報と注文情報を追加、クエリ、および更新できるシンプルな CRM ツールです。

## ステップ 1. TiDB クラスターを開始する {#step-1-start-a-tidb-cluster}

ローカル ストレージで疑似 TiDB クラスターを開始します。

{{< copyable "" >}}

```bash
docker run -p 127.0.0.1:$LOCAL_PORT:4000 pingcap/tidb:v5.1.0
```

上記のコマンドは、モック TiKV を使用して一時的な単一ノード クラスターを開始します。クラスタはポート`$LOCAL_PORT`でリッスンします。クラスターが停止すると、データベースに対して既に行われた変更は保持されません。

> **ノート：**
>
> 実稼働用に「実際の」TiDB クラスターをデプロイするには、次のガイドを参照してください。
>
> -   [TiUP for On-Premises を使用して TiDB をデプロイ](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup)
> -   [TiDB を Kubernetes にデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable)
>
> また、無料試用版を提供する[TiDB Cloudを使用する](https://pingcap.com/products/tidbcloud/) 、完全に管理された Database-as-a-Service (DBaaS) を使用することもできます。

## ステップ 2. データベースを作成する {#step-2-create-a-database}

1.  SQL シェルで、アプリケーションが使用する`laravel_demo`のデータベースを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE laravel_demo;
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
    GRANT ALL ON laravel_demo.* TO <username>;
    ```

## ステップ 3. Laravel プロジェクトを準備する {#step-3-prepare-your-laravel-project}

1.  コンポーザーをインストールします。

    Laravel は、PHP の依存関係マネージャーである[作曲](https://getcomposer.org/)を使用して依存関係を管理します。 Laravel を使用する前に、Composer がマシンにインストールされていることを確認してください。

    {{< copyable "" >}}

    ```bash
    brew install composer
    ```

    > **ノート：**
    >
    > インストール方法は、プラットフォームによって異なる場合があります。詳細については、 [インストール - Linux / Unix / macOS](https://getcomposer.org/doc/00-intro.md#installation-linux-unix-macos)を参照してください。

2.  ララベルをインストールします。

    Laravel インストーラーをダウンロードし、Composer を使用して Laravel フレームワークをインストールします。

    {{< copyable "" >}}

    ```bash
    composer global require laravel/installer
    ```

3.  プロジェクトを作成します。

    Laravel がインストールされたので、次のコマンドを使用してプロジェクトを開始できます。

    {{< copyable "" >}}

    ```bash
    laravel new laravel-demo
    ```

4.  構成を編集します。

    Laravel プロジェクトを作成したら、アプリケーションが TiDB に接続するように構成ファイルを編集する必要があります。

    {{< copyable "" >}}

    ```
    DB_CONNECTION=mysql
    DB_HOST=127.0.0.1
    DB_PORT=4000
    DB_DATABASE=laravel_demo
    DB_USERNAME=root
    DB_PASSWORD=
    ```

## ステップ 4. アプリケーション ロジックを記述する {#step-4-write-the-application-logic}

アプリケーションのデータベース接続を構成したら、アプリケーションの構築を開始できます。アプリケーション ロジックを記述するには、モデルを定義し、コントローラーを作成し、URL ルートを更新する必要があります。

### モジュールを定義する {#define-modules}

Laravel は、ORM フレームワークである[雄弁](https://laravel.com/docs/8.x/eloquent)モデルを使用して、テーブルと対話します。通常、モデルは`app\Models`ディレクトリに配置されます。次の手順に従ってモデルを作成し、モデルを対応するテーブルにマップします。

1.  `make:model` [職人の命令](https://laravel.com/docs/8.x/artisan)を使用して新しいモデルを生成し、 [データベースの移行](https://laravel.com/docs/8.x/migrations)を生成します。

    {{< copyable "" >}}

    ```bash
    php artisan make:model Order -m
    php artisan make:model Customer -m
    ```

    新しい移行は`database/migrations`ディレクトリに配置されます。

2.  `database/migrations/2021_10_08_064043_order.php`ファイルを編集して order テーブルを作成します。ファイル名は、時間の経過とともに変化します。

    {{< copyable "" >}}

    ```php
    <?php

    use Illuminate\Database\Migrations\Migration;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    class CreateOrdersTable extends Migration
    {
        /**
        * Runs the migrations.
        *
        * @return void
        */
        public function up()
        {
            Schema::create('order', function (Blueprint $table) {
                $table->bigIncrements('oid');
                $table->bigInteger('cid');
                $table->float('price');
            });
        }

        /**
        * Reverses the migrations.
        *
        * @return void
        */
        public function down()
        {
            Schema::dropIfExists('order');
        }
    }
    ```

3.  `database/migrations/2021_10_08_064056_customer.php`ファイルを編集して customer テーブルを作成します。ファイル名は、時間の経過とともに変化します。

    {{< copyable "" >}}

    ```php
    <?php

    use Illuminate\Database\Migrations\Migration;
    use Illuminate\Database\Schema\Blueprint;
    use Illuminate\Support\Facades\Schema;

    class CreateCustomersTable extends Migration
    {
        /**
         * Runs the migrations.
         *
         * @return void
         */
        public function up()
        {
            Schema::create('customer', function (Blueprint $table) {
                $table->bigIncrements('cid');
                $table->string('name',100);
            });
        }

        /**
         * Reverses the migrations.
         *
         * @return void
         */
        public function down()
        {
            Schema::dropIfExists('customer');
        }
    }
    ```

4.  `migrate` [職人の命令](https://laravel.com/docs/8.x/artisan)を使用してテーブルを生成します。

    {{< copyable "" >}}

    ```php
    > $ php artisan migrate
    Migration table created successfully.
    Migrating: 2014_10_12_000000_create_users_table
    Migrated:  2014_10_12_000000_create_users_table (634.92ms)
    Migrating: 2014_10_12_100000_create_password_resets_table
    Migrated:  2014_10_12_100000_create_password_resets_table (483.58ms)
    Migrating: 2019_08_19_000000_create_failed_jobs_table
    Migrated:  2019_08_19_000000_create_failed_jobs_table (456.25ms)
    Migrating: 2019_12_14_000001_create_personal_access_tokens_table
    Migrated:  2019_12_14_000001_create_personal_access_tokens_table (877.47ms)
    Migrating: 2021_10_08_081739_create_orders_table
    Migrated:  2021_10_08_081739_create_orders_table (154.53ms)
    Migrating: 2021_10_08_083522_create_customers_table
    Migrated:  2021_10_08_083522_create_customers_table (82.02ms)
    ```

5.  `app/Models/Order.php`ファイルを編集して、 `Order`モデルに使用するテーブルをフレームワークに指示します。

    {{< copyable "" >}}

    ```php
    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Factories\HasFactory;
    use Illuminate\Database\Eloquent\Model;

    class Order extends Model
    {
        protected $table = 'order';

        protected $primaryKey = 'oid';

        public $timestamps = false;

        protected $fillable = [
            'cid',
            'price',
        ];

        protected $guarded = [
            'oid',
        ];

        protected $casts = [
            'uid'   => 'real',
            'price' => 'float',
        ];

        use HasFactory;
    }
    ```

6.  `app/Models/Customer.php`ファイルを編集して、 `customer`モデルに使用するテーブルをフレームワークに指示します。

    {{< copyable "" >}}

    ```php
    <?php

    namespace App\Models;

    use Illuminate\Database\Eloquent\Factories\HasFactory;
    use Illuminate\Database\Eloquent\Model;

    class Customer extends Model
    {
        use HasFactory;
        protected $table = 'customer';

        protected $primaryKey = 'cid';

        public $timestamps = false;

        protected $fillable = [
            'name',
        ];

        protected $guarded = [
            'cid',
        ];

        protected $casts = [
            'name'  => 'string',
            'cid' => 'int',
        ];
    }
    ```

### コントローラーを作成する {#create-the-controller}

1.  コマンド ラインから[コントローラ](https://laravel.com/docs/8.x/controllers)を作成するには、次のコマンドを実行します。

    {{< copyable "" >}}

    ```bash
    php artisan make:controller CustomerController
    php artisan make:controller OrderController
    ```

2.  `app/Http/Controllers/CustomerController.php`を編集して、 `customer`テーブルに対するアクションを制御します。

    {{< copyable "" >}}

    ```php
    <?php

    namespace App\Http\Controllers;

    use App\Models\Customer;
    use Illuminate\Http\Request;

    class CustomerController extends Controller
    {
        public function getByCid($cid)
        {
            $customer_info = Customer::where('cid',$cid)->get();
            if ($customer_info->count() > 0){
                return $customer_info;
            }
            return abort(404);
        }

        public function insert(Request $request) {
            return Customer::create(['name' => $request->name]);
        }
    }
    ```

3.  `app/Http/Controllers/OrderController.php`を編集して、 `order`テーブルに対するアクションを制御します。

    {{&lt;コピー可能な &quot;&quot; &gt;}}

    ```php
    <?php

    namespace App\Http\Controllers;

    use App\Models\Order;
    use Illuminate\Http\Request;

    class OrderController extends Controller
    {

        public function insert(Request $request) {
            return Order::create(['cid' => $request->cid, 'price' => $request->price]);
        }

        public function delete($oid)
        {
            return Order::where('oid', $oid)->delete();
        }

        public function updateByOid(Request $request, $oid)
        {
            return Order::where('oid', $oid)->update(['price' => $request->price]);
        }

        public function queryByCid(Request $request)
        {
            return Order::where('cid', $request->query('cid'))->get();
        }
    }
    ```

### URL ルートを更新する {#update-the-url-routes}

URL ルーティングを使用すると、リクエスト URL を受け入れるようにアプリケーションを構成できます。アプリケーションの[ルート](https://laravel.com/docs/8.x/routing)のほとんどは`app/api.php`ファイルで定義されています。最も単純な Laravel ルートは、URI と Closure コールバックで構成されます。 `api.php`ファイルには、このデモのすべてのコードが含まれています。

{{< copyable "" >}}

```php
<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\customerController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::get('/customer/{id}', 'App\Http\Controllers\CustomerController@getByCid');
Route::post('/customer', 'App\Http\Controllers\CustomerController@insert');


Route::post('/order', 'App\Http\Controllers\OrderController@insert');
Route::delete('/order/{oid}', 'App\Http\Controllers\OrderController@delete');
Route::post('/order/{oid}','App\Http\Controllers\OrderController@updateByOid');
Route::get('/order','App\Http\Controllers\OrderController@queryByCid');
```

## ステップ 5. Laravel アプリケーションを実行する {#step-5-run-the-laravel-application}

PHP がローカルにインストールされていて、PHP のビルトイン開発サーバーを使用してアプリケーションを提供したい場合は、 serve Artisan コマンドを使用して`http://localhost:8000`で開発サーバーを起動できます。

{{< copyable "" >}}

```bash
php artisan serve
```

サンプル データを挿入してアプリケーションをテストするには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/customer' --form 'name="Peter"'

curl --location --request POST 'http://127.0.0.1:8000/api/order' --form 'cid=1' --form 'price="3.12"'

curl --location --request POST 'http://127.0.0.1:8000/api/order/1' --form 'price="312"'

curl --location --request GET 'http://127.0.0.1:8000/api/order?cid=1'
```

挿入が成功したかどうかを確認するには、SQL シェルで次のステートメントを実行します。

{{< copyable "" >}}

```sql
MySQL root@127.0.0.1:(none)> select * from laravel_demo.order;
+-----+-----+-------+
| oid | uid | price |
+-----+-----+-------+
| 1   | 1   | 312.0 |
+-----+-----+-------+
1 row in set
Time: 0.008s
```

上記の結果は、データの挿入が成功したことを示しています。
