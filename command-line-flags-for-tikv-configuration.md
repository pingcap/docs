---
title: TiKV Configuration Flags
summary: Learn some configuration flags of TiKV.
---

# TiKVコンフィグレーションフラグ {#tikv-configuration-flags}

TiKV は、コマンド ライン パラメーターの読み取り可能な単位変換をサポートしています。

-   ファイル サイズ (バイト単位): KB、MB、GB、TB、PB (または小文字)
-   時間 (ms に基づく): ms、s、m、h

## <code>-A, --addr</code> {#code-a-addr-code}

-   TiKVサーバーが監視するアドレス
-   デフォルト: `"127.0.0.1:20160"`
-   クラスターをデプロイするには、 `--addr`を使用して現在のホストの IP アドレス ( `"192.168.100.113:20160"`など) を指定する必要があります。クラスターが Docker で実行されている場合は、Docker の IP アドレスを`"0.0.0.0:20160"`として指定します。

## <code>--advertise-addr</code> {#code-advertise-addr-code}

-   外部からのクライアント トラフィックのサーバーアドバタイズ アドレス
-   デフォルト: `${addr}`
-   Docker または NAT ネットワークが原因で、クライアントが`--addr`アドレスを介して TiKV に接続できない場合は、手動で`--advertise-addr`アドレスを設定する必要があります。
-   たとえば、Docker の内部 IP アドレスは 172.17.0.1 ですが、ホストの IP アドレスは 192.168.100.113 で、ポート マッピングは`-p 20160:20160`に設定されています。この場合、 `--advertise-addr` 「192.168.100.113:20160」に設定できます。クライアントは、192.168.100.113:20160 でこのサービスを見つけることができます。

## <code>--status-addr</code> {#code-status-addr-code}

-   TiKV サービスのステータスをリッスンするポート
-   デフォルト: `"20180"`
-   Prometheus は`http://host:status_port/metrics`経由でこのステータス情報にアクセスできます。
-   プロファイルは、 `http://host:status_port/debug/pprof/profile`を介してこのステータス情報にアクセスできます。

## <code>--advertise-status-addr</code> {#code-advertise-status-addr-code}

-   TiKVが外部からサービスステータスにアクセスするためのアドレス。
-   デフォルト: 値`--status-addr`が使用されます。
-   Docker または NAT ネットワークが原因で、クライアントが`--status-addr`アドレスを介して TiKV に接続できない場合は、手動で`--advertise-status-addr`アドレスを設定する必要があります。
-   たとえば、Docker の内部 IP アドレスは`172.17.0.1`ですが、ホストの IP アドレスは`192.168.100.113`で、ポート マッピングは`-p 20180:20180`に設定されています。この場合は`--advertise-status-addr="192.168.100.113:20180"`を設定します。クライアントは`192.168.100.113:20180`でこのサービスを見つけることができます。

## <code>-C, --config</code> {#code-c-config-code}

-   設定ファイル
-   デフォルト: `""`
-   コマンド ラインを使用して構成を設定すると、構成ファイル内の同じ設定が上書きされます。

## <code>--capacity</code> {#code-capacity-code}

-   店舗のキャパシティ
-   デフォルト: `0` (無制限)
-   PD はこのフラグを使用して、TiKV サーバーのバランスをとる方法を決定します。 (ヒント: 1073741824 の代わりに 10GB を使用できます)

## <code>--config-info &#x3C;FORMAT></code> {#code-config-info-x3c-format-code}

-   このフラグを使用すると、使用可能な構成値が`FORMAT`に従って一覧表示され、終了します。
-   `FORMAT` : `json`の値オプション。現在、JSON 形式のみがサポートされています。
-   出力 JSON には、構成名 (Name)、デフォルト値 (DefaultValue)、および現在の値 (ValueInFile) のみがリストされます。 `-C`または`--config`を指定すると、ファイル内の構成項目の現在の値とデフォルト値が一緒にリストされ、 `-C`または`--config`が指定されていないその他の項目はデフォルト値のみになります。次に例を示します。

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

-   データ ディレクトリへのパス
-   デフォルト: `"/tmp/tikv/store"`

## <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト: `"info"`
-   オプションの値: `"debug"` 、 `"info"` 、 `"warn"` 、 `"error"` 、 `"fatal"`

## <code>--log-file</code> {#code-log-file-code}

-   ログファイル
-   デフォルト: `""`
-   このフラグが設定されていない場合、ログは「stderr」に書き込まれます。このフラグが設定されている場合、ログは対応するファイルに出力されます。

## <code>--pd</code> {#code-pd-code}

-   PD サーバーのアドレス一覧
-   デフォルト: `""`
-   TiKV を機能させるには、値`--pd`を使用して TiKVサーバーをPDサーバーに接続する必要があります。複数の PD アドレスは、「192.168.100.113:2379, 192.168.100.114:2379, 192.168.100.115:2379」のようにカンマで区切ります。
