---
title: Connect to TiDB with MyBatis
summary: MyBatisを使ってTiDBに接続する方法を学びましょう。このチュートリアルでは、MyBatisを使ってTiDBを操作するJavaサンプルコードを紹介します。
---

# MyBatisでTiDBに接続する {#connect-to-tidb-with-mybatis}

TiDB は MySQL 互換のデータベースであり、 [マイバティス](https://mybatis.org/mybatis-3/index.html)人気のオープンソースのJava ORM です。

このチュートリアルでは、TiDB と MyBatis を使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   MyBatis を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的なCRUD操作用の[サンプルコードスニペット](#sample-code-snippets)見つけることもできます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Dedicated、および TiDB Self-Managed で機能します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   **Java Development Kit (JDK) 17**以上。ビジネスおよび個人の要件に応じて、 [オープンJDK](https://openjdk.org/)または[オラクル JDK](https://www.oracle.com/hk/java/technologies/downloads/)選択できます。
-   [メイヴン](https://maven.apache.org/install.html) **3.8**以上。
-   [ギット](https://git-scm.com/downloads) 。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Starter クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Starter クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプルアプリを実行してTiDBに接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプル コード リポジトリのクローンを作成するには、ターミナル ウィンドウで次のコマンドを実行します。

```shell
git clone https://github.com/tidb-samples/tidb-java-mybatis-quickstart.git
cd tidb-java-mybatis-quickstart
```

### ステップ2: 接続情報を構成する {#step-2-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています

    -   **ブランチ**は`main`に設定されています

    -   **接続先が**`General`に設定されています

    -   **オペレーティング システムは**環境に適合します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」を**クリックして新しいパスワードを生成することができます。

5.  次のコマンドを実行して`env.sh.example`コピーし、名前を`env.sh`に変更します。

    ```shell
    cp env.sh.example env.sh
    ```

6.  対応する接続文字列をコピーして、 `env.sh`ファイルに貼り付けます。結果の例は次のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメータに置き換えてください。

    TiDB Cloud Starterは安全な接続を必要とします。そのため、 `USE_SSL`を`true`に設定する必要があります。

7.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストをまだ設定していない場合は、 **「IP アクセス リストの設定」を**クリックするか、手順[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って、最初の接続の前に設定してください。

    TiDB Cloud Dedicatedは、**パブリック**接続タイプに加えて、**プライベートエンドポイント**と**VPCピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)ご覧ください。

4.  次のコマンドを実行して`env.sh.example`コピーし、名前を`env.sh`に変更します。

    ```shell
    cp env.sh.example env.sh
    ```

5.  対応する接続文字列をコピーして、 `env.sh`ファイルに貼り付けます。結果の例は次のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメータに置き換えてください。

6.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Self-Managed">

1.  次のコマンドを実行して`env.sh.example`コピーし、名前を`env.sh`に変更します。

    ```shell
    cp env.sh.example env.sh
    ```

2.  対応する接続文字列をコピーして、 `env.sh`ファイルに貼り付けます。結果の例は次のとおりです。

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    プレースホルダー`{}`接続パラメータに置き換え、 `USE_SSL`を`false`に設定してください。TiDBをローカルで実行している場合、デフォルトのホストアドレスは`127.0.0.1`で、パスワードは空です。

3.  `env.sh`ファイルを保存します。

</div>
</SimpleTab>

### ステップ3: コードを実行して結果を確認する {#step-3-run-the-code-and-check-the-result}

1.  サンプル コードを実行するには、次のコマンドを実行します。

    ```shell
    make
    ```

2.  [期待出力.txt](https://github.com/tidb-samples/tidb-java-mybatis-quickstart/blob/main/Expected-Output.txt)チェックして、出力が一致するかどうかを確認します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-java-mybatis-クイックスタート](https://github.com/tidb-samples/tidb-java-mybatis-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

MyBatis設定ファイル`mybatis-config.xml`を編集します。

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

`${tidb_jdbc_url}` `${tidb_user}` TiDBクラスタの実際の値に置き換えてください。また、 `${mapper_location}` `${tidb_password}` XML設定ファイルのパスに置き換えてください。マッパーXML設定ファイルが複数ある場合は、それぞれに`<mapper/>`タグを追加する必要があります。次に、以下の関数を定義します。

```java
public SqlSessionFactory getSessionFactory() {
    InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
    SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
}
```

### データを挿入する {#insert-data}

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

詳細については[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

マッパーXMLにノードを追加し、XML設定ファイルの`mapper.namespace`属性で設定されたインターフェースクラスに同じ名前の関数を追加します。特に、MyBatisクエリ関数の戻り値の型として`resultMap`使用する場合は、 `<resultMap/>`ノードが正しく設定されていることを確認してください。

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

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

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

詳細については[データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

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

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 次のステップ {#next-steps}

-   MyBatis の使い方を[MyBatisのドキュメント](http://www.mybatis.org/mybatis-3/)から詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入する](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB認定](https://www.pingcap.com/education/certification/)獲得します。
-   Java開発者向けコースを通じて学習します: [JavaからTiDBを操作する](https://eng.edu.pingcap.com/catalog/info/id:212) .

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
