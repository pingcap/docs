---
title: TiDB Cloud Filesystem をコンソールから使い始める
summary: TiDB Cloud コンソールでファイルシステムを作成し、コンピュータから接続して、テストファイルを書き込み、コンソールでそのファイルを表示します。
---

# TiDB Cloud Filesystem をコンソールから使い始める

[TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-intro.md) は、アプリケーション、自動化、AI エージェント向けの永続的で共有可能なクラウドファイルシステムです。ファイルは、それを作成したマシンやプロセスに依存せず利用可能な状態が維持されるため、セッションや環境をまたいでワークスペースを再利用できます。

このクイックスタートでは、[TiDB Cloud コンソール](https://tidbcloud.com/) を使用してファイルシステムを作成し、macOS または Linux コンピュータにマウントし、テストファイルを書き込み、コンソールでそのメタデータを確認する方法を説明します。

> **Note:**
>
> TiDB Cloud Filesystem は現在パブリックプレビューです。機能やインターフェースは予告なく変更される場合があります。

## ステップ 1. ファイルシステムを作成する {#step-1-create-a-file-system}

1. TiDB Cloud アカウントを持っていない場合は、[サインアップ](https://tidbcloud.com/free-trial)してください。
2. TiDB Cloud アカウントで [TiDB Cloud コンソール](https://tidbcloud.com/) にログインします。
3. 左側のナビゲーションペインで組織を選択し、**File Systems** をクリックします。
4. 右上隅で **Create File System** をクリックします。
5. **Create File System** ページで、ファイルシステム名を入力し、クラウドプロバイダーとリージョンを選択します。概要に表示される使用量制限を確認します。

    > **Tip:**
    >
    > クレジットカードが登録されていない組織では、ファイルシステムの制限は固定されています。使用量制限を編集するには、組織にクレジットカードを追加してください。詳細は、[TiDB Cloud Filesystem の使用量制限を管理する](/tidb-cloud-filesystem/manage-filesystem-limits.md) を参照してください。

6. **Create** をクリックします。**Your File System is Ready!** ダイアログが表示されたら、次の手順のためにそのダイアログを開いたままにしておきます。

## ステップ 2. ファイルシステムをマウントする {#step-2-mount-the-file-system}

macOS または Linux では、**Your File System is Ready!** ダイアログの手順に従って TiDB Cloud CLI をインストールし、ファイルシステムをマウントします。Windows では、マウントせずにファイルを操作するには [CLI でのクイックスタート](/tidb-cloud-filesystem/filesystem-quick-start.md) に従ってください。

1. TiDB Cloud CLI `ti` をインストールします。

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh
    ```

2. 同じシェルで **Mount Your File System** の下にあるコマンドをコピーして実行します。このコマンドは、`ti` を `PATH` に追加し、`TI_FS_TOKEN` を設定し、`~/tidbcloudfs` ディレクトリを作成して、そのディレクトリにファイルシステムをマウントします。

    > **Note:**
    >
    > - マウントコマンドには、`TI_FS_TOKEN` に [デフォルトのオーナートークン](/tidb-cloud-filesystem/filesystem-authorization.md#owner-tokens) が含まれています。このトークンはファイルシステムへのフルアクセスを許可し、表示されるのは 1 回だけです。安全に保存してください。コマンドやトークンをログ、issue、チャットメッセージ、ソース管理に記載しないでください。
    > - Linux では、マウントに `fuse3` と `/dev/fuse` へのアクセスが必要です。必要に応じて、マウントコマンドを実行する前に [FUSE ユーザースペースツールをインストールする](/tidb-cloud-filesystem/filesystem-mount-linux.md#install-fuse-userspace-tools) を参照してください。

3. **Start Using It** の下にあるコマンドをコピーして実行し、マウントされたディレクトリを一覧表示します。
4. **Done** をクリックして、ファイルシステムの概要を開きます。

概要ページで **Connect** をクリックすると接続ガイダンスを再度開けますが、デフォルトのオーナートークンを後から取得できません。

## ステップ 3. ファイルを書き込み、表示する {#step-3-write-and-view-a-file}

ファイルシステムをマウントした後、マウントされたディレクトリを使用してテストファイルの書き込みと読み取りを行います。

マウントされたディレクトリにファイルを書き込みます。

```bash
echo 'Hello from TiDB Cloud Filesystem' > ~/tidbcloudfs/hello.txt
cat ~/tidbcloudfs/hello.txt
```

ファイルシステムの左側ナビゲーションペインで **Files** をクリックします。ルートディレクトリに `hello.txt` が表示されます。ファイルを検索するか、ファイル名をクリックしてそのメタデータを確認できます。コンソールにはファイル情報が表示されますが、ファイル内容の読み取りやファイルの変更には TiDB Cloud CLI `ti` またはマウントが必要です。

## （オプション）ステップ 4. ファイルシステムをアンマウントする {#optional-step-4-unmount-the-file-system}

マウントされたディレクトリからファイルシステムにアクセスする必要がない場合は、アンマウントできます。

```bash
ti fs unmount-file-system --mount-path ~/tidbcloudfs
```

Linux では、FUSE が正常にアンマウントされるまで書き込みをローカルにバッファすることがあります。アンマウントに失敗した場合は、マシンを離れたりローカルキャッシュを削除したりする前に [安全に終了する](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely) に従ってください。

## 次のステップ {#what-s-next}

- [ファイルシステムを管理する](/tidb-cloud-filesystem/manage-filesystem-resources.md): ファイルシステムの確認、名前変更、削除を行います。
- [ファイルシステムトークンを管理する](/tidb-cloud-filesystem/manage-filesystem-tokens.md): 制限付きアクセスのトークンを作成します。
- [CLI でのクイックスタート](/tidb-cloud-filesystem/filesystem-quick-start.md): CLI のみで作成するワークフローを確認します。