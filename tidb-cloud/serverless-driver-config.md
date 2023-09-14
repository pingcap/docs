---
title: Configure TiDB Serverless Driver (Beta)
summary: Learn how to configure TiDB Serverless driver
---

# Configure TiDB Serverless driver (Beta)

TiDB Serverless driver provides connection level configurations and SQL level options. Learn how to configure TiDB Serverless driver.

## Connection level configurations

At the connection level, you can make the following configurations:

| name       | type       | default      | comment                                                                                                                 |
|------------|------------|--------------|-------------------------------------------------------------------------------------------------------------------------|
| username   | string     | /            | Username of TiDB Serverless                                                                                             |
| password   | string     | /            | Password of TiDB Serverless                                                                                             |
| host       | string     | /            | Host of TiDB Serverless                                                                                                 |
| database   | string     | test         | Database of TiDB Serverless                                                                                             |
| url        | string     | /            | A single url format as `mysql://username:password@host/database`. The `database` can be skipped to use the default one. |
| fetch      | function   | global fetch | Custom fetch function                                                                                                   |
| arrayMode  | bool       | false        | whether to return results as arrays instead of objects. Set it to `true` to get better performance.                     |
| fullResult | bool       | false        | whether to return full result object instead of just rows. Set it to `true` to get more details.                        |

### Database URL

For the URL of a single database, you can configure values for `host`, `username`, `password`, and `database`. The following codes are equivalent:

```ts
const config = {
  host: '<host>',
  username: '<user>',
  password: '<password>',
  database: '<database>'
}

const conn = connect(config)
```

```ts
const conn = connect({url: process.env['DATABASE_URL'] || 'mysql://username:password@host/database'})
```

## SQL level Options

> **Note:**
>
> The SQL level options have a higher priority over connection level configurations.

At the SQL level, you can configure the following options:

| Option     | Type | Default value | Description                                                                                         |
|------------|------|---------|-----------------------------------------------------------------------------------------------------|
| `arrayMode`  | bool | false   | whether to return results as arrays instead of objects. Set it to `true` to get better performance. |
| `fullResult` | bool | false   | whether to return full result object instead of rows only. Set it to `true` to get more details.                                         |

```ts
const conn = connect({url: process.env['DATABASE_URL'] || 'mysql://username:password@host/database'})
const results = await conn.execute('select * from test',null,{arrayMode:true,fullResult:true})
```
