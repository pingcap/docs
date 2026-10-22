---
title: Linux でファイルシステムをマウントする
summary: FUSE ユーザースペースツールをインストールし、Linux でファイルシステムをマウントして、アクセスを確認し、一般的なマウント権限の問題をトラブルシュートします。
---

# Linux でファイルシステムをマウントする

Linux では、TiDB Cloud Filesystem は FUSE を使用して、ローカルディレクトリ経由でファイルシステムのデータを利用できるようにします。ファイルシステムをマウントすると、アプリケーションやツールは通常のローカルファイルパスを使ってファイルシステムにアクセスできます。

> **Note:**
>
> TiDB Cloud Filesystem は現在パブリックプレビューです。機能やインターフェースは予告なく変更される場合があります。

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- [TiDB Cloud CLI (`ti`) をインストールする](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- ファイルシステムとそのトークンを `ti` から利用できるようにします。詳細は [既存のファイルシステムにアクセスする](/tidb-cloud-filesystem/access-filesystem.md) を参照してください。
- `fuse3` パッケージをインストールできる Linux ホストを使用します。コンテナの場合は、代わりに [Docker と Docker Compose](/tidb-cloud-filesystem/filesystem-mount-docker.md) に従ってください。

マウントと、それにアクセスするアプリケーションは、同じ OS ユーザーとして実行してください。

## FUSE ユーザースペースツールをインストールする {#install-fuse-userspace-tools}

1. Ubuntu または Debian では、`fuse3` パッケージをインストールします。

    ```bash
    sudo apt-get update
    sudo apt-get install -y --no-install-recommends fuse3
    ```

2. FUSE のマウントヘルパーがインストールされていることを確認します。

    ```bash
    command -v fusermount3
    ```

    このコマンドは、次のように `fusermount3` へのパスを出力します。

    ```text
    /usr/bin/fusermount3
    ```

3. FUSE デバイスが利用可能であることを確認します。

    ```bash
    ls -l /dev/fuse
    ```

    このコマンドは `/dev/fuse` のエントリを表示します。

`fusermount3` が見つからない場合は、`fuse3` パッケージがインストールされていることを確認してください。`/dev/fuse` が存在しない場合、またはマウント時に使用できない場合は、ホスト管理者に FUSE を有効化し、ユーザーにそのデバイスへのアクセス権を付与するよう依頼してください。

他の Linux ディストリビューションでは、`fusermount3` を提供する FUSE パッケージをインストールし、同じ確認を行ってください。

## ファイルシステムをマウントして確認する {#mount-and-verify-the-file-system}

1. マウント用のローカルディレクトリを作成します。

    ```bash
    mkdir -p "$HOME/workspace"
    ```

    マウントにアクセスするアプリケーションを実行するのと同じ OS ユーザーが所有するディレクトリを使用してください。

2. ファイルシステムをマウントします。

    ```bash
    ti fs mount-file-system --mount-path "$HOME/workspace"
    ```

    Linux では、`ti` はデフォルトで FUSE を使用します。

    このコマンドは、マウントの準備が完了するまで待機してから終了します。コマンド終了後もマウントはバックグラウンドで動作し続けるため、ターミナルを閉じてもアンマウントされません。

    マウントが成功すると、`$HOME/workspace` 経由でファイルシステムにアクセスできます。

    ファイルシステムトークンが特定のリモートパスへのアクセスのみを許可している場合は、前述のマウントコマンドの代わりに次のコマンドを使用してください。

    ```bash
    ti fs mount-file-system \
      --remote-path /workspace \
      --mount-path "$HOME/workspace"
    ```

    この例では、リモートの `/workspace` ディレクトリがローカルマウントのルートになります。詳細は [ファイルシステムの一部のみをマウントする](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-file-system) を参照してください。

    ローカルマウント経由の書き込みを防ぐには、マウントコマンドに `--read-only` を追加します。たとえば、ファイルシステムのルートを読み取り専用でマウントするには、次のようにします。

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --read-only
    ```

    `--read-only` オプションは、このローカルマウントにのみ影響します。ファイルシステムサービス側で読み取り専用アクセスを強制するには、読み取り専用権限を持つスコープ付きトークンを使用してください。

3. マウントされたファイルシステムにアクセスできることを確認します。

    ```bash
    ls "$HOME/workspace"
    ```

    このコマンドは、マウントされたパスのルートにあるファイルとディレクトリを一覧表示します。

    書き込み可能なマウントを使用していて、トークンに書き込み権限がある場合は、テストファイルを作成して読み取ることもできます。

    ```bash
    TEST_FILE="mount-check-$(date +%s).txt"

    printf 'Hello from Linux\n' > "$HOME/workspace/$TEST_FILE"
    cat "$HOME/workspace/$TEST_FILE"
    ```

    出力例:

    ```text
    Hello from Linux
    ```

4. 作業が完了したら、マウントされたディレクトリに書き込みを行っているアプリケーションを停止し、開いているファイルを閉じてから、ファイルシステムをアンマウントします。

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    アンマウントが成功すると、保留中の FUSE 書き込みをフラッシュしてからマウントを停止します。

    上記のテストファイルを作成した場合は、アンマウント後に、そのファイルがファイルシステムから直接利用できることを必要に応じて確認できます。

    ```bash
    ti fs read-file --path "/$TEST_FILE"
    ```

    出力例:

    ```text
    Hello from Linux
    ```

アンマウントするとローカルマウントは削除されますが、ファイルシステムやそのデータは削除されません。

> **Warning:**
>
> アンマウントに失敗した場合は、エラーを解消し、必要なファイルがファイルシステムに到達したことを確認するまで、マウントとマシンを稼働させたままにしてください。一部の保留中の書き込みは、まだそのマシン上にしか存在していない可能性があります。

## アンマウントせずに FUSE 書き込みをフラッシュする {#flush-fuse-writes-without-unmounting}

マウントを維持したまま保留中の書き込みをファイルシステムに到達させる必要がある場合は、まず対象ファイルへの書き込みを行うアプリケーションを停止し、それらのファイルを閉じてください。その後、マウントをドレインします。

```bash
ti fs drain-file-system \
  --mount-path "$HOME/workspace" \
  --timeout 30s
```

ドレインが成功すると、マウントを維持したまま保留中の書き込みがファイルシステムに到達したことを確認できます。ドレインがタイムアウトした場合やエラーを返した場合は、マウントとマシンを利用可能な状態に保ち、エラーを解消し、セッションを終了したり他のユーザーに更新の準備ができたと伝えたりする前に、ファイルを確認してください。コマンド構文については、[`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md) を参照してください。

## マウント権限エラーをトラブルシュートする {#troubleshoot-mount-permission-errors}

マウントが `Permission denied` で失敗する場合は、次の項目を順に確認してください。

1. マウントディレクトリに現在のユーザーの書き込み権限があることを確認します。

    ```bash
    ls -ld "$HOME/workspace"
    ```

2. `/dev/fuse` が存在することを確認します。

    ```bash
    ls -l /dev/fuse
    ```

3. アプリケーションを実行するのと同じ OS ユーザーとしてマウントを作成していることを確認します。

    FUSE マウントを `root` として作成し、その後でマウントディレクトリの所有権を変更して別のユーザーにアクセスさせようとしないでください。代わりに、アプリケーションユーザーとしてマウントを作成してください。

4. 別のマウントがすでに同じパスを使用していないか確認します。

    ```bash
    mount | grep "$HOME/workspace"
    ```

    マウントが表示された場合は、新しいマウントを作成する前に、`ti fs unmount-file-system --mount-path "$HOME/workspace"` または `fusermount3 -u "$HOME/workspace"` でアンマウントしてください。

5. `ti` が診断ログのパスを報告した場合は、そのログを調べて根本的なエラーを確認してください。

AppArmor などの追加のセキュリティ制御があるシステムでは、ディレクトリ権限が正しく見えていても、オペレーティングシステムがマウントを拒否することがあります。

追加のマウントエラーについては、[TiDB Cloud Filesystem のトラブルシューティング](/tidb-cloud-filesystem/filesystem-troubleshooting.md) を参照してください。

## Ubuntu 26.04 のマウントパス制限 {#ubuntu-2604-mount-path-restrictions}

Ubuntu 26.04 では、`fusermount3` の AppArmor プロファイルにより、一部のパスで FUSE マウントができないことがあります。特に、`/workspace` のようなトップレベルディレクトリでは、ファイル権限が正しく見えていても `Permission denied` で失敗する場合があります。

このガイドのコマンドでは、マウントディレクトリとして `/workspace` ではなく `$HOME/workspace` を使用してください。

`/workspace` の所有者を変更したり、`root` としてマウントを実行したりしても、AppArmor の制限は回避できません。

アプリケーションで `/workspace` が必須の場合は、ホスト管理者に依頼して `/etc/apparmor.d/local/fusermount3` でそのパスを許可してもらってください。

```text
mount fstype=@{fuse_types} options=(nosuid,nodev) options in (ro,rw,noatime,dirsync,nodiratime,noexec,sync) -> /workspace/{,**/},
umount /workspace/{,**/},
```

その後、管理者は AppArmor プロファイルをリロードできます。

```shell
sudo apparmor_parser -r /etc/apparmor.d/fusermount3
```

プロファイルの更新後、`/workspace` で再度マウントを試してください。

AppArmor が失敗の原因かどうかを確認する方法については、[Ubuntu 26.04 で `/workspace` 配下の FUSE マウントが拒否される](/tidb-cloud-filesystem/filesystem-troubleshooting.md#ubuntu-2604-rejects-a-fuse-mount-under-workspace) を参照してください。

## 次のステップ {#what-s-next}

- 読み取り専用マウント、レイヤーまたはチェックポイントのマウント、およびその他の共通のマウントオプションについては、[ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md) を参照してください。
- レイヤーまたはチェックポイントをマウントして操作する方法については、[ファイルシステムのレイヤーとチェックポイントを管理する](/tidb-cloud-filesystem/manage-filesystem-layers.md) を参照してください。
- 別のユーザーまたは環境にファイルシステムへのアクセスを提供する方法については、[マシン間でファイルシステムを共有する](/tidb-cloud-filesystem/filesystem-sharing.md) を参照してください。