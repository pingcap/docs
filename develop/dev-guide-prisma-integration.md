---
title: Integrate TiDB with Prisma
summary: Introduce how to integrate TiDB with Prisma step by step.
---

# Integrate TiDB with Prisma

This document describes how to integrate **TiDB** with the Node.js ORM framework **Prisma**.

## Quick Start

### Startup TiDB Cluster

<SimpleTab groupId="startup-tidb">

<div label="TiDB Cloud" value="tidb-cloud">

You can refer to [Build a TiDB cluster in TiDB Cloud (Developer Tier)](/develop/dev-guide-build-cluster-in-cloud.md).

</div>

<div label="TiUP" value="tiup">

[TiUP](/tiup/tiup-overview.md), as the TiDB package manager, makes it easier to manage different cluster components in the TiDB ecosystem, such as TiDB, PD, and TiKV.

1. Install TiUP:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Start TiDB in a test environment:

    ```shell
    tiup playground
    ```

</div>

</SimpleTab>

## Startup CRUD Demo

1. Download the demo code and install its dependencies by `yarn`.

```shell
git clone https://github.com/pingcap/tidb-prisma-vercel-demo
cd tidb-prisma-vercel-demo
yarn
```

2. Config TiDB data source.

Add environment variables into the `.env` file in the project root directory.

```
DATABASE_URL="mysql://root@127.0.0.1:4000/test"
```

1. Start the demo.

```
yarn run dev
```

## Basic feature

### Connect to TiDB

1. Add the model definition to the `prisma/schema.prisma` file.

```prisma
datasource db {
  provider = "mysql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model Post {
  id        Int      @id @default(autoincrement())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  title     String   @db.VarChar(255)
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int

  @@index(authorId)
}

model Profile {
  id     Int     @id @default(autoincrement())
  bio    String?
  user   User    @relation(fields: [userId], references: [id])
  userId Int     @unique

  @@index(userId)
}

model User {
  id      Int      @id @default(autoincrement())
  email   String   @unique
  name    String?
  posts   Post[]
  profile Profile?
}
```

2. Run the following command to generate tables on TiDB according to the schema definition file `schema.prisma`.

```shell
npx prisma db push
```

### Query records

```typescript
const bookIds = [1, 2, 3];
const bookAverageRatings = await prisma.rating.groupBy({
    by: ['bookId'],
    _avg: {
      score: true
    },
    where: {
      bookId: {
        in: bookIds
      }
    },
    orderBy: {
      _avg: {
        score: 'asc'
      }
    }
});
```

### Create record

For example: add new rating for a book.

```typescript
// Insert a new rating record.
try {
    const resp = await prisma.rating.create({
        data: {
            bookId: bookId,
            userId: user.id,
            score: score,
            ratedAt: new Date()
        }
    });
    res.status(200).json({
        message: 'success',
        data: resp
    });
} catch(err: any) {
    // Error handling.
    //
    // Reference: https://www.prisma.io/docs/concepts/components/prisma-client/handling-exceptions-and-errors
    // About P2002: https://www.prisma.io/docs/reference/api-reference/error-reference#p2002
    if (err instanceof Prisma.PrismaClientKnownRequestError) {
        if (err.code === 'P2002') {
            res.status(200).json({
                message: `User <${user.id}> has already rate for book <${bookId}>.`
            });
        }
    } else {
        throw err
    }
}
```

### Update record

For example, update a book detail:

```typescript
const bookId = BigInt(req.query.id);
const updateData = {
    
};

return await prisma.book.update({
    data: updateData,
    where: {
        id: bookId
    }
});
```

### Delete record

For example: delete a book rating.

```typescript
// Delete a single rating record.
// 
// Reference: https://www.prisma.io/docs/concepts/components/prisma-client/crud#delete
try {
    await prisma.rating.delete({
        where: {
            bookId_userId: {
                bookId: bookId,
                userId: userId
            }
        }
    });
    res.status(200).json({
        message: 'success'
    });
} catch(err) {
    if (err instanceof Prisma.PrismaClientKnownRequestError) {
        // About P2025: https://www.prisma.io/docs/reference/api-reference/error-reference#p2025
        if (err.code === 'P2025') {
            res.status(200).json({
                message: `Rating record to delete does not exist.`
            });
        }
    } else {
        throw err
    }
}
```

### Transaction

For example: buy a book.

```typescript
try {
    const result = await prisma.$transaction(async prisma => {
        // Found the book that the user want to purchase.
        const book = await prisma.book.findFirst({
            where: {
                id: bookId
            },    
        });

        if (book === undefined || book === null) {
            throw new Error(`Can not found the book <${bookId}> that you want to buy.`);
        }

        // Check if has enough books for the user purchase.
        const stock = book.stock;
        if (quality > stock) {
            throw new Error(`Didn't have enough stock of book <${bookId}> for your purchase.`);
        }

        // Cost the user balance to buy the book.
        const cost = book?.price.mul(quality).toNumber();
        const purchaser = await prisma.user.update({
            data: {
                balance: {
                    decrement: cost,
                },
            },
            where: {
                id: userId,
            },
        });
        if (purchaser.balance.lt(0)) {
            throw new Error(`User <${userId}> doesn't have enough money to buy book <${bookId}>, which need to cost ${cost}.`)
        }

        // Update the book stock.
        const newBook = await prisma.book.update({
            data: {
                stock: {
                    decrement: 1,
                }
            },
            where: {
                id: bookId
            }
        });
        if (newBook.stock < 0) {
            throw new Error(`The book ${newBook.stock} is out of stock.`);
        }

        // Generate a new order to record.
        const order = prisma.order.create({
            data: {
                userId: userId,
                bookId: bookId,
                quality: quality
            }
        })

        return {
            userId: userId,
            bookId: bookId,
            bookTitle: book.title,
            cost: cost,
            remaining: purchaser.balance,
            orderId: order
        };
    });
    return {
        status: 200,
        message: `User <${userId}> buy ${quality} books <${bookId}> successfully, cost: ${result.cost}, remain: ${result.remaining} .`,
        data: result
    };
} catch(err: any) {
    console.error(err);
    return {
        status: 500,
        message: `Failed to buy book ${bookId} for user ${userId}: ${err.message}`
    };
}
```

## Testes

TODO:

- [TiDB with Prisma Client Integration Test](https://github.com/Icemap/tidb-proxysql-integration-test)
- [TiDB with Prisma Engines Integration Test](https://github.com/Mini256/prisma-engines/tree/fix-testes-for-tidb)

## Limitation and compatibility

- The default sorting of the query results of the `WHERE... IN...` statement is unstable. If you need a determined order, please explicitly declare it through the `ORDER BY` statement. (pingcap/tidb#37285)
- Do not support foreign key constraints (Issue: pingcap/tidb#18209, Develop plan: pingcap/tidb#36982)
- Do not support `FULLTEXT` indexes (pingcap/tidb#1793)
- Do not support GEO data types and `SPATIAL` indexes (pingcap/tidb#6347)
- In the 6.1 version and the previous version, TIDB does not support multiple SCHEMA changes in the one DDL statement. After version 6.2, it supports almost multiple schema changes (pingcap/tidb#14766)
- Primary key column 
  - Unsupported drop primary key when the table's `pkIsHandle` is `true`. 
  - Not allow setting `auto_increment` for an existing primary field by default.
  - Not allow removing `auto_increment` without `@@tidb_allow_remove_auto_inc` variable enabled.
- The default definition of some types in the `INFORMATION_SCHEMA.COLUMNS` table is different from MySQL
  - For `YEAR` type, TiDB shows the type as `year(4) unsigned`, while MySQL is `year`
  - For `BIT` type, TiDB shows the type as `bit(1) unsigned`, while MySQL is `bit(1)`
- TiDB table name is **case insensitive** by default, which is different from MySQL（pingcap/tidb#10817）

For more compatibility issues, please check MYSQL compatibility documents.

## Further reading

- [TiDB Developer Guide](/develop/dev-guide-overview.md)
- [Prisma Documentation](https://www.prisma.io/docs/getting-started)