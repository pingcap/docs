---
title: Connect to TiDB with MyBatis
summary: MyBatisを使用してTiDBに接続する方法を学びましょう。このチュートリアルでは、MyBatisを使用してTiDBと連携するJavaのサンプルコードを紹介します。
aliases: ['/ja/tidb/stable/dev-guide-sample-application-java-mybatis/','/ja/tidb/dev/dev-guide-sample-application-java-mybatis/','/ja/tidbcloud/dev-guide-sample-application-java-mybatis/']
---

# MyBatisを使用してTiDBに接続する {#connect-to-tidb-with-mybatis}

TiDBはMySQL互換のデータベースであり、 [MyBatis](https://mybatis.org/mybatis-3/index.html)は人気の高いオープンソースのJava ORMです。

このチュートリアルでは、TiDBとMyBatisを使用して以下のタスクを実行する方法を学ぶことができます。

-   環境をセットアップしてください。
-   MyBatisを使用してTiDBに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   **Java Development Kit (JDK) 17**以降が必要です。業務要件や個人のニーズに応じて、 [OpenJDK](https://openjdk.org/)または[Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/)を選択できます。
-   [メイブン](https://maven.apache.org/install.html)**3.8**以上。
-   [Git](https://git-scm.com/downloads) 。
-   TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## TiDBに接続するには、サンプルアプリを実行してください。 {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプルアプリケーションコードを実行してTiDBに接続する方法を説明します。

### ステップ1：サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプルコードリポジトリをクローンするには、ターミナルウィンドウで以下のコマンドを実行してください。

```shell
git clone https://github.com/tidb-samples/tidb-java-mybatis-quickstart.git
cd tidb-java-mybatis-quickstart
```

### ステップ2：接続情報を設定する {#step-2-configure-connection-information}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **Connect With は**`General`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **ヒント：**
    >
    > プログラムがWindows Subsystem for Linux（WSL）上で実行されている場合は、対応するLinuxディストリビューションに切り替えてください。

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

5.  `env.sh.example`をコピーして`env.sh`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp env.sh.example env.sh
    ```

6.  対応する接続​​文字列`env.sh`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    必ずプレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに置き換えてください。

    TiDB Cloud Starter は安全な接続を必要とします。そのため、 `USE_SSL`の値を`true`に設定する必要があります。

7.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、「**接続タイプ」**ドロップダウンリストから**「パブリック」**を選択し、 **「CA証明書」**をクリックしてCA証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] をクリックするか、「IP アクセス リストを設定する」**の手順に従って[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)。

    TiDB Cloud Dedicated は、**パブリック**接続タイプに加えて、**プライベート エンドポイント**および**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud Dedicatedクラスタに接続します](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  `env.sh.example`をコピーして`env.sh`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp env.sh.example env.sh
    ```

5.  対応する接続​​文字列`env.sh`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```shell
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    必ずプレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに置き換えてください。

6.  `env.sh`ファイルを保存します。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  `env.sh.example`をコピーして`env.sh`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp env.sh.example env.sh
    ```

2.  対応する接続​​文字列`env.sh`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    プレースホルダー`{}`を接続パラメータに置き換え、 `USE_SSL` `false`に設定してください。TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `env.sh`ファイルを保存します。

</div>
</SimpleTab>

### ステップ3：コードを実行して結果を確認する {#step-3-run-the-code-and-check-the-result}

1.  サンプルコードを実行するには、以下のコマンドを実行してください。

    ```shell
    make
    ```

2.  [期待される出力.txt](https://github.com/tidb-samples/tidb-java-mybatis-quickstart/blob/main/Expected-Output.txt)をチェックして、出力が一致するかどうかを確認してください。

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-java-mybatis-quickstart](https://github.com/tidb-samples/tidb-java-mybatis-quickstart)リポジトリを参照してください。

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

`${tidb_jdbc_url}` 、 `${tidb_user}` 、および`${tidb_password}`を、ご使用のTiDBの実際の値に置き換えてください。また、 `${mapper_location}`マッパーXML設定ファイルのパスに置き換えてください。複数のマッパーXML設定ファイルがある場合は、それぞれに`<mapper/>`タグを追加する必要があります。次に、次の関数を定義します。

```java
public SqlSessionFactory getSessionFactory() {
    InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
    SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(inputStream);
}
```

### データを挿入する {#insert-data}

マッパーXMLにノードを追加し、XML設定ファイルの`mapper.namespace`属性で設定されたインターフェースクラスに、同じ名前の関数を追加します。

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

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

マッパーXMLにノードを追加し、XML設定ファイルの`mapper.namespace`属性で設定されているインターフェースクラスに、同じ名前の関数を追加します。具体的には、MyBatisクエリ関数の戻り値の型として`resultMap`を使用する場合は、 `<resultMap/>`ノードが正しく設定されていることを確認してください。

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

### データの更新 {#update-data}

マッパーXMLにノードを追加し、XML設定ファイルの`mapper.namespace`属性で設定されたインターフェースクラスに、同じ名前の関数を追加します。

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

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

マッパーXMLにノードを追加し、XML設定ファイルの`mapper.namespace`属性で設定されたインターフェースクラスに、同じ名前の関数を追加します。

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

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 次のステップ {#next-steps}

-   MyBatis の使用法について詳しくは[MyBatisのドキュメント](http://www.mybatis.org/mybatis-3/)ご覧ください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。
-   Java開発者向けのコース「 [JavaからTiDBを操作する](https://eng.edu.pingcap.com/catalog/info/id:212)を通じて学習します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
