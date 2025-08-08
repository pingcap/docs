---
title: PD Configuration Flags
summary: PD のいくつかの構成フラグについて学習します。
---

# PDコンフィグレーションフラグ {#pd-configuration-flags}

PD は、コマンドラインフラグと環境変数を使用して構成できます。

## <code>--advertise-client-urls</code> {#code-advertise-client-urls-code}

-   クライアントがPDにアクセスするためのアドバタイズURLのリスト
-   デフォルト: `"${client-urls}"`
-   Docker または NAT ネットワーク環境などの状況では、クライアントが PD がリッスンするデフォルトのクライアント URL を通じて PD にアクセスできない場合は、アドバタイズ クライアント URL を手動で設定する必要があります。
-   例えば、Dockerの内部IPアドレスは`172.17.0.1` 、ホストのIPアドレスは`192.168.100.113` 、ポートマッピングは`-p 2379:2379`に設定されています。この場合、 `--advertise-client-urls`を`"http://192.168.100.113:2379"`に設定できます。クライアントは`"http://192.168.100.113:2379"`を通じてこのサービスを見つけられます。

## <code>--advertise-peer-urls</code> {#code-advertise-peer-urls-code}

-   他のPDノード（ピア）がPDノードにアクセスするためのアドバタイズURLのリスト
-   デフォルト: `"${peer-urls}"`
-   Docker または NAT ネットワーク環境などの状況では、他のノード (ピア) がこの PD ノードによってリッスンされるデフォルトのピア URL を介して PD ノードにアクセスできない場合は、アドバタイズ ピア URL を手動で設定する必要があります。
-   例えば、Dockerの内部IPアドレスが`172.17.0.1`で、ホストのIPアドレスが`192.168.100.113` 、ポートマッピングが`-p 2380:2380`に設定されている場合、 `--advertise-peer-urls`を`"http://192.168.100.113:2380"`に設定できます。他のPDノードは`"http://192.168.100.113:2380"`を介してこのサービスを検出できます。

## <code>--client-urls</code> {#code-client-urls-code}

-   PDがリッスンするクライアントURLのリスト
-   デフォルト: `"http://127.0.0.1:2379"`
-   クラスターをデプロイする際は、現在のホストのIPアドレスを`--client-urls` （例： `"http://192.168.100.113:2379"` ）に指定する必要があります。クラスターをDocker上で実行する場合は、DockerのIPアドレスを`"http://0.0.0.0:2379"`に指定してください。

## <code>--peer-urls</code> {#code-peer-urls-code}

-   PDノードがリッスンするピアURLのリスト
-   デフォルト: `"http://127.0.0.1:2380"`
-   クラスターをデプロイする際は、現在のホストのIPアドレスを`--peer-urls` （例： `"http://192.168.100.113:2380"`に指定する必要があります。クラスターがDocker上で実行される場合は、DockerのIPアドレスを`"http://0.0.0.0:2380"`に指定してください。

## <code>--config</code> {#code-config-code}

-   設定ファイル
-   デフォルト: `""`
-   コマンドラインを使用して設定を行った場合、設定ファイル内の同じ設定が上書きされます。

## <code>--data-dir</code> {#code-data-dir-code}

-   データディレクトリへのパス
-   デフォルト: `"default.${name}"`

## <code>--initial-cluster</code> {#code-initial-cluster-code}

-   ブートストラップのための初期クラスタ構成
-   デフォルト: `"{name}=http://{advertise-peer-url}"`
-   たとえば、 `name`が「pd」、 `advertise-peer-urls`が`"http://192.168.100.113:2380"`の場合、 `initial-cluster`は`"pd=http://192.168.100.113:2380"`なります。
-   3 つの PD サーバーを起動する必要がある場合、 `initial-cluster`は次のようになります。

        pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380

## <code>--join</code> {#code-join-code}

-   クラスターに動的に参加する
-   デフォルト: `""`
-   既存のクラスターに参加する場合は、 `--join="${advertise-client-urls}"`使用できます。 `advertise-client-url`既存の PD のいずれかで、複数のアドバタイズ クライアント URL はコンマで区切られます。

## <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト: `"info"`
-   `"warn"` `"fatal"` `"error"` `"debug"` `"info"`

## <code>--log-file</code> {#code-log-file-code}

-   ログファイル
-   デフォルト: `""`
-   このフラグが設定されていない場合、ログは「stderr」に書き込まれます。このフラグが設定されている場合、ログは対応するファイルに出力されます。

## <code>--log-rotate</code> {#code-log-rotate-code}

-   ログローテーションを有効または無効にするには
-   デフォルト: `true`
-   値が true の場合、PD 構成ファイルの`[log.file]`に従います。

## <code>--name</code> {#code-name-code}

-   このPDメンバーの人間が読める一意の名前
-   デフォルト: `"pd-${hostname}"`
-   複数の PD を開始する場合は、それぞれに異なる名前を使用する必要があります。

## <code>--cacert</code> {#code-cacert-code}

-   TLSを有効にするために使用されるCAのファイルパス
-   デフォルト: `""`

## <code>--cert</code> {#code-cert-code}

-   TLSを有効にするために使用されるX509証明書を含むPEMファイルのパス
-   デフォルト: `""`

## <code>--key</code> {#code-key-code}

-   TLSを有効にするために使用されるX509キーを含むPEMファイルのパス
-   デフォルト: `""`

## <code>--metrics-addr</code> {#code-metrics-addr-code}

-   デフォルトでは Prometheus にデータをプッシュしない Prometheus Pushgateway のアドレス。
-   デフォルト: `""`
