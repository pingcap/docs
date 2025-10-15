---
title: Best Practices for TiDB Security Configuration
summary: 潜在的なセキュリティ リスクを軽減するために、TiDB セキュリティ構成のベスト プラクティスを学習します。
---

# TiDBSecurityコンフィグレーションのベストプラクティス {#best-practices-for-tidb-security-configuration}

TiDBのセキュリティは、データの整合性と機密性を保護するために不可欠です。このドキュメントでは、導入時にTiDBクラスタを安全に構成するためのガイドラインを示します。これらのベストプラクティスに従うことで、潜在的なセキュリティリスクを効果的に軽減し、データ侵害を防ぎ、TiDBデータベースシステムの継続的かつ安定した信頼性の高い運用を確保できます。

> **注記：**
>
> このドキュメントは、TiDBのセキュリティ設定に関する一般的な推奨事項を示しています。PingCAPは、情報の完全性または正確性を保証するものではなく、このガイドの使用から生じるいかなる問題についても責任を負いません。ユーザーは、これらの推奨事項を自身の特定のニーズに基づいて評価し、専門家に相談して適切なアドバイスを受ける必要があります。

## ルートユーザーの初期パスワードを設定する {#set-the-initial-password-for-the-root-user}

デフォルトでは、新規作成されたTiDBクラスタのrootユーザーにはパスワードが設定されていないため、潜在的なセキュリティリスクが生じます。パスワードが設定されていない場合、誰でもrootユーザーとしてTiDBデータベースにログインを試みることができ、データにアクセスして変更される可能性があります。

このリスクを回避するには、デプロイメント中にルート パスワードを設定することをお勧めします。

-   TiUPを使用したデプロイメントの場合は、 [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md#step-7-start-a-tidb-cluster)を参照して、ルート ユーザーのランダム パスワードを生成します。
-   TiDB Operatorを使用したデプロイメントの場合は、 [初期アカウントとパスワードを設定する](https://docs.pingcap.com/tidb-in-kubernetes/stable/initialize-a-cluster#set-initial-account-and-password)を参照して root パスワードを設定してください。

[`--initialize-secure`](/command-line-flags-for-tidb-configuration.md#--initialize-secure)オプションを使用して、初期ルート ユーザーのネットワーク アクセスを制限することもできます。

## パスワードの複雑さのチェックを有効にする {#enable-password-complexity-checks}

デフォルトでは、TiDB はパスワードの複雑さのポリシーを強制しないため、弱いパスワードや空のパスワードが使用され、セキュリティ リスクが増大する可能性があります。

データベースユーザーが強力なパスワードを作成できるようにするには、適切な[パスワードの複雑さのポリシー](/password-management.md#password-complexity-policy)を設定することをお勧めします。例えば、パスワードに大文字、小文字、数字、特殊文字の組み合わせを含めることを要求するポリシーを設定します。パスワードの複雑さのチェックを強制することで、データベースのセキュリティを向上させ、ブルートフォース攻撃を防ぎ、内部の脅威を軽減し、規制へのコンプライアンスを確保し、データ侵害のリスクを低減し、全体的なセキュリティを強化できます。

## デフォルトのGrafanaパスワードを変更する {#change-the-default-grafana-password}

TiDBのインストールにはデフォルトでGrafanaコンポーネントが含まれており、デフォルトのユーザー名とパスワード`admin`通常`admin`です。パスワードを速やかに変更しないと、攻撃者がこれを悪用してシステムを制御できる可能性があります。

TiDBの導入中は、Grafanaのパスワードを強力なものに変更し、システムのセキュリティを確保するために定期的に更新することをお勧めします。Grafanaのパスワードを変更する手順は次のとおりです。

-   Grafana に初めてログインしたら、プロンプトに従ってパスワードを変更します。

    ![Grafana Password Reset Guide](/media/grafana-password-reset1.png)

-   パスワードを変更するには、Grafana 個人設定センターにアクセスします。

    ![Grafana Password Reset Guide](/media/grafana-password-reset2.png)

## TiDBダッシュボードのセキュリティ強化 {#enhance-tidb-dashboard-security}

### 最小権限ユーザーを使用する {#use-a-least-privilege-user}

TiDBダッシュボードはTiDB SQLユーザーとアカウントシステムを共有し、TiDBダッシュボードの認証はTiDB SQLユーザーの権限に基づいています。TiDBダッシュボードは最小限の権限しか必要とせず、読み取り専用アクセスでも操作可能です。

セキュリティを強化するために、TiDB ダッシュボードにアクセスするための[最小権限の SQL ユーザー](/dashboard/dashboard-user.md)作成し、高い権限を持つユーザーの使用を避けることをお勧めします。

### アクセス制御を制限する {#restrict-access-control}

TiDBダッシュボードは、デフォルトでは信頼できるユーザー向けに設計されています。デフォルトのポートには、TiDBダッシュボードに加えて追加のAPIインターフェースが含まれています。外部ネットワークや信頼できないユーザーからのTiDBダッシュボードへのアクセスを許可する場合は、セキュリティ上の脆弱性を回避するために、以下の対策を講じてください。

-   ファイアウォールまたはその他のメカニズムを使用して、デフォルトの`2379`ポートを信頼できるドメインに制限し、外部ユーザーによるアクセスを防止します。

    > **注記：**
    >
    > TiDB、TiKV、その他のコンポーネントは、PDクライアントポートを介してPDコンポーネントと通信する必要があります。コンポーネント間の内部ネットワークアクセスをブロックしないでください。ブロックすると、クラスターが利用できなくなります。

-   [リバースプロキシを構成する](/dashboard/dashboard-ops-reverse-proxy.md#use-tidb-dashboard-behind-a-reverse-proxy) 、別のポート上の外部ユーザーに TiDB ダッシュボード サービスを安全に提供します。

## 内部ポートを保護する {#protect-internal-ports}

TiDBのインストールには、デフォルトでコンポーネント間通信用の特権インターフェースがいくつか含まれています。これらのポートは主に内部通信用であるため、通常、ユーザーがアクセスできるようにする必要はありません。これらのポートをパブリックネットワークに公開すると、攻撃対象領域が拡大し、最小権限の原則に違反し、セキュリティ脆弱性のリスクが高まります。次の表は、TiDBクラスタのデフォルトのリスニングポートを示しています。

| 成分              | デフォルトポート | プロトコル      |
| --------------- | -------- | ---------- |
| ティドブ            | 4000     | MySQL      |
| ティドブ            | 10080    | HTTP       |
| TiKV            | 20160    | プロトコル      |
| TiKV            | 20180    | HTTP       |
| PD              | 2379     | HTTP/プロトコル |
| PD              | 2380     | プロトコル      |
| TiFlash         | 3930     | プロトコル      |
| TiFlash         | 20170    | プロトコル      |
| TiFlash         | 20292    | HTTP       |
| TiFlash         | 8234     | HTTP       |
| DMマスター          | 8261     | HTTP       |
| DMマスター          | 8291     | HTTP       |
| DMワーカー          | 8262     | HTTP       |
| TiCDC           | 8300     | HTTP       |
| TiDB Lightning  | 8289     | HTTP       |
| TiDB Operator   | 6060     | HTTP       |
| TiDBダッシュボード     | 2379     | HTTP       |
| TiDBBinlog      | 8250     | HTTP       |
| TiDBBinlog      | 8249     | HTTP       |
| TMS             | 8082     | HTTP       |
| 透過型電子顕微鏡        | 8080     | HTTP       |
| 透過型電子顕微鏡        | 8000     | HTTP       |
| 透過型電子顕微鏡        | 4110     | HTTP       |
| 透過型電子顕微鏡        | 4111     | HTTP       |
| 透過型電子顕微鏡        | 4112     | HTTP       |
| 透過型電子顕微鏡        | 4113     | HTTP       |
| 透過型電子顕微鏡        | 4124     | HTTP       |
| プロメテウス          | 9090     | HTTP       |
| グラファナ           | 3000     | HTTP       |
| アラートマネージャー      | 9093     | HTTP       |
| アラートマネージャー      | 9094     | プロトコル      |
| ノードエクスポーター      | 9100     | HTTP       |
| ブラックボックスエクスポーター | 9115     | HTTP       |
| NGモニタリング        | 12020    | HTTP       |

データベース用のポート`4000`とGrafanaダッシュボード用のポート`9000`のみを一般ユーザーに公開し、ネットワークセキュリティポリシーやファイアウォールを使用して他のポートへのアクセスを制限することをお勧めします。以下は、 `iptables`を使用してポートアクセスを制限する例です。

```shell
# Allow internal port communication from the whitelist of component IP addresses
sudo iptables -A INPUT -s internal IP address range -j ACCEPT

# Only open ports 4000 and 9000 to external users
sudo iptables -A INPUT -p tcp --dport 4000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9000 -j ACCEPT

# Deny all other traffic by default
sudo iptables -P INPUT DROP
```

TiDB ダッシュボードにアクセスする必要がある場合は、別[リバースプロキシを設定する](/dashboard/dashboard-ops-reverse-proxy.md#use-tidb-dashboard-behind-a-reverse-proxy)ポートで外部ネットワークに安全にサービスを提供することを推奨します。

## サードパーティのMySQL脆弱性スキャナーからの誤検知を解決する {#resolving-false-positives-from-third-party-mysql-vulnerability-scanners}

ほとんどの脆弱性スキャナーは、MySQLの脆弱性をバージョン情報に基づいて検出します。TiDBはMySQLプロトコルと互換性がありますが、MySQL自体は互換性がないため、バージョンベースの脆弱性スキャンは誤検知につながる可能性があります。脆弱性スキャンは原則に基づく評価に重点を置くことをお勧めします。コンプライアンススキャンツールが特定のMySQLバージョンを要求する場合は、 [サーバーのバージョン番号を変更する](/faq/high-reliability-faq.md#does-tidb-support-modifying-the-mysql-version-string-of-the-server-to-a-specific-one-that-is-required-by-the-security-vulnerability-scanning-tool)使用して要件を満たすことができます。

サーバーのバージョン番号を変更することで、脆弱性スキャナーによる誤検知を回避できます。1 [`server-version`](/tidb-configuration-file.md#server-version)値は、TiDB ノードが現在の TiDB バージョンを確認するために使用されます。TiDB クラスターをアップグレードする前に、予期しない動作を回避するために、 `server-version`値が空であるか、実際の TiDB バージョンであることを確認してください。
