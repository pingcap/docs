---
title: Deploy TiCDC
summary: Learn how to deploy TiCDC and the hardware and software recommendations for deploying and running it.
---

# TiCDC をデプロイ {#deploy-ticdc}

このドキュメントでは、TiCDCクラスタをデプロイする方法と、それをデプロイして実行するためのハードウェアとソフトウェアの推奨事項について説明します。 TiCDC を新しい TiDBクラスタと共にデプロイするか、TiCDC コンポーネントを既存の TiDBクラスタに追加することができます。一般に、TiUP を使用して TiCDC を展開することをお勧めします。また、必要に応じてバイナリを使用してデプロイすることもできます。

## ソフトウェアとハードウェアの推奨事項 {#software-and-hardware-recommendations}

本番環境では、TiCDC のソフトウェアとハードウェアの推奨事項は次のとおりです。

| Linux OS              |     バージョン    |
| :-------------------- | :----------: |
| レッドハット エンタープライズ リナックス | 7.3 以降のバージョン |
| CentOS                | 7.3 以降のバージョン |

| CPU   | メモリー   | ディスクタイプ | 通信網                    | TiCDCクラスタインスタンスの数 (本番環境の最小要件) |
| :---- | :----- | :------ | :--------------------- | :---------------------------- |
| 16コア+ | 64GB以上 | SSD     | 10ギガビットネットワークカード（2枚推奨） | 2                             |

詳細については、 [ソフトウェアおよびハードウェアの推奨事項](/hardware-and-software-requirements.md)を参照してください。

## TiUP を使用して TiCDC を含む新しい TiDBクラスタをデプロイする {#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup}

TiUP を使用して新しい TiDBクラスタをデプロイすると、TiCDC も同時にデプロイできます。 TiUP が TiDBクラスタを開始するために使用する初期化構成ファイルに`cdc_servers`セクションを追加するだけで済みます。詳細な操作については、 [初期設定ファイルの編集](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)を参照してください。構成可能なフィールドの詳細については、 [`cdc_servers`を使用して cdc_server を構成する](/tiup/tiup-cluster-topology-reference.md#cdc_servers)を参照してください。

## TiUP を使用して既存の TiDBクラスタに TiCDC を追加する {#add-ticdc-to-an-existing-tidb-cluster-using-tiup}

TiUP を使用して、TiCDC コンポーネントを既存の TiDBクラスタに追加することもできます。次の手順を実行します。

1.  現在の TiDB バージョンが TiCDC をサポートしていることを確認してください。それ以外の場合は、TiDBクラスタを`v4.0.0-rc.1`以降のバージョンにアップグレードする必要があります。 v4.0.6 以降、TiCDC は一般提供 (GA) の機能になりました。 v4.0.6 以降のバージョンを使用することをお勧めします。

2.  TiCDC をデプロイするには、 [TiCDCクラスタをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster)を参照してください。

## バイナリを使用して TiCDC を既存の TiDBクラスタに追加する (非推奨) {#add-ticdc-to-an-existing-tidb-cluster-using-binary-not-recommended}

PDクラスタに、サービスを提供できる PD ノード (クライアント URL は`10.0.10.25:2379` ) があるとします。 3 つの TiCDC ノードをデプロイする場合は、次のコマンドを実行して TiCDCクラスタを起動します。同じ PD アドレスを指定するだけで、新しく開始されたノードが自動的に TiCDCクラスタに参加します。

{{< copyable "" >}}

```shell
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --addr=0.0.0.0:8302 --advertise-addr=127.0.0.1:8302
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --addr=0.0.0.0:8303 --advertise-addr=127.0.0.1:8303
```

## TiCDC <code>cdc server</code>のコマンドライン パラメータの説明 {#description-of-ticdc-code-cdc-server-code-command-line-parameters}

以下は、 `cdc server`コマンドで使用可能なオプションの説明です。

-   `addr` : TiCDC のリッスン アドレス、HTTP API アドレス、および TiCDC サービスの Prometheus アドレス。デフォルト値は`127.0.0.1:8300`です。
-   `advertise-addr` : クライアントが TiCDC にアクセスするために使用するアドバタイズされたアドレス。指定しない場合、値は`addr`の値と同じです。
-   `pd` : PD エンドポイントのコンマ区切りリスト。
-   `config` : TiCDC が使用する構成ファイルのアドレス (オプション)。このオプションは、TiCDC v5.0.0 以降でサポートされています。このオプションは、TiUP v1.4.0 以降の TiCDC 展開で使用できます。
-   `data-dir` : ファイルを格納するためにディスクを使用する必要がある場合に TiCDC が使用するディレクトリを指定します。 Unified Sorter は、このディレクトリを使用して一時ファイルを保存します。このディレクトリの空きディスク容量が 500 GiB 以上であることを確認することをお勧めします。詳細については、 [ユニファイドソーター](/ticdc/manage-ticdc.md#unified-sorter)を参照してください。 TiUP を使用している場合は、 [`cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers)セクションで`data_dir`を構成するか、 `global`でデフォルトの`data_dir`パスを直接使用できます。
-   `gc-ttl` : TiCDC によって設定された PD のサービス レベル`GC safepoint`の TTL (Time To Live) と、レプリケーション タスクが中断できる期間 (秒単位)。デフォルト値は`86400`で、これは 24 時間を意味します。注: TiCDC レプリケーション タスクの一時停止は、TiCDC GC セーフポイントの進行状況に影響を与えます。つまり、 [TiCDC GC セーフポイントの完全な動作](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)で詳述されているように、上流の TiDB GC の進行状況に影響を与えます。
-   `log-file` : TiCDC プロセスの実行時にログが出力されるパス。このパラメーターが指定されていない場合、ログは標準出力 (stdout) に書き込まれます。
-   `log-level` : TiCDC プロセスが実行されているときのログ レベル。デフォルト値は`"info"`です。
-   `ca` : TLS 接続用の PEM 形式の CA 証明書ファイルのパスを指定します (オプション)。
-   `cert` : TLS 接続用の PEM 形式の証明書ファイルのパスを指定します (オプション)。
-   `cert-allowed-cn` : TLS 接続の共通名のパスを PEM 形式で指定します (オプション)。
-   `key` : TLS 接続用の PEM 形式の秘密鍵ファイルのパスを指定します (オプション)。
-   `tz` : TiCDC サービスが使用するタイムゾーン。 TiCDC は、 `TIMESTAMP`などの時間データ タイプを内部で変換するとき、またはデータをダウンストリームにレプリケートするときに、このタイム ゾーンを使用します。デフォルトは、プロセスが実行されるローカル タイム ゾーンです。 `time-zone` ( `sink-uri` ) と`tz`を同時に指定すると、内部の TiCDC プロセスは`tz`で指定されたタイム ゾーンを使用し、シンクは`time-zone`で指定されたタイム ゾーンを使用してデータをダウンストリームにレプリケートします。
