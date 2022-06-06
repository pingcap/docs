---
title: PD Configuration Flags
summary: Learn some configuration flags of PD.
---

# PDConfiguration / コンフィグレーションフラグ {#pd-configuration-flags}

PDは、コマンドラインフラグと環境変数を使用して構成できます。

## <code>--advertise-client-urls</code> {#code-advertise-client-urls-code}

-   クライアントがPDにアクセスするためのアドバタイズURLのリスト
-   デフォルト： `"${client-urls}"`
-   DockerまたはNATネットワーク環境などの一部の状況で、クライアントがPDによってリッスンされるデフォルトのクライアントURLを介してPDにアクセスできない場合は、アドバタイズするクライアントURLを手動で設定する必要があります。
-   たとえば、Dockerの内部IPアドレスは`172.17.0.1`ですが、ホストのIPアドレスは`192.168.100.113`で、ポートマッピングは`-p 2379:2379`に設定されています。この場合、 `--advertise-client-urls`を設定でき`"http://192.168.100.113:2379"` 。クライアントは`"http://192.168.100.113:2379"`までこのサービスを見つけることができます。

## <code>--advertise-peer-urls</code> {#code-advertise-peer-urls-code}

-   PDノードにアクセスするための他のPDノード（ピア）のアドバタイズURLのリスト
-   デフォルト： `"${peer-urls}"`
-   DockerまたはNATネットワーク環境などの一部の状況で、他のノード（ピア）がこのPDノードによってリッスンされるデフォルトのピアURLを介してPDノードにアクセスできない場合は、アドバタイズするピアURLを手動で設定する必要があります。
-   たとえば、Dockerの内部IPアドレスは`172.17.0.1`ですが、ホストのIPアドレスは`192.168.100.113`で、ポートマッピングは`-p 2380:2380`に設定されています。この場合、 `--advertise-peer-urls`を設定でき`"http://192.168.100.113:2380"` 。他のPDノードは`"http://192.168.100.113:2380"`を介してこのサービスを見つけることができます。

## <code>--client-urls</code> {#code-client-urls-code}

-   PDがリッスンするクライアントURLのリスト
-   デフォルト： `"http://127.0.0.1:2379"`
-   クラスタを展開するときは、現在のホストのIPアドレスを`--client-urls` （たとえば、 `"http://192.168.100.113:2379"` ）として指定する必要があります。クラスタがDockerで実行されている場合は、DockerのIPアドレスを`"http://0.0.0.0:2379"`として指定します。

## <code>--peer-urls</code> {#code-peer-urls-code}

-   PDノードがリッスンするピアURLのリスト
-   デフォルト： `"http://127.0.0.1:2380"`
-   クラスタを展開するときは、現在のホストのIPアドレスとして`--peer-urls` （ `"http://192.168.100.113:2380"`など）を指定する必要があります。クラスタがDockerで実行されている場合は、DockerのIPアドレスを`"http://0.0.0.0:2380"`として指定します。

## <code>--config</code> {#code-config-code}

-   構成ファイル
-   デフォルト： `""`
-   コマンドラインを使用して構成を設定すると、構成ファイルの同じ設定が上書きされます。

## <code>--data-dir</code> {#code-data-dir-code}

-   データディレクトリへのパス
-   デフォルト： `"default.${name}"`

## <code>--initial-cluster</code> {#code-initial-cluster-code}

-   ブートストラップの初期クラスタ構成
-   デフォルト： `"{name}=http://{advertise-peer-url}"`
-   たとえば、 `name`が「pd」で`advertise-peer-urls`が`"http://192.168.100.113:2380"`の場合、 `initial-cluster`は`"pd=http://192.168.100.113:2380"`です。
-   3台のPDサーバーを起動する必要がある場合、 `initial-cluster`台は次のようになります。

    ```
    pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380
    ```

## <code>--join</code> {#code-join-code}

-   動的にクラスタに参加する
-   デフォルト： `""`
-   既存のクラスタに参加する場合は、 `--join="${advertise-client-urls}"`を使用できます`advertise-client-url`は既存のPDであり、複数のアドバタイズクライアントのURLはコンマで区切られます。

## <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト： `"info"`
-   `"error"` `"fatal"` `"info"` `"warn"` `"debug"`

## <code>--log-file</code> {#code-log-file-code}

-   ログファイル
-   デフォルト： `""`
-   このフラグが設定されていない場合、ログは「stderr」に書き込まれます。このフラグが設定されている場合、ログは対応するファイルに出力されます。

## <code>--log-rotate</code> {#code-log-rotate-code}

-   ログローテーションを有効または無効にするには
-   デフォルト： `true`
-   値がtrueの場合、PD構成ファイルの`[log.file]`に従います。

## <code>--name</code> {#code-name-code}

-   このPDメンバーの人間が読める一意の名前
-   デフォルト： `"pd"`
-   複数のPDを開始する場合は、PDごとに異なる名前を使用する必要があります。

## <code>--cacert</code> {#code-cacert-code}

-   TLSを有効にするために使用されるCAのファイルパス
-   デフォルト： `""`

## <code>--cert</code> {#code-cert-code}

-   TLSを有効にするために使用されるX509証明書を含むPEMファイルのパス
-   デフォルト： `""`

## <code>--key</code> {#code-key-code}

-   TLSを有効にするために使用されるX509キーを含むPEMファイルのパス
-   デフォルト： `""`

## <code>--metrics-addr</code> {#code-metrics-addr-code}

-   デフォルトでデータをPrometheusにプッシュしないPrometheusPushgatewayのアドレス。
-   デフォルト： `""`
