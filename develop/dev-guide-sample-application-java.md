---
title: Build a Simple CRUD App with TiDB and Java
summary: Learn how to build a simple CRUD application with TiDB and Java.
---

<!-- markdownlint-disable MD024 -->

<!-- markdownlint-disable MD029 -->

# TiDBとJavaを使用してシンプルなCRUDアプリを構築する {#build-a-simple-crud-app-with-tidb-and-java}

このドキュメントでは、TiDBとJavaを使用して単純なCRUDアプリケーションを構築する方法について説明します。

> **ノート：**
>
> Java8以降のJavaバージョンを使用することをお勧めします。
>
> アプリケーション開発にSpringBootを使用する場合は、 [SpringBootを使用してTiDBアプリケーションを構築する](/develop/dev-guide-sample-application-spring-boot.md)を参照してください。

## ステップ1.TiDBクラスタを起動します {#step-1-launch-your-tidb-cluster}

以下に、TiDBクラスタを開始する方法を紹介します。

### TiDB Cloudの無料クラスタを使用する {#use-a-tidb-cloud-free-cluster}

詳細な手順については、 [無料のクラスタを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-free-cluster)を参照してください。

### ローカルクラスタを使用する {#use-a-local-cluster}

詳細な手順については、 [ローカルテストクラスタをデプロイする](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[TiUPを使用してTiDBクラスターをデプロイする](/production-deployment-using-tiup.md)を参照してください。

## ステップ2.コードを取得する {#step-2-get-the-code}

{{< copyable "" >}}

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
```

<SimpleTab>

<div label="Using JDBC" href="get-code-jdbc">

`plain-java-jdbc`ディレクトリに移動します。

{{< copyable "" >}}

```shell
cd plain-java-jdbc
```

このディレクトリの構造は次のとおりです。

```
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
```

テーブル作成の初期化ステートメントは`dbinit.sql`にあります。

{{< copyable "" >}}

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

`JDBCExample.java`は`plain-java-jdbc`の本体です。 TiDBはMySQLプロトコルとの互換性が高いため、TiDBに接続するにはMySQLソースインスタンス`MysqlDataSource`を初期化する必要があります。次に、オブジェクト管理用に`PlayerDAO`を初期化し、それを使用してデータの読み取り、編集、追加、および削除を行うことができます。

`PlayerDAO`はデータの管理に使用されるクラスで、 `DAO`は[データアクセスオブジェクト](https://en.wikipedia.org/wiki/Data_access_object)を意味します。このクラスは、データを書き込む機能を提供する一連のデータ操作メソッドを定義します。

`PlayerBean`は、テーブルのマッピングであるデータエンティティクラスです。 `PlayerBean`の各プロパティは、 `player`テーブルのフィールドに対応します。

{{< copyable "" >}}

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

<div label="Using Hibernate (Recommended)" href="get-code-hibernate">

Hibernateと比較すると、JDBC実装はベストプラクティスではない可能性があります。これは、エラー処理ロジックを手動で作成する必要があり、コードを簡単に再利用できないため、コードがわずかに冗長になるためです。

Hibernateは人気のあるオープンソースのJavaORMであり、TiDBの機能によく適合する`v6.0.0.Beta2`から始まるTiDB方言をサポートします。次の手順では、例として`v6.0.0.Beta2`を取り上げます。

`plain-java-hibernate`ディレクトリに移動します。

{{< copyable "" >}}

```shell
cd plain-java-hibernate
```

このディレクトリの構造は次のとおりです。

```
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
```

`hibernate.cfg.xml`はHibernate構成ファイルです。

{{< copyable "" >}}

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

`HibernateExample.java`は`plain-java-hibernate`の本体です。 JDBCと比較して、Hibernateを使用する場合、Hibernateは異なるデータベース間のデータベース作成の違いを回避するため、構成ファイルのパスを書き込むだけで済みます。

`PlayerDAO`はデータの管理に使用されるクラスで、 `DAO`は[データアクセスオブジェクト](https://en.wikipedia.org/wiki/Data_access_object)を意味します。このクラスは、データを書き込むための一連のデータ操作メソッドを定義します。 JDBCと比較すると、Hibernateは、オブジェクトマッピングや基本オブジェクトのCRUDなどの多数の操作をカプセル化するため、コードが大幅に簡素化されます。

`PlayerBean`は、テーブルのマッピングであるデータエンティティクラスです。 `PlayerBean`の各プロパティは、 `player`テーブルのフィールドに対応します。 JDBCと比較して、Hibernateの`PlayerBean`は、より多くの情報のマッピング関係を示す注釈を追加します。

{{< copyable "" >}}

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

</SimpleTab>

## ステップ3.コードを実行します {#step-3-run-the-code}

次のコンテンツでは、コードを段階的に実行する方法を紹介します。

### ステップ3.1テーブルの初期化 {#step-3-1-table-initialization}

<SimpleTab>

<div label="Using JDBC" href="jdbc-table-init-jdbc">

JDBCを使用する場合は、データベーステーブルを手動で初期化する必要があります。ローカルクラスタを使用していて、MySQLクライアントがローカルにインストールされている場合は、次の`plain-java-jdbc`のディレクトリで直接実行できます。

{{< copyable "" >}}

```shell
make mysql
```

または、次のコマンドを実行できます。

{{< copyable "" >}}

```shell
mysql --host 127.0.0.1 --port 4000 -u root<src/main/resources/dbinit.sql
```

非ローカルクラスタを使用している場合、またはMySQLクライアントがインストールされていない場合は、クラスタに接続して`src/main/resources/dbinit.sql`ファイルのステートメントを実行します。

</div>

<div label="Using Hibernate (Recommended)" href="jdbc-table-init-hibernate">

テーブルを手動で初期化する必要はありません。

</div>

</SimpleTab>

### ステップTiDB Cloudのパラメーターを変更する {#step-3-2-modify-parameters-for-tidb-cloud}

<SimpleTab>

<div label="Using JDBC" href="tidb-cloud-jdbc">

TiDB Cloudやその他のリモートクラスターなど、ローカル以外のデフォルトクラスタを使用している場合は、ホスト、ポート、ユーザー、およびパスワードのパラメーターを`JDBCExample.java`で変更します。

{{< copyable "" >}}

```java
mysqlDataSource.setServerName("localhost");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("");
```

設定したパスワードが`123456`で、 TiDB Cloudから取得した接続文字列が次のとおりであるとします。

```
mysql --connect-timeout 15 -u root -h xxx.tidbcloud.com -P 4000 -p
```

この場合、次のようにパラメータを変更できます。

{{< copyable "" >}}

```java
mysqlDataSource.setServerName("xxx.tidbcloud.com");
mysqlDataSource.setPortNumber(4000);
mysqlDataSource.setDatabaseName("test");
mysqlDataSource.setUser("root");
mysqlDataSource.setPassword("123456");
```

</div>

<div label="Using Hibernate (Recommended)" href="tidb-cloud-hibernate">

`hibernate.connection.password` TiDB Cloudや`hibernate.cfg.xml`のリモートクラスタなど、ローカル以外のデフォルトクラスタを使用している場合は、 `hibernate.connection.url`を変更し`hibernate.connection.username` 。

{{< copyable "" >}}

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

設定したパスワードが`123456`で、 TiDB Cloudから取得した接続文字列が次のとおりであるとします。

{{< copyable "" >}}

```shell
mysql --connect-timeout 15 -u root -h tidb.e049234d.d40d1f8b.us-east-1.prod.aws.tidbcloud.com -P 4000 -p
```

この場合、次のようにパラメータを変更できます。

{{< copyable "" >}}

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
        <property name="hibernate.connection.url">jdbc:mysql://tidb.e049234d.d40d1f8b.us-east-1.prod.aws.tidbcloud.com:4000/test</property>
        <property name="hibernate.connection.username">root</property>
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

</SimpleTab>

### ステップ3.3実行 {#step-3-3-run}

<SimpleTab>

<div label="Using JDBC" href="run-jdbc">

コードを実行するには、それぞれ`make build`と`make run`を実行します。

{{< copyable "" >}}

```shell
make build # this command executes `mvn clean package`
make run # this command executes `java -jar target/plain-java-jdbc-0.0.1-jar-with-dependencies.jar`
```

または、ネイティブコマンドを使用できます。

{{< copyable "" >}}

```shell
mvn clean package
java -jar target/plain-java-jdbc-0.0.1-jar-with-dependencies.jar
```

または、 `make build`と`make run`の組み合わせである`make`コマンドを直接実行します。

</div>

<div label="Using Hibernate (Recommended)" href="run-hibernate">

コードを実行するには、それぞれ`make build`と`make run`を実行します。

{{< copyable "" >}}

```shell
make build # this command executes `mvn clean package`
make run # this command executes `java -jar target/plain-java-jdbc-0.0.1-jar-with-dependencies.jar`
```

または、ネイティブコマンドを使用できます。

{{< copyable "" >}}

```shell
mvn clean package
java -jar target/plain-java-jdbc-0.0.1-jar-with-dependencies.jar
```

または、 `make build`と`make run`の組み合わせである`make`コマンドを直接実行します。

</div>

</SimpleTab>

## ステップ4.期待される出力 {#step-4-expected-output}

<SimpleTab>

<div label="Using JDBC" href="output-jdbc">

[JDBCの期待される出力](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-jdbc)

</div>

<div label="Using Hibernate (Recommended)" href="output-hibernate">

[Hibernateの期待される出力](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-hibernate)

</div>

</SimpleTab>
