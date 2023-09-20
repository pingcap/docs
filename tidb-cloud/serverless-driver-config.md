---
title: Configure TiDB Cloud Serverless Driver (Beta)
summary: Learn how to configure TiDB Cloud Serverless Driver.
---

# Configure TiDB Cloud Serverless Driver (Beta)

You can configure TiDB Cloud serverless driver at both the connection level and the SQL level.

## Connection level configurations

At the connection level, you can make the following configurations:

| Name       | Type       | Default value     | Description                                                                                                             |
|------------|------------|--------------|-------------------------------------------------------------------------------------------------------------------------|
| `username`   | string     | N/A          | Username of TiDB Serverless                                                                                             |
| `password`   | string     | N/A            | Password of TiDB Serverless                                                                                             |
| `host`       | string     | N/A           | Hostname of TiDB Serverless                                                                                             |
| `database`   | string     | `test`         | Database of TiDB Serverless                                                                                             |
| `url`        | string     | N/A            | The URL for the database, in the `mysql://username:password@host/database` format, where `database` can be skipped if you intend to connect to the default database.   |
| `fetch`      | function   | global fetch | Custom fetch function. For example, you can use the `undici` fetch in node.js.                                          |
| `arrayMode`  | bool       | `false`        | Whether to return results as arrays instead of objects. To get better performance, set it to `true`.                    |
| `fullResult` | bool       | `false`        | Whether to return full result object instead of just rows. To get more detailed results, set it to `true`.              |

### Database URL

> **Note:**
>
> You must percentage-encode special characters for your username,password and database, whether it in url or not. For example, password1@//? becomes password1%40%2F%2F%3F.

When `url` is configured, there is no need to configure `host`, `username`, `password`, and `database` separately. The following codes are equivalent:

```ts
const config = {
  host: '<host>',
  username: '<user>',
  password: '<password>',
  database: '<database>',
  arrayMode: true,
}

const conn = connect(config)
```

```ts
const config = {
  url: process.env['DATABASE_URL'] || 'mysql://username:password@host/database',
  arrayMode: true
}

const conn = connect(config)
```

## SQL level options

> **Note:**
>
> The SQL level options have a higher priority over connection level configurations.

At the SQL level, you can configure the following options:

| Option     | Type | Default value | Description                                                                                         |
|------------|------|---------|-----------------------------------------------------------------------------------------------------|
| `arrayMode`  | bool | `false`   | Whether to return results as arrays instead of objects. To get better performance, set it to `true`.  |
| `fullResult` | bool | `false`   | Whether to return full result object instead of just rows. To get more detailed results, set it to `true`.                                         |

For example:

```ts
const conn = connect({url: process.env['DATABASE_URL'] || 'mysql://username:password@host/database'})
const results = await conn.execute('select * from test',null,{arrayMode:true,fullResult:true})
```
