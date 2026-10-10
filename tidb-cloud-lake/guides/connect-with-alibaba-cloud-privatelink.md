---
title: Alibaba Cloud PrivateLink を使用して TiDB Cloud Lake に接続する
summary: Alibaba Cloud のプライベートエンドポイントを設定し、そのカスタムドメイン名を有効化して、TiDB Cloud Lake へのプライベート接続を検証します。
---

# Alibaba Cloud PrivateLink を使用して TiDB Cloud Lake に接続する

このドキュメントでは、Alibaba Cloud のプライベートエンドポイントを設定し、そのカスタムドメイン名を有効化して、TiDB Cloud Lake へのプライベート接続を検証する方法について説明します。

## Alibaba Cloud PrivateLink をセットアップする {#set-up-alibaba-cloud-privatelink}

1. **Connect to {{{ .lake }}}** ダイアログからエンドポイントサービス名を取得します。

    例: `com.aliyuncs.privatelink.ap-northeast-1.epsrv-6weddzcbkanrx5sc2zv4`

2. ポート 443 への受信 TCP トラフィックを許可するセキュリティグループを準備します。

    ![HTTPS トラフィックを許可するセキュリティグループ](/media/tidb-cloud-lake/alibaba-privatelink-security-group.png)

3. [Alibaba Cloud VPC コンソール](https://vpc.console.aliyun.com/endpoint/ap-northeast-1/endpoints/new) で、エンドポイントを作成します。この例では Japan (Tokyo) を使用します。

    ステップ 1 で取得したエンドポイントサービス名を入力し、**Verify** をクリックします。

    ![Lake のエンドポイントサービス名を使用してエンドポイントを作成する](/media/tidb-cloud-lake/alibaba-privatelink-create-endpoint.png)

    設定を確認し、ページ下部の作成ボタンをクリックします。

4. エンドポイント詳細ページで、**Custom Domain Name** を有効にします。

    ![カスタムドメイン名を有効にする](/media/tidb-cloud-lake/alibaba-privatelink-custom-domain-name.png)

5. VPC 内の Elastic Compute Service (ECS) インスタンスからエンドポイント接続を検証します。

    1. TiDB Cloud Lake のホームページで **Connect** をクリックします。**Connect to TiDB Cloud** ダイアログで、**Connection Information** の下にある **Host** の値をコピーします。

        ![接続情報から TiDB Cloud Lake のホストをコピーする](/media/tidb-cloud-lake/alibaba-privatelink-connection-host.png)

    2. `LAKE_HOST` にコピーしたホストを設定し、次のコマンドを実行します。

        ```shell
        LAKE_HOST='<your-tidb-cloud-lake-host>'

        getent ahostsv4 "$LAKE_HOST"

        curl --noproxy '*' -4 -sS -o /dev/null \
          -w 'remote_ip=%{remote_ip}\ntls_verify=%{ssl_verify_result}\n' \
          "https://$LAKE_HOST"
        ```

    3. Alibaba Cloud VPC コンソールでエンドポイント詳細ページを開き、エンドポイントの elastic network interfaces (ENI) に割り当てられたプライベート IP アドレスを確認します。`getent ahostsv4` が返すすべての IPv4 アドレスがエンドポイント ENI のプライベート IP アドレスであり、かつ `remote_ip` がそれらのいずれかのアドレスと一致することを確認してください。これにより、TiDB Cloud Lake へのテスト接続が Alibaba Cloud PrivateLink を使用しており、パブリックインターネットを経由していないことが確認できます。`tls_verify=0` の結果は、HTTPS 証明書の検証が成功したことを示します。

    4. リージョンゲートウェイの正常性を確認します。Japan (Tokyo) リージョンを例にします。

        ```shell
        curl --noproxy '*' -sS \
          https://gw.aliyun-ap-northeast-1.default.lake.tidbcloud.com/status
        ```

        レスポンスに `"status": "ok"` が含まれていれば、リージョンゲートウェイは利用可能です。