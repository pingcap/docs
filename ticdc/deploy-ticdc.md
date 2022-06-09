---
title: Deploy TiCDC
summary: Learn how to deploy TiCDC and the hardware and software recommendations for deploying and running it.
---

# TiCDCをデプロイ {#deploy-ticdc}

このドキュメントでは、TiCDCクラスタを展開する方法と、それを展開および実行するためのハードウェアとソフトウェアの推奨事項について説明します。 TiCDCを新しいTiDBクラスタと一緒にデプロイするか、TiCDCコンポーネントを既存のTiDBクラスタに追加することができます。一般に、TiUPを使用してTiCDCを展開することをお勧めします。さらに、必要に応じてバイナリを使用してデプロイすることもできます。

## ソフトウェアとハードウェアの推奨事項 {#software-and-hardware-recommendations}

実稼働環境では、TiCDCのソフトウェアとハードウェアの推奨事項は次のとおりです。

| Linux OS                 |    バージョン    |
| :----------------------- | :---------: |
| Red Hat Enterprise Linux | 7.3以降のバージョン |
| CentOS                   | 7.3以降のバージョン |

| CPU   | メモリー    | ディスクタイプ | 通信網                    | TiCDCクラスタインスタンスの数（実稼働環境の最小要件） |
| :---- | :------ | :------ | :--------------------- | :---------------------------- |
| 16コア+ | 64 GB + | SSD     | 10ギガビットネットワークカード（2枚推奨） | 2                             |

詳細については、 [ソフトウェアとハードウェアの推奨事項](/hardware-and-software-requirements.md)を参照してください。

## TiUPを使用してTiCDCを含む新しいTiDBクラスタをデプロイします {#deploy-a-new-tidb-cluster-that-includes-ticdc-using-tiup}

TiUPを使用して新しいTiDBクラスタをデプロイする場合、同時にTiCDCをデプロイすることもできます。 TiUPがTiDBクラスタを開始するために使用する初期化構成ファイルに`cdc_servers`のセクションを追加するだけで済みます。詳細な操作については、 [初期化構成ファイルを編集します](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file)を参照してください。構成可能なフィールドの詳細については、 [`cdc_servers`を使用してcdc_serversを構成します](/tiup/tiup-cluster-topology-reference.md#cdc_servers)を参照してください。

## TiUPを使用して既存のTiDBクラスタにTiCDCを追加します {#add-ticdc-to-an-existing-tidb-cluster-using-tiup}

TiUPを使用して、TiCDCコンポーネントを既存のTiDBクラスタに追加することもできます。次の手順を実行します。

1.  現在のTiDBバージョンがTiCDCをサポートしていることを確認してください。それ以外の場合は、TiDBクラスタを`v4.0.0-rc.1`以降のバージョンにアップグレードする必要があります。 v4.0.6以降、TiCDCは一般提供（GA）の機能になりました。 v4.0.6以降のバージョンを使用することをお勧めします。

2.  TiCDCを展開するには、 [TiCDCクラスタをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster)を参照してください。

## バイナリを使用して既存のTiDBクラスタにTiCDCを追加します（非推奨） {#add-ticdc-to-an-existing-tidb-cluster-using-binary-not-recommended}

PDクラスタにサービスを提供できるPDノード（クライアントURLは`10.0.10.25:2379` ）があるとします。 3つのTiCDCノードを展開する場合は、次のコマンドを実行してTiCDCクラスタを起動します。同じPDアドレスを指定するだけで、新しく開始されたノードが自動的にTiCDCクラスタに参加します。

{{< copyable "" >}}

```shell
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --addr=0.0.0.0:8302 --advertise-addr=127.0.0.1:8302
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --addr=0.0.0.0:8303 --advertise-addr=127.0.0.1:8303
```

## TiCDCcdc <code>cdc server</code>のコマンドラインパラメーターの説明 {#description-of-ticdc-code-cdc-server-code-command-line-parameters}

以下は、 `cdc server`コマンドで使用可能なオプションの説明です。

-   `addr` ：TiCDCのリスニングアドレス、HTTP APIアドレス、およびTiCDCサービスのPrometheusアドレス。デフォルト値は`127.0.0.1:8300`です。
-   `advertise-addr` ：クライアントがTiCDCにアクセスするためにアドバタイズされたアドレス。指定しない場合、値は`addr`の値と同じになります。
-   `pd` ：PDエンドポイントのコンマ区切りのリスト。
-   `config` ：TiCDCが使用する構成ファイルのアドレス（オプション）。このオプションは、TiCDCv5.0.0以降でサポートされています。このオプションは、TiUPv1.4.0以降のTiCDC展開で使用できます。
-   `data-dir` ：ファイルを保存するためにディスクを使用する必要がある場合にTiCDCが使用するディレクトリを指定します。 Unified Sorterは、このディレクトリを使用して一時ファイルを保存します。このディレクトリの空きディスク容量が500GiB以上であることを確認することをお勧めします。詳細については、 [ユニファイドソーター](/ticdc/manage-ticdc.md#unified-sorter)を参照してください。 TiUPを使用している場合は、 [`cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers)セクションで`data_dir`を構成するか、 `global`でデフォルトの`data_dir`パスを直接使用できます。
-   `gc-ttl` ：TiCDCによって設定されたPDのサービスレベル`GC safepoint`のTTL（Time To Live）、およびレプリケーションタスクが一時停止できる期間（秒単位）。デフォルト値は`86400`で、これは24時間を意味します。注：TiCDCレプリケーションタスクの一時停止は、TiCDC GCセーフポイントの進行に影響します。つまり、 [TiCDCGCセーフポイントの完全な動作](/ticdc/troubleshoot-ticdc.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint)で詳しく説明されているように、アップストリームTiDBGCの進行に影響します。
-   `log-file` ：TiCDCプロセスの実行中にログが出力されるパス。このパラメーターが指定されていない場合、ログは標準出力（stdout）に書き込まれます。
-   `log-level` ：TiCDCプロセス実行時のログレベル。デフォルト値は`"info"`です。
-   `ca` ：TLS接続用のCA証明書ファイルのパスをPEM形式で指定します（オプション）。
-   `cert` ：TLS接続用の証明書ファイルのパスをPEM形式で指定します（オプション）。
-   `cert-allowed-cn` ：TLS接続用のPEM形式の共通名のパスを指定します（オプション）。
-   `key` ：TLS接続用の秘密鍵ファイルのパスをPEM形式で指定します（オプション）。
-   `tz` ：TiCDCサービスによって使用されるタイムゾーン。 TiCDCは、 `TIMESTAMP`などの時間データ型を内部で変換するとき、またはデータをダウンストリームに複製するときに、このタイムゾーンを使用します。デフォルトは、プロセスが実行されるローカルタイムゾーンです。一度に`time-zone` （ `sink-uri` ）と`tz`を指定すると、内部TiCDCプロセスは`tz`で指定されたタイムゾーンを使用し、シンクはデータをダウンストリームに複製するために`time-zone`で指定されたタイムゾーンを使用します。
