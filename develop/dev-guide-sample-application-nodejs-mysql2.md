---
title: Build a Simple CRUD App with TiDB and node-mysql2
summary: Learn how to build a simple CRUD application with TiDB and mysql2 driver in Node.js.
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# Build a Simple CRUD App with TiDB and node-mysql2

[node-mysql2](https://github.com/sidorares/node-mysql2) is a popular open-source driver for Node.js.

This document describes how to use TiDB and node-mysql2 driver to build a simple CRUD application.

> **Note:**
> It is recommended to use Node.js 18.x or a later Node.js version.

## Step 1. Launch your TiDB cluster

<CustomContent platform="tidb">

The following introduces how to start a TiDB cluster.

**Use a TiDB Serverless cluster**

For detailed steps, see [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster).

**Use a local cluster**

For detailed steps, see [Deploy a local test cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a TiDB cluster using TiUP](/production-deployment-using-tiup.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

See [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster).

</CustomContent>

## Step 2. Get the code

Download the example code locally via Git command:

```shell
git clone https://github.com/pingcap/tidb-example-nodejs.git --depth=1
cd tidb-example-nodejs
```

The code for this example is located in the `node_mysql2/src/sample/index.js` file in the code repository, and the content is as follows:

```javascript
import {createConnection} from 'mysql2/promise';
import dotenv from "dotenv";
import {loadSampleData} from "../helper.js";
import path from "path";

// Main function.

async function main() {
    // Load environment variables from .env file.
    dotenv.config();

    // Load sample data.
    const conn = await createConnection(process.env.DATABASE_URL);
    try {
        await loadSampleData(conn, path.join(process.cwd(), 'sql/players.init.sql'));
    } finally {
        await conn.end();
    }

    // Run examples.
    console.log('[Simple Example Output]\n');
    await simple_example();

    console.log('\n[Bulk Example Output]\n');
    await  bulk_example();

    console.log('\n[Trade Example Output]\n');
    await  trade_example();
}

void main();

// Common functions.

async function getConnection() {
    return createConnection(process.env.DATABASE_URL);
}

// Simple example.

async function simple_example() {
    const conn = await getConnection();

    try {
        // Create player.
        const newPlayerID = await createPlayer(conn, {
            coins: 1,
            goods: 1,
        });
        console.log(`Created new player with ID ${newPlayerID}.`);

        // Get player by ID.
        const player = await getPlayerByID(conn, 3);
        console.log(`Get player by ID 3: Player { id:${player.id}, coins:${player.coins}, goods:${player.goods} }`);

        // Delete player by ID.
        await deletePlayerByID(conn, 3);
        console.log(`Deleted player with ID 3.`);

        // Count players.
        const playerTotal = await countPlayers(conn);
        console.log(`The total number of players: ${playerTotal}`);

        // List players with limit.
        console.log('List players with limit 3:')
        const players = await listPlayersWithLimit(conn, 3);
        players.forEach(p => {
            console.log(`- Player { id:${p.id}, coins:${p.coins}, goods:${p.goods} }`);
        });
    } finally {
        await conn.end();
    }
}

async function createPlayer(conn, player) {
    const [rsh] = await conn.execute(
        'INSERT INTO players (id, coins, goods) VALUES (?, ?, ?);',
        [player.id || null, player.coins, player.goods]
    );
    return rsh.insertId;
}

async function getPlayerByID(conn, playerId) {
    const [rows] = await conn.execute(
        'SELECT id, coins, goods FROM players WHERE id = ?;',
        [playerId]
    );
    return rows[0];
}

async function deletePlayerByID(conn, playerId) {
    const [rsh] = await conn.execute(
        'DELETE FROM players WHERE id = ?;',
        [playerId]
    );
    return rsh.affectedRows === 1;
}

async function listPlayersWithLimit(conn, limit) {
    const [rows] = await conn.query('SELECT id, coins, goods FROM players LIMIT ?;', [limit]);
    return rows;
}

async function countPlayers(conn) {
    const [rows] = await conn.execute('SELECT COUNT(*) AS cnt FROM players;');
    return rows[0]?.cnt || null;
}

// Bulk operations example.

async function bulk_example() {
    const conn = await getConnection();
    try {
        // Bulk create players.
        const players = [];
        for (let i = 1000; i < 2000; i++) {
            players.push([i, 10000, 10000]);
        }

        for (let i = 0; i < players.length; i += 200) {
            const chunk = players.slice(i, i + 200);
            const insertedRows = await bulkCreatePlayer(conn, chunk);
            console.log(`Bulk inserted ${insertedRows} rows.`);
        }
    } finally {
        await conn.end();
    }
}

async function bulkCreatePlayer(conn, players) {
    const [rsh] = await conn.query('INSERT INTO players (id, coins, goods) VALUES ?;', [players]);
    return rsh.affectedRows;
}

// Transaction example.

async function trade_example() {
    const conn = await getConnection();

    try {
        // Create players.
        await createPlayer(conn, { id: 101, coins: 100, goods: 0 });
        await createPlayer(conn, { id: 102, coins: 2000, goods: 20 });

        // Trade attempt 1.
        await trade(1, conn, 102, 101, 10, 500);

        // Trade attempt 2.
        await trade(2, conn, 102, 101, 2, 100);

        // Get player status.
        console.log('\nPlayer status after trade:');

        const player1 = await getPlayerByID(conn, 101);
        console.log(`- Player { id:101, coins:${player1.coins}, goods:${player1.goods} }`);

        const player2 = await getPlayerByID(conn, 102);
        console.log(`- Player { id:102, coins:${player2.coins}, goods:${player2.goods} }`);
    } finally {
        await conn.end();
    }
}

async function trade(tradeSeq, conn, sellId, buyId, amount, price) {
    console.log(`[Trade ${tradeSeq}] Doing trade ${amount} goods from player ${sellId} to player ${buyId} for ${price} coins.`)

    // Start transaction.
    await conn.beginTransaction();
    try {
        // Lock rows and check.
        const getPlayerSql = 'SELECT coins, goods FROM players WHERE id = ? FOR UPDATE;';

        const [sellRows] = await conn.execute(getPlayerSql, [sellId]);
        const sellGoods = sellRows[0].goods;
        const sellCoins = sellRows[0].coins;
        if (sellGoods < amount) {
            throw new Error(`The goods of sell player ${sellId} are not enough.`);
        }

        const [buyRows] = await conn.execute(getPlayerSql, [buyId]);
        const buyGoods = buyRows[0].goods;
        const buyCoins = buyRows[0].coins;
        if (buyCoins < price) {
            throw new Error(`The coins of buy player ${buyId} is not enough.`);
        }

        // Update if checks passed.
        const updatePlayerSql = 'UPDATE players SET goods = ?, coins = ? WHERE id = ?;';
        await conn.execute(updatePlayerSql, [sellGoods - amount, sellCoins + price, sellId]);
        await conn.execute(updatePlayerSql, [buyGoods + amount, buyCoins - price, buyId]);

        // Commit transaction.
        await conn.commit();
        console.log(`[Trade ${tradeSeq}] Trade success!`);
    } catch (error) {
        // Rollback transaction.
        await conn.rollback();
        console.error(`[Trade ${tradeSeq}] Trade failed (rollback the transaction): ${error.message}\n`);
    }
}
```

For more information about how to use node-mysql2, refer to documentation on the [node-mysql2 repository](https://github.com/sidorares/node-mysql2#mysql-2).

## Step 3. Run the code

The following content introduces how to run the code step by step.

### Step 3.1 Configure environment variables

Create a new `.env` file in the `node_mysql2` directory and add the environment variable `DATABASE_URL` to that file.

> **⚠️ Note:**
> Avoid using a production cluster to run the sample code, the sample program will delete the existing `players` table when initializing the table schema.

#### Environment variables `DATABASE_URL`

<SimpleTab groupId="cluster">

<div label="Local/Self-hosted cluster" value="local-cluster">

If you are using a local or self-hosted TiDB cluster (SSL is not enabled by default), you can fill in the `DATABASE_URL` in the following format:

```dotenv
DATABASE_URL=mysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DB_NAME>
```

<details>
<summary>Example <code>DATABASE_URL</code> for connecting to a TiUP Playground cluster</summary>

```dotenv
DATABASE_URL=mysql://root:password@127.0.0.1:4000/test
```

</details>

</div>

<div label="TiDB Cloud Serverless cluster" value="serverless-cluster">

If you are using a TiDB Cloud Serverless cluster, you must connect to the TiDB cluster over SSL, so you need to add the `ssl` parameter to `DATABASE_URL` in the following format:

```dotenv
DATABASE_URL=mysql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DB_NAME>?ssl={"minVersion":"TLSv1.2","rejectUnauthorized":true}
```

<details>
<summary>Example <code>DATABASE_URL</code> for connecting to a TiDB Serverless cluster</summary>

```dotenv
DATABASE_URL=mysql://xxxxx.root:password@gateway01.us-west-2.prod.aws.tidbcloud.com:4000/test?ssl={"minVersion":"TLSv1.2","rejectUnauthorized":true}
```

</details>

</div>

</SimpleTab>

### Step 3.2 Install dependencies

Install the dependencies required by the example code by executing the following command in the `node_mysql2` directory:

```shell
npm install
```

You can install the recommended version of the `mysql2` driver in your project code with the `npm install mysql2@3.5.2` command.

### Step 3.4 Run the code

Start the example program by executing the following command in the `node_mysql2` directory:

```shell
npm run demo:sample
```

## Step 4. Expected output

```
[Simple Example Output]

Created new player with ID 9.
Get player by ID 3: Player { id:3, coins:4, goods:256 }
Deleted player with ID 3.
The total number of players: 8
List players with limit 3:
- Player { id:1, coins:1, goods:1024 }
- Player { id:2, coins:2, goods:512 }
- Player { id:4, coins:8, goods:128 }

[Bulk Example Output]

Bulk inserted 200 rows.
Bulk inserted 200 rows.
Bulk inserted 200 rows.
Bulk inserted 200 rows.
Bulk inserted 200 rows.

[Trade Example Output]

[Trade 1] Doing trade 10 goods from player 102 to player 101 for 500 coins.
[Trade 1] Trade failed (rollback the transaction): The coins of buy player 101 is not enough.

[Trade 2] Doing trade 2 goods from player 102 to player 101 for 100 coins.
[Trade 2] Trade success!

Player status after trade:
- Player { id:101, coins:0, goods:2 }
- Player { id:102, coins:2100, goods:18 }
```

[Expected output of node-mysql2 sample code](https://github.com/pingcap/tidb-example-nodejs/tree/main/node_mysql2/src/sample#expected-output)
