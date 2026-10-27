---
title: マシン間でファイルシステムを共有する
summary: 受信者ごとに個別のスコープ付きトークンを使ってマシン間でファイルを共有し、権限を確認して、アクセスを個別に取り消す方法を学びます。
aliases: ['/ja/ai/ti-share-filesystem-across-machines-example']
---

# マシン間でファイルシステムを共有する

TiDB Cloud Filesystem では、環境間でファイルをコピーすることなく、別のユーザー、マシン、CI ジョブ、またはエージェントとファイルを共有できます。受信者ごとに個別のスコープ付きトークンを発行することで、パスと操作ごとにアクセスを制限でき、他の受信者に影響を与えずに特定の受信者のアクセスだけを取り消せます。

このガイドでは、ディレクトリへの読み取り専用アクセスを 24 時間付与し、受信者の権限を確認してから、トークンを取り消す方法を説明します。

> **Note:**
>
> TiDB Cloud Filesystem は現在パブリックプレビューです。機能やインターフェースは予告なく変更される場合があります。

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- 既存のファイルシステム用のオーナートークンを持っており、そのリージョンを把握していること。
- 所有者の環境と受信者の環境の両方に [TiDB Cloud CLI (`ti`)](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli) をインストールしていること。
- スコープ付きトークンを転送するための、シークレットマネージャーなどの安全なチャネルがあること。

Bash または Zsh を使用してください。チュートリアル全体を通して、2 つの別々のシェルを開いたままにします。1 つは信頼できるマシン上でトークンの作成と取り消しを行う **所有者シェル**、もう 1 つはアクセスをテストするための **受信者シェル** です。受信者はオーナートークンや TiDB Cloud API キーを持つ必要はありません。

CI またはエージェントでは、入力プロンプトを実行する代わりに、各環境の `TI_FS_TOKEN` に適切なトークンを注入してください。表示されているとおりにリージョンを設定し、`TI_FS_FILE_SYSTEM_ID` をクリアします。クリーンアップまで、両方の環境で `share_path` を、所有者の環境で `reviewer_token_id` を保持してください。

所有者シェルで、リージョンを設定し、プロンプトでオーナートークンを読み込みます。入力内容は表示されません。

```bash
unset TI_FS_FILE_SYSTEM_ID
export TI_REGION_CODE="<filesystem-region-code>"
printf 'Owner token: '
read -rs TI_FS_TOKEN && export TI_FS_TOKEN && printf '\n'
```

アクセスの取り消しが完了するまで、オーナートークンは `TI_FS_TOKEN` に保持してください。これはファイル操作とトークン管理の両方の認証に使用されます。その他の認証方法については、[ファイルシステムトークンを管理する](/tidb-cloud-filesystem/manage-filesystem-tokens.md#inspect-and-change-token-status) を参照してください。

## 特定のファイルへのアクセスを付与する {#give-access-to-specific-files}

所有者シェルで、次の操作を行います。

1. 一意のディレクトリを作成し、サンプルファイルをアップロードします。

    ```bash
    share_path="/sharing-example-$(date +%s)-$$"
    ti fs create-directory --path "$share_path"
    printf 'Shared review sample\n' | ti fs copy-file \
      --from-stdin --to-remote "$share_path/summary.txt"
    ti fs read-file --path "$share_path/summary.txt"
    ```

    `read-file` の想定出力は `Shared review sample` です。エラーがある場合は、先に解消してから続行してください。

2. このディレクトリに対する読み取りと一覧表示のみを許可するトークンを作成します。

    ```bash
    ti fs generate-file-system-scoped-token \
      --subject reviewer \
      --ttl 24h \
      --allow "$share_path:read,list"
    ```

    返された `fs_token` は安全に保存してください。これは発行時にのみ表示されます。取り消しのために、返された `token_id` も保存します。

    ```bash
    reviewer_token_id="<returned-token-id>"
    ```

3. 安全なチャネルを通じて、スコープ付きトークン、リージョンコード、および `share_path` の正確な値を受信者に送信します。オーナートークンは非公開のままにしてください。マウント経由でファイルを更新した場合は、アクセス情報を送る前に、[更新内容が共有可能な状態になっていることを確認](#make-sure-updates-are-ready-to-share)してください。

受信者ごとに個別のスコープ付きトークンを作成すると、アクセスを個別に取り消せます。その他の権限の組み合わせについては、[ファイルシステムトークンを管理する](/tidb-cloud-filesystem/manage-filesystem-tokens.md) を参照してください。

## 別のマシンから共有ファイルにアクセスする {#access-the-shared-files-from-another-machine}

受信者シェルで、次の操作を行います。

1. リージョンと共有パスを設定し、プロンプトでスコープ付きトークンを読み込みます。

    ```bash
    unset TI_FS_FILE_SYSTEM_ID
    export TI_REGION_CODE="<filesystem-region-code>"
    share_path="<shared-directory-path>"
    printf 'Scoped token: '
    read -rs TI_FS_TOKEN && export TI_FS_TOKEN && printf '\n'
    ```

    所有者から提供されたリージョンと正確なディレクトリパスを使用してください。トークンがファイルシステムを識別するため、ファイルシステム ID や CLI プロファイルをコピーする必要はありません。

2. ディレクトリを一覧表示し、ファイルを読み取ります。

    ```bash
    ti fs list-files --path "$share_path"
    ti fs read-file --path "$share_path/summary.txt"
    ```

    `read-file` の想定出力は `Shared review sample` です。

3. 書き込みと、ディレクトリ外へのアクセスが拒否されることを確認します。

    ```bash
    printf 'This write must be rejected\n' | ti fs copy-file \
      --from-stdin --to-remote "$share_path/denied-write.txt"
    ti fs list-files --path /
    ```

    各コマンドで認可エラーが返ることを想定しています。その他のエラーでは権限を確認したことにはなりません。いずれかの操作が成功した場合は、続行する前にトークンを取り消してください。

所有者シェルで、`ti fs describe-file --path "$share_path/denied-write.txt"` を実行し、ファイルが存在しないことが報告されることを確認します。

### 共有ディレクトリをマウントする（オプション） {#mount-the-shared-directory-optional}

以下のコマンドは Linux FUSE または macFUSE を使用する macOS 向けです。macFUSE がない Mac では、`--driver webdav` を使用し、このコマンドから `--read-only` を省略してください。WebDAV はそのオプションを受け付けません。スコープ付きトークンにより、サービス側では引き続き読み取り専用アクセスが強制されます。[マウントの前提条件](/tidb-cloud-filesystem/filesystem-mount.md#choose-a-mount-method) も参照してください。

受信者シェルで、共有ディレクトリをマウントします。

```bash
review_mount="$(mktemp -d "$HOME/ti-fs-review.XXXXXX")"
ti fs mount-file-system \
  --remote-path "$share_path" \
  --mount-path "$review_mount" \
  --driver fuse \
  --read-only
```

サンプルファイルを読み取ります。

```bash
cat "$review_mount/summary.txt"
```

想定出力は `Shared review sample` です。読み取りに 30 秒以上かかる場合は中断し、[マウントのトラブルシューティング](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs) に従ってください。

スコープ付きトークンにより、サービス側で読み取り専用アクセスが強制されます。FUSE の `--read-only` オプションも、このローカルマウント経由の書き込みをブロックします。

## 更新内容が共有可能な状態になっていることを確認する {#make-sure-updates-are-ready-to-share}

後続のワークフローでマウント経由の書き込みを行う場合は、別のユーザーに渡す前にファイルを閉じ、[安全に書き込みを完了](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely)してください。FUSE の場合は、マウントをドレインするか、正常にアンマウントしてください。WebDAV の場合は通常どおりアンマウントします。ドレインはサポートされていません。更新されたファイルは、直接 `ti fs read-file` リクエストで確認してください。

同じファイルへの同時書き込みは避けてください。変更は自動的にはマージされません。ユーザーごとに分離されたワークスペースが必要な場合は、[レイヤーとチェックポイント](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md) を使用してください。

## 共有アクセスを停止する {#stop-sharing-access}

以下の手順を順番に実行してください。

1. **受信者:** 共有ファイルを使用しているアプリケーションを停止します。ディレクトリをマウントしている場合は、アンマウントします。

    ```bash
    ti fs unmount-file-system --mount-path "$review_mount"
    ```

    手順 3 の確認のため、スコープ付きトークンは設定したままにしてください。

2. **所有者:** 元の所有者シェルで、作成時に保存した ID を使ってトークンを取り消します。

    ```bash
    ti fs delete-file-system-token --token-id "$reviewer_token_id"
    ```

    このコマンドは TiDB Cloud API 認証情報またはオーナートークンのいずれかを受け付けます。オーナートークンは `TI_FS_TOKEN` または `--fs-token` を通じて渡す必要があります。`import-file-system-token` によってローカル認証情報にのみ保存されたオーナートークンはここでは無視され、その場合 `delete-file-system-token` と `list-file-system-tokens` はどちらも API 認証情報を要求して終了コード `3` で終了します。トークンメタデータを確認するには、`ti fs list-file-system-tokens --output text` を使用してください。

3. **受信者:** 認証キャッシュが更新されるまで約 10 秒待ってから、同じスコープ付きトークンで再度読み取りを実行します。

    ```bash
    ti fs read-file --path "$share_path/summary.txt"
    ```

    認証エラーまたは認可エラーが返ることを想定しています。読み取りがまだ成功する場合は、取り消したトークン ID を確認し、キャッシュ間隔の後に再試行してください。ネットワークエラーでは取り消しを確認したことにはなりません。

    取り消しを確認したら、トークンをクリアします。

    ```bash
    unset TI_FS_TOKEN TI_REGION_CODE
    ```

    この例をマウントしていた場合は、`rmdir "$review_mount"` で空のローカルディレクトリを削除してください。

4. **所有者:** サンプルディレクトリを削除し、削除されたことを確認します。

    ```bash
    ti fs delete-file --path "${share_path:?Set the example directory first}" --recursive
    ti fs describe-file --path "$share_path"
    ```

    `describe-file` では not-found エラーが返ることを想定しています。

取り消しによって、ファイルシステム本体や他のトークンはそのまま維持されます。受信者がすでにダウンロードまたはキャッシュしたファイルは消去できません。環境変数をクリアするだけでは、トークンは取り消されません。

## 次のステップ {#what-s-next}

- トークンの作成、ローテーション、無効化、取り消しについては [ファイルシステムトークンを管理する](/tidb-cloud-filesystem/manage-filesystem-tokens.md) を参照してください。
- ベースファイルシステムに適用する前に変更を個別に行う方法については、[TiDB Cloud Filesystem のレイヤーとチェックポイント](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md) を参照してください。
- 共有ファイルシステムデータを使用するワークフローについては、[自動化と AI エージェントのワークフロー](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md) を参照してください。