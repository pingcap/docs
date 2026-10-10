---
title: LakeSQL を使用して TiDB Cloud Lake に接続する
summary: LakeSQL は {{{ .lake }}} 向けに特別に設計されたコマンドラインツールです。これを使用すると、ユーザーは {{{ .lake }}} への接続を確立し、CLI ウィンドウから直接クエリを実行できます。
---

# LakeSQL を使用して TiDB Cloud Lake に接続する

[LakeSQL](https://github.com/tidbcloud/lakesql) は {{{ .lake }}} 向けに特別に設計されたコマンドラインツールです。これを使用すると、ユーザーは {{{ .lake }}} への接続を確立し、CLI ウィンドウから直接クエリを実行できます。

LakeSQL は、コマンドラインインターフェイスを好み、日常的に {{{ .lake }}} を利用するユーザーに特に便利です。LakeSQL を使用すると、データベース、テーブル、データを簡単かつ効率的に管理でき、さまざまなクエリや操作を容易に実行できます。

## LakeSQL のインストール {#installing-lakesql}

LakeSQL には、さまざまなプラットフォームや好みに対応する複数のインストール方法があります。以下のセクションから希望する方法を選択するか、[LakeSQL release page](https://github.com/tidbcloud/lakesql/releases) からインストールパッケージをダウンロードして手動でインストールしてください。

### Shell Script {#shell-script}

LakeSQL では、便利な Shell script によるインストール方法を提供しています。次の 2 つのオプションから選択できます。

#### Default Installation {#default-installation}

ユーザーのホームディレクトリ (`~/.lakesql`) に LakeSQL をインストールします。

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

#### `--prefix` を使用したカスタムインストール {#custom-installation-with-prefix}

指定したディレクトリ (例: `/usr/local`) に LakeSQL をインストールします。

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

### Homebrew (macOS 向け) {#homebrew-for-macos}

macOS では、次の簡単なコマンドを使用して Homebrew で LakeSQL を簡単にインストールできます。

```bash
brew install tidbcloud/homebrew-tap/lakesql
```

### Apt (Ubuntu/Debian 向け) {#apt-for-ubuntu-debian}

Ubuntu および Debian システムでは、Apt パッケージマネージャーを使用して LakeSQL をインストールできます。

```bash
curl -fsSL https://lakesql-bin.tidbcloud.com/keys/lakesql-archive-keyring.gpg \
  | sudo tee /usr/share/keyrings/lakesql-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/lakesql-archive-keyring.gpg] https://lakesql-bin.tidbcloud.com/apt stable main" \
  | sudo tee /etc/apt/sources.list.d/lakesql.list >/dev/null
sudo apt-get update
sudo apt-get install -y lakesql
```

### Cargo (Rust パッケージマネージャー) {#cargo-rust-package-manager}

Cargo を使用して LakeSQL をインストールするには、`cargo-binstall` ツールを利用するか、提供されているコマンドを使用してソースからビルドします。

> **Note:**
>
> Cargo でインストールする前に、完全な Rust ツールチェーンと `cargo` コマンドがコンピュータにインストールされていることを確認してください。インストールされていない場合は、[https://rustup.rs/](https://rustup.rs/) のインストールガイドに従ってください。

**cargo-binstall を使用する**

`cargo-binstall` をインストールし、`cargo binstall <crate-name>` サブコマンドを有効にするには、[Cargo B(inary)Install - Installation](https://github.com/cargo-bins/cargo-binstall#installation) を参照してください。

```bash
cargo binstall lakesql
```

**ソースからビルドする**

ソースからビルドする場合、一部の依存関係では C/C++ コードのコンパイルが必要になることがあります。GCC/G++ または Clang ツールチェーンがコンピュータにインストールされていることを確認してください。

```bash
cargo install lakesql
```

## ユーザー認証 {#user-authentication}

{{{ .lake }}} への接続には、デフォルトの `cloudapp` ユーザー、または [CREATE USER](/tidb-cloud-lake/sql/create-user.md) コマンドで作成した SQL ユーザーを使用できます。[{{{ .lake }}} console](https://app.lake.tidbcloud.com) へのログインに使用するユーザーアカウントは、{{{ .lake }}} への接続には使用できないことに注意してください。

## LakeSQL で接続する {#connecting-with-lakesql}

LakeSQL を使用すると、両方の {{{ .lake }}} インスタンスに接続できます。

### DSN を使用して接続をカスタマイズする {#customize-connections-with-a-dsn}

DSN (Data Source Name) は、単一の URI 形式の文字列を使用して、LakeSQL で {{{ .lake }}} への接続を設定および管理するための、シンプルでありながら強力な方法です。この方法では、認証情報や接続設定を環境に直接埋め込むことができるため、接続プロセスを簡素化できます。

#### DSN の形式とパラメータ {#dsn-format-and-parameters}

```bash title='DSN Format'
lake[+flight]://user[:password]@host[:port]/[database][?sslmode=disable][&arg1=value1]
```

| 一般的な DSN パラメータ | 説明                                 |
|-----------------------|--------------------------------------|
| `tenant`              | Tenant ID。{{{ .lake }}} のみ。      |
| `warehouse`           | Warehouse 名。{{{ .lake }}} のみ。   |
| `sslmode`             | TLS を使用しない場合は `disable` に設定します。 |
| `tls_ca_file`         | カスタム root CA 証明書のパス。      |
| `connect_timeout`     | 接続タイムアウト (秒)。              |

| RestAPI クライアントパラメータ | 説明                                                                                                                   |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `wait_time_secs`            | ページのリクエスト待機時間。デフォルトは `1`。                                                                                   |
| `max_rows_in_buffer`        | ページバッファ内の最大行数。                                                                                                 |
| `max_rows_per_page`         | 1 ページあたりのレスポンスの最大行数。                                                                                      |
| `page_request_timeout_secs` | 1 回のページリクエストのタイムアウト。デフォルトは `30`。                                                                           |
| `presign`                   | データロード用の presign を有効にします。オプション: `auto`, `detect`, `on`, `off`。デフォルトは `auto` ({{{ .lake }}} でのみ有効)。 |

| FlightSQL クライアントパラメータ | 説明                                                          |
|-----------------------------|----------------------------------------------------------------------|
| `query_timeout`             | クエリタイムアウト (秒)。                                            |
| `tcp_nodelay`               | デフォルトは `true`。                                                  |
| `tcp_keepalive`             | TCP keepalive (秒) (デフォルトは `3600`、無効にするには `0` を設定)。 |
| `http2_keep_alive_interval` | keep-alive 間隔 (秒)。デフォルトは `300`。                    |
| `keep_alive_timeout`        | keep-alive タイムアウト (秒)。デフォルトは `20`。                      |
| `keep_alive_while_idle`     | デフォルトは `true`。                                                  |

#### DSN の例 {#dsn-examples}

```bash
# Local connection using HTTP API with presign detection
lake://root:@localhost:8000/?sslmode=disable&presign=detect

# {{{ .lake }}} connection with tenant and warehouse info
lake://user1:password1@tnxxxx--default.gw.aws-us-east-2.default.tidbcloud.com:443/benchmark?enable_dphyp=1

# Local connection using FlightSQL API
lake+flight://root:@localhost:8900/database1?connect_timeout=10
```

### {{{ .lake }}} への接続 {#connect-to-lake}

{{{ .lake }}} に接続するベストプラクティスは、{{{ .lake }}} から DSN を取得し、それを環境変数として export することです。DSN を取得するには、次の手順を実行します。

1. {{{ .lake }}} にログインし、**Overview** ページで **Connect** をクリックします。

2. 接続したいデータベースと Warehouse を選択します。

3. **Examples** セクションで DSN が自動的に生成されます。DSN の下には、DSN を `LAKESQL_DSN` という名前の環境変数として export し、正しい設定で LakeSQL を起動する LakeSQL スニペットがあります。これをそのままターミナルにコピー＆ペーストできます。

    ```bash title='Example'
    export LAKESQL_DSN="lake://cloudapp:******@tn3ftqihs.gw.aws-us-east-2.default.tidbcloud.com:443/information_schema?warehouse=small-xy2t"
    lakesql
    ```

## LakeSQL の設定 {#lakesql-settings}

LakeSQL には、クエリ結果の表示方法を定義できるさまざまな設定があります。

| 設定 | 説明 |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `display_pretty_sql` | `true` に設定すると、SQL クエリが見やすい形式で整形され、読みやすく理解しやすくなります。 |
| `prompt`             | コマンドラインインターフェースに表示されるプロンプトです。通常は、アクセス中のユーザー、Warehouse、データベースを示します。 |
| `progress_color`     | 進行状況インジケーターに使用する色を指定します。たとえば、完了までに時間がかかるクエリの実行時に使用されます。 |
| `show_progress`      | `true` に設定すると、長時間実行されるクエリや操作の進行状況を示すインジケーターが表示されます。 |
| `show_stats`         | `true` の場合、各クエリの実行後に、実行時間、読み取った行数、処理したバイト数などのクエリ統計情報が表示されます。 |
| `max_display_rows`   | クエリ結果の出力に表示される最大行数を設定します。 |
| `max_col_width`      | 各カラムの表示レンダリングにおける最大文字幅を設定します。3 未満の値を指定すると、この制限は無効になります。 |
| `max_width`          | 表示出力全体の最大文字幅を設定します。値を `0` にすると、デフォルトでターミナルウィンドウの幅が使用されます。 |
| `output_format`      | クエリ結果の表示形式を設定します（`table`, `csv`, `tsv`, `null`）。 |
| `expand`             | クエリの出力を個別レコードとして表示するか、表形式で表示するかを制御します。使用可能な値は `on`、`off`、`auto` です。 |
| `multi_line`         | SQL クエリで複数行入力を許可するかどうかを決定します。`true` に設定すると、可読性向上のためにクエリを複数行にまたがって記述できます。 |
| `replace_newline`    | クエリ結果の出力内の改行文字をスペースに置き換えるかどうかを指定します。これにより、表示時の意図しない改行を防ぐことができます。 |

各設定の詳細については、以下のリファレンス情報を参照してください。

### `display_pretty_sql` {#display-pretty-sql}

`display_pretty_sql` 設定は、SQL クエリを視覚的に整形して表示するかどうかを制御します。以下の最初のクエリのように `false` に設定すると、SQL クエリは見やすい形式に整形されません。一方、2 番目のクエリのように `true` に設定すると、SQL クエリが見やすい形式で整形され、読みやすく理解しやすくなります。

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

`prompt` 設定は、コマンドラインインターフェースのプロンプト形式を制御します。以下の例では、最初はユーザーと Warehouse（`{user}@{warehouse}`）を表示するように設定されています。これを `{user}@{warehouse}/{database}` に更新すると、プロンプトにユーザー、Warehouse、データベースが含まれるようになります。

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

`progress_color` 設定は、クエリ実行中の進行状況インジケーターに使用する色を制御します。この例では、色が `blue` に設定されています。

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set progress_color blue
```

### `show_progress` {#show-progress}

`true` に設定すると、クエリの実行中に進行状況情報が表示されます。進行状況情報には、処理済みの行数、クエリ内の総行数、1 秒あたりの処理行数、処理済みメモリ量、および 1 秒あたりのメモリ処理速度が含まれます。

```shell title='Example:'
// highlight-next-line
root@localhost:8000/default> !set show_progress true
root@localhost:8000/default> select * from numbers(1000000000000000);
⠁ [00:00:08] Processing 18.02 million/1 quadrillion (2.21 million rows/s), 137.50 MiB/7.11 PiB (16.88 MiB/s) ░
```

### `show_stats` {#show-stats}

`show_stats` 設定は、各クエリの実行後にクエリ統計情報を表示するかどうかを制御します。以下の例の最初のクエリのように `false` に設定すると、クエリ統計情報は表示されません。一方、2 番目のクエリのように `true` に設定すると、各クエリの実行後に、実行時間、読み取った行数、処理したバイト数などのクエリ統計情報が表示されます。

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

`max_display_rows` 設定は、クエリ結果の出力に表示される最大行数を制御します。以下の例では `5` に設定されているため、クエリ結果には最大 5 行のみが表示されます。残りの行は (5 shown) として示されます。

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

`max_col_width` と `max_width` の設定は、それぞれ個々のカラムおよび表示出力全体に対して、文字数ベースで許可される最大幅を指定します。次の例では、カラムの表示幅を 10 文字、表示全体の幅を 100 文字に設定しています。

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

`output_format` を `table`、`csv`、`tsv`、または `null` に設定することで、クエリ結果の形式を制御できます。`table` 形式では、カラムヘッダー付きの表形式で結果を表示します。`csv` と `tsv` 形式では、それぞれカンマ区切り値とタブ区切り値で出力されます。`null` 形式では、出力の整形を行いません。

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

`expand` 設定は、クエリの出力を個別レコード形式で表示するか、表形式で表示するかを制御します。`expand` を `auto` に設定すると、クエリが返す行数に応じて、システムが出力方法を自動的に決定します。クエリが 1 行だけを返す場合、出力は単一レコードとして表示されます。

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

`multi_line` を `true` に設定すると、入力を複数行にまたがって入力できるようになります。その結果、SQL クエリの各句を別々の行に記述できるため、可読性と整理しやすさが向上します。

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

`replace_newline` 設定は、出力内の改行文字 (`\n`) をリテラル文字列 (`\\n`) に置き換えるかどうかを決定します。次の例では、`replace_newline` を `true` に設定しています。その結果、文字列 `'Hello\nWorld'` を選択すると、改行文字 (`\n`) はリテラル文字列 (`\\n`) に置き換えられます。つまり、改行文字をそのまま表示する代わりに、出力には `'Hello\nWorld'` が `'Hello\\nWorld'` として表示されます。

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

### LakeSQL 設定の構成 {#configuring-lakesql-settings}

LakeSQL の設定を構成するには、次の方法があります。

- `!set <setting> <value>` コマンドを使用します。詳細は、[Utility Commands](#utility-commands) を参照してください。

- 設定ファイル `~/.config/lakesql/config.toml` に設定を追加して構成します。これを行うには、ファイルを開き、`[settings]` セクションの下に設定を追加します。次の例では、`max_display_rows` を 10、`max_width` を 100 に設定しています。

```toml title='Example:'
...
[settings]
max_display_rows = 10
max_width = 100
...
```

- LakeSQL を起動した後、`.<setting> <value>` 形式で設定を指定して、実行時に設定します。この方法で構成した設定は、現在のセッションでのみ有効になる点に注意してください。

```shell title='Example:'
root@localhost:8000/default> .max_display_rows 10
root@localhost:8000/default> .max_width 100
```

## Utility Commands {#utility-commands}

LakeSQL には、ワークフローを効率化し、利用体験をカスタマイズするためのさまざまなコマンドが用意されています。以下は、LakeSQL で使用できるコマンドの概要です。

| Command                  | 説明 |
| ------------------------ | ---------------------------------- |
| `!exit`                  | LakeSQL を終了します。                     |
| `!quit`                  | LakeSQL を終了します。                     |
| `!configs`               | 現在の LakeSQL 設定を表示します。 |
| `!set <setting> <value>` | LakeSQL の設定を変更します。        |
| `!source <sql_file>`     | SQL ファイルを実行します。               |

各コマンドの例については、以下のリファレンス情報を参照してください。

### `!exit` {#exit}

{{{ .lake }}} から切断し、LakeSQL を終了します。

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

{{{ .lake }}} から切断し、LakeSQL を終了します。

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

現在の LakeSQL 設定を表示します。

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

LakeSQL の設定を変更します。

```shell title='Example:'
root@localhost:8000/default> !set display_pretty_sql false
```

### `!source <sql_file>` {#source}

SQL ファイルを実行します。

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