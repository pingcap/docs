---
title: TiDB Cloud Filesystem をマウントする
summary: macOS、Linux、またはコンテナ内で TiDB Cloud Filesystem を安全にマウント、使用、drain、アンマウントする方法を学びます。
---

# TiDB Cloud Filesystem をマウントする

TiDB Cloud CLI では、アプリケーションがローカルファイルシステムのパスを通じてリモートデータにアクセスする必要がある場合に、TiDB Cloud Filesystem をマウントできます。

## 前提条件 {#prerequisites}

- [TiDB Cloud CLI をインストールして設定する](/ai/ti/reference/ti-install-configure-update.md)。
- `--file-system-id` を渡す、`TI_FS_FILE_SYSTEM_ID` を設定する、または Filesystem を識別する FS トークンを指定して、Filesystem を選択します。
- `--fs-token`、`TI_FS_TOKEN`、または選択した Filesystem 用に保存されているローカル認証情報を通じて FS トークンを指定します。
- Linux では、FUSE3 をインストールし、`/dev/fuse` へのアクセスを提供します。

## マウントドライバーを選択する {#choose-a-mount-driver}

| プラットフォーム | `--driver auto` | 注記 |
|---|---|---|
| macOS | WebDAV | FUSE サポートを使用するには macFUSE をインストールし、`--driver fuse` を選択します。 |
| Linux | FUSE | WebDAV マウントはサポートされていません。 |
| Windows | サポートされていません | マウントせずに `ti fs` のデータプレーンコマンドを使用します。 |

## Filesystem をマウントする {#mount-the-filesystem}

macOS または Linux では、ローカルパスを作成し、Filesystem をバックグラウンドでマウントします。

```shell
mkdir -p /path/to/workspace
ti fs mount-file-system \
  --file-system-id "<file-system-id>" \
  --mount-path /path/to/workspace
```

CLI はバックグラウンドのマウントプロセスを開始し、drain コマンドとアンマウントコマンドが正しいプロセスを見つけられるように、ローカルのマウントロケーターを書き込みます。

サブツリーを公開するには `--remote-path` を使用し、書き込みを防ぐには `--read-only` を使用します。レイヤーまたは checkpoint をマウントするには、FUSE ドライバーを選択し、[`mount-file-system` リファレンス](/ai/ti/reference/ti-fs-mount-file-system.md)で説明されている適切な layer オプションを渡します。

## コンテナ内でマウントする {#mount-in-a-container}

イメージ内に FUSE3 をインストールするだけでは不十分です。ホストが `/dev/fuse` を公開し、コンテナがマウントを実行できるよう許可されている必要があります。Docker では、次と同等の設定を指定します。

```shell
docker run --rm -it \
  --device /dev/fuse \
  --cap-add SYS_ADMIN \
  --security-opt apparmor=unconfined \
  --env TI_FS_TOKEN \
  --env TI_REGION_CODE \
  --env TI_FS_FILE_SYSTEM_ID \
  <image>
```

Docker Compose では、同じデバイス、ケーパビリティ、セキュリティ、および環境変数の設定を渡します。

```yaml
services:
  agent:
    image: <image>
    devices:
      - /dev/fuse:/dev/fuse
    cap_add:
      - SYS_ADMIN
    security_opt:
      - apparmor=unconfined
    environment:
      TI_FS_TOKEN: ${TI_FS_TOKEN}
      TI_REGION_CODE: ${TI_REGION_CODE}
      TI_FS_FILE_SYSTEM_ID: ${TI_FS_FILE_SYSTEM_ID}
```

> **Warning:**
>
> `SYS_ADMIN` と制限のない AppArmor プロファイルは、コンテナ分離を弱めます。これらは、専用で信頼できるコンテナに対してのみ使用してください。FUSE アクセスを利用できない場合は、マウントせずに `ti fs` のデータコマンドを使用してください。

## Ubuntu 26.04 のマウントパス {#ubuntu-2604-mount-paths}

Ubuntu 26.04 は `/usr/bin/fusermount3` に AppArmor プロファイルを適用します。デフォルトでは、`/workspace` の代わりに、現在のユーザーのホームディレクトリ、`/mnt`、`/media`、`/tmp`、または `/run/user/<uid>` の配下にあるパスを使用してください。

例:

```shell
mkdir -p "$HOME/workspace"
ti fs mount-file-system \
  --file-system-id "<file-system-id>" \
  --mount-path "$HOME/workspace"
```

アプリケーションが `/workspace` を必要とする場合は、次のルールを `/etc/apparmor.d/local/fusermount3` に追加します。

```text
mount fstype=@{fuse_types} options=(nosuid,nodev) options in (ro,rw,noatime,dirsync,nodiratime,noexec,sync) -> /workspace/{,**/},
umount /workspace/{,**/},
```

その後、プロファイルを再読み込みします。

```shell
sudo apparmor_parser -r /etc/apparmor.d/fusermount3
```

関連するエラーについては、[TiDB Cloud CLI のトラブルシューティング](/ai/ti/reference/ti-troubleshooting.md)を参照してください。

## drain またはアンマウントする {#drain-or-unmount}

`unmount-file-system` を実行すると、CLI はマウントを停止する前に、開いているファイルハンドルと保留中の FUSE 処理を自動的にフラッシュします。

```shell
ti fs unmount-file-system --mount-path /path/to/workspace
```

FUSE マウントをオンラインのまま維持しつつ耐久性バリアが必要な場合（たとえば、レイヤーのチェックポイントを作成する前など）は、`drain-file-system` を明示的に実行します。このコマンドは、アンマウントせずに保留中の書き込みをフラッシュし、それらが完了するまで待機します。

```shell
ti fs drain-file-system --mount-path /path/to/workspace --timeout 30s
```

> **Note:**
>
> Drain は FUSE マウントでのみサポートされます。WebDAV マウントでは、通常のファイルクローズ操作を通じて書き込みがフラッシュされます。

> **Warning:**
>
> 書き込みが保留中のまま、またはアンマウントがエラーを返した後に、マシンを停止しないでください。メモリ内の書き込みとローカルのみに存在するオーバーレイファイルが失われる可能性があります。FUSE マウントでは、シャットダウン前に `drain-file-system` を実行して、保留中の書き込みがリモート Filesystem に到達したことを確認してください。WebDAV マウントでは、アプリケーション内でファイルを閉じ、`unmount-file-system` が成功することを確認してください。

## 次のステップ {#what-s-next}

- [TiDB Cloud Filesystem の Layers と Checkpoints を管理する](/ai/ti/guides/manage-filesystem-layers.md)
- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
