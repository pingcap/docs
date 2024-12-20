---
title: Best Practices for TiDB Security Configuration
summary: 潜在的なセキュリティ リスクを軽減するために、TiDB セキュリティ構成のベスト プラクティスを学習します。
---

# TiDBSecurityコンフィグレーションのベスト プラクティス {#best-practices-for-tidb-security-configuration}

TiDB のセキュリティは、データの整合性と機密性を保護するために重要です。このドキュメントでは、展開時に TiDB クラスターを安全に構成するためのガイドラインを示します。これらのベスト プラクティスに従うことで、潜在的なセキュリティ リスクを効果的に軽減し、データ侵害を防ぎ、TiDB データベース システムの継続的かつ安定した信頼性の高い運用を確保できます。

> **注記：**
>
> このドキュメントでは、TiDB セキュリティ構成に関する一般的な推奨事項を示します。PingCAP は情報の完全性や正確性を保証するものではなく、このガイドの使用によって生じる問題について一切の責任を負いません。ユーザーは、特定のニーズに基づいてこれらの推奨事項を評価し、専門家に相談してカスタマイズされたアドバイスを受ける必要があります。

## ルートユーザーの初期パスワードを設定する {#set-the-initial-password-for-the-root-user}

デフォルトでは、新しく作成された TiDB クラスターの root ユーザーにはパスワードがないため、潜在的なセキュリティ リスクが生じます。パスワードが設定されていない場合、誰でも root ユーザーとして TiDB データベースにログインでき、データにアクセスして変更できる可能性があります。

このリスクを回避するには、展開時にルート パスワードを設定することをお勧めします。

-   TiUPを使用したデプロイメントの場合は、 [TiUP を使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md#step-7-start-a-tidb-cluster)を参照して、root ユーザーのランダム パスワードを生成します。
-   TiDB Operator を使用したデプロイメントの場合は、 [初期アカウントとパスワードを設定する](https://docs.pingcap.com/tidb-in-kubernetes/stable/initialize-a-cluster#set-initial-account-and-password)を参照して root パスワードを設定してください。

## パスワードの複雑さのチェックを有効にする {#enable-password-complexity-checks}

デフォルトでは、TiDB はパスワードの複雑さのポリシーを適用しないため、弱いパスワードや空のパスワードが使用され、セキュリティ リスクが増大する可能性があります。

データベース ユーザーが強力なパスワードを作成できるようにするには、妥当な[パスワードの複雑さのポリシー](/password-management.md#password-complexity-policy)設定することをお勧めします。たとえば、パスワードに大文字、小文字、数字、特殊文字の組み合わせを含めることを要求するポリシーを設定します。パスワードの複雑さのチェックを実施することで、データベースのセキュリティを強化し、ブルート フォース攻撃を防ぎ、内部の脅威を減らし、規制への準拠を保証し、データ侵害のリスクを軽減して、全体的なセキュリティを強化できます。

## デフォルトのGrafanaパスワードを変更する {#change-the-default-grafana-password}

TiDB のインストールにはデフォルトで Grafanaコンポーネントが含まれており、デフォルトのユーザー名とパスワードは通常`admin`です。パスワードをすぐに変更しないと、攻撃者がこれを悪用してシステムを制御する可能性があります`admin`

TiDB の展開中は、Grafana のパスワードをすぐに強力なものに変更し、システムのセキュリティを確保するために定期的にパスワードを更新することをお勧めします。Grafana のパスワードを変更する手順は次のとおりです。

-   Grafana に初めてログインしたら、プロンプトに従ってパスワードを変更します。

    ![Grafana Password Reset Guide](/media/grafana-password-reset1.png)

-   パスワードを変更するには、Grafana 個人設定センターにアクセスします。

    ![Grafana Password Reset Guide](/media/grafana-password-reset2.png)

## TiDBダッシュボードのセキュリティ強化 {#enhance-tidb-dashboard-security}

### 最小権限ユーザーを使用する {#use-a-least-privilege-user}

TiDB ダッシュボードはTiDB SQLユーザーとアカウント システムを共有し、TiDB ダッシュボードの認証はTiDB SQLユーザーの権限に基づいています。TiDB ダッシュボードには最小限の権限が必要であり、読み取り専用アクセスでも操作できます。

セキュリティを強化するために、TiDB ダッシュボードにアクセスするための[最小権限の SQL ユーザー](/dashboard/dashboard-user.md)作成し、高い権限を持つユーザーの使用を避けることをお勧めします。

### アクセス制御を制限する {#restrict-access-control}

デフォルトでは、TiDB ダッシュボードは信頼できるユーザー向けに設計されています。デフォルトのポートには、TiDB ダッシュボードのほかに追加の API インターフェースが含まれています。外部ネットワークまたは信頼できないユーザーからの TiDB ダッシュボードへのアクセスを許可する場合は、セキュリティの脆弱性を回避するために次の対策を講じてください。

-   ファイアウォールまたはその他のメカニズムを使用して、デフォルトの`2379`ポートを信頼できるドメインに制限し、外部ユーザーによるアクセスを防止します。

    > **注記：**
    >
    > TiDB、TiKV、およびその他のコンポーネントは、PD クライアント ポートを介して PDコンポーネントと通信する必要があります。コンポーネント間の内部ネットワーク アクセスをブロックしないでください。ブロックすると、クラスターが使用できなくなります。

-   [リバースプロキシを構成する](/dashboard/dashboard-ops-reverse-proxy.md#use-tidb-dashboard-behind-a-reverse-proxy)すると、別のポート上の外部ユーザーに TiDB ダッシュボード サービスを安全に提供できます。

## 内部ポートを保護する {#protect-internal-ports}

デフォルトでは、TiDB インストールには、コンポーネント間通信用の特権インターフェイスがいくつか含まれています。これらのポートは主に内部通信用であるため、通常、ユーザーがアクセスできるようにする必要はありません。これらのポートをパブリック ネットワークに公開すると、攻撃対象領域が拡大し、最小権限の原則に違反し、セキュリティ脆弱性のリスクが高まります。次の表は、TiDB クラスターのデフォルトのリスニング ポートを示しています。

| 成分              | デフォルトポート | プロトコル      |
| --------------- | -------- | ---------- |
| ティビ             | 4000     | マイグレーション   |
| ティビ             | 10080    | ウェブ        |
| ティクヴ            | 20160    | プロトコル      |
| ティクヴ            | 20180    | ウェブ        |
| PD              | 2379     | HTTP/プロトコル |
| PD              | 2380     | プロトコル      |
| TiFlash         | 3930     | プロトコル      |
| TiFlash         | 20170    | プロトコル      |
| TiFlash         | 20292    | ウェブ        |
| TiFlash         | 8234     | ウェブ        |
| ティフロー           | 8261     | ウェブ        |
| ティフロー           | 8291     | ウェブ        |
| ティフロー           | 8262     | ウェブ        |
| ティフロー           | 8300     | ウェブ        |
| TiDB Lightning  | 8289     | ウェブ        |
| TiDB Operator   | 6060     | ウェブ        |
| TiDBダッシュボード     | 2379     | ウェブ        |
| TiDBBinlog      | 8250     | ウェブ        |
| TiDBBinlog      | 8249     | ウェブ        |
| テレメトリ           | 8082     | ウェブ        |
| 電子              | 8080     | ウェブ        |
| 電子              | 8000     | ウェブ        |
| 電子              | 4110     | ウェブ        |
| 電子              | 4111     | ウェブ        |
| 電子              | 4112     | ウェブ        |
| 電子              | 4113     | ウェブ        |
| 電子              | 4124     | ウェブ        |
| プロメテウス          | 9090     | ウェブ        |
| グラファナ           | 3000     | ウェブ        |
| アラートマネージャー      | 9093     | ウェブ        |
| アラートマネージャー      | 9094     | プロトコル      |
| ノードエクスポーター      | 9100     | ウェブ        |
| ブラックボックスエクスポーター | 9115     | ウェブ        |
| NGモニタリング        | 12020    | ウェブ        |

ネットワーク セキュリティ ポリシーまたはファイアウォールを使用して他のポートへのアクセスを制限しながら、データベース用の`4000`ポートと Grafana ダッシュボード用の`9000`ポートのみを一般ユーザーに公開することをお勧めします。以下は、 `iptables`使用してポート アクセスを制限する例です。

```shell
# Allow internal port communication from the whitelist of component IP addresses
sudo iptables -A INPUT -s internal IP address range -j ACCEPT

# Only open ports 4000 and 9000 to external users
sudo iptables -A INPUT -p tcp --dport 4000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 9000 -j ACCEPT

# Deny all other traffic by default
sudo iptables -P INPUT DROP
```

TiDB ダッシュボードにアクセスする必要がある場合は、別のポートで外部ネットワークに安全にサービスを提供すること[リバースプロキシを設定する](/dashboard/dashboard-ops-reverse-proxy.md#use-tidb-dashboard-behind-a-reverse-proxy)推奨します。

## サードパーティのMySQL脆弱性スキャナーによる誤検知を解決する {#resolving-false-positives-from-third-party-mysql-vulnerability-scanners}

ほとんどの脆弱性スキャナーは、バージョン情報に基づいて MySQL の脆弱性を検出します。TiDB は MySQL プロトコルと互換性がありますが、MySQL 自体は互換性がないため、バージョンベースの脆弱性スキャンでは誤検知が発生する可能性があります。脆弱性スキャンは原則ベースの評価に重点を置くことをお勧めします。コンプライアンス スキャン ツールで特定の MySQL バージョンが必要な場合は、 [サーバーのバージョン番号を変更する](/faq/high-reliability-faq.md#does-tidb-support-modifying-the-mysql-version-string-of-the-server-to-a-specific-one-that-is-required-by-the-security-vulnerability-scanning-tool)実行して要件を満たすことができます。

サーバーのバージョン番号を変更することで、脆弱性スキャナーによる誤検知を回避できます。1 [`server-version`](/tidb-configuration-file.md#server-version)値は、TiDB ノードが現在の TiDB バージョンを確認するために使用されます。TiDB クラスターをアップグレードする前に、予期しない動作を回避するために、 `server-version`値が空であるか、TiDB の実際のバージョンであることを確認してください。
