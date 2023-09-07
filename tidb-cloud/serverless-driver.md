---
title: TiDB serverless driver (Beta)
summary: Learn how to connect to TiDB serverless from serverless and edge environments over HTTP.
aliases: ['/tidbcloud/serverless-driver']
---

# TiDB serverless driver (Beta)

The [TiDB serverless driver (Beta)](https://github.com/tidbcloud/serverless-js) for JavaScript allows you to connect to TiDB serverless over HTTPS. It is particularly useful in serverless and edge environments where there is limited TCP support.

## Use the TiDB serverless driver

**Install**

You can install the driver with npm:

```bash
npm install @tidbcloud/serverless
```

**Query**

To query from TiDB serverless, you need to create a connection first. Then you can use the connection to execute raw SQL queries. For example:

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://username:password@host/database'})
const results = await conn.execute('select * from test where id = ?',[1])
```

**Transaction (Experimental)**

You can also perform interactive transactions with the TiDB serverless driver. For example:

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

Here are some examples of using the TiDB serverless driver at the edge. You can also try this [live demo](https://github.com/tidbcloud/car-sales-insight).

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

### Supported SQL

The following SQL statements are supported:  `Select`, `Show`, `Explain`, `Use`, `Insert`, `Update`, `Delete`, `Begin`, `Commit`, `Rollback`. Most of the DDL are supported.

### Data Type Mapping

The type mapping between TiDB Serverless and Javascript are as follows:

| TiDB Serverless Type | Javascript Type |
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

### Limitations

- Up to 10,000 rows can be fetched in a single query.
- You can execute only one SQL at a time, multiple SQLs in one query are not supported yet.

## Pricing

TiDB serverless driver generates the same costs as you use the TiDB serverless. Check the [TiDB serverless pricing](https://www.pingcap.com/tidb-serverless-pricing-details) for more details. 

## What's next

- [Learn how to configure TiDB serverless driver](/tidb-cloud/serverless-driver-config.md).
