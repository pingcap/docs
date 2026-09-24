---
title: TiProxy Configuration File
summary: TiProxy を構成する方法を学びます。
---

# TiProxy設定ファイル {#tiproxy-configuration-file}

このドキュメントでは、 TiProxyの導入と使用に関連する設定パラメータについて説明します。TiUP導入トポロジの設定については、 [tiproxy-servers の設定](/tiup/tiup-cluster-topology-reference.md#tiproxy_servers)を参照してください。

以下に構成例を示します。

```toml
[proxy]
addr = "0.0.0.0:6000"
max-connections = 100

[api]
addr = "0.0.0.0:3080"

[ha]
virtual-ip = "10.0.1.10/24"
interface = "eth0"

[security]
[security.cluster-tls]
skip-ca = true

[security.sql-tls]
skip-ca = true
```

## `tiproxy.toml`ファイルを設定する {#configure-the-tiproxy-toml-file}

このセクションでは、TiProxy の設定パラメータについて説明します。

> **Tip:**
>
> 設定項目の値を調整する必要がある場合は、 [設定を変更する](/maintain-tidb-using-tiup.md#modify-the-configuration)を参照してください。通常、変更を行うと再起動が必要になります。TiProxy はホットリロードをサポートしているため、 `tiup cluster reload --skip-restart`を実行することで再起動を省略できます。

### プロキシ {#proxy}

SQL ポートの設定。

#### `addr` {#addr}

- デフォルト値: `0.0.0.0:6000`
- ホットリロードのサポート: いいえ
- SQLサービスのリスニングアドレス。形式は`<ip>:<port>`です。この設定項目は、 TiUPまたはTiDB Operatorを使用してTiProxyをデプロイすると自動的に設定されます。

#### `advertise-addr` {#advertise-addr}

- デフォルト値: `""`
- ホットリロードのサポート: いいえ
- 他のコンポーネントがこのTiProxyインスタンスに接続するために使用するアドレスを指定します。このアドレスにはホスト名のみが含まれ、ポート番号は含まれません。このアドレスは[`addr`](#addr)のホスト名とは異なる場合があります。例えば、TiProxyのTLS証明書の`Subject Alternative Name`ドメイン名のみが含まれている場合、他のコンポーネントはIP経由でTiProxyに接続できません。この設定項目は、 TiUPまたはTiDB Operatorを使用してTiProxyをデプロイすると自動的に設定されます。設定されていない場合は、TiProxyインスタンスの外部IPアドレスが使用されます。

#### `graceful-wait-before-shutdown` {#graceful-wait-before-shutdown}

- デフォルト値: `0`
- ホットリロードのサポート: はい
- 単位: 秒
- TiProxyがシャットダウンすると、HTTPステータスはunhealthyを返しますが、SQLポートは`graceful-wait-before-shutdown`秒間は新規接続を受け付けます。その後、新規接続は拒否され、クライアントをドレインします。クライアントとTiProxyの間に他のプロキシ（NLBなど）が存在しない場合は、この値を`0`に設定することをお勧めします。

#### `graceful-close-conn-timeout` {#graceful-close-conn-timeout}

- デフォルト値: `15`
- ホットリロードのサポート: はい
- 単位: 秒
- TiProxy がシャットダウンする際、現在のトランザクション（ドレインクライアントとも呼ばれます）が`graceful-close-conn-timeout`秒以内に完了すると、接続が閉じられます。その後、すべての接続が一度に閉じられます。`graceful-close-conn-timeout`は`graceful-wait-before-shutdown`の後に発生します。このタイムアウトは、トランザクションのライフサイクルよりも長く設定することをお勧めします。

#### `fail-backend-list` <span class="version-mark">v1.3.3 の新機能</span> {#fail-backend-list-new-in-v133}

+ デフォルト値: `[]`
+ ホットリロードのサポート: はい
+ ルーティングから除外するバックエンドのリストを指定します。TiDB サーバーの障害を確認した後、そのサーバーをこのリストに追加できます。TiProxy はこれらのバックエンドへの新規接続のルーティングを停止し、既存の接続をそれらから移行します。リスト内の各項目は、次の 2 つの形式のいずれかにできます。

    - バックエンド Pod 名。例: `"db-tidb-0"`
    - `<ip>:<port>` 形式のバックエンドアドレス。例: `"10.0.0.10:4000"`

+ このリストを適用するとルーティング可能なバックエンドがなくなる場合、接続要求を引き続きルーティングできるようにするため、TiProxy はこのリストを無視します。

#### `failover-timeout` <span class="version-mark">v1.3.3 の新機能</span> {#failover-timeout-new-in-v133}

+ デフォルト値: `60`
+ ホットリロードのサポート: はい
+ 単位: 秒
+ 範囲: `>= 0`
+ バックエンドが [`fail-backend-list`](#fail-backend-list-new-in-v133) に含まれると、TiProxy はそのバックエンドから既存の接続を移行します。`failover-timeout` 秒後もそのバックエンドに接続が残っている場合、TiProxy はこれらの接続を強制的に閉じます。`0` は、TiProxy が残っている接続を直ちに強制的に閉じることを意味します。

#### `max-connections` {#max-connections}

- デフォルト値: `0`
- ホットリロードのサポート: はい
- 各 TiProxy インスタンスは最大`max-connections`接続を受け入れることができます。`0`は制限がないことを意味します。

#### `high-memory-usage-reject-threshold` <span class="version-mark">v1.3.3 の新機能</span> {#high-memory-usage-reject-threshold-new-in-v133}

+ デフォルト値: `0.9`
+ ホットリロードのサポート: はい
+ 範囲: `[0, 1]`
+ TiProxy のメモリ使用率がこのしきい値に達するか、これを超えると、TiProxy は新規接続を拒否し、status ポートは異常ステータスを返します。既存の接続には影響しません。[`ha.virtual-ip`](#virtual-ip) が設定されている場合、インスタンスは仮想 IP も解放します。たとえば、`0.9` は、メモリ使用率が 90% に達したときに TiProxy が新規接続の拒否を開始することを意味します。
+ `0` は、TiProxy がメモリ使用率に基づいて新規接続を拒否しないことを意味します。設定値が `0` より大きく `0.5` より小さい場合、TiProxy はそれを `0.5` に調整します。

#### `conn-buffer-size` {#conn-buffer-size}

- デフォルト値: `32768`
- ホットリロードのサポート: はい、ただし新規接続のみ
- 範囲: `[1024, 16777216]`
- この設定項目では、接続バッファのサイズを指定できます。各接続は、読み取りバッファと書き込みバッファをそれぞれ1つずつ使用します。これはメモリとパフォーマンスのトレードオフです。バッファサイズを大きくするとパフォーマンスは向上しますが、メモリ消費量も増加します。`0`に設定すると、TiProxy はデフォルトのバッファサイズを使用します。

#### `pd-addrs` {#pd-addrs}

- デフォルト値: `127.0.0.1:2379`
- ホットリロードのサポート: いいえ
- TiProxyが接続するPDアドレス。TiProxyはPDからTiDBリストを取得することでTiDBインスタンスを検出します。TiUPまたはTiDB OperatorによってTiProxyがデプロイされると、自動的に設定されます。

#### `proxy-protocol` {#proxy-protocol}

- デフォルト値: `""`
- ホットリロードのサポート: はい、ただし新規接続のみ
- 値のオプション: `""` 、 `"v2"`
- ポートの[PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)を有効にしてください。PROXYプロトコルを有効にすると、TiProxyは実際のクライアントIPアドレスをTiDBに渡すことができます。`"v2"` PROXYプロトコルバージョン2の使用を示し、 `""` PROXYプロトコルの無効化を示します。TiProxyでPROXYプロトコルが有効になっている場合は、TiDBサーバーでも[PROXYプロトコル](/tidb-configuration-file.md#proxy-protocol)を有効にする必要があります。

### API {#api}

HTTP ゲートウェイの構成。

#### `addr` {#addr}

- デフォルト値: `0.0.0.0:3080`
- ホットリロードのサポート: いいえ
- APIゲートウェイアドレス。`ip:port`を指定できます。

#### `proxy-protocol` {#proxy-protocol}

- デフォルト値: `""`
- ホットリロードのサポート: いいえ
- 値のオプション: `""` 、 `"v2"`
- ポートの[PROXYプロトコル](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)を有効にします。`"v2"` PROXY プロトコル バージョン 2 を使用することを示し、 `""` PROXY プロトコルを無効にすることを示します。

### バランス {#balance}

TiProxy の負荷分散ポリシーの構成。

#### `label-name` {#label-name}

- デフォルト値: `""`
- ホットリロードのサポート: はい
- [ラベルベースの負荷分散](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing)に使用するラベル名を指定します。TiProxy は、このラベル名に基づいて TiDB サーバーのラベル値を照合し、自分と同じラベル値を持つ TiDB サーバーへのルーティングリクエストを優先します。
- デフォルト値の`label-name`は空文字列で、ラベルベースの負荷分散が使用されないことを示します。この負荷分散ポリシーを有効にするには、この設定項目を空でない文字列に設定し、TiProxy で[`labels`](#labels) 、TiDB で[`labels`](/tidb-configuration-file.md#labels)の両方を設定する必要があります。詳細については、 [ラベルベースの負荷分散](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing)を参照してください。

#### `policy` {#policy}

- デフォルト値: `resource`
- ホットリロードのサポート: はい
- 値のオプション: `resource` 、 `location` 、 `connection`
- 負荷分散ポリシーを指定します。各値の意味については、 [TiProxy 負荷分散ポリシー](/tiproxy/tiproxy-load-balance.md#configure-load-balancing-policies)を参照してください。

#### `routing-policy` <span class="version-mark">v1.3.3 の新機能</span> {#routing-policy-new-in-v133}

+ デフォルト値: `prefer-idle`
+ ホットリロードのサポート: はい
+ 取り得る値: `prefer-idle`, `random`, `idlest`
+ 新規接続のルーティングポリシーを指定します。

    - `prefer-idle`: 接続移行が必要なバックエンドを除外し、残りのルーティング可能なバックエンドからランダムに選択します。ほとんどのシナリオに適しています。
    - `random`: ルーティング可能なバックエンドからランダムに選択します。このとき、最もアイドルなバックエンドが選択される確率はわずかに高くなります。新規接続率が高いシナリオに適しています。
    - `idlest`: 常に最もアイドルなルーティング可能バックエンドに新規接続をルーティングします。長寿命の接続が多く、接続作成頻度が低いシナリオに適しています。

#### `status` <span class="version-mark">v1.3.3 の新機能</span> {#status-new-in-v133}

ステータスベースのロードバランシング設定。

##### `migrations-per-second` <span class="version-mark">v1.3.3 の新機能</span> {#migrations-per-second-new-in-v133}

+ デフォルト値: `0`
+ ホットリロードのサポート: はい
+ 範囲: `>= 0`
+ ステータスベースのロードバランシングで 1 秒あたりに移行する接続数を指定します。`0` は、TiProxy が現在の接続数に基づいて移行レートを自動計算することを意味します。TiDB サーバーのシャットダウン時には、接続移行を高速化するためにこの値を適切に増やすことができます。

#### `health` <span class="version-mark">v1.3.3 の新機能</span> {#health-new-in-v133}

ヘルスベースのロードバランシング設定。[`policy`](#policy) が `resource` または `location` の場合にのみ有効です。

##### `enabled` <span class="version-mark">v1.3.3 の新機能</span> {#enabled-new-in-v133}

+ デフォルト値: `true`
+ ホットリロードのサポート: はい
+ [ヘルスベースのロードバランシング](/tiproxy/tiproxy-load-balance.md#health-based-load-balancing) を有効にするかどうかを制御します。

##### `migrations-per-second` <span class="version-mark">v1.3.3 の新機能</span> {#migrations-per-second-new-in-v133span-1}

+ デフォルト値: `0`
+ ホットリロードのサポート: はい
+ 範囲: `>= 0`
+ ヘルスベースのロードバランシングにおいて、1 秒あたりに移行される接続数を指定します。`0` は、TiProxy が移行レートを自動的に計算することを示します。

#### `memory` <span class="version-mark">v1.3.3 の新機能</span> {#memory-new-in-v133}

メモリベースのロードバランシングの設定です。この項目は、[`policy`](#policy) が `resource` または `location` の場合にのみ有効になります。

##### `enabled` <span class="version-mark">v1.3.3 の新機能</span> {#enabled-new-in-v133span-1}

+ デフォルト値: `true`
+ ホットリロードのサポート: はい
+ [メモリベースのロードバランシング](/tiproxy/tiproxy-load-balance.md#memory-based-load-balancing) を有効にするかどうかを制御します。

##### `migrations-per-second` <span class="version-mark">v1.3.3 の新機能</span> {#migrations-per-second-new-in-v133span-2}

+ デフォルト値: `0`
+ ホットリロードのサポート: はい
+ 範囲: `>= 0`
+ メモリベースのロードバランシングにおいて、1 秒あたりに移行される接続数を指定します。`0` は、TiProxy が移行レートを自動的に計算することを示します。

#### `cpu` <span class="version-mark">v1.3.3 の新機能</span> {#cpu-new-in-v133}

CPU ベースのロードバランシングの設定です。この項目は、[`policy`](#policy) が `resource` または `location` の場合にのみ有効になります。

##### `enabled` <span class="version-mark">v1.3.3 の新機能</span> {#enabled-new-in-v133span-2}

+ デフォルト値: `true`
+ ホットリロードのサポート: はい
+ [CPU ベースのロードバランシング](/tiproxy/tiproxy-load-balance.md#cpu-based-load-balancing) を有効にするかどうかを制御します。

##### `migrations-per-second` <span class="version-mark">v1.3.3 の新機能</span> {#migrations-per-second-new-in-v133span-3}

+ デフォルト値: `0`
+ ホットリロードのサポート: はい
+ 範囲: `>= 0`
+ CPU ベースのロードバランシングにおいて、1 秒あたりに移行される接続数を指定します。`0` は、TiProxy が移行レートを自動的に計算することを示します。CPU ホットスポットが頻繁に移動する場合は、接続の繰り返し移行を避けるため、この値を高く設定しすぎないことを推奨します。

##### `min-balance-usage` <span class="version-mark">v1.3.3 の新機能</span> {#min-balance-usage-new-in-v133}

+ デフォルト値: `0`
+ ホットリロードのサポート: はい
+ 範囲: `[0, 1]`
+ ソースバックエンドの CPU 使用率がこのしきい値より低い場合、CPU ベースの接続移行はトリガーされません。たとえば、`0.2` は、ソースバックエンドの CPU 使用率が 20% 未満の場合に移行が実行されないことを意味します。

##### `max-usage-gap` <span class="version-mark">v1.3.3 の新機能</span> {#max-usage-gap-new-in-v133}

+ デフォルト値: `1`
+ ホットリロードのサポート: はい
+ 範囲: `0` または `[0.05, 1]`
+ CPU ベースの接続移行をトリガーするために必要な最小 CPU 使用率差を指定します。ソースバックエンドとターゲットバックエンドの CPU 使用率差がこのしきい値に達すると、移行がトリガーされます。たとえば、`0.1` は差が 10% に達したときに移行をトリガーできることを意味します。デフォルト値 `1` は、移行するかどうかが適応ルールのみに依存することを意味します。`0` は、このパラメータがデフォルト値を使用することを意味します。バックエンド間で CPU 使用率をより均等にしたい場合は、この値を適切に小さくできます。

#### `location` <span class="version-mark">v1.3.3 の新機能</span> {#location-new-in-v133}

ロケーションベースのロードバランシングの設定です。この項目は [`policy`](#policy) が `resource` または `location` の場合にのみ有効です。

##### `enabled` <span class="version-mark">v1.3.3 の新機能</span> {#enabled-new-in-v133span-3}

+ デフォルト値: `true`
+ ホットリロードのサポート: はい
+ [ロケーションベースのロードバランシング](/tiproxy/tiproxy-load-balance.md#location-based-load-balancing) を有効にするかどうかを制御します。

##### `migrations-per-second` <span class="version-mark">v1.3.3 の新機能</span> {#migrations-per-second-new-in-v133span-4}

+ デフォルト値: `0`
+ ホットリロードのサポート: はい
+ 範囲: `>= 0`
+ ロケーションベースのロードバランシングで 1 秒あたりに移行される接続数を指定します。`0` はデフォルトの移行レートが使用されることを意味します。

#### `conn-count` <span class="version-mark">v1.3.3 の新機能</span> {#conn-count-new-in-v133}

接続数ベースのロードバランシングの設定です。

##### `migrations-per-second` <span class="version-mark">v1.3.3 の新機能</span> {#migrations-per-second-new-in-v133span-5}

+ デフォルト値: `0`
+ ホットリロードのサポート: はい
+ 範囲: `>= 0`
+ 接続数ベースのロードバランシングで 1 秒あたりに移行される接続数を指定します。`0` は TiProxy が移行レートを自動的に計算することを意味します。接続が頻繁に行ったり来たりして移行されることが観察される場合は、この値を適切に小さくできます。

##### `count-ratio-threshold` <span class="version-mark">v1.3.3 の新機能</span> {#count-ratio-threshold-new-in-v133}

+ デフォルト値: `1.2`
+ ホットリロードのサポート: はい
+ 範囲: `0` または `> 1`
+ 接続数ベースの移行をトリガーするための接続数比率しきい値を指定します。最も多くの接続を持つバックエンドと最も少ない接続を持つバックエンドの比率がこのしきい値を超えると、TiProxy は接続の移行を開始します。この値を大きくすると、移行頻度を減らすことができます。`0` は、このパラメータがデフォルト値を使用することを意味します。

### HA {#ha}

TiProxy の高可用性構成。

#### `virtual-ip` {#virtual-ip}

- デフォルト値: `""`
- ホットリロードのサポート: いいえ
- 仮想IPアドレスをCIDR形式（例： `"10.0.1.10/24"` ）で指定します。クラスタ内で複数のTiProxyインスタンスを同じ仮想IPで構成した場合、一度にバインドできるインスタンスは1つだけです。このインスタンスがオフラインになると、別のTiProxyインスタンスが自動的に仮想IPを引き継ぎます。これにより、クライアントは常に仮想IPを介して利用可能なTiProxyに接続できるようになります。

以下に構成例を示します。

```yaml
server_configs:
  tiproxy:
    ha.virtual-ip: "10.0.1.10/24"
    ha.interface: "eth0"
```

TiProxy v1.3.1以降、複数の仮想IPアドレスの設定がサポートされます。コンピューティングレイヤーのリソースを分離する必要がある場合は、複数の仮想IPアドレスを設定し、 [ラベルベースの負荷分散](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing)と組み合わせて使用できます。設定例については、 [ラベルベースの負荷分散](/tiproxy/tiproxy-load-balance.md#label-based-load-balancing)を参照してください。

> **Note:**
>
> - 仮想 IP は Linux オペレーティングシステムでのみサポートされます。
> - TiProxy を実行する Linux ユーザーには、IP アドレスをバインドする権限が必要です。
> - 1 つの TiProxy インスタンスの実際の IP アドレスと仮想 IP アドレスは、同じ CIDR 範囲内にある必要があります。

#### `interface` {#interface}

- デフォルト値: `""`
- ホットリロードのサポート: いいえ
- 仮想IPをバインドするネットワークインターフェースを指定します（例： `"eth0"` ）。仮想IPは、 [`ha.virtual-ip`](#virtual-ip)と`ha.interface`両方が設定されている場合にのみTiProxyインスタンスにバインドされます。

#### `garp-burst-count` <span class="version-mark">v1.3.3 の新機能</span> {#garp-burst-count-new-in-v133}

+ デフォルト値: `5`
+ ホットリロードのサポート: いいえ
+ 範囲: `>= 0`
+ TiProxy インスタンスが引き継いで仮想 IP をバインドした直後に送信される GARP (Gratuitous ARP) パケット数を指定します。GARP は、スイッチおよびホストに仮想 IP に対応する MAC アドレスを更新するよう通知するために使用され、これによりクライアントトラフィックを仮想 IP を引き継いだ TiProxy インスタンスへできるだけ早く切り替えることができます。複数のパケットを連続して送信することで、最初の GARP パケットの損失による切り替え遅延のリスクを低減できます。`0` は自動的に `1` に調整されます。

#### `garp-refresh-count` <span class="version-mark">v1.3.3 の新機能</span> {#garp-refresh-count-new-in-v133}

+ デフォルト値: `30`
+ ホットリロードのサポート: いいえ
+ 範囲: `>= 0`
+ 仮想 IP を引き継いだ後に、追加で GARP バーストを送信する回数を指定します。2 回の送信の間隔は 1 秒で、毎回 [`garp-burst-count`](#garp-burst-count-new-in-v133) 個のパケットが送信されます。これは、フェイルオーバー後の一定期間、上流デバイス内の以前の仮想 IP と MAC アドレスの対応関係を更新し、トラフィックが引き続き古いインスタンスに転送されることを防ぐために使用されます。`0` は、引き継ぎ後に追加のパケットを送信しないことを意味します。

### `labels` {#labels}

- デフォルト値: `{}`
- ホットリロードのサポート: はい
- サーバーのラベルを指定します。例： `{ zone = "us-west-1", dc = "dc1" }` 。

### ログ {#log}

#### `level` {#level}

- デフォルト値: `info`
- ホットリロードのサポート: はい
- 値のオプション: `debug` 、 `info` 、 `warn` 、 `error` 、 `panic`
- ログレベルを指定します。レベル`panic`の場合、TiProxyはエラー発生時にpanicになります。

#### `encoder` {#encoder}

- デフォルト値: `tidb`
- 以下を指定できます:

    - `tidb` : TiDBで使用されるフォーマット。詳細は[統合ログ形式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)を参照してください。
    - `json` : 構造化された JSON 形式。
    - `console` : 人間が読めるログ形式。

### log.log-file {#log-log-file}

#### `filename` {#filename}

- デフォルト値: `""`
- ホットリロードのサポート: はい
- ログファイルのパス。空でない値を指定すると、ファイルへのログ記録が有効になります。TiProxy がTiUPと共にデプロイされている場合、ファイル名は自動的に設定されます。

#### `max-size` {#max-size}

- デフォルト値: `300`
- ホットリロードのサポート: はい
- 単位: MB
- ログファイルの最大サイズを指定します。ログファイルのサイズがこの制限を超えると、ログファイルはローテーションされます。

#### `max-days` {#max-days}

- デフォルト値: `3`
- ホットリロードのサポート: はい
- 古いログファイルを保存する最大日数を指定します。この期間を過ぎると、古いログファイルは削除されます。

#### `max-backups` {#max-backups}

- デフォルト値: `3`
- ホットリロードのサポート: はい
- 保持するログファイルの最大数を指定します。超過したログファイルは自動的に削除されます。

### 安全 {#security}

> **Note:**
>
> TiProxyは1時間に1回、ディスクから証明書を再読み込みします。そのため、ディスク上の証明書ファイルに加えた変更が有効になるまでに最大1時間かかる場合があります。

`[security]`セクションには、名前の異なる TLS オブジェクトが 4つあります。これらは設定形式とフィールドは同じですが、名前によって解釈が異なります。

```toml
[security]
    [sql-tls]
    skip-ca = true
    [server-tls]
    auto-certs = true
```

すべての TLS オプションはホットリロードされます。

TLS オブジェクト フィールド:

- `ca` : CAを指定する
- `cert` : 証明書を指定します
- `key` : 秘密鍵を指定する
- `auto-certs` : 主にテストに使用されます。証明書またはキーが指定されていない場合は証明書を生成します。
- `skip-ca` : クライアント オブジェクト上の CA を使用した証明書の検証をスキップするか、サーバーオブジェクト上のサーバー側の検証をスキップします。
- `min-tls-version` : 最小のTLSバージョンを設定します。設定可能な値は`1.0` 、 `1.1` 、 `1.2` 、 `1.3`です。デフォルト値は`1.2`で、v1.2以上のTLSバージョンが許可されます。
- `rsa-key-size` : `auto-certs`が有効な場合の RSA キー サイズを設定します。
- `autocert-expire-duration` : 自動生成された証明書のデフォルトの有効期限を設定します。

オブジェクトは名前によってクライアント オブジェクトまたはサーバーオブジェクトに分類されます。

クライアント TLS オブジェクトの場合:

- サーバー証明書の検証をスキップするには、 `ca`または`skip-ca`を設定する必要があります。
- オプションで、サーバー側のクライアント検証に合格するために`cert`または`key`を設定できます。
- 効果のないフィールド: `auto-certs`。

サーバーTLS オブジェクトの場合:

- TLS接続をサポートするには、 `cert` 、 `key` 、または`auto-certs`のいずれかを設定できます。それ以外の場合、TiProxyはTLS接続をサポートしません。
- オプションとして、 `ca`空でない場合、サーバー側でのクライアント検証が有効になります。クライアントは証明書を提供する必要があります。また、 `skip-ca`が true かつ`ca`空でない場合、サーバーはクライアントが証明書を提供した場合にのみ検証を行います。

#### `cluster-tls` {#cluster-tls}

クライアントTLSオブジェクト。TiDBまたはPDへのアクセスに使用されます。

#### `require-backend-tls` {#require-backend-tls}

- デフォルト値: `false`
- ホットリロードのサポート: はい、ただし新規接続のみ
- TiProxyとTiDBサーバー間のTLS接続を必須にします。TiDBサーバーがTLSをサポートしていない場合、クライアントはTiProxyへの接続時にエラーを報告します。

#### `sql-tls` {#sql-tls}

クライアントTLSオブジェクト。TiDB SQLポート（4000）へのアクセスに使用されます。

#### `server-tls` {#server-tls}

サーバーTLSオブジェクト。SQLポート（6000）でTLSを提供するために使用されます。

#### `server-http-tls` {#server-http-tls}

サーバーTLSオブジェクト。HTTPステータスポート（3080）でTLSを提供するために使用されます。
