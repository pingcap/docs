---
title: TiKV Configuration Flags
summary: TiKV のいくつかの構成フラグについて学習します。
---

# TiKVコンフィグレーションフラグ {#tikv-configuration-flags}

TiKV は、コマンドライン パラメータのいくつかの読み取り可能な単位変換をサポートしています。

-   ファイルサイズ（バイト単位）: KB、MB、GB、TB、PB（または小文字）
-   時間（ミリ秒単位）: ms、s、m、h

## <code>-A, --addr</code> {#code-a-addr-code}

-   TiKVサーバーが監視するアドレス
-   デフォルト: `"127.0.0.1:20160"`
-   クラスターをデプロイするには、 `--addr`使用して現在のホストの IP アドレス ( `"192.168.100.113:20160"`など) を指定する必要があります。クラスターが Docker 上で実行される場合は、Docker の IP アドレスを`"0.0.0.0:20160"`として指定します。

## <code>--advertise-addr</code> {#code-advertise-addr-code}

-   サーバーは外部からのクライアントトラフィックのアドレスをアドバタイズします
-   デフォルト: `${addr}`
-   Docker または NAT ネットワークが原因でクライアントが`--addr`のアドレス経由で TiKV に接続できない場合は、 `--advertise-addr`アドレスを手動で設定する必要があります。
-   たとえば、Docker の内部 IP アドレスは 172.17.0.1 ですが、ホストの IP アドレスは 192.168.100.113 で、ポート マッピングは`-p 20160:20160`に設定されています。この場合、 `--advertise-addr` 「192.168.100.113:20160」に設定できます。クライアントは 192.168.100.113:20160 を通じてこのサービスを見つけることができます。

## <code>--status-addr</code> {#code-status-addr-code}

-   TiKV サービスのステータスをリッスンするポート
-   デフォルト: `"20180"`
-   Prometheus は`http://host:status_port/metrics`介してこのステータス情報にアクセスできます。
-   プロファイルは`http://host:status_port/debug/pprof/profile`を介してこのステータス情報にアクセスできます。

## <code>--advertise-status-addr</code> {#code-advertise-status-addr-code}

-   TiKV が外部からサービス ステータスにアクセスするためのアドレス。
-   デフォルト: 値`--status-addr`が使用されます。
-   Docker または NAT ネットワークが原因でクライアントが`--status-addr`のアドレス経由で TiKV に接続できない場合は、 `--advertise-status-addr`アドレスを手動で設定する必要があります。
-   たとえば、Docker の内部 IP アドレスは`172.17.0.1`ですが、ホストの IP アドレスは`192.168.100.113`で、ポート マッピングは`-p 20180:20180`に設定されています。この場合は`--advertise-status-addr="192.168.100.113:20180"`設定します。クライアントは`192.168.100.113:20180`を通じてこのサービスを見つけることができます。

## <code>-C, --config</code> {#code-c-config-code}

-   設定ファイル
-   デフォルト: `""`
-   コマンドラインを使用して設定を行うと、設定ファイル内の同じ設定が上書きされます。

## <code>--capacity</code> {#code-capacity-code}

-   店舗収容人数
-   デフォルト: `0` (無制限)
-   PD はこのフラグを使用して、TiKV サーバーのバランスをとる方法を決定します。(ヒント: 1073741824 の代わりに 10 GB を使用できます)

## <code>--config-info &#x3C;FORMAT></code> {#code-config-info-x3c-format-code}

-   このフラグを使用すると、使用可能な設定値が`FORMAT`に従ってリストされ、終了します。
-   `FORMAT`の値オプション: `json` 。現在は JSON 形式のみがサポートされています。
-   出力 JSON には、設定名 (Name)、デフォルト値 (DefaultValue)、現在の値 (ValueInFile) のみが記載されます`-C`または`--config`が指定されている場合は、ファイル内の設定項目の現在の値とデフォルト値が一緒に記載され、 `-C`または`--config`指定されていないその他の項目にはデフォルト値のみが含まれます。次に例を示します。

    ```json
    {
    "Component": "TiKV Server",
    "Version": "6.2.0",
    "Parameters": [
        {
        "Name": "log-level",
        "DefaultValue": "info",
        "ValueInFile": "warn"
        },
        {
        "Name": "log-file",
        "DefaultValue": ""
        },
        ...
    ]
    }
    ```

## <code>--data-dir</code> {#code-data-dir-code}

-   データディレクトリへのパス
-   デフォルト: `"/tmp/tikv/store"`

## <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト: `"info"`
-   `"error"` `"fatal"` `"warn"` `"debug"` `"info"`

## <code>--log-file</code> {#code-log-file-code}

-   ログファイル
-   デフォルト: `""`
-   このフラグが設定されていない場合、ログは「stderr」に書き込まれます。このフラグが設定されている場合、ログは対応するファイルに出力されます。

## <code>--pd</code> {#code-pd-code}

-   PDサーバーのアドレスリスト
-   デフォルト: `""`
-   TiKV を動作させるには、値`--pd`を使用して TiKVサーバーをPDサーバーに接続する必要があります。複数の PD アドレスは、たとえば「192.168.100.113:2379、192.168.100.114:2379、192.168.100.115:2379」のように、コンマで区切ります。
