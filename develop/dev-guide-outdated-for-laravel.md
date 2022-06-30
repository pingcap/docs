---
title: App Development for Laravel
summary: Learn how to build a simple PHP application based on TiDB and Laravel.
aliases: ['/appdev/dev/for-laravel']
---

# Laravelのアプリ開発 {#app-development-for-laravel}

> **ノート：**
>
> このドキュメントはアーカイブされています。これは、このドキュメントがその後更新されないことを示しています。詳細については、 [開発者ガイドの概要](/develop/dev-guide-overview.md)を参照してください。

このチュートリアルでは、Laravelを使用してTiDBに基づく単純なPHPアプリケーションを構築する方法を示します。ここで構築するサンプルアプリケーションは、顧客および注文情報を追加、照会、および更新できる単純なCRMツールです。

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
> -   [オンプレミスにデプロイを使用してTiDBを導入する](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup)
> -   [KubernetesにTiDBをデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable)
>
> また、無料トライアルを提供するフルマネージドのサービスとしてのデータベース（ [TiDB Cloudを使用する](https://pingcap.com/products/tidbcloud/) ）を使用することもできます。

## ステップ2.データベースを作成する {#step-2-create-a-database}

1.  SQLシェルで、アプリケーションが使用する`laravel_demo`のデータベースを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE laravel_demo;
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
    GRANT ALL ON laravel_demo.* TO <username>;
    ```

## ステップ3.Laravelプロジェクトを準備します {#step-3-prepare-your-laravel-project}

1.  Composerをインストールします。

    Laravelは、PHPの依存関係マネージャーである[作曲](https://getcomposer.org/)を使用して、依存関係を管理します。 Laravelを使用する前に、Composerがマシンにインストールされていることを確認してください。

    {{< copyable "" >}}

    ```bash
    brew install composer
    ```

    > **ノート：**
    >
    > インストール方法は、プラットフォームによって異なる場合があります。詳細については、 [インストール-Linux/Unix / macOS](https://getcomposer.org/doc/00-intro.md#installation-linux-unix-macos)を参照してください。

2.  Laravelをインストールします。

    Laravelインストーラーをダウンロードし、Composerを使用してLaravelフレームワークをインストールします。

    {{< copyable "" >}}

    ```bash
    composer global require laravel/installer
    ```

3.  プロジェクトを作成します。

    Laravelがインストールされたので、次のコマンドを使用してプロジェクトを開始できます。

    {{< copyable "" >}}

    ```bash
    laravel new laravel-demo
    ```

4.  構成を編集します。

    Laravelプロジェクトを作成したら、アプリケーションがTiDBに接続するための構成ファイルを編集する必要があります。

    {{< copyable "" >}}

    ```
    DB_CONNECTION=mysql
    DB_HOST=127.0.0.1
    DB_PORT=4000
    DB_DATABASE=laravel_demo
    DB_USERNAME=root
    DB_PASSWORD=
    ```

## ステップ4.アプリケーションロジックを記述します {#step-4-write-the-application-logic}

アプリケーションのデータベース接続を構成した後、アプリケーションの構築を開始できます。アプリケーションロジックを作成するには、モデルを定義し、コントローラーを作成し、URLルートを更新する必要があります。

### モジュールを定義する {#define-modules}

Laravelは、ORMフレームワークである[雄弁](https://laravel.com/docs/8.x/eloquent)モデルを使用して、テーブルを操作します。モデルは通常、 `app\Models`ディレクトリに配置されます。次の手順を実行してモデルを作成し、モデルを対応するテーブルにマップします。

1.  `make:model` [職人コマンド](https://laravel.com/docs/8.x/artisan)を使用して新しいモデルを生成し、 [データベースの移行](https://laravel.com/docs/8.x/migrations)を生成します。

    {{< copyable "" >}}

    ```bash
    php artisan make:model Order -m
    php artisan make:model Customer -m
    ```

    新しい移行は`database/migrations`のディレクトリに配置されます。

2.  `database/migrations/2021_10_08_064043_order.php`のファイルを編集して、注文テーブルを作成します。ファイル名は時間の経過とともに変化します。

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

3.  `database/migrations/2021_10_08_064056_customer.php`のファイルを編集してcustomerテーブルを作成します。ファイル名は時間の経過とともに変化します。

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

4.  `migrate`を使用してテーブルを生成し[職人コマンド](https://laravel.com/docs/8.x/artisan) 。

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

5.  `app/Models/Order.php`のファイルを編集して、 `Order`のモデルに使用するテーブルをフレームワークに指示します。

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

6.  `app/Models/Customer.php`のファイルを編集して、 `customer`のモデルに使用するテーブルをフレームワークに指示します。

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

### コントローラを作成する {#create-the-controller}

1.  コマンドラインから[コントローラ](https://laravel.com/docs/8.x/controllers)を作成するには、次のコマンドを実行します。

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

    {{&lt;コピー可能&quot;&quot;&gt;}}

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

### URLルートを更新します {#update-the-url-routes}

URLルーティングを使用すると、要求URLを受け入れるようにアプリケーションを構成できます。アプリケーションの[ルート](https://laravel.com/docs/8.x/routing)のほとんどは、 `app/api.php`ファイルで定義されています。最も単純なLaravelルートは、URIとClosureコールバックで構成されています。 `api.php`ファイルには、このデモのすべてのコードが含まれています。

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

## ステップ5.Laravelアプリケーションを実行します {#step-5-run-the-laravel-application}

PHPがローカルにインストールされていて、PHPの組み込み開発サーバーを使用してアプリケーションを提供する場合は、serveArtisanコマンドを使用して開発サーバーを`http://localhost:8000`から開始できます。

{{< copyable "" >}}

```bash
php artisan serve
```

いくつかのサンプルデータを挿入してアプリケーションをテストするには、次のコマンドを実行します。

{{< copyable "" >}}

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/customer' --form 'name="Peter"'

curl --location --request POST 'http://127.0.0.1:8000/api/order' --form 'cid=1' --form 'price="3.12"'

curl --location --request POST 'http://127.0.0.1:8000/api/order/1' --form 'price="312"'

curl --location --request GET 'http://127.0.0.1:8000/api/order?cid=1'
```

挿入が成功したかどうかを確認するには、SQLシェルで次のステートメントを実行します。

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

上記の結果は、データ挿入が成功したことを示しています。
