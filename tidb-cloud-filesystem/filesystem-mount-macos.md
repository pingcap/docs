---
title: macOS でファイルシステムをマウントする
summary: WebDAV または macFUSE を使用して macOS で TiDB Cloud ファイルシステムをマウントし、ファイルアクセスを確認して安全にアンマウントする方法を学びます。
---

# macOS でファイルシステムをマウントする

macOS では、TiDB Cloud ファイルシステムをローカルディレクトリとしてマウントし、通常使用しているアプリケーションやツールでそのファイルにアクセスできます。次のいずれかのマウント方法を選択してください。

- **WebDAV**: ほとんどのワークフローに推奨されます。追加のマウントソフトウェアは不要です。
- **macFUSE**: レイヤーまたはチェックポイントのマウント、ローカルの読み取り専用マウントの作成、ファイルシステムをアンマウントせずに保留中の書き込みをフラッシュすることをサポートします。[macFUSE](https://macfuse.github.io/) のインストールが必要です。

`--driver` オプションを指定しない場合、TiDB Cloud CLI (`ti`) は macOS では、macFUSE がインストールされていても WebDAV でファイルシステムをマウントします。FUSE を使用するには、`--driver fuse` を指定してください。レイヤーおよびチェックポイントのマウントでは常に FUSE が必要です。このガイドの例では、どのマウント方法が使用されるかが分かるように、`--driver` を明示的に指定しています。

> **Note:**
>
> TiDB Cloud Filesystem は現在パブリックプレビューです。機能およびインターフェースは予告なく変更される場合があります。

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- [TiDB Cloud CLI (`ti`) をインストールする](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- 既存の TiDB Cloud ファイルシステムがあること。まだない場合は、[ファイルシステムを作成して使用する](/tidb-cloud-filesystem/filesystem-quick-start.md#step-3-create-and-use-a-file-system) を参照してください。
- 有効なトークンを使用してファイルシステムにアクセスできるように `ti` が設定されていること。[既存のファイルシステムにアクセスする](/tidb-cloud-filesystem/access-filesystem.md) を参照してください。

    ファイルの一覧表示と読み取りを行うには、トークンにリモートディレクトリに対する `list` および `read` 権限が必要です。ファイルの作成または変更には `write` も必要で、ファイルの削除には `delete` が必要です。以下の WebDAV の確認手順では、オーナートークンまたは 4 つすべての権限を持つスコープ付きトークンを使用します。読み取り専用アクセスについては、[読み取り専用アクセスに WebDAV を使用する](/tidb-cloud-filesystem/filesystem-mount-macos.md#use-webdav-for-read-only-access) を参照してください。

## WebDAV でマウントする {#mount-with-webdav}

ほとんどのワークフローでは、追加のマウントソフトウェアをインストールせずにファイルシステムをマウントできる WebDAV を使用してください。

Bash または Zsh を使用し、WebDAV の手順全体を通して同じシェルを開いたままにしてください。これにより、例で使用する変数を引き続き利用できます。

1. ローカルのマウントディレクトリを準備します。すでに `$HOME/workspace` にファイルシステムがマウントされている場合は、そのディレクトリを再利用する前にアンマウントしてください。

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    次に、ディレクトリが存在しない場合は作成します。

    ```bash
    mkdir -p "$HOME/workspace"
    ```

2. リモートディレクトリを選択し、リモート読み取りを確認するために小さなサンプルファイルをアップロードします。トークンが特定のリモートディレクトリへのアクセスのみを許可している場合は、以下の `/` を `/workspace` などのそのディレクトリに置き換えてください。

    ```bash
    remote_path="/"
    test_file="mount-check-$(date +%s)-$$.txt"
    printf 'Hello from the service\n' | ti fs copy-file \
      --from-stdin --to-remote "${remote_path%/}/$test_file"
    ```

    生成されるファイル名は、既存ファイルの上書きを避けるのに役立ちます。アップロードが成功してから次に進んでください。

3. WebDAV でファイルシステムをマウントします。

    ```bash
    ti fs mount-file-system \
      --remote-path "$remote_path" \
      --mount-path "$HOME/workspace" \
      --driver webdav
    ```

    選択したリモートディレクトリがローカルマウントのルートになります。たとえば、`remote_path="/workspace"` の場合、リモートの `/workspace` ディレクトリには `$HOME/workspace` を通じてアクセスできます。詳細は、[ファイルシステムの一部のみをマウントする](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-file-system) を参照してください。

    マウントはアンマウントするまでバックグラウンドで実行されます。ターミナルを閉じてもアンマウントされません。

4. ファイルを一覧表示し、ローカルマウント経由でアップロードしたサンプルを読み取ります。

    ```bash
    ls "$HOME/workspace"
    cat "$HOME/workspace/$test_file"
    ```

    `cat` の想定出力:

    ```text
    Hello from the service
    ```

    ディレクトリ一覧の表示だけでは、ファイルの読み取りが機能していることは確認できません。ファイル操作に 30 秒以上かかる場合は、Ctrl+C で中断し、続行する前に [マウントは成功するがファイルアクセスがハングする](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs) を参照してください。

    読み取りが成功したら、マウント経由でサンプルファイルを更新します。

    ```bash
    printf 'Hello from macOS\n' > "$HOME/workspace/$test_file"
    ```

5. 完了したら、アプリケーションによるマウント先への書き込みを停止し、開いているファイルを閉じてから、ファイルシステムをアンマウントします。

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    WebDAV は `drain-file-system` をサポートしていません。アンマウントに失敗した場合は、マシンとローカルマウントデータをそのまま保持し、続行する前に [安全に終了する](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely) を参照してください。

6. アンマウントが正常に完了したら、更新内容がサービスに反映されたことを確認します。

    ```bash
    ti fs read-file --path "${remote_path%/}/$test_file"
    ```

    想定出力:

    ```text
    Hello from macOS
    ```

    確認が成功したら、サンプルファイルを削除します。

    ```bash
    ti fs delete-file --path "${remote_path%/}/$test_file"
    ```

アンマウントするとローカルマウントは削除されますが、ファイルシステムやそのデータは削除されません。

> **Note:**
>
> WebDAV または FUSE のいずれを使用していても、Finder でマウント先を参照すると、ファイルシステム内に `.DS_Store` ファイルや `._` 付随ファイルが作成されることがあります。これらのファイルはアンマウント後も残り、ストレージを消費し、ファイル数に含まれ、同じパスにアクセスできるユーザーから見える状態になります。
>
> これらを保持したくない場合は、対応するリモートディレクトリから削除してください。たとえば、ファイルシステムのルートに対しては次のようにします。
>
> ```bash
> ti fs delete-file --path "/.DS_Store"
> ti fs delete-file --path "/._.DS_Store"
> ```

### 読み取り専用アクセスに WebDAV を使用する {#use-webdav-for-read-only-access}

WebDAV は `--read-only` オプションをサポートしていません。

WebDAV 経由で読み取り専用アクセスを強制するには、`read` と `list` 権限のみを持つスコープ付きトークンを使用し、`--read-only` を付けずに通常どおりマウントしてください。サービス側でトークンにより読み取り専用アクセスが強制されます。

例については、[共有ディレクトリをマウントする](/tidb-cloud-filesystem/filesystem-sharing.md#mount-the-shared-directory-optional) を参照してください。

ローカルマウント自体を読み取り専用にする必要がある場合は、`--driver fuse --read-only` を付けて macFUSE を使用してください。

## macFUSE を使用してマウントする {#mount-with-macfuse}

次のような FUSE の機能が必要な場合は、WebDAV ではなく FUSE を使用します。

- レイヤーまたはチェックポイントをマウントする。
- ローカルの読み取り専用マウントを作成する。
- マウントを維持したまま、`drain-file-system` で保留中の書き込みをフラッシュする。

macOS で macFUSE を使用してファイルシステムをマウントするには、次の手順を実行します。

1. [macFUSE](https://macfuse.github.io/) をインストールし、お使いの macOS バージョンで必要なインストール手順またはセキュリティ承認手順を完了します。

    `ti` をインストールしても macFUSE はインストールされません。

2. ローカルのマウントディレクトリを準備します。すでに `$HOME/workspace` にファイルシステムがマウントされている場合は、ディレクトリを再利用する前にアンマウントします。

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    次に、ディレクトリが存在しない場合は作成します。

    ```bash
    mkdir -p "$HOME/workspace"
    ```

3. 必要なリモートディレクトリとアクセスモードに応じて、FUSE のマウントコマンドを選択します。必要に合うコマンドのみを実行してください。

    FUSE でファイルシステムのルートをマウントするには、次を実行します。

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --driver fuse
    ```

    マウントはアンマウントするまでバックグラウンドで実行されます。ターミナルを閉じてもアンマウントされません。

    FUSE マウントと、それにアクセスするアプリケーションは、同じ OS ユーザーとして実行してください。

    トークンが特定のリモートディレクトリへのアクセスのみを許可している場合は、`--remote-path` で指定します。たとえば、ファイルシステムのルートではなく `/workspace` をマウントするには、次を使用します。

    ```bash
    ti fs mount-file-system \
      --remote-path /workspace \
      --mount-path "$HOME/workspace" \
      --driver fuse
    ```

    詳細は、[ファイルシステムの一部のみをマウントする](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-file-system) を参照してください。

    ローカルマウントを読み取り専用にするには、選択したマウントコマンドに `--read-only` を追加します。ファイルシステムのルートを読み取り専用でマウントするには、次を使用します。

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --driver fuse \
      --read-only
    ```

    レイヤーおよびチェックポイントのマウントには FUSE が必要であり、チェックポイントのマウントは常に読み取り専用です。詳細は、[ファイルシステムのレイヤーとチェックポイントを管理する](/tidb-cloud-filesystem/manage-filesystem-layers.md) を参照してください。

4. 作業が完了したら、アプリケーションによるマウント先への書き込みを停止し、開いているファイルを閉じてから、アンマウントします。

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    FUSE のアンマウントが正常に完了すると、保留中の書き込みがフラッシュされます。通常のアンマウントの前に `drain-file-system` を実行する必要はありません。マウントログに `force_quit` または保留中の書き込みが報告された場合は、[FUSE の書き込み動作](/tidb-cloud-filesystem/filesystem-mount.md#fuse-write-behavior) を参照してください。

アンマウントするとローカルマウントは削除されますが、ファイルシステムやそのデータは削除されません。

> **Note:**
>
> WebDAV と FUSE のいずれの場合でも、Finder でマウントを参照すると、ファイルシステム内に `.DS_Store` ファイルと `._` 付随ファイルが作成されることがあります。これらのファイルはアンマウント後も残り、ストレージを消費し、ファイル数に含まれ、同じパスにアクセスできるユーザーから見える状態になります。
>
> これらを保持したくない場合は、対応するリモートディレクトリから削除してください。たとえば、ファイルシステムのルートに対しては次のようにします。
>
> ```bash
> ti fs delete-file --path "/.DS_Store"
> ti fs delete-file --path "/._.DS_Store"
> ```

### アンマウントせずに FUSE の書き込みをフラッシュする {#flush-fuse-writes-without-unmounting}

FUSE マウントを維持したまま保留中の書き込みをファイルシステムに反映させる必要がある場合は、まず対象ファイルへのアプリケーションの書き込みを停止し、それらのファイルを閉じます。その後、マウントを drain します。

```bash
ti fs drain-file-system \
  --mount-path "$HOME/workspace" \
  --timeout 30s
```

drain が正常に完了すると、マウントを維持したまま保留中の書き込みがファイルシステムに到達したことを確認できます。

drain がタイムアウトするかエラーを返した場合は、マウントとマシンを利用可能な状態のままにし、セッションを終了したり、別のユーザーまたは環境で更新内容を利用可能にしたりする前に、エラーを解決してファイルを確認してください。

WebDAV は `drain-file-system` をサポートしていません。コマンド構文については、[`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md) を参照してください。

## マウントの問題をトラブルシューティングする {#troubleshoot-mount-issues}

WebDAV マウントの開始に失敗した場合は、次を確認してください。

- ローカルのマウントディレクトリが存在し、書き込み可能であること。
- 同じローカルディレクトリを別のマウントがすでに使用していないこと。
- 根本原因について、`ti` が報告する診断ログのパスを確認すること。

FUSE マウントの開始に失敗した場合は、次を確認してください。

- macFUSE がインストールされていること。
- macFUSE に必要な macOS のセキュリティ承認を完了していること。
- マウントと、それにアクセスするアプリケーションが同じ OS ユーザーとして実行されていること。
- 同じローカルディレクトリを別のマウントがすでに使用していないこと。
- `ti` が報告する診断ログのパスを確認すること。

ファイル操作に 30 秒以上かかる場合は、Ctrl+C で中断し、[マウントは成功するがファイルアクセスがハングする](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs) を参照してください。

アンマウントに失敗した場合は、エラーを解決し、必要なファイルがファイルシステムに到達したことを確認するまで、マウントプロセスとマシンを実行したままにしてください。保留中の書き込みが残っている可能性がある間は、ローカルのマウントデータを削除しないでください。

その他のマウントエラーについては、[TiDB Cloud Filesystem のトラブルシューティング](/tidb-cloud-filesystem/filesystem-troubleshooting.md) を参照してください。

## 次のステップ {#what-s-next}

- 読み取り専用マウント、ファイルシステムの一部のみのマウント、その他の一般的なマウントオプションについては、[ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md) を参照してください。
- FUSE を通じてレイヤーとチェックポイントを操作するには、[ファイルシステムのレイヤーとチェックポイントを管理する](/tidb-cloud-filesystem/manage-filesystem-layers.md) を参照してください。
- 別のユーザーまたは環境にファイルシステムへのアクセスを提供するには、[マシン間でファイルシステムを共有する](/tidb-cloud-filesystem/filesystem-sharing.md) を参照してください。