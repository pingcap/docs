---
title: Docker でファイルシステムをマウントする
summary: FUSE と必要なコンテナ権限を有効にして、Linux ホスト上の Docker コンテナ内にファイルシステムをマウントします。
---

# Docker でファイルシステムをマウントする

Docker コンテナ内から TiDB Cloud Filesystem のファイルシステムをマウントするには、コンテナが Linux ホスト上の FUSE にアクセスできる必要があります。コンテナ内に `fuse3` をインストールすることに加えて、`/dev/fuse` を公開し、マウントを作成する権限をコンテナに付与する必要があります。

このガイドでは、Linux ホスト上の Docker と Docker Compose の両方を扱います。使用している環境で FUSE へのアクセスや必要なコンテナ権限が提供されていない場合は、代わりに `copy-file`、`read-file`、`list-files` などの直接的な `ti fs` コマンドを使用してください。

> **Note:**
>
> TiDB Cloud Filesystem は現在パブリックプレビューです。機能およびインターフェースは予告なく変更される場合があります。

## 前提条件 {#prerequisites}

開始する前に、以下を確認してください。

- `/dev/fuse` が利用可能な Linux の Docker ホストを使用する。
- `/dev/fuse` へのアクセス権と、マウントの作成に必要な capability を付与してコンテナを起動する権限がある。
- 既存のファイルシステムに対するファイルシステムトークンとリージョンコードを用意している。[既存のファイルシステムにアクセスする](/tidb-cloud-filesystem/access-filesystem.md) を参照してください。

Docker Desktop や、管理されたコンテナ環境またはサンドボックス環境では、`/dev/fuse` が公開されていない場合や、必要な権限が許可されていない場合があります。

> **Warning:**
>
> このガイドの例では、コンテナに `SYS_ADMIN` を付与し、`apparmor=unconfined` によって AppArmor プロファイルを無効化しています。これらの設定により、コンテナには標準的な Docker コンテナよりも広い権限が与えられます。
>
> これらは、使用環境のセキュリティポリシーで許可されている場合にのみ使用してください。環境が適切な追加の分離境界を提供していない限り、これらの権限で信頼できないコードを実行しないでください。スコープ付きのファイルシステムトークンによってファイルシステムデータへのアクセスを制限することはできますが、Docker がコンテナに付与する権限自体は減りません。

## コンテナにファイルシステムアクセスを提供する {#provide-file-system-access-to-the-container}

Docker ホスト上で、ファイルシステムトークンとリージョンコードを設定します。

```bash
export TI_FS_TOKEN="<filesystem-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

ファイルシステムトークンはシークレットとして扱ってください。Dockerfile に記述したり、ソース管理にコミットしたりしないでください。

以下の Docker および Docker Compose の例では、これらの環境変数をホストからコンテナに渡します。

## コンテナを起動する {#start-the-container}

Docker または Docker Compose のいずれかを選択してください。

### Docker を使用する {#use-docker}

Docker ホスト上で、FUSE にアクセスできる対話型の Ubuntu コンテナを起動します。

```bash
docker run --rm -it \
  --device /dev/fuse \
  --cap-add SYS_ADMIN \
  --security-opt apparmor=unconfined \
  --env TI_FS_TOKEN \
  --env TI_REGION_CODE \
  ubuntu:24.04 bash
```

このコマンドは次のことを行います。

- ホストの `/dev/fuse` デバイスをコンテナに公開する。
- マウントの作成に必要な capability を付与する。
- ファイルシステムトークンとリージョンコードをコンテナに渡す。

コンテナの起動後、[コンテナ内でインストールしてマウントする](#install-and-mount-inside-the-container) に進んでください。

### Docker Compose を使用する {#use-docker-compose}

または、Docker ホスト上に次の `compose.yaml` ファイルを作成します。

```yaml
services:
  agent:
    image: ubuntu:24.04
    command: ["sleep", "infinity"]
    devices:
      - /dev/fuse:/dev/fuse
    cap_add:
      - SYS_ADMIN
    security_opt:
      - apparmor=unconfined
    environment:
      TI_FS_TOKEN: ${TI_FS_TOKEN:?Set TI_FS_TOKEN}
      TI_REGION_CODE: ${TI_REGION_CODE:?Set TI_REGION_CODE}
```

コンテナを起動し、その中でシェルを開きます。

```bash
docker compose up -d
docker compose exec agent bash
```

その後、以下の手順をコンテナ内で続けて実行します。

## コンテナ内でインストールしてマウントする {#install-and-mount-inside-the-container}

以下の手順はコンテナ内で実行します。これらの手順では、前述の例で使用した `ubuntu:24.04` イメージを使用します。このイメージはデフォルトで `root` として実行されます。

1. `fuse3` と、`ti` のインストールに必要なツールをインストールします。

    ```bash
    apt-get update
    apt-get install -y --no-install-recommends ca-certificates curl fuse3
    ```

2. TiDB Cloud CLI をインストールします。

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

3. 現在のシェルで `ti` を使えるようにし、マウント用のローカルディレクトリを作成します。

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"

    mkdir -p "$HOME/workspace"
    ```

4. ファイルシステムをマウントします。

    ```bash
    ti fs mount-file-system --mount-path "$HOME/workspace"
    ```

    Linux では、`ti` はデフォルトで FUSE を使用します。コマンドが成功すると、`$HOME/workspace` を通じてファイルシステムにアクセスできます。マウントの開始に失敗した場合は、`ti` が報告する診断ログのパスを確認してください。

    ファイルシステムトークンが特定のリモートパスへのアクセスのみを許可している場合は、前述のマウントコマンドの代わりに次のコマンドを使用してください。

    ```bash
    ti fs mount-file-system \
      --remote-path /workspace \
      --mount-path "$HOME/workspace"
    ```

    この例では、リモートの `/workspace` ディレクトリがローカルマウントのルートになります。詳細は、[ファイルシステムの一部だけをマウントする](/tidb-cloud-filesystem/filesystem-mount.md#mount-only-part-of-the-file-system) を参照してください。

    ローカルマウント経由の書き込みを防ぐには、マウントコマンドに `--read-only` を追加します。たとえば、ファイルシステムのルートを読み取り専用でマウントするには、次のようにします。

    ```bash
    ti fs mount-file-system \
      --mount-path "$HOME/workspace" \
      --read-only
    ```

    `--read-only` オプションは、このローカルマウントにのみ影響します。ファイルシステムサービス側で読み取り専用アクセスを強制するには、読み取り専用権限を持つスコープ付きトークンを使用してください。

5. マウントされたファイルシステムにアクセスできることを確認します。

    ```bash
    ls "$HOME/workspace"
    ```

マウントと、それにアクセスするアプリケーションは、同じ OS ユーザーとして実行してください。アプリケーションイメージが非 root ユーザーを使用する場合は、イメージのビルド時に必要なパッケージをインストールし、実行時にアプリケーションユーザーとしてマウントを作成してください。

## アンマウントせずに FUSE の書き込みをフラッシュする {#flush-fuse-writes-without-unmounting}

マウントを維持したまま保留中の書き込みをファイルシステムに反映させる必要がある場合は、まずアプリケーションが対象ファイルに書き込まないようにし、それらのファイルを閉じてください。その後、コンテナ内でマウントを drain します。

```bash
ti fs drain-file-system \
  --mount-path "$HOME/workspace" \
  --timeout 30s
```

drain が成功すると、マウントを維持したまま保留中の書き込みがファイルシステムに到達したことを確認できます。drain がタイムアウトするかエラーを返した場合は、コンテナと Docker ホストをそのまま利用可能な状態に保ち、エラーを解消し、コンテナを停止または削除する前にファイルを確認してください。コマンド構文については、[`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md) を参照してください。

## コンテナを安全に停止する {#stop-the-container-safely}

コンテナを停止または削除する前に、次の手順を実行してください。

1. コンテナ内で、マウントされたディレクトリに書き込みを行っているアプリケーションを停止し、開いているファイルを閉じます。

2. ファイルシステムをアンマウントします。

    ```bash
    ti fs unmount-file-system --mount-path "$HOME/workspace"
    ```

    コンテナを停止または削除する前に、アンマウントが成功するまで待機してください。FUSE のアンマウントが正常に完了すると、保留中の書き込みがフラッシュされます。

3. コンテナを停止します。

    - `docker run --rm -it` で起動した場合は、アンマウントの成功後にシェルを終了します。

        ```bash
        exit
        ```

        `--rm` を付けて起動しているため、Docker はコンテナを自動的に削除します。

    - Docker Compose を使用した場合は、コンテナのシェルを終了してから、Docker ホスト上で次のコマンドを実行します。

        ```bash
        docker compose down
        ```

コンテナを停止または削除しても、リモートファイルシステムやそのデータは削除されません。

> **Warning:**
>
> アンマウントに失敗した場合は、コンテナを停止または削除しないでください。保留中の書き込みが、まだコンテナ内にしか存在していない可能性があります。コンテナは実行したままにして、エラーを解消し、必要なファイルが先にファイルシステムに到達していることを確認してください。

## 次のステップ {#what-s-next}

- 読み取り専用マウント、レイヤーまたはチェックポイントのマウント、およびその他の一般的なマウントオプションについては、[ファイルシステムをマウントする](/tidb-cloud-filesystem/filesystem-mount.md) を参照してください。
- 別のユーザーまたは環境に同じファイルシステムへのアクセスを付与するには、[マシン間でファイルシステムを共有する](/tidb-cloud-filesystem/filesystem-sharing.md) を参照してください。
- 特定のパスや操作へのアクセスを制限するには、[ファイルシステムトークンの管理](/tidb-cloud-filesystem/manage-filesystem-tokens.md) を参照してください。