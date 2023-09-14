---
title: TiDB Serverless Driver (Beta)
summary: Learn how to connect to TiDB Serverless from serverless and edge environments over HTTP.
---

# TiDB Serverless driver (Beta)

[TiDB Serverless Driver (Beta)](https://github.com/tidbcloud/serverless-js) for JavaScript allows you to connect to your TiDB Serverless cluster over HTTPS. It is particularly useful in edge environments where TCP connections are limited.

## Install the TiDB Serverless driver

You can install the driver with npm:

```bash
npm install @tidbcloud/serverless
```

## Use the TiDB Serverless driver

You can use TiDB Serverless Driver to query data of a TiDB Serverless cluster or perform interactive transactions.

### Query

To query data from a TiDB Serverless cluster, you need to create a connection first. Then you can use the connection to execute raw SQL queries. For example:

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://username:password@host/database'})
const results = await conn.execute('select * from test where id = ?',[1])
```

### Transaction (Experimental)

You can also perform interactive transactions with the TiDB Serverless driver. For example:

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://username:password@host/database'})
const tx = await conn.begin()

try {
  await tx.execute('insert into test values (1)')
  await tx.execute('select * from test')
  await tx.commit()
}catch (err) {
  await tx.rollback()
  throw err
}
```

## Edge Examples

Here are some examples of using the TiDB Serverless driver in edge environments. For a complete example, you can also try this [live demo](https://github.com/tidbcloud/car-sales-insight).

<SimpleTab>

<div label="Vercel Edge Function">

```ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { connect } from '@tidbcloud/serverless'
export const runtime = 'edge'

export async function GET(request: NextRequest) {
  const conn = connect({url: process.env.DATABASE_URL})
  const result = await conn.execute('show tables')
  return NextResponse.json({result});
}
```

</div>

<div label="Cloudflare Workers">

```ts
import { connect } from '@tidbcloud/serverless'
export interface Env {
  DATABASE_URL: string;
}
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const conn = connect({url: env.DATABASE_URL})
    const result = await conn.execute('show tables')
    return new Response(JSON.stringify(result));
  },
};
```

</div>

<div label="Netlify Edge Function">

```ts
import { connect } from 'https://esm.sh/@tidbcloud/serverless'

export default async () => {
  const conn = connect({url: Netlify.env.get('DATABASE_URL')})
  const result = await conn.execute('show tables')
  return new Response(JSON.stringify(result));
}
```

</div>

<div label="Supabase Edge Function">

```ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { connect } from 'https://esm.sh/@tidbcloud/serverless'

serve(async (req) => {

  const conn = connect({url: Deno.env.get('DATABASE_URL')})
  const result = await conn.execute('show tables')
  return new Response(
      JSON.stringify(result),
      { headers: { "Content-Type": "application/json" } },
  )
})
```

</div>

<div label="Deno">

```ts
import { connect } from "npm:@tidbcloud/serverless-js"

const conn = connect({url: Deno.env.get('DATABASE_URL')})
const result = await conn.execute('show tables')
```

</div>

</SimpleTab>

## Features

### Supported SQL statements

The following SQL statements are supported:  `SELECT`, `SHOW`, `EXPLAIN`, `USE`, `INSERT`, `UPDATE`, `DELETE`, `BEGIN`, `COMMIT`, `ROLLBACK`. DDL is supported.

### Data type mapping

The type mapping between TiDB Serverless and Javascript is as follows:

| TiDB Serverless type | Javascript type |
|----------------------|-----------------|
| TINYINT              | number          |
| UNSIGNED TINYINT     | number          |
| BOOL                 | number          |
| SMALLINT             | number          |
| UNSIGNED SMALLINT    | number          |
| MEDIUMINT            | number          |
| INT                  | number          |
| UNSIGNED INT         | number          |
| YEAR                 | number          |
| FLOAT                | number          |
| DOUBLE               | number          |
| BIGINT               | string          |
| UNSIGNED BIGINT      | string          |
| DECIMAL              | string          |
| CHAR                 | string          |
| VARCHAR              | string          |
| BINARY               | string          |
| VARBINARY            | string          |
| TINYTEXT             | string          |
| TEXT                 | string          |
| MEDIUMTEXT           | string          |
| LONGTEXT             | string          |
| TINYBLOB             | string          |
| BLOB                 | string          |
| MEDIUMBLOB           | string          |
| LONGBLOB             | string          |
| DATE                 | string          |
| TIME                 | string          |
| DATETIME             | string          |
| TIMESTAMP            | string          |
| ENUM                 | string          |
| SET                  | string          |
| BIT                  | string          |
| JSON                 | object          |
| NULL                 | null            |
| Others               | string          |

## Pricing

TiDB Serverless Driver follows the [TiDB Serverless pricing](https://www.pingcap.com/tidb-serverless-pricing-details/) model. The driver itself is free but using the driver to access data generates Request Units (RUs) and storage usage.

## Limitations

Currently, using TiDB Serverless Driver has the following limitations:

- Up to 10,000 rows can be fetched in a single query.
- You can execute only a single SQL statement at a time, multiple SQL statements in one query are not supported yet.
- Connection with [private endpoints](/tidb-cloud/set-up-private-endpoint-connections-serverless.md) is not supported yet.

## What's next

- [Learn how to configure TiDB Serverless driver](/tidb-cloud/serverless-driver-config.md).
- [Learn how to use Kysely ORM with TiDB Serverless driver dialect](https://github.com/tidbcloud/kysely).