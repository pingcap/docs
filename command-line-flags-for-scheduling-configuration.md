---
title: Scheduling Configuration Flags
summary: スケジュール構成フラグは、コマンド ライン フラグまたは環境変数を介して構成できます。
---

# スケジュールコンフィグレーションフラグ {#scheduling-configuration-flags}

スケジューリングノードは、PD用の`scheduling`マイクロサービスを提供するために使用されます。コマンドラインフラグまたは環境変数を使用して設定できます。

## <code>--advertise-listen-addr</code> {#code-advertise-listen-addr-code}

-   クライアントがスケジューリング ノードにアクセスするための URL。
-   デフォルト: `${listen-addr}`
-   Docker や NAT ネットワーク環境などの状況では、クライアントが`scheduling`でリッスンされるデフォルトのクライアント URL を通じてスケジューリング ノードにアクセスできない場合は、クライアント アクセス用に`--advertise-listen-addr`手動で設定する必要があります。
-   例えば、Dockerの内部IPアドレスは`172.17.0.1`ですが、ホストのIPアドレスは`192.168.100.113`で、ポートマッピングは`-p 3379:3379`に設定されています。この場合、 `--advertise-listen-addr="http://192.168.100.113:3379"`設定できます。そうすることで、クライアントは`http://192.168.100.113:3379`を通じてこのサービスを見つけることができるようになります。

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
-   設定ファイルを指定すると、スケジューリングノードはまずそのファイルから設定を読み取ります。同じ設定がコマンドラインフラグでも指定されている場合、スケジューリングノードはコマンドラインフラグの設定を使用して設定ファイルの設定を上書きします。

## <code>--data-dir</code> {#code-data-dir-code}

-   スケジューリング ノード上のデータ ディレクトリへのパス。
-   デフォルト: `"default.${name}"`

## <code>--key</code> {#code-key-code}

-   TLS を有効にするために使用される、X.509 キーを含む PEM ファイルのパス。
-   デフォルト: `""`

## <code>--listen-addr</code> {#code-listen-addr-code}

-   現在のスケジューリング ノードがリッスンするクライアント URL。
-   デフォルト: `"http://127.0.0.1:3379"`
-   クラスターをデプロイする際は、現在のホストのIPアドレスを`--listen-addr` （例： `"http://192.168.100.113:3379"` ）に指定する必要があります。ノードがDocker上で実行されている場合は、DockerのIPアドレスを`"http://0.0.0.0:3379"`に指定してください。

## <code>--log-file</code> {#code-log-file-code}

-   ログ ファイル。
-   デフォルト: `""`
-   このフラグが設定されていない場合、ログは「stderr」に出力されます。このフラグが設定されている場合、ログは対応するファイルに出力されます。

## <code>--name</code> <span class="version-mark">v8.3.0 の新機能</span> {#code-name-code-span-class-version-mark-new-in-v8-3-0-span}

-   現在のスケジューリング ノードの名前。
-   デフォルト: `"scheduling-${hostname}"`
-   複数のスケジューリング ノードを起動する必要がある場合は、識別しやすいように、ノードごとに異なる名前を設定することをお勧めします。

## <code>-L</code> {#code-l-code}

-   ログ レベル。
-   デフォルト: `"info"`
-   `"warn"` `"fatal"` `"error"` `"debug"` `"info"`

## <code>-V</code> , <code>--version</code> {#code-v-code-code-version-code}

-   バージョン情報を出力して終了します。
