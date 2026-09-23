---
title: TiDB Cloud CLI の設定と認証情報
summary: TiDB Cloud CLI のプロファイル、優先順位ルール、ローカル状態パス、file system 認証情報、SQL 認証情報、マウントロケーター、および操作ログのリファレンスです。
---

# TiDB Cloud CLI の設定と認証情報

`ti` は、プロダクトが所有するすべてのローカル状態を `~/.ti/` 配下に保存し、機密性のない設定と認証情報を分離します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 主なファイル {#main-files}

```toml
# ~/.ti/config
[default]
region_code = "aws-us-east-1"
```

```toml
# ~/.ti/credentials
[default]
tidb_cloud_public_key = "..."
tidb_cloud_private_key = "..."
```

認証情報ファイルは、プラットフォームが POSIX モードをサポートしている場合、所有者のみがアクセスできる権限を使用します。

グローバル設定は、プロファイルおよび認証情報とは分離されています。

```toml
# ~/.ti/.preferences
schema_version = 1

[logging]
enabled = true
max_file_mb = 10
max_files = 5

[telemetry]
enabled = false
```

ドットプレフィックス付きの設定ファイルは任意であり、通常のディレクトリ一覧では非表示になり、すべてのプロファイルに適用されます。新規インストール時および `ti configure` 実行時には、このファイルは作成されません。ユーザーが作成したファイルを読み取っても、その権限、コメント、書式は書き換えられません。

## プロファイルの選択 {#profile-selection}

プロファイル名前空間は、次の順序で選択されます。

1. 明示的な `--profile`
2. `TI_PROFILE`
3. `default`

明示的に空のプロファイルを指定することは無効です。

## TiDB Cloud API 認証情報 {#tidb-cloud-api-credentials}

認証情報の選択順序は次のとおりです。

1. `TIDB_CLOUD_PUBLIC_KEY` と `TIDB_CLOUD_PRIVATE_KEY` のいずれかが設定されている場合は、その両方
2. `~/.ti/credentials` の選択されたセクション

2 つの環境変数は必ずセットで必要です。`ti` は、環境変数側の片方とファイル側の片方を混在させることはありません。

配置先の選択順序は次のとおりです。

1. 明示的なグローバル `--region`
2. `TI_REGION_CODE`
3. プロファイルの `region_code`

コマンドフラグ、環境入力、保存済み設定、およびコマンドのデフォルト値は、フィールドごとに解決されます。そのため、API キーペアのようなアトミックな組み合わせでない限り、値は異なるレベルから取得される場合があります。

## Starter プロジェクトの配置先 {#starter-project-placement}

TiDB Cloud CLI は、プロジェクトセレクターを受け付けず、保存もしません。TiDB Cloud Starter インスタンスの作成ではプロジェクト配置先を省略し、TiDB Cloud がサーバー側のデフォルトプロジェクトを選択します。TiDB Cloud から返されるプロジェクトフィールドおよびラベルは、リソースメタデータとして引き続き表示されますが、後続のリクエストで再利用されることはありません。

## File system 認証情報とリモートインベントリ {#file-system-credentials-and-remote-inventory}

1 つのプロファイルで複数の file system にアクセスできます。リージョン単位のリモートインベントリが、リソースの存在と状態に関する信頼できる情報源です。ローカル状態には、認証情報とそのルーティングヒントのみが保存されます。

```text
~/.ti/fs_credentials/<profile-key>/<file-system-id-key>/credentials
```

この認証情報には、サーバーが割り当てた file system ID、正規のリージョンコード、選択された `api_key`、および任意の正式なトークンメタデータが含まれ、所有者のみがアクセスできる権限を使用します。`ti fs list-file-systems` はリモートリソースを読み取り、機密情報ではない `has_local_token` ヒントのみをテーブル結合します。

1 つのリモート file system に複数のトークンを持たせることはできますが、各プロファイルが file system ごとに保存する選択済みトークンは最大 1 つです。ローカルストアは運用上の選択情報であり、リモートのトークンインベントリのレプリカではありません。プロビジョニングまたは古いインポートによって作成された認証情報には、`token_id`、`scope_kind`、`token_name`、`expires_at`、または `scopes` が含まれていない場合がありますが、それでもデータプレーン用途では有効です。また、`ti` は不足しているメタデータをトークン一覧の行から推測しません。

`ti fs generate-file-system-token` は、`--store-locally` が設定されていない限り、選択済み認証情報を変更しません。`--replace` はローカルの選択のみを変更し、以前のリモートトークンは引き続き有効なままです。ローカル認証情報をソースとするリフレッシュでは、それがアトミックに置き換えられます。フラグまたは `TI_FS_TOKEN` をソースとするリフレッシュでは、置換後のプレーンテキストが返され、ローカル状態には書き込まれません。

`ti fs generate-file-system-scoped-token` はオーナートークンのみを受け付け、その正式なパススコープをローカルに保存できます。トークン JWT 自体には file system ID は含まれますが、トークンの種類、トークン ID、またはスコープは含まれません。そのため、明示的に指定されたトークンまたは環境変数のトークンは、ローカルで分類されるのではなく、認可のためにサービスへ渡されます。`TI_FS_TOKEN` にはオーナートークンまたはスコープ付きトークンのいずれも指定できます。利用可能な操作は、そのサーバー側の能力に依存します。

file system オーナートークンは、file system データアクセスとトークンインベントリまたはライフサイクル操作を認可します。TiDB Cloud Filesystem リソースの作成、一覧表示、詳細表示、削除は認可しません。また、別のオーナートークンを生成することもできません。これらの操作には TiDB Cloud API 認証情報が必要です。さらに、`ti fs delete-file-system` では明示的な `--file-system-id` が必要です。`TI_FS_TOKEN` に埋め込まれた ID が、削除対象の file system 選択に使われることはありません。

リソースの選択順序は次のとおりです。

1. 明示的な `--file-system-id`
2. `TI_FS_FILE_SYSTEM_ID`
3. 明示的に指定された file system トークンから ID を導出
4. それ以外の場合は `fs.missing_file_system_id` で失敗

`ti` は、保存済みデフォルトやローカル認証情報の数から file system を推測することはありません。単一コマンドには `--file-system-id` を、シェル、サンドボックス、または自動化環境には `TI_FS_FILE_SYSTEM_ID` を使用してください。

リモート `fs`、`fs-git`、`fs-journal`、およびオーナー `fs-vault` 操作における FS オーナー認証情報の選択順序は次のとおりです。

1. 明示的な `--fs-token`
2. `TI_FS_TOKEN`
3. 選択されたリソース認証情報

フラグはシェル履歴やプロセス一覧に残る可能性があるため、フラグよりも `TI_FS_TOKEN` を推奨します。

## 設定不要の file system 入力 {#config-free-filesystem-inputs}

クリーンなサンドボックスで必要なのは次の内容だけです。

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="aws-us-east-1"
```

これらの値はメモリ内の名前空間のみを構成します。`ti` はトークンから ID を導出し、どちらの値も `~/.ti/` に書き込みません。`TI_FS_FILE_SYSTEM_ID` は任意ですが、指定する場合はトークンと一致している必要があります。リモート file system のインベントリ、詳細表示、プロビジョニング、および削除には TiDB Cloud API 認証情報が必要です。file system トークンは file system 削除の認可としては不要であり、受け付けられません。

## DB SQL 認証情報 {#db-sql-credentials}

生成される SQL 認証情報はクラスター単位です。

```text
~/.ti/db_users/<cluster-id>/credentials
```

```toml
[read_only]
username = "..."
password = "..."

[read_write]
username = "..."
password = "..."

[admin]
username = "..."
password = "..."
```

`ti db create-db-sql-users` は、これらの安定したユーザーを作成または修復します。これらはメインの認証情報ファイルには保存されません。

3 つのアクセスモードは、TiDB Cloud の組み込みデータベースロールに対応します。

| `ti` access mode | TiDB Cloud built-in role | 想定用途 |
| --- | --- | --- |
| `read_only` | `role_readonly` | データを変更せずにクエリおよび検証を行う |
| `read_write` | `role_readwrite` | アプリケーションデータのクエリおよび変更を行う |
| `admin` | `role_admin` | スキーマ変更を行い、権限を管理する |

TiDB Cloud の完全なロールモデルについては、[データベースユーザーとロールの管理](/tidb-cloud/configure-sql-users.md) を参照してください。

## Companion 状態とマウントロケーター {#companion-state-and-mount-locators}

インストーラーには `ti-drive9` が含まれており、これは `ti fs`、`ti fs-git`、`ti fs-journal`、および `ti fs-vault` の操作を実行する companion runtime です。これを直接呼び出すことはありません。登録された各 file system には、分離された companion home があります。

```text
~/.ti/drive9-home/<profile-key>/<resource-key>/
```

`ti` ワークフローでは、この状態やスタンドアロンの `~/.drive9` 設定を編集しないでください。

バックグラウンドの FS または vault マウントが成功すると、機密情報を含まないロケーターが書き込まれます。

```text
~/.ti/mounts/<mount-hash>.locator.json
```

このロケーターには、同じ `HOME` から drain およびアンマウントを行うために必要な配置先情報と companion-home 情報が記録されます。file system トークンは含まれません。アンマウントが成功すると削除されます。

## 操作ログ {#operation-logs}

`ti` は、ローカルの JSON Lines 形式のイベントを秘匿化して次の場所に書き込みます。

```text
~/.ti/logs/ti.jsonl
```

このログは、テレメトリーではなく、ローカルの監査およびデバッグ用データです。コマンド名、フラグ名、プロファイルとリージョン、所要時間、終了コードと安定したエラーコード、HTTP メソッド/ステータス、操作、およびリクエスト ID を含む場合があります。フラグ値、SQL、ファイルパスとその内容、ペイロード、接続文字列、および認証情報は含まれません。

1 つのプロセスに対して無効にするには、次を実行します。

```bash
TI_LOGGING=off ti db list-db-clusters --db-cluster-type starter
```

または、`~/.ti/.preferences` を作成または編集します。

```toml
schema_version = 1

[logging]
enabled = false
```

環境変数の値 `off`、`false`、`0`、`no` はロギングを無効にし、`on`、`true`、`1`、`yes` は有効にします。環境変数は設定より優先されます。無効な設定値が指定された場合、要求されたコマンドを失敗させることなく、操作ログは無効になります。

既存のインストールで `[logging]` を `~/.ti/config` に保存している場合、それらの値は自動的に `~/.ti/.preferences` に移行されます。この移行では、プロファイルと認証情報は保持されます。`ti update` は、`~/.ti/` 配下の設定、プロファイル、認証情報、操作ログ、またはその他の状態を読み書きしません。

## 匿名テレメトリー {#anonymous-telemetry}

リリースビルドは、対象となるコマンドについて、ベストエフォートで 1 件の完了イベントを TiDB Cloud CLI のテレメトリーサービスに送信します。このイベントには、正規化されたコマンド、明示的に指定されたフラグ名、安定した終了コードとエラーコード、所要時間、リージョン、CLI バージョン、OS、アーキテクチャ、インストール元、およびランダムな仮名化されたインストール ID が含まれます。フラグ値、認証情報、トークン、SQL テキスト、ファイルパスまたはその内容、コマンド出力、API ペイロード、プロファイル名、またはクラウドリソース ID は含まれません。

開発ビルドおよび認識された CI 環境では、デフォルトで無効です。help、version、コマンドなしの使用、およびすべての `ti update` モードは常に除外されます。テレメトリーを永続的に無効にするには、次のグローバル設定を追加します。

```toml
[telemetry]
enabled = false
```

ファイルを変更せずに 1 つのプロセスに対して無効にするには、次を実行します。

```bash
TI_TELEMETRY=off ti db list-db-clusters --db-cluster-type starter
```

TiDB Cloud CLI は、最初の対象イベントに対して `~/.ti/.telemetry-installation-id` を遅延作成し、POSIX 権限が利用可能な場合は現在のユーザーのみに制限します。仮名化された ID をリセットするには、このファイルを削除してください。テレメトリーの配信は損失を伴う可能性があり、コマンド出力、エラー、または終了ステータスを変更することはありません。

統合は、プロファイルやコマンドを変更せずに、明示的なプロセススコープのメタデータを付加できます。`TI_TELEMETRY_TAG` は最大 128 バイトの UTF-8 文字列を受け付けます。`TI_TELEMETRY_EXTRA` は、圧縮後 2 KiB までの完全な JSON 値 1 つを受け付けます。無効なメタデータ、禁止されたメタデータ、深くネストされたメタデータ、またはサイズ超過のメタデータは、コマンドに影響を与えることなく省略されます。どちらの値にも、認証情報、トークン、SQL、パス、個人データ、プロファイル名、またはクラウドリソース ID を含めないでください。

```bash
TI_TELEMETRY_TAG="e2b-preview" \
TI_TELEMETRY_EXTRA='{"campaign":"launch","runtime":"e2b"}' \
ti fs list-files --file-system-id <file-system-id> --path /
```

## 機密情報 {#sensitive-values}

次の値はシークレットとして扱ってください。

- TiDB Cloud API の秘密鍵と公開鍵のペア
- FS オーナートークン
- DB SQL のユーザー名、パスワード、および接続文字列
- 委任された vault トークンとシークレット値

これらをソース管理、チケット、ログ、コマンド例、または保護されていないシェル履歴に保存しないでください。

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud CLI のリージョン、セキュリティ、および制限事項](/ai/ti/reference/ti-regions-security-and-limitations.md)
- [TiDB Cloud CLI のトラブルシューティング](/ai/ti/reference/ti-troubleshooting.md)
