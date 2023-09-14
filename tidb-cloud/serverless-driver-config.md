---
title: Configure TiDB Serverless Driver (Beta)
summary: Learn how to configure TiDB Serverless driver
---

# Configure TiDB Serverless driver (Beta)

TiDB Serverless driver provides connection level configurations and SQL level options. Learn how to configure TiDB Serverless driver.

## Connection level Configurations

The following configurations are supported in connection level:

| name       | type       | default      | comment                                                                                                                  |
|------------|------------|--------------|--------------------------------------------------------------------------------------------------------------------------|
| username   | string     | /            | Username of TiDB Serverless                                                                                              |
| password   | string     | /            | Password of TiDB Serverless                                                                                              |
| host       | string     | /            | Host of TiDB Serverless                                                                                                  |
| database   | string     | test         | Database of TiDB Serverless                                                                                              |
| url        | string     | /            | A single url format as `mysql://username:password@host/database`. The `database` can be skipped to use the default one.  |
| fetch      | function   | global fetch | Custom fetch function                                                                                                    |
| arrayMode  | bool       | false        | whether to return results as arrays instead of objects                                                                   |
| fullResult | bool       | false        | whether to return full result object instead of just rows                                                                |

### Database URL

A single database URL value can be used to configure the `host`, `username`, `password` and `database` values. The following codes are equivalent:

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

> Note: SQL level options priority is higher than connection level configurations.

The following options are supported in SQL level:

| option     | type | default | comment                                                   |
|------------|------|---------|-----------------------------------------------------------|
| arrayMode  | bool | false   | whether to return results as arrays instead of objects    |
| fullResult | bool | false   | whether to return full result object instead of just rows |

```ts
const conn = connect({url: process.env['DATABASE_URL'] || 'mysql://username:password@host/database'})
const results = await conn.execute('select * from test',null,{arrayMode:true,fullResult:true})
```
