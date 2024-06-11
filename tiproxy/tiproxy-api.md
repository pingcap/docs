---
title: TiProxy API
summary: Learn how to use the TiProxy API to access its configuration, health status, and monitoring data.
---

# TiProxy API

[TiProxy](/tiproxy/tiproxy-overview.md) provides API endpoints for accessing its configuration, health status, and monitoring data.

> **Note:**
>
> TiProxy API is specifically designed for debugging purposes and might not be fully compatible with future capabilities introduced in TiProxy. It's not recommended to include this tool in application or utility development to get information.

The address for accessing the TiProxy API is `http://${host}:${port}${path}`, where `${host}:${port}` is specified by the TiProxy configuration item [`api.addr`](/tiproxy/tiproxy-configuration.md#addr-1), and `${path}` is the specific API endpoint you want to access. For example:

```bash
curl http://127.0.0.1:3080/api/admin/config/
```

## Get TiProxy configuration

### Request URI

`GET /api/admin/config/`

### Parameter descriptions

The query parameter is as follows:

- `format`: (optional) specifies the format of the returned configuration. Value options are `json` and `toml`. The default value is `toml`.

### Example

The following example gets the TiProxy configuration in JSON format:

```bash
curl "http://127.0.0.1:3080/api/admin/config/?format=json"
```

## Set TiProxy configuration

Currently, you can only use the TOML format to modify TiProxy configuration. Unspecified configuration items will remain unchanged, so you only need to specify the items that you want to modify.

### Request URI

`PUT /api/admin/config/`

### Request body

You need to provide the TiProxy configuration in TOML format. For example:

```toml
[log]
level='warning'
```

### Example

The following example sets `log.level` as `'warning'`, while leaving other configuration items unchanged.

1. Get the current TiProxy configuration:

    ```bash
    curl http://127.0.0.1:3080/api/admin/config/
    ```

    The output is as follows:

    ```toml
    [log]
    encoder = 'tidb'
    level = 'info'
    ```

2. Specify the value of `log.level` in the `test.toml` file, and then send a `PUT /api/admin/config/` request to update the value of `log.level`:

    ```shell
    $ cat test.toml
    [log]
    level='warning'
    $ curl -X PUT --data-binary @test.toml http://127.0.0.1:3080/api/admin/config/
    ```

3. Get the modified TiProxy configuration:

    ```bash
    curl http://127.0.0.1:3080/api/admin/config/
    ```

    The output is as follows:

    ```toml
    [log]
    encoder = 'tidb'
    level = 'warning'
    ```

## Get TiProxy health status

This endpoint is used to get the health status of TiProxy and the checksum of the configuration. When TiProxy is running normally, this endpoint returns the checksum of the configuration. When TiProxy is shutting down or offline, it returns an error.

### Request URI

`GET /api/debug/health`

### Example

```bash
curl http://127.0.0.1:3080/api/debug/health
```

The output is as follows:

```bash
{"config_checksum":3006078629}
```

## Get TiProxy monitoring data

### Request URI

`GET /metrics/`

### Example

```bash
curl http://127.0.0.1:3080/metrics/
```
