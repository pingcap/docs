---
title: TiDB Cloud Filesystem でファイルシステムを管理する
summary: TiDB Cloud コンソールまたは TiDB Cloud CLI を使用してファイルシステムを管理し、コンソールで名前を変更し、CLI アクセスを確認する方法を学びます。
aliases: ['/ja/ai/manage-filesystem-resources']
---

# TiDB Cloud Filesystem でファイルシステムを管理する

[TiDB Cloud コンソール](https://tidbcloud.com/) または [TiDB Cloud CLI (`ti`)](/ai/ti/ti-overview.md) を使用して、TiDB Cloud Filesystem 内のファイルシステムを作成、確認、削除できます。コンソールではファイルシステム名の変更も可能で、CLI ではアクセス診断を利用できます。

コマンド構文、フラグ、出力フィールドについては、[`ti fs` コマンドリファレンス](/ai/ti/reference/ti-filesystem.md) を参照してください。

## 前提条件 {#prerequisites}

- [TiDB Cloud コンソール](https://tidbcloud.com/) を使用してファイルシステムを管理するには、コンソールにログインして組織を選択します。
- TiDB Cloud CLI (`ti`) を使用してファイルシステムを管理するには、[CLI でのクイックスタート](/tidb-cloud-filesystem/filesystem-quick-start.md) に従って `ti` をインストールし、アクセスを設定します。

## ファイルシステムを作成する {#create-a-file-system}

TiDB Cloud コンソールまたは TiDB Cloud CLI を使用してファイルシステムを作成できます。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

1. [TiDB Cloud コンソール](https://tidbcloud.com) の左側のナビゲーションペインで組織を選択し、**File Systems** をクリックします。
2. 右上隅で **Create File System** をクリックします。
3. **Create File System** ページで、ファイルシステム名を入力し、**Cloud Provider** と **Region** を選択します。
4. （任意）概要で使用量制限を確認し、編集します。

    使用量制限を編集するには、組織にクレジットカードを追加してください。クレジットカードがない場合、作成時に無料枠の制限は編集できません。詳細は [使用量制限を管理する](/tidb-cloud-filesystem/manage-filesystem-limits.md) を参照してください。

5. **Create** をクリックします。**Your File System is Ready!** ダイアログには、TiDB Cloud CLI のインストールと、macOS または Linux でのファイルシステムのマウントに関する任意の手順が表示されます。マウントコマンド内のデフォルトのオーナートークンは一度だけ表示されるため、ダイアログを閉じる前に安全に保存してください。

</div>

<div label="CLI" value="cli">

ファイルシステムを作成し、準備完了になるまで待機します。

```shell
ti fs create-file-system \
  --display-name agent-workspace \
  --label environment=development \
  --wait
```

出力から、`file_system_id` フィールドでファイルシステム ID を、`fs_token` フィールドでファイルシステムオーナートークンを取得できます。CLI はファイルシステムオーナートークンを自動的にローカルへ保存します。

返された `file_system_id` をコピーし、現在のシェルで以降のコマンドの対象としてそのファイルシステムを選択します。

```shell
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

`TI_FS_FILE_SYSTEM_ID` を設定すると、以降のコマンドでは毎回 `--file-system-id` を指定しなくても対象のファイルシステムを識別できます。データアクセス用コマンドでは、CLI は選択されたファイルシステムに対してローカルに保存されたファイルシステムトークンを使用します。

> **Warning:**
>
> `fs_token` 内のファイルシステムオーナートークンの平文は、トークンが発行されたときにのみ返されます。これをシークレットとして扱い、ログ、issue、ソース管理に公開しないでください。別のマシンでトークンを使用したり、バックアップを保存したりする必要がある場合は、シークレットマネージャーに安全に保存してください。詳細は [ファイルシステムトークンの管理](/tidb-cloud-filesystem/manage-filesystem-tokens.md) を参照してください。

> **Note:**
>
> ファイルシステムのラベルには、認証情報、接続文字列、プライベートパス、個人データを含めないでください。

</div>

</SimpleTab>

## ファイルシステムを一覧表示して確認する {#list-and-inspect-file-systems}

TiDB Cloud コンソールまたは TiDB Cloud CLI を使用して、ファイルシステムを一覧表示し、その詳細を確認できます。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

1. [TiDB Cloud コンソール](https://tidbcloud.com) の左側のナビゲーションペインで組織を選択し、**File Systems** をクリックします。
2. [**File Systems**](https://tidbcloud.com/filesystems) ページで、クラウドプロバイダーとリージョンを選択して、その場所にあるファイルシステムを一覧表示します。**Search Name** または **Status** を使用して一覧を絞り込めます。

ファイルシステムの詳細を表示するには、ファイルシステム名をクリックして概要ページに移動します。

表示名を変更するには、概要ページの右上隅にある **...** をクリックし、**Rename** を選択します。

</div>

<div label="CLI" value="cli">

現在のリージョンで利用可能なファイルシステムを一覧表示します。

```shell
ti fs list-file-systems --output text
```

ファイルシステムのメタデータを表示します。

```shell
ti fs describe-file-system --file-system-id "<file-system-id>"
```

複数のファイルシステムを扱う場合は、次のいずれかの方法で対象のファイルシステムを指定します。

- 個別のコマンドに `--file-system-id "<file-system-id>"` を渡します。
- `TI_FS_FILE_SYSTEM_ID` を設定して、現在のシェルで以降のコマンドの対象ファイルシステムを選択します。

CLI は、ファイルシステム数やローカルに保存された認証情報に基づいてファイルシステムを自動選択しません。

現在の CLI には、作成後にファイルシステムの表示名やラベルを変更するコマンドはありません。これらの値はファイルシステム作成時に選択してください。

</div>

</SimpleTab>

## アクセスを確認する {#check-access}

CLI がファイルシステムにアクセスできるかどうかを確認します。

```shell
ti fs check-file-system --file-system-id "<file-system-id>"
```

結果には、全体の `status` と、ローカル認証情報、エンドポイント選択、バンドルされたファイルシステムランタイム、リモート接続性のチェック結果が含まれます。

- `passed` は、すべてのチェックが成功したことを意味します。
- `warning` または `failed` は、注意が必要なチェックを示します。

一般的なアクセスおよび接続性の問題については、[TiDB Cloud Filesystem のトラブルシューティング](/tidb-cloud-filesystem/filesystem-troubleshooting.md) を参照してください。

## ファイルシステムを削除する {#delete-a-file-system}

TiDB Cloud コンソールまたは TiDB Cloud CLI を使用してファイルシステムを削除できます。

> **Warning:**
>
> ファイルシステムを削除すると、そのリモートデータは完全に削除されます。削除前に、ファイルシステムを使用しているアプリケーションを停止し、アクティブなローカルマウントを正常にアンマウントしてください。保留中の書き込みを安全に完了する方法については、[安全に終了する](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely) を参照してください。

<SimpleTab groupId="console-cli">

<div label="Console" value="console">

1. TiDB Cloud コンソールで、組織の [**File Systems**](https://tidbcloud.com/filesystems) ページを開き、対象ファイルシステムの **Cloud Provider** と **Region** を選択します。
2. 対象ファイルシステムの行で **...** をクリックし、**Delete** を選択します。
3. 確認ダイアログで、要求されたリージョンとファイルシステム名を `region/name` 形式で入力し、**I understand, delete it.** をクリックします。

削除は非同期です。リクエスト送信後、削除が完了するまでファイルシステムは `deleting` ステータスで表示されたままになる場合があります。

</div>

<div label="CLI" value="cli">

ID を指定してファイルシステムを削除します。

```shell
ti fs delete-file-system --file-system-id "<file-system-id>"
```

ファイルシステムの削除は非同期です。サービスがリクエストを受け付けると、CLI はファイルシステムのステータスを `deleting` として報告し、一致するローカル保存済み認証情報を削除します。このステータスは削除が開始されたことを意味し、リモートファイルシステムとそのデータがすでに削除されたことを意味するものではありません。

</div>

</SimpleTab>

## 次のステップ {#what-s-next}

- ファイルシステムアクセスを生成、委任、ローテーション、または取り消すには、[ファイルシステムトークンの管理](/tidb-cloud-filesystem/manage-filesystem-tokens.md) を参照してください。
- ファイルシステムデータのコピー、読み取り、整理、検索を行うには、[ファイルとディレクトリを操作する](/tidb-cloud-filesystem/work-with-filesystem-data.md) を参照してください。
- ローカルディレクトリを通じてリモートファイルにアクセスするには、[ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md) を参照してください。
- コマンド構文、フラグ、出力フィールドについては、[TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md) を参照してください。