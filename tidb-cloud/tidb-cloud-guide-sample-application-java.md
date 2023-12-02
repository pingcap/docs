---
title: Build a Simple CRUD App with TiDB and Java
summary: Learn how to build a simple CRUD application with TiDB and Java.
---

<!-- markdownlint-disable MD024 -->

<!-- markdownlint-disable MD029 -->

# TiDB とJavaを使用してシンプルな CRUD アプリを構築する {#build-a-simple-crud-app-with-tidb-and-java}

このドキュメントでは、TiDB とJavaを使用して単純な CRUD アプリケーションを構築する方法について説明します。

> **注記：**
>
> Java 8 以降のJavaバージョンを使用することをお勧めします。
>
> Spring Boot を使用してアプリケーション開発を行う場合は、 [Spring Boot を使用して TiDB アプリを構築する](/develop/dev-guide-sample-application-java-spring-boot.md)を参照してください。

## ステップ 1. TiDB クラスターを起動する {#step-1-launch-your-tidb-cluster}

<CustomContent platform="tidb">

TiDB クラスターの起動方法を紹介します。

**TiDB サーバーレス クラスターを使用する**

詳細な手順については、 [TiDB サーバーレスクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster)を参照してください。

**ローカルクラスターを使用する**

詳細な手順については、 [ローカルテストクラスターをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[TiUPを使用した TiDBクラスタのデプロイ](/production-deployment-using-tiup.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB サーバーレスクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster)を参照してください。

</CustomContent>

## ステップ 2. コードを取得する {#step-2-get-the-code}

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
```

<SimpleTab groupId="language">

<div label="Using Mybatis (Recommended)" value="mybatis">

[マイバティス](https://mybatis.org/mybatis-3/index.html)と比較すると、JDBC 実装はベスト プラクティスではない可能性があります。エラー処理ロジックを手動で記述する必要があり、コードを簡単に再利用できないため、コードが若干冗長になります。

Mybatis は、人気のあるオープンソースのJavaクラス永続フレームワークです。以下では[MyBatis ジェネレーター](https://mybatis.org/generator/quickstart.html) Maven プラグインとして使用して永続化レイヤーコードを生成します。

`plain-java-mybatis`ディレクトリに移動します。

```shell
cd plain-java-mybatis
```

このディレクトリの構造は次のとおりです。

    .
    ├── Makefile
    ├── pom.xml
    └── src
        └── main
            ├── java
            │   └── com
            │       └── pingcap
            │           ├── MybatisExample.java
            │           ├── dao
            │           │   └── PlayerDAO.java
            │           └── model
            │               ├── Player.java
            │               ├── PlayerMapper.java
            │               └── PlayerMapperEx.java
            └── resources
                ├── dbinit.sql
                ├── log4j.properties
                ├── mapper
                │   ├── PlayerMapper.xml
                │   └── PlayerMapperEx.xml
                ├── mybatis-config.xml
                └── mybatis-generator.xml

自動生成されるファイルは次のとおりです。

-   `src/main/java/com/pingcap/model/Player.java` : `Player`エンティティ クラス。
-   `src/main/java/com/pingcap/model/PlayerMapper.java` : `PlayerMapper`のインターフェース。
-   `src/main/resources/mapper/PlayerMapper.xml` : `Player`の XML マッピング。 Mybatis はこの構成を使用して、 `PlayerMapper`インターフェースの実装クラスを自動的に生成します。

これらのファイルを生成するための戦略は、 [マイバティスジェネレーター](https://mybatis.org/generator/quickstart.html)の構成ファイルである`mybatis-generator.xml`に書かれています。次の設定ファイルには、その使用方法を説明するコメントがあります。

```xml
<!DOCTYPE generatorConfiguration PUBLIC
 "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN"
 "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">

<generatorConfiguration>
    <!--
        <context/> entire document: https://mybatis.org/generator/configreference/context.html

        context.id: A unique identifier you like
        context.targetRuntime: Used to specify the runtime target for generated code.
            It has MyBatis3DynamicSql / MyBatis3Kotlin / MyBatis3 / MyBatis3Simple 4 selection to choice.
    -->
    <context id="simple" targetRuntime="MyBatis3">
        <!--
            <commentGenerator/> entire document: https://mybatis.org/generator/configreference/commentGenerator.html

            commentGenerator:
                - property(suppressDate): remove timestamp in comments
                - property(suppressAllComments): remove all comments
        -->
        <commentGenerator>
            <property name="suppressDate" value="true"/>
            <property name="suppressAllComments" value="true" />
        </commentGenerator>

        <!--
            <jdbcConnection/> entire document: https://mybatis.org/generator/configreference/jdbcConnection.html

            jdbcConnection.driverClass: The fully qualified class name for the JDBC driver used to access the database.
                Used mysql-connector-java:5.1.49, should specify JDBC is com.mysql.jdbc.Driver
            jdbcConnection.connectionURL: The JDBC connection URL used to access the database.
        -->
        <jdbcConnection driverClass="com.mysql.jdbc.Driver"
            connectionURL="jdbc:mysql://localhost:4000/test?user=root" />

        <!--
            <javaModelGenerator/> entire document: https://mybatis.org/generator/configreference/javaModelGenerator.html
            Model code file will be generated at ${targetProject}/${targetPackage}

            javaModelGenerator:
                - property(constructorBased): If it's true, generator will create constructor function in model
        -->
        <javaModelGenerator targetPackage="com.pingcap.model" targetProject="src/main/java">
            <property name="constructorBased" value="true"/>
        </javaModelGenerator>

        <!--
            <sqlMapGenerator/> entire document: https://mybatis.org/generator/configreference/sqlMapGenerator.html
            XML SQL mapper file will be generated at ${targetProject}/${targetPackage}
        -->
        <sqlMapGenerator targetPackage="." targetProject="src/main/resources/mapper"/>

        <!--
            <javaClientGenerator/> entire document: https://mybatis.org/generator/configreference/javaClientGenerator.html
            Java code mapper interface file will be generated at ${targetProject}/${targetPackage}

            javaClientGenerator.type (context.targetRuntime is MyBatis3):
                This attribute indicated Mybatis how to implement interface.
                It has ANNOTATEDMAPPER / MIXEDMAPPER / XMLMAPPER 3 selection to choice.
        -->
        <javaClientGenerator type="XMLMAPPER" targetPackage="com.pingcap.model" targetProject="src/main/java"/>

        <!--
            <table/> entire document: https://mybatis.org/generator/configreference/table.html

            table.tableName: The name of the database table.
            table.domainObjectName: The base name from which generated object names will be generated. If not specified, MBG will generate a name automatically based on the tableName.
            table.enableCountByExample: Signifies whether a count by example statement should be generated.
            table.enableUpdateByExample: Signifies whether an update by example statement should be generated.
            table.enableDeleteByExample: Signifies whether a delete by example statement should be generated.
            table.enableSelectByExample: Signifies whether a select by example statement should be generated.
            table.selectByExampleQueryId: This value will be added to the select list of the select by example statement in this form: "'<value>' as QUERYID".
        -->
        <table tableName="player" domainObjectName="Player"
               enableCountByExample="false" enableUpdateByExample="false"
               enableDeleteByExample="false" enableSelectByExample="false"
               selectByExampleQueryId="false"/>
    </context>
</generatorConfiguration>
```

`mybatis-generator-maven-plugin`の構成として、 `pom.xml`には`mybatis-generator.xml`が含まれる。

```xml
<plugin>
    <groupId>org.mybatis.generator</groupId>
    <artifactId>mybatis-generator-maven-plugin</artifactId>
    <version>1.4.1</version>
    <configuration>
        <configurationFile>src/main/resources/mybatis-generator.xml</configurationFile>
        <verbose>true</verbose>
        <overwrite>true</overwrite>
    </configuration>

    <dependencies>
        <!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java -->
        <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>5.1.49</version>
        </dependency>
    </dependencies>
</plugin>
```

Maven プラグインに組み込むと、古い生成ファイルを削除し、 `mvn mybatis-generate`を使用して新しいファイルを作成できます。または、 `make gen`使用して古いファイルを削除し、同時に新しいファイルを生成することもできます。

> **注記：**
>
> プロパティ`configuration.overwrite` `mybatis-generator.xml` 、生成されたJavaコード ファイルが上書きされることを保証するだけです。ただし、XML マッピング ファイルは追加されたまま書き込まれます。したがって、Mybaits Generator が新しいファイルを生成する前に、古いファイルを削除することをお勧めします。

`Player.java`は、Mybatis Generator を使用して生成されたデータ エンティティ クラス ファイルであり、アプリケーション内のデータベース テーブルのマッピングです。 `Player`クラスの各プロパティは、 `player`テーブルのフィールドに対応します。

```java
package com.pingcap.model;

public class Player {
    private String id;

    private Integer coins;

    private Integer goods;

    public Player(String id, Integer coins, Integer goods) {
        this.id = id;
        this.coins = coins;
        this.goods = goods;
    }

    public Player() {
        super();
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Integer getCoins() {
        return coins;
    }

    public void setCoins(Integer coins) {
        this.coins = coins;
    }

    public Integer getGoods() {
        return goods;
    }

    public void setGoods(Integer goods) {
        this.goods = goods;
    }
}
```

`PlayerMapper.java`は、Mybatis Generator を使用して生成されたマッピング インターフェイス ファイルです。このファイルはインターフェースのみを定義しており、インターフェースの実装クラスはXMLやアノテーションを利用して自動生成されます。

```java
package com.pingcap.model;

import com.pingcap.model.Player;

public interface PlayerMapper {
    int deleteByPrimaryKey(String id);

    int insert(Player row);

    int insertSelective(Player row);

    Player selectByPrimaryKey(String id);

    int updateByPrimaryKeySelective(Player row);

    int updateByPrimaryKey(Player row);
}
```

`PlayerMapper.xml`は、Mybatis Generator を使用して生成されたマッピング XML ファイルです。 Mybatis はこれを使用して`PlayerMapper`インターフェースの実装クラスを自動生成します。

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
  <sql id="Base_Column_List">
    id, coins, goods
  </sql>
  <select id="selectByPrimaryKey" parameterType="java.lang.String" resultMap="BaseResultMap">
    select
    <include refid="Base_Column_List" />
    from player
    where id = #{id,jdbcType=VARCHAR}
  </select>
  <delete id="deleteByPrimaryKey" parameterType="java.lang.String">
    delete from player
    where id = #{id,jdbcType=VARCHAR}
  </delete>
  <insert id="insert" parameterType="com.pingcap.model.Player">
    insert into player (id, coins, goods
      )
    values (#{id,jdbcType=VARCHAR}, #{coins,jdbcType=INTEGER}, #{goods,jdbcType=INTEGER}
      )
  </insert>
  <insert id="insertSelective" parameterType="com.pingcap.model.Player">
    insert into player
    <trim prefix="(" suffix=")" suffixOverrides=",">
      <if test="id != null">
        id,
      </if>
      <if test="coins != null">
        coins,
      </if>
      <if test="goods != null">
        goods,
      </if>
    </trim>
    <trim prefix="values (" suffix=")" suffixOverrides=",">
      <if test="id != null">
        #{id,jdbcType=VARCHAR},
      </if>
      <if test="coins != null">
        #{coins,jdbcType=INTEGER},
      </if>
      <if test="goods != null">
        #{goods,jdbcType=INTEGER},
      </if>
    </trim>
  </insert>
  <update id="updateByPrimaryKeySelective" parameterType="com.pingcap.model.Player">
    update player
    <set>
      <if test="coins != null">
        coins = #{coins,jdbcType=INTEGER},
      </if>
      <if test="goods != null">
        goods = #{goods,jdbcType=INTEGER},
      </if>
    </set>
    where id = #{id,jdbcType=VARCHAR}
  </update>
  <update id="updateByPrimaryKey" parameterType="com.pingcap.model.Player">
    update player
    set coins = #{coins,jdbcType=INTEGER},
      goods = #{goods,jdbcType=INTEGER}
    where id = #{id,jdbcType=VARCHAR}
  </update>
</mapper>
```

Mybatis Generator はテーブル定義からソースコードを生成する必要があるため、最初にテーブルを作成する必要があります。テーブルを作成するには、 `dbinit.sql`を使用できます。

```sql
USE test;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
    `id` VARCHAR(36),
    `coins` INTEGER,
    `goods` INTEGER,
    PRIMARY KEY (`id`)
);
```

インターフェイス`PlayerMapperEx`さらに分割して`PlayerMapper`を拡張し、一致する`PlayerMapperEx.xml`ファイルを書き込みます。 `PlayerMapper.java`と`PlayerMapper.xml`を直接変更することは避けてください。これは、Mybatis Generator による上書きを避けるためです。

`PlayerMapperEx.java`で追加したインターフェースを定義します。

```java
package com.pingcap.model;

import java.util.List;

public interface PlayerMapperEx extends PlayerMapper {
    Player selectByPrimaryKeyWithLock(String id);

    List<Player> selectByLimit(Integer limit);

    Integer count();
}
```

`PlayerMapperEx.xml`でマッピング ルールを定義します。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapperEx">
  <resultMap id="BaseResultMap" type="com.pingcap.model.Player">
    <constructor>
      <idArg column="id" javaType="java.lang.String" jdbcType="VARCHAR" />
      <arg column="coins" javaType="java.lang.Integer" jdbcType="INTEGER" />
      <arg column="goods" javaType="java.lang.Integer" jdbcType="INTEGER" />
    </constructor>
  </resultMap>
  <sql id="Base_Column_List">
    id, coins, goods
  </sql>

  <select id="selectByPrimaryKeyWithLock" parameterType="java.lang.String" resultMap="BaseResultMap">
    select
    <include refid="Base_Column_List" />
    from player
    where `id` = #{id,jdbcType=VARCHAR}
    for update
  </select>

  <select id="selectByLimit" parameterType="java.lang.Integer" resultMap="BaseResultMap">
    select
    <include refid="Base_Column_List" />
    from player
    limit #{id,jdbcType=INTEGER}
  </select>

  <select id="count" resultType="java.lang.Integer">
    select count(*) from player
  </select>

</mapper>
```

`PlayerDAO.java`はデータを管理するために使用されるクラスで、 `DAO` [データアクセスオブジェクト](https://en.wikipedia.org/wiki/Data_access_object)を意味します。このクラスは、データを書き込むための一連のデータ操作メソッドを定義します。 Mybatis はその中で、オブジェクト マッピングや基本オブジェクトの CRUD などの多数の操作をカプセル化し、コードを大幅に簡素化します。

```java
package com.pingcap.dao;

import com.pingcap.model.Player;
import com.pingcap.model.PlayerMapperEx;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;

import java.util.List;
import java.util.function.Function;

public class PlayerDAO {
    public static class NotEnoughException extends RuntimeException {
        public NotEnoughException(String message) {
            super(message);
        }
    }

    // Run SQL code in a way that automatically handles the
    // transaction retry logic, so we don't have to duplicate it in
    // various places.
    public Object runTransaction(SqlSessionFactory sessionFactory, Function<PlayerMapperEx, Object> fn) {
        Object resultObject = null;
        SqlSession session = null;

        try {
            // open a session with autoCommit is false
            session = sessionFactory.openSession(false);

            // get player mapper
            PlayerMapperEx playerMapperEx = session.getMapper(PlayerMapperEx.class);

            resultObject = fn.apply(playerMapperEx);
            session.commit();
            System.out.println("APP: COMMIT;");
        } catch (Exception e) {
            if (e instanceof NotEnoughException) {
                System.out.printf("APP: ROLLBACK BY LOGIC; \n%s\n", e.getMessage());
            } else {
                System.out.printf("APP: ROLLBACK BY ERROR; \n%s\n", e.getMessage());
            }

            if (session != null) {
                session.rollback();
            }
        } finally {
            if (session != null) {
                session.close();
            }
        }

        return resultObject;
    }

    public Function<PlayerMapperEx, Object> createPlayers(List<Player> players) {
        return playerMapperEx -> {
            Integer addedPlayerAmount = 0;
            for (Player player: players) {
                playerMapperEx.insert(player);
                addedPlayerAmount ++;
            }
            System.out.printf("APP: createPlayers() --> %d\n", addedPlayerAmount);
            return addedPlayerAmount;
        };
    }

    public Function<PlayerMapperEx, Object> buyGoods(String sellId, String buyId, Integer amount, Integer price) {
        return playerMapperEx -> {
            Player sellPlayer = playerMapperEx.selectByPrimaryKeyWithLock(sellId);
            Player buyPlayer = playerMapperEx.selectByPrimaryKeyWithLock(buyId);

            if (buyPlayer == null || sellPlayer == null) {
                throw new NotEnoughException("sell or buy player not exist");
            }

            if (buyPlayer.getCoins() < price || sellPlayer.getGoods() < amount) {
                throw new NotEnoughException("coins or goods not enough, rollback");
            }

            int affectRows = 0;
            buyPlayer.setGoods(buyPlayer.getGoods() + amount);
            buyPlayer.setCoins(buyPlayer.getCoins() - price);
            affectRows += playerMapperEx.updateByPrimaryKey(buyPlayer);

            sellPlayer.setGoods(sellPlayer.getGoods() - amount);
            sellPlayer.setCoins(sellPlayer.getCoins() + price);
            affectRows += playerMapperEx.updateByPrimaryKey(sellPlayer);

            System.out.printf("APP: buyGoods --> sell: %s, buy: %s, amount: %d, price: %d\n", sellId, buyId, amount, price);
            return affectRows;
        };
    }

    public Function<PlayerMapperEx, Object> getPlayerByID(String id) {
        return playerMapperEx -> playerMapperEx.selectByPrimaryKey(id);
    }

    public Function<PlayerMapperEx, Object> printPlayers(Integer limit) {
        return playerMapperEx -> {
            List<Player> players = playerMapperEx.selectByLimit(limit);

            for (Player player: players) {
                System.out.println("\n[printPlayers]:\n" + player);
            }
            return 0;
        };
    }

    public Function<PlayerMapperEx, Object> countPlayers() {
        return PlayerMapperEx::count;
    }
}
```

`MybatisExample`は`plain-java-mybatis`サンプル アプリケーションのメイン クラスです。エントリ関数を定義します。

```java
package com.pingcap;

import com.pingcap.dao.PlayerDAO;
import com.pingcap.model.Player;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.Collections;

public class MybatisExample {
    public static void main( String[] args ) throws IOException {
        // 1. Create a SqlSessionFactory based on our mybatis-config.xml configuration
        // file, which defines how to connect to the database.
        InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
        SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

        // 2. And then, create DAO to manager your data
        PlayerDAO playerDAO = new PlayerDAO();

        // 3. Run some simple examples.

        // Create a player who has 1 coin and 1 goods.
        playerDAO.runTransaction(sessionFactory, playerDAO.createPlayers(
                Collections.singletonList(new Player("test", 1, 1))));

        // Get a player.
        Player testPlayer = (Player)playerDAO.runTransaction(sessionFactory, playerDAO.getPlayerByID("test"));
        System.out.printf("PlayerDAO.getPlayer:\n    => id: %s\n    => coins: %s\n    => goods: %s\n",
                testPlayer.getId(), testPlayer.getCoins(), testPlayer.getGoods());

        // Count players amount.
        Integer count = (Integer)playerDAO.runTransaction(sessionFactory, playerDAO.countPlayers());
        System.out.printf("PlayerDAO.countPlayers:\n    => %d total players\n", count);

        // Print 3 players.
        playerDAO.runTransaction(sessionFactory, playerDAO.printPlayers(3));

        // 4. Getting further.

        // Player 1: id is "1", has only 100 coins.
        // Player 2: id is "2", has 114514 coins, and 20 goods.
        Player player1 = new Player("1", 100, 0);
        Player player2 = new Player("2", 114514, 20);

        // Create two players "by hand", using the INSERT statement on the backend.
        int addedCount = (Integer)playerDAO.runTransaction(sessionFactory,
                playerDAO.createPlayers(Arrays.asList(player1, player2)));
        System.out.printf("PlayerDAO.createPlayers:\n    => %d total inserted players\n", addedCount);

        // Player 1 wants to buy 10 goods from player 2.
        // It will cost 500 coins, but player 1 cannot afford it.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will fail");
        Integer updatedCount = (Integer)playerDAO.runTransaction(sessionFactory,
                playerDAO.buyGoods(player2.getId(), player1.getId(), 10, 500));
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);

        // So player 1 has to reduce the incoming quantity to two.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will success");
        updatedCount = (Integer)playerDAO.runTransaction(sessionFactory,
                playerDAO.buyGoods(player2.getId(), player1.getId(), 2, 100));
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);
    }
}
```

</div>

<div label="Using Hibernate (Recommended)" value="hibernate">

Hibernate と比較すると、JDBC 実装はベスト プラクティスではない可能性があります。エラー処理ロジックを手動で記述する必要があり、コードを簡単に再利用できないため、コードが若干冗長になります。

Hibernate は人気のあるオープンソースJava ORM であり、TiDB 機能によく適合する`v6.0.0.Beta2`から始まる TiDB 方言をサポートしています。次の手順では例として`v6.0.0.Beta2`を取り上げます。

`plain-java-hibernate`ディレクトリに移動します。

```shell
cd plain-java-hibernate
```

このディレクトリの構造は次のとおりです。

    .
    ├── Makefile
    ├── plain-java-hibernate.iml
    ├── pom.xml
    └── src
        └── main
            ├── java
            │   └── com
            │       └── pingcap
            │           └── HibernateExample.java
            └── resources
                └── hibernate.cfg.xml

`hibernate.cfg.xml`は Hibernate 構成ファイルです。

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- Database connection settings -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://localhost:4000/test</property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password"></property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Required so a table can be created from the 'PlayerDAO' class -->
        <property name="hibernate.hbm2ddl.auto">create-drop</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

`HibernateExample.java`は`plain-java-hibernate`の本体です。 JDBC と比較して、Hibernate を使用する場合は、異なるデータベース間でのデータベース作成の差異が回避されるため、構成ファイルのパスを記述するだけで済みます。

`PlayerDAO`はデータを管理するために使用されるクラスで、 `DAO` [データアクセスオブジェクト](https://en.wikipedia.org/wiki/Data_access_object)を意味します。このクラスは、データを書き込むための一連のデータ操作メソッドを定義します。 JDBC と比較して、Hibernate はオブジェクト マッピングや基本オブジェクトの CRUD などの多数の操作をカプセル化するため、コードが大幅に簡素化されます。

`PlayerBean`は、テーブルのマッピングであるデータ エンティティ クラスです。 `PlayerBean`の各プロパティは、 `player`テーブルのフィールドに対応します。 JDBC と比較すると、Hibernate `PlayerBean`では、詳細情報のマッピング関係を示す注釈が追加されています。

```java
package com.pingcap;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import org.hibernate.JDBCException;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.hibernate.cfg.Configuration;
import org.hibernate.query.NativeQuery;
import org.hibernate.query.Query;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;

@Entity
@Table(name = "player_hibernate")
class PlayerBean {
    @Id
    private String id;
    @Column(name = "coins")
    private Integer coins;
    @Column(name = "goods")
    private Integer goods;

    public PlayerBean() {
    }

    public PlayerBean(String id, Integer coins, Integer goods) {
        this.id = id;
        this.coins = coins;
        this.goods = goods;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Integer getCoins() {
        return coins;
    }

    public void setCoins(Integer coins) {
        this.coins = coins;
    }

    public Integer getGoods() {
        return goods;
    }

    public void setGoods(Integer goods) {
        this.goods = goods;
    }

    @Override
    public String toString() {
        return String.format("    %-8s => %10s\n    %-8s => %10s\n    %-8s => %10s\n",
                "id", this.id, "coins", this.coins, "goods", this.goods);
    }
}

/**
 * Main class for the basic Hibernate example.
 **/
public class HibernateExample
{
    public static class PlayerDAO {
        public static class NotEnoughException extends RuntimeException {
            public NotEnoughException(String message) {
                super(message);
            }
        }

        // Run SQL code in a way that automatically handles the
        // transaction retry logic so we don't have to duplicate it in
        // various places.
        public Object runTransaction(Session session, Function<Session, Object> fn) {
            Object resultObject = null;

            Transaction txn = session.beginTransaction();
            try {
                resultObject = fn.apply(session);
                txn.commit();
                System.out.println("APP: COMMIT;");
            } catch (JDBCException e) {
                System.out.println("APP: ROLLBACK BY JDBC ERROR;");
                txn.rollback();
            } catch (NotEnoughException e) {
                System.out.printf("APP: ROLLBACK BY LOGIC; %s", e.getMessage());
                txn.rollback();
            }
            return resultObject;
        }

        public Function<Session, Object> createPlayers(List<PlayerBean> players) throws JDBCException {
            return session -> {
                Integer addedPlayerAmount = 0;
                for (PlayerBean player: players) {
                    session.persist(player);
                    addedPlayerAmount ++;
                }
                System.out.printf("APP: createPlayers() --> %d\n", addedPlayerAmount);
                return addedPlayerAmount;
            };
        }

        public Function<Session, Object> buyGoods(String sellId, String buyId, Integer amount, Integer price) throws JDBCException {
            return session -> {
                PlayerBean sellPlayer = session.get(PlayerBean.class, sellId);
                PlayerBean buyPlayer = session.get(PlayerBean.class, buyId);

                if (buyPlayer == null || sellPlayer == null) {
                    throw new NotEnoughException("sell or buy player not exist");
                }

                if (buyPlayer.getCoins() < price || sellPlayer.getGoods() < amount) {
                    throw new NotEnoughException("coins or goods not enough, rollback");
                }

                buyPlayer.setGoods(buyPlayer.getGoods() + amount);
                buyPlayer.setCoins(buyPlayer.getCoins() - price);
                session.persist(buyPlayer);

                sellPlayer.setGoods(sellPlayer.getGoods() - amount);
                sellPlayer.setCoins(sellPlayer.getCoins() + price);
                session.persist(sellPlayer);

                System.out.printf("APP: buyGoods --> sell: %s, buy: %s, amount: %d, price: %d\n", sellId, buyId, amount, price);
                return 0;
            };
        }

        public Function<Session, Object> getPlayerByID(String id) throws JDBCException {
            return session -> session.get(PlayerBean.class, id);
        }

        public Function<Session, Object> printPlayers(Integer limit) throws JDBCException {
            return session -> {
                NativeQuery<PlayerBean> limitQuery = session.createNativeQuery("SELECT * FROM player_hibernate LIMIT :limit", PlayerBean.class);
                limitQuery.setParameter("limit", limit);
                List<PlayerBean> players = limitQuery.getResultList();

                for (PlayerBean player: players) {
                    System.out.println("\n[printPlayers]:\n" + player);
                }
                return 0;
            };
        }

        public Function<Session, Object> countPlayers() throws JDBCException {
            return session -> {
                Query<Long> countQuery = session.createQuery("SELECT count(player_hibernate) FROM PlayerBean player_hibernate", Long.class);
                return countQuery.getSingleResult();
            };
        }
    }

    public static void main(String[] args) {
        // 1. Create a SessionFactory based on our hibernate.cfg.xml configuration
        // file, which defines how to connect to the database.
        SessionFactory sessionFactory
                = new Configuration()
                .configure("hibernate.cfg.xml")
                .addAnnotatedClass(PlayerBean.class)
                .buildSessionFactory();

        try (Session session = sessionFactory.openSession()) {
            // 2. And then, create DAO to manager your data.
            PlayerDAO playerDAO = new PlayerDAO();

            // 3. Run some simple example.

            // Create a player who has 1 coin and 1 goods.
            playerDAO.runTransaction(session, playerDAO.createPlayers(Collections.singletonList(
                    new PlayerBean("test", 1, 1))));

            // Get a player.
            PlayerBean testPlayer = (PlayerBean)playerDAO.runTransaction(session, playerDAO.getPlayerByID("test"));
            System.out.printf("PlayerDAO.getPlayer:\n    => id: %s\n    => coins: %s\n    => goods: %s\n",
                    testPlayer.getId(), testPlayer.getCoins(), testPlayer.getGoods());

            // Count players amount.
            Long count = (Long)playerDAO.runTransaction(session, playerDAO.countPlayers());
            System.out.printf("PlayerDAO.countPlayers:\n    => %d total players\n", count);

            // Print 3 players.
            playerDAO.runTransaction(session, playerDAO.printPlayers(3));

            // 4. Getting further.

            // Player 1: id is "1", has only 100 coins.
            // Player 2: id is "2", has 114514 coins, and 20 goods.
            PlayerBean player1 = new PlayerBean("1", 100, 0);
            PlayerBean player2 = new PlayerBean("2", 114514, 20);

            // Create two players "by hand", using the INSERT statement on the backend.
            int addedCount = (Integer)playerDAO.runTransaction(session,
                    playerDAO.createPlayers(Arrays.asList(player1, player2)));
            System.out.printf("PlayerDAO.createPlayers:\n    => %d total inserted players\n", addedCount);

            // Player 1 wants to buy 10 goods from player 2.
            // It will cost 500 coins, but player 1 can't afford it.
            System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will fail");
            Integer updatedCount = (Integer)playerDAO.runTransaction(session,
                    playerDAO.buyGoods(player2.getId(), player1.getId(), 10, 500));
            System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);

            // So player 1 have to reduce his incoming quantity to two.
            System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will success");
            updatedCount = (Integer)playerDAO.runTransaction(session,
                    playerDAO.buyGoods(player2.getId(), player1.getId(), 2, 100));
            System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);
        } finally {
            sessionFactory.close();
        }
    }
}
```

</div>

<div label="Using JDBC" value="jdbc">

`plain-java-jdbc`ディレクトリに移動します。

```shell
cd plain-java-jdbc
```

このディレクトリの構造は次のとおりです。

    .
    ├── Makefile
    ├── plain-java-jdbc.iml
    ├── pom.xml
    └── src
        └── main
            ├── java
            │   └── com
            │       └── pingcap
            │            └── JDBCExample.java
            └── resources
                └── dbinit.sql

テーブル作成の初期化ステートメントは`dbinit.sql`にあります。

```sql
USE test;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
    `id` VARCHAR(36),
    `coins` INTEGER,
    `goods` INTEGER,
   PRIMARY KEY (`id`)
);
```

`JDBCExample.java`は`plain-java-jdbc`の本体です。 TiDB は MySQL プロトコルと高い互換性があるため、TiDB に接続するには MySQL ソース インスタンス`MysqlDataSource`を初期化する必要があります。次に、オブジェクト管理用に`PlayerDAO`初期化し、それを使用してデータの読み取り、編集、追加、削除を行うことができます。

`PlayerDAO`はデータを管理するために使用されるクラスで、 `DAO` [データアクセスオブジェクト](https://en.wikipedia.org/wiki/Data_access_object)を意味します。このクラスは、データを書き込む機能を提供する一連のデータ操作メソッドを定義します。

`PlayerBean`は、テーブルのマッピングであるデータ エンティティ クラスです。 `PlayerBean`の各プロパティは、 `player`テーブルのフィールドに対応します。

```java
package com.pingcap;

import com.mysql.cj.jdbc.MysqlDataSource;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.*;

/**
 * Main class for the basic JDBC example.
 **/
public class JDBCExample
{
    public static class PlayerBean {
        private String id;
        private Integer coins;
        private Integer goods;

        public PlayerBean() {
        }

        public PlayerBean(String id, Integer coins, Integer goods) {
            this.id = id;
            this.coins = coins;
            this.goods = goods;
        }

        public String getId() {
            return id;
        }

        public void setId(String id) {
            this.id = id;
        }

        public Integer getCoins() {
            return coins;
        }

        public void setCoins(Integer coins) {
            this.coins = coins;
        }

        public Integer getGoods() {
            return goods;
        }

        public void setGoods(Integer goods) {
            this.goods = goods;
        }

        @Override
        public String toString() {
            return String.format("    %-8s => %10s\n    %-8s => %10s\n    %-8s => %10s\n",
                    "id", this.id, "coins", this.coins, "goods", this.goods);
        }
    }

    /**
     * Data access object used by 'ExampleDataSource'.
     * Example for CURD and bulk insert.
     */
    public static class PlayerDAO {
        private final MysqlDataSource ds;
        private final Random rand = new Random();

        PlayerDAO(MysqlDataSource ds) {
            this.ds = ds;
        }

        /**
         * Create players by passing in a List of PlayerBean.
         *
         * @param players Will create players list
         * @return The number of create accounts
         */
        public int createPlayers(List<PlayerBean> players){
            int rows = 0;

            Connection connection = null;
            PreparedStatement preparedStatement = null;
            try {
                connection = ds.getConnection();
                preparedStatement = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)");
            } catch (SQLException e) {
                System.out.printf("[createPlayers] ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
                e.printStackTrace();

                return -1;
            }

            try {
                for (PlayerBean player : players) {
                    preparedStatement.setString(1, player.getId());
                    preparedStatement.setInt(2, player.getCoins());
                    preparedStatement.setInt(3, player.getGoods());

                    preparedStatement.execute();
                    rows += preparedStatement.getUpdateCount();
                }
            } catch (SQLException e) {
                System.out.printf("[createPlayers] ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
                e.printStackTrace();
            } finally {
                try {
                    connection.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }

            System.out.printf("\n[createPlayers]:\n    '%s'\n", preparedStatement);
            return rows;
        }

        /**
         * Buy goods and transfer funds between one player and another in one transaction.
         * @param sellId Sell player id.
         * @param buyId Buy player id.
         * @param amount Goods amount, if sell player has not enough goods, the trade will break.
         * @param price Price should pay, if buy player has not enough coins, the trade will break.
         *
         * @return The number of effected players.
         */
        public int buyGoods(String sellId, String buyId, Integer amount, Integer price) {
            int effectPlayers = 0;

            Connection connection = null;
            try {
                connection = ds.getConnection();
            } catch (SQLException e) {
                System.out.printf("[buyGoods] ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
                e.printStackTrace();
                return effectPlayers;
            }

            try {
                connection.setAutoCommit(false);

                PreparedStatement playerQuery = connection.prepareStatement("SELECT * FROM player WHERE id=? OR id=? FOR UPDATE");
                playerQuery.setString(1, sellId);
                playerQuery.setString(2, buyId);
                playerQuery.execute();

                PlayerBean sellPlayer = null;
                PlayerBean buyPlayer = null;

                ResultSet playerQueryResultSet = playerQuery.getResultSet();
                while (playerQueryResultSet.next()) {
                    PlayerBean player =  new PlayerBean(
                            playerQueryResultSet.getString("id"),
                            playerQueryResultSet.getInt("coins"),
                            playerQueryResultSet.getInt("goods")
                    );

                    System.out.println("\n[buyGoods]:\n    'check goods and coins enough'");
                    System.out.println(player);

                    if (sellId.equals(player.getId())) {
                        sellPlayer = player;
                    } else {
                        buyPlayer = player;
                    }
                }

                if (sellPlayer == null || buyPlayer == null) {
                    throw new SQLException("player not exist.");
                }

                if (sellPlayer.getGoods().compareTo(amount) < 0) {
                    throw new SQLException(String.format("sell player %s goods not enough.", sellId));
                }

                if (buyPlayer.getCoins().compareTo(price) < 0) {
                    throw new SQLException(String.format("buy player %s coins not enough.", buyId));
                }

                PreparedStatement transfer = connection.prepareStatement("UPDATE player set goods = goods + ?, coins = coins + ? WHERE id=?");
                transfer.setInt(1, -amount);
                transfer.setInt(2, price);
                transfer.setString(3, sellId);
                transfer.execute();
                effectPlayers += transfer.getUpdateCount();

                transfer.setInt(1, amount);
                transfer.setInt(2, -price);
                transfer.setString(3, buyId);
                transfer.execute();
                effectPlayers += transfer.getUpdateCount();

                connection.commit();

                System.out.println("\n[buyGoods]:\n    'trade success'");
            } catch (SQLException e) {
                System.out.printf("[buyGoods] ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());

                try {
                    System.out.println("[buyGoods] Rollback");

                    connection.rollback();
                } catch (SQLException ex) {
                    // do nothing
                }
            } finally {
                try {
                    connection.close();
                } catch (SQLException e) {
                    // do nothing
                }
            }

            return effectPlayers;
        }

        /**
         * Get the player info by id.
         *
         * @param id Player id.
         * @return The player of this id.
         */
        public PlayerBean getPlayer(String id) {
            PlayerBean player = null;

            try (Connection connection = ds.getConnection()) {
                PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM player WHERE id = ?");
                preparedStatement.setString(1, id);
                preparedStatement.execute();

                ResultSet res = preparedStatement.executeQuery();
                if(!res.next()) {
                    System.out.printf("No players in the table with id %s", id);
                } else {
                    player = new PlayerBean(res.getString("id"), res.getInt("coins"), res.getInt("goods"));
                }
            } catch (SQLException e) {
                System.out.printf("PlayerDAO.getPlayer ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
            }

            return player;
        }

        /**
         * Insert randomized account data (id, coins, goods) using the JDBC fast path for
         * bulk inserts.  The fastest way to get data into TiDB is using the
         * TiDB Lightning(https://docs.pingcap.com/tidb/stable/tidb-lightning-overview).
         * However, if you must bulk insert from the application using INSERT SQL, the best
         * option is the method shown here. It will require the following:
         *
         *    Add `rewriteBatchedStatements=true` to your JDBC connection settings.
         *    Setting rewriteBatchedStatements to true now causes CallableStatements
         *    with batched arguments to be re-written in the form "CALL (...); CALL (...); ..."
         *    to send the batch in as few client/server round trips as possible.
         *    https://dev.mysql.com/doc/relnotes/connector-j/5.1/en/news-5-1-3.html
         *
         *    You can see the `rewriteBatchedStatements` param effect logic at
         *    implement function: `com.mysql.cj.jdbc.StatementImpl.executeBatchUsingMultiQueries`
         *
         * @param total Add players amount.
         * @param batchSize Bulk insert size for per batch.
         *
         * @return The number of new accounts inserted.
         */
        public int bulkInsertRandomPlayers(Integer total, Integer batchSize) {
            int totalNewPlayers = 0;

            try (Connection connection = ds.getConnection()) {
                // We're managing the commit lifecycle ourselves, so we can
                // control the size of our batch inserts.
                connection.setAutoCommit(false);

                // In this example we are adding 500 rows to the database,
                // but it could be any number.  What's important is that
                // the batch size is 128.
                try (PreparedStatement pstmt = connection.prepareStatement("INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)")) {
                    for (int i=0; i<=(total/batchSize);i++) {
                        for (int j=0; j<batchSize; j++) {
                            String id = UUID.randomUUID().toString();
                            pstmt.setString(1, id);
                            pstmt.setInt(2, rand.nextInt(10000));
                            pstmt.setInt(3, rand.nextInt(10000));
                            pstmt.addBatch();
                        }

                        int[] count = pstmt.executeBatch();
                        totalNewPlayers += count.length;
                        System.out.printf("\nPlayerDAO.bulkInsertRandomPlayers:\n    '%s'\n", pstmt);
                        System.out.printf("    => %s row(s) updated in this batch\n", count.length);
                    }
                    connection.commit();
                } catch (SQLException e) {
                    System.out.printf("PlayerDAO.bulkInsertRandomPlayers ERROR: { state => %s, cause => %s, message => %s }\n",
                            e.getSQLState(), e.getCause(), e.getMessage());
                }
            } catch (SQLException e) {
                System.out.printf("PlayerDAO.bulkInsertRandomPlayers ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
            }
            return totalNewPlayers;
        }


        /**
         * Print a subset of players from the data store by limit.
         *
         * @param limit Print max size.
         */
        public void printPlayers(Integer limit) {
            try (Connection connection = ds.getConnection()) {
                PreparedStatement preparedStatement = connection.prepareStatement("SELECT * FROM player LIMIT ?");
                preparedStatement.setInt(1, limit);
                preparedStatement.execute();

                ResultSet res = preparedStatement.executeQuery();
                while (!res.next()) {
                    PlayerBean player = new PlayerBean(res.getString("id"),
                            res.getInt("coins"), res.getInt("goods"));
                    System.out.println("\n[printPlayers]:\n" + player);
                }
            } catch (SQLException e) {
                System.out.printf("PlayerDAO.printPlayers ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
            }
        }


        /**
         * Count players from the data store.
         *
         * @return All players count
         */
        public int countPlayers() {
            int count = 0;

            try (Connection connection = ds.getConnection()) {
                PreparedStatement preparedStatement = connection.prepareStatement("SELECT count(*) FROM player");
                preparedStatement.execute();

                ResultSet res = preparedStatement.executeQuery();
                if(res.next()) {
                    count = res.getInt(1);
                }
            } catch (SQLException e) {
                System.out.printf("PlayerDAO.countPlayers ERROR: { state => %s, cause => %s, message => %s }\n",
                        e.getSQLState(), e.getCause(), e.getMessage());
            }

            return count;
        }
    }

    public static void main(String[] args) {
        // 1. Configure the example database connection.

        // 1.1 Create a mysql data source instance.
        MysqlDataSource mysqlDataSource = new MysqlDataSource();

        // 1.2 Set server name, port, database name, username and password.
        mysqlDataSource.setServerName("localhost");
        mysqlDataSource.setPortNumber(4000);
        mysqlDataSource.setDatabaseName("test");
        mysqlDataSource.setUser("root");
        mysqlDataSource.setPassword("");

        // Or you can use jdbc string instead.
        // mysqlDataSource.setURL("jdbc:mysql://{host}:{port}/test?user={user}&password={password}");

        // 2. And then, create DAO to manager your data.
        PlayerDAO dao = new PlayerDAO(mysqlDataSource);

        // 3. Run some simple example.

        // Create a player, has a coin and a goods.
        dao.createPlayers(Collections.singletonList(new PlayerBean("test", 1, 1)));

        // Get a player.
        PlayerBean testPlayer = dao.getPlayer("test");
        System.out.printf("PlayerDAO.getPlayer:\n    => id: %s\n    => coins: %s\n    => goods: %s\n",
                testPlayer.getId(), testPlayer.getCoins(), testPlayer.getGoods());

        // Create players with bulk inserts, insert 1919 players totally, and per batch for 114 players.
        int addedCount = dao.bulkInsertRandomPlayers(1919, 114);
        System.out.printf("PlayerDAO.bulkInsertRandomPlayers:\n    => %d total inserted players\n", addedCount);

        // Count players amount.
        int count = dao.countPlayers();
        System.out.printf("PlayerDAO.countPlayers:\n    => %d total players\n", count);

        // Print 3 players.
        dao.printPlayers(3);

        // 4. Getting further.

        // Player 1: id is "1", has only 100 coins.
        // Player 2: id is "2", has 114514 coins, and 20 goods.
        PlayerBean player1 = new PlayerBean("1", 100, 0);
        PlayerBean player2 = new PlayerBean("2", 114514, 20);

        // Create two players "by hand", using the INSERT statement on the backend.
        addedCount = dao.createPlayers(Arrays.asList(player1, player2));
        System.out.printf("PlayerDAO.createPlayers:\n    => %d total inserted players\n", addedCount);

        // Player 1 wants to buy 10 goods from player 2.
        // It will cost 500 coins, but player 1 can't afford it.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will fail");
        int updatedCount = dao.buyGoods(player2.getId(), player1.getId(), 10, 500);
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);

        // So player 1 have to reduce his incoming quantity to two.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will success");
        updatedCount = dao.buyGoods(player2.getId(), player1.getId(), 2, 100);
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);
    }
}
```

</div>

</SimpleTab>

## ステップ 3. コードを実行する {#step-3-run-the-code}

次のコンテンツでは、コードを実行する方法をステップごとに紹介します。

### ステップ 3.1 テーブルの初期化 {#step-3-1-table-initialization}

<SimpleTab groupId="language">

<div label="Using Mybatis (Recommended)" value="mybatis">

Mybatis を使用する場合、データベース テーブルを手動で初期化する必要があります。ローカル クラスターを使用していて、MySQL クライアントがローカルにインストールされている場合は、 `plain-java-mybatis`ディレクトリで直接実行できます。

```shell
make prepare
```

または、次のコマンドを実行することもできます。

```shell
mysql --host 127.0.0.1 --port 4000 -u root < src/main/resources/dbinit.sql
```

非ローカル クラスターを使用している場合、または MySQL クライアントがインストールされていない場合は、クラスターに接続し、 `src/main/resources/dbinit.sql`ファイル内のステートメントを実行します。

</div>

<div label="Using Hibernate (Recommended)" value="hibernate">

テーブルを手動で初期化する必要はありません。

</div>

<div label="Using JDBC" value="jdbc">

<CustomContent platform="tidb">

JDBC を使用する場合、データベース テーブルを手動で初期化する必要があります。ローカル クラスターを使用していて、MySQL クライアントがローカルにインストールされている場合は、 `plain-java-jdbc`ディレクトリで直接実行できます。

```shell
make mysql
```

または、次のコマンドを実行することもできます。

```shell
mysql --host 127.0.0.1 --port 4000 -u root<src/main/resources/dbinit.sql
```

非ローカル クラスターを使用している場合、または MySQL クライアントがインストールされていない場合は、クラスターに接続し、 `src/main/resources/dbinit.sql`ファイル内のステートメントを実行します。

</CustomContent>

<CustomContent platform="tidb-cloud">

JDBC を使用する場合は、クラスターに接続し、 `src/main/resources/dbinit.sql`ファイル内のステートメントを実行してデータベース テーブルを手動で初期化する必要があります。

</CustomContent>

</div>

</SimpleTab>

### ステップ 3.2 TiDB Cloudのパラメータを変更する {#step-3-2-modify-parameters-for-tidb-cloud}

<SimpleTab groupId="language">

<div label="Using Mybatis (Recommended)" value="mybatis">

TiDB サーバーレス クラスターを使用している場合は、 `mybatis-config.xml`の`dataSource.url` 、 `dataSource.username` 、 `dataSource.password`を変更します。

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

    <typeAliases>
        <package name="com.pingcap.dao"/>
    </typeAliases>

    <environments default="development">
        <environment id="development">
            <!-- JDBC transaction manager -->
            <transactionManager type="JDBC"/>
            <!-- Database pool -->
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://127.0.0.1:4000/test"/>
                <property name="username" value="root"/>
                <property name="password" value=""/>
            </dataSource>
        </environment>
    </environments>

    <mappers>
        <mapper resource="mapper/PlayerMapper.xml"/>
        <mapper resource="mapper/PlayerMapperEx.xml"/>
    </mappers>

</configuration>
```

設定したパスワードが`123456`で、クラスターの詳細ページから取得した接続パラメーターが次であるとします。

-   エンドポイント: `xxx.tidbcloud.com`
-   ポート: `4000`
-   ユーザー: `2aEp24QWEDLqRFs.root`

この場合、 `dataSource`ノードのパラメータを次のように変更できます。

```xml
<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

        ...
            <!-- Database pool -->
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://xxx.tidbcloud.com:4000/test?sslMode=VERIFY_IDENTITY&amp;enabledTLSProtocols=TLSv1.2,TLSv1.3"/>
                <property name="username" value="2aEp24QWEDLqRFs.root"/>
                <property name="password" value="123456"/>
            </dataSource>
        ...

</configuration>
```

</div>

<div label="Using Hibernate (Recommended)" value="hibernate">

TiDB サーバーレス クラスターを使用している場合は、 `hibernate.cfg.xml`の`hibernate.connection.url` 、 `hibernate.connection.username` 、 `hibernate.connection.password`を変更します。

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- Database connection settings -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://localhost:4000/test</property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password"></property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Required so a table can be created from the 'PlayerDAO' class -->
        <property name="hibernate.hbm2ddl.auto">create-drop</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

設定したパスワードが`123456`で、クラスターの詳細ページから取得した接続パラメーターが次であるとします。

-   エンドポイント: `xxx.tidbcloud.com`
-   ポート: `4000`
-   ユーザー: `2aEp24QWEDLqRFs.root`

この場合、次のようにパラメータを変更できます。

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>

        <!-- Database connection settings -->
        <property name="hibernate.connection.driver_class">com.mysql.cj.jdbc.Driver</property>
        <property name="hibernate.dialect">org.hibernate.dialect.TiDBDialect</property>
        <property name="hibernate.connection.url">jdbc:mysql://xxx.tidbcloud.com:4000/test?sslMode=VERIFY_IDENTITY&amp;enabledTLSProtocols=TLSv1.2,TLSv1.3</property>
        <property name="hibernate.connection.username">2aEp24QWEDLqRFs.root</property>
        <property name="hibernate.connection.password">123456</property>
        <property name="hibernate.connection.autocommit">false</property>

        <!-- Required so a table can be created from the 'PlayerDAO' class -->
        <property name="hibernate.hbm2ddl.auto">create-drop</property>

        <!-- Optional: Show SQL output for debugging -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>
    </session-factory>
</hibernate-configuration>
```

</div>

<div label="Using JDBC" value="jdbc">

TiDB サーバーレス クラスターを使用している場合は、 `JDBCExample.java`でホスト、ポート、ユーザー、およびパスワードのパラメーターを変更します。

```java
mysqlDataSource.setServerName("localhost");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("");
```

設定したパスワードが`123456`で、クラスターの詳細ページから取得した接続パラメーターが次であるとします。

-   エンドポイント: `xxx.tidbcloud.com`
-   ポート: `4000`
-   ユーザー: `2aEp24QWEDLqRFs.root`

この場合、次のようにパラメータを変更できます。

```java
mysqlDataSource.setServerName("xxx.tidbcloud.com");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("2aEp24QWEDLqRFs.root");
mysqlDataSource.setPassword("123456");
mysqlDataSource.setSslMode(PropertyDefinitions.SslMode.VERIFY_IDENTITY.name());
mysqlDataSource.setEnabledTLSProtocols("TLSv1.2,TLSv1.3");
```

</div>

</SimpleTab>

### ステップ 3.3 実行 {#step-3-3-run}

<SimpleTab groupId="language">

<div label="Using Mybatis (Recommended)" value="mybatis">

コードを実行するには、 `make prepare` 、 `make gen` 、 `make build` 、 `make run`をそれぞれ実行します。

```shell
make prepare
# this command executes :
# - `mysql --host 127.0.0.1 --port 4000 -u root < src/main/resources/dbinit.sql`
# - `mysql --host 127.0.0.1 --port 4000 -u root -e "TRUNCATE test.player"`

make gen
# this command executes :
# - `rm -f src/main/java/com/pingcap/model/Player.java`
# - `rm -f src/main/java/com/pingcap/model/PlayerMapper.java`
# - `rm -f src/main/resources/mapper/PlayerMapper.xml`
# - `mvn mybatis-generator:generate`

make build # this command executes `mvn clean package`
make run # this command executes `java -jar target/plain-java-mybatis-0.0.1-jar-with-dependencies.jar`
```

または、ネイティブ コマンドを使用することもできます。

```shell
mysql --host 127.0.0.1 --port 4000 -u root < src/main/resources/dbinit.sql
mysql --host 127.0.0.1 --port 4000 -u root -e "TRUNCATE test.player"
rm -f src/main/java/com/pingcap/model/Player.java
rm -f src/main/java/com/pingcap/model/PlayerMapper.java
rm -f src/main/resources/mapper/PlayerMapper.xml
mvn mybatis-generator:generate
mvn clean package
java -jar target/plain-java-mybatis-0.0.1-jar-with-dependencies.jar
```

または`make prepare` 、 `make gen` 、 `make build`および`make run`を組み合わせた`make`コマンドを直接実行します。

</div>

<div label="Using Hibernate (Recommended)" value="hibernate">

コードを実行するには、 `make build`と`make run`をそれぞれ実行します。

```shell
make build # this command executes `mvn clean package`
make run # this command executes `java -jar target/plain-java-jdbc-0.0.1-jar-with-dependencies.jar`
```

または、ネイティブ コマンドを使用することもできます。

```shell
mvn clean package
java -jar target/plain-java-jdbc-0.0.1-jar-with-dependencies.jar
```

または、 `make build`と`make run`を組み合わせた`make`コマンドを直接実行します。

</div>

<div label="Using JDBC" value="jdbc">

コードを実行するには、 `make build`と`make run`をそれぞれ実行します。

```shell
make build # this command executes `mvn clean package`
make run # this command executes `java -jar target/plain-java-jdbc-0.0.1-jar-with-dependencies.jar`
```

または、ネイティブ コマンドを使用することもできます。

```shell
mvn clean package
java -jar target/plain-java-jdbc-0.0.1-jar-with-dependencies.jar
```

または、 `make build`と`make run`を組み合わせた`make`コマンドを直接実行します。

</div>

</SimpleTab>

## ステップ 4. 期待される出力 {#step-4-expected-output}

<SimpleTab groupId="language">

<div label="Using Mybatis (Recommended)" value="mybatis">

[Mybatis の期待される出力](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-mybatis)

</div>

<div label="Using Hibernate (Recommended)" value="hibernate">

[Hibernate の予想される出力](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-hibernate)

</div>

<div label="Using JDBC" value="jdbc">

[JDBC の予期される出力](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-jdbc)

</div>

</SimpleTab>
