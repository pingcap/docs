---
title: Connect to TiDB with MyBatis
summary: Learn how to connect to TiDB using MyBatis. This tutorial gives Java sample code snippets that work with TiDB using MyBatis.
---

# MyBatis を使用して TiDB に接続する {#connect-to-tidb-with-mybatis}

TiDB は MySQL 互換データベースであり、 [マイバティス](https://mybatis.org/mybatis-3/index.html)は人気のあるオープンソースJava ORM です。

このチュートリアルでは、TiDB と MyBatis を使用して次のタスクを実行する方法を学習できます。

-   環境をセットアップします。
-   MyBatis を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> このチュートリアルは、TiDB サーバーレス、TiDB 専用、および TiDB セルフホストで動作します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   **Java開発キット (JDK) 17**以降。ビジネスや個人の要件に基づいて[OpenJDK](https://openjdk.org/)または[オラクルJDK](https://www.oracle.com/hk/java/technologies/downloads/)を選択できます。
-   [メイビン](https://maven.apache.org/install.html) **3.8**以上。
-   [ギット](https://git-scm.com/downloads) 。
-   TiDB クラスター。

<CustomContent platform="tidb">
  **TiDB クラスターがない場合は、次のように作成できます。**

  -   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
  -   [ローカル テスト TiDB クラスターをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。
</CustomContent>

<CustomContent platform="tidb-cloud">
  **TiDB クラスターがない場合は、次のように作成できます。**

  -   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
  -   [ローカル テスト TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。
</CustomContent>

## サンプル アプリを実行して TiDB に接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

### ステップ 1: サンプル アプリ リポジトリのクローンを作成する {#step-1-clone-the-sample-app-repository}

ターミナル ウィンドウで次のコマンドを実行して、サンプル コード リポジトリのクローンを作成します。

```shell
git clone https://github.com/tidb-samples/tidb-java-mybatis-quickstart.git
cd tidb-java-mybatis-quickstart
```

### ステップ 2: 接続情報を構成する {#step-2-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
  <div label="TiDB Serverless">
    1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

    2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

    3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

        -   **エンドポイント タイプは**`Public`に設定されます

        -   **[接続先] は**`General`に設定されています

        -   **オペレーティング システムが**環境に一致します。

        > **ヒント：**
        >
        > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

    4.  **「パスワードの作成」**をクリックしてランダムなパスワードを作成します。

        > **ヒント：**
        >
        > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成できます。

    5.  次のコマンドを実行して`env.sh.example`をコピーし、名前を`env.sh`に変更します。

        ```shell
        cp env.sh.example env.sh
        ```

    6.  対応する接続​​文字列をコピーして`env.sh`ファイルに貼り付けます。結果の例は次のとおりです。

        ```shell
        export TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
        export TIDB_PORT='4000'
        export TIDB_USER='{user}'  # e.g. xxxxxx.root
        export TIDB_PASSWORD='{password}'
        export TIDB_DB_NAME='test'
        export USE_SSL='true'
        ```

        プレースホルダー`{}` 、接続ダイアログから取得した接続パラメーターに必ず置き換えてください。

        TiDB サーバーレスには安全な接続が必要です。したがって、 `USE_SSL` ～ `true`の値を設定する必要があります。

    7.  `env.sh`ファイルを保存します。
  </div>

  <div label="TiDB Dedicated">
    1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

    2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

    3.  **「どこからでもアクセスを許可」**をクリックし、 **「TiDB クラスター CA のダウンロード」**をクリックして CA 証明書をダウンロードします。

        接続文字列の取得方法の詳細については、 [TiDB専用標準接続](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)を参照してください。

    4.  次のコマンドを実行して`env.sh.example`をコピーし、名前を`env.sh`に変更します。

        ```shell
        cp env.sh.example env.sh
        ```

    5.  対応する接続​​文字列をコピーして`env.sh`ファイルに貼り付けます。結果の例は次のとおりです。

        ```shell
        export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
        export TIDB_PORT='4000'
        export TIDB_USER='{user}'  # e.g. root
        export TIDB_PASSWORD='{password}'
        export TIDB_DB_NAME='test'
        export USE_SSL='false'
        ```

        プレースホルダー`{}` 、接続ダイアログから取得した接続パラメーターに必ず置き換えてください。

    6.  `env.sh`ファイルを保存します。
  </div>

  <div label="TiDB Self-Hosted">
    1.  次のコマンドを実行して`env.sh.example`をコピーし、名前を`env.sh`に変更します。

        ```shell
        cp env.sh.example env.sh
        ```

    2.  対応する接続​​文字列をコピーして`env.sh`ファイルに貼り付けます。結果の例は次のとおりです。

        ```shell
        export TIDB_HOST='{host}'
        export TIDB_PORT='4000'
        export TIDB_USER='root'
        export TIDB_PASSWORD='{password}'
        export TIDB_DB_NAME='test'
        export USE_SSL='false'
        ```

        必ずプレースホルダー`{}`接続パラメーターに置き換えて、 `USE_SSL`を`false`に設定してください。 TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

    3.  `env.sh`ファイルを保存します。
  </div>
</SimpleTab>

### ステップ 3: コードを実行して結果を確認する {#step-3-run-the-code-and-check-the-result}

1.  次のコマンドを実行してサンプル コードを実行します。

    ```shell
    make
    ```

2.  [予想される出力.txt](https://github.com/tidb-samples/tidb-java-mybatis-quickstart/blob/main/Expected-Output.txt)チェックして、出力が一致するかどうかを確認します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了できます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-java-mybatis-quickstart](https://github.com/tidb-samples/tidb-java-mybatis-quickstart)リポジトリを確認してください。

### TiDB に接続する {#connect-to-tidb}

MyBatis 構成ファイル`mybatis-config.xml`を編集します。

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <settings>
        <setting name="cacheEnabled" value="true"/>
        <setting name="lazyLoadingEnabled" value="false"/>
        <setting name="aggressiveLazyLoading" value="true"/>
        <setting name="logImpl" value="LOG4J"/>
    </settings>

    <environments default="development">
        <environment id="development">
            <!-- JDBC transaction manager -->
            <transactionManager type="JDBC"/>
            <!-- Database pool -->
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="${tidb_jdbc_url}"/>
                <property name="username" value="${tidb_user}"/>
                <property name="password" value="${tidb_password}"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <mapper resource="${mapper_location}.xml"/>
    </mappers>
</configuration>
```

`${tidb_jdbc_url}` 、 `${tidb_user}` 、および`${tidb_password}`必ず TiDB クラスターの実際の値に置き換えてください。また、 `${mapper_location}`マッパー XML 構成ファイルのパスに置き換えます。複数のマッパー XML 構成ファイルの場合は、それぞれに`<mapper/>`タグを追加する必要があります。次に、次の関数を定義します。

```java
public SqlSessionFactory getSessionFactory() {
    InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
    SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
}
```

### データの挿入 {#insert-data}

マッパー XML にノードを追加し、XML 構成ファイルの`mapper.namespace`属性で構成されたインターフェイス クラスに同じ名前の関数を追加します。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapper">
    <insert id="insert" parameterType="com.pingcap.model.Player">
    insert into player (id, coins, goods)
    values (#{id,jdbcType=VARCHAR}, #{coins,jdbcType=INTEGER}, #{goods,jdbcType=INTEGER})
    </insert>
</mapper>
```

詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

マッパー XML にノードを追加し、XML 構成ファイルの`mapper.namespace`属性で構成されたインターフェース クラスに同じ名前の関数を追加します。特に、MyBatis クエリ関数の戻り値の型として`resultMap`使用する場合は、 `<resultMap/>`ノードが正しく構成されていることを確認してください。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapper">
    <resultMap id="BaseResultMap" type="com.pingcap.model.Player">
        <constructor>
            <idArg column="id" javaType="java.lang.String" jdbcType="VARCHAR" />
            <arg column="coins" javaType="java.lang.Integer" jdbcType="INTEGER" />
            <arg column="goods" javaType="java.lang.Integer" jdbcType="INTEGER" />
        </constructor>
    </resultMap>

    <select id="selectByPrimaryKey" parameterType="java.lang.String" resultMap="BaseResultMap">
    select id, coins, goods
    from player
    where id = #{id,jdbcType=VARCHAR}
    </select>
</mapper>
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

マッパー XML にノードを追加し、XML 構成ファイルの`mapper.namespace`属性で構成されたインターフェイス クラスに同じ名前の関数を追加します。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapper">
    <update id="updateByPrimaryKey" parameterType="com.pingcap.model.Player">
    update player
    set coins = #{coins,jdbcType=INTEGER},
      goods = #{goods,jdbcType=INTEGER}
    where id = #{id,jdbcType=VARCHAR}
    </update>
</mapper>
```

詳細については、 [データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データの削除 {#delete-data}

マッパー XML にノードを追加し、XML 構成ファイルの`mapper.namespace`属性で構成されたインターフェイス クラスに同じ名前の関数を追加します。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapper">
    <delete id="deleteByPrimaryKey" parameterType="java.lang.String">
    delete from player
    where id = #{id,jdbcType=VARCHAR}
    </delete>
</mapper>
```

詳細については、 [データの削除](/develop/dev-guide-delete-data.md)を参照してください。

## 次のステップ {#next-steps}

-   MyBatis の詳しい使い方は[MyBatis のドキュメント](http://www.mybatis.org/mybatis-3/)からご覧ください。
-   TiDB アプリケーション[データの削除](/develop/dev-guide-delete-data.md) [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md)ベスト プラクティス[SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)は、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md)など) [データを更新する](/develop/dev-guide-update-data.md)参照[トランザクション](/develop/dev-guide-transaction-overview.md)てください。
-   プロフェッショナルを通じて[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。
-   Java開発者向けのコースを通じて[Javaから TiDB を操作する](https://eng.edu.pingcap.com/catalog/info/id:212)を学びます。

## 助けが必要？ {#need-help}

[不和](https://discord.gg/vYU9h56kAX)または[サポートチケットを作成する](https://support.pingcap.com/)について質問してください。
