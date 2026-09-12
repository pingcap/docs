---
title: 使用 LakeSQL 连接到 TiDB Cloud Lake
summary: LakeSQL 是专为 {{{ .lake }}} 设计的命令行工具。它允许用户建立与 {{{ .lake }}} 的连接，并直接在 CLI 窗口中执行查询。
---

# 使用 LakeSQL 连接到 TiDB Cloud Lake

[LakeSQL](https://github.com/tidbcloud/lakesql) 是专为 {{{ .lake }}} 设计的命令行工具。它允许用户建立与 {{{ .lake }}} 的连接，并直接在 CLI 窗口中执行查询。

LakeSQL 特别适合偏好命令行接口并且需要经常使用 {{{ .lake }}} 的用户。借助 LakeSQL，用户可以轻松高效地管理数据库、表和数据，并便捷地执行各种查询和操作。

## 安装 LakeSQL {#installing-lakesql}

LakeSQL 提供了多种安装方式，以适配不同的平台和使用偏好。你可以从以下各节中选择适合自己的方法，或者从 [LakeSQL release page](https://github.com/tidbcloud/lakesql/releases) 下载安装包进行手动安装。

### Shell 脚本 {#shell-script}

LakeSQL 提供了便捷的 Shell 安装脚本。你可以选择以下两种方式之一：

#### 默认安装 {#default-installation}

将 LakeSQL 安装到用户的主目录 (~/.lakesql)：

```bash
curl -fsSL https://lakesql-bin.tidbcloud.com/install/lakesql.sh | bash
```

```bash title='Example:'
# highlight-next-line
curl -fsSL https://lakesql-bin.tidbcloud.com/install/lakesql.sh | bash

                                  L A K E S Q L
                                    Installer

--------------------------------------------------------------------------------
Website: https://tidbcloud.com
Docs: https://docs.pingcap.com/tidbcloudlake/
Github: https://github.com/tidbcloud/lakesql
--------------------------------------------------------------------------------

>>> We'll be installing LakeSQL via a pre-built archive at https://lakesql-bin.tidbcloud.com/lakesql/v0.22.2/
>>> Ready to proceed? (y/n)

>>> Please enter y or n.
>>> y

--------------------------------------------------------------------------------

>>> Downloading LakeSQL archive via https://lakesql-bin.tidbcloud.com/lakesql/v0.22.2/lakesql-aarch64-apple-darwin.tar.gz ✓
>>> Unpacking archive to /Users/eric/.lakesql ... ✓
>>> Adding LakeSQL path to /Users/eric/.zprofile ✓
>>> Adding LakeSQL path to /Users/eric/.profile ✓
>>> Install succeeded! 🚀
>>> To start LakeSQL:

    lakesql --help

>>> More information at https://github.com/tidbcloud/lakesql
```

#### 使用 `--prefix` 自定义安装 {#custom-installation-with-prefix}

将 LakeSQL 安装到指定目录（例如 /usr/local）：

```bash
curl -fsSL https://lakesql-bin.tidbcloud.com/install/lakesql.sh | bash -s -- -y --prefix /usr/local
```

```bash title='Example:'
# highlight-next-line
curl -fsSL https://lakesql-bin.tidbcloud.com/install/lakesql.sh | bash -s -- -y --prefix /usr/local
                                  L A K E S Q L
                                    Installer

--------------------------------------------------------------------------------
Website: https://tidbcloud.com
Docs: https://docs.pingcap.com
Github: https://github.com/tidbcloud/lakesql
--------------------------------------------------------------------------------

>>> Downloading LakeSQL via https://lakesql-bin.tidbcloud.com/lakesql/v0.22.2/lakesql-aarch64-apple-darwin.tar.gz ✓
>>> Unpacking archive to /usr/local ... ✓
>>> Install succeeded! 🚀
>>> To start LakeSQL:

    lakesql --help

>>> More information at https://github.com/tidbcloud/lakesql
```

### Homebrew（适用于 macOS） {#homebrew-for-macos}

在 macOS 上，你可以使用 Homebrew 通过一条简单的命令轻松安装 LakeSQL：

```bash
brew install tidbcloud/homebrew-tap/lakesql
```

### Apt（适用于 Ubuntu/Debian） {#apt-for-ubuntu-debian}

在 Ubuntu 和 Debian 系统上，你可以使用 Apt 包管理器安装 LakeSQL：

```bash
curl -fsSL https://lakesql-bin.tidbcloud.com/keys/lakesql-archive-keyring.gpg \
  | sudo tee /usr/share/keyrings/lakesql-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/lakesql-archive-keyring.gpg] https://lakesql-bin.tidbcloud.com/apt stable main" \
  | sudo tee /etc/apt/sources.list.d/lakesql.list >/dev/null
sudo apt-get update
sudo apt-get install -y lakesql
```

### Cargo（Rust 包管理器） {#cargo-rust-package-manager}

要使用 Cargo 安装 LakeSQL，可以使用 `cargo-binstall` 工具，或者通过提供的命令从源码构建。

> **Note:**
>
> 在使用 Cargo 安装之前，请确保你的计算机上已安装完整的 Rust 工具链以及 `cargo` 命令。如果尚未安装，请参考 [https://rustup.rs/](https://rustup.rs/) 上的安装指南。

**使用 cargo-binstall**

请参考 [Cargo B(inary)Install - Installation](https://github.com/cargo-bins/cargo-binstall#installation) 安装 `cargo-binstall`，并启用 `cargo binstall <crate-name>` 子命令。

```bash
cargo binstall lakesql
```

**从源码构建**

从源码构建时，某些依赖项可能涉及编译 C/C++ 代码。请确保你的计算机上已安装 GCC/G++ 或 Clang 工具链。

```bash
cargo install lakesql
```

## 用户认证 {#user-authentication}

对于连接到 {{{ .lake }}}，你可以使用默认的 `cloudapp` 用户，或者使用通过 [CREATE USER](/tidb-cloud-lake/sql/create-user.md) 命令创建的 SQL 用户。请注意，你用于登录 [{{{ .lake }}} console](https://app.lake.tidbcloud.com) 的用户账户不能用于连接到 {{{ .lake }}}。

## 使用 LakeSQL 连接 {#connecting-with-lakesql}

LakeSQL 支持连接到 {{{ .lake }}} 实例。

### 使用 DSN 自定义连接 {#customize-connections-with-a-dsn}

DSN（Data Source Name）是一种简单而强大的方式，可让你在 LakeSQL 中使用单个 URI 风格的字符串来配置和管理 {{{ .lake }}} 连接。通过这种方式，你可以将凭证和连接设置直接嵌入到环境中，从而简化连接过程。

#### DSN 格式和参数 {#dsn-format-and-parameters}

```bash title='DSN Format'
lake[+flight]://user[:password]@host[:port]/[database][?sslmode=disable][&arg1=value1]
```

| 常见 DSN 参数 | 描述                          |
|-----------------------|--------------------------------------|
| `tenant`              | 租户 ID，仅适用于 {{{ .lake }}}。      |
| `warehouse`           | 计算集群名称，仅适用于 {{{ .lake }}}。 |
| `sslmode`             | 如果不使用 TLS，则设置为 `disable`。   |
| `tls_ca_file`         | 自定义根 CA 证书路径。                 |
| `connect_timeout`     | 连接超时时间（秒）。                   |

| RestAPI 客户端参数   | 描述                                                                                                                   |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `wait_time_secs`            | 页面请求等待时间，默认为 `1`。                                                                                                |
| `max_rows_in_buffer`        | 页面缓冲区中的最大行数。                                                                                                      |
| `max_rows_per_page`         | 单个页面响应的最大行数。                                                                                                      |
| `page_request_timeout_secs` | 单个页面请求的超时时间，默认为 `30`。                                                                                         |
| `presign`                   | 为数据加载启用 presign。可选值：`auto`、`detect`、`on`、`off`。默认值为 `auto`（仅对 {{{ .lake }}} 启用）。 |

| FlightSQL 客户端参数 | 描述                                                                 |
|-----------------------------|----------------------------------------------------------------------|
| `query_timeout`             | 查询超时时间（秒）。                                                 |
| `tcp_nodelay`               | 默认为 `true`。                                                      |
| `tcp_keepalive`             | TCP keepalive 时间（秒）（默认值为 `3600`，设置为 `0` 可禁用）。     |
| `http2_keep_alive_interval` | keep-alive 间隔时间（秒），默认值为 `300`。                          |
| `keep_alive_timeout`        | keep-alive 超时时间（秒），默认值为 `20`。                           |
| `keep_alive_while_idle`     | 默认为 `true`。                                                      |

#### DSN 示例 {#dsn-examples}

```bash
# Local connection using HTTP API with presign detection
lake://root:@localhost:8000/?sslmode=disable&presign=detect

# {{{ .lake }}} connection with tenant and warehouse info
lake://user1:password1@tnxxxx--default.gw.aws-us-east-2.default.tidbcloud.com:443/benchmark?enable_dphyp=1

# Local connection using FlightSQL API
lake+flight://root:@localhost:8900/database1?connect_timeout=10
```

### 连接到 {{{ .lake }}} {#connect-to-lake}

连接到 {{{ .lake }}} 的最佳实践是从 {{{ .lake }}} 获取你的 DSN，并将其导出为环境变量。要获取 DSN，请执行以下操作：

1. 登录 {{{ .lake }}}，然后在 **Overview** 页面点击 **Connect**。

2. 选择你要连接的数据库和计算集群 (Warehouse)。

3. 你的 DSN 会在 **Examples** 部分自动生成。在 DSN 下方，你会看到一段 LakeSQL 代码片段，它会将 DSN 导出为名为 `LAKESQL_DSN` 的环境变量，并使用正确的配置启动 LakeSQL。你可以直接将其复制并粘贴到终端中。

    ```bash title='Example'
    export LAKESQL_DSN="lake://cloudapp:******@tn3ftqihs.gw.aws-us-east-2.default.tidbcloud.com:443/information_schema?warehouse=small-xy2t"
    lakesql
    ```

## LakeSQL 设置 {#lakesql-settings}

LakeSQL 提供了一系列设置，用于定义如何展示查询结果：

| 设置              | 描述                                                                                                                                                 |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `display_pretty_sql` | 设置为 `true` 时，SQL 查询会以更美观的方式格式化显示，从而更易于阅读和理解。                                                                                |
| `prompt`             | 命令行接口中显示的提示符，通常用于指示当前访问的用户、计算集群和数据库。                                                                                    |
| `progress_color`     | 指定进度指示器使用的颜色，例如在执行需要一定时间才能完成的查询时。                                                                                          |
| `show_progress`      | 设置为 `true` 时，会显示进度指示器，以展示长时间运行的查询或操作的进度。                                                                                    |
| `show_stats`         | 如果为 `true`，则在每次执行查询后显示查询统计信息，例如执行时间、读取的行数和处理的字节数。                                                                |
| `max_display_rows`   | 设置查询结果输出中显示的最大行数。                                                                                                                          |
| `max_col_width`      | 设置每列显示渲染的最大字符宽度。小于 3 的值会禁用该限制。                                                                                                   |
| `max_width`          | 设置整个显示输出的最大字符宽度。值为 0 时，默认使用终端窗口的宽度。                                                                                         |
| `output_format`      | 设置用于显示查询结果的格式（`table`, `csv`, `tsv`, `null`）。                                                                                               |
| `expand`             | 控制查询输出是以单条记录形式显示，还是以表格形式显示。可选值：`on`、`off` 和 `auto`。                                                                      |
| `multi_line`         | 决定是否允许 SQL 查询使用多行输入。设置为 `true` 时，查询可以跨多行书写，以提高可读性。                                                                     |
| `replace_newline`    | 指定是否将查询结果输出中的换行符替换为空格。这可以避免显示中出现非预期的换行。                                                                              |

有关各项设置的详细信息，请参阅以下参考内容：

### `display_pretty_sql` {#display-pretty-sql}

`display_pretty_sql` 设置用于控制 SQL 查询是否以视觉上格式化的方式显示。设置为 `false` 时，如下面第一个查询所示，SQL 查询不会为了美观而进行格式化。相反，设置为 `true` 时，如第二个查询所示，SQL 查询会以更美观的方式格式化显示，从而更易于阅读和理解。

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set display_pretty_sql false
root@localhost:8000/default> SELECT TO_STRING(ST_ASGEOJSON(ST_GEOMETRYFROMWKT('SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'))) AS pipeline_geojson;
┌─────────────────────────────────────────────────────────────────────────┐
│                             pipeline_geojson                            │
│                                  String                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ {"coordinates":[[400000,6000000],[401000,6010000]],"type":"LineString"} │
└─────────────────────────────────────────────────────────────────────────┘
1 row read in 0.063 sec. Processed 1 row, 1 B (15.76 rows/s, 15 B/s)

// highlight-next-line
root@localhost:8000/default> !set display_pretty_sql true
root@localhost:8000/default> SELECT TO_STRING(ST_ASGEOJSON(ST_GEOMETRYFROMWKT('SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'))) AS pipeline_geojson;

SELECT
  TO_STRING(
    ST_ASGEOJSON(
      ST_GEOMETRYFROMWKT(
        'SRID=4326;LINESTRING(400000 6000000, 401000 6010000)'
      )
    )
  ) AS pipeline_geojson

┌─────────────────────────────────────────────────────────────────────────┐
│                             pipeline_geojson                            │
│                                  String                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ {"coordinates":[[400000,6000000],[401000,6010000]],"type":"LineString"} │
└─────────────────────────────────────────────────────────────────────────┘
1 row read in 0.087 sec. Processed 1 row, 1 B (11.44 rows/s, 11 B/s)
```

### `prompt` {#prompt}

`prompt` 设置用于控制命令行接口提示符的格式。在下面的示例中，它最初被设置为显示用户和计算集群（`{user}@{warehouse}`）。更新为 `{user}@{warehouse}/{database}` 后，提示符现在会包含用户、计算集群和数据库。

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set prompt {user}@{warehouse}
root@localhost:8000 !configs
Settings {
    display_pretty_sql: true,
    prompt: "{user}@{warehouse}",
    progress_color: "cyan",
    show_progress: true,
    show_stats: true,
    max_display_rows: 40,
    max_col_width: 1048576,
    max_width: 1048576,
    output_format: Table,
    quote_style: Necessary,
    expand: Off,
    time: None,
    multi_line: true,
    replace_newline: true,
}
// highlight-next-line
root@localhost:8000 !set prompt {user}@{warehouse}/{database}
root@localhost:8000/default
```

### `progress_color` {#progress-color}

`progress_color` 设置用于控制查询执行期间进度指示器使用的颜色。在此示例中，颜色已设置为 `blue`：

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set progress_color blue
```

### `show_progress` {#show-progress}

设置为 `true` 时，会在查询执行期间显示进度信息。进度信息包括已处理的行数、查询中的总行数、每秒处理的行数、已处理的内存量，以及每秒处理的内存速度。

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set show_progress true
root@localhost:8000/default> select * from numbers(1000000000000000);
⠁ [00:00:08] Processing 18.02 million/1 quadrillion (2.21 million rows/s), 137.50 MiB/7.11 PiB (16.88 MiB/s) ░
```

### `show_stats` {#show-stats}

`show_stats` 设置用于控制是否在每次执行查询后显示查询统计信息。设置为 `false` 时，如下面示例中的第一个查询所示，不会显示查询统计信息。相反，设置为 `true` 时，如第二个查询所示，会在每次执行查询后显示查询统计信息，例如执行时间、读取的行数和处理的字节数。

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set show_stats false
root@localhost:8000/default> select now();
┌────────────────────────────┐
│            now()           │
│          Timestamp         │
├────────────────────────────┤
│ 2024-04-23 23:27:11.538673 │
└────────────────────────────┘
// highlight-next-line
root@localhost:8000/default> !set show_stats true
root@localhost:8000/default> select now();
┌────────────────────────────┐
│            now()           │
│          Timestamp         │
├────────────────────────────┤
│ 2024-04-23 23:49:04.754296 │
└────────────────────────────┘
1 row read in 0.045 sec. Processed 1 row, 1 B (22.26 rows/s, 22 B/s)
```

### `max_display_rows` {#max-display-rows}

`max_display_rows` 设置用于控制查询结果输出中显示的最大行数。在下面的示例中，当其设置为 `5` 时，查询结果中最多只显示 5 行。其余行会以 (5 shown) 标示。

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set max_display_rows 5
root@localhost:8000/default> SELECT * FROM system.configs;
┌──────────────────────────────────────────────────────┐
│   group   │       name       │  value  │ description │
│   String  │      String      │  String │    String   │
├───────────┼──────────────────┼─────────┼─────────────┤
│ query     │ tenant_id        │ default │             │
│ query     │ cluster_id       │ default │             │
│ query     │ num_cpus         │ 0       │             │
│ ·         │ ·                │ ·       │ ·           │
│ ·         │ ·                │ ·       │ ·           │
│ ·         │ ·                │ ·       │ ·           │
│ storage   │ cos.endpoint_url │         │             │
│ storage   │ cos.root         │         │             │
│ 176 rows  │                  │         │             │
│ (5 shown) │                  │         │             │
└──────────────────────────────────────────────────────┘
176 rows read in 0.059 sec. Processed 176 rows, 10.36 KiB (2.98 thousand rows/s, 175.46 KiB/s)
```

### `max_col_width` & `max_width` {#max-col-width-max-width}

设置 `max_col_width` 和 `max_width` 分别用于指定单个列以及整个显示输出允许的最大字符宽度。以下示例将列显示宽度设置为 10 个字符，并将整个显示宽度设置为 100 个字符：

```sql title='Example:'
// highlight-next-line
root@localhost:8000/default> .max_col_width 10
// highlight-next-line
root@localhost:8000/default> .max_width 100
root@localhost:8000/default> select * from system.settings;
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│    name    │  value  │ default │   range  │  level  │            description            │  type  │
│   String   │  String │  String │  String  │  String │               String              │ String │
├────────────┼─────────┼─────────┼──────────┼─────────┼───────────────────────────────────┼────────┤
│ acquire... │ 15      │ 15      │ None     │ DEFAULT │ Sets the maximum timeout in se... │ UInt64 │
│ aggrega... │ 0       │ 0       │ None     │ DEFAULT │ Sets the maximum amount of mem... │ UInt64 │
│ aggrega... │ 0       │ 0       │ [0, 100] │ DEFAULT │ Sets the maximum memory ratio ... │ UInt64 │
│ auto_co... │ 50      │ 50      │ None     │ DEFAULT │ Threshold for triggering auto ... │ UInt64 │
│ collation  │ utf8    │ utf8    │ ["utf8"] │ DEFAULT │ Sets the character collation. ... │ String │
│ ·          │ ·       │ ·       │ ·        │ ·       │ ·                                 │ ·      │
│ ·          │ ·       │ ·       │ ·        │ ·       │ ·                                 │ ·      │
│ ·          │ ·       │ ·       │ ·        │ ·       │ ·                                 │ ·      │
│ storage... │ 1048576 │ 1048576 │ None     │ DEFAULT │ Sets the byte size of the buff... │ UInt64 │
│ table_l... │ 10      │ 10      │ None     │ DEFAULT │ Sets the seconds that the tabl... │ UInt64 │
│ timezone   │ UTC     │ UTC     │ None     │ DEFAULT │ Sets the timezone.                │ String │
│ unquote... │ 0       │ 0       │ None     │ DEFAULT │ Determines whether {{{ .lake }}} tr... │ UInt64 │
│ use_par... │ 0       │ 0       │ [0, 1]   │ DEFAULT │ This setting is deprecated        │ UInt64 │
│ 96 rows    │         │         │          │         │                                   │        │
│ (10 shown) │         │         │          │         │                                   │        │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
96 rows read in 0.040 sec. Processed 96 rows, 16.52 KiB (2.38 thousand rows/s, 410.18 KiB/s)
```

### `output_format` {#output-format}

通过将 `output_format` 设置为 `table`、`csv`、`tsv` 或 `null`，你可以控制查询结果的格式。`table` 格式会以带列标题的表格形式展示结果；`csv` 和 `tsv` 格式则分别提供逗号分隔值和制表符分隔值；`null` 格式则会完全抑制输出格式化。

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set output_format table
root@localhost:8000/default> show users;
┌────────────────────────────────────────────────────────────────────────────┐
│  name  │ hostname │  auth_type  │ is_configured │  default_role │ disabled │
│ String │  String  │    String   │     String    │     String    │  Boolean │
├────────┼──────────┼─────────────┼───────────────┼───────────────┼──────────┤
│ root   │ %        │ no_password │ YES           │ account_admin │ false    │
└────────────────────────────────────────────────────────────────────────────┘
1 row read in 0.032 sec. Processed 1 row, 113 B (31.02 rows/s, 3.42 KiB/s)

// highlight-next-line
root@localhost:8000/default> !set output_format csv
root@localhost:8000/default> show users;
root,%,no_password,YES,account_admin,false
1 row read in 0.062 sec. Processed 1 row, 113 B (16.03 rows/s, 1.77 KiB/s)

// highlight-next-line
root@localhost:8000/default> !set output_format tsv
root@localhost:8000/default> show users;
root % no_password YES account_admin false
1 row read in 0.076 sec. Processed 1 row, 113 B (13.16 rows/s, 1.45 KiB/s)

// highlight-next-line
root@localhost:8000/default> !set output_format null
root@localhost:8000/default> show users;
1 row read in 0.036 sec. Processed 1 row, 113 B (28.1 rows/s, 3.10 KiB/s)
```

### `expand` {#expand}

`expand` 设置用于控制查询输出是显示为单独的记录，还是以表格格式显示。当 `expand` 设置为 `auto` 时，系统会根据查询返回的行数自动决定输出的显示方式。如果查询只返回一行，则输出会显示为单条记录。

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set expand on
root@localhost:8000/default> show users;
-[ RECORD 1 ]-----------------------------------
         name: root
     hostname: %
    auth_type: no_password
is_configured: YES
 default_role: account_admin
     disabled: false

1 row read in 0.055 sec. Processed 1 row, 113 B (18.34 rows/s, 2.02 KiB/s)

// highlight-next-line
root@localhost:8000/default> !set expand off
root@localhost:8000/default> show users;
┌────────────────────────────────────────────────────────────────────────────┐
│  name  │ hostname │  auth_type  │ is_configured │  default_role │ disabled │
│ String │  String  │    String   │     String    │     String    │  Boolean │
├────────┼──────────┼─────────────┼───────────────┼───────────────┼──────────┤
│ root   │ %        │ no_password │ YES           │ account_admin │ false    │
└────────────────────────────────────────────────────────────────────────────┘
1 row read in 0.046 sec. Processed 1 row, 113 B (21.62 rows/s, 2.39 KiB/s)

// highlight-next-line
root@localhost:8000/default> !set expand auto
root@localhost:8000/default> show users;
-[ RECORD 1 ]-----------------------------------
         name: root
     hostname: %
    auth_type: no_password
is_configured: YES
 default_role: account_admin
     disabled: false

1 row read in 0.037 sec. Processed 1 row, 113 B (26.75 rows/s, 2.95 KiB/s)
```

### `multi_line` {#multi-line}

当 `multi_line` 设置为 `true` 时，允许跨多行输入内容。因此，SQL 查询中的每个子句都可以单独占一行，从而提升可读性和条理性。

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set multi_line true;
root@localhost:8000/default> SELECT *
> FROM system.configs;
┌──────────────────────────────────────────────────────┐
│   group   │       name       │  value  │ description │
│   String  │      String      │  String │    String   │
├───────────┼──────────────────┼─────────┼─────────────┤
│ query     │ tenant_id        │ default │             │
│ query     │ cluster_id       │ default │             │
│ query     │ num_cpus         │ 0       │             │
│ ·         │ ·                │ ·       │ ·           │
│ ·         │ ·                │ ·       │ ·           │
│ ·         │ ·                │ ·       │ ·           │
│ storage   │ cos.endpoint_url │         │             │
│ storage   │ cos.root         │         │             │
│ 176 rows  │                  │         │             │
│ (5 shown) │                  │         │             │
└──────────────────────────────────────────────────────┘
176 rows read in 0.060 sec. Processed 176 rows, 10.36 KiB (2.91 thousand rows/s, 171.39 KiB/s)
```

### `replace_newline` {#replace-newline}

`replace_newline` 设置用于确定是否将输出中的换行符 (`\n`) 替换为字面字符串 (`\\n`)。在下面的示例中，`replace_newline` 设置为 `true`。因此，当选择字符串 `'Hello\nWorld'` 时，换行符 (`\n`) 会被替换为字面字符串 (`\\n`)。也就是说，输出不会显示实际的换行，而是将 `'Hello\nWorld'` 显示为 `'Hello\\nWorld'`：

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set replace_newline true
root@localhost:8000/default> SELECT 'Hello\nWorld' AS message;
┌──────────────┐
│    message   │
│    String    │
├──────────────┤
│ Hello\nWorld │
└──────────────┘
1 row read in 0.056 sec. Processed 1 row, 1 B (18 rows/s, 17 B/s)

// highlight-next-line
root@localhost:8000/default> !set replace_newline false;
root@localhost:8000/default> SELECT 'Hello\nWorld' AS message;
┌─────────┐
│ message │
│  String │
├─────────┤
│ Hello   │
│ World   │
└─────────┘
1 row read in 0.067 sec. Processed 1 row, 1 B (14.87 rows/s, 14 B/s)
```

### 配置 LakeSQL 设置 {#configuring-lakesql-settings}

你可以通过以下方式配置 LakeSQL 设置：

- 使用 `!set <setting> <value>` 命令。更多信息，请参见[实用命令](#utility-commands)。

- 在配置文件 `~/.config/lakesql/config.toml` 中添加并配置设置。为此，打开该文件，并在 `[settings]` 部分下添加你的设置。以下示例将 `max_display_rows` 设置为 10，并将 `max_width` 设置为 100：

```toml title='Example:'
...
[settings]
max_display_rows = 10
max_width = 100
...
```

- 在运行时配置设置：启动 LakeSQL 后，使用 `.<setting> <value>` 格式指定设置。请注意，以这种方式配置的设置仅在当前会话中生效。

```shell title='Example:'
root@localhost:8000/default> .max_display_rows 10
root@localhost:8000/default> .max_width 100
```

## Utility Commands {#utility-commands}

LakeSQL 提供了多种命令，帮助用户简化工作流程并自定义使用体验。以下是 LakeSQL 中可用命令的概览：

| 命令                  | 描述                  |
| ------------------------ | ---------------------------- |
| `!exit`                  | 退出 LakeSQL。               |
| `!quit`                  | 退出 LakeSQL。               |
| `!configs`               | 显示当前的 LakeSQL 设置。    |
| `!set <setting> <value>` | 修改 LakeSQL 设置。          |
| `!source <sql_file>`     | 执行 SQL 文件。              |

有关各个命令的示例，请参见以下参考信息：

### `!exit` {#exit}

断开与 {{{ .lake }}} 的连接并退出 LakeSQL。

```shell title='Example:'
➜  ~ lakesql
Welcome to LakeSQL 0.17.0-homebrew.
Connecting to localhost:8000 as user root.
Connected to {{{ .lake }}} Query v1.2.427-nightly-b1b622d406(rust-1.77.0-nightly-2024-04-20T22:12:35.318382488Z)

// highlight-next-line
root@localhost:8000/default> !exit
Bye~
```

### `!quit` {#quit}

断开与 {{{ .lake }}} 的连接并退出 LakeSQL。

```shell title='Example:'
➜  ~ lakesql
Welcome to LakeSQL 0.17.0-homebrew.
Connecting to localhost:8000 as user root.
Connected to {{{ .lake }}} Query v1.2.427-nightly-b1b622d406(rust-1.77.0-nightly-2024-04-20T22:12:35.318382488Z)

// highlight-next-line
root@localhost:8000/default> !quit
Bye~
➜  ~
```

### `!configs` {#configs}

显示当前的 LakeSQL 设置。

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !configs
Settings {
    display_pretty_sql: true,
    prompt: "{user}@{warehouse}/{database}> ",
    progress_color: "cyan",
    show_progress: true,
    show_stats: true,
    max_display_rows: 40,
    max_col_width: 1048576,
    max_width: 1048576,
    output_format: Table,
    quote_style: Necessary,
    expand: Off,
    time: None,
    multi_line: true,
    replace_newline: true,
}
```

### `!set <setting> <value>` {#set}

修改 LakeSQL 设置。

```shell title='Example:'
root@localhost:8000/default> !set display_pretty_sql false
```

### `!source <sql_file>` {#source}

执行 SQL 文件。

```shell title='Example:'
➜  ~ more ./desktop/test.sql
CREATE TABLE test_table (
    id INT,
    name VARCHAR(50)
);

INSERT INTO test_table (id, name) VALUES (1, 'Alice');
INSERT INTO test_table (id, name) VALUES (2, 'Bob');
INSERT INTO test_table (id, name) VALUES (3, 'Charlie');
➜  ~ lakesql
Welcome to LakeSQL 0.17.0-homebrew.
Connecting to localhost:8000 as user root.
Connected to {{{ .lake }}} Query v1.2.427-nightly-b1b622d406(rust-1.77.0-nightly-2024-04-20T22:12:35.318382488Z)

// highlight-next-line
root@localhost:8000/default> !source ./desktop/test.sql
root@localhost:8000/default> SELECT * FROM test_table;

SELECT
  *
FROM
  test_table

┌────────────────────────────────────┐
│        id       │       name       │
│ Nullable(Int32) │ Nullable(String) │
├─────────────────┼──────────────────┤
│               1 │ Alice            │
│               2 │ Bob              │
│               3 │ Charlie          │
└────────────────────────────────────┘
3 rows read in 0.064 sec. Processed 3 rows, 81 B (46.79 rows/s, 1.23 KiB/s)
```
