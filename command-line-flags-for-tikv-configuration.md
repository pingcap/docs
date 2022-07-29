---
title: TiKV Configuration Flags
summary: Learn some configuration flags of TiKV.
---

# TiKVConfiguration / コンフィグレーションフラグ {#tikv-configuration-flags}

TiKVは、コマンドラインパラメーターの読み取り可能な単位変換をサポートしています。

-   ファイルサイズ（バイトに基づく）：KB、MB、GB、TB、PB（または小文字）
-   時間（msに基づく）：ms、s、m、h

## <code>-A, --addr</code> {#code-a-addr-code}

-   TiKVサーバーが監視するアドレス
-   デフォルト： `"127.0.0.1:20160"`
-   クラスタをデプロイするには、 `--addr`を使用して現在のホストのIPアドレス（ `"192.168.100.113:20160"`など）を指定する必要があります。クラスタがDockerで実行されている場合は、DockerのIPアドレスを`"0.0.0.0:20160"`として指定します。

## <code>--advertise-addr</code> {#code-advertise-addr-code}

-   サーバーは外部からのクライアントトラフィックのアドレスをアドバタイズします
-   デフォルト： `${addr}`
-   DockerまたはNATネットワークが原因でクライアントが`--addr`アドレスを介してTiKVに接続できない場合は、 `--advertise-addr`アドレスを手動で設定する必要があります。
-   たとえば、Dockerの内部IPアドレスは172.17.0.1ですが、ホストのIPアドレスは192.168.100.113で、ポートマッピングは`-p 20160:20160`に設定されています。この場合、 `--advertise-addr`を「192.168.100.113:20160」に設定できます。クライアントは、192.168.100.113：20160を介してこのサービスを見つけることができます。

## <code>--status-addr</code> {#code-status-addr-code}

-   TiKVサービスステータスがリッスンされるポート
-   デフォルト： `"20180"`
-   Prometheusは、 `http://host:status_port/metrics`を介してこのステータス情報にアクセスできます。
-   プロファイルは、 `http://host:status_port/debug/pprof/profile`を介してこのステータス情報にアクセスできます。

## <code>--advertise-status-addr</code> {#code-advertise-status-addr-code}

-   TiKVが外部からサービスステータスにアクセスするために使用するアドレス。
-   デフォルト：値`--status-addr`が使用されます。
-   DockerまたはNATネットワークが原因でクライアントが`--status-addr`アドレスを介してTiKVに接続できない場合は、 `--advertise-status-addr`アドレスを手動で設定する必要があります。
-   たとえば、Dockerの内部IPアドレスは`172.17.0.1`ですが、ホストのIPアドレスは`192.168.100.113`で、ポートマッピングは`-p 20180:20180`に設定されています。この場合、 `--advertise-status-addr="192.168.100.113:20180"`を設定します。クライアントは`192.168.100.113:20180`までこのサービスを見つけることができます。

## <code>-C, --config</code> {#code-c-config-code}

-   設定ファイル
-   デフォルト： `""`
-   コマンドラインを使用して構成を設定すると、構成ファイルの同じ設定が上書きされます。

## <code>--capacity</code> {#code-capacity-code}

-   店舗容量
-   デフォルト： `0` （無制限）
-   PDはこのフラグを使用して、TiKVサーバーのバランスをとる方法を決定します。 （ヒント：1073741824の代わりに10GBを使用できます）

## <code>--data-dir</code> {#code-data-dir-code}

-   データディレクトリへのパス
-   デフォルト： `"/tmp/tikv/store"`

## <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト： `"info"`
-   `"error"` `"fatal"` `"warn"` `"debug"` `"info"`

## <code>--log-file</code> {#code-log-file-code}

-   ログファイル
-   デフォルト： `""`
-   このフラグが設定されていない場合、ログは「stderr」に書き込まれます。このフラグが設定されている場合、ログは対応するファイルに出力されます。

## <code>--pd</code> {#code-pd-code}

-   PDサーバーのアドレスリスト
-   デフォルト： `""`
-   TiKVを機能させるには、値`--pd`を使用してTiKVサーバーをPDサーバーに接続する必要があります。複数のPDアドレスは、「192.168.100.113:2379、192.168.100.114:2379,192.168.100.115:2379」のようにカンマで区切ります。
