---
title: TiDB Cloud Filesystem の認可
summary: TiDB Cloud API credentials、owner token、scoped token が、TiDB Cloud Filesystem に対してどのように異なるレベルのアクセスを提供するかを学びます。
---

# TiDB Cloud Filesystem の認可

TiDB Cloud Filesystem では、ファイルシステムの管理とそのデータへのアクセスに、それぞれ異なる認証情報を使用します。これにより、高い権限を持つ認証情報は信頼できる環境に保持しつつ、ユーザー、アプリケーション、エージェントには必要最小限のアクセスのみを付与できます。

一般に、アクセスは各レベルで次第に制限されます。

```plaintext
TiDB Cloud API credentials
        ↓
Manage file system resources
        ↓
Owner token
        ↓
Access one file system
        ↓
Scoped token
        ↓
Access selected paths and operations
```

> **Note:**
>
> TiDB Cloud Filesystem は現在パブリックプレビューです。機能およびインターフェースは予告なく変更される場合があります。

## 認可モデル {#authorization-model}

TiDB Cloud Filesystem では、次の種類の認証情報を使用します。

| Credential                 | Access                                                                              | Typical use                                                             |
| -------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| TiDB Cloud API credentials | アカウントの権限に応じて、ファイルシステムリソースと owner token を管理する         | 信頼できる環境でのファイルシステム管理                                  |
| Owner token                | データおよび scoped token の管理を含む、1 つのファイルシステムへの広範なアクセス    | ファイルシステムへのフルアクセスが必要な信頼できるワークフロー          |
| Scoped token               | 1 つのファイルシステム内の指定されたパスと操作のみにアクセス                        | 制限付きアクセスが必要なユーザー、アプリケーション、エージェント、または他のマシン |

これらの認証情報は相互に置き換え可能ではありません。TiDB Cloud API credentials はファイルシステムリソース自体を管理し、ファイルシステムトークンはファイルシステム内でのアクセスを制御します。

## TiDB Cloud API credentials {#tidb-cloud-api-credentials}

TiDB Cloud API credentials は、公開 API キーと秘密 API キーのペアで構成されます。これらの権限は、関連付けられた TiDB Cloud アカウントによって決まります。

TiDB Cloud API credentials は、ファイルシステムの作成、一覧表示、詳細表示、削除などの CLI 操作に使用します。また、CLI で追加の owner token を生成する際にも必要です。

これらの認証情報は、ファイルシステムデータへのアクセスだけを必要とするアプリケーションやエージェントに配布するのではなく、信頼できる管理環境または自動化環境に保持してください。

これらの認証情報は `ti configure` で設定するか、`TIDB_CLOUD_PUBLIC_KEY` と `TIDB_CLOUD_PRIVATE_KEY` を一緒に指定してください。詳細は、[TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md)を参照してください。

## Owner tokens {#owner-tokens}

owner token は、1 つのファイルシステムに対する広範なアクセスを提供します。ファイルの読み取り、書き込み、削除が可能であり、そのファイルシステム用の scoped token の作成と管理も行えます。

owner token は、そのファイルシステムにのみ適用されます。ファイルシステムの作成や削除など、リソースレベルの操作において TiDB Cloud API credentials の代わりにはなりません。また、owner token は別の owner token を作成することもできません。別の owner token を生成するには、TiDB Cloud API credentials が必要です。

owner token はファイルシステム内で広範な権限を持つため、信頼できるマシンまたはシークレットマネージャーに保管してください。別のユーザー、アプリケーション、またはエージェントが限定的なアクセスのみを必要とする場合は、owner token を共有するのではなく、scoped token を作成してください。

1 つのファイルシステムには、複数の有効な owner token を持たせることができます。これにより、異なるユーザー、アプリケーション、または環境で、同じトークンを共有する代わりに個別の認証情報を使用できます。

owner token の生成と管理の手順については、[ファイルシステムトークンの管理](/tidb-cloud-filesystem/manage-filesystem-tokens.md)を参照してください。

## Scoped tokens {#scoped-tokens}

scoped token は、1 つのファイルシステム内の指定されたパスと操作にアクセスを制限します。

サポートされる操作は次のとおりです。

- `read`: ファイルの内容とメタデータを読み取ります。
- `list`: ディレクトリ配下のエントリを一覧表示します。
- `search`: 許可されたパス配下のファイルを検索します。`search` には `read` も必要です。
- `write`: ファイルおよびディレクトリを作成または変更します。
- `delete`: ファイルまたはディレクトリを削除します。

たとえば、レポートアプリケーションには次のようなアクセスを付与できます。

- `/inputs` に対する `read,list` アクセス
- `/reports` に対する `read,list,write` アクセス

生成済みレポートの確認だけが必要な別のユーザーには、`/reports` に対する `read,list` アクセスを付与できます。

スコープ付き権限は、マウント経由でファイルシステムにアクセスする場合も含めて、ファイルシステムサービスによって強制されます。scoped token は自身の権限を拡張したり、他のトークンを作成または管理したりすることはできません。scoped token は有効期間中に更新できますが、更新しても権限が拡張されることはありません。

scoped token が発行された後、その作成元である owner token を無効化または取り消しても、scoped token は自動的には取り消されません。アクセスが不要になった場合は、scoped token を個別に取り消してください。

ファイルシステムへのフルアクセスを必要としないユーザー、アプリケーション、エージェント、または他のマシンにファイルシステムアクセスを付与する場合は、scoped token を使用してください。

scoped token の作成と委任の手順については、[ファイルシステムトークンの管理](/tidb-cloud-filesystem/manage-filesystem-tokens.md#generate-and-delegate-a-scoped-token)を参照してください。

## 認証情報の境界 {#credential-boundaries}

ワークフローに必要な最小限のアクセスを持つ認証情報を使用してください。

* ファイルシステムリソースの管理には **TiDB Cloud API credentials** を使用します。
* 信頼できるワークフローで、1 つのファイルシステムへの広範なアクセスまたはアクセスの委任が必要な場合は **owner token** を使用します。
* ユーザー、アプリケーション、またはエージェントが特定のパスと操作のみにアクセスする必要がある場合は **scoped token** を使用します。

同じ環境で複数種類の認証情報を利用できても、それらの権限が結合されることはありません。たとえば、TiDB Cloud API credentials も設定されていても、scoped token は scoped のままです。

TiDB Cloud CLI は、利便性のために選択したファイルシステムトークンをローカルに保存できます。ローカルでの認証情報の選択によって、リモートトークンが変更、無効化、または取り消されることはありません。`ti` がファイルシステムと認証情報をどのように選択するかの詳細は、[TiDB Cloud CLI の設定と認証情報](/ai/ti/reference/ti-configuration-and-credentials.md)を参照してください。

## 次のステップ {#what-s-next}

- [ファイルシステムトークンの管理](/tidb-cloud-filesystem/manage-filesystem-tokens.md)
- [複数のマシン間でファイルシステムを共有する](/tidb-cloud-filesystem/filesystem-sharing.md)
- [ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md)