---
title: Scheduling Configuration Flags
summary: スケジュール構成フラグは、コマンド ライン フラグまたは環境変数を使用して構成できます。
---

# スケジュールコンフィグレーションフラグ {#scheduling-configuration-flags}

スケジューリング ノードは、PD の`scheduling`マイクロサービスを提供するために使用されます。コマンドライン フラグまたは環境変数を使用して構成できます。

## <code>--advertise-listen-addr</code> {#code-advertise-listen-addr-code}

-   クライアントがスケジューリング ノードにアクセスするための URL。
-   デフォルト: `${listen-addr}`
-   Docker や NAT ネットワーク環境などの状況では、クライアントが`scheduling`でリッスンされるデフォルトのクライアント URL を通じてスケジューリング ノードにアクセスできない場合は、クライアント アクセス用に`--advertise-listen-addr`手動で設定する必要があります。
-   たとえば、Docker の内部 IP アドレスは`172.17.0.1`ですが、ホストの IP アドレスは`192.168.100.113`で、ポート マッピングは`-p 3379:3379`に設定されています。この場合、 `--advertise-listen-addr="http://192.168.100.113:3379"`設定できます。すると、クライアントは`http://192.168.100.113:3379`を通じてこのサービスを見つけることができます。

## <code>--backend-endpoints</code> {#code-backend-endpoints-code}

-   現在のスケジューリング ノードがリッスンする他のスケジューリング ノードのバックエンド エンドポイントのリスト。
-   デフォルト: `http://127.0.0.1:2379`

## <code>--cacert</code> {#code-cacert-code}

-   TLS を有効にするために使用される CA のファイル パス。
-   デフォルト: `""`

## <code>--cert</code> {#code-cert-code}

-   TLS を有効にするために使用される、X.509 証明書を含む PEM ファイルのパス。
-   デフォルト: `""`

## <code>--config</code> {#code-config-code}

-   設定ファイル。
-   デフォルト: `""`
-   構成ファイルを指定すると、スケジューリング ノードは最初にそのファイルから構成を読み取ります。同じ構成がコマンド ライン フラグでも指定されている場合、スケジューリング ノードはコマンド ライン フラグ構成を使用して構成ファイル内の構成を上書きします。

## <code>--data-dir</code> {#code-data-dir-code}

-   スケジューリング ノード上のデータ ディレクトリへのパス。
-   デフォルト: `"default.${name}"`

## <code>--key</code> {#code-key-code}

-   TLS を有効にするために使用される、X.509 キーを含む PEM ファイルのパス。
-   デフォルト: `""`

## <code>--listen-addr</code> {#code-listen-addr-code}

-   現在のスケジューリング ノードがリッスンするクライアント URL。
-   デフォルト: `"http://127.0.0.1:3379"`
-   クラスターをデプロイするときは、現在のホストの IP アドレスを`--listen-addr` (たとえば`"http://192.168.100.113:3379"` ) として指定する必要があります。ノードが Docker 上で実行される場合は、Docker IP アドレスを`"http://0.0.0.0:3379"`として指定します。

## <code>--log-file</code> {#code-log-file-code}

-   ログファイル。
-   デフォルト: `""`
-   このフラグが設定されていない場合、ログは「stderr」に出力されます。このフラグが設定されている場合、ログは対応するファイルに出力されます。

## <code>--name</code> <span class="version-mark">v8.3.0 の新機能</span> {#code-name-code-span-class-version-mark-new-in-v8-3-0-span}

-   現在のスケジューリング ノードの名前。
-   デフォルト: `"scheduling-${hostname}"`
-   複数のスケジューリング ノードを起動する必要がある場合は、識別しやすいように、ノードごとに異なる名前を設定することをお勧めします。

## <code>-L</code> {#code-l-code}

-   ログレベル。
-   デフォルト: `"info"`
-   `"error"` `"fatal"` `"warn"` `"debug"` `"info"`

## <code>-V</code> 、 <code>--version</code> {#code-v-code-code-version-code}

-   バージョン情報を出力して終了します。
