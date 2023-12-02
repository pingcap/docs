---
title: PD Configuration Flags
summary: Learn some configuration flags of PD.
---

# PDコンフィグレーションフラグ {#pd-configuration-flags}

PD は、コマンドライン フラグと環境変数を使用して構成できます。

## <code>--advertise-client-urls</code> {#code-advertise-client-urls-code}

-   クライアントが PD にアクセスするためのアドバタイズ URL のリスト
-   デフォルト: `"${client-urls}"`
-   Docker や NAT ネットワーク環境などの状況によっては、PD がリッスンするデフォルトのクライアント URL を介してクライアントが PD にアクセスできない場合は、アドバタイズ クライアント URL を手動で設定する必要があります。
-   たとえば、Docker の内部 IP アドレスは`172.17.0.1`ですが、ホストの IP アドレスは`192.168.100.113`で、ポート マッピングは`-p 2379:2379`に設定されています。この場合、 `--advertise-client-urls` ～ `"http://192.168.100.113:2379"`を設定できます。クライアントは`"http://192.168.100.113:2379"`を通じてこのサービスを見つけることができます。

## <code>--advertise-peer-urls</code> {#code-advertise-peer-urls-code}

-   他の PD ノード (ピア) が PD ノードにアクセスするためのアドバタイズ URL のリスト
-   デフォルト: `"${peer-urls}"`
-   Docker または NAT ネットワーク環境などの状況によっては、他のノード (ピア) が、この PD ノードがリッスンするデフォルトのピア URL を介して PD ノードにアクセスできない場合は、アドバタイズピア URL を手動で設定する必要があります。
-   たとえば、Docker の内部 IP アドレスは`172.17.0.1`ですが、ホストの IP アドレスは`192.168.100.113`で、ポート マッピングは`-p 2380:2380`に設定されています。この場合、 `--advertise-peer-urls` ～ `"http://192.168.100.113:2380"`を設定できます。他の PD ノードは`"http://192.168.100.113:2380"`を通じてこのサービスを見つけることができます。

## <code>--client-urls</code> {#code-client-urls-code}

-   PD がリッスンするクライアント URL のリスト
-   デフォルト: `"http://127.0.0.1:2379"`
-   クラスターをデプロイするときは、現在のホストの IP アドレスを`--client-urls` (たとえば、 `"http://192.168.100.113:2379"` ) として指定する必要があります。クラスターが Docker 上で実行されている場合は、Docker の IP アドレスを`"http://0.0.0.0:2379"`として指定します。

## <code>--peer-urls</code> {#code-peer-urls-code}

-   PD ノードがリッスンするピア URL のリスト
-   デフォルト: `"http://127.0.0.1:2380"`
-   クラスターをデプロイするときは、現在のホストの IP アドレスとして`--peer-urls` ( `"http://192.168.100.113:2380"`など) を指定する必要があります。クラスターが Docker 上で実行されている場合は、Docker の IP アドレスを`"http://0.0.0.0:2380"`として指定します。

## <code>--config</code> {#code-config-code}

-   設定ファイル
-   デフォルト: `""`
-   コマンドラインを使用して構成を設定した場合、構成ファイル内の同じ設定は上書きされます。

## <code>--data-dir</code> {#code-data-dir-code}

-   データディレクトリへのパス
-   デフォルト: `"default.${name}"`

## <code>--initial-cluster</code> {#code-initial-cluster-code}

-   ブートストラップ用の初期クラスター構成
-   デフォルト: `"{name}=http://{advertise-peer-url}"`
-   たとえば、 `name`が &quot;pd&quot; で、 `advertise-peer-urls`が`"http://192.168.100.113:2380"`の場合、 `initial-cluster`は`"pd=http://192.168.100.113:2380"`になります。
-   3 つの PD サーバーを起動する必要がある場合、 `initial-cluster`は次のようになります。

        pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380

## <code>--join</code> {#code-join-code}

-   クラスターに動的に参加する
-   デフォルト: `""`
-   既存のクラスターに参加する場合は、 `--join="${advertise-client-urls}"`使用できます。 `advertise-client-url`は既存の PD であり、アドバタイズ クライアント URL をカンマで区切って複数指定します。

## <code>-L</code> {#code-l-code}

-   ログレベル
-   デフォルト: `"info"`
-   オプションの値: `"debug"` 、 `"info"` 、 `"warn"` 、 `"error"` 、 `"fatal"`

## <code>--log-file</code> {#code-log-file-code}

-   ログファイル
-   デフォルト: `""`
-   このフラグが設定されていない場合、ログは「stderr」に書き込まれます。このフラグが設定されている場合、ログは対応するファイルに出力されます。

## <code>--log-rotate</code> {#code-log-rotate-code}

-   ログのローテーションを有効または無効にするには
-   デフォルト: `true`
-   値が true の場合は、PD 設定ファイルの`[log.file]`に従います。

## <code>--name</code> {#code-name-code}

-   この PD メンバーの人が判読できる一意の名前
-   デフォルト: `"pd"`
-   複数の PD を開始する場合は、それぞれに異なる名前を使用する必要があります。

## <code>--cacert</code> {#code-cacert-code}

-   TLS を有効にするために使用される CA のファイル パス
-   デフォルト: `""`

## <code>--cert</code> {#code-cert-code}

-   TLS を有効にするために使用される、X509 証明書を含む PEM ファイルのパス
-   デフォルト: `""`

## <code>--key</code> {#code-key-code}

-   TLS を有効にするために使用される、X509 キーを含む PEM ファイルのパス
-   デフォルト: `""`

## <code>--metrics-addr</code> {#code-metrics-addr-code}

-   Prometheus Pushgateway のアドレス。デフォルトではデータを Prometheus にプッシュしません。
-   デフォルト: `""`
