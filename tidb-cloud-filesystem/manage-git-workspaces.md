---
title: TiDB Cloud Filesystem で Git ワークスペースを管理する
summary: マウントされた TiDB Cloud Filesystem に Git リポジトリをクローンし、大規模リポジトリのセットアップを高速化し、リンクされた worktree を管理する方法を学びます。
aliases: ['/ja/ai/manage-git-workspaces']
---

# TiDB Cloud Filesystem で Git ワークスペースを管理する

Git リポジトリを FUSE マウントにクローンし、通常の Git コマンドを使って作業できます。大規模なリポジトリでは、blobless clone を使用すると、すべてのファイル内容のダウンロードが完了する前に作業を開始できます。リンクされた worktree を使うと、再度クローンすることなく、ブランチごとに個別の作業ディレクトリを用意できます。

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- [TiDB Cloud CLI をインストールする](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli)。
- FUSE を通じて [ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md)。Git ワークスペースは WebDAV マウントではサポートされません。
- マウントされたファイルシステムと、必要な権限を持つトークンを `ti` から利用できるようにします。詳細は [既存のファイルシステムにアクセスする](/tidb-cloud-filesystem/access-filesystem.md) を参照してください。
- Git をインストールし、使用するリポジトリの認証を設定します。

このガイドのすべての Git ワークスペースは、マウントされたファイルシステムのパス内に作成されます。

## Git リポジトリをクローンする {#clone-a-git-repository}

リポジトリ URL と、マウントされたディレクトリ内のターゲットパスを指定します。

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb
```

リポジトリは `/path/to/workspace/tidb` にクローンされます。

大規模なリポジトリでは、`--blobless` を使用すると、すべてのファイル内容のダウンロードが完了する前に作業を開始できます。

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless
```

`--blobless` を指定すると、`ti` は最初にリポジトリ構造と Git メタデータをダウンロードします。デフォルトでは、`--hydrate auto` により、作業中に残りのファイル内容がバックグラウンドでダウンロードされます。バックグラウンド hydration を無効にするには、`--hydrate off` を指定します。

クローンコマンドが終了する前にすべてのファイル内容のダウンロードを完了させる必要がある場合は、`--hydrate sync` も指定します。

```shell
ti fs-git clone-git-workspace \
  --repo-url https://github.com/pingcap/tidb.git \
  --target-path /path/to/workspace/tidb \
  --blobless \
  --hydrate sync
```

## blobless ワークスペースのダウンロードを完了する {#finish-downloading-a-blobless-workspace}

リポジトリ内のすべてのファイル内容を必要とするタスクを実行する前に、blobless ワークスペースで残っているダウンロードがあれば完了するまで待機します。

```shell
ti fs-git hydrate-git-workspace \
  --target-path /path/to/workspace/tidb \
  --timeout 30m
```

この処理は hydration と呼ばれ、ファイルの変更を破棄することなく、不足している Git データをダウンロードします。

クローンまたは hydration が失敗した場合は、再試行する前に CLI のエラーと診断ログを確認してください。詳細は [TiDB Cloud Filesystem のトラブルシューティング](/tidb-cloud-filesystem/filesystem-troubleshooting.md) を参照してください。

## リンクされた worktree を作成する {#create-a-linked-worktree}

リポジトリを再度クローンせずに、別のブランチ用の独立した作業ディレクトリが必要な場合は、リンクされた worktree を使用します。新しい worktree は、ベースワークスペースと Git データを共有します。

たとえば、新しい `feature-x` ブランチ用の worktree を作成するには、次のようにします。

```shell
ti fs-git add-git-worktree \
  --base-path /path/to/workspace/tidb \
  --worktree-path /path/to/workspace/tidb-feature \
  --branch-name feature-x
```

worktree の作成後は、`/path/to/workspace/tidb-feature` で通常の Git コマンドを使用できます。

```shell
git -C /path/to/workspace/tidb-feature status
```

特定のコミットで detached worktree を作成する場合など、その他のオプションについては、[`add-git-worktree` コマンドリファレンス](/ai/ti/reference/ti-fs-git-add-git-worktree.md) を参照してください。

## リンクされた worktree を削除する {#remove-a-linked-worktree}

リンクされた worktree が不要になったら、削除します。

```shell
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature
```

リンクされた worktree を削除しても、ベースワークスペースや、他の worktree と共有されている Git データは削除されません。

worktree にコミットされていない変更が含まれている場合、このコマンドは削除を拒否します。worktree を削除する前に、必要な変更をコミットするか、別の方法で保持してください。

コミットされていない変更を破棄してよいと確信できる場合にのみ、`--force` を使用してください。

```shell
ti fs-git remove-git-worktree \
  --worktree-path /path/to/workspace/tidb-feature \
  --force
```

## マシンを離れる前に作業内容を保持する {#preserve-work-before-leaving-a-machine}

`--mount-profile coding-agent` を使用すると、`.git` などの Git メタデータはローカルマシンに保持されます。ローカルでコミットしただけでは、その履歴を別のマシンでリカバリ可能にはできません。ドレインやアンマウントを行っても、このローカル Git メタデータは転送されません。履歴を保持するには、Git リモートへのプッシュ、または以下のメタデータアーカイブのワークフローを使用してください。

一時的なマシンを削除する前に、次を実施してください。

1. 次のいずれかの方法で Git 履歴を保持します。
    - 書き込み可能な Git リモートにコミットしてプッシュします。独立したクローンまたはフェッチから、想定したコミット ID が利用可能であることを確認してください。
    - プッシュできない場合は、リンクされた worktree のベースリポジトリのメタデータを含む、必要なローカル Git メタデータに対して明示的な `--path` 値を指定して [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) を使用します。別の環境で [`unpack-file-system`](/ai/ti/reference/ti-fs-unpack-file-system.md) を使って復元し、コミット ID と作業ファイルを比較してください。パスが変わる場合は、まず [`git worktree repair` で worktree 接続を修復](https://git-scm.com/docs/git-worktree) してください。実行可能な例については、[プッシュしていないワークスペースを別のマシンにリカバリする](#recover-an-unpushed-workspace-to-another-machine) を参照してください。
2. 必要な未追跡ファイルや無視されたファイルは別途保持してください。プッシュで保持されるのはコミット済みの内容だけです。
3. [安全にアンマウントする](/tidb-cloud-filesystem/filesystem-mount.md#unmount-when-you-are-finished)。リカバリ確認が完了するまでは元のディスクを保持してください。

各プロファイルでローカルに保持されるデータについては、[マウントプロファイルとローカルオーバーレイ](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays) を参照してください。

## プッシュしていないワークスペースを別のマシンにリカバリする {#recover-an-unpushed-workspace-to-another-machine}

この例では、リンクされた worktree を含む作業途中の Git ワークスペースを、リモートにプッシュせずに別のマシンへ移動します。ベースリポジトリの Git メタデータと、リンクされた worktree の worktree ごとのメタデータの両方をリモートアーカイブにパックし、2 台目のマシンで復元して worktree リンクを修復し、コミット ID を比較して転送を確認します。

この例では、移行元マシンで `--mount-profile coding-agent` を使用し、このページの前半で説明した次のレイアウトが作成されていることを前提としています。

```text
/path/to/workspace/tidb              (base repository, contains .git/)
/path/to/workspace/tidb-feature      (linked worktree, contains .git file pointing at the base)
```

### 移行元マシンで {#on-the-source-machine}

1. 後で比較できるようにコミット ID を記録します。

    ```shell
    (cd /path/to/workspace/tidb && git rev-parse HEAD) | tee /tmp/tidb-base.sha
    (cd /path/to/workspace/tidb-feature && git rev-parse HEAD) | tee /tmp/tidb-feature.sha
    ```

2. パック前に、キャッシュされた blob が永続化されるよう、書き込みプロセスを停止し、保留中の書き込みをドレインします。

    ```shell
    ti fs drain-file-system --mount-path /path/to/workspace
    ```

3. ローカルオーバーレイにのみ存在する Git メタデータをパックします。`coding-agent` は `.git` をリモート名前空間の外に保持するため、ベースリポジトリの `.git` ディレクトリと、各リンクされた worktree の `.git/worktrees/<name>` サブディレクトリの両方を明示的に指定する必要があります。`.env` や仮想環境など、保持したい未追跡ファイルや無視されたファイルも同じアーカイブに含めてください。`--archive-path` はアーカイブを保存するリモートファイルシステム内のパスです。`/packs/` のように、作業ツリーの外の場所を選んでください。

    ```shell
    ti fs pack-file-system \
      --mount-path /path/to/workspace \
      --mount-profile coding-agent \
      --archive-path /packs/tidb-workspace.tar.zst \
      --path tidb/.git \
      --path tidb/.git/worktrees/tidb-feature \
      --path tidb-feature/.git \
      --path tidb/.env
    ```

    `--path` の値はマウントパスからの相対パスです。保持したいディレクトリまたはファイルごとに `--path` を繰り返し指定してください。指定されていない未追跡ファイルや無視されたファイルは、移行先マシンでは復元されません。

4. [安全にアンマウントする](/tidb-cloud-filesystem/filesystem-mount.md#unmount-when-you-are-finished)。移行先マシンでリカバリが確認されるまでは、ソースディスクを利用可能な状態で保持してください。

### 移行先マシンで {#on-the-target-machine}

1. 宛先パスに、同じプロファイルで同じファイルシステムをマウントします。宛先パスはソースと異なっていてもかまいません。以下の修復手順で、リンクされた worktree に保存されているパスを修正できます。

    ```shell
    mkdir -p /new/path/to/workspace
    ti fs mount-file-system \
      --mount-path /new/path/to/workspace \
      --mount-profile coding-agent \
      --driver fuse
    ```

2. パックしたメタデータを、新しいマウントのローカルオーバーレイに復元します。

    ```shell
    ti fs unpack-file-system \
      --mount-path /new/path/to/workspace \
      --mount-profile coding-agent \
      --archive-path /packs/tidb-workspace.tar.zst
    ```

3. マウントパスがソースから変更されている場合は、その中で Git コマンドを実行する前に、リンクされた worktree の逆参照を修復します。これはベースリポジトリから実行してください。

    ```shell
    cd /new/path/to/workspace/tidb
    git worktree repair /new/path/to/workspace/tidb-feature
    git worktree list
    ```

    `git worktree list` には、新しいパスで `tidb` と `tidb-feature` の両方が表示され、`prunable` マーカーが付いていないことを確認してください。ベースリポジトリも移動している場合は、ベースリポジトリ内で引数なしの `git worktree repair` を実行し、登録されているすべての worktree を更新してください。

4. コミット ID が、移行元マシンで記録したものと一致することを確認します。

    ```shell
    (cd /new/path/to/workspace/tidb && git rev-parse HEAD)
    (cd /new/path/to/workspace/tidb-feature && git rev-parse HEAD)
    ```

    両方の出力は、移行元マシンで取得した対応する `.sha` ファイルと一致している必要があります。どちらかが異なる場合は、ソースディスクを削除しないでください。アーカイブが不完全であり、通常は追加の `--path` 値が原因です。ソース側で不足しているパスを指定して `pack-file-system` を再実行し、もう一度アンパックしてください。

5. 両方のコミット ID が一致し、保持した未追跡ファイルが対象ワークスペースで読み取れることを確認してから、移行元マシンを削除してください。

> **Warning:**
>
> `pack-file-system` は、指定したパスだけをパックします。リンクされた worktree や `.gitignore` されたファイルを自動では検出しません。パック前にリンクされた worktree を追加または削除した場合は、それに合わせて `--path` リストを更新し、各 worktree 自身の `.git` ファイルと、ベースリポジトリ配下の対応する `.git/worktrees/<name>` サブディレクトリを必ず含めてください。

## 次のステップ {#what-s-next}

- blobless clone とバックグラウンド hydration を使用するエージェントワークフローについては、[TiDB Cloud Filesystem 上でエージェント向けの Git ワークスペースを準備する](/ai/ti/guides/ti-git-workspace-for-agents-example.md) を参照してください。
- すべての `ti fs-git` コマンドとオプションについては、[TiDB Cloud Filesystem Git CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-git.md) を参照してください。